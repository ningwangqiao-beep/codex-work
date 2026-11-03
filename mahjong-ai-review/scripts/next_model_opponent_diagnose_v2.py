"""Frozen predictions and train-only structural-wait baselines. No fitting on aux."""
import collections,hashlib,json,pathlib,random,sys
import torch
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from training.next_opponent_pipeline import records,read,sha,collate,losses
from models.next_opponent import FAMILIES
from evaluation.metrics import binary_metrics
from inference.v3_observation import encode_observation

def examples(row):
 o=row['observation'];observer=o['observer_player'];known=[round((row['state_features'][t]+row['state_features'][27+t])*4) for t in range(27)]
 for k in range(3):
  q=(observer+k+1)%4;missing=o['declared_missing_suits'][q]
  if row['target_active'][k] and row['structural_tenpai'][k]:
   for tile in range(27):yield {'game_id':str(row['game_id']),'seed':row['seed'],'turn':o['turn_index'],'opponent_index':k,'absolute_target':q,'observer':observer,'missing':missing,'tile':tile,'known':known[tile],'label':row['structural_waits'][k][tile],'forbidden':tile//9==missing}
def metric(p,y):return binary_metrics(p,y) if p else None
def main():
 torch.set_num_threads(2);train=read(ROOT/'datasets/next_history1000/manifest.json');aux=read(ROOT/'datasets/next_aux_validation100/manifest.json');counts=collections.Counter();tables={k:collections.defaultdict(lambda:[0,0]) for k in ('tile','missing_tile','missing_tile_known')};train_examples=0;train_positive=0;train_opponents=0;audit=collections.Counter()
 for row in records(train['shards']['train']):
  train_opponents+=sum(a and b for a,b in zip(row['target_active'],row['structural_tenpai']))
  for e in examples(row):
   train_examples+=1;train_positive+=e['label']
   for name,key in [('tile',e['tile']),('missing_tile',(e['missing'],e['tile'])),('missing_tile_known',(e['missing'],e['tile'],e['known']))]:tables[name][key][0]+=e['label'];tables[name][key][1]+=1
 rows=list(records(aux['shards']['auxiliary']));wait_examples=[];expected={k:[] for k in ('structural_tenpai','conditional_structural_wait','legal_any_winner_risk','legal_multiwinner_risk')}
 for row in rows:
  o=row['observation'];p=o['observer_player'];encoding=encode_observation(o);assert encoding['state_features']==row['state_features'] and encoding['history_tokens']==row['history_tokens'];audit['encoder_rows_exact']+=1
  assert row['target_active']==[int(o['active'][(p+k+1)%4]) for k in range(3)]
  for k in range(3):
   waits=row['structural_waits'][k];assert len(waits)==27 and all(y in (0,1) for y in waits);assert bool(any(waits))==bool(row['structural_tenpai'][k]);assert row['target_active'][k] or not any(waits)
   if row['target_active'][k]:
    expected['structural_tenpai'].append((int(row['structural_tenpai'][k]),str(row['game_id'])))
    if row['structural_tenpai'][k]:expected['conditional_structural_wait'].extend((int(y),str(row['game_id'])) for y in waits)
  for t,legal in enumerate(row['legal_mask']):
   if legal:
    label=int(row['joint_winner_mask'][t]);expected['legal_any_winner_risk'].append((int(label!=0),str(row['game_id'])));expected['legal_multiwinner_risk'].append((int(label.bit_count()>1),str(row['game_id'])))
  for e in examples(row):
   assert not(e['forbidden'] and e['label']);assert 0<=e['known']<=4;wait_examples.append(e);audit['conditional_wait_elements']+=1;audit['conditional_wait_positive']+=e['label'];audit['forbidden_wait_elements']+=e['forbidden'];audit['positive_at_four_known_physical_copies']+=e['label'] and e['known']==4
  for t,mask in enumerate(row['joint_winner_mask']):assert mask==sum((1<<k) for k in range(3) if row['target_active'][k] and row['structural_waits'][k][t])
 audit['relative_joint_masks_exact']=len(rows)
 y=[e['label'] for e in wait_examples];global_prior=train_positive/train_examples;expected_count=train_positive/train_opponents;baseline={k:[] for k in ('train_global','train_tile_prior','public_missing_uniform','train_tile_prior_plus_missing_zero','train_missing_tile_known_prior','public_missing_unknown_copy_weight')}
 per_case={}
 for e in wait_examples:
  case=(e['game_id'],e['turn'],e['opponent_index']);per_case.setdefault(case,[]).append(e)
 for case,items in per_case.items():
  weights=[0 if e['forbidden'] else 4-e['known'] for e in items];total=sum(weights)
  for e,weight in zip(items,weights):
   tile=e['tile'];forbidden=e['forbidden'];positive,n=tables['tile'][tile];tileprior=(positive+1)/(n+2);positive2,n2=tables['missing_tile_known'][(e['missing'],tile,e['known'])]
   baseline['train_global'].append(global_prior);baseline['train_tile_prior'].append(tileprior);baseline['public_missing_uniform'].append(0 if forbidden else expected_count/18);baseline['train_tile_prior_plus_missing_zero'].append(0 if forbidden else tileprior);baseline['train_missing_tile_known_prior'].append(0 if forbidden else (positive2+1)/(n2+2));baseline['public_missing_unknown_copy_weight'].append(expected_count*weight/total if total else 0)
 models={};predictions={};reconstruction={}
 for family in FAMILIES:
  path=ROOT/f'reports/next_c_opponent1000_v1_{family}_aux100.json';report=read(path);pred=pathlib.Path(report['prediction_artifact']['path']);assert sha(pred)==report['prediction_artifact']['sha256'];tasks=collections.defaultdict(list)
  with pred.open(encoding='utf-8') as stream:
   for line in stream:
    item=json.loads(line);tasks[item['task']].append(item)
  rebuilt={}
  for task,items in tasks.items():
   assert [(x['label'],x['game_id']) for x in items]==expected[task];rebuilt[task]=metric([x['probability'] for x in items],[x['label'] for x in items])
   for key,value in rebuilt[task].items():
    prior=report['metrics'][task][key];assert value==prior or value is not None and prior is not None and abs(value-prior)<1e-7
  reconstruction[family]={'all_tasks_saved_prediction_label_order_exact':True,'all_metrics_reproduced':True,'prediction_sha256':sha(pred)};prob=[x['probability'] for x in tasks['conditional_structural_wait']];predictions[family]=prob;projected=[0 if e['forbidden'] else p for p,e in zip(prob,wait_examples)];forbidden=[i for i,e in enumerate(wait_examples) if e['forbidden']];allowed=[i for i,e in enumerate(wait_examples) if not e['forbidden']]
  groups={}
  for name,select in [('allowed_suits',allowed),*[(f'target_missing_{s}',[i for i,e in enumerate(wait_examples) if e['missing']==s]) for s in range(3)],*[(f'relative_opponent_{k}',[i for i,e in enumerate(wait_examples) if e['opponent_index']==k]) for k in range(3)]]:groups[name]=metric([prob[i] for i in select],[y[i] for i in select])
  models[family]={'raw_metrics':rebuilt,'missing_zero_rule_projection':metric(projected,y),'forbidden_mean_probability':sum(prob[i] for i in forbidden)/len(forbidden),'allowed_mean_probability':sum(prob[i] for i in allowed)/len(allowed),'fraction_predicted_wait_mass_on_forbidden_suit':sum(prob[i] for i in forbidden)/sum(prob),'forbidden_probability_above_0_1':sum(prob[i]>.1 for i in forbidden),'groups':groups}
 baseline_metrics={name:metric(p,y) for name,p in baseline.items()};allowed=[i for i,e in enumerate(wait_examples) if not e['forbidden']];baseline_allowed={name:metric([p[i] for i in allowed],[y[i] for i in allowed]) for name,p in baseline.items()}
 # Test conditional-loss mask semantics independently without changing any model.
 sample=rows[:2];_,t=collate(sample,'cpu','counts');fake={'structural_tenpai_logits':torch.zeros(2,3,requires_grad=True),'conditional_structural_wait_logits':torch.zeros(2,3,27,requires_grad=True),'legal_candidate_joint_logits':torch.zeros(2,27,8,requires_grad=True)};t['structural_tenpai'].zero_();t['structural_tenpai'][0,0]=1;t['target_active'][0,0]=1;losses(fake,t)['conditional_structural_wait_bce'].backward();grad=fake['conditional_structural_wait_logits'].grad;assert grad[0,0].abs().sum()>0 and grad[1].abs().sum()==0 and grad[0,1:].abs().sum()==0
 result={'scope':'read_only_saved_predictions_and_train_only_baselines_NO_aux_fit_NO_training','source_sha256':sha(__file__),'train_manifest_sha256':sha(ROOT/'datasets/next_history1000/manifest.json'),'aux_manifest_sha256':sha(ROOT/'datasets/next_aux_validation100/manifest.json'),'audit':dict(audit),'conditional_mask_synthetic_gradient_test_passed':True,'train_prior_fit':{'conditional_elements':train_examples,'positive':train_positive,'true_tenpai_opponent_examples':train_opponents,'global_prior':global_prior,'expected_structural_wait_count':expected_count},'prediction_reconstruction':reconstruction,'models':models,'train_only_baselines':baseline_metrics,'baselines_allowed_suits_only':baseline_allowed,'semantics':['opponent target k maps to absolute(observer+k+1)%4; static missing features remain absolute seat order','sample() derives structural waits via winning(hidden_hand+[tile],missing,melds); opponent truth is labels only','positive wait cannot be missing suit, inactive opponent wait zero, joint bit k matches same structural wait channel','known4 means own+public physical copies, not live wall availability; structural counterfactual labels can include these dead-in-unknown-pool waits','winning validation constrains opponent own fifth copy but not other visible players copies; no public-effective claim','flat81 head has no explicit per-opponent missing-zero architecture constraint; postprocessing zeroing is programmed rule ability, not learned improvement','all baseline priors fitted on1000train only; aux labels never used for model fit/calibration/selection','conditional wait AUC pooled across27tiles includes trivially impossible missing suit negatives; allowed-only metrics expose finer discrimination'],'next_experiment_proposal':'Same1000train seed42 6epoch budget: original flat81 control versus shared per-opponent/per-tile scoring head with explicit relative-target missing suit and own/public tile counts; distinguish rule-masked projection from trainable benefit, retain other heads/losses, do not expand epochs/data. Need new independent auxiliary seed range before confirmatory comparison; current aux diagnostic is exploratory.'}
 out=ROOT/'reports/next_c_opponent_diagnose_v2.json';out.write_text(json.dumps(result,indent=2));print(json.dumps({'audit':dict(audit),'baseline_metrics':baseline_metrics,'model_wait':{n:{'auc':d['raw_metrics']['conditional_structural_wait']['roc_auc'],'projected_auc':d['missing_zero_rule_projection']['roc_auc'],'forbidden_mean':d['forbidden_mean_probability'],'forbidden_mass':d['fraction_predicted_wait_mass_on_forbidden_suit']} for n,d in models.items()}},indent=2))
if __name__=='__main__':main()

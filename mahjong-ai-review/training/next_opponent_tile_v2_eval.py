"""Auxiliary100 uncalibrated final-only evaluation, never used inside trainer."""
import json,pathlib,random,torch
from models.next_opponent_tile_v2 import SharedTileOpponent as OpponentAblation
from training.next_opponent_tile_v2_gate import validate
from training.next_opponent_tile_v2_pipeline import read,sha,batches,constrained_joint_logits
from evaluation.metrics import binary_metrics

def summarize(items):
 return binary_metrics([x[0] for x in items],[x[1] for x in items]) if items else {'n':0,'positive':0,'roc_auc':None,'average_precision':None,'brier':None,'log_loss':None,'ece':None}
def evaluate(checkpoint,manifest,auxiliary,admission,output,root):
 out=pathlib.Path(output)
 predictions=out.with_suffix('.predictions.jsonl')
 if out.exists() or predictions.exists():raise ValueError('Completed evaluation output immutable')
 audit=validate(manifest,auxiliary,admission,root);s=torch.load(checkpoint,map_location='cpu',weights_only=False)
 if s.get('version')!='NEXT-OPPONENT-SHARED-TILE-v2' or s.get('epoch')!=5 or s.get('epoch_complete') is not True or s['audit']!=audit:raise ValueError('Only bound fixed final epoch5 checkpoint accepted')
 torch.set_num_threads(2);family=s['config']['family'];model=OpponentAblation(family);model.load_state_dict(s['model']);model.eval();aux=read(auxiliary);values={k:[] for k in ('structural_tenpai','conditional_structural_wait','legal_any_winner_risk','legal_multiwinner_risk')};by_phase={};by_tile={};gaps=[];joint_nll=[]
 with torch.inference_mode():
  for rows,inp,t in batches(aux['shards']['auxiliary'],'cpu',family,128):
   o=model(*inp);p=o['structural_tenpai_logits'].sigmoid();w=o['conditional_structural_wait_logits'].sigmoid();j=constrained_joint_logits(o,t).softmax(-1);marginal=torch.stack([j[:,:,[c for c in range(8) if c&(1<<k)]].sum(-1) for k in range(3)],1)
   for i,r in enumerate(rows):
    gid=str(r['game_id']);phase='turn_'+str((r['observation']['turn_index']//50)*50);phasevals=by_phase.setdefault(phase,{k:[] for k in values})
    def push(task,prob,label):
     item=(float(prob),int(label),gid);values[task].append(item);phasevals[task].append(item)
    for k,active in enumerate(r['target_active']):
     if not active:continue
     push('structural_tenpai',p[i,k],r['structural_tenpai'][k])
     if r['structural_tenpai'][k]:
      for tile in range(27):push('conditional_structural_wait',w[i,k,tile],r['structural_waits'][k][tile])
    for tile,legal in enumerate(r['legal_mask']):
     if not legal:continue
     label=int(r['joint_winner_mask'][tile]);risk=1-j[i,tile,0];multi=j[i,tile,[3,5,6,7]].sum();push('legal_any_winner_risk',risk,label!=0);push('legal_multiwinner_risk',multi,label.bit_count()>1);by_tile.setdefault(str(tile),[]).append((float(risk),int(label!=0),gid));joint_nll.append(float(-j[i,tile,label].clamp_min(1e-9).log()))
     for k,active in enumerate(r['target_active']):
      if active:gaps.append(float((marginal[i,k,tile]-p[i,k]*w[i,k,tile]).abs()))
 intervals={};rng=random.Random(42)
 for task,items in values.items():
  grouped={}
  for prob,label,gid in items:grouped.setdefault(gid,[]).append((prob,label,gid))
  groups=list(grouped.values());scores=[]
  for _ in range(300):
   sampled=[item for group in rng.choices(groups,k=len(groups)) for item in group];scores.append(summarize(sampled))
  intervals[task]={}
  for metric in ('brier','log_loss','roc_auc','average_precision'):
   v=sorted(x[metric] for x in scores if x[metric] is not None);intervals[task][metric]={'ci95':[v[int(.025*len(v))],v[min(len(v)-1,int(.975*len(v)))]] if v else None,'valid_bootstraps':len(v)}
 report={'scope':'reused_auxiliary100_DEVELOPMENT_only_no_calibration_no_final','family':family,'programmed_rule_constraint':'declared_missing_suit_hard_zero_only_NOT_learned; no public-dead hard zero','auxiliary_role':'reused_DEVELOPMENT_not_independent_final','checkpoint_sha256':sha(checkpoint),'checkpoint_epoch':5,'parameters':sum(p.numel() for p in model.parameters()),'audit':audit,'metrics':{k:summarize(v) for k,v in values.items()},'game_bootstrap95ci':intervals,'by_public_turn_bucket':{g:{k:summarize(v) for k,v in tasks.items()} for g,tasks in by_phase.items()},'risk_by_tile':{g:summarize(v) for g,v in by_tile.items()},'joint_nll':sum(joint_nll)/len(joint_nll),'probability_consistency_diagnostic':{'mean_abs_joint_opponent_marginal_minus_tenpai_times_conditional_wait':sum(gaps)/len(gaps),'max_abs_difference':max(gaps),'coherent_probability_claimed':False},'limitations':['52risk positives in20games is small; reused-development auxiliary results are not independent strength or population-generalization proof','structural/legal-hand waits are not publicly available effective waits','conditional wait metric uses true structural-tenpai labels; not unconditional discard risk','multiwinner0positive: AUC/AP NA; Brier/logloss dominated by negatives do not validate tails','joint inactive-opponent classes masked using public active state; cross-head semantic consistency remains diagnostic','no temperature fitting/calibration/threshold selection; fixed final epoch5 only']}
 if validate(manifest,auxiliary,admission,root)!=audit:raise ValueError('Source/data/admission changed during evaluation')
 with predictions.open('x',encoding='utf-8') as log:
  for task,items in values.items():
   for probability,label,game_id in items:log.write(json.dumps({'task':task,'probability':probability,'label':label,'game_id':game_id})+'\n')
 report['prediction_artifact']={'path':str(predictions),'sha256':sha(predictions),'purpose':'paired per-game comparative metrics without reevaluating or calibrating models'}
 out.write_text(json.dumps(report,indent=2));print(json.dumps({'family':family,'metrics':report['metrics'],'checkpoint_sha256':report['checkpoint_sha256']},indent=2));return report

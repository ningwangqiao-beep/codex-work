"""Read-only frozen100/1000 coverage and validation diagnostics; no development/final input."""
import collections, hashlib, json, pathlib, random, statistics, sys
import torch
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from models.next_relative_v3 import RelativeV3ActionValueNet
from training.next_scale_supervised import records as shard_records,collate
from training.next_relative_supervised import records as flat_records
def records(paths):return shard_records(paths) if isinstance(paths,list) else flat_records(paths)

def free(r):
 o=r['observation'];return not any(t//9==o['declared_missing_suits'][o['observer_player']] for t in o['observer_hand'])
def teacher(r):return max((i for i,v in enumerate(r['legal_mask']) if v),key=lambda i:r['action_targets'][i])
def family(x):return 'seven_pairs_strict' if x[10] and x[2]<x[1] else 'seven_pairs_tied' if x[10] and x[2]==x[1] else 'standard'
def progress(r):return 'history_'+str((len(r['history_tokens'])//50)*50)
def coverage(paths):
 c=collections.Counter();sh=collections.Counter();families=collections.Counter();phases=collections.Counter();ties=collections.Counter();sigs=set();games=set();values=[]
 for r in records(paths):
  c['states']+=1;games.add(r['game_id']);c['free']+=free(r);legal=[i for i,v in enumerate(r['legal_mask']) if v];x=r['candidate_features'][teacher(r)];sh[str(round(x[3]*8))]+=1;families[family(x)]+=1;phases[progress(r)]+=1;ties[str(sum(r['action_targets'][t]==1 for t in legal))]+=1
  sigs.add(hashlib.sha256(json.dumps([r['state_features'],r['candidate_features']],separators=(',',':')).encode()).hexdigest());values.append(r['state_target'])
  for k,active in enumerate(r['target_active']):
   if active:
    c['active_opponents']+=1;c['structural_tenpai_positive']+=int(r['structural_tenpai'][k])
    if r['structural_tenpai'][k]:c['conditional_wait_elements']+=27;c['conditional_wait_positive']+=sum(r['structural_waits'][k])
  for t in legal:
   mask=int(r['joint_winner_mask'][t]);c['legal_risk_candidates']+=1;c['risk_positive']+=mask!=0;c['multi_winner_positive']+=mask.bit_count()>1
 return {'counts':dict(c),'games':len(games),'distinct_own_public_candidate_signatures':len(sigs),'teacher_postdiscard_structural':dict(sh),'teacher_family':dict(families),'history_length_buckets':dict(phases),'teacher_optimal_tie_count':dict(ties),'state_target_mean':statistics.mean(values),'state_target_std':statistics.pstdev(values),'state_target_range':[min(values),max(values)]}
def load(path):
 s=torch.load(path,map_location='cpu',weights_only=False);m=RelativeV3ActionValueNet(**{k:s['model_config'][k] for k in ('state_dim','candidate_dim','hidden')});m.load_state_dict(s['model']);return m.eval(),{'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'epoch':s['epoch'],'optimizer_steps':s['optimizer_steps']}
def bootstrap(groups,index):
 rng=random.Random(42);v=list(groups.values());out=[]
 for _ in range(2000):
  sample=rng.choices(v,k=len(v));out.append(sum(x[index] for x in sample)/sum(x[2] for x in sample))
 out.sort();return [out[50],out[1949]]
def diagnose():
 torch.set_num_threads(2);old=json.loads((ROOT/'datasets/next_history100/manifest.json').read_text());new=json.loads((ROOT/'datasets/next_history1000/manifest.json').read_text());result={'scope':'frozen teacher-fit/train-validation diagnosis only; no training, no development or final selection','coverage':{'100_train':coverage(old['files']['train']),'1000_train':coverage(new['shards']['train']),'added900_train':coverage([p for p in new['shards']['train'] if int(pathlib.Path(p).parent.name)>=7000100]),'fixed_validation':coverage(old['files']['validation'])}}
 models={};bindings={}
 for name,directory in [('relative100','next_history100_relative_pairwise'),('scale1000','next_history1000_relative_pairwise')]:
  base=ROOT/'checkpoints'/directory;best=json.loads((base/'BEST.json').read_text());models[name],bindings[name]=load(base/best['checkpoint'])
  epochs=[json.loads(line) for line in (base/'metrics.jsonl').read_text().splitlines()];entry=next(x for x in epochs if x['epoch']==best['epoch']);bindings[name]['best_validation']=entry['validation'];weights={'action_value_mse':1,'pairwise_preference':1,'state_value_mse':.01,'tenpai_bce':.2,'conditional_wait_bce':.2,'joint_risk_ce':.2};bindings[name]['weighted_train_head_losses']={k:entry['train_head_loss'][k]*v for k,v in weights.items()}
 groups={n:{} for n in models};paired={};examples=[]
 rows=list(records(old['files']['validation']))
 with torch.inference_mode():
  for start in range(0,len(rows),64):
   batch=rows[start:start+64];inp,target,_=collate(batch,'cpu');choices={name:model(*inp)['masked_action_value'].argmax(-1).tolist() for name,model in models.items()}
   for j,r in enumerate(batch):
    t=teacher(r);tx=r['candidate_features'][t];g=['all','free' if free(r) else 'forced','structural:'+str(round(tx[3]*8)),'family:'+family(tx),progress(r)];vals={}
    for name in models:
     a=choices[name][j];ax=r['candidate_features'][a];regret=r['action_targets'][t]-r['action_targets'][a];vals[name]=(int(regret==0),regret)
     for key in g:
      q=groups[name].setdefault(key,collections.Counter());q['n']+=1;q['equivalent']+=regret==0;q['exact_tile']+=a==t;q['rank_regret_sum']+=regret;q['higher_missing_debt']+=ax[4]>tx[4];q['higher_structural']+=ax[3]>tx[3];q['outside_calculator_prefilter']+=not bool(ax[11]);q['lower_effective']+=ax[5]<tx[5];q['family_change']+=family(ax)!=family(tx)
    if free(r):
     q=paired.setdefault(r['game_id'],[0.,0.,0]);q[0]+=vals['scale1000'][0]-vals['relative100'][0];q[1]+=vals['scale1000'][1]-vals['relative100'][1];q[2]+=1
     if vals['scale1000'][0]!=vals['relative100'][0]:examples.append({'seed':r['seed'],'turn':r['observation']['turn_index'],'teacher':t,'relative100':choices['relative100'][j],'scale1000':choices['scale1000'][j],'teacher_family':family(tx),'teacher_structural':round(tx[3]*8),'history_length':len(r['history_tokens']),'rank_regret':{n:vals[n][1] for n in vals}})
 trainfit={name:{} for name in models}
 with torch.inference_mode():
  pending=[]
  def score_train(batch):
   inp,_,_=collate(batch,'cpu')
   for name,model in models.items():
    selected=model(*inp)['masked_action_value'].argmax(-1).tolist()
    for j,r in enumerate(batch):
     if not free(r):continue
     t=teacher(r);regret=r['action_targets'][t]-r['action_targets'][selected[j]]
     for group in ['prefix100' if r['seed']<7000100 else 'added900','structural:'+str(round(r['candidate_features'][t][3]*8)),'family:'+family(r['candidate_features'][t])]:
      q=trainfit[name].setdefault(group,collections.Counter());q['n']+=1;q['equivalent']+=regret==0;q['rank_regret_sum']+=regret
  for r in records(new['shards']['train']):
   pending.append(r)
   if len(pending)==64:score_train(pending);pending=[]
  if pending:score_train(pending)
 for groupset in trainfit.values():
  for q in groupset.values():q['equivalent_rate']=q['equivalent']/q['n'];q['rank_regret_mean']=q['rank_regret_sum']/q['n']
 result['train_free_groups']=trainfit
 result.update(model_bindings=bindings,validation_groups={n:{k:{**dict(v),'equivalent_rate':v['equivalent']/v['n'],'rank_regret_mean':v['rank_regret_sum']/v['n']} for k,v in d.items()} for n,d in groups.items()},paired_free_20game_bootstrap95ci={'equivalent_scale1000_minus_relative100':bootstrap(paired,0),'rank_regret_scale1000_minus_relative100':bootstrap(paired,1)},validation_disagreements=examples,limitations=['20 validation games retained from model selection; not independent heldout performance','structural distance/family/effective/prefilter are Calculator-provided inputs, not neural learned rule ability','lexicographic normalized rank is not cardinal counterfactual Q; different candidate sets change rank scales','fixed6epochs increases optimizer steps60to582; data and update budgets both change','auxiliary structural waits not public-effective waits; rare multi-winner cases may remain NA','weighted scalar losses do not measure shared gradient interference; prior matched100 experiment did not support negative transfer'])
 out=ROOT/'reports/next_c_scale_diagnosis.json';out.write_text(json.dumps(result,indent=2));print(json.dumps({'output':str(out),'coverage':{k:v['counts'] for k,v in result['coverage'].items()},'paired_ci':result['paired_free_20game_bootstrap95ci']},indent=2))
if __name__=='__main__':diagnose()

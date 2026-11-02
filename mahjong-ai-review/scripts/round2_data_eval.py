"""Frozen-policy evaluation only; bootstrap clusters complete seed groups."""
import sys,argparse,json,random,statistics,hashlib,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from simulator.selfplay import play
from simulator.policy_learning import PolicyValue
from observations.public import features
from inference.predictor import Predictor

def evaluate(checkpoint,games=100,seed=1100000,old_checkpoint='checkpoints/simulation_v1/best.pt',out='reports/round2_d_policy_evaluation.json'):
 started=time.perf_counter();torch.set_num_threads(2);m=PolicyValue();state=torch.load(checkpoint,map_location='cpu',weights_only=False);m.load_state_dict(state['model']);m.eval();old=Predictor(old_checkpoint);old.model.eval()
 def baseline(o,c):
  def quality(t):
   h=list(o['observer_hand']);h.remove(t)
   return sum(h.count(x)>=2 for x in set(h))*3+sum(abs(x-y) in (1,2) and x//9==y//9 for i,x in enumerate(h) for y in h[i+1:])
  return max(c,key=quality)
 def risk(o,c):
  # First neural joint-risk strategy. No hidden-state or label access.
  with torch.inference_mode():
   logits=old.model(torch.tensor([features(o)],dtype=torch.float32))['joint_logits'][0]
   p=1-logits.softmax(-1)[:,0]
  return min(c,key=lambda t:(p[t],t))
 def learned(o,c):
  with torch.no_grad():logits,_=m(torch.tensor(features(o)).float())
  return max(c,key=lambda t:float(logits[t]))
 policies={'heuristic':baseline,'old_reading_risk':risk,'trained_policy_value':learned};rows=[];group_sums={name:{s:0 for s in range(seed,seed+games)} for name in policies}
 for name,policy in policies.items():
  for s in range(seed,seed+games):
   for seat in range(4):
    r=play(s,policy=policy,policy_seat=seat);group_sums[name][s]+=r['scores'][seat];rows.append(dict(policy=name,seed=s,seat=seat,net_score=r['scores'][seat],scores=r['scores']))
 groups={name:[group_sums[name][s]/4 for s in range(seed,seed+games)] for name in policies}
 rng=random.Random(42);comparisons={}
 for name in ('old_reading_risk','trained_policy_value'):
  differences=[a-b for a,b in zip(groups[name],groups['heuristic'])];boot=sorted(statistics.mean(rng.choices(differences,k=len(differences))) for _ in range(2000))
  comparisons[name]={'mean_difference':statistics.mean(differences),'paired_seed_cluster_bootstrap_95ci':[boot[50],boot[1949]]}
 result=dict(seconds=time.perf_counter()-started,simulation_only=True,not_for_tuning=True,seed_groups=games,executed_games=len(rows),means={k:statistics.mean(v) for k,v in groups.items()},comparisons=comparisons,per_game=rows,flags=['OLD_MODEL_NEW_CONCEALED_KONG_AND_ACTION_DISTRIBUTION_SHIFT','PAIRED_INITIAL_DEAL_NOT_IDENTICAL_FUTURE_TRAJECTORY','SMALL_SAMPLE_NO_STRENGTH_CLAIM'],checkpoint_sha256=hashlib.sha256(Path(checkpoint).read_bytes()).hexdigest(),old_checkpoint_sha256=hashlib.sha256(Path(old_checkpoint).read_bytes()).hexdigest())
 Path(out).parent.mkdir(parents=True,exist_ok=True);Path(out).write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='per_game'}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--checkpoint',required=True);p.add_argument('--games',type=int,default=100);p.add_argument('--seed',type=int,default=1100000);p.add_argument('--old-checkpoint',default='checkpoints/simulation_v1/best.pt');p.add_argument('--out',default='reports/round2_d_policy_evaluation.json');a=p.parse_args()
 if a.games<2:raise ValueError('Need at least two seed groups')
 evaluate(a.checkpoint,a.games,a.seed,a.old_checkpoint,a.out)

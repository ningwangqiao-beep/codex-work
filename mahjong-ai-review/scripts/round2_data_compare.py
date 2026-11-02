import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import argparse,json,statistics
from simulator.selfplay import play

def baseline(o,c):return c[0]
def cautious(o,c):
    # Legal public-only policy, no hidden-label oracle.
    disc=[t for _,t in o['visible_discards']]
    return max(c,key=lambda t:disc.count(t))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--games',type=int,default=20);p.add_argument('--seed',type=int,default=600000);p.add_argument('--checkpoint');a=p.parse_args();result={}
 policies=[('baseline',baseline),('public_count',cautious)]
 if a.checkpoint:
  import torch
  from simulator.policy_learning import PolicyValue
  from observations.public import features
  m=PolicyValue();m.load_state_dict(torch.load(a.checkpoint,weights_only=False)['model']);m.eval()
  def learned(o,c):
   with torch.no_grad():logits,_=m(torch.tensor(features(o)).float())
   return max(c,key=lambda t:float(logits[t]))
  policies.append(('learned',learned))
 for name,policy in policies:
  values=[]
  for seed in range(a.seed,a.seed+a.games):
   for seat in range(4):values.append(play(seed,policy=policy,policy_seat=seat)['scores'][seat])
  result[name]={'games':len(values),'mean_net_score':statistics.mean(values),'scores':values}
 print(json.dumps({'simulation_only':True,'paired_seed_and_rotated_seats':True,'results':result}))

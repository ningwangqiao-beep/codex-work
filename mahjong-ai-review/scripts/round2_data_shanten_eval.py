"""Public-only shanten experiment, fixed choices without final-test tuning."""
import sys,argparse,json,time,random,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from simulator.selfplay import play
from rules.hand_analysis import shanten,effective_draws
from rules.core import winning

def validate(seed=42,n=100):
 rng=random.Random(seed);checked=0
 for _ in range(n):
  wall=list(range(27))*4;rng.shuffle(wall);h=wall[:14];missing=rng.randrange(3)
  assert (shanten(h,missing_suit=missing)['minimum']==-1)==winning(h,missing)
  checked+=1
 return checked

def run(games=20,seed=1900000,out='reports/round2_d_shanten_eval.json',timeout=120):
 start=time.perf_counter();checks=validate();rows=[];calls=0
 def baseline(o,legal):
  def q(t):
   h=list(o['observer_hand']);h.remove(t);return sum(h.count(x)>=2 for x in set(h))*3+sum(abs(x-y) in (1,2) and x//9==y//9 for i,x in enumerate(h) for y in h[i+1:])
  return max(legal,key=q)
 def policy(o,legal):
  nonlocal calls
  calls+=1
  if time.perf_counter()-start>timeout:raise TimeoutError('bounded shanten experiment')
  seat=o['observer_player'];opened=len(o['public_melds'][seat]);missing=o['declared_missing_suits'][seat]
  public=[t for _,t in o['visible_discards']]+[t for ms in o['public_melds'] for m in ms for t in m if t>=0]+o.get('public_winning_tiles',[])
  ranks=[]
  for tile in legal:
   h=list(o['observer_hand']);h.remove(tile);pub=public+[tile]
   distance=shanten(h,opened,missing,pub)['minimum'];ranks.append((distance,tile,h,pub))
  best=min(x[0] for x in ranks);candidates=[]
  for distance,tile,h,pub in ranks:
   if distance==best:candidates.append((sum(x['remaining'] for x in effective_draws(h,opened,missing,pub)),-tile,tile))
  return max(candidates)[2]
 status='completed';error=None
 try:
  for s in range(seed,seed+games):
   for seat in range(4):
    for name,callback in [('shape',baseline),('shanten',policy)]:
     r=play(s,policy=callback,policy_seat=seat);rows.append(dict(seed=s,seat=seat,policy=name,net_score=r['scores'][seat]))
 except Exception as e:status='incomplete';error=repr(e)
 complete=[s for s in range(seed,seed+games) if sum(r['seed']==s for r in rows)==8];diff=[]
 for s in complete:diff.append(sum(r['net_score']*(1 if r['policy']=='shanten' else -1) for r in rows if r['seed']==s)/4)
 rng=random.Random(42);boot=sorted(statistics.mean(rng.choices(diff,k=len(diff))) for _ in range(2000)) if diff else []
 result=dict(status=status,error=error,crosscheck_random_hands=checks,seconds=time.perf_counter()-start,calls=calls,complete_seed_groups=len(complete),rows=rows,mean_difference=statistics.mean(diff) if diff else None,paired_seed_bootstrap_95ci=[boot[50],boot[1949]] if boot else None,simulation_only=True,teacher_uses_only_legal_observation=True)
 Path(out).write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--games',type=int,default=20);p.add_argument('--seed',type=int,default=1900000);p.add_argument('--timeout',type=float,default=120);p.add_argument('--out',default='reports/round2_d_shanten_eval.json');a=p.parse_args();run(a.games,a.seed,a.out,a.timeout)

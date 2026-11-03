"""V3 paired initial deal and rotated-seat comparison; no training."""
import sys,argparse,time,json,random,statistics,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from simulator.v3_selfplay import play
from inference.v3_legacy import LegacyV3DiscardPolicy

def shape(o,legal):
 def quality(t):
  h=list(o['observer_hand']);h.remove(t);return sum(h.count(x)>=2 for x in set(h))*3+sum(abs(x-y) in (1,2) and x//9==y//9 for i,x in enumerate(h) for y in h[i+1:])
 return max(legal,key=quality)
def metrics(r,seat):
 parts={}
 for e in r['ledger']:
  amount=e['amount']*((e['receiver']==seat)-(e['payer']==seat));parts[e['category']]=parts.get(e['category'],0)+amount
 assert sum(parts.values())==r['scores'][seat]
 own=[w for w in r['win_events'] if w['seat']==seat];paid=[w for w in r['win_events'] if w['payer']==seat]
 return dict(net=r['scores'][seat],parts=parts,win=int(bool(own)),self_draw=sum(w['kind']=='self_draw' for w in own),fan_sum=sum(w['final_fan'] for w in own),win_events=len(own),deal_in_events=len(paid),deal_in_loss=sum(w['payment'] for w in paid))
def run(games=2,seed=3400000,timeout=90,strong=False):
 import torch
 torch.set_num_threads(2);start=time.perf_counter();rows=[];error=None
 policies={'random':None,'shape':shape,'old_candidate':LegacyV3DiscardPolicy(root/'experiments/round2_c/candidate/best.pt','candidate'),'old_residual':LegacyV3DiscardPolicy(root/'checkpoints/round2_candidate_rl_rounded/last.pt','residual')}
 if strong:
  from baselines.v3_bot import BaselineV3
  policies['new_baseline']=BaselineV3()
 sources=[root/p for p in ('rules/core.py','rules/v3.py','simulator/table.py','simulator/v3_selfplay.py','observations/v3_public.py','observations/public.py')];before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
 partial=root/'reports'/f'v3_d_compare_{seed}.jsonl'
 try:
  with partial.open('w') as f:
   for s in range(seed,seed+games):
    for seat in range(4):
     for name,callback in policies.items():
      rng=random.Random(s*4+seat)
      def policy(o,legal):
       if time.perf_counter()-start>timeout:raise TimeoutError('comparison budget')
       return callback(o,legal) if o['observer_player']==seat and callback else rng.choice(legal)
      r=play(s,policy=policy,policy_seat=None,exchange_offset=s%3+1);row=dict(seed=s,seat=seat,policy=name,metrics=metrics(r,seat),scores=r['scores']);rows.append(row);f.write(json.dumps(row)+'\n');f.flush()
 except (Exception,KeyboardInterrupt) as e:error=repr(e)
 after={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
 if before!=after:error='source changed'
 complete=[s for s in range(seed,seed+games) if sum(r['seed']==s for r in rows)==4*len(policies)];summary={};comparisons={};rng=random.Random(42)
 for name in policies:
  selected=[r for r in rows if r['policy']==name and r['seed'] in complete]
  if not selected:continue
  n=len(selected);summary[name]={k:sum(r['metrics'][k] for r in selected)/n for k in ('net','win','self_draw','deal_in_events','deal_in_loss')};w=sum(r['metrics']['win_events'] for r in selected);summary[name]['mean_winning_fan']=sum(r['metrics']['fan_sum'] for r in selected)/w if w else None
  summary[name]['parts_mean']={c:sum(r['metrics']['parts'].get(c,0) for r in selected)/n for c in {c for r in selected for c in r['metrics']['parts']}}
  if name!='shape':
   differences=[sum(r['metrics']['net']*(1 if r['policy']==name else -1) for r in rows if r['seed']==s and r['policy'] in (name,'shape'))/4 for s in complete];boot=sorted(statistics.mean(rng.choices(differences,k=len(differences))) for _ in range(2000));comparisons[name]={'mean_vs_shape':statistics.mean(differences),'paired_seed_ci':[boot[50],boot[1949]]}
 result=dict(status='incomplete' if error else 'completed',error=error,complete_seed_groups=len(complete),seconds=time.perf_counter()-start,summary=summary,comparisons=comparisons,source_before=before,source_after=after,legacy_metadata={k:v.metadata for k,v in policies.items() if hasattr(v,'metadata')},limitations=['random opponent discards; meld actions shared simulator','win events not transfer count','configured singlemax settlement; not verified room','paired initial deal not identical future','small sample no strength claim'])
 (root/'reports'/f'v3_d_compare_{seed}.json').write_text(json.dumps(result,indent=2));print(result)
 if error:raise SystemExit(2)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--games',type=int,default=2);p.add_argument('--seed',type=int,default=3400000);p.add_argument('--timeout',type=float,default=90);p.add_argument('--strong',action='store_true');a=p.parse_args();run(a.games,a.seed,a.timeout,a.strong)




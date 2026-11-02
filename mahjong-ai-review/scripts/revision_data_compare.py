import sys,argparse,time,json,random,statistics,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from baselines.revision_bot import BaselineBot
from simulator.selfplay import play
p=argparse.ArgumentParser();p.add_argument('--games',type=int,default=2);p.add_argument('--seed',type=int,default=2800000);p.add_argument('--timeout',type=float,default=120);a=p.parse_args();source=Path(__file__).resolve().parents[1]/'rules/hand_analysis.py';source_before=hashlib.sha256(source.read_bytes()).hexdigest();partial=Path('reports/revision_d_partial.jsonl');partial.write_text('');start=time.perf_counter();rows=[];error=None
try:
 for seed in range(a.seed,a.seed+a.games):
  for seat in range(4):
   for name in ('random','baseline'):
    rng=random.Random(seed*4+seat);bot=BaselineBot()
    def callback(o,legal):
     if time.perf_counter()-start>a.timeout:raise TimeoutError('bounded comparison')
     return bot(o,legal) if name=='baseline' and o['observer_player']==seat else rng.choice(legal)
    r=play(seed,policy=callback,policy_seat=None);row=dict(seed=seed,seat=seat,policy=name,scores=r['scores'],net_score=r['scores'][seat]);rows.append(row)
    with partial.open('a') as f:f.write(json.dumps(row)+'\n')
except (Exception,KeyboardInterrupt) as e:error=repr(e)
complete=[s for s in range(a.seed,a.seed+a.games) if sum(r['seed']==s for r in rows)==8];diff=[sum(r['net_score']*(1 if r['policy']=='baseline' else -1) for r in rows if r['seed']==s)/4 for s in complete];rng=random.Random(42);boot=sorted(statistics.mean(rng.choices(diff,k=len(diff))) for _ in range(2000)) if diff else []
after=hashlib.sha256(source.read_bytes()).hexdigest()
if after!=source_before:error='Source changed during evaluation'
report=dict(source_before=source_before,source_after=after,status='completed' if error is None else 'incomplete',error=error,seconds=time.perf_counter()-start,complete_seed_groups=len(complete),mean_difference=statistics.mean(diff) if diff else None,bootstrap_ci=[boot[50],boot[1949]] if boot else None,rows=rows,simulation_only=True,limitations=['two-step truncated to 2 effective draw types','structural missing-suit distance optimistic; explicit missing debt separate','opponent risk uncalibrated public heuristic','random discard opponents retain shared simulator meld decisions','no strength claim small sample'])
Path('reports/revision_d_baseline_comparison.json').write_text(json.dumps(report,indent=2));print({k:v for k,v in report.items() if k!='rows'})

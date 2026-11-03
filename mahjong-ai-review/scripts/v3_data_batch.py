"""V3 strict audit/performance runner. Approval artifact is required for batches."""
import sys,argparse,json,hashlib,time,concurrent.futures
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from simulator.v3_selfplay import play

def work(seed):return play(seed,exchange_offset=seed%3+1)
def run(games,seed,ready):
 approval=json.loads(Path(ready).read_text())
 sources=[root/p for p in ('rules/core.py','rules/v3.py','simulator/table.py','simulator/v3_selfplay.py','observations/v3_public.py','observations/public.py')]
 before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
 if not approval.get('passed') or approval.get('source_hashes')!=before:raise ValueError('Missing current V3 test-ready binding')
 start=time.perf_counter();steps=0;categories={};partial=root/'reports'/f'v3_d_batch_{games}_{seed}.jsonl'
 with partial.open('w') as f,concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
  for r in pool.map(work,range(seed,seed+games),chunksize=4):
   steps+=r['steps'];assert sum(r['scores'])==0
   for e in r['ledger']:categories[e['category']]=categories.get(e['category'],0)+1
   f.write(json.dumps({k:v for k,v in r.items() if k!='rows'})+'\n');f.flush()
 after={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources};assert before==after
 report=dict(games=games,seed_range=[seed,seed+games-1],steps=steps,seconds=time.perf_counter()-start,source_hashes=before,unchanged=True,categories=categories,workers=4)
 (root/'reports'/f'v3_d_batch_{games}_{seed}.json').write_text(json.dumps(report,indent=2));print(report)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--games',type=int,required=True);p.add_argument('--seed',type=int,required=True);p.add_argument('--ready',required=True);a=p.parse_args();run(a.games,a.seed,a.ready)

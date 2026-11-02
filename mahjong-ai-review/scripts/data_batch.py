"""Spawn-safe audited batch driver; writes small JSONL shards incrementally."""
import argparse,concurrent.futures,hashlib,json,time
from pathlib import Path
from simulator.selfplay import play

def worker(args):return play(*args)
def run(n,collect=False,offset=0):
    root=Path(__file__).resolve().parents[1];out=root/'datasets'/'simulation_v2';out.mkdir(exist_ok=True)
    sources=[root/'rules/core.py',root/'simulator/table.py',root/'simulator/selfplay.py',root/'observations/public.py'];before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    started=time.perf_counter();states=steps=0;counts={s:0 for s in ('train','validation','test')}
    handles={s:open(out/(s+'.jsonl'),'w',encoding='utf-8') for s in counts} if collect else {}
    try:
      with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
       for r in pool.map(worker,((i,collect) for i in range(offset,offset+n)),chunksize=8):
        steps+=r['steps']
        if sum(r['scores']):raise ValueError('nonzero scores')
        split='train' if r['seed']%10<7 else 'validation' if r['seed']%10<9 else 'test'
        for row in r['rows']:
          handles[split].write(json.dumps(row,separators=(',',':'))+'\n');states+=1;counts[split]+=1
    finally:
      for f in handles.values():f.close()
    hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'rules/core.py',root/'simulator/table.py',root/'simulator/selfplay.py',root/'observations/public.py']}
    assert hashes==before,'Source changed during batch'
    report=dict(source_hashes_unchanged=True,games=n,states=states,steps=steps,seconds=time.perf_counter()-started,workers=4,split_rows=counts,hashes=hashes,simulation_only=True,strict_inventory=True)
    (root/'reports'/f'employee_d_v2_batch_{n}_{int(collect)}.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--games',type=int,required=True);p.add_argument('--collect',action='store_true');p.add_argument('--offset',type=int,default=0);a=p.parse_args();run(a.games,a.collect,a.offset)

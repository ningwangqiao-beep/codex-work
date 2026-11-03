import sys,json,time
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from simulator.v3_history_v2 import play
from baselines.v3_bot import BaselineV3
start=time.perf_counter()
with (root/'datasets/next_history100/game_returns.jsonl').open('w') as f:
 for i in range(120):
  seed=7000000+i if i<100 else 7100000+i-100;r=play(seed,policy=BaselineV3(),policy_seat=i%4,exchange_offset=seed%3+1)
  f.write(json.dumps({k:v for k,v in r.items() if k!='rows'},separators=(',',':'))+'\n');f.flush()
print('games=120 seconds='+str(time.perf_counter()-start))

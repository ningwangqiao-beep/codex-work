import sys,time,json,random,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from rules.hand_analysis import shanten as slow,effective_draws as slow_draws
from rules.fast_hand_analysis import shanten as fast,effective_draws as fast_draws
cases=[]
for opened,n,domain in [(4,1,range(27)),(4,2,range(27)),(3,4,[0,1,2,9]),(3,5,[0,1,2,9])]:
 for h in itertools.combinations_with_replacement(domain,n):
  if max(__import__('collections').Counter(h).values())<=4:cases.append((list(h),opened,None))
for opened in (0,1,2):cases.append(([0,3,6,9,12,15,18,21,24,0,3,9,12][:13-3*opened],opened,None))
rng=random.Random(871)
for opened in range(5):
 for extra in (0,1):
  for missing in (None,0,1,2):
   for _ in range(3):
    wall=list(range(27))*4;rng.shuffle(wall);cases.append((wall[:13-3*opened+extra],opened,missing))
t=time.perf_counter();expected=[slow(h,o,m) for h,o,m in cases];slow_seconds=time.perf_counter()-t
t=time.perf_counter();actual=[fast(h,o,m) for h,o,m in cases];cold=time.perf_counter()-t
assert actual==expected
for h,o,m in cases[-120::7]:
 if len(h)==13-3*o:assert fast_draws(h,o,m)==slow_draws(h,o,m)
t=time.perf_counter()
for _ in range(10):
 for h,o,m in cases:fast(h,o,m)
warm=time.perf_counter()-t
result=dict(cases=len(cases),parity=True,slow_seconds=slow_seconds,first_fast_seconds=cold,warm_10passes_seconds=warm,warm_calls_per_second=len(cases)*10/warm,note='cold fast measured after slow target enumeration; not process cold start; no GPU')
Path('reports/v3_b_fast_analysis.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))


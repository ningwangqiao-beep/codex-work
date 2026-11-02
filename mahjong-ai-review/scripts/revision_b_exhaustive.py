"""Finite exhaustive audit. Run from project: py -3.13 scripts/revision_b_exhaustive.py"""
import sys,json,time,itertools,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from rules.hand_analysis import shanten,legal_progress
from rules.hand_analysis_reference import target_distance,suit_target_distance

def main():
 start=time.perf_counter();counts=collections.Counter();hist=collections.Counter();fail=[]
 for opened,length,domain in [(4,1,range(27)),(4,2,range(27)),(3,4,[0,1,2,9]),(3,5,[0,1,2,9])]:
  for h in itertools.combinations_with_replacement(domain,length):
   if max(collections.Counter(h).values())>4:continue
   a=shanten(list(h),opened)['standard'];b=target_distance(h,opened);c=suit_target_distance(h,opened)
   counts[f'open{opened}_len{length}']+=1;hist[f'open{opened}_len{length}_s{a}']+=1
   if a!=b or b!=c:fail.append(dict(hand=h,opened=opened,production=a,direct=b,suit_dp=c))
 # Additional high-distance represented cases, no cap2 filtering.
 for opened in (0,1,2):
  length=13-3*opened
  h=[0,3,6,9,12,15,18,21,24,0,3,9,12][:length]
  a=shanten(h,opened)['standard'];c=suit_target_distance(h,opened)
  counts[f'open{opened}_high_len{length}']+=1;hist[f'open{opened}_len{length}_s{a}']+=1
  if a!=c:fail.append(dict(hand=h,opened=opened,production=a,suit_dp=c))
 # Independent direct seven-pair target enumeration in a bounded four-type universe.
 # Four tiles can hold seven pairs only as three quads plus one pair.
 targets=[]
 for ns in itertools.product((0,2,4),repeat=4):
  if sum(ns)==14:targets.append(ns)
 pairs_cases=0
 for length in (13,14):
  for h in itertools.combinations_with_replacement(range(4),length):
   cc=collections.Counter(h)
   if max(cc.values())>4:continue
   # Outside-domain tiles might improve unrestricted target, so compute independent
   # exact direct targets using seven pair units across the hand's four types plus
   # seven fresh types; enumerate only pair allocations to known types, then fill.
   best=99
   for ns in itertools.product((0,2,4),repeat=4):
    if sum(ns)>14:continue
    deficit=sum(max(0,n-cc[t]) for t,n in enumerate(ns))+(14-sum(ns))
    best=min(best,deficit-1)
   got=legal_progress(list(h))['legal_seven_pairs'];pairs_cases+=1
   if got!=best:fail.append(dict(hand=h,seven_dp=got,seven_direct=best))
 result={'status':'passed' if not fail else 'failed','command':'py -3.13 scripts/revision_b_exhaustive.py','cases_by_group':dict(counts),'histogram':dict(sorted(hist.items())),'standard_cases':sum(counts.values()),'three_plus_cases':sum(n for k,n in hist.items() if int(k.rsplit('_s',1)[1])>=3),'seven_pair_cases':pairs_cases,'failures':fail,'seconds':time.perf_counter()-start,'scope':'exhaustive specified finite domains only; full27 open4, four-type open3; no distance truncation'}
 Path('reports/revision_b_exhaustive.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return bool(fail)
if __name__=='__main__':raise SystemExit(main())


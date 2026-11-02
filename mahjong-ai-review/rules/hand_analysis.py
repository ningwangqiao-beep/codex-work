"""Own-hand shanten and visible remaining tiles; no opponent hidden-state inputs.

Standard DFS enumerates disjoint melds, pair/head, partial sequences and leftovers.
For each partition: 8-2*(open+melds)-min(taatsu,4-open-melds)-head.
Missing-suit tiles cannot participate, but remain discardable leftovers. Seven-pairs
uses 6 - sum(count//2): a quad counts as two pairs, matching frozen core.
"""
from collections import Counter
from functools import lru_cache

def _validate(hand,open_melds,missing,public):
 if type(open_melds)!=int or not 0<=open_melds<=4:raise ValueError('open meld count')
 if missing is not None and (type(missing)!=int or missing not in range(3)):raise ValueError('missing suit')
 if len(hand) not in (13-3*open_melds,14-3*open_melds):raise ValueError('13/14-equivalent hand required')
 if any(type(t)!=int or t not in range(27) for t in list(hand)+list(public)):raise ValueError('tile')
 if any(n>4 for n in Counter(list(hand)+list(public)).values()):raise ValueError('physical fifth copy')

@lru_cache(maxsize=50000)
def _standard(counts,opened):
 best=8
 def dfs(c,m,t,h):
  nonlocal best
  if not any(c):best=min(best,8-2*(opened+m)-min(t,max(0,4-opened-m))-h);return
  i=next(i for i,n in enumerate(c) if n)
  def branch(indices,dm=0,dt=0,dh=0):
   a=list(c)
   for k in indices:a[k]-=1
   dfs(tuple(a),m+dm,t+dt,h+dh)
  if opened+m<4:
   if c[i]>=3:branch([i]*3,dm=1)
   if i%9<=6 and c[i+1] and c[i+2]:branch([i,i+1,i+2],dm=1)
  if c[i]>=2:
   if not h:branch([i]*2,dh=1)
   branch([i]*2,dt=1)
  if i%9<=7 and c[i+1]:branch([i,i+1],dt=1)
  if i%9<=6 and c[i+2]:branch([i,i+2],dt=1)
  branch([i])
 dfs(counts,0,0,0)
 return best

def shanten(hand,open_melds=0,missing_suit=None,public_tiles=()):
 """Return structural distance. public_tiles excludes own hand, includes own melds.

 Already-formed open melds must obey missing suit, validated by caller (tiles are
 not supplied separately). Structural distance may be optimistic when all outs dead.
 """
 _validate(hand,open_melds,missing_suit,public_tiles)
 c=Counter(t for t in hand if t//9!=missing_suit)
 standard=_standard(tuple(c[i] for i in range(27)),open_melds)
 # Exact target constraints prevent impossible fifth-copy structural completions.
 if not any(t//9==missing_suit for t in hand):
  from rules.hand_analysis_reference import suit_target_distance
  standard=suit_target_distance(hand,open_melds,missing_suit)
 seven=None
 if not open_melds:
  seven=6-sum(n//2 for n in c.values())
 # No legal win while still holding any missing-suit tile.
 if missing_suit is not None and any(t//9==missing_suit for t in hand):
  standard=max(0,standard)
  if seven is not None:seven=max(0,seven)
 return {'standard':standard,'seven_pairs':seven,'minimum':min(standard,seven) if seven is not None else standard}

def effective_draws(hand,open_melds=0,missing_suit=None,public_tiles=()):
 """13-equivalent hand only. Draws reducing structural distance with visible outs."""
 _validate(hand,open_melds,missing_suit,public_tiles)
 if len(hand)!=13-3*open_melds:raise ValueError('effective draws require post-discard hand')
 before=shanten(hand,open_melds,missing_suit,public_tiles)['minimum'];known=Counter(list(hand)+list(public_tiles));out=[]
 for tile in range(27):
  remaining=4-known[tile]
  if remaining>0 and tile//9!=missing_suit:
   after=shanten(list(hand)+[tile],open_melds,missing_suit,public_tiles)['minimum']
   if after<before:out.append({'tile':tile,'remaining':remaining,'shanten':after})
 return out


def legal_progress(hand,open_melds=0,missing_suit=None,public_tiles=()):
 """Exact legal-target draw deficit minus one, separate from legacy structure.

 Uses enumerated suit targets, including missing-suit replacement debt. Ignores
 externally dead targets: public tiles validate inventory but do not change target
 reachability. Optional audit/teacher API, slower than shanten; no timing guarantee.
 """
 _validate(hand,open_melds,missing_suit,public_tiles)
 from rules.hand_analysis_reference import suit_target_distance
 standard=suit_target_distance(hand,open_melds,missing_suit)
 seven=None
 if open_melds==0:
  counts=Counter(hand);dp={0:0}
  for tile in range(27):
   if tile//9==missing_suit:continue
   nxt={}
   for pairs,cost in dp.items():
    for n in (0,2,4):
     total=pairs+n//2
     if total<=7:nxt[total]=min(nxt.get(total,999),cost+max(0,n-counts[tile]))
   dp=nxt
  seven=dp[7]-1
 return {'legal_standard':standard,'legal_seven_pairs':seven,'legal_minimum':min(standard,seven) if seven is not None else standard,'missing_tiles':sum(t//9==missing_suit for t in hand),'metric':'legal-target draw deficit minus one; external dead tiles ignored'}



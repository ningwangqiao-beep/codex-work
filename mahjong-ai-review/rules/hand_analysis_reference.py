"""Independent exact target-overlap oracle for small open-hand states.

No DFS taatsu formula: enumerate complete concealed target multisets and minimize
missing copies minus one. Optional tile_domain restricts target space; results are
then exact only for that restricted domain. Intended for tests, not live policy.
"""
from itertools import combinations_with_replacement
from collections import Counter

def target_distance(hand,opened,missing=None,tile_domain=range(27)):
 if opened not in range(2,5):raise ValueError('oracle deliberately bounded to open2..4')
 domain=set(t for t in tile_domain if t//9!=missing)
 melds=[(t,t,t) for t in sorted(domain)]+[(t,t+1,t+2) for t in sorted(domain) if t%9<=6 and t+1 in domain and t+2 in domain]
 counts=Counter(hand);best=99
 for ms in combinations_with_replacement(melds,4-opened):
  for pair in domain:
   target=Counter([pair,pair])
   for m in ms:target.update(m)
   if max(target.values())>4:continue
   best=min(best,sum(max(0,n-counts[t]) for t,n in target.items())-1)
 return best

@__import__('functools').lru_cache(maxsize=64)
def _suit_targets(melds,pair):
    units=[(i,i,i) for i in range(9)]+[(i,i+1,i+2) for i in range(7)]
    result=set()
    for ms in combinations_with_replacement(units,melds):
        base=Counter(t for m in ms for t in m)
        for head in range(9) if pair else [None]:
            c=base.copy()
            if head is not None:c[head]+=2
            if max(c.values(),default=0)<=4:result.add(tuple(c[i] for i in range(9)))
    return tuple(result)

def suit_target_distance(hand,opened=0,missing=None):
    return _suit_distance_cached(tuple(hand),opened,missing)

@__import__("functools").lru_cache(maxsize=50000)
def _suit_distance_cached(hand,opened=0,missing=None):
    """Independent exact standard target deficit via suit target DP; all open counts.

    Includes missing-suit debt. Ignores external dead tiles. Returns draws-to-target
    minus one; a 14-equivalent hand can discard surplus freely in this distance.
    """
    if type(opened)!=int or opened not in range(5):raise ValueError('opened')
    if len(hand) not in (13-3*opened,14-3*opened):raise ValueError('hand size')
    if any(type(t)!=int or t not in range(27) for t in hand) or max(Counter(hand).values(),default=0)>4:raise ValueError('tiles')
    c=Counter(hand);needed=4-opened;dp={(0,0):0}
    for suit in range(3):
        costs={}
        for m in range(needed+1):
            for p in (0,1):
                if suit==missing and (m or p):continue
                targets=_suit_targets(m,p)
                costs[m,p]=min(sum(max(0,n-c[suit*9+i]) for i,n in enumerate(t)) for t in targets)
        nxt={}
        for (a,b),cost in dp.items():
            for (m,p),extra in costs.items():
                if a+m<=needed and b+p<=1:
                    key=(a+m,b+p);nxt[key]=min(nxt.get(key,999),cost+extra)
        dp=nxt
    return dp[needed,1]-1


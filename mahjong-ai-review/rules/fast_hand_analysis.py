"""Vectorized exact suit-target costs. Shares target sets, not legacy taatsu DFS."""
from functools import lru_cache
from collections import Counter
import numpy as np
from rules.hand_analysis_reference import _suit_targets
from rules.hand_analysis import _validate
@lru_cache(maxsize=10)
def matrix(m,p):return np.asarray(_suit_targets(m,p),dtype=np.int16).reshape(-1,9)
@lru_cache(maxsize=50000)
def _cost(c,m,p):return int(np.maximum(matrix(m,p)-np.asarray(c,dtype=np.int16),0).sum(axis=1).min())
@lru_cache(maxsize=50000)
def _distance(hand,opened,missing):
 counts=Counter(hand);need=4-opened;dp={(0,0):0}
 for suit in range(3):
  c=tuple(counts[suit*9+i] for i in range(9));costs={}
  for m in range(need+1):
   for p in (0,1):
    if suit==missing and (m or p):continue
    costs[m,p]=_cost(c,m,p)
  nxt={}
  for (a,b),v in dp.items():
   for (m,p),w in costs.items():
    if a+m<=need and b+p<=1:nxt[a+m,b+p]=min(nxt.get((a+m,b+p),999),v+w)
  dp=nxt
 return dp[need,1]-1

def shanten(hand,open_melds=0,missing_suit=None,public_tiles=()):
 _validate(hand,open_melds,missing_suit,public_tiles)
 if any(t//9==missing_suit for t in hand):
  # Preserve legacy optimistic missing-debt semantics exactly.
  from rules.hand_analysis import shanten as original
  return original(hand,open_melds,missing_suit,public_tiles)
 standard=_distance(tuple(sorted(hand)),open_melds,missing_suit);seven=None
 if not open_melds:seven=6-sum(n//2 for n in Counter(hand).values())
 return {'standard':standard,'seven_pairs':seven,'minimum':min(standard,seven) if seven is not None else standard}

def effective_draws(hand,open_melds=0,missing_suit=None,public_tiles=()):
 _validate(hand,open_melds,missing_suit,public_tiles)
 if len(hand)!=13-3*open_melds:raise ValueError('post-discard hand required')
 before=shanten(hand,open_melds,missing_suit,public_tiles)['minimum'];known=Counter(list(hand)+list(public_tiles));result=[]
 for tile in range(27):
  if known[tile]<4 and tile//9!=missing_suit:
   after=shanten(list(hand)+[tile],open_melds,missing_suit,public_tiles)['minimum']
   if after<before:result.append({'tile':tile,'remaining':4-known[tile],'shanten':after})
 return result

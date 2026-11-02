from collections import Counter
from functools import lru_cache
import random
@lru_cache(maxsize=100000)
def groups(c):
 if not any(c): return True
 i=next(i for i,n in enumerate(c) if n);a=list(c)
 if a[i]>=3:
  a[i]-=3
  if groups(tuple(a)): return True
  a[i]+=3
 if i%9<=6 and a[i+1] and a[i+2]:
  for j in (i,i+1,i+2):a[j]-=1
  if groups(tuple(a)):return True
 return False
def winning(hand,missing,meld_count=0,melds=None):
 validate_context(hand,missing,meld_count,melds)
 if melds and any(t//9==missing for m in melds for t in m):return False
 c=Counter(hand)
 if len(hand)!=14-3*meld_count or any(t//9==missing for t in hand):return False
 counts=tuple(c[i] for i in range(27))
 if meld_count==0 and all(n%2==0 for n in counts):return True
 for i,n in enumerate(counts):
  if n>=2:
   a=list(counts);a[i]-=2
   if groups(tuple(a)):return True
 return False
def waits(hand,missing,meld_count=0):
 return [t for t in range(27) if hand.count(t)<4 and winning(hand+[t],missing,meld_count)]
def legal_discards(hand,missing):
 validate_context(hand,missing)
 return sorted({t for t in hand if t//9==missing} or set(hand))
def deal(seed):
 w=list(range(27))*4;random.Random(seed).shuffle(w)
 return [w[p*13:p*13+13] for p in range(4)],w[52:]
def transfer(balances,payer,winners,amounts):
 if len(balances)!=4 or type(payer)!=int or payer not in range(4) or any(type(w)!=int or w not in range(4) for w in winners):raise ValueError("seat")
 if len(set(winners))!=len(winners) or payer in winners or len(winners)!=len(amounts) or any(a<0 for a in amounts):raise ValueError('settlement')
 out=list(balances)
 for w,a in zip(winners,amounts):out[payer]-=a;out[w]+=a
 assert sum(out)==sum(balances)
 return out

# Configuration below is an explicit simulation proposal, pending owner approval.
from dataclasses import dataclass
@dataclass(frozen=True)
class AssumptionConfig:
 fan_cap:int=4
 base_fan:int=0
 triplets_fan:int=1
 seven_pairs_fan:int=2
 dragon_pair_quad_fan:int=0
 pure_suit_fan:int=2
 exchange_offset:int=1
 cha_jiao_enabled:bool=True
 gang_payments_enabled:bool=False
 refund_unready_gangs:bool=True
 concealed_kong_fee:int=2
 exposed_kong_fee:int=2
 added_kong_fee:int=1
 approved:bool=False
 def __post_init__(self):
  if type(self.fan_cap)!=int or self.fan_cap!=4 or type(self.exchange_offset)!=int or self.exchange_offset not in (1,2,3):raise ValueError('configuration')
  for name in ("base_fan","triplets_fan","seven_pairs_fan","dragon_pair_quad_fan","pure_suit_fan","concealed_kong_fee","exposed_kong_fee","added_kong_fee"):
   if type(getattr(self,name))!=int or getattr(self,name)<0:raise ValueError("negative/noninteger scoring parameter")

def validate_context(hand,missing,meld_count=0,melds=None):
 if type(missing)!=int or missing not in (0,1,2):raise ValueError('missing suit')
 if type(meld_count)!=int or not 0<=meld_count<=4:raise ValueError('meld count')
 tiles=list(hand)
 if melds is not None:
  if len(melds)!=meld_count:raise ValueError('meld mismatch')
  for m in melds:
   if len(m) not in (3,4) or len(set(m))!=1:raise ValueError('only peng/kong melds')
   tiles+=list(m)
 if any(type(t)!=int or not 0<=t<27 for t in tiles) or max(Counter(tiles).values(),default=0)>4:raise ValueError('tile inventory')

def exchange(hands,selections,offset):
 if len(hands)!=4 or len(selections)!=4 or type(offset)!=int or offset not in (1,2,3):raise ValueError('exchange parameters')
 if Counter(sum((list(h) for h in hands),[])) != Counter({t:4 for t in range(27)}) and any(n>4 for n in Counter(sum((list(h) for h in hands),[])).values()):raise ValueError('inventory')
 out=[list(h) for h in hands]
 for p,tiles in enumerate(selections):
  validate_context(out[p],0)
  if len(tiles)!=3 or len({t//9 for t in tiles})!=1:raise ValueError('same-suit three required')
  for t in tiles:out[p].remove(t)
 for p,tiles in enumerate(selections):out[(p+offset)%4].extend(tiles)
 return out

def score(hand,missing,melds=(),config=AssumptionConfig()):
 if not winning(hand,missing,len(melds),melds):raise ValueError('not winning')
 c=Counter(hand);fan=config.base_fan;patterns=['basic']
 if not melds and all(n%2==0 for n in c.values()):
  fan+=config.seven_pairs_fan;patterns+=['seven_pairs']
  if config.dragon_pair_quad_fan and any(n==4 for n in c.values()):fan+=config.dragon_pair_quad_fan*sum(n==4 for n in c.values());patterns+=['dragon_pairs']
 elif sum(n%3==2 for n in c.values())==1 and all(n%3 in (0,2) for n in c.values()):fan+=config.triplets_fan;patterns+=['all_triplets']
 if len({t//9 for t in hand}|{t//9 for m in melds for t in m})==1:fan+=config.pure_suit_fan;patterns+=['pure_suit']
 return {'fan':min(fan,config.fan_cap),'payment':2**min(fan,config.fan_cap),'patterns':patterns,'assumption':True}




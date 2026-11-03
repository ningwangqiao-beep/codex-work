"""Explicit user-specified V3 fan levels, separate from legacy additive scoring."""
from dataclasses import dataclass
from functools import lru_cache
from collections import Counter
from rules.core import AssumptionConfig,winning
VERSION='SICHUAN-XUEZHAN-4FAN-V3'
@dataclass(frozen=True)
class V3Config(AssumptionConfig):
 rule_version:str=VERSION
 cha_jiao_mode:str="max_wait_payment"
 gang_payments_enabled:bool=True
 base_fan:int=1
 refund_unready_gangs:bool=True
 pattern_levels:tuple=(("basic",1),("all_triplets",2),("pure_suit",2),("dai_yao",2),("seven_pairs",2),("dragon_pairs",3),("pure_triplets",3),("jiang_triplets",3),("pure_seven_pairs",4),("pure_dragon_pairs",4))
 combination_policy:str="max_target_level"
 dai_yao_policy:str="terminal_each_meld_and_pair"
 jiang_policy:str="all_triplets_258"
 def __post_init__(self):
  super().__post_init__()
  if self.cha_jiao_mode not in ("max_wait_payment","min_wait_payment","disabled"):raise ValueError("cha jiao mode")
  if self.rule_version!=VERSION or self.combination_policy!="max_target_level" or self.dai_yao_policy!="terminal_each_meld_and_pair" or self.jiang_policy!="all_triplets_258":raise ValueError("unsupported V3 rule definition")
  if (self.concealed_kong_fee,self.added_kong_fee,self.exposed_kong_fee)!=(2,1,2):raise ValueError("V3 specified gang fees")
  if len(dict(self.pattern_levels))!=len(self.pattern_levels) or any(type(v)!=int or not 1<=v<=4 for _,v in self.pattern_levels):raise ValueError("pattern levels")

@lru_cache(maxsize=10000)
def terminal_groups(c):
 if not any(c):return True
 i=next(i for i,n in enumerate(c) if n)
 if c[i]>=3 and i%9 in (0,8):
  a=list(c);a[i]-=3
  if terminal_groups(tuple(a)):return True
 if i%9 in (0,6) and c[i+1] and c[i+2]:
  a=list(c)
  for j in (i,i+1,i+2):a[j]-=1
  if terminal_groups(tuple(a)):return True
 return False

def score_v3(hand,missing,melds=(),config=None,self_draw=False):
 if not winning(hand,missing,len(melds),melds):raise ValueError('not winning')
 c=Counter(hand);alltiles=list(hand)+[t for m in melds for t in m]
 pure=len({t//9 for t in alltiles})==1
 pairs=not melds and all(n%2==0 for n in c.values())
 dragon=pairs and any(n==4 for n in c.values())
 triplets=all(n%3 in (0,2) for n in c.values()) and sum(n%3==2 for n in c.values())==1
 jiang=triplets and all(t%9 in (1,4,7) for t in alltiles)
 dai=False
 if all(m[0]%9 in (0,8) for m in melds):
  for t,n in c.items():
   if n>=2 and t%9 in (0,8):
    a=[c[i] for i in range(27)];a[t]-=2
    if terminal_groups(tuple(a)):dai=True
 levels={'basic':1}
 if triplets:levels['all_triplets']=2
 if pure:levels['pure_suit']=2
 if dai:levels['dai_yao']=2
 if pairs:levels['seven_pairs']=2
 if dragon:levels['dragon_pairs']=3
 if pure and triplets:levels['pure_triplets']=3
 if jiang:levels['jiang_triplets']=3
 if pure and pairs:levels['pure_seven_pairs']=4
 if pure and dragon:levels['pure_dragon_pairs']=4
 config=config or V3Config()
 targets=dict(config.pattern_levels)
 if set(targets)!=set(dict(V3Config().pattern_levels)):raise ValueError("pattern names")
 base=max(targets[k] for k in levels);fan=min(4,base+int(self_draw))
 return {'base_fan':base,'fan':fan,'payment':2**fan,'patterns':list(levels),'rule_version':VERSION,'self_draw':self_draw,'rule_source':'user_specification','room_verified':False,'assumed_components':['dai_yao_decomposition','jiang_258','unlisted_combination_max']}




"""Constrained random prior sampler, NOT a calibrated posterior.
Only explicit observable counts are supported. Never accepts a Table.
"""
from collections import Counter
import random
class UnsupportedObservation(ValueError):pass

def sample_hidden(observation,n=10,seed=42):
 required=('observer_player','observer_hand','public_melds','visible_discards','active','declared_missing_suits','concealed_hand_sizes','remaining_wall_information')
 if any(k not in observation for k in required):raise UnsupportedObservation('Explicit hand-size/public-wall-count schema required')
 o={k:observation[k] for k in required};p=o['observer_player'];sizes=o['concealed_hand_sizes'];active=o['active'];melds=o['public_melds']
 if type(p)!=int or p not in range(4) or len(sizes)!=4 or len(active)!=4 or len(melds)!=4:raise ValueError('four seats required')
 if any(not a for a in active) and observation.get('inactive_archives_complete') is not True:raise UnsupportedObservation('Inactive concealed archives not accounted for')
 if any(type(x)!=int or x<0 or x>14 for x in sizes) or sizes[p]!=len(o['observer_hand']):raise ValueError('hand sizes')
 wall_n=o['remaining_wall_information']
 if type(wall_n)!=int or wall_n<0 or wall_n>108:raise UnsupportedObservation('Public exact wall count required')
 known=list(o['observer_hand'])+[t for _,t in o['visible_discards']]+list(observation.get('public_winning_tiles',[]));unknown_kongs=[];known_melds=[[] for _ in range(4)]
 for q,ms in enumerate(melds):
  for i,m in enumerate(ms):
   if m==[-1]*4:unknown_kongs.append((q,i));known_melds[q].append(None)
   elif len(m) in (3,4) and len(set(m))==1 and all(type(t)==int and t in range(27) for t in m):known.extend(m);known_melds[q].append(list(m))
   else:raise UnsupportedObservation('Unknown meld identity must be a complete four-tile kong')
 if any(type(t)!=int or t not in range(27) for t in known) or any(c>4 for c in Counter(known).values()):raise ValueError('visible inventory')
 expected=len(known)+sum(sizes[q] for q in range(4) if q!=p)+wall_n+4*len(unknown_kongs)
 if expected!=108:raise UnsupportedObservation('Physical inventory including inactive archives must sum to 108')
 if type(n)!=int or n<1 or n>1000:raise ValueError('bounded sample count')
 rng=random.Random(seed);results=[]
 for _ in range(n):
  remaining=Counter({t:4 for t in range(27)});remaining.subtract(known);assigned=[]
  for q,i in unknown_kongs:
   choices=[t for t in range(27) if remaining[t]==4]
   if not choices:raise UnsupportedObservation('No feasible concealed-kong allocation')
   t=rng.choice(choices);remaining[t]-=4;assigned.append(dict(player=q,meld_index=i,tiles=[t]*4))
  pool=[t for t,c in remaining.items() for _ in range(c)];rng.shuffle(pool);hands=[None]*4;hands[p]=list(o['observer_hand']);offset=0
  for q in range(4):
   if q!=p:hands[q]=pool[offset:offset+sizes[q]];offset+=sizes[q]
  wall=pool[offset:];assert len(wall)==wall_n
  physical=known+sum((hands[q] for q in range(4) if q!=p),[])+wall+[t for a in assigned for t in a['tiles']]
  assert Counter(physical)==Counter({t:4 for t in range(27)})
  results.append(dict(concealed_hands=hands,wall=wall,unknown_kongs=assigned,kind='constraint_random_prior_NOT_calibrated_posterior',seed=seed,flags=['NO_OPPONENT_MISSING_SUIT_CLEAR_ASSUMPTION','EXCHANGE_IS_SETUP_EVIDENCE_NOT_HOLDING_CONSTRAINT','INACTIVE_HANDS_REMAIN_IN_POOL']))
 return results

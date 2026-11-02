"""Versioned adapter for D's legal BaselineBot candidate analysis.
Targets encode lexicographic preference ranks, NOT expected terminal returns.
"""
import math
from rules.core import legal_discards
from observations.public import features
FEATURE_NAMES=['tile_scaled','standard_scaled','seven_pairs_scaled','structural_scaled','missing_debt_scaled','effective_scaled','one_draw_truncated_scaled','two_draw_truncated','fan_cap_potential_scaled','public_risk_scaled','seven_pairs_available','details_evaluated']
SCHEMA_VERSION='revision-bot-candidate-v1'
def preference_key(r):return (r['missing_debt'],r['structural'],-r['effective'],-r['two_draw_value'],-r['one_draw_value'],-r['fan_cap_potential'],r['public_risk'])
def adapt(observation,analysis,game_id,seed,source_group):
 p=observation['observer_player'];legal=legal_discards(observation['observer_hand'],observation['declared_missing_suits'][p]);tiles=[r['tile'] for r in analysis]
 if len(set(tiles))!=len(tiles) or set(tiles)!=set(legal):raise ValueError('Analysis does not match legal candidates')
 for r in analysis:
  for k in ['tile','standard','structural','missing_debt','effective','one_draw_value','two_draw_value','fan_cap_potential','public_risk']:
   if not isinstance(r[k],(float,int)) or not math.isfinite(r[k]):raise ValueError('Invalid analysis '+k)
  if r['seven_pairs'] is not None and not math.isfinite(r['seven_pairs']):raise ValueError('Invalid seven pairs')
 best=min((r['missing_debt'],r['structural']) for r in analysis);keys=sorted(set(preference_key(r) for r in analysis));q={k:1-i/max(len(keys)-1,1) for i,k in enumerate(keys)};x=[[0.]*len(FEATURE_NAMES) for _ in range(27)];y=[0.]*27
 for r in analysis:
  t=r['tile'];x[t]=[t/26,r['standard']/8,(r['seven_pairs'] or 0)/8,r['structural']/8,r['missing_debt']/14,r['effective']/108,r['one_draw_value']/108,r['two_draw_value'],r['fan_cap_potential']/4,r['public_risk']/3,float(r['seven_pairs'] is not None),float((r['missing_debt'],r['structural'])==best)];y[t]=q[preference_key(r)]
 return {'game_id':game_id,'seed':seed,'source_group':source_group,'state_features':features(observation),'candidate_features':x,'legal_mask':[t in legal for t in range(27)],'action_targets':y,'target_semantics':'lexicographic_preference_rank','candidate_schema_version':SCHEMA_VERSION,'teacher_definition':'audited BaselineBot lexicographic preference; tile tie excluded from equivalent set','state_target_missing':True}

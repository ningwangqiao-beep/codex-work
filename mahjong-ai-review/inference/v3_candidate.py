"""V3 T2 record adapter. Preference targets are never counterfactual Q returns."""
from models.revision_candidate_schema import adapt,FEATURE_NAMES as LEGACY_NAMES
from inference.v3_observation import encode_observation
FEATURE_NAMES=[('teacher_heuristic_fan_potential_scaled' if n=='fan_cap_potential_scaled' else n) for n in LEGACY_NAMES]
CANDIDATE_SCHEMA='v3-T2-calculator12-preference-v1'
def make_t2_record(observation,analysis,game_id,seed,deal_group_id,source_group='v3-T2'):
 r=adapt(observation,analysis,game_id,seed,source_group);encoded=encode_observation(observation);r.update(encoded);r.update(deal_group_id=deal_group_id,target_semantics='heuristic_preference_rank',candidate_schema_version=CANDIDATE_SCHEMA,teacher_definition='V3 development BaselineBot lexicographic preference, not counterfactual action return')
 r.pop('state_target_missing',None);return r

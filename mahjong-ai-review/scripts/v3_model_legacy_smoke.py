"""Fixture-only V3 legacy migration smoke, no benchmark or training."""
import pathlib,sys,json,hashlib,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from inference.v3_legacy import LegacyV3DiscardPolicy,legacy_static_features
from observations.public import features
from rules.core import legal_discards

torch.set_num_threads(2);o={'observer_player':0,'observer_hand':[0,0,1,2,3,4,5,9,9,10,11,12,13,14],'declared_missing_suits':[2,0,1,2],'visible_discards':[],'public_melds':[[],[],[],[]],'public_winning_tiles':[],'active':[True]*4,'remaining_wall_information':55,'turn_index':0,'current_player':0,'public_action_history':[],'exchange':{'sent':[18,18,18],'received':[0,1,2],'direction':1,'source_player':3}}
assert legacy_static_features(o)==features(o);legal=tuple(legal_discards(o['observer_hand'],2));results=[]
for kind,path in [('static',root/'checkpoints/round2_warmstart/imitation_last.pt'),('candidate',root/'experiments/round2_c/candidate/best.pt'),('residual',root/'checkpoints/round2_candidate_rl_rounded/last.pt')]:
 policy=LegacyV3DiscardPolicy(path,kind);action=policy(o,legal);poison=dict(o,hidden_hands=[[26]*13]*4,future_wall=[25]*50);assert policy(poison,legal)==action;assert action in legal;results.append(dict(policy.metadata,fixture_action=action,hidden_future_invariance=True))
r={'scope':'fixture_migration_only_not_V3_game_performance','results':results,'source_sha256':hashlib.sha256((root/'inference/v3_legacy.py').read_bytes()).hexdigest()};(root/'reports/v3_c_legacy_wrapper_smoke.json').write_text(json.dumps(r,indent=2));print('legacy static/candidate/residual fixture legal & hidden/future invariant PASS')

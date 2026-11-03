"""Explicit legacy-to-V3 legal discard migration, not a V3-trained model.
Old value/risk/loss outputs are never interpreted as V3 score units.
"""
import pathlib,hashlib,torch
from torch import nn
from models.round2_candidate import CandidateLinear,candidate_features
from models.round2_candidate_residual import CandidateResidual
from rules.core import legal_discards

def legacy_static_features(o):
 public=[t for _,t in o['visible_discards']]+[t for ms in o['public_melds'] for m in ms for t in m]+o.get('public_winning_tiles',[])
 v=[o['observer_hand'].count(t)/4 for t in range(27)]+[public.count(t)/4 for t in range(27)]
 v += [float(s==k) for s in o['declared_missing_suits'] for k in range(3)]
 v += list(map(float,o['active']))+[len(ms)/4 for ms in o['public_melds']]+[o['remaining_wall_information']/108,min(o['turn_index'],216)/216]
 v += [float(o['observer_player']==p) for p in range(4)]+[float(o['current_player']==p) for p in range(4)]
 recent=o['public_action_history'][-11:];recent=[{}]*(11-len(recent))+recent
 for e in recent:v += [float(e.get('player',-1)==p)*((e.get('tile',-1)+1)/27+{'discard':0,'peng':1,'exposed_kong':2}.get(e.get('action'),3))/4 for p in range(4)]
 if len(v)!=128:raise ValueError('Legacy feature encoding drift')
 return v
class _Static(nn.Module):
 def __init__(self):
  super().__init__();self.body=nn.Sequential(nn.Linear(128,64),nn.Tanh());self.policy=nn.Linear(64,27);self.value=nn.Linear(64,1)
 def forward(self,x):return self.policy(self.body(x))
class LegacyV3DiscardPolicy:
 def __init__(self,checkpoint,kind,expected_sha256=None):
  p=pathlib.Path(checkpoint);digest=hashlib.sha256(p.read_bytes()).hexdigest()
  if expected_sha256 is not None and digest!=expected_sha256:raise ValueError('Legacy checkpoint hash mismatch')
  s=torch.load(p,map_location='cpu',weights_only=False)
  if kind=='static':self.model=_Static()
  elif kind=='candidate':self.model=CandidateLinear()
  elif kind=='residual':self.model=CandidateResidual(CandidateLinear())
  else:raise ValueError('kind must be static/candidate/residual')
  self.model.load_state_dict(s['model'],strict=True);self.model.eval();self.kind=kind
  self.metadata={'kind':kind,'checkpoint':str(p),'checkpoint_sha256':digest,'trained_under':'legacy_non_V3','evaluation_rule_version':'SICHUAN-XUEZHAN-4FAN-V3','financial_output_compatible':False,'decision_scope':'legal discard only; other actions simulator baseline','flags':['LEGACY_NOT_V3_TRAINED','LEGACY_STATE_VALUE_IGNORED','LEGACY_RISK_AND_LOSS_NOT_V3_SCORES','OWN_EXCHANGE_AND_FULL_HISTORY_NOT_ENCODED']}
 def __call__(self,observation,legal):
  names=['observer_player','observer_hand','declared_missing_suits','visible_discards','public_melds','active','remaining_wall_information','turn_index','current_player','public_action_history']
  o={k:observation[k] for k in names};o['public_winning_tiles']=observation.get('public_winning_tiles',[])
  expected=set(legal_discards(o['observer_hand'],o['declared_missing_suits'][o['observer_player']]))
  if not legal or len(set(legal))!=len(legal) or set(legal)!=expected:raise ValueError('V3 caller legal action mismatch')
  with torch.no_grad():
   if self.kind=='static':scores=self.model(torch.tensor(legacy_static_features(o)).float())[list(legal)]
   else:
    x=torch.tensor([candidate_features(o,t) for t in legal]).float()
    scores=(self.model(x)*64).round() if self.kind=='candidate' else self.model(x)[0]
  if not torch.isfinite(scores).all():raise ValueError('Nonfinite legacy scores')
  return legal[int(scores.argmax())]

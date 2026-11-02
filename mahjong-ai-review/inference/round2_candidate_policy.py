"""Legal-observation candidate callback. Teacher distillation, no strength claim."""
import pathlib,hashlib,torch
from models.round2_candidate import CandidateLinear,candidate_features
from rules.core import legal_discards
class CandidatePolicy:
 def __init__(self,checkpoint,verify_source=True):
  self.root=pathlib.Path(__file__).resolve().parents[1];self.checkpoint=pathlib.Path(checkpoint);s=torch.load(checkpoint,map_location='cpu',weights_only=False)
  if s.get('model_version')!='candidate-linear-teacher-v1':raise ValueError('Unsupported model version')
  if verify_source:
   for relative,sha in s['source'].items():
    if hashlib.sha256((self.root/relative).read_bytes()).hexdigest()!=sha:raise ValueError('Checkpoint source drift: '+relative)
  self.model=CandidateLinear();self.model.load_state_dict(s['model']);self.model.eval();self.version=s['model_version'];self.last_scores=None
 def __call__(self,observation,legal):
  # Explicit whitelist: simulator hidden hands/wall/future never read.
  o={k:observation[k] for k in ('observer_player','observer_hand','declared_missing_suits','visible_discards','public_melds')};o['public_winning_tiles']=observation.get('public_winning_tiles',[])
  expected=set(legal_discards(o['observer_hand'],o['declared_missing_suits'][o['observer_player']]))
  if not legal or len(set(legal))!=len(legal) or set(legal)!=expected:raise ValueError('Caller legal actions disagree with audited own-hand rules')
  with torch.no_grad():scores=self.model(torch.tensor([candidate_features(o,t) for t in legal]).float())*64
  self.last_scores=scores.tolist()
  # Teacher utility is integer; round removes floating tie noise, preserves legal order.
  return legal[int(scores.round().argmax())]

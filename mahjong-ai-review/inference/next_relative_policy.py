"""Frozen V3 T2 preference callback. State V is diagnostic, never action Q."""
import pathlib,json,hashlib,torch
from models.next_relative_v3 import RelativeV3ActionValueNet as V3ActionValueNet
from baselines.v3_bot import BaselineV3
from models.revision_candidate_schema import adapt
from inference.v3_observation import encode_observation
class RelativePolicy:
 def __init__(self,checkpoint,root=None):
  self.root=pathlib.Path(root) if root else pathlib.Path(__file__).resolve().parents[1];p=pathlib.Path(checkpoint);s=torch.load(p,map_location='cpu',weights_only=False)
  if s.get('version')!='NEXT-HISTORY100-RELATIVE-PAIRWISE-v1' or s.get('rule_version')!='SICHUAN-XUEZHAN-4FAN-V3':raise ValueError('Unsupported checkpoint')
  for rel,digest in s['source_hashes'].items():
   if hashlib.sha256((self.root/rel).read_bytes()).hexdigest()!=digest:raise ValueError('Trained model source drift '+rel)
  manifest=self.root/'datasets/next_history100/manifest.json'
  if hashlib.sha256(manifest.read_bytes()).hexdigest()!=s['data_admission']['manifest_sha256']:raise ValueError('Training manifest drift')
  m=json.load(open(manifest))
  for rel,digest in m['source_hashes'].items():
   if hashlib.sha256((self.root/rel).read_bytes()).hexdigest()!=digest:raise ValueError('Calculator/data source drift '+rel)
  config=s['model_config'];self.model=V3ActionValueNet(**{k:config[k] for k in ['state_dim','candidate_dim','hidden']});self.model.load_state_dict(s['model']);self.model.eval();self.calculator=BaselineV3();self.metadata={'checkpoint':str(p),'checkpoint_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rule_version':s['rule_version'],'binding':s['binding'],'action_semantics':'teacher preference rank NOT terminal action Q','state_semantics':s['head_semantics']['state'],'decision_scope':'discard-only; other stages remain simulator baselines','training_games':100,'validation_games':20,'rl_performed':False};self.last_state_v=None;self.last_decision=None;self.metadata['checkpoint_epoch']=s['epoch'];self.metadata['loss_mode']=s['config']['loss_mode'];self.metadata['state_head_supervised']=s['config']['loss_mode']=='multitask'
 def __call__(self,o,legal):
  # Calculator only receives public observation. adapt checks legal candidates.
  teacher=self.calculator(o,legal);r=adapt(o,self.calculator.last_analysis,'inference',0,'V3-T2');e=encode_observation(o);tokens=e['history_tokens'] or [[0,4,0]];hm=e['history_mask'] or [False]
  inputs=(torch.tensor([e['state_features']]).float(),torch.tensor([r['candidate_features']]).float(),torch.tensor([r['legal_mask']],dtype=torch.bool),torch.tensor([tokens],dtype=torch.long),torch.tensor([hm],dtype=torch.bool))
  with torch.inference_mode():output=self.model(*inputs)
  self.last_state_v=float(output['state_value'][0]);scores=output['action_value'][0]
  chosen=max(legal,key=lambda t:float(scores[t]));rows={r['tile']:r for r in self.calculator.last_analysis};a=rows[chosen];b=rows[teacher];missing=o['declared_missing_suits'][o['observer_player']];free=not any(t//9==missing for t in o['observer_hand']);self.last_decision={'free':free,'exact':chosen==teacher,'equivalent':r['action_targets'][chosen]==r['action_targets'][teacher],'rank_regret':r['action_targets'][teacher]-r['action_targets'][chosen],'ukeire_regret':b['effective']-a['effective'],'same_structural':a['structural']==b['structural'],'higher_structural':a['structural']>b['structural'],'higher_missing_debt':a['missing_debt']>b['missing_debt']};return chosen

"""Small shared public-state encoder plus per-candidate calculator features.
Q is a supervised target estimate; semantics are supplied by audited dataset,
not automatically a whole-game return or an RL value function.
"""
import torch
from torch import nn
class ActionValueNet(nn.Module):
 def __init__(self,state_dim=128,candidate_dim=12,hidden=32):
  super().__init__();self.config=dict(state_dim=state_dim,candidate_dim=candidate_dim,hidden=hidden)
  self.state_encoder=nn.Sequential(nn.Linear(state_dim,hidden),nn.ReLU())
  self.candidate_encoder=nn.Sequential(nn.Linear(candidate_dim,16),nn.ReLU())
  self.joint=nn.Sequential(nn.Linear(hidden+16,hidden),nn.ReLU())
  self.action_value=nn.Linear(hidden,1);self.state_value=nn.Linear(hidden,1)
 def forward(self,state,candidates,legal_mask):
  if state.ndim!=2 or candidates.ndim!=3 or candidates.shape[:2]!=legal_mask.shape or state.shape[0]!=candidates.shape[0] or state.shape[-1]!=self.config['state_dim'] or candidates.shape[-1]!=self.config['candidate_dim']:raise ValueError('Shape mismatch')
  if legal_mask.dtype!=torch.bool or not legal_mask.any(-1).all():raise ValueError('Nonempty boolean legal mask required')
  if not torch.isfinite(state).all() or not torch.isfinite(candidates).all():raise ValueError('Nonfinite inputs')
  z=self.state_encoder(state);c=self.candidate_encoder(candidates);h=self.joint(torch.cat((z.unsqueeze(1).expand(-1,c.shape[1],-1),c),-1));q=self.action_value(h).squeeze(-1)
  return {'action_value':q,'masked_action_value':q.masked_fill(~legal_mask,float('-inf')),'state_value':self.state_value(z).squeeze(-1)}

def supervised_losses(output,targets,legal_mask,tolerance=0.):
 q=output['action_value'];y=targets['action_targets']
 if q.shape!=y.shape or not torch.isfinite(y[legal_mask]).all():raise ValueError('Invalid action targets')
 error=(q-torch.where(legal_mask,y,torch.zeros_like(y))).square();regression=((error*legal_mask).sum(-1)/legal_mask.sum(-1)).mean()
 best=y.masked_fill(~legal_mask,float('-inf')).max(-1,keepdim=True).values;optimal=(y>=best-tolerance)&legal_mask;logp=output['masked_action_value'].log_softmax(-1);ranking=-(torch.where(optimal,logp,torch.zeros_like(logp)).sum(-1)/optimal.sum(-1)).mean()
 losses={'action_value_mse':regression,'equivalent_ranking_ce':ranking}
 if 'state_targets' in targets:
  target=targets['state_targets']
  if target.shape!=output['state_value'].shape or not torch.isfinite(target).all():raise ValueError('Invalid state targets')
  losses['state_value_mse']=(output['state_value']-target).square().mean()
 return losses

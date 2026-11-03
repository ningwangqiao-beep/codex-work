"""Explicit combined direction: relative candidate features + pairwise targets.
Not a one-factor causal ablation; same state/history backbone and head widths.
"""
import torch
from models.v3_action_value import V3ActionValueNet
from models.next_candidate import pairwise_teacher_loss
from training.v3_losses import v3_losses
class RelativeV3ActionValueNet(V3ActionValueNet):
 def __init__(self,state_dim=191,candidate_dim=12,hidden=32):
  super().__init__(state_dim,candidate_dim*2,hidden);self.raw_candidate_dim=candidate_dim;self.config.update(candidate_dim=candidate_dim,representation='raw_plus_legal_relative_v1')
 def forward(self,state,candidates,legal_mask,history_tokens,history_mask):
  if candidates.shape[-1]!=self.raw_candidate_dim or not legal_mask.any(-1).all():raise ValueError('Bad relative candidate inputs')
  mask=legal_mask.unsqueeze(-1);n=mask.sum(1,keepdim=True);mean=(candidates*mask).sum(1,keepdim=True)/n;scale=(((candidates-mean).square()*mask).sum(1,keepdim=True)/n).sqrt().clamp_min(.01);relative=(candidates-mean)/scale
  return super().forward(state,torch.cat((candidates,relative),-1),legal_mask,history_tokens,history_mask)
def relative_losses(output,targets,legal_mask,tolerance=0.):
 ls=v3_losses(output,targets,legal_mask,tolerance);ls.pop('equivalent_ranking_ce');ls['pairwise_preference']=pairwise_teacher_loss(output['action_value'],targets['action_targets'],legal_mask);return ls

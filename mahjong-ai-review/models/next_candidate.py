"""Small candidate-relative teacher rank model, NOT terminal Q or RL."""
import torch
from torch import nn
class RelativeCandidateRanker(nn.Module):
 def __init__(self,state_dim=191,candidate_dim=12):
  super().__init__();self.state=nn.Sequential(nn.Linear(state_dim,32),nn.ReLU());self.candidate=nn.Sequential(nn.Linear(candidate_dim*2,32),nn.ReLU());self.rank=nn.Sequential(nn.Linear(64,16),nn.ReLU(),nn.Linear(16,1))
 def forward(self,state,candidates,mask):
  if mask.dtype!=torch.bool or candidates.shape[:2]!=mask.shape or not mask.any(-1).all():raise ValueError('Invalid candidate mask')
  if not torch.isfinite(state).all() or not torch.isfinite(candidates).all():raise ValueError('Nonfinite features')
  m=mask.unsqueeze(-1);n=m.sum(1,keepdim=True);mean=(candidates*m).sum(1,keepdim=True)/n;spread=(((candidates-mean).square()*m).sum(1,keepdim=True)/n).sqrt().clamp_min(.01);relative=(candidates-mean)/spread;c=self.candidate(torch.cat((candidates,relative),-1));z=self.state(state).unsqueeze(1).expand(-1,c.shape[1],-1);return self.rank(torch.cat((z,c),-1)).squeeze(-1).masked_fill(~mask,float('-inf'))
def pairwise_teacher_loss(scores,target,mask):
 better=(target.unsqueeze(2)>target.unsqueeze(1))&mask.unsqueeze(2)&mask.unsqueeze(1);difference=scores.unsqueeze(2)-scores.unsqueeze(1);safe=torch.where(better,difference,torch.zeros_like(difference));loss=torch.nn.functional.softplus(.1-safe);per_state=(loss*better).sum((1,2))/better.sum((1,2)).clamp_min(1);return per_state.mean()

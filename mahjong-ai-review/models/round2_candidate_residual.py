"""Zero-initialized bounded residual around frozen teacher candidate scorer.
Interface only; not RL-trained or evaluated for strength.
"""
import torch
from torch import nn
from torch.distributions import Categorical
class CandidateResidual(nn.Module):
 def __init__(self,frozen_base,amplitude=1.):
  super().__init__();self.base=frozen_base;self.base.requires_grad_(False);self.amplitude=amplitude;self.residual=nn.Sequential(nn.Linear(12,16),nn.Tanh(),nn.Linear(16,1));nn.init.zeros_(self.residual[-1].weight);nn.init.zeros_(self.residual[-1].bias);self.value=nn.Sequential(nn.Linear(24,16),nn.Tanh(),nn.Linear(16,1))
 def forward(self,candidates):
  if candidates.ndim!=2 or candidates.shape[0]<1 or candidates.shape[1]!=12:raise ValueError('Expected nonempty legal candidate features [N,12]')
  with torch.no_grad():base=(self.base(candidates)*64).round()
  logits=base+self.amplitude*self.residual(candidates).squeeze(-1).tanh();v=self.value(torch.cat((candidates.mean(0),candidates.max(0).values))).squeeze(-1)
  return logits,v
 def distribution(self,candidates,temperature=1.):
  if temperature<=0:raise ValueError('positive temperature required')
  logits,v=self(candidates);return Categorical(logits=logits/temperature),v


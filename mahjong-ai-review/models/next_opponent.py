"""Same-parameter public-information ablations; no scores/hidden inputs."""
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence
FAMILIES=('counts','progress','history','exchange','history_shuffled')
class OpponentAblation(nn.Module):
 def __init__(self,family='counts'):
  super().__init__()
  if family not in FAMILIES:raise ValueError('Unknown input family')
  self.family=family;mask=torch.zeros(191);mask[:74]=1;mask[76:80]=1
  if family!='counts':mask[74:76]=1;mask[190]=1
  if family=='exchange':mask[128:190]=1
  self.register_buffer('static_mask',mask);self.static=nn.Sequential(nn.Linear(191,32),nn.ReLU());self.action=nn.Embedding(16,5);self.player=nn.Embedding(5,3);self.tile=nn.Embedding(28,8);self.history=nn.GRU(16,16,batch_first=True);self.fuse=nn.Sequential(nn.Linear(48,32),nn.ReLU());self.tenpai=nn.Linear(32,3);self.wait=nn.Linear(32,81);self.joint=nn.Linear(32,216)
 def forward(self,state,tokens,history_mask):
  if state.shape[-1]!=191 or tokens.dtype!=torch.long or history_mask.dtype!=torch.bool:raise ValueError('Invalid input schema')
  if tokens.shape[:2]!=history_mask.shape or tokens.shape[-1]!=3 or tokens.shape[1]<1 or (history_mask[:,1:]&~history_mask[:,:-1]).any():raise ValueError('Invalid padded history')
  h=torch.zeros(len(state),16,device=state.device)
  if self.family in ('history','exchange','history_shuffled'):
   lengths=history_mask.sum(-1);e=torch.cat((self.action(tokens[:,:,0]),self.player(tokens[:,:,1]),self.tile(tokens[:,:,2])),-1);_,hidden=self.history(pack_padded_sequence(e,lengths.clamp_min(1).cpu(),batch_first=True,enforce_sorted=False));h=hidden[-1]*lengths.gt(0).unsqueeze(-1)
  z=self.fuse(torch.cat((self.static(state*self.static_mask),h),-1));return {'structural_tenpai_logits':self.tenpai(z),'conditional_structural_wait_logits':self.wait(z).reshape(-1,3,27),'legal_candidate_joint_logits':self.joint(z).reshape(-1,27,8)}

"""Small shared-state/full-public-history candidate action-value prototype.
Untrained interface only; financial semantics require audited V3 return labels.
"""
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence
from models.revision_action_value import ActionValueNet
class V3ActionValueNet(nn.Module):
 def __init__(self,state_dim=191,candidate_dim=12,hidden=32):
  super().__init__();self.config=dict(state_dim=state_dim,candidate_dim=candidate_dim,hidden=hidden,rule_version='SICHUAN-XUEZHAN-4FAN-V3',history_schema='action_relative_player_tile_v1')
  self.action_embedding=nn.Embedding(16,5);self.player_embedding=nn.Embedding(5,3);self.tile_embedding=nn.Embedding(28,8);self.history_encoder=nn.GRU(16,16,batch_first=True);self.heads=ActionValueNet(state_dim+16,candidate_dim,hidden);self.tenpai_head=nn.Linear(hidden,3);self.wait_head=nn.Linear(hidden,81);self.joint_risk_head=nn.Linear(hidden,27*8)
 def forward(self,state,candidates,legal_mask,history_tokens,history_mask):
  if history_tokens.ndim!=3 or history_tokens.shape[-1]!=3 or history_tokens.shape[:2]!=history_mask.shape or len(history_tokens)!=len(state) or history_tokens.dtype!=torch.long or history_mask.dtype!=torch.bool:raise ValueError('Invalid history shape/type')
  if history_mask.shape[1]==0:raise ValueError('Pad empty histories to one masked token')
  if (history_mask[:,1:] & ~history_mask[:,:-1]).any():raise ValueError('History mask must be contiguous prefix')
  for i,limit in enumerate((16,5,28)):
   if ((history_tokens[:,:,i]<0)|(history_tokens[:,:,i]>=limit)).any():raise ValueError('History token out of range')
  lengths=history_mask.sum(-1);emb=torch.cat((self.action_embedding(history_tokens[:,:,0]),self.player_embedding(history_tokens[:,:,1]),self.tile_embedding(history_tokens[:,:,2])),-1);packed=pack_padded_sequence(emb,lengths.clamp_min(1).cpu(),batch_first=True,enforce_sorted=False);_,h=self.history_encoder(packed);history=h[-1]*lengths.gt(0).unsqueeze(-1);output=self.heads(torch.cat((state,history),-1),candidates,legal_mask);output['history_encoded_length']=lengths;z=self.heads.state_encoder(torch.cat((state,history),-1));output['tenpai_logits']=self.tenpai_head(z);output['conditional_wait_logits']=self.wait_head(z).reshape(-1,3,27);output['joint_risk_logits']=self.joint_risk_head(z).reshape(-1,27,8);return output

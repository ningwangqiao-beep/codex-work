"""Shared per-opponent/per-tile scoring. Missing-zero is programmed rule logic."""
import torch
from torch import nn
FAMILIES=('shared_tile',)
FEATURE_NAMES=('own_count','public_count','unknown_pool_count','is_target_missing','target_missing_0','target_missing_1','target_missing_2','tile_suit_0','tile_suit_1','tile_suit_2','tile_rank','target_public_meld_tile_count','target_meld_count','target_active')
class SharedTileOpponent(nn.Module):
 def __init__(self,family='shared_tile'):
  super().__init__()
  if family!='shared_tile':raise ValueError('Only shared_tile architecture')
  self.family=family;mask=torch.zeros(191);mask[:80]=1;mask[190]=1;self.register_buffer('static_mask',mask)
  self.static=nn.Sequential(nn.Linear(191,32),nn.ReLU());self.fuse=nn.Sequential(nn.Linear(48,32),nn.ReLU());self.tile=nn.Embedding(27,4);self.opponent=nn.Embedding(3,2);self.scorer=nn.Sequential(nn.Linear(52,16),nn.ReLU(),nn.Linear(16,1));self.tenpai=nn.Linear(32,3);self.joint=nn.Linear(32,216)
 def forward(self,state,tile_features):
  if state.ndim!=2 or state.shape[-1]!=191 or tile_features.shape!=(len(state),3,27,14) or not torch.isfinite(state).all() or not torch.isfinite(tile_features).all():raise ValueError('Invalid public tile input schema')
  z=self.fuse(torch.cat((self.static(state*self.static_mask),state.new_zeros(len(state),16)),-1));context=z[:,None,None,:].expand(-1,3,27,-1);tile=self.tile(torch.arange(27,device=state.device))[None,None,:,:].expand(len(state),3,-1,-1);opponent=self.opponent(torch.arange(3,device=state.device))[None,:,None,:].expand(len(state),-1,27,-1)
  raw=self.scorer(torch.cat((context,tile_features,tile,opponent),-1)).squeeze(-1);wait=raw.masked_fill(tile_features[:,:,:,3].bool(),torch.finfo(raw.dtype).min)
  return {'structural_tenpai_logits':self.tenpai(z),'conditional_structural_wait_logits':wait,'conditional_structural_wait_raw_logits':raw,'legal_candidate_joint_logits':self.joint(z).reshape(-1,27,8)}

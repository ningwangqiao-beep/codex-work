"""Separate V3 target losses; no old-rule loss labels admitted implicitly."""
import torch
from models.revision_action_value import supervised_losses

def v3_losses(output,targets,legal_mask,tolerance=0.):
 losses=supervised_losses(output,targets,legal_mask,tolerance)
 if 'tenpai' in targets:
  y=targets['tenpai'];active=targets['target_active'].bool()
  if y.shape!=output['tenpai_logits'].shape or active.shape!=y.shape or not torch.isfinite(y).all() or ((y!=0)&(y!=1)).any():raise ValueError('Invalid V3 tenpai labels')
  losses['tenpai_bce']=(torch.nn.functional.binary_cross_entropy_with_logits(output['tenpai_logits'],y,reduction='none')*active).sum()/active.sum().clamp_min(1)
 if 'conditional_waits' in targets:
  y=targets['conditional_waits'];mask=(targets['tenpai']*targets['target_active']).bool().unsqueeze(-1).expand_as(y)
  if y.shape!=output['conditional_wait_logits'].shape or not torch.isfinite(y).all() or ((y!=0)&(y!=1)).any():raise ValueError('Invalid V3 wait labels')
  losses['conditional_wait_bce']=(torch.nn.functional.binary_cross_entropy_with_logits(output['conditional_wait_logits'],y,reduction='none')*mask).sum()/mask.sum().clamp_min(1)
 if 'joint_winner_mask' in targets:
  y=targets['joint_winner_mask']
  if y.shape!=legal_mask.shape or ((y<0)|(y>7)|(y!=y.round())).any():raise ValueError('Invalid V3 joint labels')
  loss=torch.nn.functional.cross_entropy(output['joint_risk_logits'].reshape(-1,8),y.long().flatten(),reduction='none').reshape_as(legal_mask);losses['joint_risk_ce']=(loss*legal_mask).sum()/legal_mask.sum().clamp_min(1)
 return losses

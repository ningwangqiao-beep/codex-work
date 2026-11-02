"""Legal-candidate value metrics; equivalent actions are tolerance-defined."""
import torch

def action_value_metrics(predicted,target,mask,tolerance=0.,action_ids=None):
 if predicted.shape!=target.shape or predicted.shape!=mask.shape or predicted.ndim!=2 or mask.dtype!=torch.bool or not mask.any(-1).all() or tolerance<0:raise ValueError('Invalid shapes/mask/tolerance')
 if not torch.isfinite(predicted[mask]).all() or not torch.isfinite(target[mask]).all():raise ValueError('Invalid values')
 q=predicted.masked_fill(~mask,float('-inf'));y=target.masked_fill(~mask,float('-inf'));teacher=y.argmax(-1);chosen=q.argmax(-1);best=y.max(-1).values;chosen_target=y.gather(1,chosen[:,None]).squeeze(1);equivalent=chosen_target>=best-tolerance;order=q.argsort(dim=-1,descending=True,stable=True);n=len(q)
 r={'n':n,'exact_rate':float((chosen==teacher).float().mean()),'equivalent_rate':float(equivalent.float().mean()),'teacher_value_regret_mean':float((best-chosen_target).mean()),'teacher_value_regret_max':float((best-chosen_target).max()),'legal_action_mse':float(((predicted[mask]-target[mask])**2).mean()),'tolerance':tolerance}
 for k in (1,3,5):
  selected=order[:,:min(k,q.shape[1])];islegal=mask.gather(1,selected);included=(selected==teacher[:,None])&islegal;values=y.gather(1,selected);r['top'+str(k)+'_exact_rate']=float(included.any(-1).float().mean());r['top'+str(k)+'_equivalent_rate']=float(((values>=best[:,None]-tolerance)&islegal).any(-1).float().mean())
 return r


"""Affine binary calibration fixes bias and confidence; validation-only fit."""
import torch

def fit_affine(logits,y):
    x=logits.detach().float().cpu().flatten();y=y.detach().float().cpu().flatten()
    if x.shape!=y.shape or not x.numel() or not torch.isfinite(x).all() or not torch.isfinite(y).all() or ((y!=0)&(y!=1)).any():raise ValueError('Invalid calibration data')
    a=torch.tensor(1.,requires_grad=True);b=torch.tensor(0.,requires_grad=True);opt=torch.optim.LBFGS([a,b],max_iter=40,line_search_fn='strong_wolfe')
    def closure():
        opt.zero_grad();loss=torch.nn.functional.binary_cross_entropy_with_logits(a.clamp(.01,20)*x+b,y);loss.backward();return loss
    opt.step(closure)
    return {'slope':float(a.detach().clamp(.01,20)),'intercept':float(b.detach())}

def calibrated(logits,params):return (logits*params['slope']+params['intercept']).sigmoid()

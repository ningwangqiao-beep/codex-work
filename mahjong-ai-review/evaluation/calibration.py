"""Temperature fitted only against validation logits."""
import torch

def fit_temperature(logits,labels):
    if logits.shape!=labels.shape or not logits.numel() or not torch.isfinite(logits).all() or not torch.isfinite(labels).all() or ((labels!=0)&(labels!=1)).any(): raise ValueError('Invalid calibration inputs')
    logits=logits.detach(); labels=labels.detach().float(); log_t=torch.zeros((),device=logits.device,requires_grad=True)
    opt=torch.optim.LBFGS([log_t],max_iter=30)
    def closure():
        opt.zero_grad(); loss=torch.nn.functional.binary_cross_entropy_with_logits(logits/log_t.exp().clamp(.05,20),labels);loss.backward();return loss
    opt.step(closure)
    return float(log_t.detach().exp().clamp(.05,20))

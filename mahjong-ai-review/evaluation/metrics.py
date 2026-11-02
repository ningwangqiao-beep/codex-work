import torch

def binary_metrics(p,y,bins=10):
    p=torch.as_tensor(p).detach().float().cpu(); y=torch.as_tensor(y).detach().float().cpu()
    if p.shape!=y.shape or not p.numel(): raise ValueError('Shape mismatch or empty input')
    if bins<1 or not torch.isfinite(p).all() or not torch.isfinite(y).all() or ((p<0)|(p>1)).any() or ((y!=0)&(y!=1)).any(): raise ValueError('Invalid probabilities/labels')
    p=p.flatten(); y=y.flatten(); order=torch.argsort(p,descending=True); sy=y[order]
    _,counts=torch.unique_consecutive(p[order],return_counts=True); ends=counts.cumsum(0)-1
    tp=sy.cumsum(0)[ends]; fp=(1-sy).cumsum(0)[ends]; pos=y.sum(); neg=(1-y).sum()
    ap=float(((tp-torch.cat((torch.zeros(1),tp[:-1])))*(tp/(tp+fp))).sum()/pos) if pos else None
    auc=float(torch.trapz(torch.cat((torch.zeros(1),tp/pos)),torch.cat((torch.zeros(1),fp/neg)))) if pos and neg else None
    ece=0.
    for i in range(bins):
        mask=(p>=i/bins)&((p<((i+1)/bins)) if i<bins-1 else (p<=1))
        if mask.any(): ece+=float(mask.float().mean()*(p[mask].mean()-y[mask].mean()).abs())
    pc=p.clamp(1e-7,1-1e-7)
    return {'n':len(y),'positive':int(pos),'roc_auc':auc,'average_precision':ap,'brier':float(((p-y)**2).mean()),'log_loss':float(-(y*pc.log()+(1-y)*(1-pc).log()).mean()),'ece':ece}

"""Versioned local checkpoint inference."""
import torch
from evaluation.round2_io import load_checkpoint
class Predictor:
    def __init__(self,path,device='cpu'):
        self.model,s=load_checkpoint(path,device);self.device=device;self.version=s.get('dataset_version','unknown')+':epoch'+str(s['epoch']);self.temperature=s.get('temperature',1.)
    def predict(self,features):
        x=torch.as_tensor(features,dtype=torch.float32,device=self.device)
        if x.ndim==1:x=x.unsqueeze(0)
        if x.shape[-1]!=self.model.config.get('feature_dim',128) or not torch.isfinite(x).all():raise ValueError('Invalid features')
        r=self.model.predict(x,self.temperature,self.version)
        return {k:v.cpu().tolist() if torch.is_tensor(v) else v for k,v in r.items()}

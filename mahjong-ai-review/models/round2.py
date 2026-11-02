"""Round2 causal feature ablations; no hidden state or old test access."""
import torch
from torch import nn
from models.networks import MahjongBrain

SLICES={'A':[(27,54)],'B':[(27,66)],'C':[(27,66),(70,74)],'D':[(27,66),(70,74),(84,128)],'E':[(0,128)],'F':[(0,128)]}

class AblationBrain(MahjongBrain):
    def __init__(self,variant='E',hidden=64,loss_bins=(0,1)):
        super().__init__(128,hidden,loss_bins);self.variant=variant
        mask=torch.zeros(128)
        for a,b in SLICES[variant]:mask[a:b]=1
        self.register_buffer('feature_mask',mask)
        self.history=nn.GRU(4,16,batch_first=True) if variant=='F' else None
        if self.history is not None:self.history_project=nn.Linear(16,44)
        self.config.update(variant=variant)
    def forward(self,x):
        x=x*self.feature_mask
        if self.history is not None:
            _,h=self.history(x[:,84:].reshape(-1,11,4));x=torch.cat((x[:,:84],self.history_project(h[-1])),dim=-1)
        return super().forward(x)

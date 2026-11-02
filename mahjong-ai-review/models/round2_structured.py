"""Deterministic tile/suit structure from legal 128-vector only."""
import torch
from models.networks import MahjongBrain
class StructuredBrain(MahjongBrain):
    def __init__(self,hidden=64,loss_bins=(0,1)):
        super().__init__(185,hidden,loss_bins);self.config={'architecture':'structured-v1','hidden':hidden,'loss_bins':list(loss_bins)}
    def forward(self,x):
        own=x[:,:27];public=x[:,27:54];live=(1-own-public).clamp(0,1);suits=own.reshape(-1,3,9);pairs=(suits>=.5).float().sum(-1)/9;triples=(suits>=.75).float().sum(-1)/9
        adjacent=(suits[:,:,:7]*suits[:,:,1:8]*suits[:,:,2:9]).reshape(-1,21)
        extra=torch.cat((live,live.reshape(-1,3,9).mean(-1),pairs,triples,adjacent),-1)
        return super().forward(torch.cat((x,extra),-1))

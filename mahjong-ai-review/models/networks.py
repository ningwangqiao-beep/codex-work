"""Shared encoder; separate supervised heads, explicit probability diagnostics."""
import torch
from torch import nn
class MahjongBrain(nn.Module):
    def __init__(self,feature_dim=128,hidden=64,loss_bins=(0.,1.,2.,4.,8.,16.,32.,48.)):
        super().__init__();self.config={'feature_dim':feature_dim,'hidden':hidden,'loss_bins':list(loss_bins)}
        self.register_buffer('loss_bins',torch.tensor(loss_bins,dtype=torch.float32))
        self.encoder=nn.Sequential(nn.Linear(feature_dim,hidden),nn.ReLU(),nn.Linear(hidden,hidden),nn.ReLU())
        self.tenpai=nn.Linear(hidden,3);self.waits=nn.Linear(hidden,81);self.joint=nn.Linear(hidden,216);self.score=nn.Linear(hidden,27*len(loss_bins))
    def forward(self,x):
        z=self.encoder(x)
        return {'tenpai_logits':self.tenpai(z),'conditional_wait_logits':self.waits(z).reshape(-1,3,27),'joint_logits':self.joint(z).reshape(-1,27,8),'loss_logits':self.score(z).reshape(-1,27,len(self.loss_bins))}
    def predict(self,x,temperature=1.,version='untrained-schema-v2'):
        self.eval()
        with torch.no_grad():
            o=self(x);t=(o['tenpai_logits']/temperature).sigmoid();w=o['conditional_wait_logits'].sigmoid();j=o['joint_logits'].softmax(-1);s=o['loss_logits'].softmax(-1)
            bits=torch.tensor([[bool(k&(1<<i)) for k in range(8)] for i in range(3)],device=x.device,dtype=x.dtype)
            marginal=torch.einsum('btk,ik->bit',j,bits);delta=(marginal-t.unsqueeze(-1)*w).abs()
            return {'model_version':version,'tenpai_probability':t,'wait_given_tenpai':w,'wait_product_probability':t.unsqueeze(-1)*w,'opponent_deal_in_probability':marginal,'deal_in_probability':1-j[:,:,0],'joint_winner_distribution':j,'loss_distribution':s,'expected_loss':(s*self.loss_bins).sum(-1),'marginal_disagreement':delta,'flags':['UNCALIBRATED_JOINT','HEADS_NOT_PROBABILISTICALLY_CONSTRAINED']}
# Public names denote one shared multitask implementation, not independently trained networks.
OpponentNet=MahjongBrain
TenpaiWaitNet=MahjongBrain
DealInRiskNet=MahjongBrain

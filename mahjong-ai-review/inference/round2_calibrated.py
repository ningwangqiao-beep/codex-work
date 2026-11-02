"""Research calibration preserving a coherent any-winner/joint distribution.
Wait-head predictions remain separately supervised and diagnostic, not asserted
identical to joint marginals. Only calibration-fit validation groups permitted.
"""
import json,torch
from inference.predictor import Predictor
class CalibratedPredictor(Predictor):
    def __init__(self,checkpoint,calibration,device='cpu'):
        super().__init__(checkpoint,device);self.calibration=json.load(open(calibration))
    def predict(self,features):
        r=super().predict(features)
        def apply(p,task):
            v=torch.as_tensor(p).float().clamp(1e-7,1-1e-7);result=self.calibration['tasks'][task];before=result['before'];after=result['after']
            if not (after['brier']<=before['brier'] and after['log_loss']<=before['log_loss'] and (after['brier']<before['brier'] or after['log_loss']<before['log_loss'])):return v
            param=result['parameters'];return (torch.logit(v)*param['slope']+param['intercept']).sigmoid()
        w=apply(r['wait_given_tenpai'],'wait');risk=apply(r['deal_in_probability'],'risk');joint=torch.tensor(r['joint_winner_distribution']);positive=joint[:,:,1:];positive=positive/positive.sum(-1,keepdim=True).clamp_min(1e-12)*risk.unsqueeze(-1);joint=torch.cat(((1-risk).unsqueeze(-1),positive),-1)
        bits=torch.tensor([[bool(k&(1<<i)) for k in range(8)] for i in range(3)]).float();marginal=torch.einsum('btk,ik->bit',joint,bits);t=apply(r['tenpai_probability'],'tenpai');product=t.unsqueeze(-1)*w
        r.update(tenpai_probability=t.tolist(),wait_given_tenpai=w.tolist(),deal_in_probability=risk.tolist(),joint_winner_distribution=joint.tolist(),opponent_deal_in_probability=marginal.tolist(),wait_product_probability=product.tolist(),marginal_disagreement=(marginal-product).abs().tolist())
        r['flags']=['RESEARCH_ONLY','SIMULATOR_ONLY','SCORE_SUPPORT_EMPIRICAL','TAIL_UNVALIDATED','WAIT_AND_JOINT_HEADS_NOT_CONSTRAINED','VALIDATION_CALIBRATION_NOT_REAL_PLAYER_VALIDATION','CALLER_MUST_ENFORCE_LEGALITY_MASKS']
        return r

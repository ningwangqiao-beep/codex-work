import pathlib,sys,torch,json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from evaluation.metrics import binary_metrics
from evaluation.calibration import fit_temperature
from training.streaming import pack,losses
from models.networks import MahjongBrain
p=torch.tensor([.5,.5]); a=binary_metrics(p,torch.tensor([0.,1.]));b=binary_metrics(p,torch.tensor([1.,0.]));assert a==b and a['average_precision']==.5 and a['roc_auc']==.5
for p,y in [(torch.tensor([float('nan')]),torch.tensor([0.])),(torch.tensor([1.1]),torch.tensor([1.])),(torch.tensor([.5]),torch.tensor([2.]))]:
    try:binary_metrics(p,y)
    except ValueError:pass
    else:raise AssertionError('invalid accepted')
t=fit_temperature(torch.tensor([-1.,1.]),torch.tensor([0.,1.]));assert .05<=t<=20
r={'features':[0.]*128,'tenpai':[0.,1.,0.],'waits':[[0.]*27 for _ in range(3)],'joint_outcome':[0]*27,'loss':[0]*27}
m=MahjongBrain().cuda();ls=losses(m,pack([r,r],'cuda'));sum(ls.values()).backward()
print(json.dumps({'tie_metrics':a,'temperature':t,'stream_batch_backward':True,'synthetic_only':True}))


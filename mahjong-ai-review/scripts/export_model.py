import sys,pathlib,torch,json
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.networks import MahjongBrain
out=root/'checkpoints'/'simulation-v2';s=torch.load(out/'deploy.pt',map_location='cpu',weights_only=False);m=MahjongBrain(**s['model_config']);m.load_state_dict(s['model']);m.eval();example=torch.zeros(1,128);traced=torch.jit.trace(m,example,strict=False);traced.save(str(out/'model_raw_logits.torchscript.pt'));loaded=torch.jit.load(str(out/'model_raw_logits.torchscript.pt'))
for k,v in m(example).items():assert torch.allclose(v,loaded(example)[k])
print('CPU TorchScript raw logits export parity PASS; calibration/legality/research flags require Python wrapper')

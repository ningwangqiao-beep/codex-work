import sys, pathlib, json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import torch
from models.networks import MahjongBrain
from training.gate import validate_manifest

torch.manual_seed(42)
m=MahjongBrain().cuda(); x=torch.randn(128,128,device='cuda'); o=m(x)
loss=sum(v.square().mean() for v in o.values()); loss.backward()
p=m.predict(x)
assert p['deal_in_probability'].shape==(128,27)
assert torch.allclose(p['joint_winner_distribution'].sum(-1),torch.ones(128,27,device='cuda'),atol=1e-6)
try: validate_manifest({})
except ValueError: pass
else: raise AssertionError('gate failed')
r={'synthetic_interface_test_only':True,'batch_size':128,'gpu':torch.cuda.get_device_name(),'finite_gradients':all(torch.isfinite(v.grad).all().item() for v in m.parameters()),'formal_training_run':False}
path=pathlib.Path(__file__).resolve().parents[1]/'reports'/'employee_c_smoke.json'; path.write_text(json.dumps(r,indent=2)); print(r)

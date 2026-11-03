"""Relative+pairwise combined interface test, no optimizer or training."""
import sys,pathlib,json,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.next_relative_v3 import RelativeV3ActionValueNet,relative_losses
from training.next_supervised import batches
torch.set_num_threads(2);torch.manual_seed(42);m=json.load(open(root/'datasets/next_history100/manifest.json'));inp,target,meta=next(batches(m['files']['train'],'cpu',8));model=RelativeV3ActionValueNet();o=model(*inp);ls=relative_losses(o,target,inp[2]);sum(ls.values()).backward();assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters());r={'interface_only_no_optimizer':True,'parameters':sum(p.numel() for p in model.parameters()),'batch':len(meta),'losses':{k:float(v.detach()) for k,v in ls.items()},'finite_all_head_gradients':True,'scope':'combined representation+pairwise direction, not isolated causal factor','formal_training':False};(root/'reports/next_c_relative_smoke.json').write_text(json.dumps(r,indent=2));print(r)

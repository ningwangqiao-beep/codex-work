"""Read one audited-format batch, forward/backward only. No optimizer or training."""
import pathlib,sys,json,hashlib,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from training.v3_supervised import batches
from models.v3_action_value import V3ActionValueNet
from training.v3_losses import v3_losses
m=json.load(open(root/'datasets/v3_teacher100/manifest.json'));torch.set_num_threads(2);torch.manual_seed(42);inp,target,meta=next(batches(m['files']['train'],'cpu',128));model=V3ActionValueNet(candidate_dim=len(m['candidate_feature_names']));o=model(*inp);loss=v3_losses(o,target,inp[2]);sum(loss.values()).backward();assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters());r={'scope':'data_contract_forward_backward_only_NO_optimizer','batch':len(meta),'history_padded_length':inp[3].shape[1],'history_true_max':int(inp[4].sum(-1).max()),'parameters':sum(p.numel() for p in model.parameters()),'finite_gradients':True,'per_head_loss':{k:float(v.detach()) for k,v in loss.items()},'formal_training':False,'optimizer_steps':0,'rl_performed':False,'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()};(root/'reports/v3_c_t2_batch_smoke.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

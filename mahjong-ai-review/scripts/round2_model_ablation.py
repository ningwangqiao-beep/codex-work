"""Bounded A-F ablation. Train/validation only; no final test metrics."""
import argparse,sys,pathlib,json,time,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.round2 import AblationBrain
from training.streaming import train,batches
from evaluation.metrics import binary_metrics
p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--variant',choices=list('ABCDEF'),required=True);p.add_argument('--epochs',type=int,default=2);p.add_argument('--output',required=True);p.add_argument('--seed',type=int,default=42);p.add_argument('--resume',action='store_true');a=p.parse_args()
torch.set_num_threads(4);torch.manual_seed(a.seed);m=json.load(open(a.manifest));out=pathlib.Path(a.output);start=time.perf_counter()
if (out/'validation.json').exists():raise RuntimeError('Completed output immutable; choose new directory')
model=AblationBrain(a.variant,loss_bins=m['loss_bins']).cuda();train(model,m,out,epochs=a.epochs,resume=out/'last.pt' if a.resume and (out/'last.pt').exists() else None)
s=torch.load(out/'best.pt',map_location='cuda',weights_only=False);model.load_state_dict(s['model']);model.eval();ps=[];ys=[]
with torch.no_grad():
 for b in batches(m['shards']['validation'],128,'cuda'):
  mask=b['target_active'].bool();ps.append(model(b['features'])['tenpai_logits'].sigmoid()[mask].cpu());ys.append(b['tenpai'][mask].cpu())
r={'variant':a.variant,'seed':a.seed,'epochs_limit':a.epochs,'seconds':time.perf_counter()-start,'scope':'train_validation_only','features':{'A':'public counts','B':'counts+missing','C':'counts+missing+meld counts','D':'C+last11 encoded actions','E':'all128 incl own/wall/turn/seats/active','F':'E+GRU over last11 actions'}[a.variant],'not_full_requested_ablation':'D uses last11 history, not complete discard sequence; E differs by several feature groups','validation_tenpai':binary_metrics(torch.cat(ps),torch.cat(ys))};(out/'validation.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

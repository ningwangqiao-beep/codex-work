"""Bounded structured training. Never evaluates test; calibration separate."""
import argparse,sys,pathlib,json,time,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.round2_structured import StructuredBrain
from training.streaming import train
from baselines.frequency import fit
p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--output',required=True);p.add_argument('--epochs',type=int,default=8);p.add_argument('--resume',action='store_true');a=p.parse_args()
torch.set_num_threads(4);torch.manual_seed(42);m=json.load(open(a.manifest));out=pathlib.Path(a.output)
if (out/'TRAIN_COMPLETE.json').exists():raise RuntimeError('Frozen trained output')
model=StructuredBrain(loss_bins=m['loss_bins']).cuda();start=time.perf_counter();train(model,m,out,epochs=a.epochs,resume=out/'last.pt' if a.resume and (out/'last.pt').exists() else None)
(out/'baseline.json').write_text(json.dumps(fit(m['shards']['train'])));(out/'TRAIN_COMPLETE.json').write_text(json.dumps({'seconds':time.perf_counter()-start,'seed':42,'epochs_limit':a.epochs,'scope':'train_validation_only','model':'structured-v1','warning':'handcrafted structure experiment; improvement not assumed'}));print('TRAIN_COMPLETE, final test untouched')

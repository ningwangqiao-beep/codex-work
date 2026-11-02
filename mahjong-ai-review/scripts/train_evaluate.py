import sys,pathlib,json,argparse,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.networks import MahjongBrain
from training.streaming import train,batches
from baselines.frequency import fit
from evaluation.calibration import fit_temperature
from evaluation.heldout import evaluate
p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('--epochs',type=int,default=8);p.add_argument('--output');a=p.parse_args()
m=json.loads(pathlib.Path(a.manifest).read_text());out=pathlib.Path(a.output) if a.output else root/'checkpoints'/m['dataset_version'];
if (out/'deploy.pt').exists(): raise RuntimeError('Frozen completed experiment: use a new output directory')
torch.manual_seed(42);torch.set_num_threads(4)
model=MahjongBrain(128,loss_bins=m['loss_bins']).cuda();train(model,m,out,epochs=a.epochs)
s=torch.load(out/'best.pt',weights_only=False);model.load_state_dict(s['model']);logits=[];labels=[]
with torch.no_grad():
 for b in batches(m['shards']['validation'],128,'cuda'):
  active=b['target_active'].bool();logits.append(model(b['features'])['tenpai_logits'][active].cpu());labels.append(b['tenpai'][active].cpu())
t=fit_temperature(torch.cat(logits),torch.cat(labels));s['temperature']=t;torch.save(s,out/'deploy.pt')
baseline=fit(m['shards']['train']);(out/'baseline.json').write_text(json.dumps(baseline))
result=evaluate(model,m['shards']['test'],baseline,t);result['temperature']=t;(root/'reports'/('employee_c_'+m['dataset_version']+'_final_test.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))


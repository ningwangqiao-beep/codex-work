"""Run on validation only. Old final-test shards are never opened."""
import argparse,sys,pathlib,json,hashlib,time,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from evaluation.round2_io import load_checkpoint
from training.streaming import batches
from evaluation.metrics import binary_metrics
from evaluation.round2_calibration import fit_affine,calibrated
p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--checkpoint',required=True);p.add_argument('--output',default=str(root/'reports'/'round2_c_calibration.json'));a=p.parse_args()
torch.set_num_threads(4);start=time.perf_counter();m=json.load(open(a.manifest));model,s=load_checkpoint(a.checkpoint,'cuda');model.eval();store={key:{part:[] for part in ('fit_x','fit_y','eval_x','eval_y')} for key in ('tenpai','wait','risk')};games={'fit':set(),'eval':set()}
with torch.no_grad():
 for b in batches(m['shards']['validation'],128,'cuda'):
  o=model(b['features']);parts=[]
  for meta in b['metadata']:
   group='fit' if int(hashlib.sha256(str(meta['game_id']).encode()).hexdigest(),16)%2==0 else 'eval';parts.append(group=='fit');games[group].add(str(meta['game_id']))
  fit=torch.tensor(parts,device='cuda');active=b['target_active'].bool();waitmask=(b['tenpai']*b['target_active']).bool().unsqueeze(-1).expand_as(b['waits']);cand=b['candidate_mask'].bool();risk=torch.logsumexp(o['joint_logits'][:,:,1:],-1)-o['joint_logits'][:,:,0]
  for name,x,y,mask in [('tenpai',o['tenpai_logits'],b['tenpai'],active),('wait',o['conditional_wait_logits'],b['waits'],waitmask),('risk',risk,(b['joint_outcome']>0).float(),cand)]:
   for label,select in [('fit',fit),('eval',~fit)]:
    shape=[len(select)]+[1]*(mask.ndim-1);selected=mask & select.reshape(shape)
    store[name][label+'_x'].append(x[selected].cpu());store[name][label+'_y'].append(y[selected].cpu())
report={'scope':'validation_only_game_split','dataset_version':m['dataset_version'],'fit_games':len(games['fit']),'eval_games':len(games['eval']),'tasks':{}}
for name,values in store.items():
 v={k:torch.cat(x) for k,x in values.items()};params=fit_affine(v['fit_x'],v['fit_y']);report['tasks'][name]={'parameters':params,'fit_positive':int(v['fit_y'].sum()),'fit_n':len(v['fit_y']),'before':binary_metrics(v['eval_x'].sigmoid(),v['eval_y']),'after':binary_metrics(calibrated(v['eval_x'],params),v['eval_y'])}
for task,result in report['tasks'].items():
 before=result['before'];after=result['after'];result['accepted']=after['brier']<=before['brier'] and after['log_loss']<=before['log_loss'] and (after['brier']<before['brier'] or after['log_loss']<before['log_loss']);result['selection_rule']='validation_eval_half_brier_and_logloss_nonworse_at_least_one_better'
report['seconds']=time.perf_counter()-start;pathlib.Path(a.output).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

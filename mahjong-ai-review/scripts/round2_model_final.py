"""One new-seed final evaluation; output guard prevents accidental repeat."""
import argparse,sys,pathlib,json,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from evaluation.round2_io import load_checkpoint
from evaluation.heldout import evaluate
from training.gate import validate_manifest
p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--checkpoint',required=True);p.add_argument('--calibration',required=True);p.add_argument('--baseline',required=True);p.add_argument('--output',required=True);a=p.parse_args();out=pathlib.Path(a.output)
if out.exists():raise RuntimeError('Final test output immutable')
m=json.load(open(a.manifest));cal=json.load(open(a.calibration))
if m['dataset_version'] in ('simulation-v1','simulation-v2'):raise RuntimeError('Old final test forbidden')
if cal['dataset_version']!=m['dataset_version']:raise ValueError('Calibration dataset mismatch')
bound=validate_manifest(m)
torch.set_num_threads(4);model,state=load_checkpoint(a.checkpoint,'cuda')
if state['dataset_fingerprint']!=bound:raise ValueError('Checkpoint dataset fingerprint mismatch')
base=json.load(open(a.baseline));original=model.predict
# Calibration applies wait and any-winner probabilities; joint redistribution stays coherent.
def predict(x,temperature=1.):
 r=original(x,temperature);j=r['joint_winner_distribution']
 def scale(p,key):
  result=cal['tasks'][key];before=result['before'];after=result['after'];accepted=after['brier']<=before['brier'] and after['log_loss']<=before['log_loss'] and (after['brier']<before['brier'] or after['log_loss']<before['log_loss'])
  if not accepted:return p
  z=result['parameters'];return (torch.logit(p.clamp(1e-7,1-1e-7))*z['slope']+z['intercept']).sigmoid()
 r['tenpai_probability']=scale(r['tenpai_probability'],'tenpai');r['wait_given_tenpai']=scale(r['wait_given_tenpai'],'wait');risk=scale(r['deal_in_probability'],'risk');pos=j[:,:,1:];pos=pos/pos.sum(-1,keepdim=True).clamp_min(1e-12)*risk.unsqueeze(-1);r['joint_winner_distribution']=torch.cat(((1-risk).unsqueeze(-1),pos),-1);r['deal_in_probability']=risk
 bits=torch.tensor([[bool(k&(1<<i)) for k in range(8)] for i in range(3)],dtype=x.dtype,device=x.device);r['opponent_deal_in_probability']=torch.einsum('btk,ik->bit',r['joint_winner_distribution'],bits);r['wait_product_probability']=r['tenpai_probability'].unsqueeze(-1)*r['wait_given_tenpai'];r['marginal_disagreement']=(r['opponent_deal_in_probability']-r['wait_product_probability']).abs()
 return r
model.predict=predict
report=evaluate(model,m['shards']['test'],base);report['calibration_scope']='new_validation_groups_only';report['checkpoint_epoch']=state['epoch'];report['calibration_decisions']={key:(v['after']['brier']<=v['before']['brier'] and v['after']['log_loss']<=v['before']['log_loss'] and (v['after']['brier']<v['before']['brier'] or v['after']['log_loss']<v['before']['log_loss'])) for key,v in cal['tasks'].items()};report['dataset_fingerprint']=bound;report['limitations']=['no real-player validation','empirical score support; tails unvalidated','independent wait/joint marginal disagreement','no complete A-F full-history study'];out.write_text(json.dumps(report,indent=2));print('NEW FINAL TEST FROZEN:',out)

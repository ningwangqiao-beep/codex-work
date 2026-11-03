"""Isolated CPU interface and STOP/resume evidence; never signs formal admission."""
import contextlib,io,json,os,pathlib,sys,tempfile
from unittest.mock import patch
import torch
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from models.next_opponent import OpponentAblation,FAMILIES
from training import next_opponent_fit as fit
from training import next_opponent_eval as evaluation
from training.next_opponent_pipeline import read,records,collate,losses
from training.next_opponent_gate import validate,source_hashes
from evaluation.metrics import binary_metrics

def main():
 torch.set_num_threads(2);m=read(ROOT/'datasets/next_history1000/manifest.json');sample=[]
 for r in records(m['shards']['train']):
  sample.append(r)
  if len(sample)==8:break
 evidence={'TEST_ONLY':True,'formal_training_started':False,'families':{}}
 with tempfile.TemporaryDirectory(dir=ROOT/'reports',prefix='next_c_opponent_smoke_') as temp:
  temp=pathlib.Path(temp);shard=temp/'train'/'7000000'/'records.jsonl';shard.parent.mkdir(parents=True);shard.write_text(''.join(json.dumps(r)+'\n' for r in sample));manifest=temp/'manifest.json';manifest.write_text(json.dumps({'shards':{'train':[str(shard)]}}));unsigned=temp/'unsigned.json';unsigned.write_text('{}')
  try:validate(ROOT/'datasets/next_history1000/manifest.json',ROOT/'datasets/next_aux_validation100/manifest.json',unsigned,ROOT);raise AssertionError('Unsigned admission accepted')
  except ValueError:pass
  audit={'TEST_ONLY_scoped_mock':True,'training_allowed':True,'aux_used_for_training':False}
  for family in FAMILIES:
   torch.manual_seed(42);model=OpponentAblation(family);inp,t=collate(sample,'cpu',family);t['structural_tenpai'][0,0]=1;t['structural_waits'][0,0,0]=1;o=model(*inp);sum(losses(o,t).values()).backward();assert all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters())
   assert sum(p.numel() for p in model.parameters())==19563
   # Every excluded static coordinate is an information firewall, tested directly.
   altered=inp[0].clone();altered[:,model.static_mask==0]+=torch.randn_like(altered[:,model.static_mask==0])*100
   model.eval()
   with torch.no_grad():
    one=model(*inp);two=model(altered,*inp[1:]);assert all(torch.equal(one[k],two[k]) for k in one)
   evidence['families'][family]={'parameters':19563,'finite_masked_loss_backward':True,'synthetic_positive_wait_interface_only':True,'excluded_static_poison_invariant':True}
  with patch.object(fit,'validate',return_value=audit),contextlib.redirect_stdout(io.StringIO()):
   fit.train(manifest,manifest,unsigned,temp/'full','history_shuffled',ROOT,'cpu')
   original=torch.optim.Adam.step;count=0;stop=temp/'STOP'
   def step(opt,*args,**kwargs):
    nonlocal count
    result=original(opt,*args,**kwargs);count+=1
    if count==2:stop.write_text('test only')
    return result
   with patch.dict(os.environ,{'MAHJONG_STOP_FILE':str(stop)}),patch.object(torch.optim.Adam,'step',step):
    try:fit.train(manifest,manifest,unsigned,temp/'resumed','history_shuffled',ROOT,'cpu');raise AssertionError('STOP not observed')
    except SystemExit as e:assert e.code==75
   partial=torch.load(temp/'resumed'/'last.pt',weights_only=False);assert partial['optimizer_steps']==2
   stop.unlink();fit.train(manifest,manifest,unsigned,temp/'resumed','history_shuffled',ROOT,'cpu',True)
  left=torch.load(temp/'full'/'last.pt',weights_only=False);right=torch.load(temp/'resumed'/'last.pt',weights_only=False);delta=max(float((left['model'][k]-right['model'][k]).abs().max()) for k in left['model']);assert delta<=1e-7;assert right['optimizer_steps']==6
  for key in left['optimizer']['state']:
   for name,x in left['optimizer']['state'][key].items():assert torch.allclose(x,right['optimizer']['state'][key][name],atol=1e-7,rtol=1e-6)
  assert binary_metrics([.1,.2],[0,0])['roc_auc'] is None
  auxmanifest=temp/'aux.json';auxmanifest.write_text(json.dumps({'shards':{'auxiliary':[str(shard)]}}))
  with patch.object(evaluation,'validate',return_value=audit),contextlib.redirect_stdout(io.StringIO()):
   evaluated=evaluation.evaluate(temp/'resumed'/'epoch_5.pt',manifest,auxmanifest,unsigned,temp/'eval.json',ROOT)
  assert evaluated['checkpoint_epoch']==5 and evaluated['parameters']==19563
  evidence['isolated_uncalibrated_evaluation_smoke']={k:v['n'] for k,v in evaluated['metrics'].items()}
  evidence.update(stop_exitcode=75,stop_after_updates=2,resumed_updates=6,model_max_abs_difference=delta,optimizer_allclose=True,unsigned_gate_refused=True,zero_positive_auc_is_NA=True,auxiliary_records_read_for_training=0)
 evidence['passed']=True;(ROOT/'reports/next_c_opponent_smoke_v1.json').write_text(json.dumps(evidence,indent=2));print(json.dumps(evidence,indent=2))
if __name__=='__main__':main()

"""Supervised action-value CLI. No RL and no final-test access."""
import argparse,pathlib,sys,json,hashlib,os,time,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.revision_action_value import ActionValueNet,supervised_losses
from evaluation.revision_action_value import action_value_metrics

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def rows(paths):
 for path in paths:
  with open(path,encoding='utf-8') as f:
   for line in f:yield json.loads(line)

def batch(records,config):
 state=torch.tensor([r['state_features'] for r in records]).float();c=torch.tensor([r['candidate_features'] for r in records]).float();mask=torch.tensor([r['legal_mask'] for r in records],dtype=torch.bool);target={'action_targets':torch.tensor([r['action_targets'] for r in records]).float()}
 if config.get('state_target_definition'):
  target['state_targets']=torch.tensor([r['state_target'] for r in records]).float()
 if c.shape[1]!=27 or mask.shape!=(len(records),27):raise ValueError('Canonical 27 candidate slots required')
 return state,c,mask,target

def batches(paths,config,size=64):
 pending=[]
 for r in rows(paths):
  pending.append(r)
  if len(pending)==size:yield batch(pending,config);pending=[]
 if pending:yield batch(pending,config)

def admit(m):
 for k in ['dataset_version','teacher_definition','target_semantics','candidate_feature_names','state_dim','candidate_dim','shards','audit_path','audit_sha256','source_fingerprints']:
  if k not in m:raise ValueError('Missing '+k)
 if len(m['candidate_feature_names'])!=m['candidate_dim']:raise ValueError('Feature schema mismatch')
 if m['target_semantics'] not in ['supervised_heuristic_utility','lexicographic_preference_rank','counterfactual_rollout_net_return']:raise ValueError('Explicit target semantics required')
 files={str(p):sha(p) for key in ['train','validation'] for p in m['shards'][key]};bound=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
 if sha(m['audit_path'])!=m['audit_sha256']:raise ValueError('Audit fingerprint mismatch')
 audit=json.load(open(m['audit_path']))
 if audit.get('passed') is not True or audit.get('observation_filter_audited') is not True or audit.get('dataset_fingerprint')!=bound or audit.get('source_fingerprints')!=m['source_fingerprints']:raise ValueError('Dataset/observation audit missing or unbound')
 for p,digest in m['source_fingerprints'].items():
  if sha(p)!=digest:raise ValueError('Source drift '+p)
 seen={};sources={}
 for split in ['train','validation']:
  count=0
  for r in rows(m['shards'][split]):
   for k in ['game_id','seed','source_group','state_features','candidate_features','legal_mask','action_targets']:
    if k not in r:raise ValueError('Missing record '+k)
   for key,registry in [(str(r['game_id']),seen),(str((r['source_group'],r['seed'])),sources)]:
    if key in registry and registry[key]!=split:raise ValueError('Game/source leakage')
    registry[key]=split
   state,c,mask,t=batch([r],m)
   if len(r['state_features'])!=m['state_dim'] or c.shape[-1]!=m['candidate_dim'] or not mask.any() or not torch.isfinite(state).all() or not torch.isfinite(c).all() or not torch.isfinite(t['action_targets'][mask]).all():raise ValueError('Invalid record')
   if any(type(v) not in (bool,int) or v not in (0,1) for v in r['legal_mask']):raise ValueError('Mask not binary')
   count+=1
  if count==0:raise ValueError('Empty '+split)
 code={str(p.relative_to(root)):sha(p) for p in [root/'models/revision_action_value.py',root/'evaluation/revision_action_value.py',pathlib.Path(__file__)]}
 return hashlib.sha256(json.dumps({'dataset':bound,'manifest':m,'code':code},sort_keys=True).encode()).hexdigest()

def evaluate(model,paths,m):
 predictions=[];targets=[];masks=[];heads={};n=0
 model.eval()
 with torch.no_grad():
  for state,c,mask,t in batches(paths,m):
   o=model(state,c,mask);loss=supervised_losses(o,t,mask,m.get('equivalence_tolerance',0.));n+=1
   for k,v in loss.items():heads[k]=heads.get(k,0.)+float(v)
   predictions.append(o['action_value']);targets.append(t['action_targets']);masks.append(mask)
 return {'per_head_loss':{k:v/n for k,v in heads.items()},'action_metrics':action_value_metrics(torch.cat(predictions),torch.cat(targets),torch.cat(masks),m.get('equivalence_tolerance',0.)),'state_head_trained':bool(m.get('state_target_definition'))}

def train(manifest,out,epochs,resume):
 m=json.load(open(manifest));bound=admit(m);out.mkdir(parents=True,exist_ok=True)
 if epochs<1:raise ValueError('Positive epoch limit required')
 if not resume and any(out.iterdir()):raise ValueError('Nonempty output requires --resume or a new directory')
 if (out/'COMPLETE.json').exists():raise ValueError('Completed output immutable')
 torch.manual_seed(42);model=ActionValueNet(m['state_dim'],m['candidate_dim']);opt=torch.optim.Adam(model.parameters(),lr=.001);start=0;best=float('inf');best_epoch=-1
 if resume and (out/'last.pt').exists():
  s=torch.load(out/'last.pt',weights_only=False)
  if s['binding']!=bound:raise ValueError('Resume data/source/schema mismatch')
  model.load_state_dict(s['model']);opt.load_state_dict(s['optimizer']);torch.set_rng_state(s['rng']);start=s['epoch']+1;best=s['best'];best_epoch=s['best_epoch']
 def save(epoch,interrupted=False):
  s={'model':model.state_dict(),'model_config':model.config,'optimizer':opt.state_dict(),'rng':torch.get_rng_state(),'epoch':epoch,'best':best,'best_epoch':best_epoch,'binding':bound,'target_semantics':m['target_semantics'],'teacher_definition':m['teacher_definition'],'state_target_definition':m.get('state_target_definition'),'feature_names':m['candidate_feature_names'],'interrupted_epoch_restarts':interrupted,'version':'revision-shared-action-value-v1'};torch.save(s,out/'last.tmp');os.replace(out/'last.tmp',out/'last.pt');return s
 for epoch in range(start,epochs):
  model.train();heads={};n=0
  for state,c,mask,t in batches(m['shards']['train'],m):
   stop=os.environ.get('MAHJONG_STOP_FILE')
   if stop and pathlib.Path(stop).exists():save(epoch-1,True);raise SystemExit(75)
   o=model(state,c,mask);ls=supervised_losses(o,t,mask,m.get('equivalence_tolerance',0.));opt.zero_grad();sum(ls.values()).backward();opt.step();n+=1
   for k,v in ls.items():heads[k]=heads.get(k,0.)+float(v.detach())
  val=evaluate(model,m['shards']['validation'],m);score=val['per_head_loss']['action_value_mse'];improved=score<best
  if improved:best=score;best_epoch=epoch
  s=save(epoch)
  if improved:
   # Preserve every selected best; best.pt is only an atomic alias, never an overwritten sole artifact.
   snapshot=out/('best_epoch_'+str(epoch)+'.pt')
   if snapshot.exists():raise ValueError('Refusing to overwrite best snapshot')
   torch.save(s,snapshot);(out/'BEST.tmp').write_text(json.dumps({'checkpoint':snapshot.name,'epoch':epoch,'validation_action_value_mse':best}));os.replace(out/'BEST.tmp',out/'BEST.json')
  with (out/'metrics.jsonl').open('a') as f:f.write(json.dumps({'epoch':epoch,'train_head_loss':{k:v/n for k,v in heads.items()},'validation':val})+'\n')
 (out/'COMPLETE.json').write_text(json.dumps({'best_epoch':best_epoch,'binding':bound,'target_semantics':m['target_semantics'],'state_head_trained':bool(m.get('state_target_definition')),'rl_performed':False}))

def smoke(output):
 torch.manual_seed(42)
 from models.round2_candidate import candidate_features,teacher_utility
 from observations.public import features
 from rules.core import legal_discards
 hands=[[0,0,1,2,3,4,5,9,10,11,18,19,20,21],[0,0,1,2,3,4,5,9,9,10,11,12,13,14]];records=[]
 for i,hand in enumerate(hands):
  o={'observer_player':0,'observer_hand':hand,'declared_missing_suits':[2,0,1,2],'visible_discards':[],'public_melds':[[],[],[],[]],'public_winning_tiles':[],'active':[True]*4,'remaining_wall_information':55,'turn_index':0,'current_player':0,'public_action_history':[]};legal=legal_discards(hand,2);c=[[0.]*12 for _ in range(27)];y=[0.]*27
  for tile in legal:c[tile]=candidate_features(o,tile);y[tile]=teacher_utility(o,tile)/64
  records.append({'state_features':features(o),'candidate_features':c,'legal_mask':[t in legal for t in range(27)],'action_targets':y,'state_target':float(i)})
 config={'state_target_definition':'synthetic_fixture_index_only'};state,c,mask,t=batch(records,config);model=ActionValueNet();opt=torch.optim.Adam(model.parameters(),lr=.001);o=model(state,c,mask);ls=supervised_losses(o,t,mask);sum(ls.values()).backward();assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters());opt.step();assert mask.gather(1,o['masked_action_value'].argmax(-1)[:,None]).all()
 # Same-value different actions count equivalent, not exact; illegal high score excluded.
 metrics=action_value_metrics(torch.tensor([[0.,2.,3.,999.]]),torch.tensor([[1.,2.,2.,-99.]]),torch.tensor([[True,True,True,False]]));assert metrics['exact_rate']==0 and metrics['equivalent_rate']==1 and metrics['teacher_value_regret_mean']==0
 for badstate,badmask in [(state,torch.zeros_like(mask)),(state*float('nan'),mask)]:
  try:model(badstate,c,badmask)
  except ValueError:pass
  else:raise AssertionError('Invalid interface input accepted')
 output.parent.mkdir(parents=True,exist_ok=True);ckpt=output.with_suffix('.pt');torch.save({'model':model.state_dict(),'optimizer':opt.state_dict(),'rng':torch.get_rng_state(),'config':model.config,'scope':'two_legal_fixtures_synthetic_state_targets_not_mahjong_training'},ckpt);restored=ActionValueNet();s=torch.load(ckpt,weights_only=False);restored.load_state_dict(s['model']);assert torch.equal(model(state,c,mask)['action_value'],restored(state,c,mask)['action_value'])
 r={'smoke_only':True,'legal_fixtures':2,'parameters':sum(p.numel() for p in model.parameters()),'per_head_loss':{k:float(v.detach()) for k,v in ls.items()},'finite_all_head_gradients':True,'legal_argmax':True,'equivalent_tie_test':metrics,'checkpoint_roundtrip':True,'rl_performed':False,'actual_mahjong_training':False,'state_target':'synthetic fixture index, not game return'};output.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--manifest');p.add_argument('--output',required=True);p.add_argument('--epochs',type=int,default=3);p.add_argument('--resume',action='store_true');p.add_argument('--smoke',action='store_true');a=p.parse_args();torch.set_num_threads(2)
 if a.smoke:smoke(pathlib.Path(a.output))
 else:
  if not a.manifest:p.error('--manifest required for audited supervised training')
  train(a.manifest,pathlib.Path(a.output),a.epochs,a.resume)

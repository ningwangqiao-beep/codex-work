"""Combined candidate-relative input + pairwise ranking; not single-factor. No RL or final-test use."""
import pathlib,json,hashlib,os,random,time,torch,ctypes,subprocess
from models.next_relative_v3 import RelativeV3ActionValueNet as V3ActionValueNet
from training.next_scale_gate import validate_scale_manifest as validate_next_manifest
from training.v3_gate import sha
from models.next_relative_v3 import relative_losses as v3_losses
from evaluation.revision_action_value import action_value_metrics

def records(path):
 paths=path if isinstance(path,list) else [path]
 for shard in sorted(paths,key=lambda p:int(pathlib.Path(p).parent.name)):
  with open(shard,encoding='utf-8') as f:
   for line in f:yield json.loads(line)
def collate(rows,device):
 length=max(1,max(len(r['history_tokens']) for r in rows));tokens=torch.zeros(len(rows),length,3,dtype=torch.long,device=device);tokens[:,:,1]=4;hm=torch.zeros(len(rows),length,dtype=torch.bool,device=device)
 for i,r in enumerate(rows):
  n=len(r['history_tokens'])
  if n:tokens[i,:n]=torch.tensor(r['history_tokens'],device=device);hm[i,:n]=True
 inp=(torch.tensor([r['state_features'] for r in rows],dtype=torch.float32,device=device),torch.tensor([r['candidate_features'] for r in rows],dtype=torch.float32,device=device),torch.tensor([r['legal_mask'] for r in rows],dtype=torch.bool,device=device),tokens,hm)
 target={name:torch.tensor([r[key] for r in rows],dtype=torch.float32,device=device) for name,key in [('action_targets','action_targets'),('state_targets','state_target'),('tenpai','structural_tenpai'),('conditional_waits','structural_waits'),('joint_winner_mask','joint_winner_mask'),('target_active','target_active')]}
 meta=[{'game_id':r['game_id'],'free_discard':not any(t//9==r['observation']['declared_missing_suits'][r['observation']['observer_player']] for t in r['observation']['observer_hand']),'best_postdiscard_structural':round(min(r['candidate_features'][i][3]*8 for i,v in enumerate(r['legal_mask']) if v))} for r in rows]
 return inp,target,meta

def batches(path,device,size):
 rows=[]
 for r in records(path):
  rows.append(r)
  if len(rows)==size:yield collate(rows,device);rows=[]
 if rows:yield collate(rows,device)

def train(manifest,admission,out,root,epochs=6,batch_size=128,seed=42,device='cuda',resume=False,mode='multitask'):
 root=pathlib.Path(root);out=pathlib.Path(out);audit=validate_next_manifest(manifest,root,admission);m=json.loads(pathlib.Path(manifest).read_text(encoding='utf-8'));m['files']=m['shards'];sources={str(p.relative_to(root)):sha(p) for p in [root/'models/v3_action_value.py',root/'models/revision_action_value.py',root/'training/next_scale_supervised.py',root/'training/v3_losses.py',root/'training/next_scale_gate.py',root/'models/next_relative_v3.py',root/'models/next_candidate.py',root/'training/v3_gate.py',root/'evaluation/revision_action_value.py']};config={'epochs':epochs,'batch_size':batch_size,'seed':seed,'device':device,'loss_weights':{'action_value_mse':1.,'pairwise_preference':1.,'state_value_mse':.01,'tenpai_bce':.2,'conditional_wait_bce':.2,'joint_risk_ce':.2},'action_target_semantics':m['target_semantics'],'state_target_units':m['state_target_units'],'state_target_policy':m['state_target_policy']};binding=hashlib.sha256(json.dumps({'admission':audit,'sources':sources,'config':{k:v for k,v in config.items() if k!='epochs'}},sort_keys=True).encode()).hexdigest()
 allowed=json.loads(pathlib.Path(admission).read_text(encoding='utf-8'))
 if seed!=42:raise ValueError('Fixed seed42 required')
 if epochs>allowed.get('max_epochs',0) or batch_size>allowed.get('max_batch_size',0):raise ValueError('Chief epoch/batch admission bound exceeded')
 if mode!='multitask':raise ValueError('Unknown loss control')
 config['loss_mode']=mode
 config['experimental_direction']='candidate_relative_input_plus_pairwise_NOT_single_factor'
 config['parameter_count']=20541
 config['control_parameter_count']=20349
 if mode=='action_only':
  for k in ('state_value_mse','tenpai_bce','conditional_wait_bce','joint_risk_ce'):config['loss_weights'][k]=0.
 binding=hashlib.sha256(json.dumps({'admission':audit,'sources':sources,'config':{k:v for k,v in config.items() if k!='epochs'}},sort_keys=True).encode()).hexdigest()
 if epochs<1 or batch_size<1:raise ValueError('Positive bounded epochs/batch required')
 if device=='cuda' and not torch.cuda.is_available():raise ValueError('CUDA required but unavailable')
 out.mkdir(parents=True,exist_ok=True)
 if (out/'COMPLETE.json').exists():raise ValueError('Completed run immutable')
 if not resume and any(out.iterdir()):raise ValueError('Nonempty output needs --resume')
 if resume and any(out.iterdir()) and not (out/'last.pt').exists():raise ValueError('Nonempty output has no resumable last checkpoint')
 torch.set_num_threads(2);torch.manual_seed(seed);random.seed(seed);model=V3ActionValueNet(candidate_dim=len(m['candidate_feature_names'])).to(device);opt=torch.optim.Adam(model.parameters(),lr=.001);start_epoch=0;skip=0;best=float('inf');best_epoch=-1;steps=0;resumed_heads={};resumed_rows=0;started=time.perf_counter()
 if device=='cuda':torch.cuda.reset_peak_memory_stats()
 if resume and (out/'last.pt').exists():
  s=torch.load(out/'last.pt',map_location=device,weights_only=False)
  if s['binding']!=binding:raise ValueError('Resume rules/data/admission/model/config fingerprint mismatch')
  model.load_state_dict(s['model']);opt.load_state_dict(s['optimizer']);torch.set_rng_state(s['rng'].cpu());random.setstate(s['python_rng'])
  if s.get('cuda_rng') and torch.cuda.is_available():torch.cuda.set_rng_state_all([v.cpu() for v in s['cuda_rng']])
  start_epoch=s['epoch']+int(s['epoch_complete']);skip=0 if s['epoch_complete'] else s['next_batch_index'];best=s['best'];best_epoch=s['best_epoch'];steps=s['optimizer_steps'];resumed_heads=s.get('train_epoch_heads',{});resumed_rows=s.get('train_epoch_rows',0)
 def save(epoch,complete,next_batch):
  state={'version':'NEXT-HISTORY1000-RELATIVE-PAIRWISE-v1','rule_version':m.get('rule_version','SICHUAN-XUEZHAN-4FAN-V3'),'model':model.state_dict(),'model_config':model.config,'optimizer':opt.state_dict(),'rng':torch.get_rng_state(),'cuda_rng':torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],'python_rng':random.getstate(),'epoch':epoch,'epoch_complete':complete,'next_batch_index':next_batch,'optimizer_steps':steps,'train_epoch_heads':heads,'train_epoch_rows':n,'best':best,'best_epoch':best_epoch,'binding':binding,'config':config,'source_hashes':sources,'data_admission':audit,'head_semantics':{'action':'teacher preference NOT counterfactual Q','state':m['state_target_policy']+'; '+m['state_target_units'],'aux_tenpai':'structural/legal-hand NOT public-effective'},'rl_performed':False};torch.save(state,out/'last.tmp');os.replace(out/'last.tmp',out/'last.pt');return state
 def stop(epoch,next_batch):
  path=os.environ.get('MAHJONG_STOP_FILE')
  if path and pathlib.Path(path).exists():save(epoch,False,next_batch);raise SystemExit(75)
 def evaluate(epoch,next_batch):
  model.eval();heads={};n=0;pv=[];yv=[];masks=[];states=[];statey=[];metadata=[]
  with torch.no_grad():
   for inp,t,meta in batches(m['files']['validation'],device,batch_size):
    stop(epoch,next_batch);o=model(*inp);losses=v3_losses(o,t,inp[2]);size=len(meta);n+=size
    for k,v in losses.items():heads[k]=heads.get(k,0.)+float(v)*size
    pv.append(o['action_value'].cpu());yv.append(t['action_targets'].cpu());masks.append(inp[2].cpu());states.append(o['state_value'].cpu());statey.append(t['state_targets'].cpu());metadata.extend(meta)
  p=torch.cat(pv);y=torch.cat(yv);mask=torch.cat(masks);value=torch.cat(states);vt=torch.cat(statey);groups={}
  for name in ('all','free_discard','missing_forced'):
   select=torch.tensor([True if name=='all' else (r['free_discard'] if name=='free_discard' else not r['free_discard']) for r in metadata])
   if select.any():groups[name]=action_value_metrics(p[select],y[select],mask[select])
  for shanten in sorted(set(r['best_postdiscard_structural'] for r in metadata)):
   select=torch.tensor([r['best_postdiscard_structural']==shanten for r in metadata]);groups['best_postdiscard_structural:'+str(shanten)]=action_value_metrics(p[select],y[select],mask[select])
  return {'per_head_loss':{k:v/n for k,v in heads.items()},'action_groups':groups,'state_v_mae_raw':float((value-vt).abs().mean()),'state_v_mse_raw':float((value-vt).square().mean()),'state_v_target_mean':float(vt.mean()),'state_zero_baseline_mae':float(vt.abs().mean()),'interpretation':'teacher preference ranking and policy-conditioned terminal V, not counterfactual Q; no net-strength evaluation'}
 for epoch in range(start_epoch,epochs):
  model.train();heads=dict(resumed_heads) if epoch==start_epoch and skip else {};n=resumed_rows if epoch==start_epoch and skip else 0;next_batch=skip
  for index,(inp,t,meta) in enumerate(batches(m['files']['train'],device,batch_size)):
   if epoch==start_epoch and index<skip:continue
   stop(epoch,index);o=model(*inp);ls=v3_losses(o,t,inp[2]);opt.zero_grad();sum(ls[k]*config['loss_weights'][k] for k in ls).backward();torch.nn.utils.clip_grad_norm_(model.parameters(),5.);opt.step();steps+=1;next_batch=index+1;n+=len(meta)
   for k,v in ls.items():heads[k]=heads.get(k,0.)+float(v.detach())*len(meta)
  val=evaluate(epoch,next_batch);score=val['per_head_loss']['action_value_mse'];improved=score<best
  if improved:best=score;best_epoch=epoch
  state=save(epoch,True,0)
  if improved:
   dest=out/('best_epoch_'+str(epoch)+'.pt')
   if dest.exists():raise ValueError('Best snapshot immutable')
   torch.save(state,dest);(out/'BEST.tmp').write_text(json.dumps({'checkpoint':dest.name,'epoch':epoch,'validation_action_mse':best}));os.replace(out/'BEST.tmp',out/'BEST.json')
  with (out/'resources.jsonl').open('a') as f:f.write(json.dumps({'epoch':epoch,**resources(device)})+'\n')
  with (out/'metrics.jsonl').open('a') as f:f.write(json.dumps({'epoch':epoch,'train_head_loss':{k:v/max(n,1) for k,v in heads.items()},'validation':val,'optimizer_steps':steps})+'\n')
  skip=0
 summary={'complete':True,'epochs_limit':epochs,'best_epoch':best_epoch,'optimizer_steps':steps,'seconds_this_invocation':time.perf_counter()-started,'binding':binding,'rule_version':'SICHUAN-XUEZHAN-4FAN-V3','comparison_caveat':'same6epochs but more data means moreoptimizersteps; not data-only causal','reference100_optimizersteps':60,'loss_mode':mode,'state_head_supervised':mode=='multitask','train_games':m.get('train_games'),'validation_games':m.get('validation_games'),'target_semantics':m['target_semantics'],'state_target_policy':m['state_target_policy'],'source_hashes':sources,'formal_RL':False,'playing_strength_promotion_claimed':False,'resources':resources(device)};(out/'COMPLETE.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))


def resources(device):
 r={'utc_seconds':time.time(),'device':device}
 if device=='cuda':r.update(cuda_peak_allocated_bytes=torch.cuda.max_memory_allocated(),cuda_peak_reserved_bytes=torch.cuda.max_memory_reserved())
 if os.name=='nt':
  class Counters(ctypes.Structure):
   _fields_=[('cb',ctypes.c_ulong),('faults',ctypes.c_ulong)]+[(n,ctypes.c_size_t) for n in ('peak_working_set','working_set','peak_paged','paged','peak_nonpaged','nonpaged','pagefile','peak_pagefile')]
  c=Counters();c.cb=ctypes.sizeof(c);handle=ctypes.windll.kernel32.GetCurrentProcess();ctypes.windll.psapi.GetProcessMemoryInfo.argtypes=[ctypes.c_void_p,ctypes.POINTER(Counters),ctypes.c_ulong]
  if ctypes.windll.psapi.GetProcessMemoryInfo(handle,ctypes.byref(c),c.cb):r.update(process_peak_working_set_bytes=c.peak_working_set,process_working_set_bytes=c.working_set)
 try:r['gpu_sample']=subprocess.check_output(['nvidia-smi','--query-gpu=temperature.gpu,memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True,timeout=5).strip()
 except Exception as e:r['gpu_sample_error']=repr(e)
 return r


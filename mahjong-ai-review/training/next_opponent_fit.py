"""Fixed6epoch final-only training; never reads auxiliary records or selects best."""
import hashlib,json,os,pathlib,random,time,torch
from models.next_opponent import OpponentAblation,FAMILIES
from training.next_opponent_pipeline import read,batches,losses
from training.next_opponent_gate import validate

def train(manifest,auxiliary,admission,output,family,root,device='cuda',resume=False):
 root=pathlib.Path(root);audit=validate(manifest,auxiliary,admission,root);m=read(manifest);config={'epochs':6,'batch_size':128,'seed':42,'family':family,'parameters':19563,'learning_rate':.001,'loss_weights':{'structural_tenpai_bce':1.,'conditional_structural_wait_bce':1.,'legal_joint_ce':1.},'selection':'fixed_final_epoch5_no_validation_selection','calibration':'none'}
 if family not in FAMILIES:raise ValueError('Unknown family')
 binding=hashlib.sha256(json.dumps({'audit':audit,'config':config},sort_keys=True).encode()).hexdigest();out=pathlib.Path(output)
 if (out/'COMPLETE.json').exists():raise ValueError('Completed output immutable')
 if out.exists() and any(out.iterdir()) and (not resume or not (out/'last.pt').exists()):raise ValueError('Nonempty output requires resumable checkpoint')
 torch.set_num_threads(2);torch.manual_seed(42);random.seed(42);model=OpponentAblation(family).to(device);optimizer=torch.optim.Adam(model.parameters(),lr=.001);out.mkdir(parents=True,exist_ok=True);epoch_start=0;skip=0;steps=0;previous_heads={};previous_n=0;began=time.perf_counter()
 if device=='cuda':torch.cuda.reset_peak_memory_stats()
 if resume and (out/'last.pt').exists():
  checkpoint=torch.load(out/'last.pt',map_location=device,weights_only=False)
  if checkpoint['binding']!=binding:raise ValueError('Resume source/data/family/config mismatch')
  model.load_state_dict(checkpoint['model']);optimizer.load_state_dict(checkpoint['optimizer']);torch.set_rng_state(checkpoint['rng'].cpu());random.setstate(checkpoint['python_rng'])
  if checkpoint['cuda_rng'] and torch.cuda.is_available():torch.cuda.set_rng_state_all([r.cpu() for r in checkpoint['cuda_rng']])
  epoch_start=checkpoint['epoch']+int(checkpoint['epoch_complete']);skip=0 if checkpoint['epoch_complete'] else checkpoint['next_batch_index'];steps=checkpoint['optimizer_steps'];previous_heads=checkpoint['train_epoch_heads'];previous_n=checkpoint['train_epoch_rows']
 def save(epoch,complete,next_batch):
  checkpoint={'version':'NEXT-OPPONENT-ABLATION-v1','binding':binding,'config':config,'audit':audit,'model':model.state_dict(),'optimizer':optimizer.state_dict(),'epoch':epoch,'epoch_complete':complete,'next_batch_index':next_batch,'optimizer_steps':steps,'rng':torch.get_rng_state(),'cuda_rng':torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],'python_rng':random.getstate(),'train_epoch_heads':heads,'train_epoch_rows':n}
  torch.save(checkpoint,out/'last.tmp');os.replace(out/'last.tmp',out/'last.pt');return checkpoint
 def stop(epoch,index):
  flag=os.environ.get('MAHJONG_STOP_FILE')
  if flag and pathlib.Path(flag).exists():save(epoch,False,index);raise SystemExit(75)
 for epoch in range(epoch_start,6):
  model.train();heads=dict(previous_heads) if epoch==epoch_start and skip else {};n=previous_n if epoch==epoch_start and skip else 0
  for index,(rows,inputs,targets) in enumerate(batches(m['shards']['train'],device,family,128)):
   if epoch==epoch_start and index<skip:continue
   stop(epoch,index);optimizer.zero_grad();ls=losses(model(*inputs),targets);sum(ls.values()).backward();torch.nn.utils.clip_grad_norm_(model.parameters(),5.);optimizer.step();steps+=1;n+=len(rows)
   for k,v in ls.items():heads[k]=heads.get(k,0.)+float(v.detach())*len(rows)
   stop(epoch,index+1)
  state=save(epoch,True,0);snapshot=out/('epoch_'+str(epoch)+'.pt')
  if snapshot.exists():raise ValueError('Epoch checkpoint immutable')
  torch.save(state,snapshot)
  with (out/'metrics.jsonl').open('a') as log:log.write(json.dumps({'epoch':epoch,'train_per_head_loss':{k:v/n for k,v in heads.items()},'rows':n,'optimizer_steps':steps})+'\n')
  skip=0
 if validate(manifest,auxiliary,admission,root)!=audit:raise ValueError('Source/data/admission changed during training')
 summary={'complete':True,'final_checkpoint':'epoch_5.pt','optimizer_steps':steps,'config':config,'seconds':time.perf_counter()-began,'binding':binding,'auxiliary_records_read':0,'old_validation_records_read':0,'calibration_performed':False,'cuda_peak_allocated_bytes':torch.cuda.max_memory_allocated() if device=='cuda' else None,'cuda_peak_reserved_bytes':torch.cuda.max_memory_reserved() if device=='cuda' else None,'caveat':'equal allocated parameters; disabled history/static input blocks have no useful gradient, so effective capacity differs'}
 (out/'COMPLETE.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));return summary

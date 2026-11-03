"""Independent actual V3 trainer STOP/resume parity; main best untouched.
Stop is injected before training batch3 via a test-only loader wrapper, leaving
production trainer source unchanged. No final-test or RL execution.
"""
import pathlib,sys,argparse,os,json,subprocess,torch,hashlib
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
p=argparse.ArgumentParser();p.add_argument('--child',choices=['interrupt','resume','control']);a=p.parse_args();stop=root/'reports/v3_c_resume_TEST_STOP';base=root/'checkpoints/v3_T2_resume_smoke';control=root/'checkpoints/v3_T2_resume_control'
if a.child:
 import training.v3_supervised as module
 os.environ['MAHJONG_STOP_FILE']=str(stop);torch.set_num_threads(2)
 if a.child=='interrupt':
  original=module.batches;triggered=False
  def wrapped(path,device,size):
   global triggered
   for index,item in enumerate(original(path,device,size)):
    if str(path).endswith('train.jsonl') and index==3 and not triggered:stop.write_text('test stop after3optimizersteps');triggered=True
    yield item
  module.batches=wrapped
 module.train(root/'datasets/v3_teacher100/manifest.json',root/'reports/v3_chief_t2_admission.json',control if a.child=='control' else base,root,epochs=2,batch_size=128,seed=42,device='cuda',resume=a.child!='interrupt')
else:
 main=root/'checkpoints/v3_T2_teacher100_seed42/best_epoch_5.pt';before=hashlib.sha256(main.read_bytes()).hexdigest();codes={}
 for mode,expected in [('interrupt',75),('resume',0),('control',0)]:
  command=[sys.executable,str(pathlib.Path(__file__).resolve()),'--child',mode]
  r=subprocess.run(command,capture_output=True,text=True);(root/('reports/v3_c_resume_'+mode+'.log')).write_text(r.stdout+'\n'+r.stderr);codes[mode]=r.returncode
  if r.returncode!=expected:raise RuntimeError(mode+' exit='+str(r.returncode)+': '+r.stderr)
  if mode=='interrupt':
   interrupted=torch.load(base/'last.pt',map_location='cpu',weights_only=False);assert interrupted['optimizer_steps']==3 and interrupted['next_batch_index']==3 and not interrupted['epoch_complete'];stop.unlink()
 left=torch.load(base/'last.pt',map_location='cpu',weights_only=False);right=torch.load(control/'last.pt',map_location='cpu',weights_only=False);diff=max(float((left['model'][k]-right['model'][k]).abs().max()) for k in left['model']);assert diff<1e-6;assert left['optimizer_steps']==right['optimizer_steps']==16
 assert hashlib.sha256(main.read_bytes()).hexdigest()==before
 report={'test_scope':'actual_admitted_T2_trainer_stop_resume_correctness_only','child_exit_codes':codes,'interrupt_after_optimizer_steps':3,'restored_next_batch_cursor':3,'final_optimizer_steps':16,'max_parameter_abs_difference':diff,'exact_parameter_parity':diff==0,'main_best_unchanged_sha256':before,'CUDA_RNG_saved_restored':bool(left['cuda_rng']),'optimizer_state_restored':bool(left['optimizer']['state']),'no_final_test_used':True,'rl_performed':False,'harness_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()};(root/'reports/v3_c_T2_resume_stop_smoke.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

"""Actual candidate STOP checkpoint and resumed-control parity."""
import pathlib,sys,subprocess,os,json,shutil,torch
root=pathlib.Path(__file__).resolve().parents[1];out=root/'experiments/round2_c/candidate_stop_probe';out.mkdir(exist_ok=True);source=root/'experiments/round2_c/candidate_resume_probe';main_report=root/'reports/round2_c_candidate.json';original=main_report.read_bytes()
for split in ('train','validation'):shutil.copytree(source/split,out/split,dirs_exist_ok=True)
stop=out/'STOP';stop.write_text('checkpoint test');cmd=[sys.executable,str(root/'scripts/round2_model_candidate.py'),'--out',str(out),'--games','4','--val-games','2','--epochs','2','--resume'];env=os.environ.copy();env['MAHJONG_STOP_FILE']=str(stop)
try:
 result=subprocess.run(cmd,env=env,capture_output=True,text=True);assert result.returncode==75,result.stderr;s=torch.load(out/'last.pt',weights_only=False);assert s['interrupted_epoch_restarts'] and s['epoch']==-1;stop.unlink();result=subprocess.run(cmd,capture_output=True,text=True);assert result.returncode==0,result.stderr;a=torch.load(out/'last.pt',weights_only=False);b=torch.load(root/'experiments/round2_c/candidate_resume_control/last.pt',weights_only=False);equal=all(torch.equal(a['model'][k],b['model'][k]) for k in a['model']);assert equal;r={'stop_exit':75,'last_checkpoint_saved':True,'resume_equals_uninterrupted':equal};(root/'reports/round2_c_candidate_stop.json').write_text(json.dumps(r,indent=2));print(r)
finally:main_report.write_bytes(original)

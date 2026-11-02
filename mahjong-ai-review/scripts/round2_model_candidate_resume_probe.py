"""Actual candidate CLI --resume versus uninterrupted control. CPU2 only."""
import pathlib,subprocess,sys,json,torch
root=pathlib.Path(__file__).resolve().parents[1];report=root/'reports/round2_c_candidate.json';original=report.read_bytes();base=root/'experiments/round2_c/candidate_resume_probe';control=root/'experiments/round2_c/candidate_resume_control';script=root/'scripts/round2_model_candidate.py'
def run(out,epochs,resume=False):
 cmd=[sys.executable,str(script),'--out',str(out),'--games','4','--val-games','2','--epochs',str(epochs)]
 if resume:cmd.append('--resume')
 result=subprocess.run(cmd,capture_output=True,text=True);assert result.returncode==0,result.stderr
try:
 run(base,1);(base/'result.json').rename(base/'stage1_result.json');run(base,2,True);run(control,2)
 a=torch.load(base/'last.pt',weights_only=False);b=torch.load(control/'last.pt',weights_only=False);equal=all(torch.equal(a['model'][k],b['model'][k]) for k in a['model']);assert equal and a['epoch']==1 and a['optimizer']['state']
 r={'actual_cli_resume':True,'resumed_epoch':a['epoch'],'optimizer_restored':True,'model_exactly_equals_uninterrupted':equal,'train_games':4,'validation_games':2,'scope':'resume_correctness_only'};(root/'reports/round2_c_candidate_resume.json').write_text(json.dumps(r,indent=2));print(r)
finally:report.write_bytes(original)

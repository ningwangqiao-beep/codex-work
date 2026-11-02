"""Actual subprocess queue failure/resume check, using a small local probe."""
import json,pathlib,subprocess,sys,time,hashlib
root=pathlib.Path(__file__).resolve().parents[1]
if len(sys.argv)>1:
    if sys.argv[1]=='fail':raise SystemExit(7)
    p=root/'experiments/scheduler_probe/count.txt';p.write_text(str(int(p.read_text())+1) if p.exists() else '1');raise SystemExit(0)
d=root/'experiments'/('scheduler_probe_'+str(time.time_ns()));d.mkdir(parents=True,exist_ok=True)
q={'run_dir':str((d/'run').relative_to(root)),'limits':{'min_free_ram_gb':.1,'poll_seconds':.1},'jobs':[{'id':'one','script':'scripts/chief_scheduler_probe.py','args':['ok']},{'id':'failure','script':'scripts/chief_scheduler_probe.py','args':['fail'],'depends':['one']}]}
q['jobs'][0]['fingerprints']={'scripts/chief_scheduler_probe.py':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
p=d/'queue.json';p.write_text(json.dumps(q));cmd=[sys.executable,str(root/'scheduler/runner.py'),str(p)]
subprocess.run(cmd,check=False);s=json.loads((d/'run/state.json').read_text());assert s['jobs']['one']['status']=='completed' and s['jobs']['failure']['status']=='failed'
q['jobs'][1]['args']=['ok'];p.write_text(json.dumps(q));subprocess.run(cmd,check=True)
s=json.loads((d/'run/state.json').read_text());assert s['status']=='completed' and s['jobs']['one']['attempt']==1
r={'failure_stopped':True,'completed_job_skipped_on_resume':True,'failed_job_retried':s['jobs']['failure']['attempt']==2}
(root/'reports/round2_scheduler_probe.json').write_text(json.dumps(r,indent=2));print(r)

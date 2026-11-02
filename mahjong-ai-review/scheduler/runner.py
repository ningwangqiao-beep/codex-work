"""Local, single-job experiment queue. No network, shell, or generated commands."""
import argparse, ctypes, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
try:
    from scheduler.audit_helpers import append_event
except ModuleNotFoundError:
    from audit_helpers import append_event

ROOT=Path(__file__).resolve().parents[1]
def alive(pid):
    if os.name=='nt':
        k=ctypes.windll.kernel32;k.OpenProcess.restype=ctypes.c_void_p
        h=k.OpenProcess(0x1000,False,int(pid))
        if not h:return False
        code=ctypes.c_ulong();ok=k.GetExitCodeProcess(ctypes.c_void_p(h),ctypes.byref(code));k.CloseHandle(ctypes.c_void_p(h));return bool(ok and code.value==259)
    try:os.kill(pid,0);return True
    except OSError:return False
def save(p,v):
    tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(v,indent=2),encoding='utf-8');tmp.replace(p)
def memory_free_gb():
    if os.name!='nt': return 100.
    class M(ctypes.Structure):
        _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(n,ctypes.c_ulonglong) for n in ('total','available','page','availpage','virtual','availvirtual','extended')]
    m=M();m.length=ctypes.sizeof(m);ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m));return m.available/2**30
def gpu():
    try:
        s=subprocess.check_output(['nvidia-smi','--query-gpu=temperature.gpu,memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True,timeout=10)
        t,m,u=map(float,s.splitlines()[0].split(','));return {'temperature':t,'memory_mib':m,'utilization':u}
    except Exception as e: return {'error':str(e)}
def inside(p):
    p=p.resolve();p.relative_to(ROOT);return p
def run(queue_path):
    q=json.loads(queue_path.read_text(encoding='utf-8-sig'));directory=inside(ROOT/q['run_dir']);directory.mkdir(parents=True,exist_ok=True)
    state_path=directory/'state.json';lock=ROOT/'scheduler/project_runner.lock'
    if lock.exists():
        old=json.loads(lock.read_text())
        if alive(old['pid']):raise RuntimeError('Runner already active; do not duplicate')
        lock.unlink()
    with lock.open('x') as f:json.dump({'pid':os.getpid()},f)
    state=json.loads(state_path.read_text()) if state_path.exists() else {'jobs':{},'started':time.time()}
    state['pid']=os.getpid();state['status']='running';state.pop('error',None);state.pop('finished',None);save(state_path,state)
    limits=q.get('limits',{});deadline=state['started']+limits.get('max_hours',8)*3600
    child=None
    try:
      for job in q['jobs']:
        key=job['id'];entry=state['jobs'].get(key,{})
        if not re.fullmatch('[A-Za-z0-9_-]+',key):raise ValueError('Invalid job id')
        digest=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()
        for name,source_hash in job.get('fingerprints',{}).items():
            if hashlib.sha256(inside(ROOT/name).read_bytes()).hexdigest()!=source_hash:raise RuntimeError('Source changed '+name)
        if entry.get('status')=='completed':
            if entry.get('job_sha256')!=digest:raise RuntimeError('Completed job definition changed or legacy state: '+key)
            continue
        if entry.get('status')=='running' and entry.get('child_pid'):
            if alive(entry['child_pid']):raise RuntimeError('Previous child still active; refusing duplicate '+key)
        if any(state['jobs'].get(d,{}).get('status')!='completed' for d in job.get('depends',[])):raise RuntimeError('Dependency missing '+key)
        script=inside(ROOT/job['script'])
        if script.suffix!='.py':raise ValueError('Only project Python scripts accepted')
        rl_script=script.name in {'round2_data_policy.py','round2_data_candidate_rl.py'} and '--evaluate' not in job.get('args',[])
        if rl_script or job.get('kind')=='reinforcement_learning':
            gate=json.loads((ROOT/'configs/rl_admission.json').read_text())
            if gate.get('reinforcement_learning_allowed') is not True:raise RuntimeError('RL admission closed: '+gate.get('reason','audit incomplete'))
        if (directory/'STOP').exists():raise RuntimeError('User STOP requested')
        if memory_free_gb()<limits.get('min_free_ram_gb',1.):raise RuntimeError('Insufficient free RAM before '+key)
        request=directory/'STOP_CHECKPOINT_REQUESTED';request.unlink(missing_ok=True)
        env=os.environ.copy();env.update(OMP_NUM_THREADS=str(limits.get('cpu_threads',4)),MKL_NUM_THREADS=str(limits.get('cpu_threads',4)),PYTHONUNBUFFERED='1',MAHJONG_STOP_FILE=str(request))
        entry={'status':'running','started':time.time(),'attempt':entry.get('attempt',0)+1,'job_sha256':digest};state['jobs'][key]=entry;save(state_path,state)
        with (directory/(key+'.log')).open('a',encoding='utf-8') as log:
          child=subprocess.Popen([sys.executable,str(script),*job.get('args',[])],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
          entry['child_pid']=child.pid;save(state_path,state);append_event(directory/'attempts.jsonl',{'event':'started','job':key,**entry})
          reason=None
          while child.poll() is None:
            sample={'time':time.time(),'free_ram_gb':memory_free_gb(),'gpu':gpu()}
            with (directory/'resources.jsonl').open('a') as f:f.write(json.dumps(sample)+'\n')
            if (directory/'STOP').exists():reason='STOP requested'
            if sample['free_ram_gb']<limits.get('min_free_ram_gb',1.):reason='RAM limit'
            g=sample['gpu']
            if 'error' in g:reason='GPU monitor unavailable'
            if g.get('temperature',0)>limits.get('max_gpu_temperature',82) or g.get('memory_mib',0)>limits.get('max_gpu_memory_mib',7200):reason='GPU resource limit'
            if time.time()>deadline or time.time()-entry['started']>job.get('timeout_seconds',3600):reason='Time limit'
            if reason:
                (directory/'STOP_CHECKPOINT_REQUESTED').write_text(reason)
                # Trainers may notice the shared request and checkpoint voluntarily.
                try: child.wait(timeout=limits.get('checkpoint_grace_seconds',30))
                except subprocess.TimeoutExpired:child.terminate();child.wait(timeout=30)
                break
            time.sleep(limits.get('poll_seconds',5))
          entry.update(status='completed' if child.returncode==0 and not reason else 'failed',exit_code=child.returncode,reason=reason,finished=time.time());save(state_path,state);append_event(directory/'attempts.jsonl',{'event':'finished','job':key,**entry})
          if entry['status']!='completed':raise RuntimeError('Job failed: '+key)
      state['status']='completed'
    except Exception as e:
      state['status']='stopped';state['error']=str(e)
    finally:
      if child is not None and child.poll() is None:
        (directory/'STOP_CHECKPOINT_REQUESTED').write_text('Scheduler exception; checkpoint requested')
        try:child.wait(timeout=30)
        except subprocess.TimeoutExpired:child.terminate();child.wait(timeout=30)
      state['finished']=time.time();save(state_path,state);lock.unlink(missing_ok=True)
      (directory/'REPORT.md').write_text('# Local experiment queue\n\n'+json.dumps(state,indent=2)+'\n',encoding='utf-8')
    return 0 if state['status']=='completed' else 1
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('queue');a=p.parse_args();sys.exit(run(inside(Path(a.queue))))

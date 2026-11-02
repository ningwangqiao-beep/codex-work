import sys,json,hashlib,time,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from simulator.selfplay import play
root=Path(__file__).resolve().parents[1]
sources=[root/'rules/core.py',root/'simulator/table.py',root/'simulator/selfplay.py',root/'observations/public.py']
before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources};start=time.perf_counter()
test=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests'],cwd=root,capture_output=True,text=True)
(root/'reports/round2_d_policy_audit_tests.txt').write_text(test.stdout+test.stderr)
assert test.returncode==0
steps=0
for seed in range(970000,971000):steps+=play(seed)['steps']
after={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources};assert before==after
r=dict(passed=True,source_hashes=after,games=1000,steps=steps,seconds=time.perf_counter()-start,simulation_only=True,tests_sha256=hashlib.sha256((root/'reports/round2_d_policy_audit_tests.txt').read_bytes()).hexdigest())
(root/'reports/round2_d_policy_audit.json').write_text(json.dumps(r,indent=2));print(r)

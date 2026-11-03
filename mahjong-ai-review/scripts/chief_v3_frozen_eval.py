"""Predeclared frozen V3 evaluation; no training or test-driven tuning."""
import hashlib,json,os,pathlib,subprocess,sys
r=pathlib.Path(__file__).resolve().parents[1]
ready=json.loads((r/'reports/v3_chief_ready.json').read_text())
if not ready.get('passed'):raise RuntimeError('V3 audit readiness missing')
for name,h in ready['source_hashes'].items():
    if hashlib.sha256((r/name).read_bytes()).hexdigest()!=h:raise RuntimeError('V3 audit source drift '+name)
for n,s in [(1000,3200000),(10000,3300000)]:
    a=json.loads((r/'reports'/f'v3_d_batch_{n}_{s}.json').read_text())
    if a['games']!=n or not a['unchanged'] or a['source_hashes']!=ready['source_hashes']:raise RuntimeError('V3 batch audit mismatch')
seed=5000000;groups=5000;final=r/'reports'/f'v3_d_compare_{seed}_mixed.json';partial=final.with_suffix('.jsonl')
if final.exists():
    if json.loads(final.read_text()).get('complete_seed_groups')==groups:raise SystemExit(0)
    raise RuntimeError('Existing final output is not complete')
args=[sys.executable,str(r/'scripts/v3_data_resumable_compare.py'),'--games',str(groups),'--seed',str(seed),'--strong','--opponents','mixed','--timeout','21600']
if partial.exists():args.append('--resume')
code=subprocess.call(args,cwd=r)
if code:raise SystemExit(code)
v=json.loads(final.read_text())
if v.get('status')!='completed' or v.get('complete_seed_groups')!=groups:raise RuntimeError('Final evaluation incomplete')
print('Frozen V3 evaluation completed: 5000 seed groups, 4 seats, 5 policies')

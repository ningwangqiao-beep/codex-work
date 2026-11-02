"""Wait for an existing queue, then launch the explicitly configured next queue."""
import json,sys,time,subprocess
from pathlib import Path
from runner import alive
root=Path(__file__).resolve().parents[1]
previous=(root/sys.argv[1]).resolve();following=(root/sys.argv[2]).resolve()
previous.relative_to(root);following.relative_to(root)
while True:
    s=json.loads(previous.read_text())
    if s['status']=='completed':break
    if s['status']=='stopped':raise SystemExit('Previous queue stopped; manual diagnosis required')
    if not alive(s['pid']):
        s=json.loads(previous.read_text())
        if s['status']=='completed':break
        raise SystemExit('Previous runner died; explicit resume required')
    time.sleep(5)
raise SystemExit(subprocess.call([sys.executable,str(root/'scheduler/runner.py'),str(following)],cwd=root))

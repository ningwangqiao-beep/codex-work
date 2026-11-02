import sys,json,pathlib,unittest,hashlib
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from training.gate import validate_manifest
import torch
results={}
for version in ('simulation_v1','simulation_v2'):
    m=json.loads((root/'datasets'/version/'manifest.json').read_text())
    results[version]={'dataset_fingerprint':validate_manifest(m)}
    p=root/'checkpoints'/m['dataset_version']/'best.pt'
    if not p.exists():p=root/'checkpoints'/version/'best.pt'
    s=torch.load(p,map_location='cpu',weights_only=False)
    assert s['dataset_fingerprint']==results[version]['dataset_fingerprint']
    assert 'optimizer' in s and all(torch.isfinite(v).all() for v in s['model'].values())
    results[version].update(checkpoint_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),epoch=s['epoch'],dataset_version=s['dataset_version'])
test=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover(str(root/'tests')))
results['tests']={'run':test.testsRun,'failures':len(test.failures),'errors':len(test.errors)}
(root/'reports/round2_chief_independent_audit.json').write_text(json.dumps(results,indent=2))
assert test.wasSuccessful()
print(json.dumps(results,indent=2))

import hashlib,json,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from training.gate import validate_manifest
results={}
for p in sorted((root/'datasets').glob('*/manifest.json')):
    m=json.loads(p.read_text());fingerprint=validate_manifest(m);snap=p.parent/'source_snapshot';checks={}
    for name,expected in m.get('pipeline_sha256',{}).items():
        f=snap/pathlib.PureWindowsPath(name).name
        if not f.exists():raise ValueError('Missing frozen pipeline source '+str(f))
        checks[name]=hashlib.sha256(f.read_bytes()).hexdigest()==expected
    if checks and not all(checks.values()):raise ValueError('Frozen source mismatch '+str(p))
    results[str(p.parent.relative_to(root))]={'dataset_version':m['dataset_version'],'actual_manifest_gate_passed':True,'dataset_fingerprint':fingerprint,'frozen_pipeline_source_matches':checks}
(root/'reports/revision_chief_data_fingerprints.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))

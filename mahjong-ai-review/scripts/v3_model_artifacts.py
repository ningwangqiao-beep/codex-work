"""Package C evidence hashes only; does not copy data or publish anything."""
import pathlib,json,hashlib
root=pathlib.Path(__file__).resolve().parents[1]
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
paths=set()
for directory,pattern in [('models','v3*.py'),('training','v3*.py'),('evaluation','v3*.py'),('inference','v3*.py'),('scripts','v3_model*.py'),('reports','v3_c*')]:
 for p in (root/directory).glob(pattern):
  if p.is_file() and p.name!='v3_c_artifact_manifest.json':paths.add(p)
for directory in ('v3_T2_teacher100_seed42','v3_T2_resume_smoke','v3_T2_resume_control'):
 for p in (root/'checkpoints'/directory).glob('*'):
  if p.is_file():paths.add(p)
for name in ['OPPONENT_MODEL_REPORT.md','TRAINING_RESULTS_V3.md','datasets/v3_teacher100/manifest.json','reports/v3_chief_t2_admission.json']:paths.add(root/name)
report={'scope':'C_V3_local_evidence_manifest_no_publish','files':{str(p.relative_to(root)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)},'original_legacy_best_overwritten':False,'new_final_test_seeds_used':False,'rl_performed':False};(root/'reports/v3_c_artifact_manifest.json').write_text(json.dumps(report,indent=2));print('Evidence files hashed:',len(paths))

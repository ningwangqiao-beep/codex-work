"""Combined candidate-relative input + pairwise ranking gate (not single-factor)."""
import pathlib,json
from training.v3_gate import inspect_v3_data,sha,bound_evidence
VERSION='SICHUAN-XUEZHAN-4FAN-V3'
def validate_next_manifest(path,root,admission_path):
 root=pathlib.Path(root);data,m=inspect_v3_data(path,root);a=json.load(open(admission_path))
 if m.get('dataset_version')!='next-history100' or a.get('stage')!='NEXT_HISTORY100_RELATIVE_COMBO' or a.get('rule_version')!=VERSION or a.get('manifest_sha256')!=sha(path):raise ValueError('New-history admission mismatch')
 for flag in ('relative_combo_allowed','passed','supervised_training_allowed','baseline_development_audited','dataset_isolation_audited','state_target_definition_audited','history_v2_tests_passed','seed_family_split_audited'):
  if a.get(flag) is not True:raise ValueError('Missing chief admission '+flag)
 if a.get('rl_training_allowed') is not False:raise ValueError('No RL admission')
 for k in ('rules/core.py','rules/v3.py','simulator/table.py','simulator/v3_history_v2.py','observations/v3_history_v2.py'):
  rel=next((r for r in m['source_hashes'] if r.replace('\\','/')==k),None)
  if rel is None or a.get('source_hashes',{}).get(rel)!=m['source_hashes'][rel]:raise ValueError('Missing new rule/history source binding '+k)
 for evidence in ('full_tests','history_tests','data_isolation','terminal_returns'):
  spec=a[evidence];p=pathlib.Path(spec['path']);p=p if p.is_absolute() else root/p
  if sha(p)!=spec['sha256']:raise ValueError('Evidence hash mismatch '+evidence)
  if spec.get('exit_code')!=0:raise ValueError('Evidence not successful '+evidence)
 data.update(training_allowed=True,admission_sha256=sha(admission_path),scope='combined candidate-relative input + pairwise ranking; not single-factor');return data

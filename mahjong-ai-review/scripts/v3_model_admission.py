"""Check V3 supervised admission; deliberately has no train or RL mode."""
import pathlib,sys,json,argparse,tempfile
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root));from training.v3_gate import validate_v3_manifest,inspect_v3_data
p=argparse.ArgumentParser();p.add_argument('--manifest');p.add_argument('--admission');p.add_argument('--inspect-only',action='store_true');p.add_argument('--output',required=True);p.add_argument('--rejection-smoke',action='store_true');a=p.parse_args()
if a.rejection_smoke:
 with tempfile.TemporaryDirectory() as d:
  path=pathlib.Path(d)/'incomplete.json';path.write_text('{}')
  try:validate_v3_manifest(path,root)
  except ValueError as e:r={'expected_rejection':str(e),'formal_training_started':False,'rl_started':False}
  else:raise AssertionError('Missing admission accepted')
else:
 if not a.manifest:p.error('--manifest required')
 r=inspect_v3_data(a.manifest,root)[0] if a.inspect_only else validate_v3_manifest(a.manifest,root,a.admission)
pathlib.Path(a.output).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

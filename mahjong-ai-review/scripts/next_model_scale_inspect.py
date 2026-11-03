import sys,pathlib,json,argparse
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root));from training.next_scale_gate import inspect_scale
p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--output',required=True);a=p.parse_args();r=inspect_scale(a.manifest,root);pathlib.Path(a.output).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

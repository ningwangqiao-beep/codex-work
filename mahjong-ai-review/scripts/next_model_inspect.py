import sys,pathlib,argparse,json
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root));from training.v3_gate import inspect_v3_data
p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--output',required=True);a=p.parse_args();r,m=inspect_v3_data(a.manifest,root);r['dataset_version']=m['dataset_version'];pathlib.Path(a.output).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

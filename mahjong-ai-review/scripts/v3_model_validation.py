import sys,pathlib,argparse,json,torch,hashlib
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root));from evaluation.v3_validation import validate
p=argparse.ArgumentParser();p.add_argument('--checkpoint',required=True);p.add_argument('--manifest',required=True);p.add_argument('--output',required=True);a=p.parse_args();out=pathlib.Path(a.output)
if out.exists():raise ValueError('Validation diagnostic immutable')
torch.set_num_threads(2);r=validate(a.checkpoint,a.manifest);r['checkpoint_sha256']=hashlib.sha256(pathlib.Path(a.checkpoint).read_bytes()).hexdigest();out.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

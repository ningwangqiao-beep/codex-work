"""Execute admitted bounded V3 T2 only. No RL or test-evaluation mode."""
import sys,pathlib,argparse
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root));from training.v3_supervised import train
p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--admission',required=True);p.add_argument('--output',required=True);p.add_argument('--epochs',type=int,default=6);p.add_argument('--batch-size',type=int,default=128);p.add_argument('--seed',type=int,default=42);p.add_argument('--device',choices=['cpu','cuda'],default='cuda');p.add_argument('--resume',action='store_true');a=p.parse_args();train(a.manifest,a.admission,a.output,root,a.epochs,a.batch_size,a.seed,a.device,a.resume)

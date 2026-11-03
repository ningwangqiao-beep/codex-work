import argparse,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from training.next_opponent_tile_v2_eval import evaluate
p=argparse.ArgumentParser();p.add_argument('--checkpoint',required=True);p.add_argument('--manifest',required=True);p.add_argument('--auxiliary',required=True);p.add_argument('--admission',required=True);p.add_argument('--output',required=True);a=p.parse_args();evaluate(a.checkpoint,a.manifest,a.auxiliary,a.admission,a.output,root)

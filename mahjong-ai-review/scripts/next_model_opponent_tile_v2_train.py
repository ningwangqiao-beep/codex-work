"""Chief admitted fixed-budget public-information opponent ablation."""
import argparse,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.next_opponent_tile_v2 import FAMILIES
from training.next_opponent_tile_v2_fit import train
p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--auxiliary',required=True);p.add_argument('--admission',required=True);p.add_argument('--output',required=True);p.add_argument('--family',choices=FAMILIES,required=True);p.add_argument('--device',choices=['cpu','cuda'],default='cuda');p.add_argument('--resume',action='store_true');a=p.parse_args();train(a.manifest,a.auxiliary,a.admission,a.output,a.family,root,a.device,a.resume)

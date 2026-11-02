import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import argparse
from simulator.policy_learning import train
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--games',type=int,default=100);p.add_argument('--seed',type=int,default=900000);p.add_argument('--out',default='checkpoints/round2_policy');p.add_argument('--resume');p.add_argument('--selfplay',action='store_true');p.add_argument('--audit',required=True);a=p.parse_args();train(a.out,a.games,a.seed,a.resume,a.selfplay,a.audit)

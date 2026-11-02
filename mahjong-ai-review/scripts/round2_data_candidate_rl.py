import sys,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from simulator.candidate_learning import train,evaluate
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',default='experiments/round2_c/candidate/best.pt');p.add_argument('--audit',default='reports/round2_d_policy_audit.json');p.add_argument('--out',default='checkpoints/round2_candidate_rl');p.add_argument('--games',type=int,default=20);p.add_argument('--seed',type=int,default=2400000);p.add_argument('--temperature',type=float,default=1.);p.add_argument('--resume');p.add_argument('--evaluate');p.add_argument('--eval-out',default='reports/round2_d_candidate_eval.json');a=p.parse_args()
 if a.evaluate:evaluate(a.base,a.evaluate,a.eval_out,a.games,a.seed)
 else:train(a.base,a.audit,a.out,a.games,a.seed,a.temperature,a.resume)

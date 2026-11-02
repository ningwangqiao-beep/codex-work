"""CPU2 complete-game parity: rounded learned teacher versus exact teacher."""
import sys,pathlib,argparse,json,time,hashlib,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from inference.round2_candidate_policy import CandidatePolicy
from models.round2_candidate import teacher_utility,candidate_features
from models.round2_candidate_residual import CandidateResidual
from simulator.selfplay import play
p=argparse.ArgumentParser();p.add_argument('--checkpoint',default=str(root/'experiments/round2_c/candidate/best.pt'));p.add_argument('--games',type=int,default=20);p.add_argument('--seed',type=int,default=2300000);p.add_argument('--output',default=str(root/'reports/round2_c_candidate_game_parity.json'));a=p.parse_args();out=pathlib.Path(a.output)
if out.exists():raise RuntimeError('Completed parity immutable')
torch.set_num_threads(2);policy=CandidatePolicy(a.checkpoint);rows=[];start=time.perf_counter();action_mismatches=0;decisions=0
for seed in range(a.seed,a.seed+a.games):
 for seat in range(4):
  trace_a=[];trace_b=[]
  def learned(o,legal):
   global action_mismatches,decisions
   selected=policy(o,legal);target=max(legal,key=lambda t:teacher_utility(o,t));action_mismatches+=selected!=target;decisions+=1;trace_a.append(selected);return selected
  def teacher(o,legal):
   selected=max(legal,key=lambda t:teacher_utility(o,t));trace_b.append(selected);return selected
  learned_result=play(seed,policy=learned,policy_seat=seat);teacher_result=play(seed,policy=teacher,policy_seat=seat)
  row={'seed':seed,'seat':seat,'candidate_scores':learned_result['scores'],'teacher_scores':teacher_result['scores'],'same_action_trace':trace_a==trace_b,'same_scores':learned_result['scores']==teacher_result['scores']};rows.append(row)
# Residual starts at frozen base and learns only legal-candidate indices.
base=policy.model;residual=CandidateResidual(base);x=torch.randn(5,12);logits,v=residual(x);assert torch.equal(logits,(base(x)*64).round());dist,_=residual.distribution(x);assert 0<=int(dist.sample())<5
report={'checkpoint_sha256':hashlib.sha256(pathlib.Path(a.checkpoint).read_bytes()).hexdigest(),'seed_range':[a.seed,a.seed+a.games-1],'games':len(rows),'decisions':decisions,'action_mismatches':action_mismatches,'all_traces_equal':all(r['same_action_trace'] for r in rows),'all_scores_equal':all(r['same_scores'] for r in rows),'rows':rows,'seconds':time.perf_counter()-start,'scope':'validation_seed_complete_game_teacher_reproduction_only','playing_strength_improvement_claimed':False,'residual_zero_initialization_test':True,'rl_training_performed':False};out.write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2));assert report['all_traces_equal'] and report['all_scores_equal'] and not action_mismatches


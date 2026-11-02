"""Bounded residual actor critic, frozen public-only candidate base."""
import json,hashlib,os,random
from pathlib import Path
import torch
from models.round2_candidate import CandidateLinear,candidate_features
from models.round2_candidate_residual import CandidateResidual
from simulator.selfplay import play

def load(base):
 b=CandidateLinear();s=torch.load(base,map_location='cpu',weights_only=False);b.load_state_dict(s['model']);return CandidateResidual(b)
def binding(root,base,audit):
 a=json.loads(Path(audit).read_text());sources={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'rules/core.py',root/'simulator/table.py',root/'simulator/selfplay.py',root/'observations/public.py']}
 if not a.get('passed') or a.get('games',0)<1000 or a.get('source_hashes')!=sources:raise ValueError('Audit mismatch')
 extra={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'models/round2_candidate.py',root/'models/round2_candidate_residual.py',root/'simulator/candidate_learning.py',root/'scripts/round2_data_candidate_rl.py']}
 return dict(candidate_sources=extra,sources=sources,base=hashlib.sha256(Path(base).read_bytes()).hexdigest(),audit=hashlib.sha256(Path(audit).read_bytes()).hexdigest())
def train(base,audit,out,games=20,seed=2400000,temperature=1.,resume=None):
 torch.set_num_threads(2);torch.manual_seed(seed);random.seed(seed);root=Path(__file__).resolve().parents[1];bound=binding(root,base,audit);m=load(base);opt=torch.optim.Adam([p for p in m.parameters() if p.requires_grad],lr=.0003);start=0
 if resume:
  s=torch.load(resume,weights_only=False)
  if s['binding']!=bound or s['seed']!=seed or s['temperature']!=temperature:raise ValueError('Resume mismatch')
  m.load_state_dict(s['model']);opt.load_state_dict(s['optimizer']);torch.set_rng_state(s['rng']);random.setstate(s['python_rng']);start=s['games']
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 for index in range(start,games):
  stop=os.environ.get('MAHJONG_STOP_FILE')
  if stop and Path(stop).exists():raise SystemExit(75)
  decisions=[]
  def policy(o,legal):
   x=torch.tensor([candidate_features(o,t) for t in legal]);d,v=m.distribution(x,temperature);a=d.sample();decisions.append((d.log_prob(a),v,d.entropy(),o['observer_player']));return legal[int(a)]
  r=play(seed+index,policy=policy,policy_seat=None)
  loss=sum(-lp*(r['scores'][seat]/48-v.detach())+.5*(v-r['scores'][seat]/48).square()-.001*entropy for lp,v,entropy,seat in decisions)/max(1,len(decisions))
  opt.zero_grad();loss.backward();torch.nn.utils.clip_grad_norm_(m.parameters(),1);opt.step()
  state=dict(model=m.state_dict(),optimizer=opt.state_dict(),games=index+1,seed=seed,temperature=temperature,binding=bound,rng=torch.get_rng_state(),python_rng=random.getstate(),simulation_only=True)
  torch.save(state,out/'last.tmp');os.replace(out/'last.tmp',out/'last.pt')
  with (out/'metrics.jsonl').open('a') as f:f.write(json.dumps(dict(game=index,scores=r['scores'],loss=float(loss.detach()),decisions_by_seat=[sum(q==p for _,_,_,q in decisions) for p in range(4)]))+'\n')
 return m

def evaluate(base,checkpoint,out,games=20,seed=2500000):
 import statistics
 torch.set_num_threads(2);m=load(base);s=torch.load(checkpoint,weights_only=False);m.load_state_dict(s['model']);m.eval();rows=[]
 def baseline(o,c):
  from models.round2_candidate import teacher_utility
  return max(c,key=lambda t:teacher_utility(o,t))
 def learned(o,c):
  with torch.inference_mode():logits,_=m(torch.tensor([candidate_features(o,t) for t in c]))
  return c[int(logits.argmax())]
 for n,callback in [('base_teacher',baseline),('residual',learned)]:
  for k in range(seed,seed+games):
   for seat in range(4):rows.append(dict(policy=n,seed=k,seat=seat,score=play(k,policy=callback,policy_seat=seat)['scores'][seat]))
 diff=[sum(r['score']*(1 if r['policy']=='residual' else -1) for r in rows if r['seed']==k)/4 for k in range(seed,seed+games)];rng=random.Random(42);boot=sorted(statistics.mean(rng.choices(diff,k=len(diff))) for _ in range(2000));result=dict(rows=rows,mean_difference=statistics.mean(diff),paired_seed_bootstrap_95ci=[boot[50],boot[1949]],simulation_only=True,checkpoint_sha256=hashlib.sha256(Path(checkpoint).read_bytes()).hexdigest(),flags=['PAIRED_INITIAL_SEED_NOT_IDENTICAL_FUTURE','RESIDUAL_EVAL_GREEDY_TRAIN_SOFTMAX'])
 Path(out).write_text(json.dumps(result,indent=2));print({k:v for k,v in result.items() if k!='rows'})

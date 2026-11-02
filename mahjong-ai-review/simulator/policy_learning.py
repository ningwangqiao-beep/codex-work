"""Small discard-only actor critic. No hidden state enters policy."""
import json,random,os,hashlib
from pathlib import Path
import torch
from torch import nn
from observations.public import features
from simulator.selfplay import play
class PolicyValue(nn.Module):
 def __init__(self):
  super().__init__();self.body=nn.Sequential(nn.Linear(128,64),nn.Tanh());self.policy=nn.Linear(64,27);self.value=nn.Linear(64,1)
 def forward(self,x):
  z=self.body(x);return self.policy(z),self.value(z).squeeze(-1)
def train(out,games=100,seed=900000,resume=None,selfplay=False,audit=None):
 torch.set_num_threads(2);torch.manual_seed(seed);random.seed(seed);m=PolicyValue();opt=torch.optim.Adam(m.parameters(),lr=.0003);start=0
 root=Path(__file__).resolve().parents[1]
 bound={str(q.relative_to(root)):hashlib.sha256(q.read_bytes()).hexdigest() for q in (root/"rules/core.py",root/"simulator/table.py",root/"simulator/selfplay.py",root/"observations/public.py")}
 if audit is None:raise ValueError("Policy training needs bound audit JSON")
 audit_record=json.loads(Path(audit).read_text())
 if audit_record.get("source_hashes")!=bound or not audit_record.get("passed"):raise ValueError("Audit/source mismatch")
 if audit_record.get('games',0)<1000:raise ValueError('Insufficient strict audit games')
 log=root/'reports/round2_d_policy_audit_tests.txt'
 if not log.exists() or hashlib.sha256(log.read_bytes()).hexdigest()!=audit_record.get('tests_sha256'):raise ValueError('Audit test evidence mismatch')
 if resume:
  c=torch.load(resume,weights_only=False)
  if c.get('seed')!=seed or c.get('source_hashes')!=bound or c.get('selfplay',False)!=selfplay:raise ValueError('Resume seed/source mismatch or legacy unbound checkpoint')
  if c.get('audit_sha256')!=hashlib.sha256(Path(audit).read_bytes()).hexdigest():raise ValueError('Resume audit mismatch')
  random.setstate(c['python_rng'])
  m.load_state_dict(c['model']);opt.load_state_dict(c['optimizer']);start=c['games'];torch.set_rng_state(c['rng'])
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 for index in range(start,games):
  stop=os.environ.get("MAHJONG_STOP_FILE")
  if stop and Path(stop).exists():raise SystemExit(75)
  decisions=[]
  def callback(o,legal):
   logits,v=m(torch.tensor(features(o)).float());mask=torch.full((27,),float('-inf'));mask[list(legal)]=0
   d=torch.distributions.Categorical(logits=logits+mask);a=d.sample();decisions.append((d.log_prob(a),v,d.entropy(),o["observer_player"]));return int(a)
  seat=index%4;r=play(seed+index,policy=callback,policy_seat=None if selfplay else seat)
  if decisions:
   loss=sum(-lp*(r['scores'][q]/48-v.detach())+.5*(v-r['scores'][q]/48).square()-.001*entropy for lp,v,entropy,q in decisions)/len(decisions)
   opt.zero_grad();loss.backward();nn.utils.clip_grad_norm_(m.parameters(),1);opt.step()
  with (out/'metrics.jsonl').open('a') as f:f.write(json.dumps(dict(game=index,seed=seed+index,net_score=r['scores'][seat],scores=r['scores'],selfplay=selfplay,decisions_by_seat=[sum(q==p for _,_,_,q in decisions) for p in range(4)],decisions=len(decisions)))+'\n')
  torch.save(dict(selfplay=selfplay,audit_sha256=hashlib.sha256(Path(audit).read_bytes()).hexdigest(),source_hashes=bound,python_rng=random.getstate(),model=m.state_dict(),optimizer=opt.state_dict(),games=index+1,rng=torch.get_rng_state(),seed=seed,version='discard-actor-critic-v1',simulation_only=True),out/'last.tmp')
  os.replace(out/'last.tmp',out/'last.pt')
 return m

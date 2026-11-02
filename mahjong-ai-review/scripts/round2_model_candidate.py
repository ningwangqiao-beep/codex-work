"""Candidate-aware teacher distillation. CPU2, new train/validation games only."""
import sys,pathlib,argparse,json,hashlib,os,random,time,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.round2_candidate import CandidateLinear,candidate_features,teacher_utility,FEATURE_NAMES
from simulator.selfplay import play
p=argparse.ArgumentParser();p.add_argument('--out',default=str(root/'experiments/round2_c/candidate'));p.add_argument('--audit',default=str(root/'reports/round2_d_policy_audit.json'));p.add_argument('--games',type=int,default=80);p.add_argument('--val-games',type=int,default=30);p.add_argument('--epochs',type=int,default=20);p.add_argument('--resume',action='store_true');a=p.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True);torch.set_num_threads(2);torch.manual_seed(42);random.seed(42);start=time.perf_counter()
if (out/'result.json').exists():raise RuntimeError('Completed experiment immutable')
source={str(q.relative_to(root)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [root/'rules/core.py',root/'simulator/table.py',root/'simulator/selfplay.py',root/'observations/public.py']};audit=json.load(open(a.audit));auditsha=hashlib.sha256(pathlib.Path(a.audit).read_bytes()).hexdigest()
if audit.get('source_hashes')!=source or not audit.get('passed') or audit.get('games',0)<1000:raise ValueError('1000game audit/source binding failed')
if hashlib.sha256((root/'reports/round2_d_policy_audit_tests.txt').read_bytes()).hexdigest()!=audit.get('tests_sha256'):raise ValueError('audit evidence mismatch')
source['models/round2_candidate.py']=hashlib.sha256((root/'models/round2_candidate.py').read_bytes()).hexdigest();source['scripts/round2_model_candidate.py']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest();config={'train_seed':2100000,'validation_seed':2200000,'games':a.games,'val_games':a.val_games,'seed':42,'feature_names':FEATURE_NAMES}
def stopped():return os.environ.get('MAHJONG_STOP_FILE') and pathlib.Path(os.environ['MAHJONG_STOP_FILE']).exists()
# Commit each generated game as a separate shard; incomplete game output never exposed.
for split,count,seedbase in [('train',a.games,2100000),('validation',a.val_games,2200000)]:
 directory=out/split;directory.mkdir(exist_ok=True)
 for i in range(count):
  dest=directory/(str(seedbase+i)+'.jsonl')
  if dest.exists():continue
  if stopped():raise SystemExit(75)
  rows=[]
  def teacher(o,legal):
   utility=[teacher_utility(o,t) for t in legal];missing=o['declared_missing_suits'][o['observer_player']];rows.append({'game_id':seedbase+i,'legal':list(legal),'x':[candidate_features(o,t) for t in legal],'utility':utility,'forced':any(t//9==missing for t in o['observer_hand'])});return legal[max(range(len(legal)),key=lambda j:utility[j])]
  play(seedbase+i,policy=teacher,policy_seat=None)
  tmp=dest.with_suffix('.tmp');tmp.write_text(''.join(json.dumps(r)+'\n' for r in rows));os.replace(tmp,dest)
model=CandidateLinear();opt=torch.optim.Adam(model.parameters(),lr=.03);epoch0=0;best=float('inf')
binding=hashlib.sha256(json.dumps({'source':source,'config':config,'audit':auditsha,'shards':{str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for split in ['train','validation'] for p in sorted((out/split).glob('*.jsonl'))}},sort_keys=True).encode()).hexdigest()
def save(epoch,interrupted=False):
 s={'model':model.state_dict(),'optimizer':opt.state_dict(),'epoch':epoch,'best':best,'rng':torch.get_rng_state(),'python_rng':random.getstate(),'binding':binding,'source':source,'audit_sha256':auditsha,'config':config,'interrupted_epoch_restarts':interrupted,'model_version':'candidate-linear-teacher-v1','simulation_only':True};torch.save(s,out/'last.tmp');os.replace(out/'last.tmp',out/'last.pt');return s
if a.resume and (out/'last.pt').exists():
 s=torch.load(out/'last.pt',weights_only=False)
 if s['binding']!=binding:raise ValueError('Resume binding mismatch')
 model.load_state_dict(s['model']);opt.load_state_dict(s['optimizer']);epoch0=s['epoch']+1;best=s['best'];torch.set_rng_state(s['rng']);random.setstate(s['python_rng'])
def read(split):
 for path in sorted((out/split).glob('*.jsonl')):
  with open(path,encoding='utf-8') as f:
   for line in f:yield json.loads(line)
def evaluate(split):
 model.eval();sse=0;n=0;groups={};games={}
 with torch.no_grad():
  for r in read(split):
   scores=model(torch.tensor(r['x']).float())*64;y=torch.tensor(r['utility']).float();sse+=float((scores-y).square().sum());n+=len(y);target=int(y.argmax());raw=int(scores.argmax());rounded=int(scores.round().argmax());optimal=bool(y[raw]==y.max());key='missing_forced' if r['forced'] else 'free_discard'
   for label in ['all',key]:
    g=groups.setdefault(label,{'n':0,'raw_correct':0,'utility_optimal':0,'rounded_tie_correct':0});g['n']+=1;g['raw_correct']+=raw==target;g['utility_optimal']+=optimal;g['rounded_tie_correct']+=rounded==target
   if not r['forced']:
    g=games.setdefault(r['game_id'],[0,0]);g[0]+=raw==target;g[1]+=1
 for g in groups.values():
  for key in ['raw_correct','utility_optimal','rounded_tie_correct']:g[key+'_rate']=g[key]/g['n']
 rng=random.Random(42);vals=list(games.values());rates=[]
 if vals:
  for _ in range(500):
   sampled=rng.choices(vals,k=len(vals));rates.append(sum(g[0] for g in sampled)/sum(g[1] for g in sampled))
  rates.sort()
 return {'utility_mse':sse/n,'groups':groups,'free_raw_agreement_game_bootstrap_95ci':[rates[12],rates[487]] if rates else None}
for epoch in range(epoch0,a.epochs):
 model.train();xs=[];ys=[];losses=[]
 for r in read('train'):
  if stopped():save(epoch-1,True);raise SystemExit(75)
  xs.extend(r['x']);ys.extend(r['utility'])
  if len(xs)<256:continue
  x=torch.tensor(xs).float();y=torch.tensor(ys).float()/64;opt.zero_grad();loss=(model(x)-y).square().mean();loss.backward();opt.step();losses.append(float(loss.detach()));xs=[];ys=[]
 if xs:
  opt.zero_grad();loss=(model(torch.tensor(xs).float())-torch.tensor(ys).float()/64).square().mean();loss.backward();opt.step()
 val=evaluate('validation');improved=val['utility_mse']<best
 if improved:best=val['utility_mse']
 state=save(epoch)
 if improved:torch.save(state,out/'best.pt')
 with (out/'metrics.jsonl').open('a') as f:f.write(json.dumps({'epoch':epoch,'train_mse_scaled':sum(losses)/len(losses),'validation':val})+'\n')
s=torch.load(out/'best.pt',weights_only=False);model.load_state_dict(s['model']);report={'config':config,'binding':binding,'train':evaluate('train'),'validation':evaluate('validation'),'best_epoch':s['epoch'],'seconds':time.perf_counter()-start,'teacher':'deterministic own-hand 3*pairs+links','analytic_teacher_upper_bound':1.,'scope':'new_game_train_validation_teacher_state_distribution_only','limitations':['teacher distillation, not playing-strength improvement','analytic teacher utility explicitly supplied as supervised target','ties reported separately; no final test used']};(out/'result.json').write_text(json.dumps(report,indent=2));(root/'reports/round2_c_candidate.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

"""Bounded legal-observation imitation warm start, not a playing-strength claim."""
import argparse,hashlib,json,os,pathlib,random,sys
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
import torch
from simulator.policy_learning import PolicyValue
from simulator.selfplay import play
from observations.public import features
p=argparse.ArgumentParser();p.add_argument('--games',type=int,default=300);p.add_argument('--out',default='checkpoints/round2_warmstart');p.add_argument('--audit',default='reports/round2_d_policy_audit.json');a=p.parse_args()
if a.games<1:raise ValueError('games must be positive')
torch.set_num_threads(2);torch.manual_seed(42);random.seed(42)
out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
if (out/'TRAIN_COMPLETE.json').exists():raise RuntimeError('Completed imitation experiment immutable')
bound={str(q.relative_to(root)):hashlib.sha256(q.read_bytes()).hexdigest() for q in (root/'rules/core.py',root/'simulator/table.py',root/'simulator/selfplay.py',root/'observations/public.py')}
audit=json.load(open(a.audit));assert audit.get('passed') and audit['source_hashes']==bound
if audit.get('games',0)<1000:raise ValueError('1000 strict audit games required')
test_log=root/'reports/round2_d_policy_audit_tests.txt'
if hashlib.sha256(test_log.read_bytes()).hexdigest()!=audit.get('tests_sha256'):raise ValueError('Audit tests fingerprint mismatch')
ah=hashlib.sha256(pathlib.Path(a.audit).read_bytes()).hexdigest()
m=PolicyValue();opt=torch.optim.Adam(m.parameters(),lr=.0003);start=0
if (out/'imitation_last.pt').exists():
    s=torch.load(out/'imitation_last.pt',weights_only=False)
    assert s['source_hashes']==bound and s['audit_sha256']==ah
    m.load_state_dict(s['model']);opt.load_state_dict(s['optimizer']);torch.set_rng_state(s['rng']);random.setstate(s['python_rng']);start=s['imitation_games']
for index in range(start,a.games):
    stop=os.environ.get('MAHJONG_STOP_FILE')
    if stop and pathlib.Path(stop).exists():raise SystemExit(75)
    examples=[]
    def teacher(o,legal):
        def quality(t):
            h=list(o['observer_hand']);h.remove(t)
            return sum(h.count(x)>=2 for x in set(h))*3+sum(abs(x-y) in (1,2) and x//9==y//9 for i,x in enumerate(h) for y in h[i+1:])
        chosen=max(legal,key=quality);examples.append((features(o),tuple(legal),chosen,o['observer_player']));return chosen
    game=play(1400000+index,policy=teacher,policy_seat=None)
    if examples:
        x=torch.tensor([e[0] for e in examples]);logits,values=m(x);mask=torch.full_like(logits,float('-inf'))
        for i,e in enumerate(examples):mask[i,list(e[1])]=0
        labels=torch.tensor([e[2] for e in examples]);returns=torch.tensor([game['scores'][e[3]]/48 for e in examples])
        loss=torch.nn.functional.cross_entropy(logits+mask,labels)+.5*torch.nn.functional.mse_loss(values,returns)
        opt.zero_grad();loss.backward();torch.nn.utils.clip_grad_norm_(m.parameters(),1);opt.step()
        with (out/'imitation_metrics.jsonl').open('a') as f:f.write(json.dumps({'game':index,'examples':len(examples),'loss':float(loss.detach()),'scores':game['scores']})+'\n')
    s=dict(model=m.state_dict(),optimizer=opt.state_dict(),rng=torch.get_rng_state(),python_rng=random.getstate(),games=0,imitation_games=index+1,seed=1500000,selfplay=True,source_hashes=bound,audit_sha256=ah,version='legal-teacher-warmstart-v1',simulation_only=True)
    torch.save(s,out/'imitation.tmp');os.replace(out/'imitation.tmp',out/'imitation_last.pt')
torch.save(s,out/'last.tmp');os.replace(out/'last.tmp',out/'last.pt');(out/'TRAIN_COMPLETE.json').write_text(json.dumps({'teacher_games':a.games,'teacher':'own-hand shape heuristic','hidden_input':False,'scope':'imitation_then_separately_evaluated_selfplay','strength_improvement_claimed':False}))
print('Legal-observation imitation complete; independent evaluation required')

"""Audit counts/synthetic interface only. Fit CLI deliberately awaits admission."""
import pathlib,sys,json,argparse,torch,random,collections,hashlib
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.next_opponent import OpponentAblation,FAMILIES
from evaluation.next_opponent_control import shuffle_history
p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--output',required=True);p.add_argument('--smoke',action='store_true');a=p.parse_args();torch.set_num_threads(2);m=json.load(open(a.manifest));report={'scope':'real_label_counts_and_synthetic_interfaces_only_NO_training','families':{},'splits':{}}
for split,path in m['files'].items():
 s=collections.Counter();fit=set();evaluation=set()
 for line in open(path,encoding='utf-8'):
  r=json.loads(line);s['states']+=1;s['active_targets']+=sum(r['target_active']);s['structural_tenpai_positive']+=sum(t*v for t,v in zip(r['structural_tenpai'],r['target_active']));s['conditional_wait_elements']+=27*sum(r['structural_tenpai']);s['conditional_wait_positive']+=sum(sum(w) for w in r['structural_waits']);s['legal_candidates']+=sum(r['legal_mask']);s['risk_positive']+=sum(bool(j)*v for j,v in zip(r['joint_winner_mask'],r['legal_mask']));s['multiwinner_positive']+=sum((int(j).bit_count()>1)*v for j,v in zip(r['joint_winner_mask'],r['legal_mask']))
  (fit if int(hashlib.sha256(str(r['game_id']).encode()).hexdigest(),16)%2==0 else evaluation).add(r['game_id'])
 report['splits'][split]=dict(s,multiwinner_generalization='NA' if s['multiwinner_positive']==0 else 'positive_count_only_NOT_validated',calibration_game_fit_count=len(fit),calibration_game_eval_count=len(evaluation))
if a.smoke:
 torch.manual_seed(42);state=torch.randn(2,191);tokens=torch.tensor([[[1,0,0],[2,1,4],[3,2,6]],[[1,0,0],[2,1,4],[3,2,6]]]);mask=torch.ones(2,3,dtype=torch.bool);shuffled=shuffle_history(tokens,mask,['fixtureA','fixtureB']);assert torch.equal(shuffled,shuffle_history(tokens,mask,['fixtureA','fixtureB']));assert sorted(tokens[0].tolist())==sorted(shuffled[0].tolist())
 for family in FAMILIES:
  model=OpponentAblation(family);o=model(state,shuffled if family=='history_shuffled' else tokens,mask);loss=sum(v.square().mean() for v in o.values());loss.backward();assert all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters());report['families'][family]={'parameters':sum(p.numel() for p in model.parameters()),'finite_interface_backward':True}
report['input_contract']={'always':'own/public counts,declared missing,active,public meld counts,observer seat','progress':'public wall and turn plus wall-known flag','history':'progress + entire supplied public event sequence; no last11 summary inputs','exchange':'history + own historical sent/received/direction/source; not current opponent holdings','history_shuffled':'same full event multiset, player/tile/action stay together; order shuffled deterministically per sample','calibration':'validation whole-game hash split only, no train calibration or final tuning','labels':'conditional structural waits NOT public-effective; joint risk evaluated only legal candidate mask'};pathlib.Path(a.output).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

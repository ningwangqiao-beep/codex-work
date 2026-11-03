"""Holdout audit only; never selects/calibrates model weights."""
import sys,json,hashlib,copy,argparse
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from inference.v3_observation import encode_observation

def audit(path):
 m=json.loads(Path(path).read_text());out=Path(path).resolve().parent;sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();n=m['games'];first=7120000 if n==200 else 7120900
 assert n in (2,200) and m['seed_range']==[first,first+n-1] and all(m[x] for x in ('no_training','no_calibration','no_selection'));assert len(m['source_hashes'])==16
 for p,h in m['source_hashes'].items():assert sha(root/p)==h
 for p,h in m['candidate_checkpoint_hashes'].items():assert sha(p)==h
 if n==200:assert m['candidate_checkpoint_hashes']
 seen=set();records=positive=risk=multi=0
 commits={c['seed']:c for c in m['commits']};assert len(commits)==n
 for filename in m['shards']['holdout']:
  p=Path(filename).resolve();c=json.loads((p.parent/'commit.json').read_text());seed=c['seed'];assert first<=seed<first+n and seed not in seen;seen.add(seed);assert p.parent.name==str(seed) and p.parent.parent.name=='holdout' and p.parent.parent.parent==out;assert c==commits[seed] and c['seat']==(seed-first)%4 and c['split']=='holdout';assert sha(p)==c['records_sha256'] and sha(p.parent/'game.json')==c['game_sha256'];g=json.loads((p.parent/'game.json').read_text());assert g['seed']==seed;balance=[0]*4
  for e in g['ledger']:balance[e['payer']]-=e['amount'];balance[e['receiver']]+=e['amount']
  assert balance==g['scores'] and sum(balance)==0
  count=0
  for line in p.open():
   r=json.loads(line);o=r['observation'];assert r['seed']==seed and o['observer_player']==c['seat'] and r['state_target']==g['scores'][c['seat']];a=encode_observation(o);assert a['state_features']==r['state_features'] and a['history_tokens']==r['history_tokens'] and not r['history_truncated'];poison=copy.deepcopy(o);poison.update(opponent_hands=[[26]*13]*3,future_wall=[0]*56);assert a==encode_observation(poison)
   records+=1;count+=1;positive+=sum(r['structural_tenpai'])
   for label,legal in zip(r['joint_winner_mask'],r['legal_mask']):
    if legal:risk+=bool(label);multi+=int(label.bit_count()>1)
  assert count==c['rows']
 assert len(seen)==n and records==m['records'];return dict(passed=True,games=n,records=records,seed_range=m['seed_range'],structural_tenpai_positive=positive,legal_risk_positive=risk,legal_multiwinner_positive=multi,manifest_sha256=sha(path),no_training=True,no_calibration=True,no_selection=True,limitations=['correlated within-game labels','frozen producer record source_group legacy; manifest owns holdout role'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--out',default='reports/next_d_holdout_audit.json');a=p.parse_args();r=audit(a.manifest);Path(a.out).write_text(json.dumps(r,indent=2));print(r)

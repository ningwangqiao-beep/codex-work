"""Independent streaming audit of committed scaled teacher shards."""
import sys,json,hashlib,copy,math,argparse,time
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from inference.v3_observation import encode_observation
from rules.core import legal_discards

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 return h.hexdigest()
def audit(path):
 start=time.perf_counter();manifest_path=Path(path).resolve();dataset_root=manifest_path.parent;m=json.loads(manifest_path.read_text());assert m['producer_sha256']==sha(root/'scripts/next_data_scale.py')
 for rel,digest in m['source_hashes'].items():assert sha(root/rel)==digest,rel
 old={}
 for split in ('train','validation'):
  for line in (root/'datasets/next_history100'/(split+'.jsonl')).open():
   r=json.loads(line);old.setdefault(r['seed'],[]).append(r)
 commits={c['seed']:c for c in m['commits']};assert len(commits)==len(m['commits']);seen=set();prefix=records=games=0;counts={};max_history=0
 for split in ('train','validation'):
  expected=set(range(7000000,7000000+m['train_games'])) if split=='train' else set(range(7100000,7100000+m['validation_games']));actual=set();count=0
  for filename in m['shards'][split]:
   p=Path(filename).resolve();assert p.name=='records.jsonl' and p.parent.parent.name==split and p.parent.parent.parent==dataset_root,'Shard directory/split mismatch';c=json.loads((p.parent/'commit.json').read_text());seed=c['seed'];assert p.parent.name==str(seed),'Shard directory/seed mismatch';assert type(c['seat'])==int and c['seat']==(seed-(7000000 if split=='train' else 7100000))%4,'Commit seat/task mismatch';assert seed not in seen and seed in expected;seen.add(seed);actual.add(seed);assert c==commits[seed] and c['split']==split and c['source_hashes']==m['source_hashes'];assert sha(p)==c['records_sha256'];assert sha(p.parent/'game.json')==c['game_sha256'];g=json.loads((p.parent/'game.json').read_text());assert g['seed']==seed;assert g.get('rule_version')==m['rule_version'];assert c['split']==split and c['seed']==commits[seed]['seed'] and c['seat']==commits[seed]['seat']
   balances=[0]*4
   for e in g['ledger']:assert e['amount']>=0;balances[e['payer']]-=e['amount'];balances[e['receiver']]+=e['amount']
   assert balances==g['scores'] and sum(balances)==0
   rows=[]
   for line in p.open():
    r=json.loads(line);assert r['seed']==seed and r['game_id']==f'v3-{seed}' and r['deal_group_id']==f'deal-{seed}';o=r['observation'];seat=o['observer_player'];assert seat==c['seat'];assert r['state_target']==g['scores'][seat]
    a=encode_observation(o);assert a['state_features']==r['state_features'] and a['history_tokens']==r['history_tokens'];assert not r['history_truncated'] and len(r['history_tokens'])==r['history_original_length'];max_history=max(max_history,len(r['history_tokens']))
    poison=copy.deepcopy(o);poison.update(opponent_hands=[[26]*13]*3,future_wall=[0]*56,future_result=999);assert a==encode_observation(poison)
    assert len(r['candidate_features'])==27 and all(len(x)==12 for x in r['candidate_features']);assert all(math.isfinite(x) for x in r['state_features']);legal=set(legal_discards(o['observer_hand'],o['declared_missing_suits'][seat]));assert {i for i,x in enumerate(r['legal_mask']) if x}==legal
    assert all(math.isfinite(x) for row in r['candidate_features'] for x in row);assert all(math.isfinite(x) and 0<=x<=1 for x in r['action_targets']);assert all(r['structural_tenpai'][i]==int(any(r['structural_waits'][i])) for i in range(3));rows.append(r);records+=1;count+=1
   assert len(rows)==c['rows']
   if seed in old:assert rows==old[seed];prefix+=1
   games+=1
  assert actual==expected;assert count==m['counts'][split];counts[split]=count
 assert games==m['train_games']+m['validation_games'];assert prefix==min(100,m['train_games'])+m['validation_games']
 if m['train_games']==1000:
  assert m['dataset_version']=='next-history1000' and games==1020 and prefix==120 and m['validation_games']==20,'Formal 1000+fixed20/prefix120 requirement'
 for rel,digest in m['source_hashes'].items():assert sha(root/rel)==digest
 indirect={rel:sha(root/rel) for rel in ('observations/v3_public.py','inference/v3_legacy.py','rules/hand_analysis.py','rules/hand_analysis_reference.py') if (root/rel).exists()}
 return dict(indirect_sources_current_hashes=indirect,indirect_sources_bound_during_generation=False,game_split_semantics='game.json contains no split; commit/manifest/directory plus expected permanent seed define it',passed=True,manifest_sha256=sha(path),games=games,records=records,counts=counts,prefix_games_identical=prefix,history_max=max_history,source_hashes=m['source_hashes'],seconds=time.perf_counter()-start,checks=['atomic commit and manifest agree','actual content SHA','unique permanent seed ranges and whole-deal split','all ledger score zero-sum','all observer terminal returns','all recorded inputs reencoded','hidden/future poison keys ignored','candidate legal masks and finite values','frozen100+fixedval exact records'],limitations=['poison-key noninterference alone not upstream full leakage proof','teacher preferences NOT counterfactual Q','no physical hidden states persisted for independent 108 recheck','producer binds only its ten explicit source files; indirect source hashes here are current observations not historical proof','generator has no interprocess output lock; independent audit does not certify concurrency safety'],admission='chief decision required')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--out',default='reports/next_d_scale_audit.json');a=p.parse_args()
 try:r=audit(a.manifest)
 except Exception as e:
  Path(a.out).write_text(json.dumps(dict(passed=False,error=repr(e)),indent=2));raise
 Path(a.out).write_text(json.dumps(r,indent=2));print({k:v for k,v in r.items() if k!='source_hashes'})

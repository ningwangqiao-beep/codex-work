"""Independent auxiliary validation; never training or calibration admission."""
import sys,json,hashlib,os,argparse,concurrent.futures,time
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root));sys.path.insert(0,str(root/'scripts'))
import next_data_scale as producer
EXTRA=('scripts/next_data_scale.py','scripts/next_data_holdout200.py','observations/v3_public.py','inference/v3_legacy.py','rules/hand_analysis.py','rules/hand_analysis_reference.py')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def full_hashes():return {**producer.hashes(),**{p:sha(root/p) for p in EXTRA}}
def run(a):
 if a.games not in (2,200):raise ValueError('Only 2-game smoke or approved 200-game frozen-candidate holdout')
 sources=full_hashes();base=producer.hashes();start_seed=7120000 if a.games==200 else 7120900;candidate={str(Path(p).resolve()):sha(p) for p in a.checkpoint};out=root/a.out;out.mkdir(parents=True,exist_ok=True);meta=dict(version='next-opponent-holdout200-v1' if a.games==200 else 'next-opponent-holdout-smoke2-v1',games=a.games,seed_range=[start_seed,start_seed+a.games-1],source_hashes=sources,no_training=True,no_calibration=True,no_selection=True,candidate_checkpoint_hashes=candidate,role='frozen_candidate_independent_holdout_NOT_development_aux',workers=2,min_free_mb=1536)
 if a.games==200:
  approval=json.loads(Path(a.approval).read_text()) if a.approval else {}
  if approval.get('approved') is not True or approval.get('source_hashes')!=sources or approval.get('games')!=200 or not candidate or approval.get('candidate_checkpoint_hashes')!=candidate or approval.get('candidates_frozen') is not True:raise ValueError('Chief frozen-candidate approval required for holdout200')
 runpath=out/'RUN.json'
 if runpath.exists():
  if not a.resume or json.loads(runpath.read_text())!=meta:raise ValueError('Resume source/config mismatch')
 else:runpath.write_text(json.dumps(meta,indent=2))
 tasks=[];commits=[]
 for i in range(a.games):
  seed=start_seed+i;dest=out/'holdout'/str(seed);cp=dest/'commit.json'
  if cp.exists():
   c=json.loads(cp.read_text());assert c['seed']==seed and c['seat']==i%4 and c['split']=='holdout' and c['source_hashes']==base
   assert sha(dest/'records.jsonl')==c['records_sha256'] and sha(dest/'game.json')==c['game_sha256'];commits.append(c)
  else:tasks.append((seed,i%4,'holdout',str(out),base))
 start=time.perf_counter()
 with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
  flying={}
  while tasks or flying:
   stop=os.environ.get('MAHJONG_STOP_FILE')
   if (stop and Path(stop).exists()) or producer.available_ram()<1536*1024**2:
    for f in flying:commits.append(f.result())
    raise SystemExit(75)
   assert full_hashes()==sources,'Source changed during run'
   while tasks and len(flying)<2:
    task=tasks.pop(0);flying[pool.submit(producer.work,task)]=task
   finished,_=concurrent.futures.wait(flying,return_when=concurrent.futures.FIRST_COMPLETED)
   for f in finished:commits.append(f.result());del flying[f]
 assert full_hashes()==sources
 assert all(sha(path)==digest for path,digest in candidate.items()),'Frozen candidate changed'
 counts=positive=risk_positive=0;shards=[]
 for c in sorted(commits,key=lambda x:x['seed']):
  dest=out/'holdout'/str(c['seed']);game=json.loads((dest/'game.json').read_text());assert game['seed']==c['seed'];balance=[0]*4
  for e in game['ledger']:balance[e['payer']]-=e['amount'];balance[e['receiver']]+=e['amount']
  assert balance==game['scores'] and sum(balance)==0;path=dest/'records.jsonl';shards.append(str(path))
  for line in path.open():
   r=json.loads(line);assert r['seed']==c['seed'] and r['observation']['observer_player']==c['seat'];assert r['state_target']==game['scores'][c['seat']];counts+=1;positive+=sum(r['structural_tenpai']);risk_positive+=sum(bool(mask) and legal for mask,legal in zip(r['joint_winner_mask'],r['legal_mask']))
 manifest={**meta,'rule_version':'SICHUAN-XUEZHAN-4FAN-V3','history_schema_version':'v3-history-v2-public-events','schema_version':'v3-public191-fullseq-v2','target_semantics':'lexicographic_preference_rank_NOT_Q','state_target_units':'raw V3 terminal net score','state_target_policy':'one rotating BaselineV3 seat vs three frozen simulator heuristic styles','record_source_group_legacy':'next-history100 retained by frozen producer; manifest defines independent auxiliary role','commits':commits,'shards':{'holdout':shards},'records':counts,'structural_tenpai_positive':positive,'legal_candidate_risk_positive':risk_positive,'seconds':time.perf_counter()-start,'audit_status':'LOCAL_LEDGER_SCHEMA_CHECK_PENDING_CHIEF'}
 temp=out/'manifest.tmp';temp.write_text(json.dumps(manifest,indent=2));os.replace(temp,out/'manifest.json');print({k:v for k,v in manifest.items() if k not in ('source_hashes','commits','shards')})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--games',type=int,default=2);p.add_argument('--out',default='datasets/next_opponent_holdout_smoke2');p.add_argument('--resume',action='store_true');p.add_argument('--approval');p.add_argument('--checkpoint',action='append',default=[]);run(p.parse_args())

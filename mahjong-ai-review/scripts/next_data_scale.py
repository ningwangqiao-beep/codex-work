"""Atomic per-game history scaling. Chief approval required above smoke scale."""
import sys,json,hashlib,os,time,argparse,concurrent.futures,ctypes
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from simulator.v3_history_v2 import play
from baselines.v3_bot import BaselineV3
from models.revision_candidate_schema import adapt,FEATURE_NAMES
from inference.v3_observation import encode_observation
SOURCES=('rules/core.py','rules/v3.py','simulator/table.py','simulator/v3_history_v2.py','observations/v3_history_v2.py','observations/public.py','baselines/v3_bot.py','rules/fast_hand_analysis.py','models/revision_candidate_schema.py','inference/v3_observation.py')
def hashes():return {p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in SOURCES}
def available_ram():
 class Status(ctypes.Structure):_fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(n,ctypes.c_ulonglong) for n in ('total','available','page_total','page_available','virtual_total','virtual_available','extended')]
 s=Status();s.length=ctypes.sizeof(s);ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s));return s.available

def work(task):
 seed,seat,split,out,source=task
 if hashes()!=source:raise ValueError('Worker source changed')
 bot=BaselineV3();records={}
 def policy(o,legal):
  chosen=bot(o,legal);r=adapt(o,bot.last_analysis,f'v3-{seed}',seed,'next-history100');r.update(encode_observation(o));r.update(deal_group_id=f'deal-{seed}',observation=o,state_target_missing=False);records[o['turn_index']]=r;return chosen
 game=play(seed,collect=True,policy=policy,policy_seat=seat,exchange_offset=seed%3+1);labels={(r['observer_player'],r['observation']['turn_index']):r for r in game['rows']}
 rows=[]
 for turn,r in records.items():
  label=labels[(seat,turn)];r['state_target']=game['scores'][seat];r.update(structural_tenpai=label['tenpai'],structural_waits=label['waits'],joint_winner_mask=label['joint_outcome'],target_active=label['target_active']);rows.append(r)
 destination=Path(out)/split/str(seed);temp=destination.with_name(str(seed)+'.tmp');temp.mkdir(parents=True,exist_ok=True)
 (temp/'records.jsonl').write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in rows),encoding='utf-8');(temp/'game.json').write_text(json.dumps({k:v for k,v in game.items() if k!='rows'}),encoding='utf-8')
 audit=dict(seed=seed,seat=seat,split=split,source_hashes=source,rows=len(rows),records_sha256=hashlib.sha256((temp/'records.jsonl').read_bytes()).hexdigest(),game_sha256=hashlib.sha256((temp/'game.json').read_bytes()).hexdigest());(temp/'commit.json').write_text(json.dumps(audit));assert hashes()==source;os.replace(temp,destination);return audit

def run(a):
 if not 1<=a.train_games<=1000 or not 0<=a.validation_games<=20:raise ValueError('Only bounded 1000 train/20 fixed validation supported')
 source=hashes();out=root/a.out;out.mkdir(parents=True,exist_ok=True);meta=dict(train_games=a.train_games,validation_games=a.validation_games,source_hashes=source,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),workers=2)
 if a.train_games>10:
  approval=json.loads(Path(a.approval).read_text()) if a.approval else {}
  if not approval.get('approved') or approval.get('source_hashes')!=source or approval.get('train_games')!=a.train_games:raise ValueError('Chief scale approval required')
 meta_path=out/'RUN.json'
 if meta_path.exists():
  if not a.resume or json.loads(meta_path.read_text())!=meta:raise ValueError('Resume metadata mismatch')
 else:meta_path.write_text(json.dumps(meta,indent=2))
 tasks=[(7000000+i,i%4,'train',str(out),source) for i in range(a.train_games)]+[(7100000+i,i%4,'validation',str(out),source) for i in range(a.validation_games)]
 pending=[];done=[]
 for task in tasks:
  dest=out/task[2]/str(task[0]);commit=dest/'commit.json'
  if commit.exists():
   c=json.loads(commit.read_text());assert c['source_hashes']==source
   for name in ('records','game'):assert hashlib.sha256((dest/(name+('.jsonl' if name=='records' else '.json'))).read_bytes()).hexdigest()==c[name+'_sha256']
   done.append(c)
  else:pending.append(task)
 start=time.perf_counter()
 with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
  inflight={}
  while pending or inflight:
   stop=os.environ.get('MAHJONG_STOP_FILE')
   if (stop and Path(stop).exists()) or available_ram()<a.min_free_mb*1024**2:
    pending.clear()
    for f in inflight:done.append(f.result())
    raise SystemExit(75)
   while pending and len(inflight)<2:
    task=pending.pop(0);inflight[pool.submit(work,task)]=task
   completed,_=concurrent.futures.wait(inflight,return_when=concurrent.futures.FIRST_COMPLETED)
   for f in completed:done.append(f.result());del inflight[f]
 assert hashes()==source
 # Compare complete prefix/validation records against frozen 100-stage labels and inputs.
 prefix={}
 for split in ('train','validation'):
  for line in (root/'datasets/next_history100'/(split+'.jsonl')).open():
   r=json.loads(line);prefix.setdefault(r['seed'],[]).append(r)
 comparisons=0
 for c in done:
  if c['seed'] in prefix:
   got=[json.loads(line) for line in (out/c['split']/str(c['seed'])/'records.jsonl').open()];assert got==prefix[c['seed']];comparisons+=1
 manifest=dict(dataset_version='next-history1000' if a.train_games==1000 else 'next-history-scale-smoke-v2',rule_version='SICHUAN-XUEZHAN-4FAN-V3',history_schema_version='v3-history-v2-public-events',schema_version='v3-public191-fullseq-v2',target_semantics='lexicographic_preference_rank_NOT_Q',state_target_units='raw V3 terminal net score',state_target_policy='one rotating BaselineV3 seat vs three frozen simulator heuristic styles',state_target_definition='teacher_policy_final_net_score_for_observer',state_target_scale=1.0,producer_sha256=meta['script_sha256'],train_seed_range=[7000000,7000000+a.train_games-1],validation_seed_range=[7100000,7100000+a.validation_games-1] if a.validation_games else [],train_games=a.train_games,validation_games=a.validation_games,source_hashes=source,shards={s:[str(out/s/str(c['seed'])/'records.jsonl') for c in sorted(done,key=lambda x:x['seed']) if c['split']==s] for s in ('train','validation')},commits=done,prefix_games_exactly_matched=comparisons,counts={s:sum(c['rows'] for c in done if c['split']==s) for s in ('train','validation')},candidate_feature_names=FEATURE_NAMES,state_dim=191,seconds=time.perf_counter()-start,audit_status='PENDING_CHIEF_ADMISSION')
 temp=out/'manifest.tmp';temp.write_text(json.dumps(manifest,indent=2));os.replace(temp,out/'manifest.json');print({k:v for k,v in manifest.items() if k not in ('commits','shards','source_hashes')})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--train-games',type=int,default=4);p.add_argument('--validation-games',type=int,default=2);p.add_argument('--out',default='datasets/next_history_scale_smoke');p.add_argument('--resume',action='store_true');p.add_argument('--approval');p.add_argument('--min-free-mb',type=int,default=1024);run(p.parse_args())

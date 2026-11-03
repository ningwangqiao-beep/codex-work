"""Streaming per-game shard audit; no expansion/training authorization implied."""
import pathlib,json,hashlib,math
from collections import Counter
from training.v3_gate import sha
from inference.v3_observation import encode_observation
from rules.core import legal_discards

def canonical(r):return hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def inspect_scale(manifest,root):
 root=pathlib.Path(root);m=json.load(open(manifest));reference=json.load(open(root/'datasets/next_history100/manifest.json'));prefix={}
 for split,path in reference['files'].items():
  for line in open(path,encoding='utf-8'):
   r=json.loads(line);prefix[(r['seed'],r['observation']['turn_index'])]=canonical(r)
 norm=lambda d:{k.replace('\\','/'):v for k,v in d.items()}
 if norm(m['source_hashes'])!=norm(reference['source_hashes']):raise ValueError('Scaled data changed Calculator/rules/history/encoder')
 for rel,digest in m['source_hashes'].items():
  if sha(root/rel)!=digest:raise ValueError('Source drift '+rel)
 commits={(c['split'],c['seed']):c for c in m['commits']};seen={};counts={};matches=0;history_max=0;returns=0;shard_hashes={}
 if len(commits)!=len(m['commits']):raise ValueError('Duplicate committed game')
 for split in ('train','validation'):
  count=0;games=0
  for path in m['shards'][split]:
   p=pathlib.Path(path);seed=int(p.parent.name);commit=commits[(split,seed)];gamepath=p.parent/'game.json';game=json.load(open(gamepath));games+=1
   if norm(commit['source_hashes'])!=norm(m['source_hashes']) or sha(p)!=commit['records_sha256'] or sha(gamepath)!=commit['game_sha256']:raise ValueError('Invalid committed shard binding')
   if (split=='train' and not 7000000<=seed<7001000) or (split=='validation' and not 7100000<=seed<7100020):raise ValueError('Permanent seed partition violated')
   scores=[0]*4
   for e in game['ledger']:scores[e['payer']]-=e['amount'];scores[e['receiver']]+=e['amount']
   if scores!=game['scores'] or sum(scores)!=0 or game['seed']!=seed:raise ValueError('Terminal ledger mismatch')
   shard_hashes[str(p)]=sha(p);n=0
   for line in open(p,encoding='utf-8'):
    r=json.loads(line);obs=r['observation'];key=(r['seed'],obs['turn_index']);encoded=encode_observation(obs)
    if r['seed']!=seed or r['rule_version']!='SICHUAN-XUEZHAN-4FAN-V3' or r['state_features']!=encoded['state_features'] or r['history_tokens']!=encoded['history_tokens'] or r['history_truncated'] or r['history_original_length']!=len(r['history_tokens']):raise ValueError('Causal encoder/history mismatch')
    for group in (str(r['game_id']),str(r['deal_group_id']),str(seed)):
     if group in seen and seen[group]!=split:raise ValueError('Game/deal split leakage')
     seen[group]=split
    if obs['observer_player']!=commit['seat'] or r['state_target']!=scores[commit['seat']]:raise ValueError('Terminal policy-V target mismatch')
    if any(e.get('event_index')!=i for i,e in enumerate(obs['public_action_history'])):raise ValueError('History event index discontinuity')
    legal=legal_discards(obs['observer_hand'],obs['declared_missing_suits'][obs['observer_player']])
    if [i for i,v in enumerate(r['legal_mask']) if v]!=legal or len(r['candidate_features'])!=27 or len(r['action_targets'])!=27:raise ValueError('Legal/candidate mismatch')
    if any(len(c)!=len(m['candidate_feature_names']) or any(not math.isfinite(v) for v in c) for c in r['candidate_features']):raise ValueError('Invalid candidate features')
    physical=Counter(obs['observer_hand']+[t for _,t in obs['visible_discards']]+[t for ms in obs['public_melds'] for meld in ms for t in meld if t>=0]+obs.get('public_winning_tiles',[]))
    if any(n>4 for n in physical.values()):raise ValueError('Known fifth copy')
    if key in prefix:
     if canonical(r)!=prefix[key]:raise ValueError('100-prefix/fixed validation record changed')
     matches+=1
    history_max=max(history_max,len(r['history_tokens']));n+=1
   if n!=commit['rows']:raise ValueError('Commit row mismatch')
   count+=n;returns+=1
  if games!=m[split+'_games']:raise ValueError('Committed game total mismatch')
  counts[split]=count
 return {'inspection_passed':True,'manifest_sha256':sha(manifest),'counts':counts,'terminal_game_ledgers_checked':returns,'canonical_prefix_records_matched':matches,'history_max':history_max,'dataset_fingerprint':hashlib.sha256(json.dumps(shard_hashes,sort_keys=True).encode()).hexdigest(),'training_allowed':False,'rl_allowed':False,'limitations':['smoke can use fewer than fixed20validation games; formal1000 gate will require all20','fixed6epochs with more records means more optimizersteps, not data-only causal comparison']}

def validate_scale_manifest(path,root,admission_path):
 root=pathlib.Path(root);data=inspect_scale(path,root);m=json.load(open(path));a=json.load(open(admission_path))
 if m.get('dataset_version')!='next-history1000' or m.get('train_games')!=1000 or m.get('validation_games')!=20 or data['canonical_prefix_records_matched']!=1459:raise ValueError('Formal1000 requires exact original100prefix and full fixed20validation')
 if m.get('target_semantics')!='lexicographic_preference_rank_NOT_Q' or not m.get('state_target_policy') or m.get('state_target_scale')!=1.0:raise ValueError('Explicit teacher preference and raw policy-V semantics required')
 if a.get('stage')!='NEXT_HISTORY1000_RELATIVE_PAIRWISE' or a.get('manifest_sha256')!=sha(path) or a.get('dataset_fingerprint')!=data['dataset_fingerprint']:raise ValueError('Chief1000 data admission mismatch')
 for flag in ('passed','supervised_training_allowed','prefix_100_exact_audited','fixed_validation_exact_audited','terminal_return_ledger_audited','history_data_isolation_audited'):
  if a.get(flag) is not True:raise ValueError('Missing1000 admission '+flag)
 if a.get('rl_training_allowed') is not False or a.get('max_epochs')!=6 or a.get('max_batch_size')!=128:raise ValueError('Only6epoch/batch128 supervised admitted')
 if a.get('source_hashes')!=m['source_hashes']:raise ValueError('Chief1000 source mismatch')
 spec=a['prior_100_relative_admission'];p=pathlib.Path(spec['path']);p=p if p.is_absolute() else root/p
 if sha(p)!=spec['sha256']:raise ValueError('Previous relative admission changed')
 prior=json.load(open(p))
 if not prior.get('passed') or not prior.get('relative_combo_allowed'):raise ValueError('Missing prior100 relative evidence')
 data.update(training_allowed=True,admission_sha256=sha(admission_path),scope='1000games fixed6epochs more_optimizersteps_NOT_data_only_causal');return data

"""V3 T2 admission for actual teacher100 manifest. No training/RL in this gate."""
import pathlib,json,hashlib,math
from collections import Counter
from inference.v3_observation import encode_observation
from rules.core import legal_discards
VERSION='SICHUAN-XUEZHAN-4FAN-V3'
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
def bound_evidence(spec,root):
 p=pathlib.Path(spec['path']);p=p if p.is_absolute() else root/p
 if sha(p)!=spec['sha256']:raise ValueError('Evidence hash mismatch: '+str(p))
 return json.load(open(p))
def inspect_v3_data(path,root):
 root=pathlib.Path(root);m=json.load(open(path))
 for k in ('files','source_hashes','data_hashes','candidate_feature_names','state_dim','target_semantics','state_target_units','state_target_policy'):
  if k not in m:raise ValueError('Missing V3 dataset '+k)
 if m['target_semantics']!='lexicographic_preference_rank_NOT_Q' or m['state_dim']!=191 or m.get('final_test_used') is not False:raise ValueError('V3 T2 target/split contract mismatch')
 for rel,digest in m['source_hashes'].items():
  if sha(root/rel)!=digest:raise ValueError('Source changed: '+rel)
 for split in ('train','validation'):
  if sha(m['files'][split])!=m['data_hashes'][split]:raise ValueError('Data changed: '+split)
 registries=[{}, {}, {}];counts={};history_max=0;known_sum_failures=0
 for split in ('train','validation'):
  count=0
  with open(m['files'][split],encoding='utf-8') as f:
   for line in f:
    r=json.loads(line)
    for k in ('game_id','seed','deal_group_id','rule_version','state_features','candidate_features','legal_mask','history_tokens','history_original_length','history_truncated','action_targets','observation','state_target','structural_tenpai','structural_waits','joint_winner_mask','target_active'):
     if k not in r:raise ValueError('Missing record '+k)
    if r['rule_version']!=VERSION or r.get('schema_version')!='v3-public191-fullseq-v2' or r['history_truncated'] is not False or r['history_original_length']!=len(r['history_tokens']):raise ValueError('Wrong rules or truncated history')
    for value,reg in zip((r['game_id'],r['seed'],r['deal_group_id']),registries):
     key=str(value)
     if key in reg and reg[key]!=split:raise ValueError('V3 game/seed/deal family leakage')
     reg[key]=split
    obs=r['observation'];forbidden={'hands','hidden_hands','future_wall','wall','wall_order','opponent_hands','final_scores'}
    if forbidden & set(obs):raise ValueError('Forbidden hidden/future observation key')
    encoded=encode_observation(obs)
    if encoded['state_features']!=r['state_features'] or encoded['history_tokens']!=r['history_tokens']:raise ValueError('Stored features do not equal causal observation encoder')
    physical=Counter(obs['observer_hand']+[t for _,t in obs['visible_discards']]+[t for ms in obs['public_melds'] for meld in ms for t in meld if t>=0]+obs.get('public_winning_tiles',[]))
    if any(n>4 for n in physical.values()):raise ValueError('Known physical fifth tile')
    expected=legal_discards(obs['observer_hand'],obs['declared_missing_suits'][obs['observer_player']])
    if [i for i,v in enumerate(r['legal_mask']) if v]!=expected:raise ValueError('Legal candidate mask differs from rules')
    if len(r['structural_tenpai'])!=3 or len(r['target_active'])!=3 or len(r['structural_waits'])!=3 or any(len(w)!=27 for w in r['structural_waits']) or len(r['joint_winner_mask'])!=27:raise ValueError('Bad auxiliary shapes')
    if any(v not in (0,1) for v in r['structural_tenpai']+r['target_active']+sum(r['structural_waits'],[])) or any(type(v)!=int or v not in range(8) for v in r['joint_winner_mask']):raise ValueError('Bad auxiliary labels')
    if any(bool(t)!=bool(any(w)) for t,w in zip(r['structural_tenpai'],r['structural_waits'])):raise ValueError('Tenpai/wait label mismatch')
    if len(r['state_features'])!=191 or len(r['candidate_features'])!=27 or len(r['legal_mask'])!=27 or len(r['action_targets'])!=27:raise ValueError('Bad V3 shapes')
    if any(type(v) not in (bool,int) or v not in (0,1) for v in r['legal_mask']) or not any(r['legal_mask']):raise ValueError('Bad legal mask')
    if not math.isfinite(r['state_target']) or any(not math.isfinite(v) for v in r['state_features']):raise ValueError('Bad numeric state/return')
    for i,c in enumerate(r['candidate_features']):
     if len(c)!=len(m['candidate_feature_names']) or any(not math.isfinite(v) for v in c):raise ValueError('Bad candidate features')
     if r['legal_mask'][i] and not math.isfinite(r['action_targets'][i]):raise ValueError('Bad preference labels')
    for token in r['history_tokens']:
     if len(token)!=3 or any(type(x)!=int for x in token) or not 0<=token[0]<16 or not 0<=token[1]<5 or not 0<=token[2]<28:raise ValueError('Bad history tokens')
    history_max=max(history_max,len(r['history_tokens']));count+=1
  if not count:raise ValueError('Empty V3 '+split)
  counts[split]=count
 return {'data_checks_passed':True,'manifest_sha256':sha(path),'counts':counts,'history_max':history_max,'rule_version':VERSION,'training_allowed':False,'rl_allowed':False},m

def validate_v3_manifest(path,root,admission_path=None):
 root=pathlib.Path(root);data,m=inspect_v3_data(path,root)
 if admission_path is None:raise ValueError('V3 chief supervised admission required')
 admission=json.load(open(admission_path))
 if admission.get('rule_version')!=VERSION or admission.get('stage')!='T2_SUPERVISED_ONLY' or admission.get('manifest_sha256')!=sha(path):raise ValueError('Admission rules/stage/data mismatch')
 for flag in ('passed','baseline_development_audited','dataset_isolation_audited','state_target_definition_audited','history_complete_audited','candidate_legal_audited','seed_family_split_audited','supervised_training_allowed'):
  if admission.get(flag) is not True:raise ValueError('V3 admission blocked: '+flag)
 if admission.get('rl_training_allowed') is not False:raise ValueError('T2 cannot authorize RL')
 ready=bound_evidence(admission['rules_ready'],root)
 if not ready.get('passed'):raise ValueError('Rules ready not passed')
 for key,minimum in [('strict1000',1000),('performance10000',10000)]:
  evidence=bound_evidence(admission[key],root)
  if evidence.get('games',0)<minimum or evidence.get('unchanged') is not True:raise ValueError('Missing audited '+key)
  for rel,digest in evidence['source_hashes'].items():
   if m['source_hashes'].get(rel)!=digest:raise ValueError('Batch source differs from training data')
 for rel,digest in ready['source_hashes'].items():
  if m['source_hashes'].get(rel)!=digest:raise ValueError('Ready source differs from data')
 data.update(training_allowed=True,admission_sha256=sha(admission_path),scope='T2_supervised_only_not_counterfactual_Q_not_RL');return data

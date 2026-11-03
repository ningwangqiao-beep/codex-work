"""Read-only audit of persisted fresh200 predictions; no model inference or fitting."""
import sys,json,hashlib,math,random
from pathlib import Path
from collections import defaultdict
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads((root/'reports/next_c_opponent_fresh200_eval.json').read_text());manifest=root/'datasets/next_opponent_holdout200/manifest.json';m=json.loads(manifest.read_text());assert sha(manifest)==r['holdout_manifest_sha256']
for p,h in r['candidate_hashes'].items():assert sha(p)==h
for p,h in r['source_hashes'].items():assert sha(root/p)==h
pred=root/r['sample_predictions']['path'];assert sha(pred)==r['sample_predictions']['sha256'];expected={};secondary={};allgames=set();original=0
for file in m['shards']['holdout']:
 c=next(c for c in m['commits'] if c['seed']==int(Path(file).parent.name));assert sha(file)==c['records_sha256']
 for line in Path(file).open():
  row=json.loads(line);original+=1;o=row['observation'];p=o['observer_player'];gid=row['game_id'];allgames.add(gid);rid=f"{row['seed']}:{o['turn_index']}:{p}";known=[round((row['state_features'][t]+row['state_features'][27+t])*4) for t in range(27)]
  for k,a in enumerate(row['target_active']):
   if a:secondary[(gid,rid+f':opponent{k}','tenpai')]=int(row['structural_tenpai'][k])
   if not(a and row['structural_tenpai'][k]):continue
   q=(p+k+1)%4;missing=o['declared_missing_suits'][q]
   for t in range(27):
    sid=f'{rid}:target{q}:tile{t}';assert sid not in expected;expected[sid]=dict(game_id=gid,row_id=rid,seed=row['seed'],turn_index=o['turn_index'],observer=p,relative_opponent=k,absolute_target=q,tile=t,target_missing_suit=missing,known_physical_copies=known[t],allowed_suit=t//9!=missing,structural_wait_label=int(row['structural_waits'][k][t]))
  for t,legal in enumerate(row['legal_mask']):
   if legal:secondary[(gid,rid+f':discard{t}','legal_risk')]=int(bool(row['joint_winner_mask'][t]))
assert original==2395 and len(allgames)==200
samples=[];seen=set();secseen=set()
for line in pred.open():
 s=json.loads(line)
 if s['task']=='conditional_structural_wait':
  sid=s['sample_id'];assert sid not in seen;seen.add(sid);e=expected[sid];assert all(s[k]==v for k,v in e.items());assert all(math.isfinite(p) and 0<=p<=1 for p in s['predictions'].values());assert s['predictions']['v1counts_missing_zero']==(s['predictions']['v1counts_raw'] if s['allowed_suit'] else 0);samples.append(s)
 else:
  task='tenpai' if s['task']=='tenpai' else 'legal_risk';assert s['label']==secondary[(s['game_id'],s['sample_id'],task)];key=(s['model'],s['task'],s['sample_id']);assert key not in secseen;secseen.add(key)
assert seen==set(expected)
def loss(p,y):
 p=min(1-1e-7,max(1e-7,p));return ((p-y)**2,-y*math.log(p)-(1-y)*math.log(1-p))
results={};rng=random.Random(42);gids=sorted(allgames);draws=[rng.choices(gids,k=200) for _ in range(300)]
for domain in ('all27','allowed18'):
 selected=[s for s in samples if domain=='all27' or s['allowed_suit']];groups={name:defaultdict(lambda:[0.,0.,0]) for name in selected[0]['predictions']}
 for s in selected:
  for name,p in s['predictions'].items():
   b,l=loss(p,s['structural_wait_label']);g=groups[name][s['game_id']];g[0]+=b;g[1]+=l;g[2]+=1
 results[domain]={}
 for name in groups:
  n=sum(v[2] for v in groups[name].values());point=[sum(v[i] for v in groups[name].values())/n for i in (0,1)]
  for i,metric in enumerate(('brier','log_loss')):assert abs(point[i]-r['metrics'][domain][name][metric])<1e-6
  if name=='shared_tile_v2':continue
  pair={}
  for i,metric in enumerate(('brier','log_loss')):
   delta=sum(groups['shared_tile_v2'][g][i]-groups[name][g][i] for g in gids)/n;boots=sorted(sum(groups['shared_tile_v2'][g][i]-groups[name][g][i] for g in d)/sum(groups[name][g][2] for g in d) for d in draws);ci=[boots[7],boots[292]];reported=r['paired_game_bootstrap_new_minus_comparator'][domain][name][metric];assert abs(delta-reported['new_minus_comparator'])<1e-6;assert max(abs(a-b) for a,b in zip(ci,reported['ci95']))<1e-6;pair[metric]=dict(new_minus_comparator=delta,ci95=ci)
  results[domain][name]=pair
out=dict(passed=True,original_records=original,games=200,explicit_wait_samples=len(samples),positive_waits=sum(s['structural_wait_label'] for s in samples),sample_file_sha256=sha(pred),candidate_hashes=r['candidate_hashes'],comparisons=results,bootstrap_unit='200 whole games with all correlated target/tile samples together',replicates=300,no_inference=True,no_fit=True,no_calibration=True,no_selection=True,limitations=['audit reconstructs saved model probabilities, does not rerun networks','statistical prior probabilities not independently recomputed from train in this pass','200simulated games not playing-strength or production certification'])
(root/'reports/next_d_fresh200_audit.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='comparisons'})

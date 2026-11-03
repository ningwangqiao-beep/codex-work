"""Independent paired game-cluster audit of frozen auxiliary predictions."""
import sys,json,hashlib,math,random,time
from pathlib import Path
from collections import defaultdict
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run():
 start=time.perf_counter();auxpath=root/'datasets/next_aux_validation100/manifest.json';aux=json.loads(auxpath.read_text());tasks=('structural_tenpai','conditional_structural_wait','legal_any_winner_risk','legal_multiwinner_risk');expected={t:[] for t in tasks}
 for filename in aux['shards']['auxiliary']:
  for line in Path(filename).open():
   r=json.loads(line);gid=r['game_id'];base=(gid,r['observation']['turn_index'],r['observation']['observer_player'])
   for k,active in enumerate(r['target_active']):
    if not active:continue
    expected[tasks[0]].append((base+(k,None),gid,int(r['structural_tenpai'][k])))
    if r['structural_tenpai'][k]:
     for tile in range(27):expected[tasks[1]].append((base+(k,tile),gid,int(r['structural_waits'][k][tile])))
   for tile,legal in enumerate(r['legal_mask']):
    if legal:
     mask=r['joint_winner_mask'][tile];expected[tasks[2]].append((base+(None,tile),gid,int(mask!=0)));expected[tasks[3]].append((base+(None,tile),gid,int(mask.bit_count()>1)))
 canonical=[(task,*item) for task in tasks for item in expected[task]];models={};evidence={}
 for family in ('counts','progress','history','exchange','history_shuffled'):
  stem=root/'reports'/f'next_c_opponent1000_v1_{family}_aux100';report=json.loads(stem.with_suffix('.json').read_text());prediction=stem.with_suffix('.predictions.jsonl');assert sha(prediction)==report['prediction_artifact']['sha256'];assert report['audit']['aux_manifest_sha256']==sha(auxpath)
  for rel,h in report['audit']['pipeline_source_hashes'].items():assert sha(root/rel)==h
  cp=root/'checkpoints'/f'next_opponent1000_v1_{family}'/'epoch_5.pt';assert sha(cp)==report['checkpoint_sha256']
  grouped={t:defaultdict(lambda:[0.,0.,0]) for t in tasks};count=0
  for count,(line,identity) in enumerate(zip(prediction.open(),canonical,strict=True),1):
   r=json.loads(line);task,sample_id,gid,label=identity;assert r['task']==task and r['game_id']==gid and r['label']==label;prob=r['probability'];assert math.isfinite(prob) and 0<=prob<=1;clip=min(1-1e-7,max(1e-7,prob));g=grouped[task][gid];g[0]+=(prob-label)**2;g[1]+=-(label*math.log(clip)+(1-label)*math.log(1-clip));g[2]+=1
  assert count==len(canonical)
  for task in tasks:
   n=sum(x[2] for x in grouped[task].values());b=sum(x[0] for x in grouped[task].values())/n;l=sum(x[1] for x in grouped[task].values())/n;assert abs(b-report['metrics'][task]['brier'])<1e-6 and abs(l-report['metrics'][task]['log_loss'])<1e-6
  for task in tasks:
   for gid in grouped['structural_tenpai']:grouped[task].setdefault(gid,[0.,0.,0])
  models[family]=grouped;evidence[family]=dict(prediction_sha256=sha(prediction),checkpoint_sha256=sha(cp),rows=count)
 comparisons={}
 for old,new in (('counts','progress'),('progress','history'),('history','exchange'),('history_shuffled','history')):
  comparison={}
  for task in tasks:
   gids=sorted(models[old][task]);assert gids==sorted(models[new][task]);differences={gid:[models[new][task][gid][i]-models[old][task][gid][i] for i in (0,1)]+[models[old][task][gid][2]] for gid in gids};rng=random.Random(42);draws=[rng.choices(gids,k=len(gids)) for _ in range(2000)];result={}
   for index,metric in enumerate(('brier','log_loss')):
    values=sorted(sum(differences[g][index] for g in draw)/sum(differences[g][2] for g in draw) for draw in draws);result[metric]=dict(new_minus_old=sum(x[index] for x in differences.values())/sum(x[2] for x in differences.values()),whole_game_cluster_bootstrap95ci=[values[50],values[1949]])
   comparison[task]=dict(games=len(gids),observations=len(expected[task]),positive=sum(item[2] for item in expected[task]),metrics=result)
  comparisons[new+'_minus_'+old]=comparison
 output=dict(passed=True,evidence=evidence,comparisons=comparisons,aux_manifest_sha256=sha(auxpath),sample_identity_definition='reconstructed deterministically from frozen auxiliary record order: game_id/public_turn/observer/target_relative/tile/task',prediction_explicit_sample_id_missing=True,bootstrap=dict(unit='whole game, all same-game samples resampled together',replicates=2000,seed=42,estimand='pooled observation loss difference new-old; negative improves'),seconds=time.perf_counter()-start,limitations=['prediction files contain task/game_id only; row IDs reconstructed and labels/order checked, cannot independently prove no within-game equal-label permutation','52risk candidates in20games are correlated, not52 independent trials','multiwinner0positive cannot validate tails','auxiliary only; no calibration, tuning, policy-strength or promotion claim'])
 (root/'reports/next_d_opponent_paired_audit.json').write_text(json.dumps(output,indent=2));print(json.dumps(comparisons,indent=2))
if __name__=='__main__':run()


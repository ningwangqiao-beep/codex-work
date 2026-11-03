"""One frozen-candidate holdout evaluation; train-only priors, no calibration."""
import argparse,collections,json,pathlib,random,sys,time
import torch
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from models.next_opponent import OpponentAblation
from models.next_opponent_tile_v2 import SharedTileOpponent
from training.next_opponent_pipeline import collate as flat_collate,constrained_joint_logits,read,records,sha
from training.next_opponent_tile_v2_pipeline import collate as tile_collate
from evaluation.metrics import binary_metrics
BASELINE_SOURCE='scripts/next_model_opponent_diagnose_v2.py'
COMPARATORS=['v1counts_raw','v1counts_missing_zero','train_missing_tile_known_prior','public_missing_unknown_copy_weight']
DEPENDENCIES=['models/next_opponent.py','models/next_opponent_tile_v2.py','training/next_opponent_pipeline.py','training/next_opponent_tile_v2_pipeline.py','evaluation/next_opponent_control.py','evaluation/metrics.py',BASELINE_SOURCE]

def check(manifest,approval,audit,flat,shared):
 a=read(approval);m=read(manifest);d=read(audit)
 if a.get('approved') is not True or a.get('candidates_frozen') is not True or a.get('games')!=200:raise ValueError('Chief frozen200 approval required')
 if m.get('version')!='next-opponent-holdout200-v1' or m.get('games')!=200 or m.get('seed_range')!=[7120000,7120199] or not all(m.get(x) is True for x in ('no_training','no_calibration','no_selection')):raise ValueError('Fresh200 immutable role mismatch')
 if d.get('passed') is not True or d.get('manifest_sha256')!=sha(manifest) or d.get('games')!=200:raise ValueError('Independent holdout audit required')
 if m['source_hashes']!=a['source_hashes'] or m['candidate_checkpoint_hashes']!=a['candidate_checkpoint_hashes']:raise ValueError('Generation approval binding mismatch')
 for name,digest in m['source_hashes'].items():
  if sha(ROOT/name)!=digest:raise ValueError('Data source drift '+name)
 for checkpoint in (flat,shared):
  if a['candidate_checkpoint_hashes'].get(str(pathlib.Path(checkpoint).resolve()))!=sha(checkpoint):raise ValueError('Unregistered checkpoint')
 p=a['protocol']
 if p.get('comparators')!=COMPARATORS or p.get('epoch')!=5 or p.get('train_seed')!=42 or p.get('calibration') is not False or p.get('selection') is not False or p.get('bootstrap_unit')!='whole_game_paired' or p.get('baseline_source_sha256')!=sha(ROOT/BASELINE_SOURCE):raise ValueError('Pre-registration/baseline definition drift')
 commits={c['seed']:c for c in m['commits']};seeds=[]
 for path in m['shards']['holdout']:
  f=pathlib.Path(path);seed=int(f.parent.name);seeds.append(seed);c=commits[seed]
  if f.parent.parent.name!='holdout' or c['seat']!=(seed-7120000)%4 or sha(f)!=c['records_sha256'] or sha(f.parent/'game.json')!=c['game_sha256']:raise ValueError('Holdout shard drift')
 if sorted(seeds)!=list(range(7120000,7120200)):raise ValueError('Exact200seed set required')
 return m,a
def load(path,cls,version,manifest_sha):
 s=torch.load(path,map_location='cpu',weights_only=False)
 if s.get('version')!=version or s.get('epoch')!=5 or not s.get('epoch_complete') or s['config']['seed']!=42 or s['audit']['train_manifest_sha256']!=manifest_sha:raise ValueError('Only registered final epoch5 allowed')
 for path,digest in s['audit']['pipeline_source_hashes'].items():
  if sha(ROOT/path)!=digest:raise ValueError('Frozen model source drift '+path)
 model=cls(s['config']['family']);model.load_state_dict(s['model']);return model.eval()
def fit_priors(manifest):
 m=read(manifest)
 if m.get('dataset_version')!='next-history1000':raise ValueError('Training1000 only')
 commits={c['seed']:c for c in m['commits'] if c['split']=='train'};paths=m['shards']['train']
 if sorted(int(pathlib.Path(p).parent.name) for p in paths)!=list(range(7000000,7001000)):raise ValueError('Exact1000train partition required')
 for path in paths:
  if sha(path)!=commits[int(pathlib.Path(path).parent.name)]['records_sha256']:raise ValueError('Training shard changed')
 table=collections.defaultdict(lambda:[0,0]);positive=cases=0
 for row in records(paths):
  o=row['observation'];p=o['observer_player']
  for k in range(3):
   if not(row['target_active'][k] and row['structural_tenpai'][k]):continue
   cases+=1;missing=o['declared_missing_suits'][(p+k+1)%4]
   for tile in range(27):
    known=round((row['state_features'][tile]+row['state_features'][27+tile])*4);y=int(row['structural_waits'][k][tile]);q=table[(missing,tile,known)];q[0]+=y;q[1]+=1;positive+=y
 return table,positive/cases,{'train_true_tenpai_cases':cases,'train_positive_wait_tiles':positive,'expected_wait_count':positive/cases,'train_manifest_sha256':sha(manifest)}
def stats(prob,label):return binary_metrics(prob,label) if len(label) else None
def run(args):
 out=pathlib.Path(args.output);prediction_path=out.with_suffix('.samples.jsonl')
 if out.exists() or prediction_path.exists():raise ValueError('Holdout outputs immutable; no repeated evaluation overwrite')
 torch.set_num_threads(2);began=time.perf_counter();m,a=check(args.manifest,args.approval,args.audit,args.flat,args.shared);train_sha=sha(args.train_manifest);flat=load(args.flat,OpponentAblation,'NEXT-OPPONENT-ABLATION-v1',train_sha);shared=load(args.shared,SharedTileOpponent,'NEXT-OPPONENT-SHARED-TILE-v2',train_sha);table,expected,prior=fit_priors(args.train_manifest);sources={path:sha(ROOT/path) for path in DEPENDENCIES};sources[str(pathlib.Path(__file__).relative_to(ROOT))]=sha(__file__)
 names=['shared_tile_v2',*COMPARATORS];wait={n:[] for n in names};labels=[];allowed=[];gids=[];sample_rows=[];secondary={n:{'tenpai':[],'legal_risk':[]} for n in ('shared_tile_v2','v1counts_raw')};all_games=set();seen=set();rows=[]
 def consume(rows):
  inp,t=flat_collate(rows,'cpu','counts');newinp,newt=tile_collate(rows,'cpu','shared_tile')
  with torch.inference_mode():old=flat(*inp);new=shared(*newinp);pw={'v1counts_raw':old['conditional_structural_wait_logits'].sigmoid(),'shared_tile_v2':new['conditional_structural_wait_logits'].sigmoid()};outputs={'shared_tile_v2':new,'v1counts_raw':old};auxpred={name:(output['structural_tenpai_logits'].sigmoid(),1-constrained_joint_logits(output,t).softmax(-1)[:,:,0]) for name,output in outputs.items()}
  for i,r in enumerate(rows):
   o=r['observation'];p=o['observer_player'];gid=str(r['game_id']);all_games.add(gid);rowid=f"{r['seed']}:{o['turn_index']}:{p}";known=[round((r['state_features'][tile]+r['state_features'][27+tile])*4) for tile in range(27)]
   for name,output in outputs.items():
    pt,risk=auxpred[name]
    for k in range(3):
     if r['target_active'][k]:secondary[name]['tenpai'].append((float(pt[i,k]),int(r['structural_tenpai'][k]),gid,f'{rowid}:opponent{k}'))
    for tile,legal in enumerate(r['legal_mask']):
     if legal:secondary[name]['legal_risk'].append((float(risk[i,tile]),int(bool(r['joint_winner_mask'][tile])),gid,f'{rowid}:discard{tile}'))
   for k in range(3):
    if not(r['target_active'][k] and r['structural_tenpai'][k]):continue
    q=(p+k+1)%4;missing=o['declared_missing_suits'][q];weights=[0 if tile//9==missing else 4-known[tile] for tile in range(27)];total=sum(weights)
    for tile in range(27):
     sid=f'{rowid}:target{q}:tile{tile}';assert sid not in seen;seen.add(sid);forbidden=tile//9==missing;y=int(r['structural_waits'][k][tile]);assert not(forbidden and y);positive,count=table[(missing,tile,known[tile])];v={'shared_tile_v2':float(pw['shared_tile_v2'][i,k,tile]),'v1counts_raw':float(pw['v1counts_raw'][i,k,tile]),'v1counts_missing_zero':0 if forbidden else float(pw['v1counts_raw'][i,k,tile]),'train_missing_tile_known_prior':0 if forbidden else (positive+1)/(count+2),'public_missing_unknown_copy_weight':expected*weights[tile]/total if total else 0}
     for name,value in v.items():assert 0<=value<=1;wait[name].append(value)
     labels.append(y);allowed.append(not forbidden);gids.append(gid);sample_rows.append({'game_id':gid,'sample_id':sid,'row_id':rowid,'seed':r['seed'],'turn_index':o['turn_index'],'observer':p,'relative_opponent':k,'absolute_target':q,'tile':tile,'target_missing_suit':missing,'known_physical_copies':known[tile],'allowed_suit':not forbidden,'structural_wait_label':y,'predictions':v})
 for row in records(m['shards']['holdout']):
  rows.append(row)
  if len(rows)==128:consume(rows);rows=[]
 if rows:consume(rows)
 metrics={};paired={};rng=random.Random(42);all_game_ids=sorted(all_games);bootstrap_game_draws=[rng.choices(all_game_ids,k=len(all_game_ids)) for _ in range(300)]
 for domain in ('all27','allowed18'):
  select=[i for i in range(len(labels)) if domain=='all27' or allowed[i]];target=[labels[i] for i in select];p={name:[wait[name][i] for i in select] for name in names};metrics[domain]={name:stats(prob,target) for name,prob in p.items()};index=collections.defaultdict(list)
  for j,i in enumerate(select):index[gids[i]].append(j)
  differences={name:{key:[] for key in ('brier','log_loss','roc_auc','average_precision')} for name in COMPARATORS}
  for draw in bootstrap_game_draws:
   positions=[i for gid in draw for i in index[gid]];ys=[target[i] for i in positions];newmetric=stats([p['shared_tile_v2'][i] for i in positions],ys)
   for name in COMPARATORS:
    other=stats([p[name][i] for i in positions],ys)
    for key in differences[name]:
     if newmetric is not None and newmetric[key] is not None and other[key] is not None:differences[name][key].append(newmetric[key]-other[key])
  paired[domain]={}
  for name,keys in differences.items():
   paired[domain][name]={}
   for key,values in keys.items():
    values.sort();paired[domain][name][key]={'new_minus_comparator':metrics[domain]['shared_tile_v2'][key]-metrics[domain][name][key] if metrics[domain]['shared_tile_v2'][key] is not None and metrics[domain][name][key] is not None else None,'ci95':[values[int(.025*len(values))],values[min(len(values)-1,int(.975*len(values)))]] if values else None,'valid_bootstrap_replicates':len(values)}
 report={'scope':'one_frozen_candidate_independent200game_holdout_NO_fit_NO_calibration_NO_selection_NO_policy_promotion','holdout_manifest_sha256':sha(args.manifest),'approval_sha256':sha(args.approval),'independent_audit_sha256':sha(args.audit),'candidate_hashes':a['candidate_checkpoint_hashes'],'train_prior_fit':prior,'metrics':metrics,'paired_game_bootstrap_new_minus_comparator':paired,'bootstrap_replicates':300,'secondary_metrics':{name:{task:stats([x[0] for x in items],[x[1] for x in items]) for task,items in tasks.items()} for name,tasks in secondary.items()},'games':len(all_games),'conditional_wait_elements':len(labels),'positive_waits':sum(labels),'source_hashes':sources,'seconds':time.perf_counter()-began,'limitations':['programmed missing-zero is rule ability, not learned gain','structural waits retain public-dead possibilities; no hardzero at known4','all27 includes easy forbidden-suit negatives; allowed18 is necessary finer discrimination','only200simulated games and correlated within-game targets; not production or play-strength certification','no rescaling/calibration/fitting on holdout; priors only use1000train','other-task joint and wait heads remain separately estimated; no coherence claim']}
 if check(args.manifest,args.approval,args.audit,args.flat,args.shared)[0]!=m:raise ValueError('Holdout changed during evaluation')
 if any(sha(ROOT/path)!=digest for path,digest in sources.items()):raise ValueError('Evaluation source changed')
 with prediction_path.open('x',encoding='utf-8') as stream:
  for row in sample_rows:stream.write(json.dumps({'task':'conditional_structural_wait',**row})+'\n')
  for name,tasks in secondary.items():
   for task,items in tasks.items():
    for probability,label,gid,sid in items:stream.write(json.dumps({'task':task,'model':name,'sample_id':sid,'game_id':gid,'probability':probability,'label':label})+'\n')
 report['sample_predictions']={'path':str(prediction_path),'sha256':sha(prediction_path)};out.write_text(json.dumps(report,indent=2));print(json.dumps({'output':str(out),'games':len(all_games),'conditional_wait_elements':len(labels),'metrics':metrics,'seconds':report['seconds']},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--approval',required=True);p.add_argument('--audit',required=True);p.add_argument('--train-manifest',default=str(ROOT/'datasets/next_history1000/manifest.json'));p.add_argument('--flat',required=True);p.add_argument('--shared',required=True);p.add_argument('--output',required=True);run(p.parse_args())

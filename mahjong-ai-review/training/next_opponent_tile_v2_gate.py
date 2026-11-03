"""Chief-signed fixed-budget ablation gate; auxiliary data is evaluation only."""
import pathlib
from models.next_opponent_tile_v2 import FAMILIES
from training.next_opponent_tile_v2_pipeline import read,sha
PIPELINE=('models/next_opponent_tile_v2.py','training/next_opponent_tile_v2_pipeline.py','training/next_opponent_tile_v2_gate.py','training/next_opponent_tile_v2_fit.py','training/next_opponent_tile_v2_eval.py','evaluation/next_opponent_control.py','evaluation/metrics.py','scripts/next_model_opponent_tile_v2_train.py','scripts/next_model_opponent_tile_v2_eval.py')
def source_hashes(root):return {p:sha(pathlib.Path(root)/p) for p in PIPELINE}
def validate(train_manifest,aux_manifest,admission,root):
 root=pathlib.Path(root);m=read(train_manifest);aux=read(aux_manifest);a=read(admission)
 if a.get('stage')!='NEXT_OPPONENT1000_SHARED_TILE_V2' or a.get('passed') is not True or a.get('supervised_training_allowed') is not True or a.get('rl_training_allowed') is not False or a.get('calibration_allowed') is not False:raise ValueError('Chief supervised-only opponent admission required')
 if a.get('auxiliary_role')!='reused_DEVELOPMENT_only' or a.get('missing_zero_rule_constraint') is not True or a.get('public_dead_zero_constraint') is not False:raise ValueError('Programmed missing-only rule and reused development role required')
 if a.get('families')!=list(FAMILIES) or a.get('epochs')!=6 or a.get('batch_size')!=128 or a.get('seed')!=42 or a.get('model_parameters')!=15918:raise ValueError('Pre-registered same-budget/family configuration mismatch')
 if a.get('train_manifest_sha256')!=sha(train_manifest) or a.get('aux_manifest_sha256')!=sha(aux_manifest) or a.get('pipeline_source_hashes')!=source_hashes(root):raise ValueError('Opponent source/data binding mismatch')
 if m.get('dataset_version')!='next-history1000' or m.get('train_games')!=1000 or aux.get('games')!=100 or aux.get('seed_range')!=[7110000,7110099] or aux.get('no_training') is not True or aux.get('no_calibration_yet') is not True:raise ValueError('Training1000 and evaluation-only auxiliary100 roles required')
 for label in ('prior_scale_admission','aux_independent_audit'):
  spec=a[label];path=pathlib.Path(spec['path']);path=path if path.is_absolute() else root/path;evidence=read(path)
  if sha(path)!=spec['sha256'] or evidence.get('passed') is not True:raise ValueError('Missing bound evidence '+label)
  if label=='aux_independent_audit' and evidence.get('manifest_sha256')!=sha(aux_manifest):raise ValueError('Auxiliary evidence mismatch')
  if label=='prior_scale_admission' and evidence.get('manifest_sha256')!=sha(train_manifest):raise ValueError('Prior training admission mismatch')
 for data,split,start,end in ((m,'train',7000000,7000999),(aux,'auxiliary',7110000,7110099)):
  commits={c['seed']:c for c in data['commits'] if c['split']==split};seeds=[]
  for name,digest in data['source_hashes'].items():
   if sha(root/name)!=digest:raise ValueError('Data source changed '+name)
  for path in data['shards'][split]:
   p=pathlib.Path(path);seed=int(p.parent.name);seeds.append(seed);c=commits[seed]
   if p.parent.parent.name!=split or c['seat']!=seed%4 or sha(p)!=c['records_sha256'] or sha(p.parent/'game.json')!=c['game_sha256']:raise ValueError('Shard hash/seat binding mismatch')
  if sorted(seeds)!=list(range(start,end+1)):raise ValueError('Exact permanent seed partition required')
 return {'admission_sha256':sha(admission),'train_manifest_sha256':sha(train_manifest),'aux_manifest_sha256':sha(aux_manifest),'pipeline_source_hashes':source_hashes(root),'training_allowed':True,'aux_used_for_training':False,'calibration_allowed':False,'rl_allowed':False}

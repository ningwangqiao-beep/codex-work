"""Small V3 teacher-preference dataset, never counterfactual action Q."""
import sys,json,hashlib,time,math
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from simulator.v3_selfplay import play
from baselines.v3_bot import BaselineV3
from models.revision_candidate_schema import adapt,FEATURE_NAMES
from inference.v3_observation import encode_observation
sources=[root/p for p in ('rules/core.py','rules/v3.py','simulator/table.py','simulator/v3_selfplay.py','observations/v3_public.py','observations/public.py','baselines/v3_bot.py','rules/fast_hand_analysis.py','models/revision_candidate_schema.py','inference/v3_observation.py')];before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources};out=root/'datasets/v3_teacher100';out.mkdir(exist_ok=True)
if (out/'manifest.json').exists():raise RuntimeError('Dataset immutable')
start=time.perf_counter();counts={'train':0,'validation':0};seen={};lengths=[]
with (out/'train.jsonl').open('w') as train,(out/'validation.jsonl').open('w') as validation:
 for index in range(100):
  seed=4200000+index;seat=index%4;bot=BaselineV3();records={}
  def policy(o,legal):
   chosen=bot(o,legal);r=adapt(o,bot.last_analysis,f'v3-{seed}',seed,'v3-teacher100');r.update(encode_observation(o));r.update(deal_group_id=f'deal-{seed}',observation=o,state_target_missing=False);records[o['turn_index']]=r;return chosen
  game=play(seed,collect=True,policy=policy,policy_seat=seat,exchange_offset=seed%3+1);labels={(r['observer_player'],r['observation']['turn_index']):r for r in game['rows']};split='train' if index<80 else 'validation';f=train if split=='train' else validation
  for turn,r in records.items():
   label=labels[(seat,turn)];r['state_target']=game['scores'][seat];r.update(structural_tenpai=label['tenpai'],structural_waits=label['waits'],joint_winner_mask=label['joint_outcome'],target_active=label['target_active']);assert len(r['state_features'])==191 and not r['history_truncated'];assert len(r['candidate_features'])==len(r['legal_mask'])==27
   assert all(math.isfinite(v) for v in r['state_features']);assert r['history_original_length']==len(r['history_tokens']);assert seed not in seen or seen[seed]==split;seen[seed]=split;lengths.append(len(r['history_tokens']));f.write(json.dumps(r,separators=(',',':'))+'\n');counts[split]+=1
  f.flush()
after={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources};assert before==after
files={s:str(out/(s+'.jsonl')) for s in counts};hashes={s:hashlib.sha256(Path(p).read_bytes()).hexdigest() for s,p in files.items()};manifest=dict(dataset_version='v3-teacher100',games=100,seed_range=[4200000,4200099],train_games=80,validation_games=20,files=files,data_hashes=hashes,source_hashes=before,counts=counts,candidate_feature_names=FEATURE_NAMES,state_dim=191,history_max=max(lengths),history_truncated=False,target_semantics='lexicographic_preference_rank_NOT_Q',state_target_units='V3 terminal net score in raw base units',state_target_policy='one rotating BaselineV3 seat vs three frozen simulator heuristic styles',final_test_used=False,audit_status='STRUCTURE_CHECKED_PENDING_CHIEF_ISOLATION_ADMISSION',seconds=time.perf_counter()-start)
(out/'manifest.json').write_text(json.dumps(manifest,indent=2));(root/'reports/v3_d_teacher100_audit.json').write_text(json.dumps(manifest,indent=2));print(manifest)

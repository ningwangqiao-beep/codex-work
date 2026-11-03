"""CPU2 same-state shuffled-policy cold/warm timing. No training or game eval."""
import sys,pathlib,json,time,random,statistics,torch,hashlib
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from inference.next_policy import NextPolicy
from baselines.v3_bot import BaselineV3
import rules.fast_hand_analysis as fast
import rules.hand_analysis as hand
import rules.hand_analysis_reference as reference
m=json.load(open(root/'datasets/next_history100/manifest.json'));data=[json.loads(line) for line in open(m['files']['validation'])];rng=random.Random(42);free=[r for r in data if not any(t//9==r['observation']['declared_missing_suits'][r['observation']['observer_player']] for t in r['observation']['observer_hand'])];forced=[r for r in data if r not in free];selected=rng.sample(free,4)+rng.sample(forced,4);rng.shuffle(selected);torch.set_num_threads(2);policies={'multitask':NextPolicy(root/'checkpoints/next_history100_multitask/best_epoch_5.pt'),'action_only':NextPolicy(root/'checkpoints/next_history100_action_only/best_epoch_5.pt'),'strong':BaselineV3()};rows=[];cleared=set()
def clear():
 for module in (fast,hand,reference):
  for name,fn in vars(module).items():
   if callable(fn) and hasattr(fn,'cache_clear'):fn.cache_clear();cleared.add(module.__name__+'.'+name)
start=time.perf_counter()
for index,r in enumerate(selected):
 order=list(policies);rng.shuffle(order);o=r['observation'];legal=tuple(i for i,v in enumerate(r['legal_mask']) if v)
 for name in order:
  clear();t=time.perf_counter();cold_action=policies[name](o,legal);cold=time.perf_counter()-t;warm=[]
  for _ in range(3):
   t=time.perf_counter();action=policies[name](o,legal);warm.append(time.perf_counter()-t);assert action==cold_action
  rows.append({'state_index':index,'game_id':r['game_id'],'history_length':len(r['history_tokens']),'policy':name,'randomized_order':order,'cold_seconds':cold,'warm_seconds':warm})
summary={}
for name in policies:
 values=[r for r in rows if r['policy']==name];summary[name]={'same_states':len(values),'cold_mean_seconds':statistics.mean(r['cold_seconds'] for r in values),'cold_median_seconds':statistics.median(r['cold_seconds'] for r in values),'warm_mean_seconds':statistics.mean(v for r in values for v in r['warm_seconds']),'warm_median_seconds':statistics.median(v for r in values for v in r['warm_seconds'])}
report={'scope':'validation_same_state_timing_only','seconds':time.perf_counter()-start,'cpu_threads':2,'sampling':'seed42 four free/four forced fixed validation states; randomized policy order per state','cache_clear_functions':sorted(cleared),'summary':summary,'rows':rows,'limitations':['cold includes shared table/cache rebuilding; warm repeats same state','8states not a production latency benchmark','earlier fixed-policy-order game timing confounds cache and state distribution; cannot attribute to auxiliary heads'],'no_training':True,'no_final_test':True,'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()};(root/'reports/next_c_timing_audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(summary,indent=2))

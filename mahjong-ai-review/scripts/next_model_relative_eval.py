"""Bounded development-only V3 T2 complete-game comparison. No final seeds."""
import pathlib,sys,argparse,json,time,hashlib,random,statistics,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from inference.next_policy import NextPolicy
from inference.next_relative_policy import RelativePolicy
from baselines.v3_bot import BaselineV3
from simulator.v3_history_v2 import play

def shape(o,legal):
 def quality(t):
  h=list(o['observer_hand']);h.remove(t);return 3*sum(h.count(x)>=2 for x in set(h))+sum(abs(x-y) in (1,2) and x//9==y//9 for i,x in enumerate(h) for y in h[i+1:])
 return max(legal,key=quality)
def components(result,seat):
 parts={}
 for e in result['ledger']:
  parts[e['category']]=parts.get(e['category'],0)+e['amount']*((e['receiver']==seat)-(e['payer']==seat))
 if sum(parts.values())!=result['scores'][seat] or sum(result['scores'])!=0:raise ValueError('Ledger mismatch')
 own=[w for w in result['win_events'] if w['seat']==seat];paid=[w for w in result['win_events'] if w['payer']==seat]
 return {'net_score':result['scores'][seat],'parts':parts,'won':bool(own),'self_draws':sum(w['kind']=='self_draw' for w in own),'winning_fans':[w['final_fan'] for w in own],'deal_in_events':len(paid),'deal_in_loss':sum(w['payment'] for w in paid)}
p=argparse.ArgumentParser();p.add_argument('--multitask',required=True);p.add_argument('--relative',required=True);p.add_argument('--seed',type=int,required=True);p.add_argument('--seeds',type=int,default=2);p.add_argument('--timeout',type=float,default=180);p.add_argument('--output',required=True);a=p.parse_args();out=pathlib.Path(a.output)
if out.exists():raise ValueError('Completed development output immutable')
if set(range(a.seed,a.seed+a.seeds))&set(range(5000000,5005000)):raise ValueError('Frozen final seed interval forbidden')
if a.seeds<1 or a.seeds>20:raise ValueError('Bounded1..20 development seeds only')
torch.set_num_threads(2);policies={'multitask':NextPolicy(a.multitask),'relative':RelativePolicy(a.relative),'strong':BaselineV3()};sources={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'inference/next_policy.py',root/'inference/next_relative_policy.py',pathlib.Path(__file__),root/'simulator/v3_history_v2.py',root/'baselines/v3_bot.py',root/'rules/core.py',root/'rules/v3.py',root/'simulator/table.py']};rows=[];decision_totals={};start=time.perf_counter();error=None;times={k:[0.,0] for k in policies}
try:
 with out.with_suffix('.jsonl').open('x') as log:
  for seed in range(a.seed,a.seed+a.seeds):
   for seat in range(4):
    for name,callback in policies.items():
     rng=random.Random(seed*4+seat)
     def policy(o,legal):
      if time.perf_counter()-start>a.timeout:raise TimeoutError('Development runtime bound')
      if o['observer_player']!=seat:return rng.choice(legal)
      t=time.perf_counter();action=callback(o,legal);times[name][0]+=time.perf_counter()-t;times[name][1]+=1
      if hasattr(callback,'last_decision') and callback.last_decision is not None:
       d=callback.last_decision;key=name+('/free' if d['free'] else '/forced');g=decision_totals.setdefault(key,{'n':0,'exact':0,'equivalent':0,'rank_regret':0.,'ukeire_regret':0.,'higher_structural':0,'higher_missing_debt':0});g['n']+=1
       for k in g:
        if k!='n':g[k]+=d[k]
      return action
     before_diagnostics={k:dict(v) for k,v in decision_totals.items()};result=play(seed,policy=policy,policy_seat=None,exchange_offset=seed%3+1);row={'seed':seed,'seat':seat,'policy':name,'metrics':components(result,seat),'scores':result['scores']};row['decision_diagnostics']={k:{field:value-before_diagnostics.get(k,{}).get(field,0) for field,value in g.items()} for k,g in decision_totals.items() if k.startswith(name+'/')};rows.append(row);log.write(json.dumps(row)+'\n');log.flush()
except Exception as e:error=repr(e)
for rel,digest in sources.items():
 if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=digest:error='Source changed during development evaluation: '+rel
complete=[s for s in range(a.seed,a.seed+a.seeds) if sum(r['seed']==s for r in rows)==12];summary={}
for name in policies:
 selected=[r for r in rows if r['policy']==name and r['seed'] in complete]
 if selected:
  n=len(selected);summary[name]={'games':n,'mean_net_score':statistics.mean(r['metrics']['net_score'] for r in selected),'win_rate':statistics.mean(r['metrics']['won'] for r in selected),'self_draw_rate':statistics.mean(r['metrics']['self_draws'] for r in selected),'deal_in_event_rate':statistics.mean(r['metrics']['deal_in_events'] for r in selected),'deal_in_game_rate':statistics.mean(bool(r['metrics']['deal_in_events']) for r in selected),'mean_deal_in_loss':statistics.mean(r['metrics']['deal_in_loss'] for r in selected),'seat_mean':{str(p):statistics.mean(r['metrics']['net_score'] for r in selected if r['seat']==p) for p in range(4)},'parts_mean':{c:sum(r['metrics']['parts'].get(c,0) for r in selected)/n for c in {c for r in selected for c in r['metrics']['parts']}}}
comparisons={};rng=random.Random(42)
for modelname in ('multitask','relative'):
 for baseline in (('strong','multitask') if modelname=='relative' else ('strong',)):
  diffs=[sum(r['metrics']['net_score']*(1 if r['policy']==modelname else -1) for r in rows if r['seed']==s and r['policy'] in (modelname,baseline))/4 for s in complete]
  if diffs:
   boot=sorted(statistics.mean(rng.choices(diffs,k=len(diffs))) for _ in range(1000));comparisons[modelname+'_vs_'+baseline]={'paired_initial_seed_mean':statistics.mean(diffs),'seed_bootstrap95ci':[boot[25],boot[974]],'seed_differences':diffs}
r={'status':'incomplete' if error else 'completed','error':error,'scope':'development_seeds_only_NO_final_test_NO_promotion','rule_version':'SICHUAN-XUEZHAN-4FAN-V3','seed_range':[a.seed,a.seed+a.seeds-1],'complete_seed_groups':len(complete),'seconds':time.perf_counter()-start,'summary':summary,'comparisons':comparisons,'inference_cost':{k:{'seconds':v[0],'decisions':v[1],'mean_seconds':v[0]/v[1] if v[1] else None} for k,v in times.items()},'decision_diagnostics':decision_totals,'model_metadata':{k:v.metadata for k,v in policies.items() if hasattr(v,'metadata')},'source_hashes':sources,'limitations':['random legal-discard opponents; claims/default other stages shared simulator','paired initial deal does not imply identical future trajectories','preference head not counterfactual Q; policy-conditioned V unused for choice','20seed or smaller development sample; no strength promotion']};out.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
if error:raise SystemExit(2)

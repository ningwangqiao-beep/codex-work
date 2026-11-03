"""V3 paired initial deal and rotated-seat comparison; no training."""
import sys,argparse,time,json,random,statistics,hashlib,os
from collections import Counter,defaultdict
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from simulator.v3_selfplay import play
from inference.v3_legacy import LegacyV3DiscardPolicy

def shape(o,legal):
 def quality(t):
  h=list(o['observer_hand']);h.remove(t);return sum(h.count(x)>=2 for x in set(h))*3+sum(abs(x-y) in (1,2) and x//9==y//9 for i,x in enumerate(h) for y in h[i+1:])
 return max(legal,key=quality)
def metrics(r,seat):
 parts={}
 for e in r['ledger']:
  amount=e['amount']*((e['receiver']==seat)-(e['payer']==seat));parts[e['category']]=parts.get(e['category'],0)+amount
 assert sum(parts.values())==r['scores'][seat]
 own=[w for w in r['win_events'] if w['seat']==seat];paid=[w for w in r['win_events'] if w['payer']==seat]
 return dict(net=r['scores'][seat],parts=parts,win=int(bool(own)),self_draw=sum(w['kind']=='self_draw' for w in own),fan_sum=sum(w['final_fan'] for w in own),win_events=len(own),deal_in_events=len(paid),deal_in_loss=sum(w['payment'] for w in paid))
def run(games=2,seed=3400000,timeout=90,strong=False,opponents="random",resume=False):
 import torch
 torch.set_num_threads(2);start=time.perf_counter();rows=[];error=None
 policies={'random':None,'shape':shape,'old_candidate':LegacyV3DiscardPolicy(root/'experiments/round2_c/candidate/best.pt','candidate'),'old_residual':LegacyV3DiscardPolicy(root/'checkpoints/round2_candidate_rl_rounded/last.pt','residual')}
 if strong:
  from baselines.v3_bot import BaselineV3
  policies['new_baseline']=BaselineV3()
 sources=[root/p for p in ('rules/core.py','rules/v3.py','simulator/table.py','simulator/v3_selfplay.py','observations/v3_public.py','observations/public.py')];before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
 final=root/'reports'/f'v3_d_compare_{seed}_{opponents}.json'
 if final.exists():raise ValueError('Final result immutable; use new independent seed')
 partial=root/'reports'/f'v3_d_compare_{seed}_{opponents}.jsonl'
 meta_path=partial.with_suffix('.meta.json')
 extra=[root/'baselines/v3_bot.py',root/'rules/fast_hand_analysis.py',Path(__file__).resolve()]
 config=dict(games=games,seed=seed,strong=strong,opponents=opponents,sources=before,extra_sources={str(x.relative_to(root)):hashlib.sha256(x.read_bytes()).hexdigest() for x in extra},weights={k:v.metadata['checkpoint_sha256'] for k,v in policies.items() if hasattr(v,'metadata')})
 if resume:
  if json.loads(meta_path.read_text())!=config:raise ValueError('Resume config/source/weights mismatch')
  prior=[json.loads(line) for line in partial.read_text().splitlines() if line.strip()];seen_counts=Counter(x['seed'] for x in prior);done={s for s,n in seen_counts.items() if n==4*len(policies)};rows=[x for x in prior if x['seed'] in done]
 else:
  if partial.exists():raise ValueError('Existing partial requires --resume')
  done=set();meta_path.write_text(json.dumps(config,indent=2))
 partial.write_text(''.join(json.dumps(x)+'\n' for x in rows))
 try:
  with partial.open('a') as f:
   for s in range(seed,seed+games):
    if s in done:continue
    for seat in range(4):
     for name,callback in policies.items():
      rng=random.Random(s*4+seat)
      def policy(o,legal):
       if os.environ.get('MAHJONG_STOP_FILE') and Path(os.environ['MAHJONG_STOP_FILE']).exists():raise InterruptedError('STOP requested')
       if time.perf_counter()-start>timeout:raise TimeoutError('comparison budget')
       if o['observer_player']==seat:return callback(o,legal) if callback else rng.choice(legal)
       style=(s+o['observer_player'])%4
       if opponents=='random' or style==0:return rng.choice(legal)
       if style==1:return shape(o,legal)
       if style==2:
        suit=max(range(3),key=lambda z:sum(t//9==z for t in o['observer_hand']))
        return min(legal,key=lambda t:(t//9==suit,t))
       return max(legal,key=lambda t:(sum(x==t for _,x in o['visible_discards']),-t))
      r=play(s,policy=policy,policy_seat=None,exchange_offset=s%3+1);row=dict(seed=s,seat=seat,opponent_style_combo=[(['random','shape','pure','defensive'][(s+q)%4] if opponents=='mixed' else 'random') for q in range(4) if q!=seat],policy=name,metrics=metrics(r,seat),scores=r['scores']);rows.append(row);f.write(json.dumps(row)+'\n');f.flush()
 except (Exception,KeyboardInterrupt) as e:error=repr(e)
 after={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
 if before!=after:error='source changed'
 seen_counts=Counter(r['seed'] for r in rows);complete={s for s,n in seen_counts.items() if n==4*len(policies)};indexed=defaultdict(list);seed_sums=defaultdict(float);stratified=defaultdict(list)
 for row in rows:
  if row['seed'] in complete:
   indexed[row['policy']].append(row);seed_sums[(row['seed'],row['policy'])]+=row['metrics']['net'];stratified[(row['policy'],row['seat'],tuple(row.get('opponent_style_combo',[])))].append(row['metrics']['net'])
 summary={};comparisons={};rng=random.Random(42)
 for name in policies:
  selected=indexed[name]
  if not selected:continue
  n=len(selected);summary[name]={k:sum(r['metrics'][k] for r in selected)/n for k in ('net','win','self_draw','deal_in_events','deal_in_loss')};w=sum(r['metrics']['win_events'] for r in selected);summary[name]['mean_winning_fan']=sum(r['metrics']['fan_sum'] for r in selected)/w if w else None
  summary[name]['parts_mean']={c:sum(r['metrics']['parts'].get(c,0) for r in selected)/n for c in {c for r in selected for c in r['metrics']['parts']}}
  if name!='shape':
   differences=[(seed_sums[(s,name)]-seed_sums[(s,'shape')])/4 for s in sorted(complete)];boot=sorted(statistics.mean(rng.choices(differences,k=len(differences))) for _ in range(2000));comparisons[name]={'mean_vs_shape':statistics.mean(differences),'paired_seed_ci':[boot[50],boot[1949]]}
 group_summary=[dict(policy=k[0],seat=k[1],opponent_style_combo=k[2],n=len(v),mean_net=statistics.mean(v)) for k,v in stratified.items()]
 result=dict(group_summary=group_summary,evaluation_scale='final5000_seed_groups' if games>=5000 else 'development_small_sample',opponents=opponents,config_binding=config,status='incomplete' if error else 'completed',error=error,complete_seed_groups=len(complete),seconds=time.perf_counter()-start,summary=summary,comparisons=comparisons,source_before=before,source_after=after,legacy_metadata={k:v.metadata for k,v in policies.items() if hasattr(v,'metadata')},limitations=['opponent discards configured by CLI; meld actions shared simulator','win events not transfer count','configured singlemax settlement; not verified room','paired initial deal not identical future','promotion_requires_chief_review_of_predeclared_final_evaluation'])
 target=final if error is None else final.with_suffix('.partial.json')
 target.write_text(json.dumps(result,indent=2));print(result)
 if error:raise SystemExit(2)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--games',type=int,default=2);p.add_argument('--seed',type=int,default=3400000);p.add_argument('--timeout',type=float,default=90);p.add_argument('--strong',action='store_true');p.add_argument('--opponents',choices=['random','mixed'],default='random');p.add_argument('--resume',action='store_true');a=p.parse_args();run(a.games,a.seed,a.timeout,a.strong,a.opponents,a.resume)





"""Training only: never loads W0. All candidates pre-registered in search_space.json."""
from common import *
assert sha(ROOT/'search_space.json')=='487d77a08526f2ed454d58545f6c3c7b11469e9e119596da173e8e55171d8d48'
if (RESULTS/'selection.json').exists():raise RuntimeError('Selection already locked; refuse overwrite or training after holdout.')
params=json.loads((ROOT/'search_space.json').read_text());assert len(params)==24
ranges={'W1':('2024-11-01','2025-05-01'),'W2':('2025-05-01','2025-11-01'),'W3':('2026-05-01','2026-10-31')}
data={w:load_window(w) for w in ranges}
validations=[validate(w,data[w],*ranges[w]) for w in ranges]
(RESULTS/'training_data_validation.json').write_text(json.dumps(validations,indent=2))
comparisons=[]
for name,p in [('A_b',dict(reset=1)),('C04',C04)]:
 for w,a in data.items():
  comparisons.append(evaluate(name,w,a,p))
  comparisons.append(evaluate(name+'_TP_only',w,a,dict(p,clamp_add=0)))
pd.DataFrame(comparisons).to_csv(RESULTS/'measurement_runs.csv',index=False)
rows=[]
for name,p in params.items():
 for w,a in data.items():rows.append(evaluate(name,w,a,p))
 pd.DataFrame(rows).to_csv(RESULTS/'candidates.csv',index=False)
f=pd.DataFrame(rows);ranking=f.groupby('candidate').agg(worst_return=('return_pct','min'),sum_return=('return_pct','sum'),worst_dd=('maxdd_pct','max')).reset_index().sort_values(['worst_return','sum_return','candidate'],ascending=[False,False,True])
ranking.to_csv(RESULTS/'ranking.csv',index=False)
best=ranking.iloc[0].candidate
selection=dict(locked_utc=now(),candidate=best,parameters=params[best],selection_windows=list(ranges),ranking_rule='max min return, then max sum return, then ascending ID',candidate_results_sha256=sha(RESULTS/'candidates.csv'),space_sha256=sha(ROOT/'search_space.json'),w0_accessed=False)
(RESULTS/'selection.json').write_text(json.dumps(selection,indent=2))
print('LOCKED SELECTION',json.dumps(selection),flush=True)
old=pd.read_csv(PROJECT/'results/all_results.csv');comparison=[]
for name in ['A_b','C04']:
 for w in ranges:
  x=old[(old.candidate==name)&(old.window==w)].iloc[0]
  new=next(r for r in comparisons if r['candidate']==name and r['window']==w)
  bridge=next(r for r in comparisons if r['candidate']==name+'_TP_only' and r['window']==w)
  comparison.append(dict(strategy=name,window=w,old_return=x.return_pct,tp_only_return=bridge['return_pct'],canonical_return=new['return_pct'],tp_delta_pp=bridge['return_pct']-x.return_pct,add_clip_delta_pp=new['return_pct']-bridge['return_pct'],total_delta_pp=new['return_pct']-x.return_pct,old_dd=x.maxdd_pct,new_dd=new['maxdd_pct'],old_fees=x.fees,new_fees=new['fees'],new_account_n=new['account_n']))
pd.DataFrame(comparison).to_csv(RESULTS/'comparison.csv',index=False)

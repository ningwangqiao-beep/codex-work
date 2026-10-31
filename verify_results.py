from evaluate import ROOT,DATA
import pandas as pd,numpy as np,json

def read_csv(path):
 return pd.read_csv(path if path.exists() else type(path)(str(path)+'.gz'))

rows=[];examples=[]
frames=[read_csv(ROOT/'results'/x) for x in ['baseline.csv','anchor_replay.csv','optimization.csv','refinement.csv','structural.csv']]
all_results=pd.concat(frames,ignore_index=True)
all_results[['signal_n','signal_net']]=all_results[['signal_n','signal_net']].fillna(0)
assert len(all_results)==102 and all_results.groupby('candidate').size().eq(3).all()
for _,result in all_results.iterrows():
 name,w=result.candidate,result.window;a=DATA[w];folder=ROOT/'results'/name
 t=read_csv(folder/f'{w}_trades.csv');e=read_csv(folder/f'{w}_equity.csv');i=t.bar.astype(int).to_numpy();buy=np.where(t.kind<=1,t.side,-t.side)>0
 bad=np.where(buy,t.price.to_numpy()<a[i,3]-1e-8,t.price.to_numpy()>a[i,2]+1e-8)
 assert len(e)==len(a)
 assert abs(e.equity.iloc[-1]-10000*(1+result.return_pct/100))<1e-6
 assert abs(10000+(t.gross-t.fee).sum()+result.open_gross-e.equity.iloc[-1])<1e-5
 assert abs(t.fee.sum()-result.fees)<1e-6
 # Closed basket net is gross less all entry/addition fees and exit fee.
 for bid,basket in t.groupby('basket_id'):
  closed=basket[basket.kind>=2]
  if len(closed):assert abs((basket.gross-basket.fee).sum()-closed.basket_net.sum())<1e-6
 closed=(t[t.kind>=2].basket_net.sum()+result.open_gross-result.open_entry_fees)
 assert abs(closed-10000*result.return_pct/100)<1e-5
 peaks=np.maximum.accumulate(np.r_[10000.,e.equity.to_numpy()])[1:]
 assert abs(np.max(1.-e.equity.to_numpy()/peaks)*100-result.maxdd_pct)<1e-7
 # Frozen phases permit at most one TP per side per minute.
 assert not t[t.kind==2].duplicated(['bar','side']).any()
 if not name.startswith('Anchor'):assert bad.sum()==0,(name,w,'invalid fill')
 # At every close an optimized nonbankrupt account holds exactly two baskets.
 if name.startswith('C'):
  t['signed_qty']=np.where(t.kind<=1,t.qty,-t.qty)
  for side in [1.,-1.]:
   pos=t[t.side==side].groupby('bar').signed_qty.sum().reindex(range(len(a)),fill_value=0).cumsum()
   active=e.equity.to_numpy()>0
   assert (pos.to_numpy()[active]>1e-9).all(),(name,w,'missing basket')
 rows.append(dict(candidate=name,window=w,trades=len(t),favorable_outside_extreme=int(bad.sum()),outside_range=int(((t.price<a[i,3]-1e-8)|(t.price>a[i,2]+1e-8)).sum())))
 for idx in np.flatnonzero(bad)[:2]:
  x=t.iloc[idx].to_dict();x.update(candidate=name,window=w,bar_low=a[i[idx],3],bar_high=a[i[idx],2]);examples.append(x)
(ROOT/'results'/'fill_audit.json').write_text(json.dumps(dict(summary=rows,examples=examples),indent=2))
all_results.to_csv(ROOT/'results'/'all_results.csv',index=False)
print('PASS: 102 candidate-window runs; ledger, basket fees, drawdown, TP limit, favorable-fill bounds, and optimized dual baskets.')
print(pd.DataFrame(rows).query('favorable_outside_extreme>0').to_string(index=False))

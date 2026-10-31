from common import *
selection=json.loads((RESULTS/'selection.json').read_text());assert sha(RESULTS/'candidates.csv')==selection['candidate_results_sha256']
protocol=json.loads((RESULTS/'holdout_protocol.json').read_text());assert protocol['selection_sha256']==sha(RESULTS/'selection.json')
assert protocol['first_access_utc']>selection['locked_utc']
frames=[pd.read_csv(RESULTS/f) for f in ['measurement_runs.csv','candidates.csv','holdout.csv']]
allrows=pd.concat(frames,ignore_index=True);assert len(allrows)==86
assert set(frames[2].candidate)=={selection['candidate'],'C04'} and len(frames[2])==2
params=json.loads((ROOT/'search_space.json').read_text());data={w:load_window(w) for w in ['W1','W2','W3','W0']};audits=[]
for _,r in allrows.iterrows():
 name,w=r.candidate,r.window;a=data[w];out=RESULTS/name
 p=json.loads((out/f'{w}_parameters.json').read_text());t=pd.read_csv(out/f'{w}_trades.csv');e=pd.read_csv(out/f'{w}_equity.csv.gz').equity.to_numpy()
 i=t.bar.astype(int).to_numpy();lo=a[i,3];hi=a[i,2];adverse_bridge=name.endswith('_TP_only')
 outside=(t.price.to_numpy()<lo-1e-8)|(t.price.to_numpy()>hi+1e-8)
 if not adverse_bridge:assert not outside.any(),(name,w,'out of bar execution')
 assert (t.fee-t.notional*.0007).abs().max()<1e-8
 assert len(e)==len(a) and abs(e[-1]/10000*100-100-r.return_pct)<1e-7
 assert abs(10000+(t.gross-t.fee).sum()+r.open_gross-e[-1])<1e-5
 assert abs(t.fee.sum()-r.fees)<1e-6
 peaks=np.maximum.accumulate(np.r_[10000.,e])[1:];assert abs(np.max(1-e/peaks)*100-r.maxdd_pct)<1e-7
 assert not t[t.kind==2].duplicated(['bar','side']).any()
 for bid,basket in t.groupby('basket_id'):
  close=basket[basket.kind>=2]
  if len(close):assert abs((basket.gross-basket.fee).sum()-close.basket_net.sum())<1e-6
 # Independently reconstruct each TP target and each addition from the trade ledger.
 q={1.:0.,-1.:0.};cost={1.:0.,-1.:0.};last={1.:0.,-1.:0.};depth={1.:0,-1.:0};g=p.get('g',.01);tp=p.get('tp',.008);gap=0;clipped=0
 for j,x in t.iterrows():
  bar=int(x.bar);side=x.side;price=x.price;o,h,l,c=a[bar,1:5]
  if x.kind in [0,1]:
   if x.kind==0:q[side]=0.;cost[side]=0.;depth[side]=0
   else:
    grid=last[side]*(1-side*g)
    assert (l<=grid+1e-8) if side==1 else (h>=grid-1e-8)
    actual=grid if adverse_bridge else min(h,max(l,grid))
    assert abs(price-actual)<1e-7
    clipped+=int(not adverse_bridge and abs(actual-grid)>1e-8);depth[side]+=1
   q[side]+=x.qty;cost[side]+=x.notional;last[side]=price
  else:
   assert abs(q[side]-x.qty)<1e-7
   if x.kind==2:
    target=cost[side]/q[side]*(1+side*tp)
    assert (h>=target-1e-7) if side==1 else (l<=target+1e-7)
    expected=target if l<=target<=h else o
    assert abs(price-expected)<1e-6,(name,w,'TP fill',price,expected)
    gap+=int(not l<=target<=h)
    reopen=t.iloc[j+1];assert reopen.kind==0 and reopen.side==side and reopen.bar==bar and abs(reopen.price-price)<1e-8
   q[side]=0.;cost[side]=0.
 assert gap==r.tp_gap_n and clipped==r.add_clamp_n,(name,w,'gap counts')
 if name.startswith('R') or name=='C04':
  for side in [1.,-1.]:
   z=t[t.side==side];pos=pd.Series(np.where(z.kind<=1,z.qty,-z.qty),index=z.bar.astype(int)).groupby(level=0).sum().reindex(range(len(a)),fill_value=0).cumsum()
   assert (pos.to_numpy()[e>0]>1e-9).all()
 rr,dd,s,b,curve,_=run(a,**p)
 assert abs(rr*100-r.return_pct)<1e-8 and abs(dd*100-r.maxdd_pct)<1e-8 and np.allclose(curve,e,rtol=0,atol=1e-7)
 audits.append(dict(candidate=name,window=w,rows=len(t),tp_gap_n=gap,add_clamp_n=clipped,outside_range=int(outside.sum())))
# Frozen C04 appears as R11; source is unchanged across train and holdout.
candidates=frames[1]
for w in ['W1','W2','W3']:
 x=candidates[(candidates.candidate=='R11')&(candidates.window==w)].iloc[0];y=frames[0][(frames[0].candidate=='C04')&(frames[0].window==w)].iloc[0]
 assert all(abs(x[k]-y[k])<1e-8 for k in ['return_pct','maxdd_pct','fees','tp_n','ladder_n'])
assert json.loads((RESULTS/selection['candidate']/'W0_parameters.json').read_text())==selection['parameters']
assert json.loads((RESULTS/'C04/W0_parameters.json').read_text())==C04
pd.DataFrame(audits).to_csv(RESULTS/'execution_audit.csv',index=False)
allrows.to_csv(RESULTS/'all_results.csv',index=False)
(RESULTS/'verification.txt').write_text('PASS: all 86 runs, final-source replay, fee and basket ledgers, TP target/open fills, addition clipping, TP frequency, close drawdown, dual baskets, R11=C04, pre-holdout selection lock and identical holdout parameters.\n')
print((RESULTS/'verification.txt').read_text(),flush=True)

#!/usr/bin/env python3
"""Frozen AF-RV-01. Run from repository root: python af-rv-01/run_af_rv_01.py."""
import hashlib,json,platform
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'; W=720
KINDS=['dollar','volatility','rolling_beta','C1_ETH','C2_fixed_beta']
def load():
    bars=[pd.read_csv(ROOT/f'{s}usdt_um_1h.csv') for s in ['eth','btc']]
    funds=[pd.read_csv(ROOT/f'{s}usdt_um_funding.csv') for s in ['eth','btc']]
    assert all(len(b)==8016 for b in bars), 'bar count mismatch'
    assert all(len(f)==1002 for f in funds), 'funding count mismatch'
    assert bars[0].open_time.equals(bars[1].open_time), 'bar grid mismatch'
    t=bars[0].open_time.to_numpy()
    assert np.array_equal(t,np.arange(pd.Timestamp('2025-11-01',tz='UTC').value//10**6,pd.Timestamp('2026-10-01',tz='UTC').value//10**6,3600000)), 'invalid grid'
    for f in funds:
        ft=(f.calc_time.to_numpy()//3600000)*3600000
        assert np.array_equal(ft,np.arange(t[0],t[-1]+1,8*3600000)), 'funding settlement grid invalid'
    return bars,funds

def features(bars):
    e,b=[np.log(x.close) for x in bars]
    beta=e.rolling(W).cov(b)/b.rolling(W).var()
    spread=e-beta*b
    z=(spread-spread.rolling(W).mean())/spread.rolling(W).std()
    vol=np.column_stack([x.diff().rolling(W).std() for x in [e,b]])
    fix=float(np.cov(e.iloc[:W],b.iloc[:W],ddof=1)[0,1]/np.var(b.iloc[:W],ddof=1))
    return beta.to_numpy(),z.to_numpy(),vol,fix,spread.to_numpy()

def run(bars,funds,kind,stress=1.,liquidate=True):
    beta,z,vol,fix,spread=features(bars)
    n=len(bars[0]); times=bars[0].open_time.to_numpy(); op=np.column_stack([x.open for x in bars]); cl=np.column_stack([x.close for x in bars])
    fm=[dict(zip((f.calc_time//3600000)*3600000,f.last_funding_rate)) for f in funds]
    cash=1000.; q=np.zeros(2); pos=None; pending=None; cooldown=-1; trades=[]; eq=[]; ledger=[]
    fee=.0005*stress; slip=.0002*stress
    def close(i,px,reason):
        nonlocal cash,q,pos,cooldown
        fill=px*(1-np.sign(q)*slip); fees=np.abs(q)*fill*fee; gross=q*(fill-pos['entry_px'])
        cash+=float(sum(gross-fees))
        for leg in range(2): ledger.append({'ts':int(times[i]),'leg':leg,'fee':float(fees[leg]),'funding':0.})
        rec={k:v for k,v in pos.items() if k not in ['entry_px','funding','fees']}
        rec.update(exit_ts=int(times[i]),exit_reason=reason,holding_hours=(times[i]-pos['entry_ts'])/3600000,gross_pnl=float(sum(gross)),fees=float(sum(fees)+sum(pos['fees'])),funding_eth=float(pos['funding'][0]),funding_btc=float(pos['funding'][1]))
        rec['net_pnl']=rec['gross_pnl']-rec['fees']+rec['funding_eth']+rec['funding_btc']
        for j,name in enumerate(['eth','btc']): rec.update({f'{name}_qty':float(q[j]),f'{name}_entry_px':float(pos['entry_px'][j]),f'{name}_exit_px':float(fill[j])})
        trades.append(rec); q=np.zeros(2); pos=None; cooldown=i+24
    for i in range(n):
        if pending:
            action,reason,sig=pending; pending=None
            if action=='exit': close(i,op[i],reason)
            else:
                h=beta[sig] if kind=='rolling_beta' else fix
                weights=np.array([.5,.5])
                if kind=='volatility': weights=1/vol[sig]; weights/=weights.sum()
                elif kind in ['rolling_beta','C2_fixed_beta']: weights=np.array([1.,h])/(1+h)
                elif kind=='C1_ETH': weights=np.array([1.,0.])
                assert np.isfinite(weights).all() and (weights>=0).all()
                direction=-1 if z[sig]>=2 else 1
                fill=op[i]*(1+np.array([direction,-direction])*slip)
                notion=cash*weights; fees=notion*fee
                q=np.array([direction,-direction])*notion/fill; cash-=sum(fees)
                pos={'entry_ts':int(times[i]),'signal_ts':int(times[sig]),'entry_index':i,'side':direction,'beta':float(beta[sig]),'entry_px':fill,'fees':fees,'funding':np.zeros(2),'eth_weight':float(weights[0])}
                for j in range(2): ledger.append({'ts':int(times[i]),'leg':j,'fee':float(fees[j]),'funding':0.})
        if pos:
            for j in range(2):
                delta=-q[j]*op[i,j]*fm[j].get(times[i],0.)
                cash+=delta; pos['funding'][j]+=delta
                if times[i] in fm[j]: ledger.append({'ts':int(times[i]),'leg':j,'fee':0.,'funding':float(delta)})
        eq.append(float(cash+sum(q*(cl[i]-pos['entry_px']))) if pos else float(cash))
        if pos:
            reason='take_profit' if abs(z[i])<=.5 else 'stop_loss' if abs(z[i])>=3.5 else 'timeout' if i-pos['entry_index']+1>=48 else None
            if reason: pending=('exit',reason,i)
        elif i>=W and i>=cooldown and np.isfinite(z[i]) and abs(z[i])>=2:
            pending=('entry',None,i)
    if pos and liquidate:
        close(n-1,cl[-1],'end_of_data'); eq[-1]=float(cash)
    return np.array(eq),trades,ledger

def ms(s): return pd.Timestamp(s,tz='UTC').value//10**6
SEG={'IS':(ms('2025-12-01'),ms('2026-06-01')),'OOS':(ms('2026-06-01'),ms('2026-10-01')),'ALL':(ms('2025-12-01'),ms('2026-10-01'))}
def metrics(times,eq,tr,ledger,a,b):
    idx=np.flatnonzero((times>=a)&(times<b)); start=eq[idx[0]-1] if idx[0] else 1000.; curve=np.r_[start,eq[idx]]
    tt=[t for t in tr if a<=t['exit_ts']<b]; pn=np.array([t['net_pnl'] for t in tt]); ll=[x for x in ledger if a<=x['ts']<b]
    gains=pn[pn>0].sum(); loss=-pn[pn<0].sum()
    return dict(net_return_pct=(curve[-1]/start-1)*100,max_drawdown_pct=float(max(1-curve/np.maximum.accumulate(curve))*100),profit_factor=float(gains/loss) if loss else None,closed_trades=len(tt),win_rate_pct=float((pn>0).mean()*100) if len(pn) else 0.,total_fees=sum(x['fee'] for x in ll),funding_eth=sum(x['funding'] for x in ll if x['leg']==0),funding_btc=sum(x['funding'] for x in ll if x['leg']==1),average_holding_hours=float(np.mean([t['holding_hours'] for t in tt])) if tt else 0.,exit_reasons={r:sum(t['exit_reason']==r for t in tt) for r in ['take_profit','stop_loss','timeout','end_of_data']},start_equity=float(start),end_equity=float(curve[-1]),closed_net_pnl=float(pn.sum()))
def bootstrap(tr):
    sums=np.zeros(4)
    for t in tr:
        if SEG['OOS'][0]<=t['exit_ts']<SEG['OOS'][1]: sums[pd.Timestamp(t['exit_ts'],unit='ms',tz='UTC').month-6]+=t['net_pnl']
    rng=np.random.default_rng(42); samples=sums[rng.integers(0,4,size=(2000,4))].sum(axis=1)
    return {'monthly_net_pnl':sums.tolist(),'ci95_usdt':np.quantile(samples,[.025,.975]).tolist(),'replicates':2000,'seed':42}
def main():
    bars,funds=load(); OUT.mkdir(exist_ok=True); times=bars[0].open_time.to_numpy(); results={}; audit=[]
    for kind in KINDS:
        eq,tr,ledger=run(bars,funds,kind)
        for fraction in [.5,.75]:
            n=int(len(times)*fraction); cutbars=[b.iloc[:n].copy() for b in bars]; cutfunds=[f[(f.calc_time//3600000)*3600000<=times[n-1]].copy() for f in funds]
            _,short,_=run(cutbars,cutfunds,kind,liquidate=False)
            expected=[t for t in tr if t['exit_ts']<=times[n-1] and t['exit_reason']!='end_of_data']
            assert short==expected, f'causal audit failed: {kind} {fraction}'
            audit.append(dict(construction=kind,fraction=fraction,closed_trades=len(short),exact_match=True))
        results[kind]={seg:metrics(times,eq,tr,ledger,*bounds) for seg,bounds in SEG.items()}
        seq,st,sl=run(bars,funds,kind,1.5)
        for fraction in [.5,.75]:
            n=int(len(times)*fraction)
            _,short,_=run([b.iloc[:n].copy() for b in bars],[f[(f.calc_time//3600000)*3600000<=times[n-1]].copy() for f in funds],kind,1.5,liquidate=False)
            expected=[t for t in st if t['exit_ts']<=times[n-1] and t['exit_reason']!='end_of_data']
            assert short==expected, f'stress causal audit failed: {kind} {fraction}'
            audit.append(dict(construction=kind,stress_multiplier=1.5,fraction=fraction,closed_trades=len(short),exact_match=True))
        results[kind]['stress_OOS']=metrics(times,seq,st,sl,*SEG['OOS']); results[kind]['bootstrap']=bootstrap(tr)
        pd.DataFrame(tr).to_csv(OUT/f'{kind}_trades.csv',index=False,float_format='%.17g')
        pd.DataFrame(st).to_csv(OUT/f'{kind}_stress_trades.csv',index=False,float_format='%.17g')
        pd.DataFrame({'open_time':times,'equity':eq,'stress_equity':seq}).to_csv(OUT/f'{kind}_equity.csv',index=False,float_format='%.17g')
        pd.DataFrame(ledger).to_csv(OUT/f'{kind}_cashflows.csv',index=False,float_format='%.17g')
    for kind in KINDS[:3]:
        r=results[kind]; o=r['OOS']
        rules=[o['net_return_pct']>0 and o['closed_net_pnl']>max(0,results['C1_ETH']['OOS']['closed_net_pnl'],results['C2_fixed_beta']['OOS']['closed_net_pnl']),o['profit_factor'] is not None and o['profit_factor']>=1.2,o['max_drawdown_pct']<=10,r['bootstrap']['ci95_usdt'][0]>0,r['stress_OOS']['net_return_pct']>0,r['IS']['net_return_pct']>0]
        r['six_rules']=[bool(v) for v in rules]; r['sample_minimum']=o['closed_trades']>=30; r['verdict']='候选' if all(rules) and r['sample_minimum'] else '不通过'
    beta,z,vol,fix,spread=features(bars); valid=spread[np.isfinite(spread)]; lag=valid[:-1]; change=np.diff(valid); slope=np.linalg.lstsq(np.column_stack([np.ones(len(lag)),lag]),change,rcond=None)[0][1]
    desc={'beta_min':float(np.nanmin(beta)),'beta_max':float(np.nanmax(beta)),'beta_mean':float(np.nanmean(beta)),'beta_fixed':fix,'half_life_hours':float(-np.log(2)/slope) if slope<0 else None,'half_life_ols_delta_s_on_lag_s_slope':float(slope),'first_valid_z_utc':str(pd.Timestamp(times[np.flatnonzero(np.isfinite(z))[0]],unit='ms',tz='UTC'))}
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'AF-RV-01_PREREG.md',*ROOT.glob('*.py'),*ROOT.glob('*.csv')]}
    final={'experiment':'AF-RV-01','data_validation':{'status':'PASS','bars_per_leg':8016,'settlements_per_leg':1002,'aligned_hourly_grid':True,'funding_timestamp_jitter_records':[int((f.calc_time%3600000!=0).sum()) for f in funds],'funding_max_jitter_ms':[int((f.calc_time%3600000).max()) for f in funds]},'audit':audit,'descriptive':desc,'results':results,'conclusion':'任一通过' if any(results[k]['verdict']=='候选' for k in KINDS[:3]) else 'NOT_SUPPORTED','hashes':hashes,'versions':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__}}
    pd.DataFrame({'open_time':times,'beta':beta,'spread':spread,'z':z,'vol_eth':vol[:,0],'vol_btc':vol[:,1]}).to_csv(OUT/'signals.csv',index=False,float_format='%.17g')
    (OUT/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    (OUT/'results.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(final,ensure_ascii=False,indent=2))
if __name__=='__main__': main()

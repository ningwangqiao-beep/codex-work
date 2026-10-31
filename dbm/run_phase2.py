#!/usr/bin/env python3
"""Phase two: frozen fills, close-boundary cycle settlement, fixed 54-point grid."""
import concurrent.futures
import csv
import datetime as dt
import hashlib
import inspect
import io
import itertools
import json
import math
from pathlib import Path
import subprocess
import zipfile
import backtest as bt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dbm/results/phase2'
CACHE = ROOT / 'work'
BASELINE = 'cc63799b55f04b58493760a9e24283a6a23cabd3'
START = int(dt.datetime(2026, 5, 1, tzinfo=dt.timezone.utc).timestamp())
END = int(dt.datetime(2026, 10, 31, 17, 5, tzinfo=dt.timezone.utc).timestamp())

def save(name, rows):
    bt.writecsv(OUT / name, rows, list(rows[0]))

def load():
    report = dict(valid=False, baseline=BASELINE, expected_bars=264545,
                  window_start_utc=bt.iso(START), window_end_exclusive_utc=bt.iso(END))
    try:
        def month(m):
            key=f'monthly/klines/ETHUSDT/1m/ETHUSDT-1m-2026-{m:02}.zip'
            r, rows = bt.fetch(key, CACHE)
            assert r.get('checksum_ok') and not r.get('error'), r
            parsed=[]
            for row in rows:
                stamp=int(row[0]); scale=1000000 if stamp>10**14 else 1000
                assert stamp % (60*scale)==0 and int(row[6])==stamp+60*scale-1
                assert float(row[5])>=0 and int(row[8])>=0
                parsed.append((stamp//scale, *map(float,row[1:5])))
            first=int(dt.datetime(2026,m,1,tzinfo=dt.timezone.utc).timestamp())
            last=int(dt.datetime(2026,m+1,1,tzinfo=dt.timezone.utc).timestamp())
            assert [b[0] for b in parsed]==list(range(first,last,60))
            r['rows']=len(parsed)
            return r,parsed
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            downloaded=list(pool.map(month, range(5,9)))
        report['archives']=[r for r,_ in downloaded]
        bars=[b for _,bs in downloaded for b in bs]
        path=ROOT/'dbm/results/window_87425/input_bars.csv'
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        pinned=json.loads((path.parent/'validation.json').read_text())['input_sha256']
        assert sha==pinned
        old=[(int(dt.datetime.fromisoformat(r['open_time_utc'].replace('Z','+00:00')).timestamp()),
              *[float(r[k]) for k in ('open','high','low','close')]) for r in csv.DictReader(path.open())]
        assert len(old)==87425
        report['reused_input_sha256']=sha
        bars.extend(old)
        assert len(bars)==264545
        assert [b[0] for b in bars]==list(range(START,END,60))
        for t,o,h,l,c in bars:
            assert all(math.isfinite(x) and x>0 for x in (o,h,l,c))
            assert l<=min(o,c)<=max(o,c)<=h
        seams=[]
        for prev,cur in zip(bars,bars[1:]):
            if bt.iso(cur[0])[8:19]=='01T00:00:00':
                seams.append(dict(previous_open_utc=bt.iso(prev[0]),next_open_utc=bt.iso(cur[0]),
                                  previous_close=prev[4],next_open=cur[1],gap=cur[1]-prev[4],continuous=cur[0]-prev[0]==60))
        report.update(valid=True, available_bars=len(bars),duplicate_count=0,missing_count=0,ohlc_valid=True,seams=seams)
        save('input_bars.csv',[dict(open_time_utc=bt.iso(t),open=o,high=h,low=l,close=c) for t,o,h,l,c in bars])
        report['input_sha256']=hashlib.sha256((OUT/'input_bars.csv').read_bytes()).hexdigest()
    except Exception as e:
        report['error']=repr(e)
        (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
        raise SystemExit('DATA INVALID: no strategy run: '+repr(e))
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    return bars

def engine():
    """Keep the baseline body verbatim except the explicit cycle boundary hook.

    The hook is after trading and before close statistics/daily reporting.
    Existing BUST liquidation is untouched. DOUBLED liquidates at that close
    using the identical close() implementation, including its sell fee.
    """
    frozen=subprocess.check_output(['git','show',BASELINE+':dbm/backtest.py'],cwd=ROOT,text=True)
    assert (ROOT/'dbm/backtest.py').read_text()==frozen
    source=inspect.getsource(bt.simulate)
    old='        peak=max(peak,equity); mdd=max(mdd,1-equity/peak)'
    source=source.replace(old,"""        terminal = busted is not None or doubled is not None
        trigger_equity = equity
        if doubled is not None and basket is not None:
            close(c,t+60,'CYCLE_DOUBLED')
            equity=cash
        record(t, equity, fees, terminal, trigger_equity)
"""+old)
    marker='    if basket is not None:\n        basket.update'
    assert source.count(marker)==1
    source=source.replace(marker,"        if terminal: break\n"+marker)
    source=source.replace('if (t+60)%86400==0 or t == bars[-1][0]:',
                          'if (t+60)%86400==0 or t == bars[-1][0] or terminal:')
    namespace=dict(bt.__dict__)
    exec(source,namespace)
    return namespace

def run(name, params, bars, ns, detail=False):
    cycles=[]; baskets=[]; fills=[]; daily=[]; minimum=(10000.,1,bt.iso(START))
    injected=recovered=fees_total=0.; index=0; days={}
    while index<len(bars):
        cid=len(cycles)+1; start=bars[index][0]; injected+=10000
        capture={}; points=[]
        ns.update(START=start,PARAMS={name:params},writecsv=lambda p,rows,fields: capture.update({p.name:rows}),
                  record=lambda *args: points.append(args))
        summary=ns['simulate'](name,bars[index:],OUT)
        for t,e,f,terminal,trigger in points:
            if e<minimum[0]: minimum=(e,cid,bt.iso(t+60))
            if (t+60)%86400==0 or t+60==END:
                days[bt.iso(t)[:10]]=dict(date_utc=bt.iso(t)[:10],close_time_utc=bt.iso(t+60),
                    cycle_id=cid,active_cycle_equity=e,total_injected=injected,
                    settled_recoveries=recovered,stitched_equity=recovered+e,
                    cumulative_net_pnl=recovered+e-injected,total_fees=fees_total+f)
        t,e,f,terminal,trigger=points[-1]; end=t+60
        outcome='BUSTED' if summary['BUSTED'] else 'DOUBLED' if summary['DOUBLED'] else 'OPEN_AT_END'
        cycles.append(dict(cycle_id=cid,start_utc=bt.iso(start),end_utc=bt.iso(end),result=outcome,
                           trigger_equity=trigger,settlement_equity=e,injection=10000.,net_pnl=e-10000,
                           duration_days=(end-start)/86400,total_fees=f))
        if detail:
            for suffix,dest in [('baskets',baskets),('fills',fills)]:
                dest.extend(dict(cycle_id=cid,**r) for r in capture[name+'_'+suffix+'.csv'])
        recovered+=e;fees_total+=f;index+=len(points)
    result=dict(variant=name,B=params[0],g=params[1],A=params[2],tp=params[3],cycles=len(cycles),
        DOUBLED=sum(c['result']=='DOUBLED' for c in cycles),BUSTED=sum(c['result']=='BUSTED' for c in cycles),
        OPEN_AT_END=sum(c['result']=='OPEN_AT_END' for c in cycles),total_injected=injected,
        total_recovered=recovered,net_pnl=recovered-injected,
        average_cycle_days=sum(c['duration_days'] for c in cycles)/len(cycles),
        longest_cycle_days=max(c['duration_days'] for c in cycles),total_fees=fees_total,
        minimum_equity=minimum[0],minimum_cycle=minimum[1],minimum_time_utc=minimum[2])
    assert index==len(bars) and abs(sum(c['net_pnl'] for c in cycles)-result['net_pnl'])<1e-6
    if detail:
        save(name+'_cycles.csv',cycles);save(name+'_baskets.csv',baskets);save(name+'_fills.csv',fills)
        save(name+'_daily_equity.csv',list(days.values()))
        save(name+'_daily_net_pnl.csv',[{k:r[k] for k in ('date_utc','close_time_utc','total_injected','cumulative_net_pnl')} for r in days.values()])
        assert abs(sum(r['fee'] for r in fills)-fees_total)<1e-6
        assert abs(sum(r['pnl_net'] for r in baskets)-result['net_pnl'])<1e-6
    return result,cycles

def main():
    OUT.mkdir(parents=True,exist_ok=True);CACHE.mkdir(exist_ok=True)
    bars=load();print('DATA VALID: 264545 bars',flush=True);ns=engine()
    baseline=[]
    for name,p in bt.PARAMS.items():
        r,_=run(name,p,bars,ns,True);baseline.append(r);print(json.dumps(r),flush=True)
    save('baseline_summary.csv',baseline)
    grid=[];settlements={}
    for i,p in enumerate(itertools.product((.15,.20,.25),(.005,.006,.008),(7,8),(.005,.006,.008)),1):
        name=f'G{i:02}';r,cs=run(name,p,bars,ns);grid.append(r);settlements[name]=cs
        print(name,r['net_pnl'],flush=True)
    grid.sort(key=lambda r:(-r['net_pnl'],-r['DOUBLED']))
    for rank,r in enumerate(grid,1):r['rank']=rank
    save('grid_54_summary.csv',grid)
    for r in grid[:10]:save(f"rank_{r['rank']:02}_{r['variant']}_cycles.csv",settlements[r['variant']])
    v2=next(r for r in grid if (r['B'],r['g'],r['A'],r['tp'])==bt.PARAMS['V2'])
    assert all(v2[k]==baseline[2][k] for k in baseline[2] if k!='variant')
    (OUT/'summary.json').write_text(json.dumps(dict(baseline=baseline,top10=grid[:10]),indent=2)+'\n')
    print('COMPLETE',flush=True)

if __name__=='__main__':main()

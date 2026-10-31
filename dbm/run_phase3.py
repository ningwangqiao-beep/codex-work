#!/usr/bin/env python3
"""Four prespecified OOS configurations; reuse phase-two execution verbatim."""
import concurrent.futures
import datetime as dt
import hashlib
import json
import math
import subprocess
import run_phase2 as p

PIN = 'd0bbcb38ff62557a0289377b57c892f5a0d0f472'
CONFIGS = {'G10':(.15,.006,8,.005), 'G16':(.15,.008,8,.005),
           'G33':(.20,.008,7,.008), 'V2':(.20,.006,8,.006)}
p.OUT = p.ROOT/'dbm/results/phase3'
p.START = int(dt.datetime(2025,11,1,tzinfo=dt.timezone.utc).timestamp())
p.END = int(dt.datetime(2026,5,1,tzinfo=dt.timezone.utc).timestamp())

def load():
    report = dict(valid=False,phase2_commit=PIN,expected_bars=260640,
                  window_start_utc=p.bt.iso(p.START),window_end_exclusive_utc=p.bt.iso(p.END))
    try:
        def month(ym):
            y,m=ym
            r,rows=p.bt.fetch(f'monthly/klines/ETHUSDT/1m/ETHUSDT-1m-{y}-{m:02}.zip',p.CACHE)
            assert r.get('checksum_ok') and not r.get('error'),r
            first=int(dt.datetime(y,m,1,tzinfo=dt.timezone.utc).timestamp())
            ny,nm=(y+1,1) if m==12 else (y,m+1)
            end=int(dt.datetime(ny,nm,1,tzinfo=dt.timezone.utc).timestamp())
            bars=[]
            for row in rows:
                stamp=int(row[0]);scale=1000000 if stamp>10**14 else 1000
                assert stamp%(60*scale)==0 and int(row[6])==stamp+60*scale-1
                assert float(row[5])>=0 and int(row[8])>=0
                b=(stamp//scale,*map(float,row[1:5]))
                _,o,h,l,c=b
                assert all(math.isfinite(x) and x>0 for x in (o,h,l,c))
                assert l<=min(o,c)<=max(o,c)<=h
                bars.append(b)
            assert [b[0] for b in bars]==list(range(first,end,60))
            r.update(rows=len(bars),first_open_utc=p.bt.iso(first),last_open_utc=p.bt.iso(end-60))
            return r,bars
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            months=list(pool.map(month,[(2025,11),(2025,12),(2026,1),(2026,2),(2026,3),(2026,4)]))
        report['archives']=[r for r,_ in months]
        bars=[b for _,bs in months for b in bs]
        assert len(bars)==260640
        assert [b[0] for b in bars]==list(range(p.START,p.END,60))
        seams=[]
        for (_,left),(_,right) in zip(months,months[1:]):
            a,b=left[-1],right[0]
            assert b[0]-a[0]==60
            seams.append(dict(previous_open_utc=p.bt.iso(a[0]),next_open_utc=p.bt.iso(b[0]),
                              previous_close=a[4],next_open=b[1],price_gap=b[1]-a[4],continuous=True))
        p.save('input_bars.csv',[dict(open_time_utc=p.bt.iso(t),open=o,high=h,low=l,close=c) for t,o,h,l,c in bars])
        report.update(valid=True,available_bars=len(bars),duplicate_count=0,missing_count=0,ohlc_valid=True,seams=seams,
                      input_sha256=hashlib.sha256((p.OUT/'input_bars.csv').read_bytes()).hexdigest())
    except Exception as e:
        report['error']=repr(e)
        (p.OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
        raise SystemExit('DATA INVALID: no strategy run: '+repr(e))
    (p.OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    return bars

def main():
    p.OUT.mkdir(parents=True,exist_ok=True);p.CACHE.mkdir(exist_ok=True)
    for file in ('dbm/backtest.py','dbm/run_phase2.py','dbm/verify_phase2.py'):
        assert (p.ROOT/file).read_bytes()==subprocess.check_output(['git','show',PIN+':'+file],cwd=p.ROOT)
    bars=load();print('DATA VALID: 260640 bars; six checksums and five seams verified',flush=True)
    ns=p.engine();results=[]
    for name,params in CONFIGS.items():
        r,cs=p.run(name,params,bars,ns,True)
        doubled=[c['settlement_equity']-10000 for c in cs if c['result']=='DOUBLED']
        busted=[10000-c['settlement_equity'] for c in cs if c['result']=='BUSTED']
        r['average_doubled_settlement_surplus']=sum(doubled)/len(doubled) if doubled else None
        r['average_busted_settlement_loss']=sum(busted)/len(busted) if busted else None
        results.append(r);print(json.dumps(r),flush=True)
    p.save('summary.csv',results)
    (p.OUT/'summary.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main()

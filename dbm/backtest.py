#!/usr/bin/env python3
"""Frozen DBM parameters. Standard library only; validation gates simulation."""
import argparse, concurrent.futures, csv, datetime as dt, hashlib, io, json, math
from pathlib import Path
import urllib.error, urllib.request, zipfile

UTC = dt.timezone.utc
START = int(dt.datetime(2026, 9, 1, tzinfo=UTC).timestamp())
END = int(dt.datetime(2026, 11, 1, tzinfo=UTC).timestamp())
FEE = .0007
PARAMS = {'V0': (.06,.008,7,.007), 'V1': (.12,.008,7,.007), 'V2': (.20,.006,8,.006)}
BASE = 'https://data.binance.vision/data/spot/'

def iso(t):
    return dt.datetime.fromtimestamp(t, UTC).isoformat().replace('+00:00','Z')

def writecsv(path, rows, fields):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fields); w.writeheader(); w.writerows(rows)

def fetch(key, cache):
    p = cache / key.rsplit('/',1)[-1]
    result = {'url': BASE+key}
    try:
        if not p.exists():
            with urllib.request.urlopen(BASE+key, timeout=45) as r: data = r.read()
            p.write_bytes(data)
        data = p.read_bytes()
        result.update(status=200, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        # Verify the publisher's checksum, in addition to ZIP CRC.
        cp = Path(str(p)+'.CHECKSUM')
        if not cp.exists():
            with urllib.request.urlopen(BASE+key+'.CHECKSUM', timeout=45) as r: cp.write_bytes(r.read())
        result['checksum_ok'] = cp.read_text().split()[0] == result['sha256']
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            if z.testzip() is not None: raise ValueError('ZIP CRC failed')
            rows = list(csv.reader(io.StringIO(z.read(z.namelist()[0]).decode())))
        return result, rows
    except urllib.error.HTTPError as e:
        result.update(status=e.code, error=str(e))
    except Exception as e: result['error'] = str(e)
    return result, []

def validate(cache, out):
    downloads, raw = [], []
    for month, ndays in [('09',30),('10',31)]:
        key=f'monthly/klines/ETHUSDT/1m/ETHUSDT-1m-2026-{month}.zip'
        report, rows = fetch(key,cache); downloads.append(report)
        if report.get('status')==404:
            keys=[f'daily/klines/ETHUSDT/1m/ETHUSDT-1m-2026-{month}-{d:02}.zip' for d in range(1,ndays+1)]
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                for rep, rs in pool.map(lambda k: fetch(k,cache), keys):
                    downloads.append(rep); raw.extend(rs)
        else: raw.extend(rows)
    bars, errors, seen = [], [], set()
    for index, r in enumerate(raw):
        try:
            stamp=int(r[0]); scale=1000000 if stamp>10**14 else 1000
            if stamp % (60*scale): raise ValueError('unaligned open timestamp')
            t=stamp//scale
            if t in seen: raise ValueError('duplicate timestamp '+iso(t))
            seen.add(t)
            if not START<=t<END: raise ValueError('outside window '+iso(t))
            o,h,l,c=map(float,r[1:5])
            if not all(math.isfinite(x) and x>0 for x in (o,h,l,c)): raise ValueError('invalid price')
            if not l<=min(o,c)<=max(o,c)<=h: raise ValueError('invalid OHLC ordering')
            if int(r[6]) != stamp+60*scale-1: raise ValueError('invalid close timestamp')
            if float(r[5])<0 or int(r[8])<0: raise ValueError('negative volume/trades')
            bars.append((t,o,h,l,c))
        except Exception as e: errors.append({'row':index,'error':str(e)})
    bars.sort()
    missing=[{'open_time_utc':iso(t)} for t in range(START,END,60) if t not in seen]
    writecsv(out/'missing_minutes.csv',missing,['open_time_utc'])
    daily=[]
    for t in range(START,END,86400):
        n=sum(t<=b[0]<t+86400 for b in bars)
        daily.append({'date_utc':iso(t)[:10],'expected':1440,'available':n,'missing':1440-n})
    writecsv(out/'data_daily_audit.csv',daily,['date_utc','expected','available','missing'])
    ok=len(bars)==87840 and not missing and not errors and all(x.get('checksum_ok') for x in downloads if x.get('status')==200) and not any(x.get('error') and x.get('status')!=404 for x in downloads)
    report={'valid':ok,'expected_bars':87840,'available_bars':len(bars),'missing_count':len(missing),'errors':errors,'downloads':downloads,'first_available':iso(bars[0][0]) if bars else None,'last_available':iso(bars[-1][0]) if bars else None}
    (out/'validation.json').write_text(json.dumps(report,indent=2))
    return ok,bars,report

def simulate(name, bars, out):
    B,g,A,tp=PARAMS[name]
    cash=10000.; qty=cost=fees=0.; basket=None; baskets=[]; fills=[]; daily=[]
    doubled=busted=None; peak=low=10000.; low_time=iso(START); mdd=0.; max_notional=0.; max_ratio=0.; max_n_time=None; max_n_ratio=None
    def exposure(price,t):
        nonlocal max_notional,max_ratio,max_n_time,max_n_ratio
        n=qty*price; e=cash+n
        if cost>max_notional:
            max_notional=cost; max_n_time=iso(t); max_n_ratio=100*cost/e if e>0 else None
        if e>0: max_ratio=max(max_ratio,100*n/e)
    def buy(price,notional,t,kind):
        nonlocal cash,qty,cost,fees
        fee=notional*FEE; cash-=notional+fee; qty+=notional/price; cost+=notional; fees+=fee
        entry={'time_utc':iso(t),'kind':kind,'price':price,'notional':notional,'fee':fee}
        basket['buys'].append(entry); fills.append(dict(basket_id=basket['basket_id'],**entry))
        exposure(price,t)
    def close(price,t,reason):
        nonlocal cash,qty,cost,fees,basket
        proceeds=qty*price; fee=proceeds*FEE; fees+=fee; cash+=proceeds-fee
        fills.append({'basket_id':basket['basket_id'],'time_utc':iso(t),'kind':reason,'price':price,'notional':proceeds,'fee':fee})
        basket.update(close_time_utc=iso(t),close_price=price,close_reason=reason,pnl_net=cash-basket['starting_equity'],fees=fees-basket['starting_fees'],add_count=len(basket['buys'])-1,buys_json=json.dumps(basket.pop('buys')))
        baskets.append(basket); basket=None; qty=cost=0.
    for t,o,h,l,c in bars:
        if busted is None:
            if basket is None:
                basket={'basket_id':len(baskets)+1,'open_time_utc':iso(t),'starting_equity':cash,'starting_fees':fees,'buys':[]}
                base=cash*B; last=o; adds=0; buy(o,base,t,'BASE')
            while adds<A and l<=last*(1-g):
                price=min(o,last*(1-g)); adds+=1
                buy(price,base*2**adds,t,'ADD_'+str(adds)); last=price
            # Strictly below the final grid, matching "被跌破". Stop overrides TP.
            if adds==A and l<last*(1-g):
                exposure(c,t+60); close(c,t+60,'STAIR_STOP')
            else:
                target=cost/qty*(1+tp)
                if h>=target:
                    price=max(o,target); exposure(price,t); close(price,t,'TAKE_PROFIT')
            equity=cash+qty*c
            if equity<=2000:
                busted=iso(t+60)
                if basket is not None: close(c,t+60,'BUST')
                equity=cash
            elif equity>=20000 and doubled is None: doubled=iso(t+60)
        else: equity=cash
        peak=max(peak,equity); mdd=max(mdd,1-equity/peak)
        if equity<low: low=equity; low_time=iso(t+60)
        if qty: exposure(c,t+60)
        if (t+60)%86400==0 or t == bars[-1][0]:
            daily.append({'date_utc':iso(t)[:10],'close_time_utc':iso(t+60),'equity':equity,'cash':cash,'quantity':qty,'close_price':c,'fees_cumulative':fees,'status':'BUSTED' if busted else 'ACTIVE'})
    if basket is not None:
        basket.update(close_time_utc='',close_price='',close_reason='OPEN_AT_END',pnl_net=equity-basket['starting_equity'],fees=fees-basket['starting_fees'],add_count=adds,buys_json=json.dumps(basket.pop('buys')))
        baskets.append(basket)
    writecsv(out/f'{name}_daily_equity.csv',daily,list(daily[0]))
    writecsv(out/f'{name}_baskets.csv',baskets,['basket_id','open_time_utc','starting_equity','starting_fees','close_time_utc','close_price','close_reason','pnl_net','fees','add_count','buys_json'])
    writecsv(out/f'{name}_fills.csv',fills,['basket_id','time_utc','kind','price','notional','fee'])
    return {'variant':name,'DOUBLED':doubled,'BUSTED':busted,'race':'DOUBLED' if doubled and (not busted or doubled<busted) else 'BUSTED' if busted else 'NEITHER','final_equity':equity,'max_drawdown_pct':100*mdd,'minimum_equity':low,'minimum_time_utc':low_time,'baskets':len(baskets),'take_profit_count':sum(b['close_reason']=='TAKE_PROFIT' for b in baskets),'stair_stop_count':sum(b['close_reason']=='STAIR_STOP' for b in baskets),'peak_total_entry_notional':max_notional,'equity_pct_at_peak_total_entry_notional':max_n_ratio,'peak_position_notional_time_utc':max_n_time,'peak_notional_equity_pct':max_ratio,'total_fees':fees}

def main():
    p=argparse.ArgumentParser();p.add_argument('--cache',type=Path,default=Path('work/data'));p.add_argument('--out',type=Path,default=Path('results'));a=p.parse_args()
    a.cache.mkdir(parents=True,exist_ok=True);a.out.mkdir(parents=True,exist_ok=True)
    ok,bars,report=validate(a.cache,a.out)
    print(json.dumps({k:v for k,v in report.items() if k!='downloads'},indent=2))
    if not ok: raise SystemExit('DATA INVALID: no strategy was run; no result CSVs generated.')
    results=[simulate(n,bars,a.out) for n in PARAMS]
    (a.out/'summary.json').write_text(json.dumps(results,indent=2)); print(json.dumps(results,indent=2))
if __name__=='__main__': main()

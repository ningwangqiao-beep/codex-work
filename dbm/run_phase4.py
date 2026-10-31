#!/usr/bin/env python3
"""Frozen phase-four bidirectional DBM; no market-data network access."""
import csv
import datetime as dt
import hashlib
import json
import math
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'dbm/results/phase4'
FEE=.0007
CONFIGS={'V2-bi':(.20,.006,8,.006),'G10-bi':(.15,.006,8,.005)}
PINS={'W1':('phase2','d0bbcb38ff62557a0289377b57c892f5a0d0f472',264545,'260c2d1d9d56a8d4ba54e9f986afc8613d3645f8f7949fa5ea075cce55658149'),
      'W2':('phase3','a1aeba7862ff504ae03d48d32bc4210c4c092a6d',260640,'fbb9bbdb4f8c4f0311480b6295190325988940d1b37f29a63eecc3688e32a2a8')}
def iso(t):return dt.datetime.fromtimestamp(t,dt.timezone.utc).isoformat().replace('+00:00','Z')
def save(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def load(window):
    phase,pin,n,sha=PINS[window];p=f'dbm/results/{phase}/input_bars.csv'
    raw=(ROOT/p).read_bytes()
    assert raw==subprocess.check_output(['git','show',f'{pin}:{p}'],cwd=ROOT)
    manifest=json.loads(subprocess.check_output(['git','show',f'{pin}:dbm/results/{phase}/manifest.json'],cwd=ROOT))
    actual=hashlib.sha256(raw).hexdigest();assert actual==sha==manifest[p], 'DATA HASH MISMATCH'
    rows=list(csv.DictReader(raw.decode().splitlines()));assert len(rows)==n,'DATA COUNT MISMATCH'
    bars=[(int(dt.datetime.fromisoformat(r['open_time_utc'].replace('Z','+00:00')).timestamp()),*[float(r[k]) for k in ('open','high','low','close')]) for r in rows]
    start=int(dt.datetime(2026,5,1,tzinfo=dt.timezone.utc).timestamp()) if window=='W1' else int(dt.datetime(2025,11,1,tzinfo=dt.timezone.utc).timestamp())
    assert [b[0] for b in bars]==list(range(start,start+n*60,60))
    assert all(all(math.isfinite(v) and v>0 for v in (o,h,l,c)) and l<=min(o,c)<=max(o,c)<=h for _,o,h,l,c in bars)
    return bars,dict(window=window,source_commit=pin,bars=n,sha256=actual,valid=True)

def run(window,name,params,bars):
    B,g,A,tp=params
    cycles=[];logs=[];fills=[];days=[];active={s:None for s in ('LONG','SHORT')}
    cash=0.;fees=0.;injected=recovered=0.;cid=0;cycle_fees=0.;minimum=(10000.,1,iso(bars[0][0]));next_cycle=True
    def equity(price):return cash+sum(b['sign']*b['qty']*price for b in active.values() if b)
    def enter(b,price,n,t,kind):
        nonlocal cash,fees
        fee=n*FEE;cash-=b['sign']*n+fee;fees+=fee;b['fees']+=fee;b['qty']+=n/price;b['cost']+=n;b['last']=price
        fills.append(dict(cycle_id=cid,basket_id=b['basket_id'],side=b['side'],time_utc=iso(t),kind=kind,price=price,notional=n,fee=fee))
    def finish(b,price,t,reason,marked=False):
        nonlocal cash,fees
        n=b['qty']*price;fee=0. if marked else n*FEE
        if not marked:
            cash+=b['sign']*n-fee;fees+=fee;b['fees']+=fee
            fills.append(dict(cycle_id=cid,basket_id=b['basket_id'],side=b['side'],time_utc=iso(t),kind=reason,price=price,notional=n,fee=fee))
        pnl=b['sign']*(n-b['cost'])-b['fees']
        logs.append(dict(cycle_id=cid,basket_id=b['basket_id'],side=b['side'],open_time_utc=b['open_time_utc'],base_notional=b['base'],starting_account_equity=b['starting_equity'],close_time_utc='' if marked else iso(t),mark_time_utc=iso(t),close_price=price,close_reason=reason,add_count=b['adds'],quantity=b['qty'],entry_notional=b['cost'],fees=b['fees'],pnl_net=pnl,realized_pnl_net=0. if marked else pnl))
        active[b['side']]=None
    for t,o,h,l,c in bars:
        if next_cycle:
            cid+=1;cash=10000.;injected+=10000.;start=t;cycle_fees=fees;next_cycle=False
        # Snapshot before either simultaneous base fill; existing positions marked at open.
        opening_equity=equity(o)
        for side,sign in [('LONG',1),('SHORT',-1)]:
            if active[side] is None:
                b=dict(side=side,sign=sign,basket_id=len(logs)+sum(x is not None for x in active.values())+1,open_time_utc=iso(t),starting_equity=opening_equity,base=opening_equity*B,qty=0.,cost=0.,fees=0.,adds=0,last=o)
                active[side]=b;enter(b,o,b['base'],t,'BASE')
        for side in ('LONG','SHORT'):
            b=active[side];s=b['sign']
            def adverse(level):return l<=level if s==1 else h>=level
            while b['adds']<A and adverse(b['last']*(1-s*g)):
                grid=b['last']*(1-s*g);price=min(o,grid) if s==1 else max(o,grid)
                b['adds']+=1;enter(b,price,b['base']*2**b['adds'],t,'ADD_'+str(b['adds']))
            stop=b['last']*(1-s*g)
            # Frozen LONG strictly crosses; SHORT mirrors strict crossing.
            if b['adds']==A and (l<stop if s==1 else h>stop):finish(b,c,t+60,'STAIR_STOP')
            else:
                target=b['cost']/b['qty']*(1+s*tp)
                if h>=target if s==1 else l<=target:
                    finish(b,max(o,target) if s==1 else min(o,target),t,'TAKE_PROFIT')
        trigger=equity(c);outcome='BUSTED' if trigger<=2000 else 'DOUBLED' if trigger>=20000 else None
        if outcome:
            for b in list(active.values()):
                if b:finish(b,c,t+60,'BUST' if outcome=='BUSTED' else 'CYCLE_DOUBLED')
        e=equity(c)
        if e<minimum[0]:minimum=(e,cid,iso(t+60))
        if (t+60)%86400==0 or t==bars[-1][0]:
            days.append(dict(date_utc=iso(t)[:10],close_time_utc=iso(t+60),cycle_id=cid,active_cycle_equity=e,total_injected=injected,settled_recoveries=recovered,stitched_equity=recovered+e,cumulative_net_pnl=recovered+e-injected,total_fees=fees))
        if outcome or t==bars[-1][0]:
            if not outcome:
                outcome='OPEN_AT_END'
                for b in list(active.values()):
                    if b:finish(b,c,t+60,'OPEN_AT_END',True)
            cycles.append(dict(cycle_id=cid,start_utc=iso(start),end_utc=iso(t+60),result=outcome,trigger_equity=trigger,settlement_equity=e,injection=10000.,net_pnl=e-10000.,duration_days=(t+60-start)/86400,total_fees=fees-cycle_fees))
            recovered+=e;next_cycle=True
    result=dict(window=window,variant=name,B=B,g=g,A=A,tp=tp,cycles=cid,**{v:sum(x['result']==v for x in cycles) for v in ('DOUBLED','BUSTED','OPEN_AT_END')},total_injected=injected,total_recovered=recovered,net_pnl=recovered-injected,average_cycle_days=sum(x['duration_days'] for x in cycles)/cid,total_fees=fees,minimum_equity=minimum[0],minimum_cycle=minimum[1],minimum_time_utc=minimum[2])
    for outcome,key,sign in [('DOUBLED','average_doubled_settlement_surplus',1),('BUSTED','average_busted_settlement_loss',-1)]:
        xs=[sign*(x['settlement_equity']-10000) for x in cycles if x['result']==outcome];result[key]=sum(xs)/len(xs) if xs else None
    for side in ('LONG','SHORT'):
        ls=[x for x in logs if x['side']==side]
        result[side]=dict(baskets=len(ls),take_profit_count=sum(x['close_reason']=='TAKE_PROFIT' for x in ls),stair_stop_count=sum(x['close_reason']=='STAIR_STOP' for x in ls),realized_pnl_net=sum(x['realized_pnl_net'] for x in ls),open_at_end_marked_pnl=sum(x['pnl_net'] for x in ls if x['close_reason']=='OPEN_AT_END'))
    assert len({x['basket_id'] for x in logs})==len(logs)
    assert math.isclose(sum(x['fee'] for x in fills),fees,abs_tol=1e-6)
    assert math.isclose(sum(x['pnl_net'] for x in logs),result['net_pnl'],abs_tol=1e-6)
    for cy in cycles:
        assert math.isclose(sum(x['pnl_net'] for x in logs if x['cycle_id']==cy['cycle_id']),cy['net_pnl'],abs_tol=1e-6)
    prefix=f'{window}_{name}'
    for suffix,rows in [('cycles',cycles),('baskets',logs),('fills',fills),('daily_equity',days)]:save(OUT/f'{prefix}_{suffix}.csv',rows)
    return result

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    # Both inputs must pass before any strategy runs.
    loaded={w:load(w) for w in PINS}
    (OUT/'validation.json').write_text(json.dumps([v[1] for v in loaded.values()],indent=2)+'\n')
    results=[]
    for window,(bars,audit) in loaded.items():
        print(json.dumps(audit),flush=True)
        for name,params in CONFIGS.items():
            r=run(window,name,params,bars);results.append(r);print(json.dumps(r),flush=True)
    (OUT/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__':main()

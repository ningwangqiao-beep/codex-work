#!/usr/bin/env python3
"""Independent fill-ledger replay and focused bidirectional execution fixtures."""
import collections
import csv
import datetime as dt
import json
import math
import tempfile
from pathlib import Path
import run_phase4 as p

def read(path):return list(csv.DictReader(path.open()))
def stamp(s):return int(dt.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())
def near(a,b):assert math.isclose(float(a),float(b),rel_tol=1e-10,abs_tol=1e-6),(a,b)
def replay(summary,bars):
    prefix=f"{summary['window']}_{summary['variant']}"
    fills=read(p.OUT/f'{prefix}_fills.csv');cycles=read(p.OUT/f'{prefix}_cycles.csv');logs=read(p.OUT/f'{prefix}_baskets.csv');daily=read(p.OUT/f'{prefix}_daily_equity.csv')
    grouped=collections.defaultdict(list)
    for f in fills:
        t=stamp(f['time_utc'])
        if f['kind'] in ('STAIR_STOP','BUST','CYCLE_DOUBLED'):t-=60
        grouped[t].append(f)
    settlements={stamp(c['end_utc']):c for c in cycles};days={stamp(d['close_time_utc']):d for d in daily}
    B,g,A,tp=[summary[k] for k in ('B','g','A','tp')]
    cash=10000.;qty={'LONG':0.,'SHORT':0.};state={};fee_total=0.;recovered=0.;injected=10000.;cid=1;prev_terminal=False;min_e=(10000.,1,p.iso(bars[0][0]));last_closed={};base_fees={}
    for t,o,h,l,c in bars:
        if prev_terminal:
            cash=10000.;injected+=10000.;cid+=1;prev_terminal=False
            assert all(abs(q)<1e-8 for q in qty.values())
        opening_equity=cash+(qty['LONG']-qty['SHORT'])*o
        fs=grouped[t]
        for f in fs:
            side=f['side'];s=1 if side=='LONG' else -1;price=float(f['price']);n=float(f['notional']);fee=float(f['fee']);kind=f['kind'];bid=f['basket_id']
            assert int(f['cycle_id'])==cid;near(fee,n*p.FEE)
            if kind=='BASE':
                assert side not in state and last_closed.get(side,-1)<t
                near(price,o);near(n,opening_equity*B)
                state[side]=dict(base=n,last=price,adds=0,cost=0.,fees=0.,bid=bid)
            b=state[side];assert b['bid']==bid
            if kind=='BASE' or kind.startswith('ADD_'):
                if kind!='BASE':
                    grid=b['last']*(1-s*g);assert l<=grid if s==1 else h>=grid
                    near(price,min(o,grid) if s==1 else max(o,grid));b['adds']+=1;assert b['adds']<=A
                    near(n,b['base']*2**b['adds'])
                cash-=s*n+fee;qty[side]+=n/price;b['cost']+=n;b['fees']+=fee;b['last']=price
            else:
                near(n,qty[side]*price)
                if kind=='TAKE_PROFIT':
                    target=b['cost']/qty[side]*(1+s*tp)
                    near(price,max(o,target) if s==1 else min(o,target));assert h>=target if s==1 else l<=target
                    assert not (b['adds']==A and (l<b['last']*(1-g) if s==1 else h>b['last']*(1+g)))
                elif kind=='STAIR_STOP':
                    assert b['adds']==A;assert l<b['last']*(1-g) if s==1 else h>b['last']*(1+g)
                    near(price,c)
                else:assert kind in ('BUST','CYCLE_DOUBLED');near(price,c)
                cash+=s*n-fee;qty[side]=0.;state.pop(side);last_closed[side]=t
            fee_total+=fee
        e=cash+(qty['LONG']-qty['SHORT'])*c
        if e<min_e[0]:min_e=(e,cid,p.iso(t+60))
        if t+60 in days:
            d=days[t+60];near(d['active_cycle_equity'],e);near(d['stitched_equity'],recovered+e);near(d['cumulative_net_pnl'],recovered+e-injected);near(d['total_fees'],fee_total)
        if t+60 in settlements:
            cy=settlements[t+60];near(cy['settlement_equity'],e)
            if cy['result']!='OPEN_AT_END':
                assert not state;trigger=float(cy['trigger_equity']);assert trigger<=2000 if cy['result']=='BUSTED' else trigger>=20000
                exit_fees=sum(float(f['fee']) for f in fs if f['kind'] in ('BUST','CYCLE_DOUBLED'));near(trigger-exit_fees,e);prev_terminal=True
            recovered+=e
    near(summary['net_pnl'],recovered-injected);near(summary['total_fees'],fee_total);near(summary['minimum_equity'],min_e[0]);assert summary['minimum_cycle']==min_e[1] and summary['minimum_time_utc']==min_e[2]
    for side in ('LONG','SHORT'):
        ls=[x for x in logs if x['side']==side];near(summary[side]['realized_pnl_net'],sum(float(x['realized_pnl_net']) for x in ls))
    near(sum(float(x['pnl_net']) for x in logs),summary['net_pnl'])
    return dict(run=prefix,fill_count=len(fills),basket_count=len(logs),cycle_count=len(cycles),daily_count=len(daily),ledger_replay=True)

def fixtures():
    original=p.OUT
    with tempfile.TemporaryDirectory() as tmp:
        p.OUT=Path(tmp)
        # Exact final stop level does not trigger; strict crossing does, overriding TP.
        t=1761955200
        p.run('TEST','mirror',(.2,.006,8,.006),[(t,100.,100.,100.,100.),(t+60,106.,106.7,90.,100.),(t+120,100.,100.,100.,100.)])
        fs=read(p.OUT/'TEST_mirror_fills.csv');bs=read(p.OUT/'TEST_mirror_baskets.csv')
        short_add=next(x for x in fs if x['side']=='SHORT' and x['kind']=='ADD_1');near(short_add['price'],106.)
        # A gap anchors the next grid at the actual fill, not at the skipped grid.
        next_short=next(x for x in fs if x['side']=='SHORT' and x['kind']=='ADD_2');near(next_short['price'],106.*1.006)
        p.run('TEST','stop',(.2,.006,8,.006),[(t,100.,106.,90.,100.),(t+60,100.,100.,100.,100.)])
        bs=read(p.OUT/'TEST_stop_baskets.csv')
        assert {b['side'] for b in bs if b['close_reason']=='STAIR_STOP'}=={'LONG','SHORT'}
        fs=read(p.OUT/'TEST_stop_fills.csv')
        for side in ('LONG','SHORT'):
            assert len([f for f in fs if f['side']==side and f['kind']=='BASE'])==2
            assert len([f for f in fs if f['side']==side and f['kind']=='TAKE_PROFIT'])==0
        p.run('TEST','tp',(.2,.006,8,.006),[(t,100.,101.,99.,100.),(t+60,100.,101.,99.,100.)])
        fs=read(p.OUT/'TEST_tp_fills.csv')
        for side in ('LONG','SHORT'):
            times=[f['time_utc'] for f in fs if f['side']==side and f['kind']=='TAKE_PROFIT'];assert len(times)==len(set(times))==2
        p.run('TEST','tp_gap',(.2,.006,8,.006),[(t,100.,100.,100.,100.),(t+60,99.,99.,99.,99.)])
        fs=read(p.OUT/'TEST_tp_gap_fills.csv')
        near(next(f['price'] for f in fs if f['side']=='SHORT' and f['kind']=='TAKE_PROFIT'),99.)
        # Final open baskets stay marked; no invented closing fills or fees.
        p.run('TEST','open',(.2,.006,8,.006),[(t,100.,100.,100.,100.)])
        fs=read(p.OUT/'TEST_open_fills.csv');bs=read(p.OUT/'TEST_open_baskets.csv');assert len(fs)==2 and all(b['close_reason']=='OPEN_AT_END' for b in bs)
    p.OUT=original
    return True

def main():
    summaries=json.loads((p.OUT/'summary.json').read_text());loaded={w:p.load(w)[0] for w in p.PINS}
    report=dict(ledger_checks=[replay(s,loaded[s['window']]) for s in summaries],execution_fixtures=fixtures(),single_direction_runs=0)
    (p.OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()

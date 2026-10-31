#!/usr/bin/env python3
"""Replay the four OOS configurations against the unchanged phase-one engine."""
import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path
from run_phase3 import p, CONFIGS

def read(name):
    return list(csv.DictReader((p.OUT/name).open()))

def stamp(s):
    return int(p.dt.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())

def main():
    source=subprocess.check_output(['git','show',p.BASELINE+':dbm/backtest.py'],cwd=p.ROOT,text=True)
    ns={'__name__':'frozen_reference'};exec(source,ns)
    assert hashlib.sha256((p.OUT/'input_bars.csv').read_bytes()).hexdigest()==json.loads((p.OUT/'validation.json').read_text())['input_sha256']
    bars=[(stamp(r['open_time_utc']),*[float(r[k]) for k in ('open','high','low','close')]) for r in read('input_bars.csv')]
    checked=0;fills_checked=0
    for name, params in CONFIGS.items():
        ns['PARAMS'] = {name: params}
        cycles=read(name+'_cycles.csv');fills=read(name+'_fills.csv')
        for cycle in cycles:
            cid=cycle['cycle_id'];start=stamp(cycle['start_utc']);end=stamp(cycle['end_utc'])
            bs=bars[(start-p.START)//60:(end-p.START)//60];capture={}
            ns.update(START=start,writecsv=lambda path,rows,fields:capture.update({path.name:rows}))
            reference=ns['simulate'](name,bs,p.OUT)
            actual=[r for r in fills if r['cycle_id']==cid]
            common=[r for r in actual if r['kind']!='CYCLE_DOUBLED']
            expected=capture[name+'_fills.csv']
            assert len(common)==len(expected),(name,cid)
            for a,b in zip(common,expected):
                for key,value in b.items():
                    assert (float(a[key])==value if isinstance(value,(int,float)) else a[key]==value),(name,cid,key)
            cash=10000.;qty=0.;fees=0.
            for r in actual:
                n=float(r['notional']);f=float(r['fee']);price=float(r['price']);fees+=f
                assert math.isclose(f,n*.0007,rel_tol=1e-12)
                if r['kind']=='BASE' or r['kind'].startswith('ADD_'):
                    cash-=n+f;qty+=n/price
                else:
                    assert math.isclose(n,qty*price,abs_tol=1e-7);cash+=n-f;qty=0.
            equity=cash+qty*bs[-1][4]
            assert math.isclose(equity,float(cycle['settlement_equity']),abs_tol=1e-7)
            assert math.isclose(fees,float(cycle['total_fees']),abs_tol=1e-7)
            if cycle['result']=='DOUBLED':assert reference['DOUBLED']==cycle['end_utc']
            elif cycle['result']=='BUSTED':assert reference['BUSTED']==cycle['end_utc']
            checked+=1;fills_checked+=len(expected)
        daily=read(name+'_daily_equity.csv')
        assert len(daily)==181
        for r in daily:
            assert math.isclose(float(r['stitched_equity'])-float(r['total_injected']),float(r['cumulative_net_pnl']),abs_tol=1e-7)
        assert math.isclose(float(daily[-1]['cumulative_net_pnl']),sum(float(c['net_pnl']) for c in cycles),abs_tol=1e-7)
    result=dict(valid=True,baseline=p.BASELINE,cycles_replayed=checked,
                exact_frozen_fills_compared=fills_checked,fee_and_settlement_ledger=True,
                daily_external_flow_reconciliation=True)
    (p.OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()

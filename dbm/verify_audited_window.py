import csv, json, subprocess, sys, types, math
from pathlib import Path
sys.path.insert(0,'dbm')
import run_audited_window as runner
import backtest
out=runner.OUT
bars,_=runner.load()
original=types.ModuleType('frozen_original')
exec(subprocess.check_output(['git','show',runner.BASELINE+':dbm/backtest.py'],text=True),original.__dict__)
original.END=runner.LAST+60
check=Path('work/baseline_check'); check.mkdir(exist_ok=True)
results=json.loads((out/'summary.json').read_text())
checks=[]
for summary in results:
    name=summary['variant']
    frozen=original.simulate(name,bars,check)
    assert all(summary[k]==v for k,v in frozen.items()),name
    read=lambda suffix:list(csv.DictReader((out/f'{name}_{suffix}.csv').open()))
    fills=read('fills'); baskets=read('baskets'); daily=read('daily_equity')
    assert len(daily)==61 and daily[-1]['close_time_utc']=='2026-10-31T17:05:00Z'
    assert math.isclose(float(daily[-1]['equity']),summary['final_equity'])
    assert math.isclose(sum(float(f['fee']) for f in fills),summary['total_fees'],abs_tol=1e-8)
    assert math.isclose(10000+sum(float(b['pnl_net']) for b in baskets),summary['final_equity'],abs_tol=1e-8)
    cash=10000.; qty=0.
    for f in fills:
        n=float(f['notional']); price=float(f['price']); fee=float(f['fee'])
        assert math.isclose(fee,n*.0007,abs_tol=1e-8)
        if f['kind']=='BASE' or f['kind'].startswith('ADD_'):
            cash-=n+fee; qty+=n/price
        else:
            assert math.isclose(n,qty*price,abs_tol=1e-7)
            cash+=n-fee; qty=0.
    assert math.isclose(cash+qty*bars[-1][4],summary['final_equity'],abs_tol=1e-7)
    assert (baskets[-1]['close_reason']=='OPEN_AT_END') == (qty>0)
    checks.append(dict(variant=name, baseline_summary_exact_match=True,daily_rows=len(daily),fill_count=len(fills),ledger_reconciles=True,fees_reconcile=True,basket_pnl_reconciles=True))
(out/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))

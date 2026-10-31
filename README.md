> Current canonical execution and latest results: [round2/REPORT.md](round2/REPORT.md). The parent engine/results below are the historical first-round study; its audit anchors have been invalidated.

# ETHUSDT 1m synthetic hedged-basket study

Read `REPORT.md` for the full Chinese report and `results/all_results.csv` for all results.
This is an in-sample structural/parameter search over three disjoint windows, not a claim of live performance.

## Run

```sh
python -m pip install -r requirements.txt
python fetch.py                 # Binance REST pagination; refuses missing/duplicate data
python test_engine.py
python baselines.py             # compliant baseline AND separately labeled anchor replay
python optimize.py              # C01-C18
python refine.py                # C19-C24, historical EMA size asymmetry
python structural.py            # C25-C30, previous-close regime exits at next open
python verify_results.py
python replay_check.py
python report.py
```

Included `data/W*.csv.gz` can be used without re-downloading. Raw HTTP page caches are excluded from Git; the canonical merged CSV hashes are recorded in `results/data_validation.json`. Gzip files contain ordinary CSV with full 1m resolution, not sampled bars. Per-fill trades remain ordinary CSV. Equity timestamps identify each minute's open time; equity is valued at that minute's close.

## Outputs

- `results/A_a/`, `results/A_b/`: execution-bound compliant baseline. Gap additions may fill adversely at their grid; TP+same-price reopen requires a price reachable for both directions.
- `results/Anchor_a/`, `results/Anchor_b/`: diagnostic replay matching supplied anchors; explicitly NOT compliant because some same-price reopens are favorable beyond the candle extreme.
- `results/C01/` through `results/C30/`: all final optimization candidates, each with W1/W2/W3 full 1m equity and per-fill trades.
- `results/parameters.json`, `all_results.csv`, `fill_audit.json`, `ranking.csv`, `best.json`, `best_monthly.csv`, `best_trade_summary.csv`, `equity_comparison.png`.
- `results/*/W*_trades.csv`: kind 0=open, 1=add, 2=TP, 3=ladder stop, 4=account stop, 5=optional terminal close, 6=EMA regime close. Side +1=long, -1=short; quantity is positive. Basket IDs are unique within each run.

`basket_net` is a complete closed-basket P&L including prior entry/add fees for kinds >=2. For entry/addition rows it is just the current negative fee; do NOT sum the entire basket_net column. The accounting identity is initial capital + sum(gross-fee) + final open_gross = final equity. Another identity is sum(closed basket_net) + final open_gross - final open_entry_fees = total profit.

Exposure cap uses cumulative entry notionals, measured before each addition against previous close equity; long additions receive priority if both compete for the cap. Skips count one blocked level per side per minute; the blocked level is retried later. The optimized base is recalculated from previous close equity and previous-close EMA direction at every fill, including additions. The first bar uses initial $10,000 and a neutral signal.

All windows start independently with $10,000. Final return uses open-basket mark-to-market without hypothetical final exit fees. Max drawdown uses 1m close equity and a non-resetting statistical peak. There is no exchange margin liquidation model; equity <=0 and drawdown >=60% are separate audit flags. Baseline suspension and ladder restart follow the requested exceptions; optimized nonbankrupt strategies maintain one basket on each side at every minute close.

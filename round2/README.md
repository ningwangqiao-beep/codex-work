# Round two: canonical fills, 24-point search, one untouched holdout

See `SEARCH_PLAN.md` and `search_space.json`, committed before any round-two evaluation, for the pre-registered space, selection rule and exact gap treatment. Round-one source/results remain unchanged in the parent directory.

From the repository root, use the parent's `requirements.txt`, then:

```sh
python round2/test_engine.py
python round2/train.py
# Commit results/selection.json and candidate scores BEFORE proceeding.
python round2/holdout.py
python round2/verify.py
python round2/report.py
```

The included locked selection and holdout protocol intentionally block repeated training or a second holdout experiment. For deterministic offline replay of the included outputs use `verify.py`; it loads the included data, checks all trades and re-runs the engine without tuning. To reproduce the entire research process from scratch, use a fresh copy without `round2/results` and keep W0 unavailable until training locks the selection.

Training windows use the original full-resolution `../data/W1.csv.gz`–`W3.csv.gz`. W0 is fetched through the same Binance spot REST pagination and stored in `round2/data/W0.csv.gz`. No resampling is used in any evaluation. Full minute-close equity is gzip CSV; fills are plain CSV. Per-run JSON records exact parameters. Each window starts independently with $10,000; no warm-up or inherited positions. Returns use final close mark-to-market without hypothetical terminal fees; drawdowns use a non-resetting statistical close-equity peak, starting at $10,000.

Canonical TP trigger is directional: long high >= target, short low <= target. Following the required frozen phase order, targets are computed after additions. If target is inside the candle range, exit/reopen at target; otherwise exit/reopen at current open. No additional TP is allowed for the same side that minute. For additions, trigger at the grid and clip the actual fill to [low,high]; the next grid uses that actual last fill. This also applies if multiple additions are triggered in one minute.

`*_TP_only` runs are attribution diagnostics only: canonical TP plus the previous round's adverse outside-range addition fills. They are excluded from optimization and selection. Other execution phases and risk semantics are inherited from round one. Exposure is summed entry notionals against 4× previous close equity; base and addition sizes use previous close equity. Optimized ladder stops reopen immediately at close, keeping dual baskets; baseline A_b restarts that side next open and pauses 24h after a 12% account stop, resetting the account-control peak at restart. Statistical max-drawdown peak never resets. Optimized dd=1 means no positive-equity account stop; equity <=0 is liquidated and permanently stops the run. Drawdown >=60% is a separate flag, not an exchange liquidation model.

Selection uses ONLY minimum W1/W2/W3 return, then sum of their three returns, then candidate ID. All 24 trials are in-sample. Only the locked winner and original C04 are evaluated on W0. W0 return <0 OR close max drawdown >=60% means failed holdout validation. No additional search follows W0.

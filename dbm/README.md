# Frozen DBM backtest — blocked by missing source data

The requested window is 2026-09-01 00:00 through 2026-10-31 23:59 UTC (87,840 minutes).
The download/validation run found 86,400 valid minutes, ending 2026-10-30 23:59 UTC.
All 1,440 minutes of 2026-10-31 are missing. The October monthly archive and October 31 daily archive returned HTTP 404. September monthly and October 1–30 daily archives were retrieved and passed publisher SHA-256 and ZIP CRC verification. No malformed rows, duplicate timestamps, misaligned times or OHLC errors were detected in the available data.

**No variant was run.** No performance figures, daily equity files or basket results are asserted. Missing data is not forward-filled, substituted, or treated as flat prices. The simulator is implemented but its real-data results remain unvalidated until the complete input passes the gate.

## Reproduce

Python 3 standard library only:

```sh
python dbm/backtest.py --cache work/data --out dbm/results
```

Missing archives are retried on subsequent runs; HTTP errors are not cached. ZIPs and publisher checksums are cached locally, not committed. The script exits unsuccessfully before simulating if input validation fails. Complete data will produce each variant's daily equity, baskets (JSON array containing every buy), fills, and summary JSON. Parameters are constants and have no tuning switches.

## Frozen implementation conventions

- Data source: Binance **spot** ETHUSDT 1m, consistent with synthetic spot accounting. Cash may be negative; no funding, borrowing interest, margin liquidation or buying-power cap is introduced.
- Initial capital $10,000; every buy and sell pays 0.07% of fill notional. Basket average is quantity-weighted purchase price, excluding fees; basket net P&L includes all fees.
- Base buy occurs at first bar open and the next bar after each close. Same-bar multiple adds are processed sequentially against the low; every grid is anchored to the actual previous fill, including gap fills.
- Add trigger is low <= grid; after all A adds, stair stop is low **<** final fill × (1−g), interpreting “被跌破” strictly. Stop closes at the bar close and overrides TP. Otherwise high >= TP closes at TP or the higher open, as specified. No same-bar reopen.
- Thresholds, drawdown and minimum equity use bar-close equity. BUST records the trigger, liquidates at that close with sell fee and stays stopped. DOUBLED records the first qualifying close and continues. Subsequent liquidation fees are included in final equity and drawdown. Close-check timestamps use the UTC right boundary of the minute, e.g. the 23:59 bar is evaluated at 00:00 next day.
- The window does not impose an extra sell: an open last basket is marked OPEN_AT_END, its net P&L is marked to the final close. Total basket count includes it. After BUST, daily equity remains the stopped cash balance to window end.
- Peak total notional is the sum of outstanding buy notionals (cost basis); its percentage uses contemporaneous marked equity at the actual fill that established that peak, after the fill fee. Summary also exposes maximum observed position-market-value/equity percentage at fills and closes. Intrabar exposure is not used for the close-based race.
- Fill timestamps identify the minute for intrabar fills, not an invented tick time. Stair-stop and BUST execution timestamps identify the bar-close boundary.

## Audit artifacts

- `results/validation.json`: archive URLs, HTTP status, SHA-256, checksum outcomes, row errors and counts.
- `results/data_daily_audit.csv`: all 61 UTC days with expected, available and missing counts.
- `results/missing_minutes.csv`: each missing minute individually (1,440 rows).

The repository contains no fabricated strategy result CSVs. Completing the requested three-variant report requires the missing October 31 public archive to become available.

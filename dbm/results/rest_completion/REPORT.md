# REST completion attempt: validation failed, simulation stopped

Baseline: `bbc0dcdf110283e9a0a7844a29c761b7b153d2b0`.
`dbm/backtest.py`, parameters and implementation conventions are unchanged.

The supplied startTime values 1793577600000 and 1793637600000 resolve to
2026-11-02 00:00 and 16:40 UTC, respectively. Both requests returned HTTP 200
with empty arrays. Per the task's UTC coverage instruction, actual replacement
requests used startTime=1793404800000, limit=1000 and
startTime=1793464800000, limit=440 on the same ETHUSDT 1m REST endpoint.
They returned 1000 and 25 rows, covering October 31 00:00 through 17:04 UTC.
All four exact URLs, response hashes and row counts are in validation.json;
the unmodified response bodies are retained alongside it.

The baseline archive validator was run unchanged and freshly retrieved September
and October 1–30 archives: 86,400 rows, valid publisher checksums and ZIP CRC,
no OHLC/row errors. Its separate report is archive_validation.json. October
monthly and October 31 daily archives still returned 404.

Combining those archives and the REST responses yields 87,425 received rows,
not the required 87,840. There are 415 missing timestamps from October 31
17:05 through 23:59 UTC inclusive. The last REST candle may still be open;
received row counts must not be represented as counts of completed candles.
All received timestamps are aligned, unique and strictly continuous, and OHLC
checks pass. The 23:59 October 30 close and 00:00 October 31 open both equal
2245.54, with timestamps exactly 60 seconds apart. Seam bars are in validation.json.

The full-window validation gate FAILS. V0, V1 and V2 were NOT run. Their race
outcomes, final equity, drawdown, minimum equity, basket counts, take profits,
stair stops, peak notional and fees are unavailable, not "untriggered" or zero.
No daily strategy equity CSVs or basket logs were generated. No prices were
filled, extrapolated or substituted. Resume only after all required completed
candles exist and full-window validation passes.

Existing parent-directory audit artifacts describe the prior baseline attempt;
this directory contains the new attempt. The missing-minute CSV and daily audit
here describe the combined received coverage.

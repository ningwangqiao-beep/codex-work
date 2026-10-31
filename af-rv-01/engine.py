#!/usr/bin/env python3
"""AlphaForge minimal backtest engine v0.1 (linear perpetual, futures-style
margin accounting).

Causality contract:
- A strategy returns target[i] = desired position (-1/0/+1) decided at the
  CLOSE of bar i, using only bars <= i.
- The engine executes target[i] at the OPEN of bar i+1, with adverse slippage.
- Funding: settlements whose timestamp falls on a bar open are charged on the
  position held after that open's fills, valued at that open (approximation,
  documented; settlements occur at 00/08/16 UTC = 15m bar opens).
- Equity at bar close = cash + qty * (close - entry_price). Cash moves only
  via fees, funding and realized PnL.
"""
import numpy as np
import pandas as pd


def funding_by_bar(bars: pd.DataFrame, funding: pd.DataFrame) -> dict:
    """Map bar index -> funding rate for settlements at that bar's open."""
    opens = bars["open_time"].to_numpy()
    out = {}
    for t, r in zip(funding["calc_time"].to_numpy(), funding["last_funding_rate"].to_numpy()):
        idx = int(np.searchsorted(opens, t))
        if idx < len(opens) and opens[idx] == t:
            out[idx] = float(r)
    return out


def run_backtest(bars, target, funding_map, start_equity=1000.0,
                 fee_rate=0.0005, slip=0.0002, leverage=1.0):
    opens = bars["open"].to_numpy(float)
    closes = bars["close"].to_numpy(float)
    times = bars["open_time"].to_numpy()
    n = len(bars)
    cash = float(start_equity)
    qty = 0.0
    entry_px = entry_ts = None
    entry_fee = 0.0
    fund_acc = 0.0  # cash delta from funding during the open trade (neg = paid)
    trades = []
    equity = np.empty(n)
    total_fees = 0.0
    total_funding = 0.0

    def close_position(i, px, reason):
        nonlocal cash, qty, entry_px, entry_ts, entry_fee, fund_acc, total_fees
        exit_px = px * (1 - slip) if qty > 0 else px * (1 + slip)
        fee = abs(qty) * exit_px * fee_rate
        gross = qty * (exit_px - entry_px)
        cash += gross - fee
        total_fees += fee
        trades.append({
            "entry_ts": entry_ts, "exit_ts": int(times[i]),
            "side": 1 if qty > 0 else -1,
            "entry_px": entry_px, "exit_px": exit_px, "qty": abs(qty),
            "gross_pnl": gross, "fees": entry_fee + fee,
            "funding": fund_acc, "net_pnl": gross - entry_fee - fee + fund_acc,
            "exit_reason": reason,
        })
        qty, entry_px, entry_ts, entry_fee, fund_acc = 0.0, None, None, 0.0, 0.0

    prev_equity = float(start_equity)
    for i in range(n):
        if i > 0:
            want = int(target[i - 1])
            cur = 0 if qty == 0 else (1 if qty > 0 else -1)
            if want != cur:
                if qty != 0:
                    close_position(i, opens[i], "signal")
                if want != 0:
                    fill = opens[i] * (1 + slip) if want > 0 else opens[i] * (1 - slip)
                    notional = prev_equity * leverage
                    fee = notional * fee_rate
                    cash -= fee
                    total_fees += fee
                    qty = want * notional / fill
                    entry_px, entry_ts, entry_fee = fill, int(times[i]), fee
        if i in funding_map and qty != 0:
            delta = -qty * opens[i] * funding_map[i]
            cash += delta
            fund_acc += delta
            total_funding += delta
        equity[i] = cash + (qty * (closes[i] - entry_px) if qty != 0 else 0.0)
        prev_equity = equity[i]

    if qty != 0:
        close_position(n - 1, closes[n - 1], "end_of_data")
        equity[n - 1] = cash

    return {
        "equity": equity, "trades": trades,
        "total_fees": total_fees, "total_funding": total_funding,
        "final_equity": float(cash),
    }


def segment_metrics(times, equity, trades, t0, t1, bars_per_year=365 * 96):
    """Metrics for the segment [t0, t1) sliced from a full run."""
    mask = (times >= t0) & (times < t1)
    eq = equity[mask]
    if len(eq) < 2:
        return {}
    start = float(eq[0])
    ret = float(eq[-1] / start - 1) if start > 0 else float("nan")
    peak = np.maximum.accumulate(eq)
    dd = float((eq / peak - 1).min()) if (peak > 0).all() else float("nan")
    rets = np.diff(eq) / eq[:-1]
    sharpe = float(rets.mean() / rets.std() * np.sqrt(bars_per_year)) if rets.std() > 0 else 0.0
    seg_trades = [t for t in trades if t0 <= t["exit_ts"] < t1]
    wins = [t for t in seg_trades if t["net_pnl"] > 0]
    return {
        "net_return_pct": round(ret * 100, 4),
        "max_drawdown_pct": round(dd * 100, 4),
        "sharpe": round(sharpe, 3),
        "trades": len(seg_trades),
        "win_rate_pct": round(100 * len(wins) / len(seg_trades), 2) if seg_trades else 0.0,
        "fees": round(sum(t["fees"] for t in seg_trades), 4),
        "funding": round(sum(t["funding"] for t in seg_trades), 4),
        "start_equity": round(start, 4), "end_equity": round(float(eq[-1]), 4),
    }

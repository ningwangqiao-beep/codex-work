# Round 2 pre-registered search plan

Frozen UTC: 2026-10-31T13:33:35.922196+00:00
Parameter JSON SHA256: 487d77a08526f2ed454d58545f6c3c7b11469e9e119596da173e8e55171d8d48

24 candidates = grids {2.5%,3%,3.5%,4%} × multipliers {1.3,1.5} × TP {1.5%,2%,2.5%}. Omit multiplier 1.7 to prioritize lower geometric exposure after round-1 results. Depth=5; base=2% of previous close equity; cap=4× previous close equity; no positive-equity account stop. All other C04 structure unchanged.

Ranking: descending minimum W1/W2/W3 return, then descending sum of three independent-window returns; exact ties use ascending candidate ID. No drawdown tie-break. All 24 are in-sample. No candidate is added after observing results.

Canonical TP: after additions, long trigger high>=target / short trigger low<=target; fill and reopen at target if in [low,high], otherwise at current open. This open fill happens in the frozen TP phase even when additions in this minute changed the average; no intrabar path is inferred. Additions: trigger at grid, actual fill=clip(grid,low,high); next grid derives from actual most recent fill. Multi-level cap checks and all fees unchanged.

For baseline A_b and C04 report old main results, TP-only bridge (old adverse-gap additions), and final canonical including clipped additions. Bridge runs are measurement diagnostics, not optimization candidates.

W0=[2023-11-01,2024-05-01) UTC is NOT downloaded, loaded, summarized, or used until selection.json locks one winning candidate and exact parameters using only W1-W3. Then run exactly that winner and original C04 under canonical execution on W0. No tuning after W0. Failure criterion: W0 return<0 OR close max drawdown>=60%. W0 starts independently at $10,000 without warm-up or prior state.

| ID | Grid | Multiplier | TP |
|---|---:|---:|---:|
| R01 | 2.5% | 1.3 | 1.5% |
| R02 | 2.5% | 1.3 | 2.0% |
| R03 | 2.5% | 1.3 | 2.5% |
| R04 | 2.5% | 1.5 | 1.5% |
| R05 | 2.5% | 1.5 | 2.0% |
| R06 | 2.5% | 1.5 | 2.5% |
| R07 | 3.0% | 1.3 | 1.5% |
| R08 | 3.0% | 1.3 | 2.0% |
| R09 | 3.0% | 1.3 | 2.5% |
| R10 | 3.0% | 1.5 | 1.5% |
| R11 | 3.0% | 1.5 | 2.0% |
| R12 | 3.0% | 1.5 | 2.5% |
| R13 | 3.5% | 1.3 | 1.5% |
| R14 | 3.5% | 1.3 | 2.0% |
| R15 | 3.5% | 1.3 | 2.5% |
| R16 | 3.5% | 1.5 | 1.5% |
| R17 | 3.5% | 1.5 | 2.0% |
| R18 | 3.5% | 1.5 | 2.5% |
| R19 | 4.0% | 1.3 | 1.5% |
| R20 | 4.0% | 1.3 | 2.0% |
| R21 | 4.0% | 1.3 | 2.5% |
| R22 | 4.0% | 1.5 | 1.5% |
| R23 | 4.0% | 1.5 | 2.0% |
| R24 | 4.0% | 1.5 | 2.5% |

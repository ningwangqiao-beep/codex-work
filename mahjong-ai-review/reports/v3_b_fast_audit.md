# Vectorized calculator audit

Independent opt-in rules/fast_hand_analysis.py added; frozen six source files unchanged. Exact legal target sets respect at most4 per tile; per-suit target deficit computed using NumPy and merged by DP, no legacy erroneous taatsu-only shortcut. Missing-uncleared fallback intentionally preserves original structural semantics. APIs shanten/effective_draws unchanged; public count4-own-public validation maintained. Targets and suit costs are cached with bounded entries.

Command .venv/Scripts/python.exe scripts/v3_b_fast_analysis_check.py:615cases parity passed exit0; includes original495 finite/high cases plus120 random open0..4,13/14-equivalent,missing none/0/1/2. Sampled effective-draw outputs also exactly equal. Slow1.3698s vs first vector pass0.0310s after shared target generation already warm. Ten repeated passes0.0231s,266130 calls/s is cache-hit microbenchmark NOT full-game performance.

Separate process-cold command .venv/Scripts/python.exe scripts/v3_b_fast_cold.py preserves measured import+first shanten/effective time and Windows working set in v3_b_fast_cold.json. Early memory query returned zero due ctypes handle truncation; failed query fixed and asserted success, not presented as valid memory evidence. Initial script path missing import root was corrected before final run.

D notified to opt-in and run actual bounded full-game strongBot tests. No training and no full-game strength claim. This accelerates existing corrected algorithm; parity is regression evidence, not an independent mathematical proof.

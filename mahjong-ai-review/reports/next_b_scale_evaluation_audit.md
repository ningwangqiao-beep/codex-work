# Independent development evaluation reconstruction

Read completed next_c_scale_development20.json and all240 JSONL rows. Actual recomputation Python exit0. Exact Cartesian coverage20 seeds7200400..7200419 x4 seats x3 policies, no duplicates or excluded seeds. Every row scores sum0, observer score equals net_score, parts sum to net_score. Recomputed means and seed-cluster bootstrap exactly match original summary/comparisons (Random42,1000 resamples, indices25/974, original comparison order).

relative100 mean3.775; scale1000 mean3.7625; strong mean3.675. Relative100-strong +0.1 CI[-0.45,0.65]; scale1000-strong +0.0875 CI[-0.9875,1.125]; scale1000-relative100 -0.0125 CI[-1.1125,1.0875]. All include zero; no evidence of improvement or promotion.

Per80games selfdraw events relative1008,scale10007,strong9; deal-in events2,0,0; mean deal-in losses0.05,0,0. These rare event counts do not establish zero true risk. Mean cha_jiao_big net1.15,1.025,0.875 respectively. Full categories and per-seed paired differences independently saved next_b_scale_evaluation_audit.json with source hashes.

JSONL contains aggregate component totals rather than raw full transfer ledger; this audit verifies accounting reconciliation at row aggregate level, not independently each source transfer. Opponents are random legal-discard with shared other-stage defaults; initial seed pairing does not force identical future trajectories. Development20 is exploratory, not independent final proof, and no seeds selected based on outcomes. No model or evaluation generator modified.

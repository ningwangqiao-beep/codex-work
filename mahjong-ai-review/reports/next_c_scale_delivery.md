# 1000-game shard support (no training run)

Only new next_scale training and next_model_scale scripts changed. Original100 fixed validation, old networks and champion are unchanged.

Actual checks: compileall exit0; --help exit0; smoke-v2 inspect exit0 (44 train,31 validation,6 terminal ledgers,75 exact prefix records,max history285); negative gate/CPU streaming-collate tests exit0. Evidence next_c_scale_smoke_v2_inspection.json and next_c_scale_support_test.json. Negative cases: duplicate shard,empty validation,changed source and smoke formal-training rejected. No new optimizer update, GPU training, or empirical resume/STOP test was performed for this new module. Existing checkpoint/resume/RNG/STOP implementation is retained; final1000 execution must verify these again independently if needed.

The trainer streams numerically seed-sorted per-game JSONL shards, uses20541 parameter relative+pairwise multitask network,seed42,batch128,6epochs,Adam.001,identical head loss weights. Full variable-length history pads per batch. It binds source,data,chief admission and optimizer config for resume, preserves unique best epochs, checks STOP each batch/validation batch and saves last before exit75. More records at fixed6epochs means more optimizer steps than100-game60-step reference, so outcomes are not a pure data-only causal comparison.

Inspect after generation:
`.venv/Scripts/python.exe scripts/next_model_scale_inspect.py --manifest datasets/next_history1000/manifest.json --output reports/next_c_scale_1000_inspection.json`

Only after chief audit/signature (NOT executed):
`.venv/Scripts/python.exe scripts/next_model_scale_train.py --manifest datasets/next_history1000/manifest.json --admission reports/next_chief_scale_admission.json --output checkpoints/next_history1000_relative_pairwise --epochs 6 --batch-size 128 --seed 42 --device cuda --resume`

Template next_c_scale_admission_template.json is deliberately passed=false/training=false; it cannot authorize a run. Chief fills actual manifest fingerprint/semantic audits and flags only after inspection. Frozen original100prefix1459 records and complete20validation are mandatory; no RL or old final set use. Teacher preference is heuristic rank NOT counterfactual Q, terminal V is behavior-policy-conditioned rawV3 score.

## Actual isolated training validation update
`python -m unittest tests.test_next_scale_training -v`: exit0,2.570s. Actual44train/31validation CPU2,2epochs,batch8,12updates. Interrupted after2real updates exits75 withlast; resumed final12updates equals uninterrupted weights exactly(maxabs0), optimizer allclose; resumed epoch-loss totals preserved. Actual old100trainer same small data/budget finalweights also maxabs0. Both old and new no shuffle; actual original-prefix order equals sorted shard order. Only test-process scoped mock admission,no formal authorization or GPU training. Old frozen code untouched. Newtrainer now saves epoch loss totals for correct resumed reporting. Gate also enforces split directory and rotatingseat=seed%4.

## Frozen model evaluation preparation
New `inference/next_scale_policy.py` and `scripts/next_model_scale_eval.py`; compile/help exit0 and old100weight rejection tested. New1000callback requires newversion,1000manifestSHA,data/model source hashes. Actual legal/poison callback awaits chief-selected frozen checkpoint, no evaluation run. Pre-registered240games7200400..419,4seats,relative100/scale1000/strong,paired initial deals/same random legal-discard opponents; policy order rotates deterministically to reduce cache timing confounds. Each seed group bootstrap aggregates4seats.

Pending chief checkpoint, command (replace best filename from actualBEST.json, not assumed):
`.venv/Scripts/python.exe scripts/next_model_scale_eval.py --relative100 checkpoints/next_history100_relative_pairwise/best_epoch_5.pt --scale1000 checkpoints/next_history1000_relative_pairwise/CHIEF_FROZEN_BEST.pt --seed 7200400 --seeds 20 --timeout 300 --output reports/next_c_scale_development20.json`

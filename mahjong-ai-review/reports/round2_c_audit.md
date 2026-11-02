# Round2 C audit and plan

Existing v1/v2 checkpoints are actual GPU-trained artifacts with separate optimizer/logs/deployment snapshots. v1 stopped after4 epochs (best0); v2 fixed8 (best7). Old final-test evaluations remain frozen; no optimization code opens them. Main deficits: global frequency baseline weak and progress confounded; sparse positives and correlated repeated states; wait conditional predictions and joint risk unconstrained; no authorized real-player data; incomplete ordered public history; empirical loss bins miss unobserved multiwinner tail. High global AUC does not establish reading discard order.

Actual round2 validation-only affine calibration: split by whole game (164 fit,196 evaluation). Wait Brier0.0570929→0.0565694, ECE0.0113643→0.0013063; risk Brier0.0118027→0.0117581, ECE0.00148694→0.00092222; tenpai Brier slightly worsened, so identity recommended. Selection policy in final CLI requires both held validation-half Brier and logloss nonworse and one strictly better. No test used for this choice.

A public-count-only2epoch run completed42.29s, validation AUC0.78506/AP0.15767. This already high public-count signal argues against assuming history neural complexity helps. B-F are queued by parent scheduler; their proxy definitions explicit in validation outputs, not full requested A-F. STOP checkpoint exit75 actually tested. Structured185-input smallMLP adds only legal tile/suit features; CPU shape and backward passed. Formal new-seed training and final evaluation delegated to parent scheduler to avoid GPU contention.

Reproducible CLI examples (run from project):

    .venv/Scripts/python.exe scripts/round2_model_ablation.py --manifest datasets/simulation_v2/manifest.json --variant B --epochs 2 --output experiments/round2_c/B --resume
    .venv/Scripts/python.exe scripts/round2_model_train.py --manifest datasets/round2/manifest.json --output checkpoints/round2_structured --epochs 8 --resume
    .venv/Scripts/python.exe scripts/round2_model_calibrate.py --manifest datasets/round2/manifest.json --checkpoint checkpoints/round2_structured/best.pt --output reports/round2_c_new_calibration.json
    .venv/Scripts/python.exe scripts/round2_model_final.py --manifest datasets/round2/manifest.json --checkpoint checkpoints/round2_structured/best.pt --calibration reports/round2_c_new_calibration.json --baseline checkpoints/round2_structured/baseline.json --output reports/round2_c_new_final.json
    .venv/Scripts/python.exe scripts/round2_model_summary.py --output reports/round2_c_summary.json

Resource estimate: one GPU job at a time,4 CPU threads, batch128, streaming JSONL, about0.5GB incremental VRAM; max8epoch job about3minutes plus final metrics. No giant model or broad hyperparameter search.

# Training log

2026-11-03: CUDA torch2.11.0+cu128 GPU forward/backward passed. Batch128 synthetic smoke passed.

Synthetic checkpoint/resume test executed scripts/resume_smoke.py: two synthetic epochs, optimizer state restored, CUDA RNG restored, inference checkpoint loaded on CPU. Artifacts under experiments/synthetic_resume are interface tests only and are NOT Mahjong-trained weights. Metadata dataset_version=SYNTHETIC-TEST.

Regression: scripts/metrics_smoke.py and scripts/model_smoke.py both passed after adding loss labels. Tie AP and ROC-AUC=.5 independent of tie order. Invalid metric inputs rejected.

No audited Mahjong data available yet; no formal Mahjong training started. Current labels and scores must be interpreted only under B's explicit simulator configuration. Loss bins must come from D/B configuration; default bins in network are placeholders for interface tests.

Formal simulator experiment started after data audit: scripts/train_evaluate.py datasets/simulation_v1/manifest.json --epochs 8. Actual CUDA training on RTX3060, 128 batch, 4 CPU threads; validation early stopping. Frozen dataset random plus uniform .65 peng policy only, no real-player claims. 76196 train states / 21802 validation / 10886 test. Test reserved until model selected and validation calibration complete. Current process active; no results asserted yet.

simulation-v1 completed: early stopping after epoch3, selected epoch0. CUDA actual training, seed42, hidden64, batch128, Adam lr0.001, patience3. Started approximately06:02 and completed06:04 (wall time approximate, no precise timer instrumented). GPU sample during training 36%/1781MiB including desktop; parent sample52C/1773MiB/freeRAM3.1GB. No peak resource claim.

Final test performed once. tenpai AUC0.67331 vs baseline0.51478, AP0.03059 vs0.01636. Conditional waits FAILED to beat baseline: logloss0.21302 vs0.20926. Risk logloss0.019892 vs0.019580, worse than baseline. 507 tenpai positives/32044 active target states; 164 deal-in positives/57410 legal candidates. These correlated states do not support independent-sample significance claims. Probability calibration only tenpai scalar temperature1.0262 on validation; joint risk remains uncalibrated. Retain frequency baseline for waits/risk. v1 artifacts frozen; no further final-test tuning.

simulation-v2 started with frozen audited 108795 states, four heuristic styles and test-only parameter combinations. Seed42, batch128, hidden64, Adam0.001, max8epochs/patience3. Validation-only temperature tuning; final test once after best validation selection. Per-game bootstrap planned for tenpai Brier delta; conditional-wait per tile and tenpai phase/style metrics included. No A-F history ablation completed. Score support learned from observed bins only, unseen multiwinner loss tail unvalidated; deploy research flags added. Baseline fallback masks exposed; caller remains responsible for legal action enforcement.

simulation-v2 completed8epochs, best7 val0.54708257. Final test once: 30455 active target samples,1491 tenpai positive; AUC0.766697 vs frequency0.514181, AP0.138869 vs0.050409. Tenpai Brier delta game-bootstrap95%CI[-0.00309103,-0.00130931],180 games,400 resamples seed42. Conditional wait AUC0.621027 vs0.551237 but Brier0.0594463 worse than0.0591750 and ECE0.014142 worse than0.001338. Risk AUC0.723937 vs0.549778, logloss0.0529683 vs0.0551333;536 positives/54551 legal candidates; not separately calibrated. Loss MAE0.0289978. Temperature0.978179 fit validation only. Phase tenpai AUC early0.7836/mid0.6535/late0.6498: no evidence that later always stronger. Style groups are opponent-style combinations, not per-opponent isolated tests. Frozen outputs, no repeated final-test tuning.

TorchScript CPU raw-logit export executed and parity-tested; Python wrapper required for calibration, flags and legality. No ONNX dependency installed/export performed.

第二轮自动实验最新结果已持久化到ROUND2_REPORT.md和reports/round2_automatic_results.json；策略有无改善以配对评估为准，不能将训练完成当作成功。


## 模仿基础策略后自对弈实验
{
  "imitation": {
    "means": {
      "heuristic": 0.445,
      "old_reading_risk": -0.8525,
      "trained_policy_value": -0.4675
    },
    "comparison": {
      "mean_difference": -0.9125,
      "paired_seed_cluster_bootstrap_95ci": [
        -1.225,
        -0.625
      ]
    },
    "clear_improvement": false,
    "scope": "configured_simulator_only"
  },
  "imitation_then_rl": {
    "means": {
      "heuristic": 0.5525,
      "old_reading_risk": -0.6975,
      "trained_policy_value": -0.32
    },
    "comparison": {
      "mean_difference": -0.8725,
      "paired_seed_cluster_bootstrap_95ci": [
        -1.27,
        -0.4775
      ]
    },
    "clear_improvement": false,
    "scope": "configured_simulator_only"
  }
}
只有独立配对区间下界大于0才标明确改善；失败方向保留记录，不宣布完整麻将AI成功。


## 候选结构残差自对弈实际结果
{
  "mean_difference": 0.0125,
  "paired_seed_bootstrap_95ci": [
    -0.3475,
    0.3675
  ],
  "simulation_only": true,
  "checkpoint_sha256": "a022c3df22b947da72d589753616c00b54b17df36867334493816d890303ad17",
  "flags": [
    "PAIRED_INITIAL_SEED_NOT_IDENTICAL_FUTURE",
    "RESIDUAL_EVAL_GREEDY_TRAIN_SOFTMAX"
  ],
  "clear_improvement": false
}
这是1000局训练后独立100种子组评估，不代表完整麻将AI；只学习舍牌，碰杠仍启发式。无明确正区间不标成功。

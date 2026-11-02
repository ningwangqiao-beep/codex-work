# Experiments

Only synthetic interface experiments completed: GPU tensor probe, MLP forward/backward, metric tie handling, temperature calibration and streaming checkpoint resume. No claim of reading opponents or beating statistical baseline.

Known limitations: score prediction is categorical over configured loss bins; supplied bins should cover exact configured loss values to prevent quantization ambiguity. Joint-risk and conditional-wait heads are independently supervised and can disagree; outputs expose marginal_disagreement and HEADS_NOT_PROBABILISTICALLY_CONSTRAINED. Calibration currently binary-temperature helper, not applied to untrained joint output. No real held-out accuracy or calibrated deal-in claims.

Pending: D's audited data, per-target active/candidate masks, complete independent test comparison and empirical frequency baseline, confidence intervals, trained calibration and deploy export.

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

模仿学习方向失败已保存完整证据：round2_warmstart_results.json。不要继续盲增自对弈局数。正在转向合法候选动作结构特征与向听/有效进张策略。

受限向听策略完整160局mean差+.15/CI[-.3125,+.6125]，未确认改进。候选线性teacher蒸馏完成，utility最优100%仅属于基础策略复现。新残差自对弈待冒烟和审计，不能提前声称成功。


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

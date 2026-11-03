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


## 新历史100训练局阶段真实开发对比
{
  "loss_control": {
    "status": "completed",
    "complete_seed_groups": 20,
    "summary": {
      "multitask": {
        "games": 80,
        "mean_net_score": 4.15,
        "win_rate": 0.5625,
        "self_draw_rate": 0.15,
        "deal_in_event_rate": 0,
        "deal_in_game_rate": 0,
        "mean_deal_in_loss": 0,
        "seat_mean": {
          "0": 4.75,
          "1": 3.75,
          "2": 4.6,
          "3": 3.5
        },
        "parts_mean": {
          "added_kong": -0.0125,
          "direct_kong": -0.0125,
          "gang_refund": 0.525,
          "discard_win": 0.925,
          "concealed_kong": -0.125,
          "cha_jiao_big": 1.2,
          "self_draw": 1.65
        }
      },
      "action_only": {
        "games": 80,
        "mean_net_score": 3.925,
        "win_rate": 0.55,
        "self_draw_rate": 0.1375,
        "deal_in_event_rate": 0,
        "deal_in_game_rate": 0,
        "mean_deal_in_loss": 0,
        "seat_mean": {
          "0": 4.8,
          "1": 4.25,
          "2": 3.65,
          "3": 3
        },
        "parts_mean": {
          "added_kong": 0.0125,
          "direct_kong": 0.0125,
          "gang_refund": 0.525,
          "discard_win": 0.925,
          "concealed_kong": -0.15,
          "cha_jiao_big": 1.1,
          "self_draw": 1.5
        }
      },
      "strong": {
        "games": 80,
        "mean_net_score": 4.0625,
        "win_rate": 0.675,
        "self_draw_rate": 0.1125,
        "deal_in_event_rate": 0.0125,
        "deal_in_game_rate": 0.0125,
        "mean_deal_in_loss": 0.025,
        "seat_mean": {
          "0": 4.4,
          "1": 3.55,
          "2": 4.9,
          "3": 3.4
        },
        "parts_mean": {
          "added_kong": -0.1,
          "direct_kong": -0.05,
          "gang_refund": 0.5375,
          "discard_win": 1.15,
          "concealed_kong": 0.05,
          "cha_jiao_big": 1.175,
          "self_draw": 1.3
        }
      }
    },
    "comparisons": {
      "multitask_vs_strong": {
        "paired_initial_seed_mean": 0.0875,
        "seed_bootstrap95ci": [
          -0.8125,
          1.0625
        ],
        "seed_differences": [
          -2.25,
          -1.0,
          -2.5,
          -2.5,
          -1.0,
          -3.0,
          1.5,
          -0.5,
          2.5,
          -2.0,
          -1.75,
          4.5,
          3.5,
          2.0,
          1.5,
          -1.25,
          2.5,
          -0.5,
          1.0,
          1.0
        ]
      },
      "action_only_vs_strong": {
        "paired_initial_seed_mean": -0.1375,
        "seed_bootstrap95ci": [
          -1.0625,
          0.775
        ],
        "seed_differences": [
          -2.25,
          -1.0,
          -4.0,
          -2.5,
          -1.0,
          -3.0,
          1.5,
          -0.5,
          2.5,
          -2.0,
          1.5,
          -0.75,
          3.5,
          2.5,
          1.5,
          1.25,
          2.5,
          -3.0,
          1.0,
          -0.5
        ]
      },
      "action_only_vs_multitask": {
        "paired_initial_seed_mean": -0.225,
        "seed_bootstrap95ci": [
          -0.9375,
          0.425
        ],
        "seed_differences": [
          0.0,
          0.0,
          -1.5,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          3.25,
          -5.25,
          0.0,
          0.5,
          0.0,
          2.5,
          0.0,
          -2.5,
          0.0,
          -1.5
        ]
      }
    },
    "limitations": [
      "random legal-discard opponents; claims/default other stages shared simulator",
      "paired initial deal does not imply identical future trajectories",
      "preference head not counterfactual Q; policy-conditioned V unused for choice",
      "20seed or smaller development sample; no strength promotion"
    ]
  },
  "relative_combo": {
    "status": "completed",
    "complete_seed_groups": 20,
    "summary": {
      "multitask": {
        "games": 80,
        "mean_net_score": 3.45,
        "win_rate": 0.525,
        "self_draw_rate": 0.0375,
        "deal_in_event_rate": 0.05,
        "deal_in_game_rate": 0.05,
        "mean_deal_in_loss": 0.125,
        "seat_mean": {
          "0": 3.9,
          "1": 3.1,
          "2": 3.5,
          "3": 3.3
        },
        "parts_mean": {
          "cha_jiao_big": 1.525,
          "discard_win": 0.85,
          "added_kong": -0.0625,
          "direct_kong": 0.075,
          "self_draw": 0.4,
          "concealed_kong": 0.2,
          "gang_refund": 0.4625
        }
      },
      "relative": {
        "games": 80,
        "mean_net_score": 4.8625,
        "win_rate": 0.7125,
        "self_draw_rate": 0.175,
        "deal_in_event_rate": 0.05,
        "deal_in_game_rate": 0.05,
        "mean_deal_in_loss": 0.125,
        "seat_mean": {
          "0": 4.45,
          "1": 5.85,
          "2": 4.75,
          "3": 4.4
        },
        "parts_mean": {
          "cha_jiao_big": 1.225,
          "discard_win": 1.0,
          "self_draw": 2.05,
          "added_kong": -0.05,
          "direct_kong": -0.0625,
          "concealed_kong": 0.125,
          "gang_refund": 0.575
        }
      },
      "strong": {
        "games": 80,
        "mean_net_score": 5,
        "win_rate": 0.7625,
        "self_draw_rate": 0.1875,
        "deal_in_event_rate": 0.05,
        "deal_in_game_rate": 0.05,
        "mean_deal_in_loss": 0.125,
        "seat_mean": {
          "0": 4.05,
          "1": 4.95,
          "2": 5.05,
          "3": 5.95
        },
        "parts_mean": {
          "cha_jiao_big": 0.9,
          "discard_win": 1.025,
          "self_draw": 2.35,
          "added_kong": 0.0375,
          "direct_kong": -0.025,
          "concealed_kong": 0.075,
          "gang_refund": 0.6375
        }
      }
    },
    "comparisons": {
      "multitask_vs_strong": {
        "paired_initial_seed_mean": -1.55,
        "seed_bootstrap95ci": [
          -2.675,
          -0.475
        ],
        "seed_differences": [
          -8.0,
          -2.5,
          -1.0,
          3.5,
          1.0,
          -0.5,
          1.0,
          -3.0,
          -0.5,
          -3.5,
          -2.0,
          -2.0,
          -3.25,
          -1.0,
          0.5,
          -5.0,
          0.25,
          1.5,
          -3.0,
          -3.5
        ]
      },
      "relative_vs_strong": {
        "paired_initial_seed_mean": -0.1375,
        "seed_bootstrap95ci": [
          -1.2625,
          0.7875
        ],
        "seed_differences": [
          -5.5,
          4.0,
          1.0,
          3.5,
          0.0,
          1.25,
          0.0,
          0.0,
          -0.75,
          0.0,
          0.5,
          1.0,
          -1.0,
          -1.5,
          0.0,
          -4.0,
          -2.0,
          3.5,
          -2.25,
          -0.5
        ]
      },
      "relative_vs_multitask": {
        "paired_initial_seed_mean": 1.4125,
        "seed_bootstrap95ci": [
          0.525,
          2.375
        ],
        "seed_differences": [
          2.5,
          6.5,
          2.0,
          0.0,
          -1.0,
          1.75,
          -1.0,
          3.0,
          -0.25,
          3.5,
          2.5,
          3.0,
          2.25,
          -0.5,
          -0.5,
          1.0,
          -2.25,
          2.0,
          0.75,
          3.0
        ]
      }
    },
    "limitations": [
      "random legal-discard opponents; claims/default other stages shared simulator",
      "paired initial deal does not imply identical future trajectories",
      "preference head not counterfactual Q; policy-conditioned V unused for choice",
      "20seed or smaller development sample; no strength promotion"
    ]
  },
  "scope": "development only; no final test tuning; no automatic promotion"
}
神经网络模仿改善不能代替净分证据；区间跨零不晋级；当前冠军不覆盖，1000/5000扩充另行受控。

## 1000局数据审计及GPU训练准入
生成第2次恢复成功exit0：1000train+20固定val，12372训练状态+235验证状态。主控inspect和D独立审计exit0，1020账本及120原始前缀全部核对。新训练器CPU STOP75/恢复与旧训练器同条件权重exact0差。已签reports/next_chief_scale_admission.json，仅6epoch/batch128/seed42监督研究；实际GPU训练由scheduler/next_history1000_training.json启动。新开发种子7200400..419已预注册，最终集未启用，冠军不覆盖。训练完成/指标以COMPLETE.json为准。

## 1000局版本实际训练及新开发评估完成
GPU(cuda)6epoch/582steps/60.05秒exit0，best_epoch5已冻结。12372训练状态，固定235验证。验证自由等价动作86.24% vs100局88.07%，rank regret .03759 vs .03114，扩充未显示收益。新7200400..419共240对局exit0：1000net3.7625，100net3.775，strong3.675；1000-strong +.0875 CI[-.9875,1.125]；1000-100 -.0125 CI[-1.1125,1.0875]，均无显著优势。点炮损失1000/strong均0（小样本），自摸净收益1.05/1.15，查叫净收益1.025/.875，不能只挑正指标。冠军不覆盖，5000/RL不放行，继续覆盖/标签诊断。完整101项测试exit0。

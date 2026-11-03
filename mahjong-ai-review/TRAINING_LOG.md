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

## 五组高级读牌消融正式启动
主控已检查实际gate、训练/评估实现、CPU STOP恢复证据及B四项信息屏蔽测试，签next_chief_opponent_admission_v1.json。独立本地队列scheduler/next_opponent1000_v1.json按顺序执行counts/progress/history/exchange/history_shuffled五组GPU训练及aux100评估；每组固定6epoch/seed42/batch128/19563 allocated参数，无并行重GPU。只训练1000train，不读取固定20val或aux记录训练，不挑epoch，不校准、不晋级。失败即停/保存断点，实际状态见experiments/next_opponent1000_v1/state.json；全部完成后REPORT.md自动保存各命令退出码。注意history仅现有token编码，非完整上下文；有效模型容量并不完全相同，风险仅52阳性、多响0，结论须保留限制。

## 五组读牌训练与评估真正完成
10个任务全部exit0，本地队列总360秒；每组6epoch/582更新，权重和预测已保存。听牌AUC约.75-.77，具体条件听口约.518-.524，合法候选风险约.710-.731；不是准确率。单看AUC点估计不能认证增量贡献，正在独立按整局配对比较并核标签与训练先验/公开规则基线。未晋级、未校准、未替换冠军。

## 读牌v1失败诊断与下一有界方向
五模型权重/预测/当前源SHA由主控核实；B四项独立标签测试exit0确认相对对手/bit映射正确、结构死听可为正；D整局配对指标重建exit0。C真实诊断：1593定缺花色项全为负，但网络仍分配约33%听口概率质量，flat81未学必零。counts定缺硬零后AUC .5213->.6911（程序规则能力）；train-only统计先验+定缺 .7157，missing/tile/known先验 .7610，公开非缺门未知张数加权 .8163（允许花色内 .7246）；不可把规则收益称训练收益。公开基线AUC更高但logloss不一定最好，禁止只挑指标。当前aux100已成为开发诊断集，不能当下一候选独立最终集。C实现逐对手逐tile共享特征v2，仍固定1000train/6epoch/582steps、未正式训练；D准备候选冻结后全新7120000..199独立200局验证，尚未生成。冠军未改/无RL。

## shared-tile v2实际启动
主控真实复核13591train+dev记录的static/history encoder及target_active相对顺序，exit0；B5tests、C真实STOP恢复exit0。已签next_chief_opponent_tile_v2_admission并启动scheduler/next_opponent_shared_tile_v2.json，15918参数，固定1000train/6epoch/582更新，单GPU；queue自动接开发aux100评估。定缺硬零为程序约束，known4不强制硬零。新fresh200未生成，等候选epoch5冻结后许可；C另新增holdout评估入口，不能修改训练gate或挑epoch。冠军不变。实际结果以experiments/next_opponent_shared_tile_v2/state.json和checkpoints/next_opponent1000_shared_tile_v2/COMPLETE.json为准。

## shared-tile v2实际训练/开发评估完成
train与development eval全部exit0，固定6epoch/582steps/15918参数。开发aux100条件听口AUC .79662（旧flat约.52），Brier .056727/logloss .203706；公开copyweight baseline AUC .81630/Brier .055078但logloss .219881，不能只挑排序指标认定胜负。missing硬零包含程序规则收益。新候选epoch5 SHAfb1a5bf797e1fe9fe17f176a76ace999598f02281123adade5a6395400e0e948已冻结；签next_chief_holdout200_approval预注册新7120000..199、四基线和主指标Brier/logloss/整局pairedCI，已启动独立本地生成+审核queue scheduler/next_opponent_holdout200.json。无校准/无选择/无晋级/无RL，fresh结果待实际评估。

## shared-tile v2独立200局真实结果（不晋级）
预注册fresh7120000..199生成/审计/唯一评估均exit0；2395状态，条件听口8883项/556阳性。v2 Brier .055697/LL .201828/AUC .773593；旧counts+missingzero .057890/.219089/.681987，整局paired Brier差CI[-.002744,-.001613]、LL[-.022555,-.011754]，说明不止missing程序规则提升。但与train-only统计prior Brier.056213/LL.204365两主指标差CI跨0，未证实超过简单统计；copyweight Brier.054663/LL.227173/AUC.789636，v2 LL较好而允许花色AUC更差(.64866vs.68596)。不能只选有利指标宣称成功，无实战晋级/无RL。下一步只准备公开prior+小残差的有界研究，尚未训练，旧fresh200已经消耗禁止复用为未来选择/最终集。
全量初次114tests有4error：B synthetic active与相对target不一致，被新增guard拒绝。只修test fixture，新增mismatch拒绝测试；115tests重跑exit0，保留原失败log，不放宽生产规则。

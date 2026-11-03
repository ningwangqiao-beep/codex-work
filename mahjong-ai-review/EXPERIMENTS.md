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

下一阶段：新历史100局数据上的损失对照未证明负迁移；候选相对特征+pairwise组合对teacher拟合和旧控制开发净分有改善，但未胜冠军，保留所有失败/非晋级证据。详reports/next_chief_stage_results.json、next_c_relative_fit_reliability.json。1000阶段待数据审计，5000训练局未获准，旧最终种子永久不再选择模型。

## 1000局边际数据阶段启动
已启动独立本地调度器 scheduler/next_history1000_generation.json，2个CPU生成进程，保留1536MiB空闲内存，最长1800秒，逐局提交可恢复。仅生成1000训练+固定20验证；训练仍需独立数据审计和新准入。冠军冻结，5000与RL未放行。实际进程与完成量以 experiments/next_history1000_generation/state.json 和已提交commit.json为准。

## 1000局数据审计及GPU训练准入
生成第2次恢复成功exit0：1000train+20固定val，12372训练状态+235验证状态。主控inspect和D独立审计exit0，1020账本及120原始前缀全部核对。新训练器CPU STOP75/恢复与旧训练器同条件权重exact0差。已签reports/next_chief_scale_admission.json，仅6epoch/batch128/seed42监督研究；实际GPU训练由scheduler/next_history1000_training.json启动。新开发种子7200400..419已预注册，最终集未启用，冠军不覆盖。训练完成/指标以COMPLETE.json为准。

## 1000局版本实际训练及新开发评估完成
GPU(cuda)6epoch/582steps/60.05秒exit0，best_epoch5已冻结。12372训练状态，固定235验证。验证自由等价动作86.24% vs100局88.07%，rank regret .03759 vs .03114，扩充未显示收益。新7200400..419共240对局exit0：1000net3.7625，100net3.775，strong3.675；1000-strong +.0875 CI[-.9875,1.125]；1000-100 -.0125 CI[-1.1125,1.0875]，均无显著优势。点炮损失1000/strong均0（小样本），自摸净收益1.05/1.15，查叫净收益1.025/.875，不能只挑正指标。冠军不覆盖，5000/RL不放行，继续覆盖/标签诊断。完整101项测试exit0。

## 独立高级读牌验证集
100局auxiliary验证7110000..7110099生成及独立审计exit0，1219状态；177结构听牌阳性来自56局，52合法候选风险阳性来自20局，多人风险阳性0。与train/固定val/dev/final隔离，16依赖指纹绑定，禁止混入训练与擅自校准。C继续准备公开计数/进度/完整历史/换三张/打乱历史等参数对照入口；尚未启动该组训练，不能声称读牌效果提升。

## 五组高级读牌消融正式启动
主控已检查实际gate、训练/评估实现、CPU STOP恢复证据及B四项信息屏蔽测试，签next_chief_opponent_admission_v1.json。独立本地队列scheduler/next_opponent1000_v1.json按顺序执行counts/progress/history/exchange/history_shuffled五组GPU训练及aux100评估；每组固定6epoch/seed42/batch128/19563 allocated参数，无并行重GPU。只训练1000train，不读取固定20val或aux记录训练，不挑epoch，不校准、不晋级。失败即停/保存断点，实际状态见experiments/next_opponent1000_v1/state.json；全部完成后REPORT.md自动保存各命令退出码。注意history仅现有token编码，非完整上下文；有效模型容量并不完全相同，风险仅52阳性、多响0，结论须保留限制。

## 五组读牌训练与评估真正完成
10个任务全部exit0，本地队列总360秒；每组6epoch/582更新，权重和预测已保存。听牌AUC约.75-.77，具体条件听口约.518-.524，合法候选风险约.710-.731；不是准确率。单看AUC点估计不能认证增量贡献，正在独立按整局配对比较并核标签与训练先验/公开规则基线。未晋级、未校准、未替换冠军。

## 读牌v1失败诊断与下一有界方向
五模型权重/预测/当前源SHA由主控核实；B四项独立标签测试exit0确认相对对手/bit映射正确、结构死听可为正；D整局配对指标重建exit0。C真实诊断：1593定缺花色项全为负，但网络仍分配约33%听口概率质量，flat81未学必零。counts定缺硬零后AUC .5213->.6911（程序规则能力）；train-only统计先验+定缺 .7157，missing/tile/known先验 .7610，公开非缺门未知张数加权 .8163（允许花色内 .7246）；不可把规则收益称训练收益。公开基线AUC更高但logloss不一定最好，禁止只挑指标。当前aux100已成为开发诊断集，不能当下一候选独立最终集。C实现逐对手逐tile共享特征v2，仍固定1000train/6epoch/582steps、未正式训练；D准备候选冻结后全新7120000..199独立200局验证，尚未生成。冠军未改/无RL。

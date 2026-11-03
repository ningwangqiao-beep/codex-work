# 当前验收结果（等待v2最终评估）

P0：独立Python3.12.14 / torch2.11.0+cu128，RTX3060真实矩阵前向与反向通过。
P1-P2：当前37项规则与数据测试主审复跑通过。仅RULES_PENDING.md假设配置，不认证微乐。
P3-P4：v1实际1000严格状态审计、10000性能；v2源码变更后重跑1000，前后指纹一致。1000和10000可能种子重叠，不累计互异局数。
P5-P6：v1 108884状态，v2 108795状态；各1800局完整game/source seed拆分、实际记录审计通过。无发现输入直接包含暗手或未来墙，但尚非形式化安全证明。
P7-P8：v1真实GPU训练4epochs，best epoch0；v2训练进行中。三个模型名是同一共享MLP多任务网络，不是独立训练三个架构。
P9：v1独立test听牌AUC .67331（基线.51478），条件听口logloss .21302（基线.20926，较差），风险logloss .019892（基线.019580，较差）。仅听牌温度校准，风险未校准。完整消融A-F、独立单任务对比尚未完成。
P10：本地PyTorch checkpoint推理实际加载通过。接口接128维公开features；还不是game_observation自动决策策略，没有ONNX。

现有证据不足以认定模型根据舍牌顺序学会读牌；未做完整消融，不能归因顺序。听口未超频率基线，保留基线。高风险与低频多响、未见规则事件、罕见番型是未充分覆盖范围；阶段差异需待分组结果，不作强结论。

代码/数据/模型/日志均在本工程各同名子目录；见README.md。训练日志TRAINING_LOG.md、实验EXPERIMENTS.md、问题BUG_REPORT.md、规则RULES_PENDING.md。

# 最终更新：simulation-v2 已完成

主智能体已实际读取最终评估JSON、八epoch日志，并成功加载v2 deploy.pt进行本地推理（3家/27听口/27候选风险输出形状正确）。v2训练76322状态、验证21774状态、独立测试10699状态（180局）。RTX3060实际训练8epochs，best epoch7。

| 指标 | 神经网络 | 训练频率基线 |
|---|---:|---:|
| 听牌ROC-AUC | 0.766697 | 0.514181 |
| 听牌AP | 0.138869 | 0.050409 |
| 听牌Brier | 0.044393 | 0.046596 |
| 条件听口ROC-AUC | 0.621027 | 0.551237 |
| 条件听口Brier | 0.059446 | 0.059175 |
| 点炮ROC-AUC | 0.723937 | 0.549778 |
| 点炮LogLoss | 0.052968 | 0.055133 |

听牌Brier差（模型减基线）按180整局400次bootstrap的95%区间[-0.003091,-0.001309]，只支持该测试模拟器下的概率预测改善。条件听口排序提高但Brier略差，不能声称全面优于基线。听口AUC提高约0.06979，LogLoss改善约0.000872，但未建立听口改善的区间。点炮有536/54551正例，神经网排序和LogLoss改善，仍没有专门概率校准，不能声称已校准风险。

听牌前/中/后期AUC为0.7836/0.6535/0.6498，不支持中后期一定更强；正例比例不同且缺少阶段置信区间，不能直接归因能力下降。完整舍牌顺序A-F消融未执行，因此不能回答是否真正依靠顺序读牌，也未证明改善出牌净收益。

可供下一阶段离线研究接口对接，尚不具备真实平台验证或可靠决策AI验收条件。研究包装保留wait/risk基线回退；调用者必须应用active/candidate合法掩码。score支持来自经验分值，罕见多人高损失尾部未验证。没有ONNX、完整八类对手、完整手型监督、多任务vs单任务比较或强化学习策略。

数据审计发现纯公开区已满四张仍有1605条结构死听标签，全部为非合法候选，风险训练candidate_mask屏蔽。标签定义为结构听口，不是可摸到的活张概率。当前没有发现直接输入暗手/未来信息；观察隔离和同源拆分测试通过，审计范围见D报告。

实际源码、配置、日志、数据、权重及报告保存在本工程；checkpoints/simulation-v2/deploy.pt为最新研究权重，simulation_v1为旧实验。虚拟环境不进入审计包。下一步应先扩规则证据与策略覆盖、做A-F消融、单任务对照与risk校准，再讨论RL。

准确批次种子范围以reports/employee_d_final_limits.md为准：v1审计0..999，性能100000..109999，数据200000..201799；v2审计300000..300999，数据400000..401799。此前关于1000与10000可能重叠的临时判断已被该范围记录纠正。

补充导出：C已实际导出checkpoints/simulation-v2/model_raw_logits.torchscript.pt并CPU原始logits一致性验证。导出不含温度校准/合法mask，需Python包装，不能单独作为决策策略。

# 第二轮状态（非项目结束）
第二轮已恢复，多智能体重新并发开发。主审实际复核旧数据/权重指纹、41tests、后台作业运行。六组受限特征实验全部执行；公开计数已接近复杂模型，不能声称序列编码更强。新的结构特征模型8epoch已完成并通过验证半组校准选择，独立新seed最终测试正在后台执行。
本地调度器已真实启动，不依赖会话继续采样生成文字；任务按配置顺序执行、失败停止。曾主动STOP测试保存exit75并从断点恢复，项目锁拒绝重复runner的实际验证通过。后续四座共享策略1000局与独立策略比较已经入队。
这不是整个项目验收通过。最终实际新结果将在ROUND2_REPORT.md汇总。完整麻将AI、攻防/碰杠学习、PPO和真实平台验证尚未完成。后台只能执行已配置程序，无法在AI额度耗尽后自主修改代码或发明新实验。恢复与状态路径见BACKGROUND_RUN.md。

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

已完成模仿300局及共享RL1000局新方向；模型对基础策略仍显著落后，不能标成功。48测试通过，向听随机300例交叉一致。未来结论须对进度强基线及基础算牌策略比较，不再以弱频率基线单独支持读牌能力。


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


## V3冻结独立评估实际结果
5000组新发牌、四座轮换、五冻结策略。不是新神经网络训练。各款项以ledger互斥对账，原始逐局JSONL保留。
{
  "status": "completed",
  "complete_seed_groups": 5000,
  "seconds": 9708.6915334,
  "summary": {
    "random": {
      "net": -1.7095,
      "win": 0.04405,
      "self_draw": 0.0099,
      "deal_in_events": 0.1354,
      "deal_in_loss": 0.351,
      "mean_winning_fan": 1.318955732122588,
      "parts_mean": {
        "added_kong": -0.0309,
        "self_draw": -0.3912,
        "direct_kong": -0.10015,
        "rob_kong_win": -0.0003,
        "concealed_kong": -0.0354,
        "gang_refund": -0.03595,
        "flower_pig": 0.0016,
        "discard_win": -0.2758,
        "cha_jiao_big": -0.8414
      }
    },
    "shape": {
      "net": 1.22665,
      "win": 0.2716,
      "self_draw": 0.0638,
      "deal_in_events": 0.1154,
      "deal_in_loss": 0.3017,
      "mean_winning_fan": 1.4477172312223858,
      "parts_mean": {
        "added_kong": -0.02475,
        "self_draw": 0.4072,
        "direct_kong": -0.13745,
        "rob_kong_win": 0.0009,
        "concealed_kong": -0.0642,
        "gang_refund": 0.29925,
        "flower_pig": -0.0024,
        "discard_win": 0.2063,
        "cha_jiao_big": 0.5418
      }
    },
    "old_candidate": {
      "net": 1.22665,
      "win": 0.2716,
      "self_draw": 0.0638,
      "deal_in_events": 0.1154,
      "deal_in_loss": 0.3017,
      "mean_winning_fan": 1.4477172312223858,
      "parts_mean": {
        "added_kong": -0.02475,
        "self_draw": 0.4072,
        "direct_kong": -0.13745,
        "rob_kong_win": 0.0009,
        "concealed_kong": -0.0642,
        "gang_refund": 0.29925,
        "flower_pig": -0.0024,
        "discard_win": 0.2063,
        "cha_jiao_big": 0.5418
      }
    },
    "old_residual": {
      "net": 1.54195,
      "win": 0.28725,
      "self_draw": 0.06905,
      "deal_in_events": 0.10965,
      "deal_in_loss": 0.2795,
      "mean_winning_fan": 1.487206266318538,
      "parts_mean": {
        "added_kong": -0.01195,
        "self_draw": 0.4972,
        "direct_kong": -0.0776,
        "rob_kong_win": 0.0003,
        "concealed_kong": -0.0318,
        "gang_refund": 0.2499,
        "flower_pig": -0.0016,
        "discard_win": 0.2722,
        "cha_jiao_big": 0.6453
      }
    },
    "new_baseline": {
      "net": 3.6048,
      "win": 0.64655,
      "self_draw": 0.16175,
      "deal_in_events": 0.0743,
      "deal_in_loss": 0.1815,
      "mean_winning_fan": 1.2753847343592917,
      "parts_mean": {
        "added_kong": -0.0194,
        "self_draw": 1.5038,
        "direct_kong": -0.0071,
        "rob_kong_win": 0.0034,
        "concealed_kong": -0.0008,
        "gang_refund": 0.3837,
        "flower_pig": -0.0048,
        "discard_win": 0.8095,
        "cha_jiao_big": 0.9365
      }
    }
  },
  "comparisons": {
    "random": {
      "mean_vs_shape": -2.93615,
      "paired_seed_ci": [
        -3.02405,
        -2.84695
      ]
    },
    "old_candidate": {
      "mean_vs_shape": 0.0,
      "paired_seed_ci": [
        0.0,
        0.0
      ]
    },
    "old_residual": {
      "mean_vs_shape": 0.3153,
      "paired_seed_ci": [
        0.24665,
        0.3825
      ]
    },
    "new_baseline": {
      "mean_vs_shape": 2.37815,
      "paired_seed_ci": [
        2.2845,
        2.46815
      ]
    }
  },
  "limitations": [
    "opponent discards configured by CLI; meld actions shared simulator",
    "win events not transfer count",
    "configured singlemax settlement; not verified room",
    "paired initial deal not identical future",
    "promotion_requires_chief_review_of_predeclared_final_evaluation"
  ],
  "primary_predeclared": "new_baseline vs shape",
  "no_training": true,
  "no_model_weights_replaced": true,
  "no_expert_claim": true
}
区间跨零即证据不足；该配置模拟结果不是现实高手认证。不得用本最终集继续调参。


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

## 1000局版本实际训练及新开发评估完成
GPU(cuda)6epoch/582steps/60.05秒exit0，best_epoch5已冻结。12372训练状态，固定235验证。验证自由等价动作86.24% vs100局88.07%，rank regret .03759 vs .03114，扩充未显示收益。新7200400..419共240对局exit0：1000net3.7625，100net3.775，strong3.675；1000-strong +.0875 CI[-.9875,1.125]；1000-100 -.0125 CI[-1.1125,1.0875]，均无显著优势。点炮损失1000/strong均0（小样本），自摸净收益1.05/1.15，查叫净收益1.025/.875，不能只挑正指标。冠军不覆盖，5000/RL不放行，继续覆盖/标签诊断。完整101项测试exit0。

## 五组读牌训练与评估真正完成
10个任务全部exit0，本地队列总360秒；每组6epoch/582更新，权重和预测已保存。听牌AUC约.75-.77，具体条件听口约.518-.524，合法候选风险约.710-.731；不是准确率。单看AUC点估计不能认证增量贡献，正在独立按整局配对比较并核标签与训练先验/公开规则基线。未晋级、未校准、未替换冠军。

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

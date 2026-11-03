# V3统一净得分基准

实际20seed3600000..3600019，轮换四座，每政策80完整局，总320局。对手随机合法舍牌，共用模拟器碰杠；不是全动作随机。命令scripts/v3_data_compare.py --games 20 --seed 3600000 --timeout 120，exit0，3.973秒。六源起止hash相同。所有逐局分项/胡事件指标/legacy权重hash保存在reports/v3_d_compare_3600000.json和jsonl。

|政策|每局净分|相对shape差|seed组bootstrap95CI|
|---|---:|---:|---|
|随机|0.075|-2.775|[-4.1625,-1.575]|
|shape|2.85|0|基准|
|旧candidate|2.85|0|[0,0]|
|旧residual|3.525|0.675|[-0.75,2.0]|

旧residual点估计较高但置信区间跨零，不晋级，不声称V3训练成功。旧candidate精确复现shape。小样本不是用户最终5000局测试。旧value/risk数值未解释成V3分数，只合法舍牌迁移。事件计数来自win_events，不是selfdraw多付费ledger条数；各类杠/退税/查叫/花猪按ledger金额单独统计。

规则配置cha_jiao_mode=max_wait_payment默认大叫；小叫和disabled有独立配置及单测，本次未做这些模式基准，仍不代表微乐房间验证。


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

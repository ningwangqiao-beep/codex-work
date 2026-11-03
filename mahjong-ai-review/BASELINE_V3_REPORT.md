# Baseline V3实际报告

新Bot是规则计算，未训练。逐候选合法性、缺门债务、修复后的standard/七对结构向听、有效进张、有限两次摸牌、牌型潜力和公开弱风险。两摸仅2首摸×2中间舍×2第二摸，概率是公开未知均匀近似，不是实际牌墙真概率。精确legal_progress尚未用于分支，定缺清理仍单列debt。

v3_memo与v3_bot新增规范化有界缓存，没有回滚第五张修复。5数据/memo测试真实通过1.885秒，含第五张反例与原算法effective一致。单次重复决策cold .484秒/warm .000188秒，只证明相同输入缓存，不代表整局提速。

1000严格审计：seed3200000..3200999，120860steps，3.065秒，exit0。10000独立性能：seed3300000..3309999，1210107steps，29.316秒，exit0。4spawn，六源前后hash一致，逐局ledger完整持久化；主审另行独立复验见v3_chief_batch_recheck.json。

强Bot完整局2seed小吞吐仍有界运行，未提前计作完成。B在另文件优化exact DP，当前不能用冷向听瓶颈掩盖正确性或盲扩训练。无新RL/训练，无best覆盖。

更新：旧memo强Bot2seed完整局实验实际超时68.785秒、0完整配对组，不算完成。B新增NumPy exact fast模块后，独立v3_bot改为opt-in此算法；真实2seed×4座×5政策=40完整局3.978秒exit0，不是同一决策热缓存速度。新20seed有界验证继续运行，不作提前成功。原比较CLI失败会exit2，修复过一次生成换行SyntaxError，修复后退出0。

## fast强Bot开发评估
20seed3900000..3900019×4座×5政策=400完整局，37.608秒exit0。new_baseline每局4.525，shape4.1125，差+.4125，完整seed组95%bootstrap CI[-1.8875,2.5]跨零；不晋级，不称优于shape。旧residual3.8625，candidate4.1125，random-.325。分项与逐局保存在v3_d_compare_3900000.json/jsonl。

## 可恢复mixed评估CLI
scripts/v3_data_resumable_compare.py支持--opponents mixed（公开合法random/shape/pure/defensive轮换），参数固定未按评估调；--resume只保留完整seed组重新跑未完整组，绑定seed/总局数/六源码/额外Bot与fast/script/旧权重。final结果不可覆盖。实际测试中断exit2→恢复exit0→再次恢复final拒绝exit1，日志v3_d_resume_*及v3_d_immutable_reject.log。两次小mixed测试只验证接口不作强度结论。

5000seed×4座×5政策按此随机对手开发吞吐线性约2.61小时，mixed状态分布和缓存成本不同需留余量；未启动最终大评估。由主审独立runner决定。


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

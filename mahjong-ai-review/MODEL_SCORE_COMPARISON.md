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

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

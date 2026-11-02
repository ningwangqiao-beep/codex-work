# Candidate residual smoke

Fixed teacher base、零初始化有界残差、候选temperature=1 softmax，各座按自身终局scores/48训练小value。四座共享自对弈，CPU2线程。非PPO。

旧raw-base smoke20局恢复22局保留在round2_candidate_rl，不用于新源续跑。C修复rounded base且验证1809动作零偏差后，新round2_candidate_rl_rounded实际20局恢复到22局通过。源码binding包含4规则/观察源、candidate特征/Residual/learning/CLI、base权重和audit哈希。STOP实测exit75，22局断点保留。

旧2seed eval仅接口冒烟，不能作为提升结论；新正式评估预定seed2600000，未根据旧结果修改策略权重或temperature。训练softmax，部署eval greedy，报告显式标示。

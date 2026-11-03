# 隐藏状态约束采样原型

search/next_hidden.py仅接观察dict，不接Table，不读取真实wall或真实对手手牌。随机约束先验，不是概率校准后验，不用于rollout/Q训练。

支持明确schema：concealed_hand_sizes四座（含已胡暗手归档）、public exact remaining_wall_information、当前弃牌/公开面子/归档赢牌实体牌、自身暗手、active和定缺。若缺数量或已胡档案未明确完整，直接UnsupportedObservation。当前实战V3观察未提供这些全部显式数量，所以不能直接接入并冒精确采样。

未知暗杠必须[-1]*4整体分配同一牌四张；不会分成四个随机牌。已胡手牌仍占未知库存，不从池移除。每样本验证108实体牌及每种四张。自身手牌保留。定缺未清不假定对手已绝缺；换出牌只历史setup证据，未当永久hold约束。

当前不强制已胡暗手结构与番型事件相容，也未按舍牌/策略拟合权重，未做听口约束后验推理；必须保持prototype标识，不能作为完整合法局面重建或已校准读牌。未来需增加档案合法成胡结构/公开事件约束，再准入MC。

实际5tests通过0.011秒exit0：100样本可复现/守恒、反事实隐藏/未来poison键无影响、缺尺寸拒绝、inactive档案拒绝与计入、100暗杠同牌样本。日志next_d_hidden_tests.log。未扩大teacher数据、未rollout、未训练/RL。

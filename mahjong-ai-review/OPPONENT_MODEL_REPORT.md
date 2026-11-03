# Opponent Model Report — V3

## 当前结论

尚未证明模型通过完整舍牌历史获得稳定的额外读牌收益，也没有真实玩家泛化证据。旧规则的概率、损失和score bins不能直接解释成V3分数。V3本轮完成了共享完整历史编码器和小规模T2辅助头训练，尚不是通过独立检验的高手OpponentNet。

## 已核对的旧证据

C独立加载并计算SHA256：17份旧权重/导出文件、3份旧数据manifest及实际分片和规则快照；见reports/v3_c_legacy_inventory.json/.log/_exitcode.txt（exit0）。旧模型及失败实验没有删除或覆盖；新V3数据/权重显式排除在legacy inventory之外。首次清单另留v3_c_legacy_inventory_initial.json。

旧自由舍牌28%已在固定验证seed1800000..99复核：exact28.00%，utility-equivalent33.28%，低准确率大部分不是同分误判。逐候选线性模型同组等效100%，仅证明复现简单teacher。旧残差净差+0.0125、95%CI[-0.3475,0.3675]来自已保存round2_candidate_summary.json，不能声称提升，更不能作为V3收益结果。

旧v2仅公开牌总量排序已达validation AUC0.786475；计数A网络0.785057。保持总量、均匀化27计数后AUC0.785993，预测相关0.981555。train拟合的进度强概率基线下，旧C/D的Brier改善区间跨零；D加最近动作后未胜C。证据为round2_c_shortcut_v2.json、round2_c_count_representation.json、round2_c_progress_baseline.json。这些是旧规则诊断，未拿旧final继续调参。

## V3输入与模型

模型models/v3_action_value.py，20,349参数：共享state191编码、全长公开事件GRU16、逐候选Calculator特征编码、动作偏好/状态V头，以及structural-tenpai、27维conditional-wait、八类联合赢家mask辅助头。

state191=旧128摘要+自身送出27计数+自身收到27计数+方向4+来源座位4+公开墙量已知标记1。旧摘要仍有last11/timecap216，但另有独立可变长完整历史分支，不把摘要冒充完整序列。实际T2数据最长134事件；CPU接口实际验证257事件和空历史padding，未做64硬截断。证据v3_c_interface_smoke.json/.log/_exitcode.txt。64与词表修正前证据另存，未丢弃。

history token=(action_id,relative_player,tile+1)。普通公开摸牌的牌种全部擦除，对手暗杠牌种擦除；draw次数和玩家仍保留。词表保留missing_declared/self_win/discard_win/rob_kong_win等区别，真实event词汇初版缺项已修复。自身换三张信息是过去已知交换事件，不作为对手当前仍持有的硬约束；本轮没有实现贝叶斯动态粒子推断。

合法观察编码器inference/v3_observation.py忽略隐藏手牌、未来墙序。fixture poison测试、真实1204样本重新编码一致性及own+public无第五张检查均独立执行通过；不等于已经证明所有未来数据管线安全。

## T2标签和辅助头边界

数据100新V3游戏seed4200000..4200099，80train955状态/20validation249状态，整局/seed/deal_group拆分。动作标签是强开发Bot的lexicographic preference rank，绝不是候选动作终局Q。状态V标签是一旋转BaselineV3座位对三冻结模拟策略的实际终局raw V3净分，不是全四teacher、不固定除48，也不是新网络自身policy的V。

辅助标签明确为structural/legal-hand waits（缺门和自身物理约束），不等于公开剩余牌约束下的effective听牌。27听口不是互斥类别；条件wait只在active且听牌目标上监督。joint8 mask保留多人相关性，不以三个边际相加。

实际标签量：

|切分|active目标|听牌阳性|条件wait元素/正例|合法候选/点炮正例|多人正例|
|---|---:|---:|---:|---:|---:|
|train|2811|139|3753/204|4833/37|2|
|validation|705|34|918/57|1283/12|0|

这些同局状态相关，正例尤其多人风险很少。辅助头loss下降不能证明复杂读牌、概率校准或高风险尾部正确。当前V3辅助概率未单独校准，没有独立V3 A-F消融、风格识别、受约束暗手分布或完整T3测试。

## 合法迁移包装与收益边界

inference/v3_legacy.py加载旧static/candidate/residual，仅迁移合法舍牌；旧state value/risk/loss不进入V3金融结论，并明确不编码新exchange/fullseq。fixture三类合法+hidden/future不变验证exit0；D可在同V3规则做旧策略净分基准，C不把只读D报告冒充亲自重跑。

新T2完整开发对局20seed4400100..4400119、四座轮换、240局（三策略各80局，对手为固定随机合法舍牌策略族）：新网络3.6125分/局，强开发Bot4.4375，shape3.6125。网络减强Bot=-0.825，整seed95%CI[-1.6875,0.1]；减shape=0，CI[-1.45,1.3125]。无提升证据，不晋级。账本逐局和四家总和均核对；配对初始牌局不等于未来轨迹相同。该20seed只是开发集，不是5000seed最终检验；没有访问预注册5000000..5004999最终集。

## 下一项最小研究

先冻结本次失败/未晋级权重。T3应在新V3 train/validation上比较进度强基线、无历史、完整历史、保持计数不变的历史顺序扰动，并以整局聚类置信区间检验增量。换三张和style只能作各自独立控制变量；模拟style标签不可直接作为真实决策输入。当前没有证据支持扩大Transformer或直接开RL。

T4若学习动作终局价值，需要受约束隐藏状态采样、已知交换事件随公开证据更新、当前合法动作反事实rollout与V3完整账本回报。当前偏好rank和teacher-policy V不能冒充这项能力。规则/基线虽通过本轮准入，但价值和收益提升未通过，RL继续禁止。

## 后续只读发现：事件覆盖并未完成认证

完成T2后进一步逐分支阅读冻结simulator/v3_selfplay.py发现：抢补杠成功时resolve_added_kong(winners)后未向public_history追加rob_kong_win；直杠在Table.claim内补摸，但history只追加exposed_kong，没有独立draw记录（暗杠和成功补杠则显式draw）。直杠补摸可由规则推知，但记录粒度与其他杠不一致。

因此本文fullseq仅指“对输入中已提供history prefix不设last11/64截断”。history_original_length一致、134真实长度和257接口stress不能证明源引擎逐项覆盖所有公开事件，也不能替代完整历史审计。当前源为预注册最终评估冻结，不由C修改；问题已通知主审与D，下一源版本应补全/明确事件语法后重新审计、绑定数据。当前T2权重和本轮失败证据保留，不据此宣称完整T3读牌能力。

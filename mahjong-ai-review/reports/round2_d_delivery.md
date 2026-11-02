# Round2 D 交付

新数据107645状态，1800整局，seed800000..801799。train75521 validation21506 test10618。1000严格审计seed700000..700999；逐动作牌数/收益/手牌阶段检查通过。四源码前后指纹相同，snapshot冻结。全部为假设规则模拟。

新增公开draw（不含摸牌身份）、胡牌、暗杠/补杠事件；对手暗杠牌用-1占位且不编码身份。数据中observation/feature是合法输入，tenpai/waits/loss等为监督字段，不能将整行作特征。3观察隔离测试实测通过。当前feature对新action主要降级unknown编码，尚非完整序列表示。

策略callback只得到合法观察快照和合法候选tuple，不传Table。PolicyValue为discard-only actor-critic：一个学习座位对三启发式对手，不是四学习agent自对弈，不是PPO。碰杠沿规则启发策略。真实31局初版训练及30局绑定版训练已执行；bound版保存optimizer、torch/Python随机状态、seed和4源码hash，atomic临时文件替换checkpoint；恢复到总games语义已实跑20->30。遗留未绑定权重拒绝resume。

MAHJONG_STOP_FILE在每局开始检查并exit75；前一完整局checkpoint已持久化，停止不会覆盖有效断点。当前实现stop在零局时无checkpoint，属于尚未训练状态。

小型策略比较真实执行20seed*4座*3政策=240局；同初始seed和轮换座位配对，策略会改变后续局面，不保证相同未来轨迹。少量局数仅接口试验，无强弱或收敛结论。评估日志round2_d_trained_policy_eval.json。

未完成：4学习座位共享策略；prediction旧模型风险policy比较；完整结构标签；历史含公开动作但无对手摸牌身份（正确隐藏）；未核实微乐规则。C负责独立读牌消融/校准，新test未用于D模型调参。

## 追加四座共享训练

实际规则/观察/selfplay四源码审计前后指纹不变，全部测试日志hash绑定，并真实1000局120887步骤。训练入口拒绝缺失/不匹配审计及少于1000审计局；resume绑定seed、模式、source和audit哈希。

共享四座实际50局训练并恢复到55局；每座决策单独归属observer，采用该座终局scores[q]/48，四座奖励不混用。CPU2线程。STOP文件实测退出75，55局checkpoint保持。不是完整PPO，未证明策略提升。

后台续跑命令：

    .venv/Scripts/python.exe scripts/round2_data_policy.py --games 1000 --selfplay --audit reports/round2_d_policy_audit.json --out checkpoints/round2_shared_policy --resume checkpoints/round2_shared_policy/last.pt

--games是累计总局数，不是追加局数。改规则/观察/selfplay后必须重审。checkpoint通过last.tmp原子替换last.pt。

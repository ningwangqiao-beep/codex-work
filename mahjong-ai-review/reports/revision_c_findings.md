# 修订 C：逐候选架构与模仿指标独立审计

## 实际执行与证据

已执行CPU2审计，未训练网络、未启用GPU、未启动RL、未打开任何冻结final test。验证重放采用既定validation seeds1800000..1800099；teacher只看自身手牌和公开观察。耗时26.72秒，实际退出码0。

- 可复现脚本：scripts/revision_model_teacher_audit.py。
- 完整指标及checkpoint/source SHA256：reports/revision_c_teacher_audit.json。
- 实际输出日志：reports/revision_c_teacher_audit.log。
- 实际进程退出码：reports/revision_c_teacher_audit_exitcode.txt（0）。

命令：

    .venv/Scripts/python.exe scripts/revision_model_teacher_audit.py --seed 1800000 --games 100 --output reports/revision_c_teacher_audit.json

本次是已定义验证牌局的独立重新审计，不是新独立最终性能测试；candidate未用这些seed训练，旧imitation的28%指标也在同一验证组直接复现。

## 28%是否只是utility同分被误判

自由舍牌共2939个决策，teacher有1272个多最优候选状态。

|模型|exact|utility-equivalent|top3 exact target|top5 exact target|平均teacher utility regret|
|---|---:|---:|---:|---:|---:|
|旧128输入模仿模型|823/2939=28.00%|978/2939=33.28%|57.88%|78.05%|1.76761|
|逐候选线性raw|2675/2939=91.02%|100%|99.56%|100%|0|
|逐候选整数utility稳定tie|100%|100%|100%|100%|0|

旧模型2116次exact失败中，155次是同效用但不同动作，1961次确实选择较差teacher utility。只有约7.33%的旧exact失败可以用同分解释；因此不能把28%主要归因于评估tie bug。旧模型最大regret7。candidate raw则264次exact失败全部是同效用不同动作，最大regret0；此处raw约91%确实主要受浮点tie影响。整数utility是该明确teacher监督目标，不是任意模型可随意取整的通用规则。

exact定义是与按给定legal顺序选择的teacher argmax完全同牌；equivalent定义是候选teacher utility等于最优值；topk使用稳定降序模型候选评分、检查该唯一teacher代表动作是否在前k；regret=最优teacher整数utility减所选候选utility。候选数少于k时topk自然较容易，不能把top5当强策略证明。

## 按structural shanten分组

下表为自由舍牌，按决策前14等价手牌的minimum structural shanten分组。计算使用rules/hand_analysis.py，源SHA已记录；它是本地实现而非独立权威oracle，不能当作该向听算法已经完整认证。

|shanten|样本数|旧exact|旧equivalent|旧平均regret|candidate rounded exact/equivalent|
|---|---:|---:|---:|---:|---:|
|0|994|30.99%|38.43%|1.59859|100%/100%|
|1|1568|27.30%|31.12%|1.86288|100%/100%|
|2|372|22.31%|27.96%|1.83333|100%/100%|
|3|5|80.00%|80.00%|0.60000|100%/100%|

shanten3只有5状态，不适合下结论。这里只按向听分组审计teacher模仿，不把3*pairs+links启发式等同于最小向听或最优进张策略。

## 对照逐候选架构要求

已实现：同一个12维线性打分器逐合法候选共享参数；候选特征只来自own/public，包括舍后pairs、links、triples、sequences、缺门数、singleton数、candidate公开/自有数量等。teacher utility作为回归目标，模型权重恢复解析pair/link系数；无须更大网络。部署采用公开白名单、合法候选交叉校验和稳定tie。

尚未实现或未认证：真正effective_draws/ukeire不是当前12维特征；没有强Bot长期收益优势证明；没有完整价值网络审计；风险头/损失尾部/teacher与RL目标不一致尚需独立验证。该线性模型只证明可拟合基础启发式，不是自主发现更强麻将策略。

核对既有candidate证据：reports/round2_c_candidate.json的30局validation中886自由舍牌，utility最优/整数tie一致均100%；本次额外100验证局2939自由舍牌也达到同样结论。reports/round2_c_candidate_game_parity.json中20新seed×4座=80完整局、1186受控决策，zero action mismatch且每局scores向量相同；它证明teacher复现，无收益提升。reports/round2_c_candidate_zero_residual.json另有1809合法决策（886自由）零残差greedy与部署teacher零偏差，修复了旧unrounded residual的tie差异。reports/round2_c_candidate_resume.json及round2_c_candidate_stop.json记录实际CLI恢复/STOP与不中断控制参数一致。

## 修订后的准入结论

遵守用户收紧的门槛：规则、强Bot、价值网络审计完成前不再启动RL。本次没有任何新RL或GPU训练。candidate基础teacher拟合可视为通过一项表示与监督目标检查，不能替代规则审计、强Bot审计或价值目标审计。只收到用户列出的Claude S0-S12条目，没有完整对应源码，因此不能声称已经审计或复现整个S0-S12系统。

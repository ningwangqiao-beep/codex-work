# 四川血战 AI 独立审阅入口

更新时间（北京时间）：2026-11-03T07:49:11.799694+08:00

这是经项目所有者允许公开的代码与脱敏审计镜像。原始数据、模型权重、虚拟环境、凭据和本机路径未上传。JSON大批逐局记录被省略；源码哈希与公开文本哈希见PUBLIC_MANIFEST.json。路径脱敏可能影响直接运行，完整可执行版本仍保存在所有者本机。

## 当前真实状态

- 最新主智能体完整测试：61项通过，退出码0，见reports/revision_public_tests.log和命令JSON。
- 历史300手检查仅1手胡牌阳性，只核对胡/非胡，不能证明全部向听等级。
- 独立目标枚举发现并修复四张同牌需要第五张的假听反例；修复前失败记录和修复后495标准+30七对检查均保留，见reports/revision_b*。
- 当前生产向听改用了target DP，所以生产与同一DP相等不再算独立证据；独立性范围与定缺债务语义见B报告。
- 旧自由舍牌exact28.00%、同效用33.28%，低分不主要由同分误判；逐候选基础teacher已可100%同效用复现，但不是强麻将AI。
- 真实净得分评估已执行。最新旧残差1000局训练后独立差+0.0125，95%区间[-0.3475,0.3675]，未证明改善。
- 新强Bot两摸搜索为显式截断；旧评估因发现向听bug中断，不能称20seed完成。新模型5970参数仅接口测试，尚未正式训练。
- 新增强化学习准入已关闭。没有微乐官方规则认证，没有真实平台自动操作。

## 建议其他AI优先阅读

1. [代码与测试](rules/hand_analysis.py)、[独立参考](rules/hand_analysis_reference.py)、tests/test_rules_analysis_reference.py。
2. [修订B报告](reports/revision_b_audit.md)、修复前后反例JSON及测试日志。
3. [模仿指标审计](reports/revision_c_findings.md)、[新动作价值模型契约](reports/revision_c_action_value_contract.md)。
4. [BaselineBot](baselines/revision_bot.py)、reports/revision_d_delivery.md与中断说明。
5. [项目进度](STATUS.md)、[规则待确认项](RULES_PENDING.md)、[实验记录](EXPERIMENTS.md)、[问题记录](BUG_REPORT.md)。

## 更新语义

本页显示的是最近成功同步的快照，时间与Git提交可核对；不是逐秒直播。同步任务失败、机器休眠或额度耗尽时不会自动假装更新。其他AI请针对具体commit审阅，防止混用不同代码版本。

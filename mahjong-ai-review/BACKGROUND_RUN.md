# 本地后台实验与恢复

调度器是独立Python程序，不依赖AI继续回答。电脑需保持开机；休眠/关机时不会计算。它只能执行已配置任务，不能自行发明实验或修复代码。

实时状态：experiments/round2_followup/state.json；各任务日志同目录*.log；资源采样resources.jsonl。pid以state.json为准，外层Python启动器PID可能不同。当前队列依次：结构特征模型训练→校准→新seed独立测试→四座共享策略累计1000局训练→100seed轮座位三策略评估→报告→审计包。

恢复（在工程目录PowerShell）：

    .\.venv\Scripts\python.exe scheduler\runner.py scheduler\round2_followup.json

只能启动一个runner。项目级锁防并发；实际样本审计和规则指纹不匹配会停止。失败需先读*.log解决根因，再恢复；任务脚本有--resume，已完成任务不重复。修改已经完成的任务定义会拒绝复用成功结果，需要新的实验目录。

安全停止：

    Set-Content experiments\round2_followup\STOP 'user stop'

runner先请求checkpoint（最多等待30秒），训练在batch/整局边界保存后退出；如果进程无法响应，保留最近断点并终止该任务。恢复前移除STOP。不要删除其他项目文件。

资源上限：单队列单任务；GPU总显存7000MiB、温度80℃、最低可用RAM0.8GB，CPU训练4线程/策略2线程，最多6小时；GPU监控失效停止。记录GPU和RAM，不声称有CPU温度传感器监测。检测存在采样间隔，不能保证OS绝不波动。

源码门槛：任务指纹+数据与规则审计绑定；任何失败后不继续下游。报告为研究结果，不代表完整麻将AI验收。无法自动修复的新错误需下一次AI会话诊断。

## 当前有效后台队列（覆盖前文旧路径）
之前round2_followup和warmstart队列都已实际完成；其旧摘要证据保留，不建议按新runner直接resume旧state。
当前有效队列：scheduler/round2_candidate_queue.json。
实时状态：experiments/round2_candidate_queue/state.json，日志同目录；后台runner实查pid44156，训练child37324，已观察到第283局。采用项目锁、递归静态import指纹、原子checkpoint和append-only attempts.jsonl。
恢复命令：

    .\.venv\Scripts\python.exe scheduler\runner.py scheduler\round2_candidate_queue.json

停止文件为experiments/round2_candidate_queue/STOP。默认CPU2、RAM最低1GB、80℃与显存7000MiB、4小时deadline；只执行已配置1000局残差自对弈→100独立seed组greedy对比→报告→审计包。机器休眠时不会继续计算。

## V3当前本地后台入口
当前独立长期评估：scheduler/v3_frozen_evaluation.json，状态experiments/v3_frozen_evaluation/state.json。恢复：

    .\.venv\Scripts\python.exe scheduler\runner.py scheduler\v3_frozen_evaluation.json

STOP文件experiments/v3_frozen_evaluation/STOP。逐完整seed组恢复，不保证被中断seed内部不重复。100000局最终评估后自动保存报告及审计包；规则/模型/数据hash变化会拒绝继续。不可在该最终集调参。该队列仅评估五个预注册冻结策略，不训练或自动发明算法。新T2小监督由单独已批准任务执行，GPU主训练最多一个。

## 1000局边际数据阶段启动
已启动独立本地调度器 scheduler/next_history1000_generation.json，2个CPU生成进程，保留1536MiB空闲内存，最长1800秒，逐局提交可恢复。仅生成1000训练+固定20验证；训练仍需独立数据审计和新准入。冠军冻结，5000与RL未放行。实际进程与完成量以 experiments/next_history1000_generation/state.json 和已提交commit.json为准。

1000局生成第1次运行exit75，354个训练局目录已保存；资源保护触发路径（生成器只在STOP或空闲内存<1536MiB时exit75；未发现STOP文件）。主控复查空闲约4.8GiB后从已提交分片恢复，不降低保护阈值。不能称1000完成。

## 1000局数据审计及GPU训练准入
生成第2次恢复成功exit0：1000train+20固定val，12372训练状态+235验证状态。主控inspect和D独立审计exit0，1020账本及120原始前缀全部核对。新训练器CPU STOP75/恢复与旧训练器同条件权重exact0差。已签reports/next_chief_scale_admission.json，仅6epoch/batch128/seed42监督研究；实际GPU训练由scheduler/next_history1000_training.json启动。新开发种子7200400..419已预注册，最终集未启用，冠军不覆盖。训练完成/指标以COMPLETE.json为准。

## 1000局版本实际训练及新开发评估完成
GPU(cuda)6epoch/582steps/60.05秒exit0，best_epoch5已冻结。12372训练状态，固定235验证。验证自由等价动作86.24% vs100局88.07%，rank regret .03759 vs .03114，扩充未显示收益。新7200400..419共240对局exit0：1000net3.7625，100net3.775，strong3.675；1000-strong +.0875 CI[-.9875,1.125]；1000-100 -.0125 CI[-1.1125,1.0875]，均无显著优势。点炮损失1000/strong均0（小样本），自摸净收益1.05/1.15，查叫净收益1.025/.875，不能只挑正指标。冠军不覆盖，5000/RL不放行，继续覆盖/标签诊断。完整101项测试exit0。

## 独立高级读牌验证集
100局auxiliary验证7110000..7110099生成及独立审计exit0，1219状态；177结构听牌阳性来自56局，52合法候选风险阳性来自20局，多人风险阳性0。与train/固定val/dev/final隔离，16依赖指纹绑定，禁止混入训练与擅自校准。C继续准备公开计数/进度/完整历史/换三张/打乱历史等参数对照入口；尚未启动该组训练，不能声称读牌效果提升。

## 五组高级读牌消融正式启动
主控已检查实际gate、训练/评估实现、CPU STOP恢复证据及B四项信息屏蔽测试，签next_chief_opponent_admission_v1.json。独立本地队列scheduler/next_opponent1000_v1.json按顺序执行counts/progress/history/exchange/history_shuffled五组GPU训练及aux100评估；每组固定6epoch/seed42/batch128/19563 allocated参数，无并行重GPU。只训练1000train，不读取固定20val或aux记录训练，不挑epoch，不校准、不晋级。失败即停/保存断点，实际状态见experiments/next_opponent1000_v1/state.json；全部完成后REPORT.md自动保存各命令退出码。注意history仅现有token编码，非完整上下文；有效模型容量并不完全相同，风险仅52阳性、多响0，结论须保留限制。

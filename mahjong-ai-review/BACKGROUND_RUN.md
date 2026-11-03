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

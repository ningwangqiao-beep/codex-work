# 1000边际数据准备（只冒烟，未启动1000）

新增scripts/next_data_scale.py，未改冻结100代码或数据。永久train7000000..7000999，固定val7100000..7100019；5000不支持。最多2spawn worker、最多2在途future；每局records.jsonl/game.json/commit.json写临时目录，最后原子rename为seed目录。resume逐局核source/seed/config与records/game内容SHA，完整commit跳过，未commit临时文件重算。

实际4train+2val冒烟：6局75状态（44/31），5.741秒exit0；六局全部字段与冻结100阶段canonical原始input/labels精确相同。再resume不重跑，0.535秒exit0。1000无chief源码绑定批准明确拒绝exit1。STOP文件实测exit75，保留已完成局原子提交。

主进程Windows实际可用RAM检查，默认低于1024MiB停止发新任务并等待最多2个已在途任务保存commit后exit75；--min-free-mb可提高保留阈值。只在调度边界检查，不是抢占worker的硬资源限额。1000数据未生成、未训练/RL/Q。

生成manifest包含shards list、逐局hash、source10份、schema、前100/固定val的canonical匹配计数。旧prefix校验只装旧100小集（约21MB）不装新1000全量；新数据以每局流式写入。当前manifest仍pending chief admission。

恢复与停止日志next_d_scale_resume.log/next_d_scale_stop.log；准入拒绝next_d_scale_approval_reject.log。正式命令待chief批准：

    .venv/Scripts/python.exe scripts/next_data_scale.py --train-games 1000 --validation-games 20 --out datasets/next_history1000 --approval reports/next_scale_approval.json --min-free-mb 1536

approval必须含approved:true/train_games:1000/source_hashes:当前10源。恢复加--resume（总局数语义），不能把固定val并入train。

## Manifest修订后新冒烟

旧smoke与日志保留。新独立next_history_scale_smoke_v2实际4train+2val，44/31状态5.7418秒exit0；6局canonical input/labels全等旧100阶段。resume0.5169秒exit0；未批准1000拒绝exit1，STOP75。

正式1000唯一dataset_version=next-history1000；smoke另用next-history-scale-smoke-v2。新增rule_version、history_schema_version、schema_version、target_semantics=lexicographic_preference_rank_NOT_Q、raw V3 state_target_units、独立state_target_policy/definition/scale1.0、producer_sha256及实际train/val seed ranges。shards按seed排序，前100与固定val完整canonical核对。

最终生成器SHA256 d686d9f83818e34287fecace19b9391bc7e841bf1ba4b12c94cc037c9f93c842。正式命令参数不变，必须chief新hash批准与runner启动，D尚未生成1000或训练。新增数据意味着optimizer step数也可能增加，学习曲线不能纯归因数据量。

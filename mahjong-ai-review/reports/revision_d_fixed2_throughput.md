# 修复后2seed吞吐结果

真实命令：.venv/Scripts/python.exe scripts/revision_data_compare.py --games 2 --seed 3000000 --timeout 90

退出码0（脚本捕获TimeoutError后保存报告；不是成功完成实验）。结果status=incomplete，耗时90.1336秒，完整配对seed组0，无mean/CI。逐局文件revision_d_fixed2_partial.jsonl仅保存已完成完整局，不能从中声称2seed完成。规则分析、独立参考、Bot三个文件起止SHA256相同，详comparison JSON。

瓶颈：修复后target-DP单候选成本明显上升，真实两摸分支放大；不能为速度恢复第五张错误旧逻辑。后续合理方向为缓存与更严格预选分支，先单决策profile，再小fixture一致性；当前不扩大局数、不进行RL。90秒timeout在决策边界检查，不抢占单次DP，极端时可能有单决策超额。

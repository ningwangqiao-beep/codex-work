# 修订BaselineBot实际交付

未读取或声称读取未提供的Claude源码。旧失败Policy权重及best均未改写；没有新RL。

差异审计：旧shape只比较对子/邻接；新独立Bot逐合法候选先定缺债务，再standard/seven-pairs结构向听、有效进张数、有限draw-discard前瞻、四番封顶牌型潜力、公开定缺/重复弃牌弱风险。risk是未校准启发，不是对手暗手真值。番型潜力不是已成胡真实番数。两步实现目前指摸一张再舍一张的两动作前瞻，且仅搜索最多2种有效摸牌，不是穷尽两次未来摸牌；此项明确未完全实现深两摸研究要求。

定缺未清时B API结构向听不能当精确替换距离；单独记录missing_debt并合法强制弃缺。剩余量仅可见未知上界，不是假设牌墙真实分布。自身弃牌后候选移入公开计数，已胡物理牌仅计wins一次，公开面子一次。

真实测试：2项通过，日志revision_d_tests.txt。对照CLI执行退出0，2seed*4座*2政策=16完整局，16.685秒；baseline相对random净分差+1.0，seed组bootstrap95CI[-.75,2.75]。样本极小且区间跨零，不证明优于random。随机对手指随机合法舍牌，碰杠沿共用模拟器规则策略，不能称完全随机全动作玩家。seed2800000..2800001，与失败模型既有评估分开。

复现：

    .venv/Scripts/python.exe -m unittest discover -s tests -p test_revision_bot.py
    .venv/Scripts/python.exe scripts/revision_data_compare.py --games 2 --seed 2800000 --timeout 90

报告revision_d_baseline_comparison.json保存逐局scores及配对统计。未启动大规模；后续需增深前瞻和专门oracle测试，不能只加局数。

# Next history-v2 100训练局阶段

真实生成100train+20固定validation，永久不交叉：train7000000..7000099，val7100000..7100019；开发分数7200000段预留，旧final5000000..5004999禁用。后续1000/5000只扩train前缀，不能把val并回。

100train1224状态/20val235状态，共1459；完整history最长298，无序列窗口截断；57.795秒。source10份起止一致，指纹见datasets/next_history100/manifest.json。审计实际全部记录编码复现、隐藏/未来poison键不影响、整局split、candidate/结构标签一致，exit0。

历史修复初draw、直杠补draw、抢杠winner、公开no-claim pass、定缺suit，event_index单调。draw和暗杠公事件不含身份。交换仅own送收与方向/source，是历史知识非当前对手持牌真值。B独立7tests含5个真实抢杠seed核对win_events/history/ledger。

结构听牌不等于活张有效听牌。teacher candidate偏好rank不是counterfactualQ；state_target为一个轮换强Bot座位对3固定启发式风格的真实终局raw净分，是该策略条件V。模型state191/fulltokens保留顺序但event_index/suit/context并非均被显式编码新feature，不能宣称所有历史新增语义已被网络使用。

当前只数据与审计，待chief admission，不扩1000/5000、不训练/RL。冠军六源未改。game_returns独立确定性重放补齐120局全座分数/ledger/history（不是新增独立对局）；完成后还需与state_target逐条对账。

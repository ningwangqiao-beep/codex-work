# 四川麻将 AI 项目进度

更新时间：2026-11-03（Asia/Shanghai）；本文件由主智能体维护。

## 当前门槛
正式大规模训练禁止。完整规则审计未通过；重要规则修改与大规模训练需用户批准。没有麻将训练权重或真实玩家准确率结论。

| 员工 | 当前状态 | 已完成并由主智能体检查 | 问题 | 下一步 |
|---|---|---|---|---|
| B 规则工程师 | 下一阶段并行开发中 | core.py 与测试源码已读；主智能体独立复跑6项测试通过 | 仍非完整血战引擎；换三张、碰杠状态机、计分查叫等待实现；输入验证薄弱 | 输入校验、七对专项、显式配置与换三张，随后碰杠及结算 |
| C 神经网络工程师 | 下一阶段并行开发中 | 源码与日志已读；主智能体复跑CUDA前反向和Batch128合成接口测试通过 | 三模型目前为共享类别名；损失分布与训练评估尚缺；manifest门槛不足以证明实际数据无泄漏；联合与边际概率未约束一致 | 流式训练评估、断点恢复、校准、损失分布、实际数据泄漏检查及概率一致性诊断 |

## 主智能体实际复验
项目独立 Python 3.12.14 / torch 2.11.0+cu128。
- .venv/Scripts/python.exe -m unittest discover -s tests -p test_rules_core.py：6项，0.001秒，OK。
- .venv/Scripts/python.exe scripts/gpu_probe.py：RTX3060，CUDA12.8，1024矩阵前向和反向成功，梯度有限，0.2038秒，峰值33817600字节。
- .venv/Scripts/python.exe scripts/model_smoke.py：Batch128，CUDA有限梯度，通过；仅合成接口测试，没有正式麻将训练。

## 已产生的主要文件
- B：rules/core.py、tests/test_rules_core.py、reports/employee_b_tests.txt、reports/employee_b_status.md。
- C：models/networks.py、training/gate.py、scripts/gpu_probe.py、scripts/model_smoke.py、reports/gpu_probe.json、reports/employee_c_smoke.json、reports/install.log。

## 协作约束
B负责rules/simulator/configs/observations/tests及其报告；C负责环境/models/training/evaluation/inference/baselines/scripts/checkpoints/experiments及其报告。主智能体独占STATUS.md。每阶段主动报告，主审通过后追加下一阶段；当前已向两人分别下达修复及后续任务。

## 结论边界
CUDA下载已完成，之前临时文件0字节的情况已失效。GPU验证通过不代表模型学会读牌。规则6测试通过仅代表小型规则基础检查点，不能开放正式数据或大规模训练。

## 最新主审更新
主智能体已独立复跑新增规则测试：13项全部通过，0.001秒。B仍缺完整碰杠状态机与查叫，已派第三阶段继续实现。
C新增实际JSONL与同源seed泄漏门槛、规则/分块指纹审计绑定及基础指标代码，主智能体已阅读源码。发现AP并列概率计算依赖排序，已要求修复并增加独立验证；完整trainer与校准仍待实现。
两个员工此前已完成第二检查点并停止，本轮主智能体已实际调用followup_task重新启动第三阶段。大规模训练门槛保持关闭。

## 无人值守授权更新
用户已授权项目范围开发、依赖安装、规则审计、自对弈、GPU训练和修复，无需常规逐项审批。不得付费、读取凭据、公开私人项目或操作真实平台。
B继续规则与table.py；C继续模型训练评估；已实际创建D负责selfplay/观察/数据与泄漏审计。未通过依赖门槛不放行大规模训练。
主审发现并向B提交：花猪16硬编码、Table未消费配置、payments外部任意输入、strict完整库存/阶段约束不足。

## 批量实测与数据里程碑
simulation-v1假设配置：1000局/121127步/2.305秒；10000局/1212221步/20.698秒；另1800生成局/108884状态/31.006秒，均4spawn。1000与10000种子重叠，不得累计为互异11000局。
数据train76196/validation21802/test10886。D审计听牌阳性3653/938/507（约1.6%，按3对手标签计）。该数据来自随机舍牌+.65碰，不能代表多风格或真实玩家。
主审实际运行validate_manifest通过，指纹8c517f3c49b5b2a135045d6fda356d9db4665e7e48ee0b583a6938231f321e65。四源码快照已冻结；此前批次没有起始hash断言，不能补造。
主审复验35测试通过；resume_smoke实际CUDA两epoch恢复成功（仅合成）。metrics_smoke曾因loss字段缺失失败，C修复后主审复跑通过。
C准备有限真实GPU训练与独立评估，D继续多策略新版，B继续边界审计。

## 主审已验收数据与首个真实模型
v2 manifest实际验证通过：c54bcfb45c27f9e6d12f9771a7200080c4c8d03e7b48361ee688b1c6574f2e8f。v2 1000审计+1800数据局，108795状态，四种启发策略+测试未见参数；非八类，未包含主动暗/补杠策略。
v1 GPU训练真实完成4epochs早停，best epoch0，已保存best/last/deploy与optimizer。主审读最终指标和loss记录，并实际CPU加载deploy推理成功。
v1听牌AUC .67331 vs频率.51478；条件wait AUC .52534 vs .54326，未超基线；risk logloss .019892 vs .019580，未超基线。risk未校准。不能据此认定学会读牌，完整消融尚未做。

## 本轮最终状态
v2 GPU八epoch训练完成，最终test冻结，180独立测试局；主审实际读JSON/日志并CPU加载v2权重推理通过。听牌AUC .766697 vs .514181，条件听口Brier未超基线，risk未专门校准。全部结果仅明确假设配置模拟。实际共两版各1800数据局，原始状态108884+108795；不能把两版当同一个独立同分布数据集。
本轮停止在可恢复研究检查点，不继续使用最终测试调参。A-F消融、八类策略、真实平台适配、RL和ONNX未完成，详FINAL_REPORT.md。

## 第二轮自主研发正在执行
已重新调度B/C/D。主智能体独立核验两版dataset指纹与checkpoint.dataset_fingerprint一致，optimizer/有限权重存在，完整审计见reports/round2_chief_independent_audit.json。
新增规则参数/暗杠隐私修复，当前41测试主审通过。新round2数据107645状态；新增policy callback仅公开观察。
本地调度器scheduler/runner.py已实际后台启动，真实状态在experiments/round2_queue/state.json（以其中pid为准，外层启动PID可能为Python启动器）。失败停止/恢复跳过已完成任务的实际子进程测试通过，reports/round2_scheduler_probe.json。
当前队列独立审计已完成，B/C/D特征消融已完成，E/F继续，单GPU串行；资源采样resources.jsonl。不是完整A-F因果研究，历史仅最近11动作且E有多个变化。
新校准validation分组：听口和risk Brier/ECE改善，听牌校准Brier恶化不采用。尚不代表新final验证。
PolicyValue已真实55局四座共享actor-critic训练，仍只学习舍牌，碰杠规则启发式，未证明强于基线。后续计划审计绑定继续1000局并独立评估。

第二轮当前后台followup state：runner pid37136、训练child43576，主审实际确认running，结构模型从STOP断点恢复attempt2。六组受限消融全部真实完成，A..F validation AUC .785057/.784595/.788570/.786963/.784256/.786501，复杂模型未明确胜出，不以此认定序列读牌。后台后续自动生成ROUND2_REPORT.md和审计包，恢复入口BACKGROUND_RUN.md。

主审实际验证：项目级锁拒绝重复runner且原runner仍存活。新训练结构模型8epoch已完成，校准按validation半组选择，后台当前new_final_test，后续shared_policy1000与独立评估待执行。状态旧error/finished字段为上次主动STOP历史残留，以status/jobs当前项为准，下一次runner版本已清理残留字段。

第二轮自动队列已运行到汇总步骤，实际指标见ROUND2_REPORT.md及调度state.json。不得由此认定完整项目完成。


## 模仿基础策略后自对弈实验
{
  "imitation": {
    "means": {
      "heuristic": 0.445,
      "old_reading_risk": -0.8525,
      "trained_policy_value": -0.4675
    },
    "comparison": {
      "mean_difference": -0.9125,
      "paired_seed_cluster_bootstrap_95ci": [
        -1.225,
        -0.625
      ]
    },
    "clear_improvement": false,
    "scope": "configured_simulator_only"
  },
  "imitation_then_rl": {
    "means": {
      "heuristic": 0.5525,
      "old_reading_risk": -0.6975,
      "trained_policy_value": -0.32
    },
    "comparison": {
      "mean_difference": -0.8725,
      "paired_seed_cluster_bootstrap_95ci": [
        -1.27,
        -0.4775
      ]
    },
    "clear_improvement": false,
    "scope": "configured_simulator_only"
  }
}
只有独立配对区间下界大于0才标明确改善；失败方向保留记录，不宣布完整麻将AI成功。

## 额度恢复后继续推进
用户已确认额度恢复，B/C/D已真实重新启动。12:10“你好”一次性提醒由Codex automation 12-10创建成功（2026-11-03 Asia/Shanghai）。
模仿300局+共享RL1000局队列实际全部完成；模仿策略对基础差-.9125(95%CI[-1.225,-.625])；模仿后RL差-.8725(CI[-1.27,-.4775])，均不成功，报告round2_warmstart_results.json。
C发现公开牌总量强进度shortcut，旧C/D相对强基线无稳定增量；新校准模型仅验证子集有小幅改善，不代表历史读牌。报告round2_c_progress_baseline.json。
D发现自由舍牌teacher一致率仅28%，训练回放也低，说明表示/拟合不足。下一改候选动作结构特征，B新增向听/有效进张，D小规模比较基础算牌策略。主审48tests通过，300随机hand shanten=-1与core winning对照0不一致。
调度digest覆盖bug已修复，非空fingerprints的failure/resume探针实际通过；旧错误state与证据不改。新增append-only attempts事件，编译/完整探针通过。旧运行state不可直接按新digest恢复，需要用新queue目录，避免误用成功结果。

## 下一瓶颈已定位
候选结构线性网络（非大模型）已真实训练80新teacher局/30validation局，20epoch约9.23秒；validated utility最优与整数tie一致率均100%，只说明复现基础策略，不代表打牌更强。原大动作头自由舍牌约28%无法拟合的问题有了解释：表示与动作目标不合适，非单纯数据局数少。
向听+有效进张20seed*4座*2策略完整160局已完成，平均差+.15，整局bootstrap95CI[-.3125,+.6125]，尚无稳定收益提升证据。有效进张是未知牌可见上界，不是牌墙真张数。下一方向在已可复现基础策略的候选表示上做小残差自对弈，不盲增网络。
C继续完整game动作/净收益复现测试；D对接候选残差actor-critic；B完成算牌对接只读审核未见直接隐藏输入或重复物理牌计数。

当前实际后台candidate residual队列已启动，pid44156/child37324，主审看到第283局；source_fingerprints已递归绑定本地import，attempts.jsonl保留历史。零残差1809动作与解析teacher无偏差；训练使用softmax探索不等于确定teacher，评估固定greedy。该流程只学习舍牌，还不是攻防/碰杠完整AI。最终结果将由chief_candidate_summary更新，未经评估不声称改进。12:10“你好”提醒保持ACTIVE，已用view核验卡片。


## 候选结构残差自对弈实际结果
{
  "mean_difference": 0.0125,
  "paired_seed_bootstrap_95ci": [
    -0.3475,
    0.3675
  ],
  "simulation_only": true,
  "checkpoint_sha256": "a022c3df22b947da72d589753616c00b54b17df36867334493816d890303ad17",
  "flags": [
    "PAIRED_INITIAL_SEED_NOT_IDENTICAL_FUTURE",
    "RESIDUAL_EVAL_GREEDY_TRAIN_SOFTMAX"
  ],
  "clear_improvement": false
}
这是1000局训练后独立100种子组评估，不代表完整麻将AI；只学习舍牌，碰杠仍启发式。无明确正区间不标成功。

## V3额度恢复后主审准入
用户确认额度恢复，B/C/D实际重新调度。V3 core/v3/table冻结，大小查叫三配置与杠分active子集测试已新增。
主智能体执行 .venv/Scripts/python.exe -m unittest discover -s tests -v，80项通过9.651秒、exit0，日志reports/v3_chief_gate_tests.log和command.json。
主智能体独立完成12 strict集成局、三交换方向，生成六源hash/testlogsha绑定reports/v3_chief_ready.json。已向D放行1000局seed3200000，成功后10000局独立seed3300000。尚不声明批次已完成。
旧模型V3 32局仅smoke，未晋级；强Bot memo单决策缓存对照不等于整局吞吐提升。新V3正式训练/RL继续不准入，等待批次及强baseline/数据价值审计。

## V3最新独立验收与实际后台运行
主审独立执行80tests通过；12strict集成、1000strict120860步骤3.065秒、10000独立性能1210107步骤29.316秒，并对11000局每笔ledger重建score零和及六源码当前hash核对，均通过。证据v3_chief_batch_recheck.json。
Calculator fast模块主审实际615case回归exit0；这是相对已修复算法一致，不是新的独立数学证明。
V3strong开发20seed400局mean4.525 vs shape4.1125，差+.4125 CI[-1.8875,2.5]，无相对shape提升证据。vs随机开发差+4.85 CI[3.975,5.6875]，仅准入基础监督，不宣称高手。
独立最终评估已实际后台启动：experiments/v3_frozen_evaluation/state.json，runner pid42188，child37532，5000新seed5000000..5004999，四座五冻结策略100000局。已现场观察2544局持久化，非完成。CPU2，最低空闲RAM1GB/温度80/显存7GB/8h，eval timeout6h；checkpoint为逐完整seed组JSONL，支持resume。预注册v3_final_preregistration.json。新T2模型不在这批已冻结最终名单，不能中途加模型。
主审实际inspect teacher100：955train/249validation/fullhistory最大134/10源+分片hash/整局隔离通过，T2_SUPERVISED_ONLY准入reports/v3_chief_t2_admission.json已验证training_allowedTrue/RLFalse。仅授权6epochs128batch小监督，老师rank非counterfactualQ、终局raw V只是老师策略的V。C正在执行，尚未报告训练结果。
强化学习仍关闭；模型不自动覆盖best，不基于最终测试调参。

T2首个V3真实GPU监督已完成：80train games/955状态、20validation games/249状态，6epochs/48 optimizer steps，best epoch5。主审已读取COMPLETE/metrics/weights文件及命令，validation exact/equivalent=.815261、Top3=.943775、teacher preference regret=.071717（非净分Q）。CUDA峰值allocated34328576B、process working set约1.57GB；C记录实际4.764秒。权重checkpoints/v3_T2_teacher100_seed42，各best_epoch独立保留；无RL，不覆盖旧best，不宣称强度晋级。后续新模型开发整局评估使用新seed，绝不插入正在运行的五冻结策略最终评估。


## V3冻结独立评估实际结果
5000组新发牌、四座轮换、五冻结策略。不是新神经网络训练。各款项以ledger互斥对账，原始逐局JSONL保留。
{
  "status": "completed",
  "complete_seed_groups": 5000,
  "seconds": 9708.6915334,
  "summary": {
    "random": {
      "net": -1.7095,
      "win": 0.04405,
      "self_draw": 0.0099,
      "deal_in_events": 0.1354,
      "deal_in_loss": 0.351,
      "mean_winning_fan": 1.318955732122588,
      "parts_mean": {
        "added_kong": -0.0309,
        "self_draw": -0.3912,
        "direct_kong": -0.10015,
        "rob_kong_win": -0.0003,
        "concealed_kong": -0.0354,
        "gang_refund": -0.03595,
        "flower_pig": 0.0016,
        "discard_win": -0.2758,
        "cha_jiao_big": -0.8414
      }
    },
    "shape": {
      "net": 1.22665,
      "win": 0.2716,
      "self_draw": 0.0638,
      "deal_in_events": 0.1154,
      "deal_in_loss": 0.3017,
      "mean_winning_fan": 1.4477172312223858,
      "parts_mean": {
        "added_kong": -0.02475,
        "self_draw": 0.4072,
        "direct_kong": -0.13745,
        "rob_kong_win": 0.0009,
        "concealed_kong": -0.0642,
        "gang_refund": 0.29925,
        "flower_pig": -0.0024,
        "discard_win": 0.2063,
        "cha_jiao_big": 0.5418
      }
    },
    "old_candidate": {
      "net": 1.22665,
      "win": 0.2716,
      "self_draw": 0.0638,
      "deal_in_events": 0.1154,
      "deal_in_loss": 0.3017,
      "mean_winning_fan": 1.4477172312223858,
      "parts_mean": {
        "added_kong": -0.02475,
        "self_draw": 0.4072,
        "direct_kong": -0.13745,
        "rob_kong_win": 0.0009,
        "concealed_kong": -0.0642,
        "gang_refund": 0.29925,
        "flower_pig": -0.0024,
        "discard_win": 0.2063,
        "cha_jiao_big": 0.5418
      }
    },
    "old_residual": {
      "net": 1.54195,
      "win": 0.28725,
      "self_draw": 0.06905,
      "deal_in_events": 0.10965,
      "deal_in_loss": 0.2795,
      "mean_winning_fan": 1.487206266318538,
      "parts_mean": {
        "added_kong": -0.01195,
        "self_draw": 0.4972,
        "direct_kong": -0.0776,
        "rob_kong_win": 0.0003,
        "concealed_kong": -0.0318,
        "gang_refund": 0.2499,
        "flower_pig": -0.0016,
        "discard_win": 0.2722,
        "cha_jiao_big": 0.6453
      }
    },
    "new_baseline": {
      "net": 3.6048,
      "win": 0.64655,
      "self_draw": 0.16175,
      "deal_in_events": 0.0743,
      "deal_in_loss": 0.1815,
      "mean_winning_fan": 1.2753847343592917,
      "parts_mean": {
        "added_kong": -0.0194,
        "self_draw": 1.5038,
        "direct_kong": -0.0071,
        "rob_kong_win": 0.0034,
        "concealed_kong": -0.0008,
        "gang_refund": 0.3837,
        "flower_pig": -0.0048,
        "discard_win": 0.8095,
        "cha_jiao_big": 0.9365
      }
    }
  },
  "comparisons": {
    "random": {
      "mean_vs_shape": -2.93615,
      "paired_seed_ci": [
        -3.02405,
        -2.84695
      ]
    },
    "old_candidate": {
      "mean_vs_shape": 0.0,
      "paired_seed_ci": [
        0.0,
        0.0
      ]
    },
    "old_residual": {
      "mean_vs_shape": 0.3153,
      "paired_seed_ci": [
        0.24665,
        0.3825
      ]
    },
    "new_baseline": {
      "mean_vs_shape": 2.37815,
      "paired_seed_ci": [
        2.2845,
        2.46815
      ]
    }
  },
  "limitations": [
    "opponent discards configured by CLI; meld actions shared simulator",
    "win events not transfer count",
    "configured singlemax settlement; not verified room",
    "paired initial deal not identical future",
    "promotion_requires_chief_review_of_predeclared_final_evaluation"
  ],
  "primary_predeclared": "new_baseline vs shape",
  "no_training": true,
  "no_model_weights_replaced": true,
  "no_expert_claim": true
}
区间跨零即证据不足；该配置模拟结果不是现实高手认证。不得用本最终集继续调参。

## 神经网络提升下一阶段：正式启动
用户要求冻结冠军、先诊断再有界改进。冠军v3-rules-20261103已冻结于champions/v3_rules_20261103，14源码依赖/7评估证据指纹，规则程序无神经网络权重；原raw评估JSONL登记原址SHA不改。入口reports/next_chief_champion_freeze.json，freeze命令exit0。
原最终种子5000000..5004999永久禁止模型选择；新训练7000000+、验证7100000+、开发7200000+分离，见configs/next_seed_registry.json；新final尚未预注册。
T2诊断实证：46自由错误均不增missing/structural，38降低进张，9降低fan proxy，未发现明确普通/七对转换；梯度量级提示单任务对照但不证明负迁移；部署约慢4.38倍。神经网继承规则teacher预筛，不可算自主学会算牌。
历史v2新文件修initial draw/直杠replacement draw/rob_kong_win/pass；B独立7tests含5真抢杠种子全部过，主审全测试87过9.521秒exit0。冠军六源未改。
100训练+20固定验证真实120游戏，1224train/235val，history最大298。D/C未伪称Q，标签仍teacher preference rank；raw终局V有全120局returns/ledger。主审独立逐1459记录验源/分片/编码/合法候选/120局零和与V标签/禁用seed通过，reports/next_chief_data100_audit.json，exit0。
下一有界两对照同架构同seed同6epoch/batch128：action-only vs原multitask；数据/源新准入签后才GPU执行。未扩1000/5000，未RL，未晋级，未覆冠军。


## 新历史100训练局阶段真实开发对比
{
  "loss_control": {
    "status": "completed",
    "complete_seed_groups": 20,
    "summary": {
      "multitask": {
        "games": 80,
        "mean_net_score": 4.15,
        "win_rate": 0.5625,
        "self_draw_rate": 0.15,
        "deal_in_event_rate": 0,
        "deal_in_game_rate": 0,
        "mean_deal_in_loss": 0,
        "seat_mean": {
          "0": 4.75,
          "1": 3.75,
          "2": 4.6,
          "3": 3.5
        },
        "parts_mean": {
          "added_kong": -0.0125,
          "direct_kong": -0.0125,
          "gang_refund": 0.525,
          "discard_win": 0.925,
          "concealed_kong": -0.125,
          "cha_jiao_big": 1.2,
          "self_draw": 1.65
        }
      },
      "action_only": {
        "games": 80,
        "mean_net_score": 3.925,
        "win_rate": 0.55,
        "self_draw_rate": 0.1375,
        "deal_in_event_rate": 0,
        "deal_in_game_rate": 0,
        "mean_deal_in_loss": 0,
        "seat_mean": {
          "0": 4.8,
          "1": 4.25,
          "2": 3.65,
          "3": 3
        },
        "parts_mean": {
          "added_kong": 0.0125,
          "direct_kong": 0.0125,
          "gang_refund": 0.525,
          "discard_win": 0.925,
          "concealed_kong": -0.15,
          "cha_jiao_big": 1.1,
          "self_draw": 1.5
        }
      },
      "strong": {
        "games": 80,
        "mean_net_score": 4.0625,
        "win_rate": 0.675,
        "self_draw_rate": 0.1125,
        "deal_in_event_rate": 0.0125,
        "deal_in_game_rate": 0.0125,
        "mean_deal_in_loss": 0.025,
        "seat_mean": {
          "0": 4.4,
          "1": 3.55,
          "2": 4.9,
          "3": 3.4
        },
        "parts_mean": {
          "added_kong": -0.1,
          "direct_kong": -0.05,
          "gang_refund": 0.5375,
          "discard_win": 1.15,
          "concealed_kong": 0.05,
          "cha_jiao_big": 1.175,
          "self_draw": 1.3
        }
      }
    },
    "comparisons": {
      "multitask_vs_strong": {
        "paired_initial_seed_mean": 0.0875,
        "seed_bootstrap95ci": [
          -0.8125,
          1.0625
        ],
        "seed_differences": [
          -2.25,
          -1.0,
          -2.5,
          -2.5,
          -1.0,
          -3.0,
          1.5,
          -0.5,
          2.5,
          -2.0,
          -1.75,
          4.5,
          3.5,
          2.0,
          1.5,
          -1.25,
          2.5,
          -0.5,
          1.0,
          1.0
        ]
      },
      "action_only_vs_strong": {
        "paired_initial_seed_mean": -0.1375,
        "seed_bootstrap95ci": [
          -1.0625,
          0.775
        ],
        "seed_differences": [
          -2.25,
          -1.0,
          -4.0,
          -2.5,
          -1.0,
          -3.0,
          1.5,
          -0.5,
          2.5,
          -2.0,
          1.5,
          -0.75,
          3.5,
          2.5,
          1.5,
          1.25,
          2.5,
          -3.0,
          1.0,
          -0.5
        ]
      },
      "action_only_vs_multitask": {
        "paired_initial_seed_mean": -0.225,
        "seed_bootstrap95ci": [
          -0.9375,
          0.425
        ],
        "seed_differences": [
          0.0,
          0.0,
          -1.5,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          3.25,
          -5.25,
          0.0,
          0.5,
          0.0,
          2.5,
          0.0,
          -2.5,
          0.0,
          -1.5
        ]
      }
    },
    "limitations": [
      "random legal-discard opponents; claims/default other stages shared simulator",
      "paired initial deal does not imply identical future trajectories",
      "preference head not counterfactual Q; policy-conditioned V unused for choice",
      "20seed or smaller development sample; no strength promotion"
    ]
  },
  "relative_combo": {
    "status": "completed",
    "complete_seed_groups": 20,
    "summary": {
      "multitask": {
        "games": 80,
        "mean_net_score": 3.45,
        "win_rate": 0.525,
        "self_draw_rate": 0.0375,
        "deal_in_event_rate": 0.05,
        "deal_in_game_rate": 0.05,
        "mean_deal_in_loss": 0.125,
        "seat_mean": {
          "0": 3.9,
          "1": 3.1,
          "2": 3.5,
          "3": 3.3
        },
        "parts_mean": {
          "cha_jiao_big": 1.525,
          "discard_win": 0.85,
          "added_kong": -0.0625,
          "direct_kong": 0.075,
          "self_draw": 0.4,
          "concealed_kong": 0.2,
          "gang_refund": 0.4625
        }
      },
      "relative": {
        "games": 80,
        "mean_net_score": 4.8625,
        "win_rate": 0.7125,
        "self_draw_rate": 0.175,
        "deal_in_event_rate": 0.05,
        "deal_in_game_rate": 0.05,
        "mean_deal_in_loss": 0.125,
        "seat_mean": {
          "0": 4.45,
          "1": 5.85,
          "2": 4.75,
          "3": 4.4
        },
        "parts_mean": {
          "cha_jiao_big": 1.225,
          "discard_win": 1.0,
          "self_draw": 2.05,
          "added_kong": -0.05,
          "direct_kong": -0.0625,
          "concealed_kong": 0.125,
          "gang_refund": 0.575
        }
      },
      "strong": {
        "games": 80,
        "mean_net_score": 5,
        "win_rate": 0.7625,
        "self_draw_rate": 0.1875,
        "deal_in_event_rate": 0.05,
        "deal_in_game_rate": 0.05,
        "mean_deal_in_loss": 0.125,
        "seat_mean": {
          "0": 4.05,
          "1": 4.95,
          "2": 5.05,
          "3": 5.95
        },
        "parts_mean": {
          "cha_jiao_big": 0.9,
          "discard_win": 1.025,
          "self_draw": 2.35,
          "added_kong": 0.0375,
          "direct_kong": -0.025,
          "concealed_kong": 0.075,
          "gang_refund": 0.6375
        }
      }
    },
    "comparisons": {
      "multitask_vs_strong": {
        "paired_initial_seed_mean": -1.55,
        "seed_bootstrap95ci": [
          -2.675,
          -0.475
        ],
        "seed_differences": [
          -8.0,
          -2.5,
          -1.0,
          3.5,
          1.0,
          -0.5,
          1.0,
          -3.0,
          -0.5,
          -3.5,
          -2.0,
          -2.0,
          -3.25,
          -1.0,
          0.5,
          -5.0,
          0.25,
          1.5,
          -3.0,
          -3.5
        ]
      },
      "relative_vs_strong": {
        "paired_initial_seed_mean": -0.1375,
        "seed_bootstrap95ci": [
          -1.2625,
          0.7875
        ],
        "seed_differences": [
          -5.5,
          4.0,
          1.0,
          3.5,
          0.0,
          1.25,
          0.0,
          0.0,
          -0.75,
          0.0,
          0.5,
          1.0,
          -1.0,
          -1.5,
          0.0,
          -4.0,
          -2.0,
          3.5,
          -2.25,
          -0.5
        ]
      },
      "relative_vs_multitask": {
        "paired_initial_seed_mean": 1.4125,
        "seed_bootstrap95ci": [
          0.525,
          2.375
        ],
        "seed_differences": [
          2.5,
          6.5,
          2.0,
          0.0,
          -1.0,
          1.75,
          -1.0,
          3.0,
          -0.25,
          3.5,
          2.5,
          3.0,
          2.25,
          -0.5,
          -0.5,
          1.0,
          -2.25,
          2.0,
          0.75,
          3.0
        ]
      }
    },
    "limitations": [
      "random legal-discard opponents; claims/default other stages shared simulator",
      "paired initial deal does not imply identical future trajectories",
      "preference head not counterfactual Q; policy-conditioned V unused for choice",
      "20seed or smaller development sample; no strength promotion"
    ]
  },
  "scope": "development only; no final test tuning; no automatic promotion"
}
神经网络模仿改善不能代替净分证据；区间跨零不晋级；当前冠军不覆盖，1000/5000扩充另行受控。

## 100局阶段第一轮实际结果
两个原架构控制6epoch/60step/seed42/batch128均exit0：multitask验证free-equivalent53.21%，action-only53.21%；去辅助任务未改善，不能断言负迁移。20开发seed7200000..19/240局：multi4.15 vsstrong4.0625，diff+.0875 CI[-.8125,1.0625]；action3.925 diff-.1375 CI[-1.0625,.775]，均不晋级。
同状态随机顺序冷暖计时显示两原架构神经网warm6.67/6.70ms，强Bot4.28ms；之前固定顺序4.38倍观测受cache/状态混杂，不可归因辅助头。
relative input+pairwise组合为20541参数（control20349），同100训练数据/6epoch/60step。fixedval109free-equivalent88.07% vs53.21%；rank regret .03114 vs .22761（不是净分Q）。整局bootstrap teacher-fit差区间为正；只说明组合更会复现teacher。
新开发7200200..219/240局：relative4.8625、strong5、旧control3.45；relative-strong -.1375 CI[-1.2625,.7875]不晋级；relative-control +1.4125 CI[.525,2.375]。不得跨不同开发seed把绝对均分直接比较。
准备1000数据边际试验（非5000），冻结relative架构与损失；固定6epoch意味着数据和optimizersteps都增加，结果不能只归因数据纯因果。后续仍需数据审计/明确新准入。当前无RL、无真实counterfactualQ，冠军未覆盖。

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

## 五组读牌训练与评估真正完成
10个任务全部exit0，本地队列总360秒；每组6epoch/582更新，权重和预测已保存。听牌AUC约.75-.77，具体条件听口约.518-.524，合法候选风险约.710-.731；不是准确率。单看AUC点估计不能认证增量贡献，正在独立按整局配对比较并核标签与训练先验/公开规则基线。未晋级、未校准、未替换冠军。

## 读牌v1失败诊断与下一有界方向
五模型权重/预测/当前源SHA由主控核实；B四项独立标签测试exit0确认相对对手/bit映射正确、结构死听可为正；D整局配对指标重建exit0。C真实诊断：1593定缺花色项全为负，但网络仍分配约33%听口概率质量，flat81未学必零。counts定缺硬零后AUC .5213->.6911（程序规则能力）；train-only统计先验+定缺 .7157，missing/tile/known先验 .7610，公开非缺门未知张数加权 .8163（允许花色内 .7246）；不可把规则收益称训练收益。公开基线AUC更高但logloss不一定最好，禁止只挑指标。当前aux100已成为开发诊断集，不能当下一候选独立最终集。C实现逐对手逐tile共享特征v2，仍固定1000train/6epoch/582steps、未正式训练；D准备候选冻结后全新7120000..199独立200局验证，尚未生成。冠军未改/无RL。

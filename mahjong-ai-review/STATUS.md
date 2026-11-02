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

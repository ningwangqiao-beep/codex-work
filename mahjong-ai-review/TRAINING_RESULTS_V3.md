# Training Results V3

## 结论

已在RTX3060实际完成一轮受准入约束的V3 T2小型监督训练，保存真实权重、optimizer/RNG、源/规则/数据绑定和分头指标。训练完成不等于策略成功：20seed开发对局未证明净分改善，状态V也未胜训练中位数常数基线。保留强开发Bot和所有旧best，不晋级、不启动RL。

## 证据等级

已由C独立执行：当前GPU前反向、17旧权重/3旧数据清单、legacy合法包装fixture、257事件/空history接口、1204真实数据逐条检查、T2六epochCUDA训练、独立STOP/resume、2seed吞吐和20seed完整开发对局、validation-only价值强基线诊断。

准入由主审审核并签名：80全测、规则1000strict/10000性能及账本、强开发Bot、数据隔离和V目标定义。C通过reports/v3_chief_t2_admission.json内容哈希和其所指证据验准入，不把其他员工或主审的运行称为C亲自重跑。

设计/接口完成但未验证能力：完整历史读牌增量、隐藏手牌后验、counterfactual action Q、多阶段动作价值和真实玩家能力。没有任何本轮RL训练。

## GPU和继承

当前独立probe：Python3.12.14，torch2.11.0+cu128，CUDA12.8，RTX3060 8192MiB，驱动610.88。1024矩阵前反向finite，0.35244秒、torch峰值33,817,600字节，exit0。证据v3_c_gpu_probe.json/.log/_exitcode.txt，不覆盖旧gpu_probe。

旧清单v3_c_legacy_inventory.json包含实际模型/数据/规则快照SHA256，旧计分不用于V3比较。旧风险/损失单位不能当V3分；legacystatic/candidate/residual包装只返回合法舍牌。

## T2主实验（已独立实际执行）

规则：SICHUAN-XUEZHAN-4FAN-V3。数据datasets/v3_teacher100/manifest.json，SHA256 `c403e3ec738496fe8c16200de46159d06bb80c4fe9a2ef564310f2bac37c5f77`。seed4200000..4200099，80train955状态/20validation249状态，完整game/seed/deal组隔离，10源及实际分片哈希绑定。最大历史134，未截断。

模型20,349参数；state191+全长GRU16+逐候选12特征，动作偏好头、teacher-policy V头、structural听牌/条件听口/joint8辅助头。动作标签为lexicographic_preference_rank_NOT_Q；V是轮换teacher座位对三冻结启发式的终局raw V3净分，非新policy V或反事实Q。

固定配置：seed42、6epoch、batch128、Adam0.001、CPU2线程、CUDA、48optimizersteps。loss权重：action MSE1，equivalent ranking CE1，state V MSE0.01，三辅助loss各0.2。每头分别写metrics.jsonl。最佳epoch5。CUDA主训练4.764秒（不含环境启动/准入检查）；peak allocated34,328,576B，reserved50,331,648B；进程peak working set1,571,819,520B；GPU独立样本48°C/1667MiB（含桌面显存，非模型专属）。

实际主命令（从项目目录运行）：

    .venv/Scripts/python.exe scripts/v3_model_train.py --manifest datasets/v3_teacher100/manifest.json --admission reports/v3_chief_t2_admission.json --output checkpoints/v3_T2_teacher100_seed42 --epochs 6 --batch-size 128 --seed 42 --device cuda --resume

exit0。reports/v3_c_T2_command.json记录命令及脚本/训练器SHA；v3_c_T2_train.log、v3_c_T2_exitcode.txt为实际进程证据。模型与optimizer/rng/config/绑定位于checkpoints/v3_T2_teacher100_seed42/last.pt及best_epoch_0.pt..best_epoch_5.pt，BEST.json仅指向不可覆盖快照。best_epoch_5.pt SHA256 `aa8418016121f6ea89939750397aa9a0858eb22f3aa811d4120cd4afc1491b1e`。完成目录禁止覆盖。

## 验证指标（非最终收益证据）

epoch5：249状态exact/equivalent81.53%；其中自由舍牌121状态61.98%，teacher rank regret0.14758；缺门强制128状态100%。总体率被强制缺门抬高，不冒充自由决策水平。不同best-postdiscard structural分组完整记录在metrics.jsonl；它不是独立oracle认证向听。

teacher-policy V MAE约2.4896 raw分。CPU独立validation诊断（浮点后端有微小差异）：vs训练median=2常数MAE2.13655，网络差+0.35306，20局bootstrap95%CI[-0.12558,0.75953]；vs0的差-0.38589，CI[-1.54831,0.80782]。不能仅凭优于零点估计通过ValueNet审计。证据v3_c_T2_validation_diagnostics.json/.log/_exitcode.txt（exit0）。

## 新开发种子完整局评估

先2seed4400000..1四座×三策略24局吞吐，4.06秒、exit0；随后固定新20seed4400100..4400119四座×三策略240完整局，45.38秒、exit0，没有改模型或追加epoch。对手随机合法舍牌，其他阶段采用相同模拟器默认，配对初始种子不保证相同未来随机轨迹。

|策略|完整局|平均净分|
|---|---:|---:|
|T2 preference网络|80|3.6125|
|强开发BaselineV3|80|4.4375|
|shape启发式|80|3.6125|

T2减强Bot=-0.825，整seedbootstrap95%CI[-1.6875,0.1]；T2减shape=0，CI[-1.45,1.3125]。没有证据证明提升，不晋级。所有账本分项逐局对账、四家净分和0；分项、各座、胡牌/自摸和点炮原始jsonl均保存。

T2含Calculator与GRU平均每次36.5ms，强Bot8.33ms；共享缓存和开发状态分布影响成本，非生产延迟保证。首2seed正差没有在20seed持续；没有挑成功子集。

命令：

    .venv/Scripts/python.exe scripts/v3_model_development_eval.py --checkpoint checkpoints/v3_T2_teacher100_seed42/best_epoch_5.pt --seed 4400100 --seeds 20 --timeout 180 --output reports/v3_c_T2_development20.json

证据v3_c_T2_development2/20.json/.jsonl/.log/_exitcode.txt。部署inference/v3_T2_policy.py验证model/calculator/training-manifest源绑定，动作只用偏好头，teacher-policy V不参与选牌。新模型未加入已冻结后台五策略最终名单；未访问5000000..5004999预注册最终集。

## STOP和恢复（独立输出）

实际运行scripts/v3_model_resume_stop_smoke.py：测试loader在第3optimizerstep后注入STOP，子进程exit75保存cursor3；恢复与不中断两epoch均16step。optimizer及CUDA/CPU RNG恢复，最大参数差7.45e-09，不宣称bitwise相等。主best SHA不变。三个子进程退出码75/0/0，总测试exit0；checkpoints/v3_T2_resume_smoke/control独立保存，未覆盖主实验。证据v3_c_T2_resume_stop_smoke.json/.log/_exitcode.txt及子log。恢复中省略批次确定，不把重复训练伪装精确恢复。

## 已发现并保留的问题与下一步

V3初版history词表缺missing_declared/self_win/discard_win，已补16词汇并重跑；原64及pre-fix接口证据保留。完整sequence可变长度，257合成事件stress通过，非物理完整局声明。

T2监督样本少、风险val仅12正例、多人val0；辅助loss不是校准或读牌成功。rank ordinal间距不是净分间距，V标签属于teacher策略族。数据/基线准入仅允许本轮有限T2，未自动授权强化学习。

下一轮最小有据研究：先用新V3 train/validation做进度强基线和完整历史顺序对照、提高候选teacher拟合与价值常数基线评估，再考虑合法受约束反事实终局Q标签；不得盲目增大网络/epoch。任何新模型需要另行预注册新最终种子，不能复用旧final调参或把当前开发集称为独立最终证明。

后续审计补充：无截断fullseq不等于源事件全部覆盖。冻结V3驱动的rob_kong_win未显式追加history，直杠补摸缺独立draw事件；已上报主审/D，不改运行中最终评估源。当前T2history审计只证明提供prefix的合法编码/长度一致，完整事件覆盖仍有缺口；下一数据版本应修复重绑，保留本轮模型及失败结果。

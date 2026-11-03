# Next C: actual T2 deficit diagnosis

CPU2 frozen-checkpoint audit exited0; reports/next_c_T2_diagnosis.json/.log/_exitcode.txt. No training, no old/new final test read.

Among121 free validation decisions46 were teacher-inequivalent. All46 had the SAME structural shanten as teacher, none had higher missing debt;38 had lower effective draws and9 lower heuristic fan proxy (overlapping categories). Failure is chiefly ranking improvements within the same shanten, so adding a min-shanten safety mask would not address it. Free equivalent rates by best-postdiscard structural0/1/2:45/55,22/50,8/16. These are teacher-feature groups, not independent shanten-oracle certification.

Existing240 development games reconcile T2-strong=-.825: selfdraw-.9, discardwin-.175, directkong-.15, concealedkong-.1, addedkong-.0375, offset by chajiao+.4 and refunds+.1375. This is accounting attribution, not a causal proof that a specific missed effective draw caused each loss. Teacher-policy state V is not candidate Q; ordinal rank spacing is not money regret.

One-batch shared-state gradient diagnostic: action MSE norm.06305; V MSE8.718*.01=.08718, risk CE.33362*.2=.06672. Thus small numeric V weight does not guarantee a small gradient contribution. Cosines to action gradient V=-.0145, tenpai=-.0369, waits=.0271, risk=.0349. These single-batch nearly orthogonal gradients motivate an action-only control, not a claim proven negative transfer.

Minimal new prototype models/next_candidate.py: candidate-relative centering/scaling exposes effective-draw differences instead of relying on raw /108 scale; small shared-state encoder, per-candidate rank head, tie-aware pairwise preference loss. No whole-game Q claim, no aux/V losses in first control. scripts/next_model_candidate.py --smoke --output reports/next_c_candidate_smoke.json passed CPU finite-gradient interface only. Actual supervised training remains unavailable until history_v2 source/data admission. Existing strong champion and all old weights untouched.

D contract: history_v2 adds firstdraw/exposed replacementdraw/robwin/no-claim pass, schema v3-history-v2-public-events; reserved new train7000000+, validation7100000+, development7200000+, old final5000000..5004999 prohibited. D preparing100train+20validation after B fixtures; validation will never be appended totrain. Before formal fit, verify token encoder preserves new event fields (event_index/suit/context) rather than merely accepting action names. Count/progress/full-history/exchange ablations must change one input family at a time and use same game splits. No automatic RL authorization.

追加实际量化（同一冻结验证集）：46个错误中增加缺门债0、增加打后structural0、越出details_evaluated前沿0；提高fan proxy0，降低fan9。七对备选距离恶化26，但七对严格优于普通→普通严格优于七对的转换0，反向0；不能把这些叫主动追番或明确牌型转换。全部错误留在相同structural的teacher预筛前沿。

重要表示归因：details_evaluated直接来自strong Bot按最低missing_debt/structural的预筛，effective/one/two只在该前沿计算。因此网络动作没有变坏向听，不能证明网络自主学会向听；规则Calculator和teacher预筛已经提供此能力。部署仍调用完整strong Bot来生成特征，36.5ms对8.33ms约4.38倍开销，不是更便宜的teacher替代。

预注册最小对照提议（尚未执行，必须新history/data主审准入）：相同新100游戏train/固定20game validation、相同原V3 architecture/seed42/batch128/6epoch/Adam.001，A仅action MSE+equivalent-ranking CE，B原6头权重不变。用独立目录保存，先比较自由equivalent/teacher rank regret/进张误选/单局聚类CI，再在新dev7200000系列四座配对净分与成本；final5000000禁用。candidate-relative结构作为后一个独立变量，不能同时更换结构和loss后归因改善。旧单batch梯度不能证明V占主导，也不能证明负迁移。

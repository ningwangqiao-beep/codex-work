# Teacherƿ����ϣ�ʵ�����У�

ѵ���ط�30�֣�1400000..1400029������validation100�֣�1800000..1800099�����޲������£�δʹ�����ղ���seed��ȫ����teacher�켣�����ۣ����ܽ���Ϊģ��ʵ�ʲ��Թ켣��ֵУ׼��

|��|imitation����һ����|RL����һ����|imitation value MSE|RL value MSE|
|---|---:|---:|---:|---:|
|train_replay (n=1791)|58.46%|58.91%|0.004550|0.003634|
|train_replay/missing_forced (n=902)|86.92%|87.03%|0.004247|0.003529|
|train_replay/stage0 (n=551)|68.78%|68.78%|0.004142|0.003460|
|train_replay/missing_forced/stage0 (n=459)|76.91%|77.12%|0.004099|0.003438|
|train_replay/free_discard (n=889)|29.58%|30.37%|0.004857|0.003741|
|train_replay/free_discard/stage0 (n=92)|28.26%|27.17%|0.004357|0.003570|
|train_replay/stage1 (n=629)|55.17%|55.33%|0.004556|0.003696|
|train_replay/free_discard/stage1 (n=374)|27.81%|28.07%|0.004605|0.003630|
|train_replay/missing_forced/stage1 (n=255)|95.29%|95.29%|0.004485|0.003793|
|train_replay/stage2 (n=611)|52.54%|53.68%|0.004911|0.003728|
|train_replay/missing_forced/stage2 (n=188)|100.00%|100.00%|0.004286|0.003394|
|train_replay/free_discard/stage2 (n=423)|31.44%|33.10%|0.005189|0.003876|
|heldout_validation (n=5971)|57.71%|58.03%|0.004491|0.003653|
|heldout_validation/missing_forced (n=3032)|86.51%|86.84%|0.004223|0.003392|
|heldout_validation/stage0 (n=1875)|67.73%|68.05%|0.004325|0.003683|
|heldout_validation/missing_forced/stage0 (n=1568)|75.57%|76.08%|0.004239|0.003572|
|heldout_validation/free_discard (n=2939)|28.00%|28.31%|0.004768|0.003921|
|heldout_validation/free_discard/stage0 (n=307)|27.69%|27.04%|0.004762|0.004249|
|heldout_validation/stage1 (n=2113)|53.15%|53.48%|0.004520|0.003664|
|heldout_validation/missing_forced/stage1 (n=810)|96.79%|97.04%|0.004101|0.003209|
|heldout_validation/free_discard/stage1 (n=1303)|26.02%|26.40%|0.004781|0.003946|
|heldout_validation/stage2 (n=1983)|53.10%|53.40%|0.004618|0.003612|
|heldout_validation/free_discard/stage2 (n=1329)|30.02%|30.47%|0.004757|0.003821|
|heldout_validation/missing_forced/stage2 (n=654)|100.00%|100.00%|0.004335|0.003187|

���ۣ�ѵ���ط���������һ����Լ29.6%����validationԼ28.0%�����߶��ͣ�����ģ����teacher������������Ϊ��δ�����ϡ���һ���ʱ�ȱ��ǿ�ƶ�������̧�ߡ�RL��validation�������ƽ�Լ28.3%��δ�����ƿ�������ܽ�������Щ���ȷ���������ʾ��ѵ����������ʧ���仹��teacher����ƽ����ɣ�����Ӧ������顣
valueĿ�갴����������/48��һ���������ֵ����ֱ�ӿ���ԭʼ������λ��teacher��Ϊһ���Բ���ͬ�齫ǿ�ȡ�Ȩ��SHA256��JSON��
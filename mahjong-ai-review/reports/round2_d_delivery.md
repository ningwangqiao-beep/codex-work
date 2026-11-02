# Round2 D ����

������107645״̬��1800���֣�seed800000..801799��train75521 validation21506 test10618��1000�ϸ����seed700000..700999����������/����/���ƽ׶μ��ͨ������Դ��ǰ��ָ����ͬ��snapshot���ᡣȫ��Ϊ�������ģ�⡣

��������draw�������������ݣ������ơ�����/�����¼������ְ�������-1ռλ�Ҳ��������ݡ�������observation/feature�ǺϷ����룬tenpai/waits/loss��Ϊ�ල�ֶΣ����ܽ�������������3�۲�������ʵ��ͨ������ǰfeature����action��Ҫ����unknown���룬�з��������б�ʾ��

����callbackֻ�õ��Ϸ��۲���պͺϷ���ѡtuple������Table��PolicyValueΪdiscard-only actor-critic��һ��ѧϰ��λ��������ʽ���֣�������ѧϰagent�Զ��ģ�����PPO�������ع����������ԡ���ʵ31�ֳ���ѵ����30�ְ󶨰�ѵ����ִ�У�bound�汣��optimizer��torch/Python���״̬��seed��4Դ��hash��atomic��ʱ�ļ��滻checkpoint���ָ�����games������ʵ��20->30������δ��Ȩ�ؾܾ�resume��

MAHJONG_STOP_FILE��ÿ�ֿ�ʼ��鲢exit75��ǰһ������checkpoint�ѳ־û���ֹͣ���Ḳ����Ч�ϵ㡣��ǰʵ��stop�����ʱ��checkpoint��������δѵ��״̬��

С�Ͳ��ԱȽ���ʵִ��20seed*4��*3����=240�֣�ͬ��ʼseed���ֻ���λ��ԣ����Ի�ı�������棬����֤��ͬδ���켣�������������ӿ����飬��ǿ�����������ۡ�������־round2_d_trained_policy_eval.json��

δ��ɣ�4ѧϰ��λ�������ԣ�prediction��ģ�ͷ���policy�Ƚϣ������ṹ��ǩ����ʷ�������������޶����������ݣ���ȷ���أ���δ��ʵ΢�ֹ���C���������������/У׼����testδ����Dģ�͵��Ρ�

## ׷����������ѵ��

ʵ�ʹ���/�۲�/selfplay��Դ�����ǰ��ָ�Ʋ��䣬ȫ��������־hash�󶨣�����ʵ1000��120887���衣ѵ����ھܾ�ȱʧ/��ƥ����Ƽ�����1000��ƾ֣�resume��seed��ģʽ��source��audit��ϣ��

��������ʵ��50��ѵ�����ָ���55�֣�ÿ�����ߵ�������observer�����ø����վ�scores[q]/48���������������á�CPU2�̡߳�STOP�ļ�ʵ���˳�75��55��checkpoint���֡���������PPO��δ֤������������

��̨�������

    .venv/Scripts/python.exe scripts/round2_data_policy.py --games 1000 --selfplay --audit reports/round2_d_policy_audit.json --out checkpoints/round2_shared_policy --resume checkpoints/round2_shared_policy/last.pt

--games���ۼ��ܾ���������׷�Ӿ������Ĺ���/�۲�/selfplay���������checkpointͨ��last.tmpԭ���滻last.pt��

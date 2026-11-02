# �޶� C�����ѡ�ܹ���ģ��ָ��������

## ʵ��ִ����֤��

��ִ��CPU2��ƣ�δѵ�����硢δ����GPU��δ����RL��δ���κζ���final test����֤�طŲ��üȶ�validation seeds1800000..1800099��teacherֻ���������ƺ͹����۲졣��ʱ26.72�룬ʵ���˳���0��

- �ɸ��ֽű���scripts/revision_model_teacher_audit.py��
- ����ָ�꼰checkpoint/source SHA256��reports/revision_c_teacher_audit.json��
- ʵ�������־��reports/revision_c_teacher_audit.log��
- ʵ�ʽ����˳��룺reports/revision_c_teacher_audit_exitcode.txt��0����

���

    .venv/Scripts/python.exe scripts/revision_model_teacher_audit.py --seed 1800000 --games 100 --output reports/revision_c_teacher_audit.json

�������Ѷ�����֤�ƾֵĶ���������ƣ������¶����������ܲ��ԣ�candidateδ����Щseedѵ������imitation��28%ָ��Ҳ��ͬһ��֤��ֱ�Ӹ��֡�

## 28%�Ƿ�ֻ��utilityͬ�ֱ�����

�������ƹ�2939�����ߣ�teacher��1272�������ź�ѡ״̬��

|ģ��|exact|utility-equivalent|top3 exact target|top5 exact target|ƽ��teacher utility regret|
|---|---:|---:|---:|---:|---:|
|��128����ģ��ģ��|823/2939=28.00%|978/2939=33.28%|57.88%|78.05%|1.76761|
|���ѡ����raw|2675/2939=91.02%|100%|99.56%|100%|0|
|���ѡ����utility�ȶ�tie|100%|100%|100%|100%|0|

��ģ��2116��exactʧ���У�155����ͬЧ�õ���ͬ������1961��ȷʵѡ��ϲ�teacher utility��ֻ��Լ7.33%�ľ�exactʧ�ܿ�����ͬ�ֽ��ͣ���˲��ܰ�28%��Ҫ����������tie bug����ģ�����regret7��candidate raw��264��exactʧ��ȫ����ͬЧ�ò�ͬ���������regret0���˴�rawԼ91%ȷʵ��Ҫ�ܸ���tieӰ�졣����utility�Ǹ���ȷteacher�ලĿ�꣬��������ģ�Ϳ�����ȡ����ͨ�ù���

exact�������밴����legal˳��ѡ���teacher argmax��ȫͬ�ƣ�equivalent�����Ǻ�ѡteacher utility��������ֵ��topkʹ���ȶ�����ģ�ͺ�ѡ���֡�����Ψһteacher���������Ƿ���ǰk��regret=����teacher����utility����ѡ��ѡutility����ѡ������kʱtopk��Ȼ�����ף����ܰ�top5��ǿ����֤����

## ��structural shanten����

�±�Ϊ�������ƣ�������ǰ14�ȼ����Ƶ�minimum structural shanten���顣����ʹ��rules/hand_analysis.py��ԴSHA�Ѽ�¼�����Ǳ���ʵ�ֶ��Ƕ���Ȩ��oracle�����ܵ����������㷨�Ѿ�������֤��

|shanten|������|��exact|��equivalent|��ƽ��regret|candidate rounded exact/equivalent|
|---|---:|---:|---:|---:|---:|
|0|994|30.99%|38.43%|1.59859|100%/100%|
|1|1568|27.30%|31.12%|1.86288|100%/100%|
|2|372|22.31%|27.96%|1.83333|100%/100%|
|3|5|80.00%|80.00%|0.60000|100%/100%|

shanten3ֻ��5״̬�����ʺ��½��ۡ�����ֻ�������������teacherģ�£�����3*pairs+links����ʽ��ͬ����С���������Ž��Ų��ԡ�

## �������ѡ�ܹ�Ҫ��

��ʵ�֣�ͬһ��12ά���Դ������Ϸ���ѡ������������ѡ����ֻ����own/public���������pairs��links��triples��sequences��ȱ������singleton����candidate����/���������ȡ�teacher utility��Ϊ�ع�Ŀ�꣬ģ��Ȩ�ػָ�����pair/linkϵ��������������硣������ù������������Ϸ���ѡ����У����ȶ�tie��

��δʵ�ֻ�δ��֤������effective_draws/ukeire���ǵ�ǰ12ά������û��ǿBot������������֤����û��������ֵ������ƣ�����ͷ/��ʧβ��/teacher��RLĿ�겻һ�����������֤��������ģ��ֻ֤������ϻ�������ʽ�������������ָ�ǿ�齫���ԡ�

�˶Լ���candidate֤�ݣ�reports/round2_c_candidate.json��30��validation��886�������ƣ�utility����/����tieһ�¾�100%�����ζ���100��֤��2939��������Ҳ�ﵽͬ�����ۡ�reports/round2_c_candidate_game_parity.json��20��seed��4��=80�����֡�1186�ܿؾ��ߣ�zero action mismatch��ÿ��scores������ͬ����֤��teacher���֣�������������reports/round2_c_candidate_zero_residual.json����1809�Ϸ����ߣ�886���ɣ���в�greedy�벿��teacher��ƫ��޸��˾�unrounded residual��tie���졣reports/round2_c_candidate_resume.json��round2_c_candidate_stop.json��¼ʵ��CLI�ָ�/STOP�벻�жϿ��Ʋ���һ�¡�

## �޶����׼�����

�����û��ս����ż�������ǿBot����ֵ����������ǰ��������RL������û���κ���RL��GPUѵ����candidate����teacher��Ͽ���Ϊͨ��һ���ʾ��ලĿ���飬�������������ơ�ǿBot��ƻ��ֵĿ����ơ�ֻ�յ��û��г���Claude S0-S12��Ŀ��û��������ӦԴ�룬��˲��������Ѿ���ƻ�������S0-S12ϵͳ��

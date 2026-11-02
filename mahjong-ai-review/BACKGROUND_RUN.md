# ���غ�̨ʵ����ָ�

�������Ƕ���Python���򣬲�����AI�����ش𡣵����豣�ֿ���������/�ػ�ʱ������㡣��ֻ��ִ�����������񣬲������з���ʵ����޸����롣

ʵʱ״̬��experiments/round2_followup/state.json����������־ͬĿ¼*.log����Դ����resources.jsonl��pid��state.jsonΪ׼�����Python������PID���ܲ�ͬ����ǰ�������Σ��ṹ����ģ��ѵ����У׼����seed�������ԡ��������������ۼ�1000��ѵ����100seed����λ�������������������ư���

�ָ����ڹ���Ŀ¼PowerShell����

    .\.venv\Scripts\python.exe scheduler\runner.py scheduler\round2_followup.json

ֻ������һ��runner����Ŀ������������ʵ��������ƺ͹���ָ�Ʋ�ƥ���ֹͣ��ʧ�����ȶ�*.log��������ٻָ�������ű���--resume������������ظ����޸��Ѿ���ɵ��������ܾ����óɹ��������Ҫ�µ�ʵ��Ŀ¼��

��ȫֹͣ��

    Set-Content experiments\round2_followup\STOP 'user stop'

runner������checkpoint�����ȴ�30�룩��ѵ����batch/���ֱ߽籣����˳�����������޷���Ӧ����������ϵ㲢��ֹ�����񡣻ָ�ǰ�Ƴ�STOP����Ҫɾ��������Ŀ�ļ���

��Դ���ޣ������е�����GPU���Դ�7000MiB���¶�80�桢��Ϳ���RAM0.8GB��CPUѵ��4�߳�/����2�̣߳����6Сʱ��GPU���ʧЧֹͣ����¼GPU��RAM����������CPU�¶ȴ�������⡣�����ڲ�����������ܱ�֤OS����������

Դ���ż�������ָ��+�����������ư󶨣��κ�ʧ�ܺ󲻼������Ρ�����Ϊ�о�����������������齫AI���ա��޷��Զ��޸����´�������һ��AI�Ự��ϡ�

## ��ǰ��Ч��̨���У�����ǰ�ľ�·����
֮ǰround2_followup��warmstart���ж���ʵ����ɣ����ժҪ֤�ݱ����������鰴��runnerֱ��resume��state��
��ǰ��Ч���У�scheduler/round2_candidate_queue.json��
ʵʱ״̬��experiments/round2_candidate_queue/state.json����־ͬĿ¼����̨runnerʵ��pid44156��ѵ��child37324���ѹ۲쵽��283�֡�������Ŀ�����ݹ龲̬importָ�ơ�ԭ��checkpoint��append-only attempts.jsonl��
�ָ����

    .\.venv\Scripts\python.exe scheduler\runner.py scheduler\round2_candidate_queue.json

ֹͣ�ļ�Ϊexperiments/round2_candidate_queue/STOP��Ĭ��CPU2��RAM���1GB��80�����Դ�7000MiB��4Сʱdeadline��ִֻ��������1000�ֲв��Զ��ġ�100����seed��greedy�Աȡ��������ư�����������ʱ����������㡣

# ����������ָ�

����ָ���������RULES_PENDING.md�����ĸ���ģ�����ã�����΢��ƽ̨��֤��

�ڱ�Ŀ¼PowerShell���У�

    .\.venv\Scripts\python.exe -m unittest discover -s tests -v
    .\.venv\Scripts\python.exe scripts\gpu_probe.py
    .\.venv\Scripts\python.exe scripts\metrics_smoke.py
    .\.venv\Scripts\python.exe scripts\resume_smoke.py
    .\.venv\Scripts\python.exe scripts\train_evaluate.py datasets\simulation_v2\manifest.json

train_evaluate�ܾ������ѵ���ʵ�飻������ʹ���µ�ʵ��Ŀ¼���������� --help �鿴��ǰ��������ѵ���ײ�training.streaming.train֧��resume checkpoint��У������ָ�Ʋ��ָ�optimizer��CUDA RNG�������޸�manifest�ƹ���ơ�

ʵ��ģ�ͣ�checkpoints/simulation_v1/deploy.pt������simulation_v2�����ɣ�����Ŀ¼�������ã�

    from inference.predictor import Predictor
    predictor = Predictor('checkpoints/simulation_v1/deploy.pt')
    prediction = predictor.predict(features_128)

��������Ϊobservations.public.features������128ά������������������game������δ������Ծ��߻���ʵƽ̨��
������Դ�;ɰ汾���ִ�����datasets���汾source_snapshot/����ʽ�������ö�Ӧ���գ����ܰ��¹�����뵱������������Դ��

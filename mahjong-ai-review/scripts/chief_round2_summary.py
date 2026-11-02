"""Persist actual outcomes, never infer success from presence of checkpoints."""
import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
reports={}
for p in [root/'reports/round2_c_new_final.json',root/'reports/round2_c_new_calibration.json',root/'reports/round2_d_policy_evaluation.json',root/'reports/round2_d_trained_policy_eval.json']:
    if p.exists():reports[str(p.relative_to(root))]=json.loads(p.read_text())
for p in (root/'experiments/round2_c').glob('*/validation.json'):
    reports[str(p.relative_to(root))]=json.loads(p.read_text())
(root/'reports/round2_automatic_results.json').write_text(json.dumps(reports,indent=2))
(root/'ROUND2_REPORT.md').write_text('# �ڶ����Զ�ʵ����\n\n������Ϊʵ��������ָ����ܣ����ʵ�鲻����ģ�͸��ơ���������齫AI��δ���ա�\n\n```json\n'+json.dumps(reports,ensure_ascii=False,indent=2)+'\n```\n',encoding='utf-8')
with (root/'STATUS.md').open('a',encoding='utf-8') as f:f.write('\n�ڶ����Զ����������е����ܲ��裬ʵ��ָ���ROUND2_REPORT.md������state.json�������ɴ��϶�������Ŀ��ɡ�\n')
for name in ('TRAINING_LOG.md','FINAL_REPORT.md','EXPERIMENTS.md'):
    with (root/name).open('a',encoding='utf-8') as f:f.write('\n�ڶ����Զ�ʵ�����½���ѳ־û���ROUND2_REPORT.md��reports/round2_automatic_results.json���������޸������������Ϊ׼�����ܽ�ѵ����ɵ����ɹ���\n')

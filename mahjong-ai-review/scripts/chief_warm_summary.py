import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1];results={}
for label,name in [('imitation','round2_imitation_eval.json'),('imitation_then_rl','round2_imitation_rl_eval.json')]:
    r=json.loads((root/'reports'/name).read_text());c=r['comparisons']['trained_policy_value'];results[label]={'means':r['means'],'comparison':c,'clear_improvement':c['paired_seed_cluster_bootstrap_95ci'][0]>0,'scope':'configured_simulator_only'}
(root/'reports/round2_warmstart_results.json').write_text(json.dumps(results,indent=2))
text='\n\n## ģ�»������Ժ��Զ���ʵ��\n'+json.dumps(results,ensure_ascii=False,indent=2)+'\nֻ�ж�����������½����0�ű���ȷ���ƣ�ʧ�ܷ�������¼�������������齫AI�ɹ���\n'
for name in ('STATUS.md','TRAINING_LOG.md','EXPERIMENTS.md','FINAL_REPORT.md'):
    with (root/name).open('a',encoding='utf-8') as f:f.write(text)
print(json.dumps(results))

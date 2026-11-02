import json,pathlib
r=pathlib.Path(__file__).resolve().parents[1];p=r/'reports/round2_d_candidate_final_eval.json';v=json.loads(p.read_text());s={k:x for k,x in v.items() if k!='rows'};s['clear_improvement']=v['paired_seed_bootstrap_95ci'][0]>0
text='\n\n## ��ѡ�ṹ�в��Զ���ʵ�ʽ��\n'+json.dumps(s,ensure_ascii=False,indent=2)+'\n����1000��ѵ�������100�����������������������齫AI��ֻѧϰ���ƣ�����������ʽ������ȷ�����䲻��ɹ���\n'
for name in ('STATUS.md','TRAINING_LOG.md','EXPERIMENTS.md','FINAL_REPORT.md'):
    with (r/name).open('a',encoding='utf-8') as f:f.write(text)
(r/'reports/round2_candidate_summary.json').write_text(json.dumps(s,indent=2));print(json.dumps(s))

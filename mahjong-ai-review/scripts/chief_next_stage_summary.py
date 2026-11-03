import json,pathlib
r=pathlib.Path(__file__).resolve().parents[1];results={}
for label,name in [('loss_control','next_c_development20.json'),('relative_combo','next_c_relative_development20.json')]:
    v=json.loads((r/'reports'/name).read_text());assert v['status']=='completed' and v['complete_seed_groups']==20
    results[label]={k:v[k] for k in ('status','complete_seed_groups','summary','comparisons','limitations')}
results['scope']='development only; no final test tuning; no automatic promotion'
(r/'reports/next_chief_stage_results.json').write_text(json.dumps(results,indent=2))
text='\n\n## 新历史100训练局阶段真实开发对比\n'+json.dumps(results,ensure_ascii=False,indent=2)+'\n神经网络模仿改善不能代替净分证据；区间跨零不晋级；当前冠军不覆盖，1000/5000扩充另行受控。\n'
for name in ('STATUS.md','TRAINING_LOG.md','EXPERIMENTS.md','FINAL_REPORT.md'):
    with (r/name).open('a',encoding='utf-8') as f:f.write(text)
print('Development outcomes saved; champion unchanged')

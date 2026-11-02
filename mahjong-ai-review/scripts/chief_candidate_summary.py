import json,pathlib
r=pathlib.Path(__file__).resolve().parents[1];p=r/'reports/round2_d_candidate_final_eval.json';v=json.loads(p.read_text());s={k:x for k,x in v.items() if k!='rows'};s['clear_improvement']=v['paired_seed_bootstrap_95ci'][0]>0
text='\n\n## 候选结构残差自对弈实际结果\n'+json.dumps(s,ensure_ascii=False,indent=2)+'\n这是1000局训练后独立100种子组评估，不代表完整麻将AI；只学习舍牌，碰杠仍启发式。无明确正区间不标成功。\n'
for name in ('STATUS.md','TRAINING_LOG.md','EXPERIMENTS.md','FINAL_REPORT.md'):
    with (r/name).open('a',encoding='utf-8') as f:f.write(text)
(r/'reports/round2_candidate_summary.json').write_text(json.dumps(s,indent=2));print(json.dumps(s))

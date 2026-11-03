import json,pathlib
r=pathlib.Path(__file__).resolve().parents[1];p=r/'reports/v3_d_compare_5000000_mixed.json';v=json.loads(p.read_text())
assert v['status']=='completed' and v['complete_seed_groups']==5000
s={k:v[k] for k in ('status','complete_seed_groups','seconds','summary','comparisons','limitations')}
s.update(primary_predeclared='new_baseline vs shape',no_training=True,no_model_weights_replaced=True,no_expert_claim=True)
(r/'reports/v3_chief_final_evaluation_summary.json').write_text(json.dumps(s,indent=2))
text='\n\n## V3冻结独立评估实际结果\n5000组新发牌、四座轮换、五冻结策略。不是新神经网络训练。各款项以ledger互斥对账，原始逐局JSONL保留。\n'+json.dumps(s,ensure_ascii=False,indent=2)+'\n区间跨零即证据不足；该配置模拟结果不是现实高手认证。不得用本最终集继续调参。\n'
for name in ('STATUS.md','FINAL_REPORT.md','MODEL_SCORE_COMPARISON.md','BASELINE_V3_REPORT.md'):
    with (r/name).open('a',encoding='utf-8') as f:f.write(text)
print('Independent evaluation report persisted; no policy promoted automatically')

"""Persist actual outcomes, never infer success from presence of checkpoints."""
import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
reports={}
for p in [root/'reports/round2_c_new_final.json',root/'reports/round2_c_new_calibration.json',root/'reports/round2_d_policy_evaluation.json',root/'reports/round2_d_trained_policy_eval.json']:
    if p.exists():reports[str(p.relative_to(root))]=json.loads(p.read_text())
for p in (root/'experiments/round2_c').glob('*/validation.json'):
    reports[str(p.relative_to(root))]=json.loads(p.read_text())
(root/'reports/round2_automatic_results.json').write_text(json.dumps(reports,indent=2))
(root/'ROUND2_REPORT.md').write_text('# 第二轮自动实验结果\n\n本报告为实际已落盘指标汇总；完成实验不代表模型改善。完整会打麻将AI尚未验收。\n\n```json\n'+json.dumps(reports,ensure_ascii=False,indent=2)+'\n```\n',encoding='utf-8')
with (root/'STATUS.md').open('a',encoding='utf-8') as f:f.write('\n第二轮自动队列已运行到汇总步骤，实际指标见ROUND2_REPORT.md及调度state.json。不得由此认定完整项目完成。\n')
for name in ('TRAINING_LOG.md','FINAL_REPORT.md','EXPERIMENTS.md'):
    with (root/name).open('a',encoding='utf-8') as f:f.write('\n第二轮自动实验最新结果已持久化到ROUND2_REPORT.md和reports/round2_automatic_results.json；策略有无改善以配对评估为准，不能将训练完成当作成功。\n')

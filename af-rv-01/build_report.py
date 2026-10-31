"""Render committed results and reproducibility registry; does not run variants."""
import json,hashlib
from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parent
j=json.loads((R/'results/results.json').read_text()); rows=[]; lines=[]
lines += ['# AF-RV-01 运行报告', '', '**结论：'+j['conclusion']+'；三种主构造均不通过，OOS 各 11 笔 < 30 笔。**','', '预注册与四个数据文件未修改。仅使用 af-rv-01/ 输入；未获取新市场数据、未添加变体或调整参数。', '', '## 实现口径', '', '- 每构造从 1,000 USDT 开始，全窗口连续运行；IS/OOS 是同一权益曲线的日历切片，不重置账户或边界强平。段收益以段前一 bar 收盘权益为基准（含首 bar 成本），回撤包含此基准。逐笔统计按退出时间归段；费用/资金费按实际发生时间归段。', '- 滚动 OLS 含截距（协方差/方差斜率），样本标准差 ddof=1。β 首个有效值为第 720 根，z 要求连续 720 个有效的当时价差值，因此首个有效 z 为 '+j['descriptive']['first_valid_z_utc']+'。不回填、不使用不足窗口、不重算历史价差。', '- 次 bar 开盘双腿同步成交，开仓 gross 等于开仓前权益，按滑点后的成交价换算数量；持仓不重平衡。信号使用上一收盘时已知 β/波动率。', '- 同时触发退出时以止盈、止损、到期顺序标记原因；满 48 个持仓 bar 的收盘发出到期信号，下一开盘成交。退出后跳过 24 根收盘决策 bar，之后才允许发信号。', '- 资金费原始时间戳有毫秒抖动；映射到实际所在结算小时，保留全部真实费率，按该小时开盘成交后持仓、开盘价计费。记录数与最大抖动见下面验证数据。直接照抄单腿引擎的毫秒精确相等匹配会漏结算，因此未沿用此匹配缺陷。', '- 成本压力在相同全程连续账户上将手续费/滑点同时乘 1.5，报告其 OOS 切片；资金费保持原值。', '- 月分簇 bootstrap 按平仓月份汇总净盈亏，含零交易月份（2026-06）；每次有放回抽取 4 个月共 2000 次，numpy default_rng(42)，分位数使用线性插值。CI 单位为 USDT。', '- 半衰期为全程有效动态价差上 Δs 对 s_lag 的带截距 OLS，-ln(2)/斜率，仅作描述，不参与判定。', '- 同步成交与 gross 1 倍免强平均为预注册研究假设；本窗口 OOS 已被历史实验查看，结果不能称为最终验证。', '', '## 数据与审计', '', '```json', json.dumps(j['data_validation'],ensure_ascii=False,indent=2),'```', '', '五组 × 基准/压力 × 50%/75% 截断审计全部 PASS：各自匹配 5/14 笔自然已平仓交易，逐字段精确相等；截断末端不制造强平交易。', '', '## 全部度量', '', '|构造|段|净收益%|最大回撤%|PF|平仓笔数|胜率%|手续费 USDT|ETH资金费 USDT|BTC资金费 USDT|平均持有h|', '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for k,r in j['results'].items():
 for seg in ['IS','OOS','ALL']:
  x=r[seg]; rows.append({'construction':k,'segment':seg,**{a:b for a,b in x.items() if a!='exit_reasons'}})
  vals=[x[a] for a in ['net_return_pct','max_drawdown_pct','profit_factor','closed_trades','win_rate_pct','total_fees','funding_eth','funding_btc','average_holding_hours']]
  lines.append('|'+k+'|'+seg+'|'+'|'.join(f'{v:.6f}' if isinstance(v,float) else str(v) for v in vals)+'|')
lines += ['','资金费为账户现金流：正数收到、负数支付。C0 每段收益/回撤/笔数/费用均为 0，PF 不适用。','','|构造|段|止盈|止损|到期|数据结束|','|---|---|---:|---:|---:|---:|']
for k,r in j['results'].items():
 for seg in ['IS','OOS','ALL']:
  lines.append('|'+k+'|'+seg+'|'+'|'.join(str(v) for v in r[seg]['exit_reasons'].values())+'|')
lines += ['','## OOS CI 与成本压力','','|构造|净盈亏95% CI（USDT）|1.5倍成本净收益%|压力PF|压力回撤%|压力笔数|','|---|---|---:|---:|---:|---:|']
for k,r in j['results'].items():
 x=r['stress_OOS'];a,b=r['bootstrap']['ci95_usdt'];lines.append(f"|{k}|[{a:.6f}, {b:.6f}]|{x['net_return_pct']:.6f}|{x['profit_factor']:.6f}|{x['max_drawdown_pct']:.6f}|{x['closed_trades']}|")
lines += ['','## 六条标准与样本下限','','|构造|1净收益及优于对照|2 PF|3回撤|4 CI|5压力|6 IS同正|≥30笔|判定|','|---|---|---|---|---|---|---|---|---|']
for k in ['dollar','volatility','rolling_beta']:
 r=j['results'][k];lines.append('|'+k+'|'+'|'.join('通过' if v else '不通过' for v in r['six_rules']+[r['sample_minimum']])+'|'+r['verdict']+'|')
lines += ['','C1/C2 是对照，不参与候选晋级；两者 OOS 净收益为负且 11 笔，均不通过样本下限。','','## 描述统计与复现','','```json',json.dumps(j['descriptive'],ensure_ascii=False,indent=2),'```','','```sh','python -m unittest discover -s af-rv-01 -p test_af_rv_01.py','python af-rv-01/run_af_rv_01.py','python af-rv-01/build_report.py','```','','results.json 包含全精度结果、数据和代码 SHA-256、运行库版本；trades.csv 为逐笔交易；cashflows.csv 为逐笔费用及资金费现金流；equity.csv 为基准及压力权益；signals.csv 为因果信号序列。']
(R/'results/REPORT.md').write_text('\n'.join(lines)+'\n');pd.DataFrame(rows).to_csv(R/'results/summary.csv',index=False,float_format='%.17g')
reg={'experiment_id':'AF-RV-01','status':j['conclusion'],'seed':42,'parameters':{'window':720,'entry_z':2.,'exit_z':.5,'stop_z':3.5,'max_holding_bars':48,'cooldown_bars':24,'start_equity':1000,'gross_fraction':1.,'fee':.0005,'slip':.0002,'stress_multiplier':1.5,'bootstrap_replicates':2000,'oos_min_trades':30},'hashes':j['hashes'],'audit':'PASS','results':'af-rv-01/results/results.json','versions':j['versions']}
p=R.parent/'experiments/registry.jsonl';p.parent.mkdir(exist_ok=True)
old=p.read_text().splitlines() if p.exists() else []
old=[s for s in old if json.loads(s).get('experiment_id')!='AF-RV-01'];p.write_text('\n'.join(old+[json.dumps(reg,ensure_ascii=False)])+'\n')

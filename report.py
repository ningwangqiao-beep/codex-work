from pathlib import Path
import pandas as pd,numpy as np,json,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read_csv(path):
 return pd.read_csv(path if path.exists() else type(path)(str(path)+'.gz'))

ROOT=Path(__file__).parent;RES=ROOT/'results'
p=read_csv(RES/'all_results.csv');opt=p[p.candidate.str.startswith('C')].copy()
groups=opt.groupby('candidate');ranking=groups.agg(worst_return=('return_pct','min'),mean_return=('return_pct','mean'),worst_dd=('maxdd_pct','max'),bankrupt=('equity_le_zero','max'))
ranking=ranking.sort_values(['worst_return','worst_dd'],ascending=[False,True]);ranking.to_csv(RES/'ranking.csv');best=ranking.index[0]
params=json.loads((RES/'parameters.json').read_text());(RES/'best.json').write_text(json.dumps(dict(candidate=best,parameters=params[best],criterion='maximize minimum of W1/W2/W3 return; ties lower worst drawdown; all in-sample'),indent=2))
# Monthly equity attribution and execution aggregates for fallback.
monthly=[];trade_summary=[]
for w in ['W1','W2','W3']:
 folder=RES/best;t=read_csv(folder/f'{w}_trades.csv');e=read_csv(folder/f'{w}_equity.csv');e['month']=e.time_utc.str[:7];t['month']=t.time_utc.str[:7]
 start=10000.
 for month,x in e.groupby('month',sort=True):
  z=t[t.month==month];end=x.equity.iloc[-1]
  monthly.append(dict(window=w,month=month,start_equity=start,end_equity=end,pnl=end-start,return_pct=(end/start-1)*100,tp_n=int((z.kind==2).sum()),tp_net=z.loc[z.kind==2,'basket_net'].sum(),ladder_n=int((z.kind==3).sum()),ladder_net=z.loc[z.kind==3,'basket_net'].sum(),fees=z.fee.sum(),fills=len(z)))
  start=end
 for (side,kind),z in t.groupby(['side','kind']):
  trade_summary.append(dict(window=w,side='long' if side==1 else 'short',kind=int(kind),fills=len(z),notional=z.notional.sum(),fees=z.fee.sum(),gross=z.gross.sum(),closed_basket_net=z.loc[z.kind>=2,'basket_net'].sum()))
pd.DataFrame(monthly).to_csv(RES/'best_monthly.csv',index=False);pd.DataFrame(trade_summary).to_csv(RES/'best_trade_summary.csv',index=False)
# Visualizations derived from full 1m equity, sampled for rendering only.
fig,axes=plt.subplots(3,1,figsize=(13,11))
for ax,w in zip(axes,['W1','W2','W3']):
 for candidate in opt.candidate.unique():
  e=read_csv(RES/candidate/f'{w}_equity.csv');idx=np.unique(np.r_[np.arange(0,len(e),120),len(e)-1]);v=e.iloc[idx]
  ax.plot(pd.to_datetime(v.time_utc),v.equity,alpha=.2,color='gray',lw=.7)
 for candidate,color in [(best,'blue'),('A_b','red')]:
  e=read_csv(RES/candidate/f'{w}_equity.csv');idx=np.unique(np.r_[np.arange(0,len(e),120),len(e)-1]);v=e.iloc[idx]
  ax.plot(pd.to_datetime(v.time_utc),v.equity,label=candidate,color=color,lw=1.2)
 ax.axhline(10000,color='black',lw=.5);ax.set_title(w+' — all measurements computed on 1m closes');ax.set_ylabel('USD equity');ax.legend();ax.grid(alpha=.2)
fig.tight_layout();fig.savefig(RES/'equity_comparison.png',dpi=150);plt.close(fig)
def table(frame):
 cols=['candidate','window','return_pct','maxdd_pct','tp_n','tp_net','ladder_n','ladder_net','worst_basket','fees','account_n','signal_n','signal_net','equity_le_zero','dd_ge_60']
 f=frame[cols].copy();f.columns=['候选','窗口','收益%','回撤%','TP数','TP净额$','阶梯数','阶梯净额$','最差已平篮$','费用$','账止数','信号平篮数','信号净额$','权益≤0','回撤≥60%']
 return f.to_markdown(index=False,floatfmt='.2f')
text='''# ETHUSDT 双向篮子策略：1 分钟独立复现与优化

数据时区 UTC。W1=[2024-11-01,2025-05-01)，W2=[2025-05-01,2025-11-01)，W3=[2026-05-01,2026-10-31)。起始权益各 $10,000；各窗独立运行。所有最终评测使用原始 1m K 线；绘图抽样不参与计算。

'''
text+=f'本次30个候选均未三窗全正，也未达到三窗+300%。按最坏窗口收益选出的 {best} 是已测集合中的折中点，不是可盈利策略推荐。\n\n'
text+='## 数据完整性\n\n'+pd.DataFrame(json.loads((RES/'data_validation.json').read_text())).drop(columns=['gaps']).to_markdown(index=False)+'\n\n'
text+='## 主基线：优先满足成交边界\n\n'+table(p[p.candidate.isin(['A_a','A_b'])])+'\n\n'
text+='主基线允许逆向穿越格点的不利跳空加仓。止盈与同价重开是一对方向相反的成交；共同成交价必须在当根 [low,high] 内，否则整对不执行。这是固定格点、同价重开与成交边界冲突时的明确裁决，会偏离锚点行为。\n\n'
text+='## 锚点重放（仅诊断，不作为合规盈利结果）\n\n'+table(p[p.candidate.str.startswith('Anchor')])+'\n\n'
text+='Anchor 使用单边触发条件（多篮 TP 只检查 high≥目标，空篮 TP 只检查 low≤目标），随后在同格点重开。收益和回撤复现审计锚点，但少量重开产生极值外有利成交。详见 fill_audit.json 的逐笔实例；这会改变后续整条路径，差异不能当作普通手续费误差。W1 A_b: -26.62196%, DD 42.45493%；W2 -31.00511%；W3 -5.19301%。A_a W1 -10.00017%、W3 -9.09014%。\n\n'
text+='## 全部优化候选（最终合规版）\n\n'+table(opt)+'\n\n'
text+='## 候选参数\n\n'+pd.DataFrame([dict(candidate=k,**v) for k,v in params.items()]).fillna({'bias':1,'fast':360,'slow':1440,'regime_exit':0}).to_markdown(index=False)+'\n\n'
text+=f'## 最佳候选 {best}\n\n以三窗最低收益最大化选择；同值时优先最坏回撤较低。选优使用了三窗数据，因此是样本内搜索，不是独立样本外检验。\n\n```json\n'+json.dumps(params[best],indent=2)+'\n```\n\n'
text+='规则：每侧一篮，初始开多空各一笔；量加权均价。基础名义=base×最近收盘权益/10000；无历史收盘时用初始10000。若 bias>1，使用上一分钟更新后的 EMA_fast 与 EMA_slow 的方向：同向基础名义乘 bias，反向除 bias；EMA 相等时不调整。EMA 从首根开盘初始化，递推系数 2/(period+1)，仅每根事件完成后用本根收盘更新。所有开仓、止盈重开、阶梯重开及每次加仓均重新按同一历史权益/方向计算基础额；加仓再乘 mult^k，k 从1至 depth。\n\n'
text+='每根先处理两侧加仓，多侧优先；逆向自最近成交价移动 g，逐级执行。拟新增名义加当前两篮累计入场名义超过 cap×最近收盘权益则跳过，本根该侧停止尝试，后续分钟可重试；跳过不推进层级。止盈目标=篮均价×(1+side×tp)，满足成交边界才整篮平仓并同价立即重开；每侧每根至多一次。全部加仓先于任一止盈。若 regime_exit=1，上根收盘所得 EMA 方向与前一次处理方向不同且非0，则在本根开盘按开盘价先平两个旧篮（记信号平篮，篮数与净额另列），随后按新方向在同一开盘价重开双篮，再执行当根加仓与止盈；首个从0到非0的信号也执行。深度满后再逆向一格，用该根极值触发、收盘平仓，并在同一收盘价立即重开该侧（优化 stopnext=0），其他侧继续持篮。非破产期间始终双篮；基线 stopnext=1 的停机/阶梯例外按原规格处理。\n\n'
text+='优化 dd=1，即不设置正权益账户回撤止损；权益≤0 时按收盘全平并永久停机，仍报告此时负权益。回撤≥60%单独标记，不等于交易所实际清算模型。本模型没有保证金、强平、资金费或借币费。每笔成交扣0.07%实际名义额。收盘权益=现金+多篮浮盈亏+空篮浮盈亏；收盘历史峰值初始10000，回撤始终不重置。末根以未平仓浮盈亏盯市，不强制平仓，不收虚构的末期平仓费。\n\n'
text+='TP/阶梯净额包含对应篮所有入场、加仓和平仓费用；最差单篮是已平篮净损失，未平篮另列 open_gross/open_entry_fees。总收益与已平篮净额差来自末期未平篮浮盈亏及已扣入场费。各窗起始、账户重启均按开盘开双篮；基线12%账户止损在收盘执行，完整停机后 i+1441 开盘重启，变体(a)参考峰值不重置，(b)重启时置为现金权益。账户爆仓前峰值与用于统计回撤的全窗峰值分开。\n\n'
text+='## 最佳候选月度拆分\n\n'+pd.DataFrame(monthly).to_markdown(index=False,floatfmt='.2f')+'\n\n## 最佳候选逐笔成交汇总\n\n'+pd.DataFrame(trade_summary).to_markdown(index=False,floatfmt='.2f')+'\n\n'
text+='## 复现\n\nPython依赖见 requirements.txt。依次运行 fetch.py、test_engine.py、baselines.py、optimize.py、refine.py、structural.py、verify_results.py、report.py。CSV 原始行情与逐分钟权益可 gzip 无损保存；读取器同时支持 .csv 和 .csv.gz。成交 CSV 保留逐笔行。所有102组结果通过资金账本、逐篮费用、收盘回撤、TP频率与成交边界校验；优化候选还检查了每分钟收盘双篮。锚点重放的有利越界成交单列为已知违规。\n'
(ROOT/'REPORT.md').write_text(text)
print('BEST',best);print(ranking.round(4).to_string());print(table(opt));print(pd.DataFrame(monthly).round(4).to_string(index=False))

from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=pd.read_csv(RESULTS/'candidates.csv');cmp=pd.read_csv(RESULTS/'comparison.csv');h=pd.read_csv(RESULTS/'holdout.csv');s=json.loads((RESULTS/'selection.json').read_text());protocol=json.loads((RESULTS/'holdout_protocol.json').read_text());params=json.loads((ROOT/'search_space.json').read_text());best=s['candidate']
# Display all 24 candidates with the three windows together and full precision in CSV.
compact=[]
for name,pr in params.items():
 x=p[p.candidate==name];row={'候选':name,'格距%':pr['g']*100,'倍数':pr['mult'],'TP%':pr['tp']*100}
 for w in ['W1','W2','W3']:
  z=x[x.window==w].iloc[0];row[w+' 收益%/回撤%/费用$/账止']=f'{z.return_pct:.2f} / {z.maxdd_pct:.2f} / {z.fees:.2f} / {int(z.account_n)}'
 row['最差窗%']=x.return_pct.min();row['三窗合计%']=x.return_pct.sum();compact.append(row)
ct=pd.DataFrame(compact);ct.to_csv(RESULTS/'candidate_display.csv',index=False)
comparison=cmp[['strategy','window','old_return','canonical_return','total_delta_pp','tp_delta_pp','add_clip_delta_pp','old_dd','new_dd','old_fees','new_fees','new_account_n']].copy()
comparison.columns=['策略','窗','旧收益%','新收益%','净变化pp','仅TP贡献pp','夹价增量pp','旧回撤%','新回撤%','旧费用$','新费用$','新账止']
ht=h[['candidate','window','return_pct','maxdd_pct','fees','account_n','tp_n','tp_net','ladder_n','ladder_net','worst_basket','equity_le_zero','dd_ge_60','passed_holdout']].copy()
ht.columns=['候选','窗','收益%','回撤%','费用$','账止','TP数','TP净额$','阶梯数','阶梯净额$','最差已平篮$','权益≤0','回撤≥60%','通过留出']
win=h[h.candidate==best].iloc[0];verdict='样本内最优未通过留出验证' if not win.passed_holdout else '样本内最优通过本次留出验证；这不构成其他市场阶段的保证'
text='# 第二轮：canonical 成交、C04 邻域搜索及 W0 留出验证\n\n'
text+=f'结论：**{verdict}**。唯一入选为 **{best}**，W0 收益 {win.return_pct:.6f}%，收盘最大回撤 {win.maxdd_pct:.6f}%。选定后未调参、未更换候选。\n\n'
text+='## 预注册搜索空间与口径\n\n'+(ROOT/'SEARCH_PLAN.md').read_text()+'\n\n'
text+='上一轮代码并未对不利跳空加仓夹价，因此本轮按用户括号中的明确要求采用 actual_fill=clip(grid,low,high)，最近成交价取 actual_fill。为避免把加仓变化误归因于 TP，额外运行了仅修正 TP 的 bridge；bridge 不是候选，不参与选优。旧数字均取第一轮合规主基线，已作废锚点不用于比较。\n\n'
text+='TP 按方向触发（多 high≥目标，空 low≤目标），目标在本根区间内用目标价，否则用本根开盘价平仓并同价重开。仍先加仓后TP；即使该分钟加仓改变了篮均价，TP阶段的开盘回退也按冻结规则执行。每侧每根至多一次TP。深度5、2%权益基础额、4倍累计入场名义额上限、0.07%逐笔费用、末期盯市和原有止损重开语义均不变。无资金费或借币费。\n\n'
text+='## 新旧口径对照\n\n'+comparison.to_markdown(index=False,floatfmt='.4f')+'\n\n净变化以百分点pp表示，且净变化=仅TP贡献+加仓夹价增量。这是路径重新运行的差，不是逐笔利润静态相加。旧/新最大回撤均为完整分钟收盘权益回撤；统计峰值不重置。\n\n'
text+='## 第二轮24候选：全部为样本内搜索\n\n'+ct.to_markdown(index=False,floatfmt='.2f')+'\n\n'
text+='排序先三窗最低收益，后独立三窗收益之和；合计不是连续复利收益，未用回撤或W0作为排序条件。所有候选无正权益账户止损，权益≤0仍清仓永久停机，回撤≥60%单列标记。详细TP、阶梯、费用、最大篮损、敞口跳过及风险标记见 candidates.csv / all_results.csv。\n\n'
text+=f'唯一入选 {best} 参数：\n\n```json\n'+json.dumps(s['parameters'],indent=2)+'\n```\n\n'
text+='## 留出访问与锁定证据\n\n锁定文件：\n\n```json\n'+json.dumps(s,indent=2)+'\n```\n\n首次访问协议：\n\n```json\n'+json.dumps(protocol,indent=2)+'\n```\n\n'
text+='W0 在锁定并提交唯一候选后才通过 Binance REST 分页获取。仅跑所选候选及原C04两次，不比较其他候选；从初始10000独立双开，无预热或窗口外状态。C04“原版”指原参数与结构，成交同样统一使用本轮canonical。\n\n'
text+='## 留出窗专表\n\n'+ht.to_markdown(index=False,floatfmt='.4f')+'\n\n**'+verdict+'**。判据为W0收益<0或分钟收盘最大回撤≥60%；结果不反向参与选优。\n\n'
text+='## 数据完整性\n\n'
v=json.loads((RESULTS/'training_data_validation.json').read_text())+[json.loads((RESULTS/'holdout_data_validation.json').read_text())]
text+=pd.DataFrame(v).to_markdown(index=False)+'\n\n'
text+='W1/W2/W3沿用上一轮完整分钟行情并重新验证根数、时间、OHLC、SHA256；W0新拉取。原始OHLCV与全分辨率权益无损gzip保存，成交CSV逐笔保存。所有时间UTC，起日包含、终日次日零点不包含。\n\n'
text+='## 验证\n\n'+(RESULTS/'verification.txt').read_text()+'\n8项引擎测试另见 test_engine.py，覆盖双方向跳空TP、区间夹价、区间外但方向未触发、同价重开、费用账本、多级加仓、根内顺序及前缀无未来依赖。\n'
(ROOT/'REPORT.md').write_text(text)
# Render-only sampling; all stored CSV and statistics retain every minute.
fig,axes=plt.subplots(4,1,figsize=(12,13))
for ax,w in zip(axes,['W1','W2','W3','W0']):
 for name in [best,'C04']:
  e=pd.read_csv(RESULTS/name/f'{w}_equity.csv.gz');idx=np.unique(np.r_[np.arange(0,len(e),120),len(e)-1]);z=e.iloc[idx]
  ax.plot(pd.to_datetime(z.time_utc),z.equity,label=name,lw=1)
 ax.axhline(10000,color='gray',lw=.6);ax.set_title(w+(' HOLDOUT' if w=='W0' else ' IN-SAMPLE'));ax.set_ylabel('Close equity USD');ax.grid(alpha=.2);ax.legend()
fig.tight_layout();fig.savefig(RESULTS/'equity_comparison.png',dpi=140);plt.close(fig)
print('COMPARISON\n'+comparison.to_markdown(index=False,floatfmt='.4f'))
print('CANDIDATES\n'+ct.to_markdown(index=False,floatfmt='.2f'))
print('HOLDOUT\n'+ht.to_markdown(index=False,floatfmt='.4f'))
print(verdict)

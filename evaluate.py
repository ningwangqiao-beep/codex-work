import pathlib,json,numpy as np,pandas as pd
from engine import run
ROOT=pathlib.Path(__file__).parent
DATA={w:np.loadtxt((ROOT/'data'/f'{w}.csv') if (ROOT/'data'/f'{w}.csv').exists() else (ROOT/'data'/f'{w}.csv.gz'),delimiter=',',skiprows=1) for w in ['W1','W2','W3']}
def evaluate(name,params,record=True,runner=run):
 rows=[]
 for w,a in DATA.items():
  r,d,s,b,e,t=runner(a,**params,record=int(record));row=dict(candidate=name,window=w,return_pct=r*100,maxdd_pct=d*100,tp_n=int(s[0]),tp_net=s[1],ladder_n=int(s[2]),ladder_net=s[3],worst_basket=s[4],fees=s[5],account_n=int(s[6]),cap_skips=int(s[7]),account_net=s[8],terminal_net=s[9],open_gross=s[10],open_entry_fees=s[11],signal_n=int(s[12]) if len(s)>12 else 0,signal_net=s[13] if len(s)>12 else 0.,equity_le_zero=bool(b),dd_ge_60=bool(d>=.6))
  rows.append(row);print(json.dumps(row),flush=True)
  if record:
   out=ROOT/'results'/name;out.mkdir(parents=True,exist_ok=True)
   pd.DataFrame({'time_utc':pd.to_datetime(a[:,0],unit='ms',utc=True),'equity':e}).to_csv(out/f'{w}_equity.csv',index=False)
   trades=pd.DataFrame(t,columns=['bar','side','kind','price','qty','notional','fee','gross','basket_net','basket_id']);trades.insert(0,'time_utc',pd.to_datetime(a[trades.bar.astype(int),0],unit='ms',utc=True));trades.to_csv(out/f'{w}_trades.csv',index=False)
 return rows
if __name__=='__main__':
 rows=[]
 for name,p in [('A_a',{'reset':0}),('A_b',{'reset':1})]:rows+=evaluate(name,p)
 pd.DataFrame(rows).to_csv(ROOT/'results'/'baseline.csv',index=False)

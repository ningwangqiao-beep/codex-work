from evaluate import ROOT,evaluate
import pandas as pd,json
# Additional trend-asymmetric trials; EMA uses previous bars only.
specs=[('C19',.01,1.3,4,.015,200,4,5,60,720),('C20',.02,1.3,4,.025,200,4,5,360,1440),('C21',.01,1.3,4,.015,500,8,5,60,720),('C22',.02,1.3,4,.025,500,8,5,360,1440),('C23',.01,1.3,4,.015,1000,16,5,60,720),('C24',.02,1.3,4,.025,1000,16,5,360,1440)]
rows=[];params=json.loads((ROOT/'results'/'parameters.json').read_text())
for name,g,m,d,tp,b,cap,bias,fast,slow in specs:
 p=dict(g=g,mult=m,depth=d,tp=tp,base=b,cap=cap,bias=bias,fast=fast,slow=slow,compound=1,dd=1.,reset=1,stopnext=0)
 params[name]=p;rows+=evaluate(name,p)
pd.DataFrame(rows).to_csv(ROOT/'results'/'refinement.csv',index=False)
(ROOT/'results'/'parameters.json').write_text(json.dumps(params,indent=2))

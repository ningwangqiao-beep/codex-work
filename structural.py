from evaluate import ROOT,evaluate
import pandas as pd,json
specs=[('C25',500,60,720),('C26',2000,360,1440),('C27',8000,360,1440),('C28',500,1440,10080),('C29',2000,1440,10080),('C30',8000,1440,10080)]
rows=[];params=json.loads((ROOT/'results'/'parameters.json').read_text())
for name,base,fast,slow in specs:
 p=dict(g=.02,mult=1.2,depth=2,tp=.04,base=base,cap=16.,bias=10.,fast=fast,slow=slow,regime_exit=1,compound=1,dd=1.,reset=1,stopnext=0)
 params[name]=p;rows+=evaluate(name,p)
pd.DataFrame(rows).to_csv(ROOT/'results'/'structural.csv',index=False)
(ROOT/'results'/'parameters.json').write_text(json.dumps(params,indent=2))

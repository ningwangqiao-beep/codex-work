from evaluate import evaluate,ROOT
import pandas as pd,json
# Fixed, disclosed 18-point structural search. All trials use all three 1m windows.
# id, grid, multiplier, depth, TP, base as dollars per initial $10k, cap
specs=[
('C01',.005,1.5,5,.004,200,4),
('C02',.01,1.5,5,.008,200,4),
('C03',.02,1.5,5,.015,200,4),
('C04',.03,1.5,5,.02,200,4),
('C05',.02,2.,5,.015,200,4),
('C06',.03,2.,5,.02,200,4),
('C07',.05,2.,5,.03,200,4),
('C08',.01,1.2,8,.008,500,4),
('C09',.02,1.2,8,.015,500,4),
('C10',.03,1.2,8,.025,500,4),
('C11',.01,1.5,5,.008,1000,4),
('C12',.02,1.5,5,.015,1000,4),
('C13',.03,1.5,5,.02,1000,4),
('C14',.02,2.,5,.015,500,8),
('C15',.03,2.,5,.02,1000,8),
('C16',.05,2.,5,.03,1000,8),
('C17',.03,2.,5,.02,2000,16),
('C18',.05,2.,5,.03,2000,16)]
if __name__=='__main__':
 rows=[];params={}
 for name,g,m,d,tp,b,cap in specs:
  p=dict(g=g,mult=m,depth=d,tp=tp,base=b,cap=cap,compound=1,dd=1.,reset=1,stopnext=0)
  params[name]=p;rows+=evaluate(name,p)
  pd.DataFrame(rows).to_csv(ROOT/'results'/'optimization.csv',index=False)
  (ROOT/'results'/'parameters.json').write_text(json.dumps(params,indent=2))

from evaluate import evaluate,ROOT
from anchor_engine import run as anchor_run
import pandas as pd
rows=[]
for name,p in [('A_a',{'reset':0}),('A_b',{'reset':1})]:rows+=evaluate(name,p)
pd.DataFrame(rows).to_csv(ROOT/'results'/'baseline.csv',index=False)
rows=[]
for name,p in [('Anchor_a',{'reset':0}),('Anchor_b',{'reset':1})]:rows+=evaluate(name,p,runner=anchor_run)
pd.DataFrame(rows).to_csv(ROOT/'results'/'anchor_replay.csv',index=False)

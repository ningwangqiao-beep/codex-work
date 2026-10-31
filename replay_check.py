"""Recompute every published run from final source without reading saved trade outcomes."""
from evaluate import ROOT,DATA
from engine import run
from anchor_engine import run as anchor_run
import json,pandas as pd,numpy as np
params=json.loads((ROOT/'results'/'parameters.json').read_text());results=pd.read_csv(ROOT/'results'/'all_results.csv')
for _,row in results.iterrows():
 name=row.candidate;fn=anchor_run if name.startswith('Anchor') else run
 p=params[name] if name.startswith('C') else dict(reset=int(name.endswith('_b')))
 r,d,s,b,e,t=fn(DATA[row.window],**p)
 assert abs(r*100-row.return_pct)<1e-8,(name,row.window,r,row.return_pct)
 assert abs(d*100-row.maxdd_pct)<1e-8
 assert abs(s[5]-row.fees)<1e-6
 assert int(s[0])==row.tp_n and int(s[2])==row.ladder_n
print('PASS: final-source replay of all 102 candidate-window results.',flush=True)

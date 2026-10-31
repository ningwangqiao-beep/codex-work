from pathlib import Path
import numpy as np,pandas as pd,json,hashlib,gzip,datetime
from engine import run
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent
RESULTS=ROOT/'results'
RESULTS.mkdir(exist_ok=True)
C04=dict(g=.03,mult=1.5,depth=5,tp=.02,base=200.,cap=4.,compound=1,dd=1.,reset=1,stopnext=0)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load_window(w):
 path=(ROOT if w=='W0' else PROJECT)/'data'/f'{w}.csv.gz'
 if not path.exists():path=path.with_suffix('')
 a=np.loadtxt(path,delimiter=',',skiprows=1)
 return a
def validate(w,a,start,end):
 startms=int(pd.Timestamp(start,tz='UTC').timestamp()*1000);endms=int(pd.Timestamp(end,tz='UTC').timestamp()*1000)
 times=a[:,0].astype(np.int64);expected=np.arange(startms,endms,60000,dtype=np.int64)
 missing=np.setdiff1d(expected,times);extra=np.setdiff1d(times,expected);duplicates=len(times)-len(np.unique(times))
 assert len(missing)==len(extra)==duplicates==0 and np.array_equal(times,expected),(w,'time validation')
 assert np.isfinite(a).all() and (a[:,1:5]>0).all() and (a[:,5]>=0).all()
 assert (a[:,2]>=np.maximum(a[:,1],a[:,4])).all() and (a[:,3]<=np.minimum(a[:,1],a[:,4])).all()
 path=(ROOT if w=='W0' else PROJECT)/'data'/f'{w}.csv.gz'
 raw=gzip.decompress(path.read_bytes()) if path.exists() else path.with_suffix('').read_bytes()
 return dict(window=w,start_utc=start,end_exclusive_utc=end,expected=len(expected),actual=len(a),missing=0,duplicates=0,outside=0,sha256_csv=hashlib.sha256(raw).hexdigest())
def evaluate(name,w,a,p):
 r,d,s,b,e,logs=run(a,record=1,**p)
 row=dict(candidate=name,window=w,return_pct=r*100,maxdd_pct=d*100,fees=s[5],account_n=int(s[6]),tp_n=int(s[0]),tp_net=s[1],ladder_n=int(s[2]),ladder_net=s[3],worst_basket=s[4],cap_skips=int(s[7]),account_net=s[8],open_gross=s[10],open_entry_fees=s[11],tp_gap_n=int(s[14]),add_clamp_n=int(s[15]),equity_le_zero=bool(b),dd_ge_60=bool(d>=.6))
 out=RESULTS/name;out.mkdir(exist_ok=True)
 pd.DataFrame(dict(time_utc=pd.to_datetime(a[:,0],unit='ms',utc=True),equity=e)).to_csv(out/f'{w}_equity.csv.gz',index=False,compression={'method':'gzip','compresslevel':3})
 trades=pd.DataFrame(logs,columns=['bar','side','kind','price','qty','notional','fee','gross','basket_net','basket_id'])
 trades.insert(0,'time_utc',pd.to_datetime(a[trades.bar.astype(int),0],unit='ms',utc=True));trades.to_csv(out/f'{w}_trades.csv',index=False)
 (out/f'{w}_parameters.json').write_text(json.dumps(p,indent=2))
 print(json.dumps(row),flush=True)
 return row

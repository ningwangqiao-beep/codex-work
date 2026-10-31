import urllib.request,urllib.parse,json,datetime,concurrent.futures,time,pathlib,hashlib,csv
ROOT=pathlib.Path(__file__).parent
WINDOWS={'W1':('2024-11-01','2025-05-01'),'W2':('2025-05-01','2025-11-01'),'W3':('2026-05-01','2026-10-31')}
def ms(d): return int(datetime.datetime.fromisoformat(d).replace(tzinfo=datetime.timezone.utc).timestamp()*1000)
def page(task):
 w,a,b=task;p=ROOT/'data'/w/f'{a}.json';p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists(): return json.loads(p.read_text())
 u='https://data-api.binance.vision/api/v3/klines?'+urllib.parse.urlencode(dict(symbol='ETHUSDT',interval='1m',startTime=a,endTime=b-1,limit=1000))
 for i in range(8):
  try:
   with urllib.request.urlopen(u,timeout=45) as r: rows=json.load(r)
   assert isinstance(rows,list)
   p.write_text(json.dumps(rows,separators=(',',':')))
   return rows
  except Exception:
   if i==7: raise
   time.sleep(min(2**i,30))
def main():
 report=[]
 for w,(start,end) in WINDOWS.items():
  a,b=ms(start),ms(end);tasks=[(w,t,min(t+60000000,b)) for t in range(a,b,60000000)]
  rows=[]
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
   for j,part in enumerate(pool.map(page,tasks)):
    rows.extend(part)
    if j%50==0: print(w,j,'/',len(tasks),flush=True)
  rows.sort(key=lambda r:r[0]);ts=[r[0] for r in rows];expected=set(range(a,b,60000));actual=set(ts)
  missing=sorted(expected-actual);dup=len(ts)-len(actual);outside=actual-expected
  gaps=[]
  for t in missing:
   if gaps and t==gaps[-1][1]+60000:gaps[-1][1]=t
   else:gaps.append([t,t])
  rec=dict(window=w,start_utc=start,end_exclusive_utc=end,expected=(b-a)//60000,actual=len(rows),duplicates=dup,missing=len(missing),outside=len(outside),gaps=gaps)
  path=ROOT/'data'/f'{w}.csv'
  with path.open('w') as f:
   wr=csv.writer(f);wr.writerow(['time','open','high','low','close','volume']);wr.writerows([r[:6] for r in rows])
  rec['sha256']=hashlib.sha256(path.read_bytes()).hexdigest();report.append(rec);print(rec,flush=True)
  (ROOT/'results'/'data_validation.json').write_text(json.dumps(report,indent=2))
  if missing or dup or outside: raise RuntimeError('Incomplete or invalid window; refuse evaluation')
if __name__=='__main__':main()

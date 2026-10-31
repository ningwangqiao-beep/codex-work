"""Only locked winner and original C04. No ranking or tuning here."""
from common import *
import importlib.util,shutil,subprocess
lock=RESULTS/'selection.json'
assert lock.exists(),'Select on W1-W3 before fetching W0'
selection=json.loads(lock.read_text());assert selection['w0_accessed'] is False
assert selection['candidate_results_sha256']==sha(RESULTS/'candidates.csv')
assert selection['space_sha256']==sha(ROOT/'search_space.json')
meta=RESULTS/'holdout_protocol.json'
if meta.exists():raise RuntimeError('W0 already accessed; refuse repeated holdout experiment')
meta.write_text(json.dumps(dict(first_access_utc=now(),pre_holdout_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=PROJECT,text=True).strip(),selection_sha256=sha(lock),candidate=selection['candidate'],tested_only=[selection['candidate'],'C04'],criterion='fail if return<0 or close max drawdown>=60%'),indent=2))
spec=importlib.util.spec_from_file_location('binance_fetch',PROJECT/'fetch.py');fetch=importlib.util.module_from_spec(spec);spec.loader.exec_module(fetch)
fetch.ROOT=ROOT;fetch.WINDOWS={'W0':('2023-11-01','2024-05-01')};fetch.main()
a=load_window('W0');validation=validate('W0',a,'2023-11-01','2024-05-01')
(RESULTS/'holdout_data_validation.json').write_text(json.dumps(validation,indent=2))
rows=[evaluate(selection['candidate'],'W0',a,selection['parameters']),evaluate('C04','W0',a,C04)]
f=pd.DataFrame(rows);f['passed_holdout']=(f.return_pct>=0)&(f.maxdd_pct<60);f.to_csv(RESULTS/'holdout.csv',index=False)
with (ROOT/'data/W0.csv').open('rb') as src,gzip.open(ROOT/'data/W0.csv.gz','wb',compresslevel=6) as dst:shutil.copyfileobj(src,dst)
(ROOT/'data/W0.csv').unlink()
print('HOLDOUT COMPLETE; NO FURTHER TUNING',flush=True)

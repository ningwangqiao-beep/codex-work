import sys,pathlib,tempfile,json,hashlib,torch
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from models.networks import MahjongBrain
from training.streaming import train
from training.gate import fingerprint
from inference.predictor import Predictor
root=pathlib.Path(__file__).resolve().parents[1];out=root/'experiments'/'synthetic_resume';out.mkdir(parents=True,exist_ok=True)
rules=out/'synthetic_rules.txt';rules.write_text('SYNTHETIC INTERFACE TEST ONLY')
shards={}
for split in ('train','validation','test'):
 p=out/(split+'.jsonl');r={'game_id':split,'seed':split,'source_group':'synthetic','features':[0.]*8,'tenpai':[0,1,0],'waits':[[0]*27 for _ in range(3)],'joint_outcome':[0]*27,'loss':[0]*27};p.write_text(json.dumps(r)+'\n');shards[split]=[str(p)]
hashes={str(p):fingerprint(p) for v in shards.values() for p in v};bound=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest();rh=fingerprint(rules)
m={'synthetic_only':True,'rules_audit_passed':True,'approval_for_training':True,'dataset_version':'SYNTHETIC-TEST','rules_path':str(rules),'rules_sha256':rh,'shards':shards,'audit':{'passed':True,'dataset_sha256':bound,'rules_sha256':rh}}
torch.manual_seed(3);a=MahjongBrain(8,loss_bins=[0,1]).cuda();train(a,m,out,epochs=1);train(a,m,out,epochs=2,resume=out/'last.pt');s=torch.load(out/'last.pt',weights_only=False);assert s['epoch']==1 and s['optimizer']['state'];p=Predictor(out/'last.pt');r=p.predict([0.]*8);assert len(r['expected_loss'][0])==27
report={'synthetic_only':True,'epochs':2,'checkpoint_resume':True,'optimizer_restored':True,'cuda_rng_saved':bool(s['cuda_rng']),'predictor_loaded':True};(root/'reports'/'employee_c_resume.json').write_text(json.dumps(report,indent=2));print(report)

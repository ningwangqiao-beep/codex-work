"""Read-only lineage inventory. No model/data retraining or final-test evaluation."""
import pathlib,json,hashlib,torch,datetime
root=pathlib.Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
paths=sorted((root/'checkpoints').glob('*/*.pt'))+[root/'experiments/round2_c/candidate/best.pt']
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'legacy_lineage_inventory_not_V3_performance','weights':[],'datasets':[],'current_source_hashes':{}}
for p in paths:
 if p.suffix!='.pt':continue
 try:
  if 'torchscript' in p.name:
   result['weights'].append({'path':str(p.relative_to(root)),'sha256':sha(p),'bytes':p.stat().st_size,'format':'TorchScript raw legacy logits','v3_score_compatible':False});continue
  s=torch.load(p,map_location='cpu',weights_only=False);entry={'path':str(p.relative_to(root)),'sha256':sha(p),'bytes':p.stat().st_size,'checkpoint_keys':list(s),'model_parameter_tensors':len(s.get('model',{})),'v3_trained':False,'v3_score_compatible':False}
  for k in ['version','model_version','dataset_version','dataset_fingerprint','binding','epoch','games','seed','model_config','config','teacher_definition','target_semantics','source_hashes','source','audit_sha256','selfplay','temperature']:
   if k in s:
    v=s[k]
    if isinstance(v,(str,int,float,bool,list,dict,type(None))):entry[k]=v
  result['weights'].append(entry)
 except Exception as e:result['weights'].append({'path':str(p.relative_to(root)),'error':repr(e)})
for p in sorted((root/'datasets').glob('*/manifest.json')):
 m=json.load(open(p));snap=pathlib.Path(m.get('rules_path',''));entry={'path':str(p.relative_to(root)),'manifest_sha256':sha(p),'dataset_version':m.get('dataset_version'),'training_rule_sha256':m.get('rules_sha256'),'rule_snapshot_exists':snap.is_file(),'rule_snapshot_sha256':sha(snap) if snap.is_file() else None,'recorded_audit':m.get('audit'),'v3_training_compatible':False,'shards':[]}
 for split,files in m.get('shards',{}).items():
  for name in files:
   f=pathlib.Path(name);entry['shards'].append({'split':split,'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f)})
 entry['statistics']=m.get('statistics');result['datasets'].append(entry)
for rel in ['rules/core.py','rules/v3.py','rules/hand_analysis.py','rules/hand_analysis_reference.py','simulator/table.py','simulator/selfplay.py','observations/public.py','models/revision_action_value.py','models/round2_candidate.py','models/round2_candidate_residual.py']:
 p=root/rel
 if p.exists():result['current_source_hashes'][rel]=sha(p)
result['source_status']='current source inventory only; V3 rules under B audit, not certified';(root/'reports/v3_c_legacy_inventory.json').write_text(json.dumps(result,indent=2));print('weights',len(result['weights']),'datasets',len(result['datasets']),'errors',sum('error' in r for r in result['weights']))

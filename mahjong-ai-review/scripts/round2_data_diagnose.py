"""Teacher-state agreement and value diagnostics, no policy tuning."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from simulator.selfplay import play
from simulator.policy_learning import PolicyValue
from observations.public import features
root=Path(__file__).resolve().parents[1];torch.set_num_threads(2);models={};report={}
for name,file in [('imitation','imitation_last.pt'),('rl','last.pt')]:
 p=root/'checkpoints/round2_warmstart'/file;m=PolicyValue();m.load_state_dict(torch.load(p,map_location='cpu',weights_only=False)['model']);m.eval();models[name]=m
 report[name]={'checkpoint_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'groups':{}}
for split,seeds in [('train_replay',range(1400000,1400030)),('heldout_validation',range(1800000,1800100))]:
 for seed in seeds:
  examples=[]
  def teacher(o,legal):
   def quality(t):
    h=list(o['observer_hand']);h.remove(t)
    return sum(h.count(x)>=2 for x in set(h))*3+sum(abs(x-y) in (1,2) and x//9==y//9 for i,x in enumerate(h) for y in h[i+1:])
   chosen=max(legal,key=quality);missing=o['declared_missing_suits'][o['observer_player']];forced=any(t//9==missing for t in o['observer_hand']);stage=min(2,int((56-o['remaining_wall_information'])*3/56));examples.append((features(o),tuple(legal),chosen,forced,stage,o['observer_player']));return chosen
  result=play(seed,policy=teacher,policy_seat=None)
  if not examples:continue
  x=torch.tensor([e[0] for e in examples],dtype=torch.float32)
  for name,m in models.items():
   with torch.inference_mode():logits,value=m(x)
   for i,e in enumerate(examples):
    _,legal,target,forced,stage,seat=e;pred=max(legal,key=lambda t:float(logits[i,t]));error=float(value[i])-result['scores'][seat]/48
    for key in (split,split+('/missing_forced' if forced else '/free_discard'),split+'/stage'+str(stage),split+('/missing_forced' if forced else '/free_discard')+'/stage'+str(stage)):
     g=report[name]['groups'].setdefault(key,dict(n=0,correct=0,value_sse=0,value_abs=0));g['n']+=1;g['correct']+=int(pred==target);g['value_sse']+=error**2;g['value_abs']+=abs(error)
for model in report.values():
 for g in model['groups'].values():g['agreement']=g['correct']/g['n'];g['value_mse']=g.pop('value_sse')/g['n'];g['value_mae']=g.pop('value_abs')/g['n']
report['metadata']={'train_seeds':[1400000,1400029],'heldout_validation_seeds':[1800000,1800099],'teacher_state_distribution':True,'value_target':'per-seat terminal net score / 48','no_training_or_tuning':True,'final_test_seeds_used':False}
(root/'reports/round2_d_teacher_diagnostics.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v['groups'] for k,v in report.items() if k!='metadata'}))

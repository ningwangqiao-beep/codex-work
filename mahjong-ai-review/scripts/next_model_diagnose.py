"""CPU2 frozen T2 diagnosis; no training, no final-test reads."""
import sys,pathlib,json,torch,hashlib
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.v3_action_value import V3ActionValueNet
from training.v3_supervised import batches
from training.v3_losses import v3_losses
m=json.load(open(root/'datasets/v3_teacher100/manifest.json'));s=torch.load(root/'checkpoints/v3_T2_teacher100_seed42/best_epoch_5.pt',map_location='cpu',weights_only=False);torch.set_num_threads(2);model=V3ActionValueNet();model.load_state_dict(s['model']);model.eval();groups={};errors={'free_wrong':0,'higher_structural':0,'higher_missing_debt':0,'lower_effective':0,'lower_fan_proxy':0,'same_structural_different_choice':0,'outside_teacher_prefilter_frontier':0,'higher_fan_proxy':0,'higher_fan_and_lower_effective':0,'seven_pairs_option_worsened':0,'seven_preferred_to_standard_preferred':0,'standard_preferred_to_seven_preferred':0};
with torch.no_grad():
 for inp,t,meta in batches(m['files']['validation'],'cpu',128):
  o=model(*inp);chosen=o['masked_action_value'].argmax(-1);teacher=t['action_targets'].masked_fill(~inp[2],float('-inf')).argmax(-1)
  for i,item in enumerate(meta):
   if not item['free_discard']:continue
   a=int(chosen[i]);b=int(teacher[i]);x=inp[1][i];wrong=t['action_targets'][i,a]<t['action_targets'][i,b];key=str(item['best_postdiscard_structural']);g=groups.setdefault(key,{'n':0,'equivalent':0});g['n']+=1;g['equivalent']+=not bool(wrong)
   if wrong:
    errors['outside_teacher_prefilter_frontier']+=bool(x[a,11]<.5);errors['higher_fan_proxy']+=bool(x[a,8]>x[b,8]);errors['higher_fan_and_lower_effective']+=bool(x[a,8]>x[b,8] and x[a,5]<x[b,5]);errors['seven_pairs_option_worsened']+=bool(x[a,10]>.5 and x[b,10]>.5 and x[a,2]>x[b,2]);errors['seven_preferred_to_standard_preferred']+=bool(x[a,10]>.5 and x[b,10]>.5 and x[b,2]<x[b,1] and x[a,1]<x[a,2]);errors['standard_preferred_to_seven_preferred']+=bool(x[a,10]>.5 and x[b,10]>.5 and x[b,1]<x[b,2] and x[a,2]<x[a,1]);errors['free_wrong']+=1;errors['higher_structural']+=bool(x[a,3]>x[b,3]);errors['higher_missing_debt']+=bool(x[a,4]>x[b,4]);errors['lower_effective']+=bool(x[a,5]<x[b,5]);errors['lower_fan_proxy']+=bool(x[a,8]<x[b,8]);errors['same_structural_different_choice']+=bool(x[a,3]==x[b,3])
# Shared-encoder gradient interaction is a diagnostic, not a causal loss ablation.
inp,t,_=next(batches(m['files']['train'],'cpu',128));o=model(*inp);ls=v3_losses(o,t,inp[2]);params=list(model.heads.state_encoder.parameters());vectors={}
for k,v in ls.items():
 g=torch.autograd.grad(v,params,retain_graph=True,allow_unused=True);vectors[k]=torch.cat([torch.zeros_like(p).flatten() if a is None else a.flatten() for a,p in zip(g,params)])
a=vectors['action_value_mse'];grads={k:{'unweighted_shared_norm':float(v.norm()),'cosine_to_action_mse':float(torch.dot(a,v)/(a.norm()*v.norm()).clamp_min(1e-12)),'weight':s['config']['loss_weights'][k]} for k,v in vectors.items()}
eval=json.load(open(root/'reports/v3_c_T2_development20.json'));parts={k:eval['summary']['T2']['parts_mean'].get(k,0)-eval['summary']['strong']['parts_mean'].get(k,0) for k in set(eval['summary']['T2']['parts_mean'])|set(eval['summary']['strong']['parts_mean'])};r={'scope':'frozen_train_validation_and_existing_development240_only','errors':errors,'free_postdiscard_structural_groups':groups,'shared_encoder_gradient_single_batch':grads,'net_component_T2_minus_strong':parts,'sum_component_difference':sum(parts.values()),'target_warning':'ordinal teacher rank is not terminal action Q; V is teacher-policy return','training_performed':False,'final_test_used':False,'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()};(root/'reports/next_c_T2_diagnosis.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

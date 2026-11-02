"""CPU validation probes of learned A. Counterfactual vectors are diagnostics only."""
import sys,pathlib,json,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root));from models.round2 import AblationBrain;from training.streaming import batches;from evaluation.metrics import binary_metrics
torch.set_num_threads(4);s=torch.load(root/'experiments/round2_c/A/best.pt',map_location='cpu',weights_only=False);model=AblationBrain('A',hidden=s['model_config']['hidden'],loss_bins=s['model_config']['loss_bins']);model.load_state_dict(s['model']);model.eval();m=json.load(open(root/'datasets/simulation_v2/manifest.json'));ps=[];qs=[];ys=[]
with torch.no_grad():
 for b in batches(m['shards']['validation'],128,'cpu'):
  x=b['features'];mask=b['target_active'].bool();p=model(x)['tenpai_logits'].sigmoid();flat=x.clone();flat[:,27:54]=x[:,27:54].mean(-1,keepdim=True);q=model(flat)['tenpai_logits'].sigmoid();ps.append(p[mask]);qs.append(q[mask]);ys.append(b['tenpai'][mask])
p=torch.cat(ps);q=torch.cat(qs);y=torch.cat(ys);r={'scope':'validation_only_CPU_frozen_model_A','diagnostic_not_legal_state':'replace27 public counts by uniform same total','original_auc':binary_metrics(p,y)['roc_auc'],'uniform_same_total_auc':binary_metrics(q,y)['roc_auc'],'prediction_correlation':float(torch.corrcoef(torch.stack((p,q)))[0,1]),'mean_abs_probability_change':float((p-q).abs().mean())};(root/'reports/round2_c_count_representation.json').write_text(json.dumps(r,indent=2));print(r)

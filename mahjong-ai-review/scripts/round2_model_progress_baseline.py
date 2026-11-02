"""CPU2 train-fit progress baseline, validation paired game comparisons only."""
import argparse,pathlib,sys,json,time,random,torch,hashlib
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from evaluation.metrics import binary_metrics
from evaluation.round2_io import load_checkpoint
from models.round2 import AblationBrain
from training.streaming import batches

def key(r):
 v=r['features'];total=round(sum(v[27:54])*4);phase=min(2,max(0,int((56-v[74]*108)*3/56+1e-6)))
 return min(27,total//4),phase

def ci(games):
 values=list(games.values());rng=random.Random(42);delta=[]
 for _ in range(600):
  sample=rng.choices(values,k=len(values));delta.append(sum(x[0] for x in sample)/sum(x[1] for x in sample))
 delta.sort();return [delta[15],delta[584]]

def run(manifest,models):
 m=json.load(open(manifest));positive=torch.zeros(28,3,3);total=torch.zeros_like(positive);gp=torch.zeros(3);gn=torch.zeros(3)
 for path in m['shards']['train']:
  with open(path,encoding='utf-8') as f:
   for line in f:
    r=json.loads(line);bin,phase=key(r);y=torch.tensor(r['tenpai']).float();active=torch.tensor(r['target_active']).float();positive[bin,phase]+=y*active;total[bin,phase]+=active;gp+=y*active;gn+=active
 prior=(gp+1)/(gn+2);progress=(positive+50*prior)/(total+50)
 data={name:[] for name in ['frequency','progress']+list(models)};ys=[];gids=[];binids=[]
 loaded={}
 for name,path in models.items():
  if name in ('C','D'):
   s=torch.load(path,map_location='cpu',weights_only=False);model=AblationBrain(name,hidden=s['model_config']['hidden'],loss_bins=s['model_config']['loss_bins']);model.load_state_dict(s['model'])
  else:model,s=load_checkpoint(path,'cpu')
  loaded[name]=model.eval()
 with torch.no_grad():
  for path in m['shards']['validation']:
   rows=[]
   with open(path,encoding='utf-8') as f:
    for line in f:
     rows.append(json.loads(line))
     if len(rows)==128:consume(rows,loaded,data,ys,gids,binids,prior,progress);rows=[]
   if rows:consume(rows,loaded,data,ys,gids,binids,prior,progress)
 y=torch.cat(ys);p={k:torch.cat(v) for k,v in data.items()};metrics={name:binary_metrics(v,y) for name,v in p.items()};pairs={}
 for left,right in [(name,'progress') for name in models]+([('D','C')] if 'D' in models else []):
  diff=(p[left]-y).square()-(p[right]-y).square();games={}
  for g,d in zip(gids,diff.tolist()):a=games.setdefault(g,[0.,0]);a[0]+=d;a[1]+=1
  pairs[left+' minus '+right]={'brier_delta':float(diff.mean()),'game_bootstrap_95ci':ci(games),'games':len(games)}
 narrow={}
 bins=torch.tensor(binids)
 for b in sorted(set(binids)):
  select=bins==b;narrow[str(b*4)+'..'+str(b*4+3)]={'n':int(select.sum()),'positive':int(y[select].sum()),'metrics':{name:binary_metrics(v[select],y[select]) for name,v in p.items()}}
  if 'C' in p and 'D' in p:
   delta=(p['D']-y).square()-(p['C']-y).square();games={}
   for idx in select.nonzero().flatten().tolist():
    g=games.setdefault(gids[idx],[0.,0]);g[0]+=float(delta[idx]);g[1]+=1
   narrow[str(b*4)+'..'+str(b*4+3)]['D_minus_C_brier_ci']=ci(games)
 calibrated_comparison=None
 if 'structured' in p:
  cal=json.load(open(root/'reports/round2_c_new_calibration.json'))['tasks']['tenpai'];param=cal['parameters'];q=(torch.logit(p['structured'].clamp(1e-7,1-1e-7))*param['slope']+param['intercept']).sigmoid() if cal['accepted'] else p['structured'];select=torch.tensor([int(hashlib.sha256(str(g).encode()).hexdigest(),16)%2==1 for g in gids]);delta=(q-y).square()-(p['progress']-y).square();games={}
  for idx in select.nonzero().flatten().tolist():
   g=games.setdefault(gids[idx],[0.,0]);g[0]+=float(delta[idx]);g[1]+=1
  calibrated_comparison={'scope':'same165_validation_eval_games_as_calibration_acceptance_not_final','metrics':{name:binary_metrics(v[select],y[select]) for name,v in [('frequency',p['frequency']),('progress',p['progress']),('structured_calibrated',q)]},'brier_delta_calibrated_minus_progress':float(delta[select].mean()),'game_bootstrap_95ci':ci(games)}
 return {'calibrated_eval_half_comparison':calibrated_comparison,'model_scores':'raw_unless_explicitly_calibrated','dataset_version':m['dataset_version'],'fitted_on':'train_only','evaluated_on':'validation_only','bin_width_tiles':4,'phase_source':'current public wall count, no future','prior_strength':50,'metrics':metrics,'paired_comparisons':pairs,'narrow_progress_buckets':narrow}

def consume(rows,models,data,ys,gids,binids,prior,progress):
 x=torch.tensor([r['features'] for r in rows]).float();y=torch.tensor([r['tenpai'] for r in rows]).float();active=torch.tensor([r['target_active'] for r in rows]).bool();preds={name:model(x)['tenpai_logits'].sigmoid() for name,model in models.items()};preds['frequency']=prior.expand_as(y);preds['progress']=torch.stack([progress[key(r)[0],key(r)[1]] for r in rows]);ys.append(y[active])
 for name,v in preds.items():data[name].append(v[active])
 for i,r in enumerate(rows):
  count=int(active[i].sum());gids.extend([r['game_id']]*count);binids.extend([key(r)[0]]*count)

p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();torch.set_num_threads(2);start=time.perf_counter()
r={'scope':'train_validation_only_no_final_test','old_v2':run(root/'datasets/simulation_v2/manifest.json',{'C':root/'experiments/round2_c/C/best.pt','D':root/'experiments/round2_c/D/best.pt'}),'new_round2':run(root/'datasets/round2/manifest.json',{'structured':root/'checkpoints/round2_structured/best.pt'})};r['seconds']=time.perf_counter()-start;pathlib.Path(a.output).write_text(json.dumps(r,indent=2));print(json.dumps({key:{k:v for k,v in r[key].items() if k!='narrow_progress_buckets'} for key in ['old_v2','new_round2']},indent=2))

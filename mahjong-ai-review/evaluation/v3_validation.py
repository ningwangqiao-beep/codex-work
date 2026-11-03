"""Validation-only diagnostic metrics for frozen V3 T2. Not strength promotion."""
import pathlib,json,torch,random,statistics
from models.v3_action_value import V3ActionValueNet
from training.v3_supervised import batches,records
from evaluation.revision_action_value import action_value_metrics

def bootstrap_game(values):
 rng=random.Random(42);groups=list(values.values());results=[]
 for _ in range(1000):
  selected=rng.choices(groups,k=len(groups));results.append(sum(x[0] for x in selected)/sum(x[1] for x in selected))
 results.sort();return [results[25],results[974]]
def validate(checkpoint,manifest):
 m=json.load(open(manifest));s=torch.load(checkpoint,map_location='cpu',weights_only=False);config=s['model_config'];model=V3ActionValueNet(**{k:config[k] for k in ('state_dim','candidate_dim','hidden')});model.load_state_dict(s['model']);model.eval();train_returns=[r['state_target'] for r in records(m['files']['train'])];mean=statistics.mean(train_returns);median=statistics.median(train_returns);pv=[];py=[];pm=[];predv=[];targetv=[];meta=[]
 with torch.inference_mode():
  for inp,t,metadata in batches(m['files']['validation'],'cpu',128):
   o=model(*inp);pv.append(o['action_value']);py.append(t['action_targets']);pm.append(inp[2]);predv.append(o['state_value']);targetv.append(t['state_targets']);meta.extend(metadata)
 p=torch.cat(pv);y=torch.cat(py);mask=torch.cat(pm);v=torch.cat(predv);vy=torch.cat(targetv);regret=y.masked_fill(~mask,float('-inf')).max(-1).values-y.gather(1,p.masked_fill(~mask,float('-inf')).argmax(-1)[:,None]).squeeze(1);result={'scope':'train_fit_constants_validation_only_NOT_final_test','action_target_semantics':m['target_semantics'],'state_target_policy':m['state_target_policy'],'action_metrics':action_value_metrics(p,y,mask),'teacher_preference_regret_not_net_points':True,'value_models':{},'groups':{}}
 for name,b in [('zero',0.),('train_mean',mean),('train_median',median)]:
  error=(v-vy).abs()-abs(vy-b);groups={}
  for i,item in enumerate(meta):g=groups.setdefault(item['game_id'],[0.,0]);g[0]+=float(error[i]);g[1]+=1
  result['value_models'][name]={'baseline_constant_raw':b,'model_mae':float((v-vy).abs().mean()),'baseline_mae':float((vy-b).abs().mean()),'model_minus_baseline_mae':float(error.mean()),'whole_game_bootstrap95ci':bootstrap_game(groups),'games':len(groups)}
 for name in ('free_discard','missing_forced'):
  select=torch.tensor([r['free_discard'] if name=='free_discard' else not r['free_discard'] for r in meta]);groups={}
  for i,item in enumerate(meta):
   if select[i]:g=groups.setdefault(item['game_id'],[0.,0]);g[0]+=float(regret[i]);g[1]+=1
  result['groups'][name]={'metrics':action_value_metrics(p[select],y[select],mask[select]),'regret_game_bootstrap95ci':bootstrap_game(groups),'games':len(groups)}
 result['limitations']=['20validation games, repeated states correlated','V target belongs teacher policy family, not new neural policy','rank regret not action terminal-score regret','history contribution and calibration not established'];return result

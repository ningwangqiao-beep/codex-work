"""CPU-only shortcut diagnostics. Train/validation only; never opens test."""
import argparse,json,pathlib,sys,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root));from evaluation.metrics import binary_metrics
p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--output',required=True);a=p.parse_args();m=json.load(open(a.manifest));rows=[]
for path in m['shards']['validation']:
 with open(path,encoding='utf-8') as f:
  for line in f:
   r=json.loads(line);v=r['features'];rows.append((sum(v[27:54])/27,v[74],v[75],r['game_phase'],r['tenpai'],r['target_active']))
x=torch.tensor([r[:4] for r in rows],dtype=torch.float64);y=torch.tensor([r[4] for r in rows]);active=torch.tensor([r[5] for r in rows]).bool();score=x[:,0].float().unsqueeze(-1).expand_as(y)[active];target=y[active];corr=torch.corrcoef(x[:,:3].T)
report={'scope':'validation_only_cpu_diagnostic','dataset_version':m['dataset_version'],'states':len(rows),'scores':'normalized public tile count (not trained prediction)','correlations_columns':['public_count','wall_feature','history_turn_feature'],'correlations':corr.tolist(),'count_score_auc':binary_metrics(score.clamp(0,1),target.float())['roc_auc'],'phase':{}}
for phase in sorted(set(r[3] for r in rows)):
 select=x[:,3]==phase;mask=active&select[:,None];sy=y[mask].float();sc=x[:,0].float().unsqueeze(-1).expand_as(y)[mask];report['phase'][str(phase)]={'states':int(select.sum()),'active_targets':int(mask.sum()),'tenpai_rate':float(sy.mean()),'public_count_score_auc':binary_metrics(sc.clamp(0,1),sy)['roc_auc'],'mean_public_tile_count':float(x[select,0].mean()*108)}
pathlib.Path(a.output).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

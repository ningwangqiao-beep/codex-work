"""One final-test pass after validation calibration; no test tuning."""
import json,torch
from training.streaming import batches
from evaluation.metrics import binary_metrics

def evaluate(model,paths,baseline,temperature=1.,device='cuda'):
    store={k:[] for k in ('tp','ty','bp','wp','wy','wb','rp','ry','rb','el','yl')}
    games={};groups={}; per_tile=[{'p':[],'y':[]} for _ in range(27)]
    model.eval()
    with torch.no_grad():
      for b in batches(paths,128,device):
        p=model.predict(b['features'],temperature);active=b['target_active'].bool();cand=b['candidate_mask'].bool();wm=(b['tenpai']*b['target_active']).bool().unsqueeze(-1).expand_as(b['waits'])
        for k,v in [('tp',p['tenpai_probability'][active]),('ty',b['tenpai'][active]),('bp',torch.tensor(baseline['tenpai'],device=device).expand_as(b['tenpai'])[active]),('wp',p['wait_given_tenpai'][wm]),('wy',b['waits'][wm]),('wb',torch.tensor(baseline['conditional_wait'],device=device).expand_as(b['waits'])[wm]),('rp',p['deal_in_probability'][cand]),('ry',(b['joint_outcome']>0).float()[cand]),('rb',(1-torch.tensor(baseline['joint'],device=device)[:,0]).expand_as(cand)[cand]),('el',p['expected_loss'][cand]),('yl',b['loss'].float()[cand])]:store[k].append(v.cpu())
        for i,meta in enumerate(b['metadata']):
            mask=active[i];pred=p['tenpai_probability'][i][mask].cpu();target=b['tenpai'][i][mask].cpu();base=torch.tensor(baseline['tenpai'])[mask.cpu()]
            game=games.setdefault(str(meta['game_id']),[0.,0]);game[0]+=float(((pred-target)**2-(base-target)**2).sum());game[1]+=len(target)
            for key in ('game_phase','style'):
                g=groups.setdefault(key+':'+str(meta[key]),{'p':[],'y':[]});g['p'].extend(pred.tolist());g['y'].extend(target.tolist())
            for tile in range(27):
                tm=wm[i,:,tile];per_tile[tile]['p'].extend(p['wait_given_tenpai'][i,:,tile][tm].cpu().tolist());per_tile[tile]['y'].extend(b['waits'][i,:,tile][tm].cpu().tolist())
    d={k:torch.cat(v) for k,v in store.items()};r={}
    for label,pk,yk,bk in [('tenpai','tp','ty','bp'),('conditional_wait','wp','wy','wb'),('deal_in','rp','ry','rb')]:
        r[label]={'model':binary_metrics(d[pk],d[yk]),'baseline':binary_metrics(d[bk],d[yk])}
    r['expected_loss_mae']=float((d['el']-d['yl']).abs().mean());r['scope']='configured_simulator_only'
    r['groups_tenpai']={k:binary_metrics(torch.tensor(v['p']),torch.tensor(v['y'])) for k,v in groups.items() if v['p']}
    r['per_tile_conditional_wait']=[binary_metrics(torch.tensor(v['p']),torch.tensor(v['y'])) if v['p'] else None for v in per_tile]
    import random
    rng=random.Random(42);values=list(games.values());deltas=[]
    for _ in range(400):
        sample=rng.choices(values,k=len(values));deltas.append(sum(x[0] for x in sample)/sum(x[1] for x in sample))
    deltas.sort();r['tenpai_brier_delta_game_bootstrap_95ci']=[deltas[10],deltas[389]];r['bootstrap_games']=len(values)
    return r

"""Streaming JSONL trainer; caller must provide an approved audited manifest."""
import json,random,os
from pathlib import Path
import torch
from training.gate import validate_manifest

def batches(paths,batch_size,device):
    rows=[]
    for path in paths:
        with open(path,encoding='utf-8') as f:
            for line in f:
                rows.append(json.loads(line))
                if len(rows)==batch_size:
                    yield pack(rows,device); rows=[]
    if rows: yield pack(rows,device)

def pack(rows,device):
    r={k:torch.tensor([x[k] for x in rows],device=device) for k in ('features','tenpai','waits','joint_outcome','loss')}
    for k in ('features','tenpai','waits'): r[k]=r[k].float()
    if any(not torch.isfinite(v).all() for v in r.values()): raise ValueError('Nonfinite batch')
    if r['tenpai'].shape!=(len(rows),3) or r['waits'].shape!=(len(rows),3,27) or r['joint_outcome'].shape!=(len(rows),27): raise ValueError('Invalid labels shape')
    for k in ('tenpai','waits'):
        if ((r[k]!=0)&(r[k]!=1)).any(): raise ValueError('Nonbinary label')
    if ((r['joint_outcome']<0)|(r['joint_outcome']>7)|(r['joint_outcome']!=r['joint_outcome'].round())).any(): raise ValueError('Invalid joint mask')
    r['candidate_mask']=torch.tensor([x.get('candidate_mask',[1]*27) for x in rows],device=device).float()
    r['target_active']=torch.tensor([x.get('target_active',[1]*3) for x in rows],device=device).float()
    for k,shape in (('candidate_mask',(len(rows),27)),('target_active',(len(rows),3))):
        if r[k].shape!=shape or ((r[k]!=0)&(r[k]!=1)).any(): raise ValueError('Invalid mask')
    r['metadata']=[{k:x.get(k) for k in ('game_id','game_phase','style')} for x in rows]
    return r

def losses(model,b):
    o=model(b['features']); f=torch.nn.functional
    active=b['target_active']; candidate=b['candidate_mask']
    def avg(v,mask): return (v*mask).sum()/mask.sum().clamp_min(1)
    a=avg(f.binary_cross_entropy_with_logits(o['tenpai_logits'],b['tenpai'],reduction='none'),active)
    mask=(b['tenpai']*active).unsqueeze(-1).expand_as(b['waits'])
    w=(f.binary_cross_entropy_with_logits(o['conditional_wait_logits'],b['waits'],reduction='none')*mask).sum()/mask.sum().clamp_min(1)
    j=avg(f.cross_entropy(o['joint_logits'].reshape(-1,8),b['joint_outcome'].long().flatten(),reduction='none').reshape_as(candidate),candidate)
    score_target=(b['loss'].float().unsqueeze(-1)-model.loss_bins).abs().argmin(-1)
    score=avg(f.cross_entropy(o['loss_logits'].reshape(-1,len(model.loss_bins)),score_target.flatten(),reduction='none').reshape_as(candidate),candidate)
    return {'tenpai':a,'conditional_wait':w,'joint_risk':j,'loss_distribution':score}

def train(model,manifest,out,epochs=10,batch_size=128,patience=3,resume=None):
    bound=validate_manifest(manifest);device=next(model.parameters()).device
    opt=torch.optim.Adam(model.parameters(),lr=.001);start=0;best=float('inf');bad=0
    if resume:
        s=torch.load(resume,map_location=device,weights_only=False)
        if s['dataset_fingerprint']!=bound: raise ValueError('Resume dataset mismatch')
        model.load_state_dict(s['model']);opt.load_state_dict(s['optimizer']);start=s['epoch']+1;best=s['best'];bad=s['bad'];torch.set_rng_state(s['rng'].cpu());random.setstate(s['python_rng'])
        if s.get('cuda_rng') and torch.cuda.is_available(): torch.cuda.set_rng_state_all([v.cpu() for v in s['cuda_rng']])
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for epoch in range(start,epochs):
        model.train(); totals={};n=0
        for batch_index,b in enumerate(batches(manifest['shards']['train'],batch_size,device)):
            stop=os.environ.get('MAHJONG_STOP_FILE')
            if stop and Path(stop).exists():
                state={'model':model.state_dict(),'optimizer':opt.state_dict(),'epoch':epoch-1,'best':best,'bad':bad,'rng':torch.get_rng_state(),'python_rng':random.getstate(),'dataset_fingerprint':bound,'dataset_version':manifest['dataset_version'],'model_config':model.config,'cuda_rng':torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],'interrupted_epoch':epoch,'batches_completed':batch_index,'resume_semantics':'restart interrupted epoch with saved optimizer; batches may repeat'}
                torch.save(state,out/'last.pt');raise SystemExit(75)
            opt.zero_grad();ls=losses(model,b);sum(ls.values()).backward();opt.step();n+=1
            for k,v in ls.items(): totals[k]=totals.get(k,0)+float(v.detach())
        model.eval();vsum=0;vn=0
        with torch.no_grad():
            for b in batches(manifest['shards']['validation'],batch_size,device):
                size=len(b['features']);vsum+=float(sum(losses(model,b).values()))*size;vn+=size
        score=vsum/vn;improved=score<best
        if improved: best=score;bad=0
        else: bad+=1
        state={'model':model.state_dict(),'optimizer':opt.state_dict(),'epoch':epoch,'best':best,'bad':bad,'rng':torch.get_rng_state(),'python_rng':random.getstate(),'dataset_fingerprint':bound,'dataset_version':manifest['dataset_version'],'model_config':model.config,'cuda_rng':torch.cuda.get_rng_state_all() if torch.cuda.is_available() else []}
        torch.save(state,out/'last.pt')
        if improved: torch.save(state,out/'best.pt')
        with open(out/'metrics.jsonl','a') as f:f.write(json.dumps({'epoch':epoch,'train_losses':{k:v/n for k,v in totals.items()},'validation_loss':score})+'\n')
        if bad>=patience:break

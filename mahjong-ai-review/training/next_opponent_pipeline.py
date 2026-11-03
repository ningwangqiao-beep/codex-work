"""Public-only ablation tensors and masked structural-label losses. No calibration."""
import hashlib,json,pathlib,torch
import torch.nn.functional as F
from evaluation.next_opponent_control import shuffle_history

def sha(path):return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
def records(paths):
 for path in sorted(paths,key=lambda p:int(pathlib.Path(p).parent.name)):
  with open(path,encoding='utf-8') as stream:
   for line in stream:yield json.loads(line)
def collate(rows,device,family,seed=42):
 n=len(rows);length=max(1,max(len(r['history_tokens']) for r in rows));tokens=torch.zeros(n,length,3,dtype=torch.long,device=device);tokens[:,:,1]=4;mask=torch.zeros(n,length,dtype=torch.bool,device=device)
 for i,r in enumerate(rows):
  count=len(r['history_tokens'])
  if count:tokens[i,:count]=torch.tensor(r['history_tokens'],device=device);mask[i,:count]=True
 keys=[str(r['game_id'])+':'+str(r['observation']['turn_index']) for r in rows]
 if family=='history_shuffled':tokens=shuffle_history(tokens,mask,keys,seed)
 state=torch.tensor([r['state_features'] for r in rows],dtype=torch.float32,device=device)
 t={key:torch.tensor([r[key] for r in rows],device=device) for key in ('structural_tenpai','structural_waits','target_active','legal_mask','joint_winner_mask')}
 return (state,tokens,mask),t
def batches(paths,device,family,size,seed=42):
 pending=[]
 for r in records(paths):
  pending.append(r)
  if len(pending)==size:yield pending,*collate(pending,device,family,seed);pending=[]
 if pending:yield pending,*collate(pending,device,family,seed)
def constrained_joint_logits(o,t):
 active=t['target_active'].bool();allowed=sum(active[:,k].long()*(1<<k) for k in range(3));classes=torch.arange(8,device=active.device);invalid=(classes[None,:]&~allowed[:,None])!=0
 return o['legal_candidate_joint_logits'].masked_fill(invalid[:,None,:],torch.finfo(o['legal_candidate_joint_logits'].dtype).min)
def losses(o,t):
 active=t['target_active'].bool();tenpai=t['structural_tenpai'].float();wait=t['structural_waits'].float();legal=t['legal_mask'].bool();joint=t['joint_winner_mask'].long()
 if not torch.isfinite(tenpai).all() or not torch.isfinite(wait).all() or ((tenpai!=0)&(tenpai!=1)).any() or ((wait!=0)&(wait!=1)).any() or ((joint<0)|(joint>7)).any():raise ValueError('Invalid structural labels')
 zero=o['structural_tenpai_logits'].sum()*0
 ten=F.binary_cross_entropy_with_logits(o['structural_tenpai_logits'][active],tenpai[active]) if active.any() else zero
 wm=(active&tenpai.bool()).unsqueeze(-1).expand_as(wait)
 conditional=F.binary_cross_entropy_with_logits(o['conditional_structural_wait_logits'][wm],wait[wm]) if wm.any() else zero
 risk=F.cross_entropy(constrained_joint_logits(o,t)[legal],joint[legal]) if legal.any() else zero
 return {'structural_tenpai_bce':ten,'conditional_structural_wait_bce':conditional,'legal_joint_ce':risk}

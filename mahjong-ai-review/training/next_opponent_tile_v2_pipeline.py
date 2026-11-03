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
def public_tile_features(rows,device):
 features=[]
 for r in rows:
  o=r['observation'];observer=o['observer_player']
  if list(r['target_active'])!=[int(o['active'][(observer+k+1)%4]) for k in range(3)]:raise ValueError('Relative active target mismatch')
  public=[t for _,t in o['visible_discards']]+[t for ms in o['public_melds'] for meld in ms for t in meld if t>=0]+o.get('public_winning_tiles',[]);sample=[]
  for k in range(3):
   q=(observer+k+1)%4;missing=o['declared_missing_suits'][q];target_meld_tiles=[t for meld in o['public_melds'][q] for t in meld if t>=0];items=[]
   for tile in range(27):
    own=o['observer_hand'].count(tile);shown=public.count(tile)
    if own+shown>4:raise ValueError('Known fifth physical copy')
    items.append([own/4,shown/4,(4-own-shown)/4,float(tile//9==missing)]+[float(missing==s) for s in range(3)]+[float(tile//9==s) for s in range(3)]+[(tile%9)/8,target_meld_tiles.count(tile)/4,len(o['public_melds'][q])/4,float(o['active'][q])])
   sample.append(items)
  features.append(sample)
 return torch.tensor(features,dtype=torch.float32,device=device)
def collate(rows,device,family,seed=42):
 if family!='shared_tile':raise ValueError('Only shared_tile')
 state=torch.tensor([r['state_features'] for r in rows],dtype=torch.float32,device=device);features=public_tile_features(rows,device)
 t={key:torch.tensor([r[key] for r in rows],device=device) for key in ('structural_tenpai','structural_waits','target_active','legal_mask','joint_winner_mask')}
 if (t['structural_waits'].bool()&features[:,:,:,3].bool()).any():raise ValueError('Positive structural wait in declared missing suit')
 return (state,features),t
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

"""Interface smoke for candidate-relative ranking; no training admission bypass."""
import pathlib,sys,json,torch,argparse
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.next_candidate import RelativeCandidateRanker,pairwise_teacher_loss
p=argparse.ArgumentParser();p.add_argument('--smoke',action='store_true');p.add_argument('--output',required=True);a=p.parse_args()
if not a.smoke:raise ValueError('Training not exposed until new-history/data chief admission')
torch.set_num_threads(2);torch.manual_seed(42);model=RelativeCandidateRanker();state=torch.zeros(2,191);c=torch.randn(2,27,12);mask=torch.zeros(2,27,dtype=torch.bool);mask[:,:5]=True;y=torch.zeros(2,27);y[:,0]=1;s=model(state,c,mask);loss=pairwise_teacher_loss(s,y,mask);loss.backward();assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters());r={'scope':'synthetic_interface_only','parameters':sum(p.numel() for p in model.parameters()),'pairwise_loss':float(loss.detach()),'finite_gradients':True,'formal_training':False,'rl':False};pathlib.Path(a.output).write_text(json.dumps(r,indent=2));print(r)

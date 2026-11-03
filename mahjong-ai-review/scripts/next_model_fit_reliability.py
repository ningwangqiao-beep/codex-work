"""Frozen-model paired game bootstrap of teacher-fit, train/validation only."""
import pathlib,sys,json,torch,random,hashlib
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.v3_action_value import V3ActionValueNet
from models.next_relative_v3 import RelativeV3ActionValueNet
from training.next_supervised import batches

def load(path,cls):
 s=torch.load(path,map_location='cpu',weights_only=False);model=cls(**{k:s['model_config'][k] for k in ('state_dim','candidate_dim','hidden')});model.load_state_dict(s['model']);return model.eval()
def boot(values):
 rng=random.Random(42);v=list(values.values());r=[]
 for _ in range(1000):
  a=rng.choices(v,k=len(v));r.append(sum(x[0] for x in a)/sum(x[1] for x in a))
 r.sort();return [r[25],r[974]]
torch.set_num_threads(2);m=json.load(open(root/'datasets/next_history100/manifest.json'));models={'control':load(root/'checkpoints/next_history100_multitask/best_epoch_5.pt',V3ActionValueNet),'relative_combo':load(root/'checkpoints/next_history100_relative_pairwise/best_epoch_5.pt',RelativeV3ActionValueNet)};result={}
with torch.inference_mode():
 for split in ('train','validation'):
  sums={name:{'n':0,'equivalent':0,'rank_regret':0.} for name in models};eqgames={};regretgames={}
  for inp,t,meta in batches(m['files'][split],'cpu',128):
   target=t['action_targets'];best=target.masked_fill(~inp[2],float('-inf')).max(-1).values;values={}
   for name,model in models.items():
    chosen=model(*inp)['masked_action_value'].argmax(-1);regret=best-target.gather(1,chosen[:,None]).squeeze(1);eq=regret==0;values[name]=(regret,eq)
    for i,item in enumerate(meta):
     if item['free_discard']:sums[name]['n']+=1;sums[name]['equivalent']+=int(eq[i]);sums[name]['rank_regret']+=float(regret[i])
   for i,item in enumerate(meta):
    if not item['free_discard']:continue
    a=eqgames.setdefault(item['game_id'],[0.,0]);a[0]+=int(values['relative_combo'][1][i])-int(values['control'][1][i]);a[1]+=1;b=regretgames.setdefault(item['game_id'],[0.,0]);b[0]+=float(values['relative_combo'][0][i]-values['control'][0][i]);b[1]+=1
  result[split]={'free':sums,'relative_minus_control_equivalent_ci':boot(eqgames),'relative_minus_control_regret_ci':boot(regretgames),'game_clusters_with_free_decisions':len(eqgames)}
report={'scope':'teacher_fit_only_NOT_net_return_NO_training_NO_final','results':result,'limitations':['fixed20validation games, not an independent new final','combined representation+pairwise, no single-factor causality','teacher fit cannot prove policy improvement or justify1000alone'],'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()};(root/'reports/next_c_relative_fit_reliability.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

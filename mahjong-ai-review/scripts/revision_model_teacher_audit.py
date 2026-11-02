"""Independent teacher agreement audit. CPU2; no training, no final-test seeds."""
import sys,pathlib,argparse,json,hashlib,time,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from simulator.policy_learning import PolicyValue
from simulator.selfplay import play
from observations.public import features
from models.round2_candidate import CandidateLinear,candidate_features,teacher_utility
from rules.hand_analysis import shanten
p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=1800000);p.add_argument('--games',type=int,default=100);p.add_argument('--output',default=str(root/'reports/revision_c_teacher_audit.json'));a=p.parse_args();torch.set_num_threads(2);start=time.perf_counter();report={'models':{},'metadata':{'seed_range':[a.seed,a.seed+a.games-1],'scope':'previously_defined_independent_validation_teacher_states_only','training_performed':False,'rl_performed':False,'gpu_used':False,'shanten_group':'predecision14-equivalent structural minimum, current hand only; hand_analysis not independent oracle','exact_definition':'same unique teacher argmax using supplied legal order','equivalent_definition':'chosen teacher utility equals max utility','topk_definition':'stable descending predicted score; exact teacher target included','utility_regret_definition':'best integer shape utility minus chosen integer utility','no_full_Claude_S0_S12_source':True}}
files={'old_imitation':root/'checkpoints/round2_warmstart/imitation_last.pt','candidate':root/'experiments/round2_c/candidate/best.pt'}
old=PolicyValue();old.load_state_dict(torch.load(files['old_imitation'],map_location='cpu',weights_only=False)['model']);old.eval();candidate=CandidateLinear();candidate.load_state_dict(torch.load(files['candidate'],map_location='cpu',weights_only=False)['model']);candidate.eval()
for name in ['old_imitation','candidate_raw','candidate_rounded']:report['models'][name]={'groups':{}}
def update(name,group,legal,utility,scores):
 target=max(range(len(legal)),key=lambda i:utility[i]);order=sorted(range(len(legal)),key=lambda i:-scores[i]);selected=order[0];best=max(utility);ties=sum(u==best for u in utility)>1;g=report['models'][name]['groups'].setdefault(group,{'n':0,'exact':0,'equivalent':0,'top3':0,'top5':0,'utility_regret_sum':0,'max_utility_regret':0,'teacher_tie_states':0,'exact_fail_but_equivalent':0,'exact_fail_and_suboptimal':0});g['n']+=1;g['exact']+=selected==target;g['equivalent']+=utility[selected]==best;g['top3']+=target in order[:3];g['top5']+=target in order[:5];regret=best-utility[selected];g['utility_regret_sum']+=regret;g['max_utility_regret']=max(g['max_utility_regret'],regret);g['teacher_tie_states']+=ties;g['exact_fail_but_equivalent']+=selected!=target and regret==0;g['exact_fail_and_suboptimal']+=regret>0
for seed in range(a.seed,a.seed+a.games):
 examples=[]
 def teacher(o,legal):
  u=[teacher_utility(o,t) for t in legal];target=max(range(len(legal)),key=lambda i:u[i]);missing=o['declared_missing_suits'][o['observer_player']];forced=any(t//9==missing for t in o['observer_hand']);distance=shanten(o['observer_hand'],len(o['public_melds'][o['observer_player']]),missing)['minimum'];examples.append((o,tuple(legal),u,forced,distance));return legal[target]
 play(seed,policy=teacher,policy_seat=None)
 with torch.inference_mode():
  logits,_=old(torch.tensor([features(e[0]) for e in examples]).float())
  for i,(o,legal,utility,forced,distance) in enumerate(examples):
   c=candidate(torch.tensor([candidate_features(o,t) for t in legal]).float())*64;preds={'old_imitation':[float(logits[i,t]) for t in legal],'candidate_raw':c.tolist(),'candidate_rounded':c.round().tolist()};category='missing_forced' if forced else 'free_discard'
   for name,scores in preds.items():
    for group in ['all',category,'shanten:'+str(distance),category+'/shanten:'+str(distance)]:update(name,group,legal,utility,scores)
for model in report['models'].values():
 for g in model['groups'].values():
  for k in ['exact','equivalent','top3','top5']:g[k+'_rate']=g[k]/g['n']
  g['mean_teacher_utility_regret']=g['utility_regret_sum']/g['n']
report['metadata']['checkpoint_sha256']={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in files.items()};report['metadata']['source_sha256']={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [pathlib.Path(__file__),root/'rules/hand_analysis.py',root/'models/round2_candidate.py',root/'simulator/selfplay.py']};report['seconds']=time.perf_counter()-start;report['status']='completed';pathlib.Path(a.output).write_text(json.dumps(report,indent=2));print(json.dumps({name:model['groups']['free_discard'] for name,model in report['models'].items()},indent=2));print('seconds',report['seconds'])

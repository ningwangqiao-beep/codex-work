"""Zero residual vs deployed teacher: legal actions on all heldout stored states."""
import pathlib,sys,json,torch
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from models.round2_candidate import CandidateLinear
from models.round2_candidate_residual import CandidateResidual
s=torch.load(root/'experiments/round2_c/candidate/best.pt',map_location='cpu',weights_only=False);base=CandidateLinear();base.load_state_dict(s['model']);res=CandidateResidual(base);torch.set_num_threads(2);counts={'all':0,'free':0,'mismatch_deployed':0,'mismatch_teacher':0}
with torch.no_grad():
 for path in (root/'experiments/round2_c/candidate/validation').glob('*.jsonl'):
  for line in path.read_text().splitlines():
   r=json.loads(line);x=torch.tensor(r['x']).float();logits,_=res(x);deployed=int((base(x)*64).round().argmax());target=max(range(len(r['legal'])),key=lambda i:r['utility'][i]);action=int(logits.argmax());counts['all']+=1;counts['free']+=not r['forced'];counts['mismatch_deployed']+=action!=deployed;counts['mismatch_teacher']+=action!=target
assert counts['mismatch_deployed']==counts['mismatch_teacher']==0
(root/'reports/round2_c_candidate_zero_residual.json').write_text(json.dumps(counts,indent=2));print(counts)

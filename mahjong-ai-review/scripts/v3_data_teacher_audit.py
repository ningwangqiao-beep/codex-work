import sys,json,hashlib,copy
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from inference.v3_observation import encode_observation
m=json.loads((root/'datasets/v3_teacher100/manifest.json').read_text());seen={};n=0
for split,p in m['files'].items():
 assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==m['data_hashes'][split]
 for line in Path(p).open():
  r=json.loads(line);key=r['deal_group_id'];assert key not in seen or seen[key]==split;seen[key]=split
  o=r['observation'];a=encode_observation(o);poison=copy.deepcopy(o);poison.update(opponent_hands=[[26]*13]*3,future_wall=list(range(27)),future_result=999)
  assert a==encode_observation(poison);assert a['state_features']==r['state_features'];assert a['history_tokens']==r['history_tokens'];assert not a['history_truncated']
  assert len(r['candidate_features'])==27 and all(len(x)==12 for x in r['candidate_features']);assert any(r['legal_mask']);assert all(r['structural_tenpai'][i]==int(any(r['structural_waits'][i])) for i in range(3));n+=1
report=dict(passed=True,records=n,unique_games=len(seen),actual_files_sha256=m['data_hashes'],checks=['whole-deal split','encoder reproduces recorded static/fullseq','hidden/future injected keys ignored','candidate shape and mask','structural tenpai waits consistency'],limitations=['poison-key noninterference not proof of all possible upstream leakage','preference rank not counterfactual Q','raw terminal state V under one-Bot-vs-three-heuristic policy'],admission='chief required')
(root/'reports/v3_d_teacher100_isolation.json').write_text(json.dumps(report,indent=2));print(report)

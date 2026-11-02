"""Read-only project inventory and reproducible historical win-only crosscheck."""
import hashlib,json,pathlib,random,sys,time
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from rules.core import winning
from rules.hand_analysis import shanten
def info(p):return {'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
inventory={}
for name in ('models','rules','simulator','observations','baselines','training','evaluation','inference','tests','checkpoints'):
    inventory[name]=[info(p) for p in (root/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
inventory['datasets']={str(p.parent.relative_to(root)):json.loads(p.read_text()) for p in (root/'datasets').glob('*/manifest.json')}
(root/'reports/revision_chief_inventory.json').write_text(json.dumps(inventory,indent=2))
rng=random.Random(233);deck=list(range(18))*4;start=time.perf_counter();bad=[];positive=0
for i in range(300):
    h=rng.sample(deck,14);expected=winning(h,2);positive+=expected
    if (shanten(h,missing_suit=2)['minimum']==-1)!=expected:bad.append(h)
report={'checks':300,'seed':233,'sampling':'14 physical tiles from two suits, four copies each','winning_positive':positive,'mismatches':bad,'seconds':time.perf_counter()-start,'independence_limit':'win-only Boolean check against core; not proof of shanten levels, 13-tile states, open melds, or missing-suit debt','historical_replay':'reconstruction of earlier inline command, source now persisted; current shanten version may differ'}
(root/'reports/revision_chief_300_win_check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));assert not bad

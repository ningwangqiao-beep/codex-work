"""Reproducible independent next-history100 source, V-label and seed audit."""
import hashlib,json,pathlib,sys
r=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(r))
from training.v3_gate import inspect_v3_data
from rules.core import legal_discards
manifest=r/'datasets/next_history100/manifest.json';inspection,m=inspect_v3_data(manifest,r)
games={g['seed']:g for g in map(json.loads,(manifest.parent/'game_returns.jsonl').open())}
for g in games.values():
    b=[0]*4
    for e in g['ledger']:b[e['payer']]-=e['amount'];b[e['receiver']]+=e['amount']
    assert b==g['scores'] and sum(b)==0
seen={};n=0
for split,p in m['files'].items():
    for row in map(json.loads,open(p)):
        seed=row['seed'];o=row['observation'];seat=o['observer_player']
        assert row['state_target']==games[seed]['scores'][seat]
        assert not 5000000<=seed<=5004999 and (seed not in seen or seen[seed]==split)
        assert (7000000<=seed<=7004999) if split=='train' else (7100000<=seed<=7100999)
        assert [i for i,v in enumerate(row['legal_mask']) if v]==legal_discards(o['observer_hand'],o['declared_missing_suits'][seat])
        seen[seed]=split;n+=1
report={'passed':True,'records':n,'unique_games':len(seen),'returns_reconciled':len(games),'inspection':inspection,'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'old_final_excluded':True,'targets':'teacher preference and terminal teacher-policy V; not Q'}
(r/'reports/next_chief_data100_recheck.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

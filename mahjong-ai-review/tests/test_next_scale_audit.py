import unittest,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ScaleAudit(unittest.TestCase):
 def test_completed_smoke_physical_and_targets(self):
  base=ROOT/'datasets/next_history_scale_smoke_v2';manifest=json.loads((base/'manifest.json').read_text());seen=set();counts=0
  for commit in manifest['commits']:
   seed=commit['seed'];split=commit['split'];self.assertNotIn(seed,seen);seen.add(seed)
   self.assertTrue(7000000<=seed<7001000 if split=='train' else 7100000<=seed<7100020)
   d=base/split/str(seed);g=json.loads((d/'game.json').read_text());self.assertEqual(g['seed'],seed);self.assertEqual(sum(g['scores']),0)
   rebuilt=[0]*4
   for e in g['ledger']:rebuilt[e['payer']]-=e['amount'];rebuilt[e['receiver']]+=e['amount']
   self.assertEqual(rebuilt,g['scores'])
   raw=(d/'records.jsonl').read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),commit['records_sha256'])
   for line in raw.splitlines():
    r=json.loads(line);self.assertEqual(r['seed'],seed);self.assertEqual(r['observation']['observer_player'],commit['seat']);self.assertEqual(r['state_target'],g['scores'][commit['seat']]);self.assertFalse(r['state_target_missing']);counts+=1
  self.assertGreater(counts,0)
 def test_full_prefix_has_120_groups(self):
  groups=[]
  for split in ('train','validation'):
   with (ROOT/'datasets/next_history100'/(split+'.jsonl')).open(encoding='utf-8') as f:groups.append({json.loads(line)['seed'] for line in f})
  self.assertFalse(groups[0]&groups[1]);self.assertEqual([len(g) for g in groups],[100,20])


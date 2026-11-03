import unittest
from copy import deepcopy
from simulator.table import Table
from observations.v3_public import observe
from simulator.v3_selfplay import play
class V3Data(unittest.TestCase):
 def test_exchange_snapshot_and_hidden(self):
  t=Table([[0],[1],[2],[3]],[2]*4,[4,5]);t.exchange_records=[dict(sent=[p],received=[(p+3)%4],direction=1,source_player=(p+3)%4) for p in range(4)]
  a=observe(t,0);t.exchange_records[1]['sent']=[20];t.wall.reverse();t.hands[1],t.hands[2]=t.hands[2],t.hands[1]
  self.assertEqual(a,observe(t,0));t.exchange_records[0]['sent'].append(9);self.assertEqual(a['exchange']['sent'],[0])
 def test_three_directions_ledger(self):
  for direction in (1,2,3):
   r=play(3100000+direction,exchange_offset=direction);self.assertEqual(sum(r['scores']),0);self.assertTrue(r['ledger'])

"""Independent adversarial boundaries, intentionally using legal small fixtures."""
import unittest
from copy import deepcopy
from simulator.table import Table
class Boundaries(unittest.TestCase):
 def test_empty_wall_kong_transaction(self):
  t=Table([[0],[0,0,0],[],[]],[2]*4);t.discard(0,0);before=deepcopy(t.__dict__)
  with self.assertRaises(ValueError):t.claim(1,'exposed_kong')
  self.assertEqual(before,t.__dict__)
 def test_bad_win_transaction(self):
  t=Table([[0],[1],[],[]],[2]*4);t.discard(0,0);before=deepcopy(t.__dict__)
  with self.assertRaises(ValueError):t.discard_win([1])
  self.assertEqual(before,t.__dict__)
 def test_bad_kong_transaction(self):
  t=Table([[0],[],[],[]],[2]*4,[8]);before=deepcopy(t.__dict__)
  with self.assertRaises(ValueError):t.concealed_kong(0,0)
  self.assertEqual(before,t.__dict__)
 def test_multihit_next_seat(self):
  a=[0,1,2,3,4,5,6,7,8,10,10,10,11]
  b=[9,9,9,12,13,14,15,16,17,18,19,20,11]
  t=Table([[11],a,b,[]],[2,2,0,0],[26]);t.discard(0,11);t.discard_win([1,2]);t.advance();self.assertEqual(t.turn,3)
 def test_win_priority_atomic(self):
  a=[9,9,9,12,13,14,18,19,20,21,21,10,12]
  t=Table([[11],[11,11],a,[]],[2,2,0,0]);t.discard(0,11);before=deepcopy(t.__dict__)
  with self.assertRaises(ValueError):t.claim(1,'peng')
  self.assertEqual(t.__dict__,before)
 def test_dragon_pairs_config(self):
  from rules.core import score,AssumptionConfig
  h=[0,0,0,0,1,1,3,3,5,5,9,9,12,12]
  self.assertEqual(score(h,2)['fan'],2)
  self.assertEqual(score(h,2,config=AssumptionConfig(dragon_pair_quad_fan=1))['fan'],3)
 def test_concealed_metadata(self):
  t=Table([[0]*4,[],[],[]],[2]*4,[8]);t.concealed_kong(0,0);self.assertIn((0,0),t.concealed_kongs)
 def test_bad_config(self):
  from rules.core import AssumptionConfig
  for params in ({'concealed_kong_fee':-1},{'base_fan':-2},{'pure_suit_fan':1.5}):
   with self.assertRaises(ValueError):AssumptionConfig(**params)
 def test_rob_no_gang_fee(self):
  from rules.core import AssumptionConfig
  a=[9,9,9,12,13,14,18,19,20,21,21,10,12]
  t=Table([[],[11,8],a,[]],[2,2,0,0],[7],config=AssumptionConfig(gang_payments_enabled=True));t.melds[1]=[[11]*3];t.inventory=t.counts();t.turn=1;t.added_kong(1,11);t.resolve_added_kong([2]);self.assertEqual(t.gang_ledger,[]);self.assertEqual(sum(t.scores),0)

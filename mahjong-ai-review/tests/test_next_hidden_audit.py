import unittest
from collections import Counter
from search.next_hidden import sample_hidden,UnsupportedObservation
class HiddenAudit(unittest.TestCase):
 def fixture(self):return dict(observer_player=0,observer_hand=list(range(13)),public_melds=[[],[],[],[]],visible_discards=[],public_winning_tiles=[],active=[True]*4,declared_missing_suits=[2]*4,concealed_hand_sizes=[13]*4,remaining_wall_information=56)
 def test_every_physical_tile(self):
  o=self.fixture()
  for s in sample_hidden(o,25,101):self.assertEqual(Counter(sum(s['concealed_hands'],[])+s['wall']),Counter({t:4 for t in range(27)}))
 def test_missing_sizes_and_bad_sum(self):
  for field in ('concealed_hand_sizes','remaining_wall_information'):
   o=self.fixture();del o[field]
   with self.assertRaises(UnsupportedObservation):sample_hidden(o)
  o=self.fixture();o['remaining_wall_information']=55
  with self.assertRaises(UnsupportedObservation):sample_hidden(o)
 def test_visible_fifth_rejected(self):
  o=self.fixture();o['observer_hand']=[0]*5+list(range(1,9))
  with self.assertRaises(ValueError):sample_hidden(o)
 def test_inactive_flag_is_not_win_constraint(self):
  # Documents current boundary: archive metadata flag alone accepts arbitrary hands.
  from rules.core import winning
  o=self.fixture();o['active'][1]=False;o['inactive_archives_complete']=True
  samples=sample_hidden(o,20,9)
  self.assertTrue(any(not winning(s['concealed_hands'][1]+[26],2) for s in samples))
 def test_sizes_not_phase_validated(self):
  o=self.fixture();o['concealed_hand_sizes'][1]=12;o['remaining_wall_information']=57
  self.assertEqual(len(sample_hidden(o,1)[0]['concealed_hands'][1]),12)
 def test_draw_metadata_not_inferred(self):
  o=self.fixture();del o['concealed_hand_sizes'];o['phase']='discard';o['current_player']=0
  with self.assertRaises(UnsupportedObservation):sample_hidden(o)

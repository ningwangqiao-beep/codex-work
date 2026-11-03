import unittest
from search.next_hidden import sample_hidden,UnsupportedObservation
class HiddenSampling(unittest.TestCase):
 def fixture(self):return dict(observer_player=0,observer_hand=list(range(13)),public_melds=[[],[],[],[]],visible_discards=[],public_winning_tiles=[],active=[True]*4,declared_missing_suits=[2]*4,concealed_hand_sizes=[13]*4,remaining_wall_information=56)
 def test_hundred(self):
  r=sample_hidden(self.fixture(),100);self.assertEqual(len(r),100);self.assertEqual(r,sample_hidden(self.fixture(),100));self.assertTrue(any(18 in x['concealed_hands'][1] for x in r))
 def test_poison_no_effect(self):
  o=self.fixture();a=sample_hidden(o);o.update(real_wall=[0]*56,opponent_hands=[[26]*13]*3,exchange={'sent':[0,1,2]});self.assertEqual(a,sample_hidden(o))
 def test_missing_sizes_rejected(self):
  o=self.fixture();del o['concealed_hand_sizes']
  with self.assertRaises(UnsupportedObservation):sample_hidden(o)
 def test_inactive_archive(self):
  o=self.fixture();o['active'][1]=False
  with self.assertRaises(UnsupportedObservation):sample_hidden(o)
  o['inactive_archives_complete']=True;self.assertEqual(len(sample_hidden(o)[0]['concealed_hands'][1]),13)
 def test_unknown_kong(self):
  o=self.fixture();o['public_melds'][1]=[[-1]*4];o['concealed_hand_sizes'][1]=10;o['remaining_wall_information']=55
  for r in sample_hidden(o,100):self.assertEqual(len(set(r['unknown_kongs'][0]['tiles'])),1)

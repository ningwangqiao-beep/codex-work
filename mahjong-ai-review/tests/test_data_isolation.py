import unittest
from copy import deepcopy
from simulator.table import Table
from observations.public import observe,features
class DataIsolation(unittest.TestCase):
 def test_counterfactual_hidden(self):
  t=Table([[0],[1],[2],[3]],[2]*4,[4,5]);a=observe(t,0)
  t.hands[1],t.hands[2]=t.hands[2],t.hands[1];t.wall.reverse()
  self.assertEqual(a,observe(t,0));self.assertEqual(len(features(a)),128)
 def test_snapshot(self):
  t=Table([[0],[1],[2],[3]],[2]*4,[4,5]);a=observe(t,0);t.hands[0].append(6)
  self.assertEqual(a['observer_hand'],[0])

class ConcealedKongIsolation(unittest.TestCase):
 def test_masked(self):
  t=Table([[0],[1],[2],[3]],[2]*4,[4,5]);t.melds[1]=[[9]*4];t.concealed_kongs={(1,0)}
  a=observe(t,0);self.assertEqual(a['public_melds'][1],[[-1]*4]);t.melds[1]=[[10]*4]
  self.assertEqual(a,observe(t,0));self.assertEqual(observe(t,1)['public_melds'][1],[[10]*4])

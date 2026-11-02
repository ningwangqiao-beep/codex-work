import unittest
from rules.hand_analysis import shanten,effective_draws
class Analysis(unittest.TestCase):
 def test_ready_complete(self):
  h=[0,1,2,3,4,5,6,7,8,9,9,9,10];self.assertEqual(shanten(h,missing_suit=2)['minimum'],0);self.assertEqual(shanten(h+[10],missing_suit=2)['minimum'],-1);self.assertIn(10,[x['tile'] for x in effective_draws(h,missing_suit=2)])
 def test_seven(self):self.assertEqual(shanten([0,0,1,1,3,3,5,5,7,7,9,9,12])['seven_pairs'],0)
 def test_open(self):self.assertEqual(shanten([0,1,2,3,4,5,9,9,9,10],1)['minimum'],0)
 def test_dead(self):
  h=[0,1,2,3,4,5,6,7,8,9,9,9,10];self.assertNotIn(10,[x['tile'] for x in effective_draws(h,public_tiles=[10]*3)])
 def test_fifth(self):
  with self.assertRaises(ValueError):shanten([0]*5+[1]*4+[2]*4)
 def test_missing(self):self.assertGreaterEqual(shanten([0,1,2,3,4,5,6,7,8,9,9,9,10,10],missing_suit=0)['minimum'],0)
 def test_quad_pairs_match_core(self):
  self.assertEqual(shanten([0]*4+[1]*2+[3]*2+[5]*2+[9]*2+[12]*2)['seven_pairs'],-1)

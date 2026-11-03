import unittest
from baselines.v3_memo import shanten,effective_draws
from rules.hand_analysis import shanten as reference,effective_draws as ref_effective
class V3Memo(unittest.TestCase):
 def test_fifth_copy_fix_preserved(self):
  h=[0]*4;self.assertEqual(shanten(h,3,2)['standard'],reference(h,3,2)['standard']);self.assertEqual(shanten(h,3,2)['standard'],1)
 def test_canonical_and_result_copy(self):
  h=[0,1,2,3,4,5,6,7,8,9,9,9,10];self.assertEqual(shanten(h,0,2),shanten(list(reversed(h)),0,2));a=shanten(h,0,2);a['standard']=999;self.assertNotEqual(shanten(h,0,2)['standard'],999)
 def test_effective_exact(self):
  h=[0,1,2,3,4,5,6,7,8,9,9,9,10];self.assertEqual(effective_draws(h,0,2),ref_effective(h,0,2))

import unittest,random
from rules.hand_analysis import shanten,effective_draws
from rules.hand_analysis_reference import target_distance
class ReferenceTests(unittest.TestCase):
 def test_open_target_oracle(self):
  rng=random.Random(903)
  for opened in (2,3,4):
   for extra in (0,1):
    for missing in (None,0,1,2):
     for _ in range(3):
      wall=list(range(27))*4;rng.shuffle(wall);h=wall[:13-3*opened+extra]
      # No missing debt for equality: oracle is exact draw-replacement distance.
      if missing is not None:h=[t if t//9!=missing else (t+9)%27 for t in h]
      if max(__import__('collections').Counter(h).values())>4:continue
      self.assertEqual(shanten(h,opened,missing)['standard'],target_distance(h,opened,missing),(h,opened,missing))
 def test_high_distance_missing_debt_is_not_exact(self):
  h=[0,1,2,3,4,5,6]
  structural=shanten(h,2,0)['standard'];exact=target_distance(h,2,0)
  self.assertEqual(structural,4);self.assertEqual(exact,7)
 def test_effective_inputs_unchanged(self):
  h=[0,1,2,3,4,5,6,7,8,9,9,9,10];p=[10,10];saved=(h[:],p[:]);out=effective_draws(h,0,2,p);self.assertEqual((h,p),saved)
  for x in out:self.assertGreater(x['remaining'],0);self.assertEqual(x['remaining'],4-h.count(x['tile'])-p.count(x['tile']))
 def test_open_zero_one_high_shanten_analytic(self):
  # Isolated ranks at gap3 across suits cannot form taatsu; distinct singles only.
  h=[0,3,6,9,12,15,18,21,24,0,3,9,12]
  self.assertGreaterEqual(shanten(h)['standard'],3)
  self.assertIsNotNone(shanten(h)['seven_pairs'])
  self.assertIsNone(shanten(h[:10],1)['seven_pairs'])

class SuitOracleTests(unittest.TestCase):
 def test_all_open_and_sizes(self):
  from rules.hand_analysis_reference import suit_target_distance
  rng=random.Random(1729);high=0
  for opened in range(5):
   for extra in (0,1):
    for _ in range(8):
     wall=list(range(27))*4;rng.shuffle(wall);h=wall[:13-3*opened+extra]
     exact=suit_target_distance(h,opened)
     self.assertEqual(shanten(h,opened)['standard'],exact,(h,opened));high+=exact>=3
  self.assertGreater(high,0)
 def test_missing_debt_reference(self):
  from rules.hand_analysis_reference import suit_target_distance
  for opened in range(5):
   h=(list(range(9))*2)[:13-3*opened]
   self.assertEqual(suit_target_distance(h,opened,0),13-3*opened)

class LegalProgressTests(unittest.TestCase):
 def test_missing_debt_separate(self):
  from rules.hand_analysis import legal_progress
  h=list(range(7));self.assertEqual(shanten(h,2,0)['standard'],4);r=legal_progress(h,2,0);self.assertEqual(r['legal_standard'],7);self.assertEqual(r['missing_tiles'],7)
 def test_pairs_quad(self):
  from rules.hand_analysis import legal_progress
  h=[0]*4+[1]*2+[3]*2+[5]*2+[9]*2+[12]*2;self.assertEqual(legal_progress(h,0,2)['legal_seven_pairs'],-1)
 def test_completed_missing_clear(self):
  from rules.hand_analysis import legal_progress
  h=[0,1,2,3,4,5,6,7,8,9,9,9,10,10];self.assertEqual(legal_progress(h,0,2)['legal_minimum'],-1)

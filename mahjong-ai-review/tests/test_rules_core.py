import unittest
from rules.core import *
class TestCore(unittest.TestCase):
 def test_deal(self):
  h,w=deal(42);self.assertEqual(Counter(sum(h,[])+w),Counter(list(range(27))*4));self.assertEqual(deal(42),(h,w))
 def test_win(self):
  h=[0,1,2,3,4,5,6,7,8,9,9,9,10,10];self.assertTrue(winning(h,2));self.assertFalse(winning(h,0))
 def test_wait(self):self.assertIn(10,waits([0,1,2,3,4,5,6,7,8,9,9,9,10],2))
 def test_missing(self):self.assertEqual(legal_discards([0,9,18],0),[0])
 def test_multiwin(self):self.assertEqual(transfer([0]*4,0,[1,2],[16,8]),[-24,16,8,0])
 def test_invalid(self):
  with self.assertRaises(ValueError):winning([0]*14,2)

class AdditionalTests(unittest.TestCase):
 def test_seven_pairs(self):self.assertTrue(winning([0,0,1,1,3,3,5,5,7,7,9,9,12,12],2))
 def test_cap(self):self.assertEqual(score([0,0,1,1,2,2,3,3,4,4,5,5,6,6],2)['payment'],16)
 def test_context(self):
  for missing,count in [(-1,0),(3,0),(2,5),(2,-1)]:
   with self.assertRaises(ValueError):winning([],missing,count)
 def test_fifth_across_meld(self):
  with self.assertRaises(ValueError):winning([0,0],2,1,[[0,0,0]])
 def test_bad_seat(self):
  with self.assertRaises(ValueError):transfer([0]*4,-1,[1],[1])
 def test_exchange(self):
  h=[[0,0,0],[9,9,9],[18,18,18],[1,1,1]]
  for direction in (1,2,3):
   result=exchange(h,h,direction);self.assertEqual(result[direction],h[0]);self.assertEqual(Counter(sum(result,[])),Counter(sum(h,[])))
 def test_bad_exchange(self):
  with self.assertRaises(ValueError):exchange([[0,1,9]]*4,[[0,1,9]]*4,1)

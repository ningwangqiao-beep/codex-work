import unittest
from baselines.revision_bot import BaselineBot
class RevisionBotTests(unittest.TestCase):
 def test_legal_deterministic(self):
  o=dict(observer_player=0,observer_hand=[0,1,2,3,4,5,6,7,8,9,9,9,10,10],declared_missing_suits=[0,1,2,0],visible_discards=[],public_melds=[[],[],[],[]],public_winning_tiles=[],active=[True]*4)
  b=BaselineBot(two_step_draw_limit=0);legal=list(range(9));a=b(o,legal);self.assertIn(a,legal);self.assertEqual(a,b(o,legal));self.assertEqual(len(b.last_analysis),9)
 def test_illegal_mask(self):
  o=dict(observer_player=0,observer_hand=[0]*2,declared_missing_suits=[0]*4)
  with self.assertRaises(ValueError):BaselineBot()(o,[1])

class TwoDrawAccounting(unittest.TestCase):
 def test_two_draw_weight_without_replacement(self):
  from unittest.mock import patch
  from baselines.revision_bot import two_draw_value
  h=[0,0,0,1,2,3,4,5,6,7,8,9,10];pub=[11]*4
  def distance(hand,*a):return {'minimum':2 if len(hand)==13 else 1}
  def effective(hand,opened,missing,public):
   from collections import Counter
   known=Counter(hand+public)
   return [{'tile':0,'remaining':4-known[0],'shanten':1}] if known[0]<4 else []
  with patch('baselines.revision_bot.shanten',side_effect=distance),patch('baselines.revision_bot.effective_draws',side_effect=effective),patch('baselines.revision_bot.legal_discards',return_value=[10]):
   # First remaining 1; after drawing the last zero, no second zero remains.
   self.assertEqual(two_draw_value(h,0,2,pub),0)
 def test_expected_branch_weight(self):
  from unittest.mock import patch
  from baselines.revision_bot import two_draw_value
  h=[0]*2+[1,2,3,4,5,6,7,8,9,10,12];pub=[];calls=[]
  def effective(hand,opened,missing,public):
   from collections import Counter
   known=Counter(hand+public);calls.append(known[0]);return [{'tile':0,'remaining':4-known[0],'shanten':0}] if known[0]<4 else []
  with patch('baselines.revision_bot.shanten',return_value={'minimum':2}),patch('baselines.revision_bot.effective_draws',side_effect=effective),patch('baselines.revision_bot.legal_discards',return_value=[10]):
   self.assertAlmostEqual(two_draw_value(h,0,2,pub),2/95*1/94*2);self.assertEqual(calls,[2,3])

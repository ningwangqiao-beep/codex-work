import unittest
from simulator.table import Table
class ActionTests(unittest.TestCase):
 def test_peng(self):
  t=Table([[0],[0,0],[9],[18]],[2,2,2,1]);t.discard(0,0);t.claim(1,'peng');self.assertEqual(t.melds[1],[[0]*3]);t.check()
 def test_kong(self):
  t=Table([[0],[0,0,0],[9],[18]],[2,2,2,1],[8]);t.discard(0,0);t.claim(1,'exposed_kong');self.assertEqual(t.hands[1],[8]);t.check()
 def test_concealed(self):
  t=Table([[0]*4,[9],[18],[]],[2,2,1,0],[8]);t.concealed_kong(0,0);self.assertEqual(t.melds[0],[[0]*4]);t.check()
 def test_multiwin(self):
  h=[0,1,2,3,4,5,6,7,8,9,9,9,10]
  # Use disjoint suits/ranks to stay within physical four-copy inventory.
  a=[0,1,2,3,4,5,6,7,8,10,10,10,11]
  b=[9,9,9,12,13,14,15,16,17,18,19,20,11]
  t=Table([[11],a,b,[]],[2,2,0,0]);t.discard(0,11);t.discard_win([1,2]);self.assertEqual(t.scores,[-2,1,1,0]);self.assertEqual(t.active,[True,False,False,True]);t.check()
 def test_reject_missing(self):
  t=Table([[0],[0,0,18],[],[]],[2,2,0,0]);t.discard(0,0)
  with self.assertRaises(ValueError):t.claim(1,'peng')
 def test_advance(self):
  t=Table([[0],[1],[],[]],[2,2,0,0],[8]);t.discard(0,0);self.assertEqual(t.advance(),8);self.assertEqual(t.turn,1);t.check()
 def test_self_win(self):
  a=[0,1,2,3,4,5,6,7,8,9,9,9,10,10]
  t=Table([a,[],[],[]],[2,0,0,0]);t.self_win(0);self.assertFalse(t.active[0]);self.assertEqual(sum(t.scores),0)
 def test_added_kong(self):
  t=Table([[0],[0,0,8],[],[]],[2,2,0,0],[0,7]);t.discard(0,0);t.claim(1,'peng');t.hands[1].append(t.wall.pop(0));t.added_kong(1,0);t.resolve_added_kong();self.assertEqual(t.melds[1],[[0]*4]);t.check()
 def test_flower_pig(self):
  t=Table([[18],[0],[],[]],[2,2,0,0]);t.finish();self.assertEqual(t.scores,[-48,16,16,16]);before=t.scores[:];t.finish();self.assertEqual(before,t.scores)
 def test_ready_settlement(self):
  a=[0,1,2,3,4,5,6,7,8,9,9,9,10]
  t=Table([a,[12],[],[]],[2,2,2,2]);t.finish();self.assertGreater(t.scores[0],0);self.assertEqual(sum(t.scores),0)

 def test_strict(self):
  from rules.core import deal
  h,w=deal(55);h[0].append(w.pop());t=Table(h,[0,1,2,0],w,strict=True);t.check()
  with self.assertRaises(ValueError):Table([[],[],[],[]],[0]*4,strict=True)
 def test_config_cha_jiao(self):
  from rules.core import AssumptionConfig
  a=[0,1,2,3,4,5,6,7,8,9,9,9,10]
  t=Table([a,[],[],[]],[2]*4,config=AssumptionConfig(cha_jiao_enabled=False));t.finish();self.assertEqual(t.scores,[0]*4)
 def test_wrong_payment(self):
  a=[0,1,2,3,4,5,6,7,8,9,9,9,10]
  t=Table([[10],a,[],[]],[2]*4);t.discard(0,10)
  with self.assertRaises(ValueError):t.discard_win([1],[999])
  t.check();self.assertTrue(t.active[1])
 def test_rob_kong(self):
  a=[9,9,9,12,13,14,18,19,20,21,21,10,12]
  t=Table([[],[11,8],a,[]],[2,2,0,0],[7]);t.melds[1]=[[11]*3];t.inventory=t.counts();t.turn=1;t.added_kong(1,11);t.resolve_added_kong([2]);self.assertFalse(t.active[2]);self.assertEqual(t.melds[1],[[11]*3]);t.check()
 def test_exhaustion(self):
  t=Table([[0],[],[],[]],[2]*4);t.discard(0,0);t.advance();self.assertEqual(t.phase,'ended');t.check()

 def test_gang_fee_refund(self):
  from rules.core import AssumptionConfig
  t=Table([[0],[0,0,0],[],[]],[2]*4,[8],config=AssumptionConfig(gang_payments_enabled=True));t.discard(0,0);t.claim(1,'exposed_kong');self.assertEqual(t.scores,[-2,2,0,0]);t.finish();self.assertEqual(t.scores,[0]*4)

import unittest
from simulator.table import Table
from simulator.v3_history_v2 import sample
from rules.v3 import V3Config
class LabelAudit(unittest.TestCase):
 def target(self):return [0,1,2,3,4,5,6,7,8,9,9,9,10]
 def table(self,observer=0,target=1):
  h=[[] for _ in range(4)];h[target]=self.target();t=Table(h,[2]*4,config=V3Config());t.turn=observer;return t
 def test_relative_seat_order(self):
  for p in range(4):
   for offset in (1,2,3):
    q=(p+offset)%4;t=self.table(p,q);r=sample(t,p,1,0,[])
    self.assertEqual(r['tenpai'],[int(i==offset-1) for i in range(3)])
    self.assertEqual(r['joint_outcome'][10],1<<(offset-1));self.assertEqual(r['waits'][offset-1][10],1)
 def test_inactive_and_missing(self):
  t=self.table();t.active[1]=False;r=sample(t,0,1,0,[]);self.assertEqual(r['tenpai'],[0,0,0]);self.assertEqual(r['joint_outcome'][10],0)
  t=self.table();t.missing[1]=0;r=sample(t,0,1,0,[]);self.assertEqual(r['tenpai'],[0,0,0])
 def test_structural_dead_wait_is_positive(self):
  t=self.table();t.discards=[(2,10)]*3;t.inventory=t.counts();t.check();r=sample(t,0,1,0,[])
  self.assertEqual(r['waits'][0][10],1);self.assertEqual(r['tenpai'][0],1);self.assertEqual(r['candidate_mask'][10],0)
  self.assertEqual(t.hands[1].count(10)+sum(tile==10 for _,tile in t.discards),4)
 def test_candidate_action_gate_separate(self):
  t=self.table();t.hands[0]=[18,10];t.inventory=t.counts();r=sample(t,0,1,0,[])
  self.assertEqual(r['joint_outcome'][10],1);self.assertEqual(r['candidate_mask'][10],0);self.assertEqual(r['candidate_mask'][18],1)

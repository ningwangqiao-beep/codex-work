import unittest
from rules.v3 import V3Config,score_v3,VERSION
from simulator.table import Table
class V3Tests(unittest.TestCase):
 def test_basic_self_draw(self):
  h=[0,1,2,3,4,5,6,7,8,9,9,9,10,10]
  self.assertEqual(score_v3(h,2)['payment'],2);self.assertEqual(score_v3(h,2,self_draw=True)['payment'],4)
 def test_fan_levels(self):
  h=[0,0,1,1,3,3,5,5,7,7,9,9,12,12];self.assertEqual(score_v3(h,2)['fan'],2)
  h=[0]*4+[1]*2+[3]*2+[5]*2+[9]*2+[12]*2;self.assertEqual(score_v3(h,2)['fan'],3);self.assertEqual(score_v3(h,2,self_draw=True)['fan'],4)
  h=[0,0,1,1,2,2,3,3,4,4,5,5,6,6];self.assertEqual(score_v3(h,2,self_draw=True)['fan'],4)
 def test_direct_kong_matrix(self):
  t=Table([[0],[0,0,0],[],[]],[2]*4,[8],config=V3Config());t.discard(0,0);t.claim(1,'exposed_kong');self.assertEqual(t.scores,[-2,4,-1,-1]);self.assertEqual(sum(t.scores),0)
 def test_concealed_kong_matrix(self):
  t=Table([[0]*4,[],[],[]],[2]*4,[8],config=V3Config());t.concealed_kong(0,0);self.assertEqual(t.scores,[6,-2,-2,-2])
 def test_self_active_only(self):
  h=[0,1,2,3,4,5,6,7,8,9,9,9,10,10];t=Table([h,[],[],[]],[2]*4,config=V3Config());t.active[3]=False;t.self_win(0);self.assertEqual(t.scores,[8,-4,-4,0]);self.assertEqual({e['category'] for e in t.settlement_ledger},{'self_draw'})
 def test_added_matrix(self):
  t=Table([[],[0,8],[],[]],[2]*4,[7],config=V3Config());t.melds[1]=[[0]*3];t.inventory=t.counts();t.turn=1;t.added_kong(1,0);t.resolve_added_kong();self.assertEqual(t.scores,[-1,3,-1,-1]);self.assertEqual({e['category'] for e in t.settlement_ledger},{'added_kong'})
 def test_ledger_reconstruct(self):
  t=Table([[0],[0,0,0],[],[]],[2]*4,[8],config=V3Config());t.discard(0,0);t.claim(1,'exposed_kong');t.finish();r=[0]*4
  for e in t.settlement_ledger:r[e['payer']]-=e['amount'];r[e['receiver']]+=e['amount']
  self.assertEqual(r,t.scores);self.assertEqual(sum(r),0)
 def test_v3_identity(self):
  with self.assertRaises(ValueError):V3Config(rule_version='other')
  with self.assertRaises(ValueError):V3Config(added_kong_fee=2)
 def test_provenance(self):
  h=[0,1,2,3,4,5,6,7,8,9,9,9,10,10];r=score_v3(h,2);self.assertFalse(r['room_verified']);self.assertEqual(r['rule_source'],'user_specification')
 def test_all_active_subsets_gang_matrix(self):
  for mask in range(8):
   others=[p for p in (1,2,3) if mask&(1<<(p-1))]
   t=Table([[0]*4,[],[],[]],[2]*4,[8],config=V3Config());t.active=[p==0 or p in others for p in range(4)];t.concealed_kong(0,0);self.assertEqual(t.scores,[2*len(others)]+[-2 if p in others else 0 for p in (1,2,3)])
   t=Table([[0,8],[],[],[]],[2]*4,[7],config=V3Config());t.melds[0]=[[0]*3];t.inventory=t.counts();t.active=[p==0 or p in others for p in range(4)];t.added_kong(0,0);t.resolve_added_kong();self.assertEqual(t.scores,[len(others)]+[-1 if p in others else 0 for p in (1,2,3)])
  for mask in range(4):
   t=Table([[0],[0,0,0],[],[]],[2]*4,[8],config=V3Config());t.active=[True,True,bool(mask&1),bool(mask&2)];t.discard(0,0);t.claim(1,'exposed_kong');self.assertEqual(t.scores,[-2,2+int(bool(mask&1))+int(bool(mask&2)),-int(bool(mask&1)),-int(bool(mask&2))])

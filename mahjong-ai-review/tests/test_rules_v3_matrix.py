import unittest
from rules.v3 import V3Config,score_v3
from simulator.table import Table
class V3Matrix(unittest.TestCase):
 def test_active_subsets(self):
  for mask in range(8):
   others=[p for p in (1,2,3) if mask&(1<<(p-1))]
   for kind,fee in [('concealed',2),('added',1)]:
    hand=[0]*4 if kind=='concealed' else [0,8]
    t=Table([hand,[],[],[]],[2]*4,[7],config=V3Config());t.active=[p==0 or p in others for p in range(4)]
    if kind=='concealed':t.concealed_kong(0,0)
    else:t.melds[0]=[[0]*3];t.inventory=t.counts();t.added_kong(0,0);t.resolve_added_kong()
    self.assertEqual(t.scores,[fee*len(others)]+[-fee if p in others else 0 for p in (1,2,3)]);t.check()
  for mask in range(4):
   t=Table([[0],[0,0,0],[],[]],[2]*4,[8],config=V3Config());t.active=[True,True,bool(mask&1),bool(mask&2)];t.discard(0,0);t.claim(1,'exposed_kong');self.assertEqual(t.scores,[-2,2+int(bool(mask&1))+int(bool(mask&2)),-int(bool(mask&1)),-int(bool(mask&2))]);self.assertTrue(all(e['category']=='direct_kong' for e in t.settlement_ledger))
 def test_pattern_fixtures(self):
  fixtures=[('basic',[0,1,2,3,4,5,6,7,8,9,9,9,10,10],1),('all_triplets',[0]*3+[3]*3+[9]*3+[12]*3+[15]*2,2),('pure_suit',[0,1,2,3,4,5,6,7,8,1,2,3,5,5],2),('dai_yao',[0,1,2,6,7,8,9,10,11,15,16,17,0,0],2),('seven_pairs',[0,0,1,1,3,3,5,5,7,7,9,9,12,12],2),('dragon_pairs',[0]*4+[1]*2+[3]*2+[5]*2+[9]*2+[12]*2,3),('pure_triplets',[0]*3+[2]*3+[4]*3+[6]*3+[8]*2,3),('jiang_triplets',[1]*3+[4]*3+[10]*3+[13]*3+[16]*2,3),('pure_seven_pairs',[0,0,1,1,2,2,3,3,4,4,5,5,6,6],4),('pure_dragon_pairs',[0]*4+[1]*2+[2]*2+[3]*2+[4]*2+[5]*2,4)]
  for pattern,h,base in fixtures:
   missing=next(s for s in range(3) if all(t//9!=s for t in h));r=score_v3(h,missing);self.assertIn(pattern,r['patterns']);self.assertEqual(r['base_fan'],base);self.assertEqual(score_v3(h,missing,self_draw=True)['fan'],min(4,base+1))
 def test_refund_ledger(self):
  t=Table([[0],[0,0,0],[],[]],[2]*4,[8],config=V3Config());t.discard(0,0);t.claim(1,'exposed_kong');t.finish();refund=[e for e in t.settlement_ledger if e['category']=='gang_refund'];self.assertEqual(len(refund),3);self.assertTrue(all(e['reversal'] for e in refund));t.check()

 def test_cha_jiao_modes(self):
  hand=[0,1,2,3,4,5,6,7,8,9,9,9,10]
  for mode,category in [('max_wait_payment','cha_jiao_big'),('min_wait_payment','cha_jiao_small'),('disabled',None)]:
   t=Table([hand,[],[],[]],[2]*4,config=V3Config(cha_jiao_mode=mode));t.finish();events=[e for e in t.settlement_ledger if e['category'].startswith('cha_jiao')]
   self.assertEqual({e['category'] for e in events},set() if category is None else {category});t.check()

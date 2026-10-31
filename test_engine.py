import unittest,numpy as np
from engine import run
class EngineTest(unittest.TestCase):
 def bars(self,rows):return np.array([[i*60000,*x,1.] for i,x in enumerate(rows)],float)
 def audit(self,a,params):
  r,d,s,b,e,t=run(a,record=1,**params)
  # Ledger identity: equity equals initial capital + realized gross - all fees + open gross.
  self.assertAlmostEqual(e[-1],10000+sum(x[7]-x[6] for x in t)+s[10],places=7)
  self.assertAlmostEqual(s[5],sum(x[6] for x in t),places=7)
  for x in t:
   bar,side,kind,p=x[:4];o,h,l,c=a[int(bar),1:5]
   direction=side if kind<=1 else -side
   if direction>0:self.assertGreaterEqual(p+1e-9,l)
   else:self.assertLessEqual(p-1e-9,h)
  return r,d,s,b,e,t
 def test_multilevel_and_order(self):
  a=self.bars([[100,100,100,100],[100,102,94,97]])
  r,d,s,b,e,t=self.audit(a,{})
  adds=[x for x in t if x[0]==1 and x[2]==1 and x[1]==1]
  self.assertEqual(len(adds),5)
  self.assertTrue(np.allclose([x[5] for x in adds],[400,800,1600,3200,6400]))
  self.assertTrue(np.allclose([x[3] for x in adds],[100*.99**k for k in range(1,6)]))
  phases=[x[2] for x in t if x[0]==1]
  self.assertLess(max(i for i,x in enumerate(phases) if x==1),min(i for i,x in enumerate(phases) if x==2))
  self.assertLessEqual(s[0],2)
 def test_gap_no_unreachable_reopen(self):
  a=self.bars([[100,100,100,100],[98,98,98,98]])
  r,d,s,b,e,t=self.audit(a,{})
  self.assertTrue(any(x[2]==1 and x[1]==1 and x[3]>98 for x in t))
  self.assertFalse(any(x[2]==2 and x[1]==-1 and x[3]>98 for x in t))
 def test_cap_skip(self):
  a=self.bars([[100,100,100,100],[100,100,90,90]])
  self.assertGreater(self.audit(a,{'cap':.05})[2][7],0)
 def test_stair_stop_and_restart(self):
  a=self.bars([[100,100,100,100],[100,100,93,93],[93,93,93,93]])
  r,d,s,b,e,t=self.audit(a,{'tp':.2})
  stop=[x for x in t if x[2]==3 and x[1]==1]
  self.assertEqual(len(stop),1);self.assertEqual(stop[0][3],93.)
  self.assertTrue(any(x[0]==2 and x[2]==0 and x[1]==1 for x in t))
 def test_prefix_invariance(self):
  a=self.bars([[100,100,100,100],[100,101,99,100],[100,103,97,99],[99,100,98,100]])
  full=self.audit(a,{})
  prefix=self.audit(a[:3],{})
  self.assertTrue(np.allclose(full[4][:3],prefix[4]))
  self.assertEqual([x for x in full[5] if x[0]<3],prefix[5])
 def test_regime_uses_past_close_and_ledgers(self):
  a=self.bars([[100,100.1,100,100.1],[100.1,100.3,100.1,100.3],[100.3,100.3,99.8,99.8],[99.8,99.8,99.5,99.5]])
  p={'bias':5.,'fast':2,'slow':4,'regime_exit':1,'g':.1,'tp':.1}
  full=self.audit(a,p);prefix=self.audit(a[:3],p)
  self.assertTrue(np.allclose(full[4][:3],prefix[4]))
  self.assertEqual([x for x in full[5] if x[0]<3],prefix[5])
  self.assertTrue(any(x[2]==6 and x[0]==1 for x in full[5]))
  self.assertTrue(all(x[3]==a[int(x[0]),1] for x in full[5] if x[2]==6))
if __name__=='__main__':unittest.main()

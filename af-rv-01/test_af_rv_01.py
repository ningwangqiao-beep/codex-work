"""Accounting and timing regression checks; no strategy parameter variants."""
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
import run_af_rv_01 as m
class Accounting(unittest.TestCase):
    def test_two_leg_round_trip_and_funding(self):
        n=730; t=np.arange(n,dtype=np.int64)*3600000
        bars=[pd.DataFrame({'open_time':t,'open':np.full(n,100.),'close':np.full(n,100.)}) for _ in range(2)]
        funds=[pd.DataFrame({'calc_time':[t[721]+1],'last_funding_rate':[.001]}),pd.DataFrame({'calc_time':[t[721]+7],'last_funding_rate':[.002]})]
        z=np.full(n,np.nan); z[720]=2.;z[721]=0.
        fake=(np.ones(n),z,np.ones((n,2)),1.,np.zeros(n))
        with patch.object(m,'features',return_value=fake): eq,tr,ledger=m.run(bars,funds,'dollar')
        self.assertEqual(len(tr),1); a=tr[0]
        self.assertEqual(a['entry_ts'],t[721]);self.assertEqual(a['exit_ts'],t[722])
        self.assertEqual(a['exit_reason'],'take_profit')
        self.assertAlmostEqual(a['eth_entry_px'],99.98);self.assertAlmostEqual(a['btc_entry_px'],100.02)
        self.assertAlmostEqual(a['funding_eth'],500/99.98*100*.001)
        self.assertAlmostEqual(a['funding_btc'],-500/100.02*100*.002)
        self.assertAlmostEqual(eq[-1]-1000,a['net_pnl'])
        self.assertAlmostEqual(a['fees'],sum(x['fee'] for x in ledger))
        self.assertLess(a['gross_pnl'],0)
    def test_timeout_cooldown_and_fixed_quantities(self):
        n=860; t=np.arange(n,dtype=np.int64)*3600000
        prices=np.linspace(100,120,n)
        bars=[pd.DataFrame({'open_time':t,'open':prices,'close':prices}) for _ in range(2)]
        funds=[pd.DataFrame({'calc_time':[], 'last_funding_rate':[]}) for _ in range(2)]
        fake=(np.linspace(.5,2,n),np.full(n,2.),np.ones((n,2)),1.,np.zeros(n))
        with patch.object(m,'features',return_value=fake): eq,tr,_=m.run(bars,funds,'rolling_beta')
        self.assertEqual([a['entry_ts']//3600000 for a in tr],[721,794])
        self.assertEqual([a['exit_ts']//3600000 for a in tr],[769,842])
        self.assertTrue(all(a['exit_reason']=='timeout' and a['holding_hours']==48 for a in tr))
        self.assertAlmostEqual(tr[0]['eth_qty']*tr[0]['eth_entry_px'],-1000/(1+fake[0][720]))
        self.assertAlmostEqual(eq[-1]-1000,sum(a['net_pnl'] for a in tr))
if __name__=='__main__': unittest.main()

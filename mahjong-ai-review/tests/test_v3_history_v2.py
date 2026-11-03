"""Independent history contracts; require D's separate history_v2 implementation."""
import unittest
from simulator.v3_history_v2 import append_event,play
class HistoryV2(unittest.TestCase):
 def test_indices_and_public_draw(self):
  h=[];append_event(h,0,'draw');append_event(h,0,'discard',tile=3)
  self.assertEqual([x['event_index'] for x in h],list(range(len(h))))
  self.assertNotIn('tile',h[0]);self.assertEqual(h[1]['tile'],3)
 def test_private_draw_rejected_or_masked(self):
  h=[]
  try:append_event(h,0,'draw',tile=8)
  except ValueError:return
  self.assertNotIn('tile',h[-1])
 def test_initial_and_replacement_draw(self):
  total=0
  for seed in range(10):
   r=play(seed);h=r['public_history'];self.assertEqual([e['event_index'] for e in h],list(range(len(h))))
   draws=[e for e in h if e['action']=='draw'];self.assertTrue(draws)
   for e in draws:self.assertNotIn('tile',e)
   for i,e in enumerate(h):
    if e['action']=='exposed_kong':
     self.assertLess(i+1,len(h));self.assertEqual(h[i+1]['action'],'draw');self.assertEqual(h[i+1]['player'],e['player']);total+=1
   for event in r['win_events']:
    if event['kind']=='rob_kong_win':self.assertTrue(any(e['action']=='rob_kong_win' and e['player']==event['seat'] for e in h))
  self.assertGreater(total,0,'fixture seeds did not exercise direct kong replacement')
 def test_projection_and_exchange_scope(self):
  from simulator.table import Table
  from observations.v3_history_v2 import observe
  t=Table([[0],[9],[],[]],[2]*4,[8]);t.exchange_records=[dict(sent=[0,1,2],received=[3,4,5],direction=1,source_player=(p-1)%4) for p in range(4)]
  h=[dict(event_index=0,player=1,action='draw',tile=8,hidden_hand='secret'),dict(event_index=1,player=1,action='concealed_kong',tile=9)]
  o=observe(t,0,h);self.assertTrue(all('tile' not in e for e in o['public_action_history']));self.assertNotIn('hidden_hand',str(o));self.assertIn('not current',o['exchange']['knowledge_scope']);self.assertNotIn('wall',o)
  t.hands[1]=[10];self.assertEqual(observe(t,0,h),o)
 def test_public_pass_and_win_sequence(self):
  h=[]
  for p,a,tile in [(0,'discard',3),(1,'pass',None),(2,'discard_win',3),(3,'discard_win',3)]:append_event(h,p,a,tile)
  self.assertEqual([e['action'] for e in h],['discard','pass','discard_win','discard_win']);self.assertNotIn('tile',h[1])
 def test_initial_draw_context(self):
  h=play(3)['public_history'];draw=next(e for e in h if e['action']=='draw');self.assertEqual(draw['player'],0);self.assertEqual(draw['context'],'initial_draw')

class RealRobberySeeds(unittest.TestCase):
 def test_rob_history_ledger_real_seeds(self):
  for seed in (3300120,3300658,3301004,3301321,3301812):
   r=play(seed,exchange_offset=seed%3+1)
   wins=[e for e in r['win_events'] if e['kind']=='rob_kong_win']
   events=[e for e in r['public_history'] if e['action']=='rob_kong_win']
   ledger=[e for e in r['ledger'] if e['category']=='rob_kong_win']
   self.assertGreater(len(wins),0,seed);self.assertEqual(len(events),len(wins));self.assertEqual(len(ledger),len(wins))
   for w in wins:
    self.assertEqual(sum(e['player']==w['seat'] for e in events),1)
    self.assertEqual(sum(e['payer']==w['payer'] and e['receiver']==w['seat'] and e['amount']==w['payment'] for e in ledger),1)
   h=r['public_history']
   for i,e in enumerate(h):
    if e['action']=='rob_kong_win':
     preceding=next(x for x in reversed(h[:i]) if x['action'] not in ('rob_kong_win','pass'))
     self.assertEqual(preceding['action'],'added_kong');self.assertEqual(preceding['tile'],e['tile'])

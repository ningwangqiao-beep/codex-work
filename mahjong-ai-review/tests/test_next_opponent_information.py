import unittest,copy
import torch
from models.next_opponent import OpponentAblation
from inference.v3_observation import encode_observation
class InformationAudit(unittest.TestCase):
 def observation(self):return dict(observer_player=0,observer_hand=list(range(13)),declared_missing_suits=[2]*4,visible_discards=[],public_melds=[[],[],[],[]],active=[True]*4,turn_index=9,current_player=0,public_action_history=[dict(player=0,action='draw',tile=4)],remaining_wall_information=55)
 def test_masks_exact(self):
  expected=set(range(74))|set(range(76,80))
  for family in ('counts','progress','history','exchange','history_shuffled'):
   mask=set(torch.where(OpponentAblation(family).static_mask.bool())[0].tolist());want=expected.copy()
   if family!='counts':want|={74,75,190}
   if family=='exchange':want|=set(range(128,190))
   self.assertEqual(mask,want)
 def test_truth_poison_ignored(self):
  o=self.observation();a=encode_observation(o);o.update(real_wall=[26]*55,opponent_hands=[[1]*13]*3,future_score=999);self.assertEqual(a,encode_observation(o))
 def test_history_draw_hidden_but_static_summary_boundary(self):
  o=self.observation();a=encode_observation(o);o['public_action_history'][0]['tile']=9;b=encode_observation(o)
  self.assertEqual(a['history_tokens'],b['history_tokens'])
  # Legacy summary does not redact malformed raw draw tile; all ablation masks remove it.
  self.assertNotEqual(a['state_features'][84:128],b['state_features'][84:128])
  self.assertEqual(a['state_features'][:84],b['state_features'][:84])
 def test_own_exchange_not_current_inventory(self):
  o=self.observation();a=encode_observation(o);o['exchange']=dict(sent=[0,1,2],received=[3,4,5],direction=1,source_player=3);b=encode_observation(o)
  self.assertEqual(a['state_features'][:128],b['state_features'][:128]);self.assertNotEqual(a['state_features'][128:190],b['state_features'][128:190])

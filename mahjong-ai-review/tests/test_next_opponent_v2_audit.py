import unittest,copy,torch
from models.next_opponent_tile_v2 import SharedTileOpponent
from training.next_opponent_tile_v2_pipeline import public_tile_features,collate,losses,constrained_joint_logits
class TileV2Audit(unittest.TestCase):
 def row(self,p=0):
  from inference.v3_observation import encode_observation
  o=dict(observer_player=p,observer_hand=[0]*4,visible_discards=[],public_melds=[[],[],[],[]],declared_missing_suits=[0,1,2,0],active=[True,True,False,True],public_winning_tiles=[],turn_index=0,current_player=p,public_action_history=[],remaining_wall_information=56)
  o['active'][p]=True
  return dict(observation=o,state_features=encode_observation(o)['state_features'],structural_tenpai=[0,0,0],structural_waits=[[0]*27 for _ in range(3)],target_active=[int(o['active'][(p+k+1)%4]) for k in range(3)],legal_mask=[1]*27,joint_winner_mask=[0]*27)
 def test_relative_mapping(self):
  for p in range(4):
   r=self.row(p);f=public_tile_features([r],'cpu')
   for k in range(3):
    q=(p+k+1)%4;s=r['observation']['declared_missing_suits'][q];self.assertEqual(f[0,k,s*9,3].item(),1);self.assertEqual(f[0,k,0,13].item(),float(r['observation']['active'][q]))
 def test_missing_zero_known_four_not_zero(self):
  r=self.row();m=SharedTileOpponent()
  for p in m.parameters():torch.nn.init.zeros_(p)
  inp,t=collate([r],'cpu','shared_tile');o=m(*inp);w=o['conditional_structural_wait_logits'].sigmoid()
  self.assertEqual(w[0,0,9].item(),0.);self.assertEqual(inp[1][0,0,0,2].item(),0.);self.assertEqual(w[0,0,0].item(),.5)
 def test_poison_no_feature_effect(self):
  r=self.row();a=public_tile_features([r],'cpu');r['observation'].update(real_wall=[26]*100,opponent_hands=[[4]*13]*3,future_score=100);self.assertTrue(torch.equal(a,public_tile_features([r],'cpu')))
 def test_missing_label_rejected(self):
  r=self.row();r['structural_waits'][0][9]=1
  with self.assertRaises(ValueError):collate([r],'cpu','shared_tile')
 def test_active_mask_loss(self):
  r=self.row();r['target_active']=[1,0,1];inp,t=collate([r],'cpu','shared_tile');o=SharedTileOpponent()(*inp);j=constrained_joint_logits(o,t).softmax(-1);self.assertEqual(j[:,:,[2,3,6,7]].sum().item(),0.);self.assertTrue(all(torch.isfinite(v) for v in losses(o,t).values()))

 def test_relative_active_mismatch_rejected(self):
  r=self.row();r['target_active'][0]=1-r['target_active'][0]
  with self.assertRaisesRegex(ValueError,'Relative active target mismatch'):collate([r],'cpu','shared_tile')

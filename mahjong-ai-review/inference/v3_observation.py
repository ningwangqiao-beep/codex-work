"""Causal V3 public-history input schema. No hand/wall truth accepted."""
from inference.v3_legacy import legacy_static_features
RULE_VERSION='SICHUAN-XUEZHAN-4FAN-V3'
ACTIONS={'draw':1,'discard':2,'peng':3,'exposed_kong':4,'concealed_kong':5,'added_kong':6,'win':7,'pass':8,'exchange':9,'missing':10,'other_public':11,'missing_declared':12,'self_win':13,'discard_win':14,'rob_kong_win':15}
STATIC_DIM=191

def encode_observation(o):
 # Legacy128 is retained as explicit summary, never mistaken for full sequence.
 required=['observer_player','observer_hand','declared_missing_suits','visible_discards','public_melds','active','turn_index','current_player','public_action_history']
 for k in required:
  if k not in o:raise ValueError('Missing public field '+k)
 observer=o['observer_player'];known=o.get('remaining_wall_information') is not None;summary=dict(o);summary['remaining_wall_information']=o.get('remaining_wall_information') or 0;state=legacy_static_features(summary);exchange=o.get('exchange') or {};sent=exchange.get('sent',[]);received=exchange.get('received',[])
 for name,tiles in [('sent',sent),('received',received)]:
  if len(tiles) not in (0,3) or any(type(t)!=int or t not in range(27) for t in tiles):raise ValueError('Invalid own exchange '+name)
 state += [sent.count(t)/4 for t in range(27)]+[received.count(t)/4 for t in range(27)]
 direction=exchange.get('direction');source=exchange.get('source_player');state += [float(direction==k) for k in (None,1,2,3)]+[float(source==k) for k in range(4)]+[float(known)]
 if len(state)!=STATIC_DIM:raise AssertionError('Static schema drift')
 tokens=[]
 for e in o['public_action_history']:
  if not isinstance(e,dict) or e.get('action') not in ACTIONS:raise ValueError('Unsupported public history action')
  action=e['action'];player=e.get('player');tile=e.get('tile',-1)
  if player is not None and (type(player)!=int or player not in range(4)):raise ValueError('Bad history player')
  # A draw is never exposed by a generic public event. Own hand already contains own draw.
  if action=='draw' or (action=='concealed_kong' and player!=observer):tile=-1
  if type(tile)!=int or tile not in range(-1,27):raise ValueError('Bad public tile')
  tokens.append([ACTIONS[action],((player-observer)%4 if player is not None else 4),tile+1])
 return {'rule_version':RULE_VERSION,'schema_version':'v3-public191-fullseq-v2','state_features':state,'history_tokens':tokens,'history_mask':[True]*len(tokens),'history_original_length':len(tokens),'history_truncated':False,'flags':['EXCHANGE_VALUES_ARE_PAST_EVENTS_NOT_CURRENT_OPPONENT_HOLDINGS','WALL_COUNT_VALID_ONLY_WHEN_PUBLIC_BY_ROOM_CONFIG']}

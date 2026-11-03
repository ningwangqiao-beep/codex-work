"""History-v2 legal event projection; no wall/other-player hand access."""
from observations.v3_public import observe as old_observe,features
PUBLIC_FIELDS=('event_index','player','action','tile','suit','context')
def observe(table,observer,history=()):
 o=old_observe(table,observer,history);events=[]
 for event in history:
  e={k:v for k,v in event.items() if k in PUBLIC_FIELDS and type(v) in (int,str)}
  if e.get('action')=='draw' or (e.get('action')=='concealed_kong' and e.get('player')!=observer):e.pop('tile',None)
  events.append(e)
 o['public_action_history']=events;o['history_schema_version']='v3-history-v2-public-events';return o

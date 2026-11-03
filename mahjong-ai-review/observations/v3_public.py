"""V3 causal exchange observation, private exchange knowledge is time-stamped."""
from observations.public import observe as legacy_observe,features

def observe(table,observer,history=()):
 o=legacy_observe(table,observer,history)
 if hasattr(table,'exchange_records'):
  e=table.exchange_records[observer];o['exchange']={k:(list(v) if isinstance(v,list) else v) for k,v in e.items()}
  o['exchange']['knowledge_scope']='tiles exchanged at setup; not current opponent holdings'
 return o

"""Small transactional action core. Room-specific settlement remains proposed."""
from collections import Counter
from copy import deepcopy
from rules.core import winning, transfer, AssumptionConfig

class Table:
 def __init__(self,hands,missing,wall=(),config=None,strict=False):
  if len(hands)!=4 or len(missing)!=4 or any(type(s)!=int or s not in range(3) for s in missing):raise ValueError('table')
  self.config=config or AssumptionConfig();self.strict=strict
  self.hands=deepcopy(hands);self.missing=list(missing);self.wall=list(wall)
  self.melds=[[] for _ in range(4)];self.discards=[];self.active=[True]*4;self.scores=[0]*4
  self.gang_ledger=[];self.concealed_kongs=set()
  self.turn=0;self.phase='discard';self.pending=None;self.wins=[]
  self.inventory=self.counts()
  if strict and (self.inventory!=Counter({t:4 for t in range(27)}) or [len(h) for h in hands]!=[14,13,13,13]):raise ValueError("strict initial inventory/hand sizes")
  self.check()
 def counts(self):
  tiles=sum(self.hands,[])+self.wall+[t for _,t in self.discards]
  tiles += [t for ms in self.melds for m in ms for t in m]
  # A multi-winner discard is a single physical tile, kept in wins once.
  tiles += [t for _,t,_ in self.wins]
  return Counter(tiles)
 def check(self):
  c=self.counts()
  if any(type(t)!=int or t not in range(27) or n>4 for t,n in c.items()) or c!=self.inventory:raise ValueError('inventory conservation')
  if sum(self.scores)!=0:raise ValueError('score conservation')
  if self.strict:
   for p in range(4):
    if not self.active[p]:
     won_discard=any(p in winners for _,_,winners in self.wins)
     expected=13-3*len(self.melds[p])+(0 if won_discard else 1)
     if len(self.hands[p])!=expected:raise ValueError("winner hand cardinality")
     continue
    expected=13-3*len(self.melds[p])
    if self.phase in ("discard","rob_kong") and p==self.turn:expected+=1
    if len(self.hands[p])!=expected:raise ValueError("phase hand cardinality")
 def seat(self,p):
  if type(p)!=int or p not in range(4) or not self.active[p]:raise ValueError('inactive/invalid seat')
 def discard(self,p,t):
  self.seat(p)
  if p!=self.turn or self.phase!='discard' or t not in self.hands[p]:raise ValueError('discard phase')
  if any(x//9==self.missing[p] for x in self.hands[p]) and t//9!=self.missing[p]:raise ValueError('must clear missing suit')
  self.hands[p].remove(t);self.discards.append((p,t));self.pending=(p,t);self.phase='claims';self.check()
 def claim(self,p,kind):
  self.seat(p)
  if self.phase!='claims' or self.pending is None:raise ValueError('no discard')
  payer,t=self.pending
  if any(self.active[q] and q!=payer and self.can_win(q,t) for q in range(4)):raise ValueError('win has priority')
  need={'peng':2,'exposed_kong':3}.get(kind)
  if p==payer or need is None or t//9==self.missing[p] or self.hands[p].count(t)<need:raise ValueError('illegal claim')
  if any(x//9==self.missing[p] for x in self.hands[p]):raise ValueError('missing suit remains')
  if kind=='exposed_kong' and not self.wall:raise ValueError('no replacement tile')
  for _ in range(need):self.hands[p].remove(t)
  self.discards.pop();self.melds[p].append([t]*(need+1));self.pending=None;self.turn=p;self.phase='discard'
  if kind=='exposed_kong':
   self.hands[p].append(self.wall.pop())
   self.pay_gang(p,[payer],self.config.exposed_kong_fee)
  self.check()
 def concealed_kong(self,p,t):
  self.seat(p)
  if p!=self.turn or self.phase!='discard' or self.hands[p].count(t)!=4 or t//9==self.missing[p] or not self.wall:raise ValueError('illegal concealed kong')
  if any(x//9==self.missing[p] for x in self.hands[p]):raise ValueError('missing suit remains')
  for _ in range(4):self.hands[p].remove(t)
  self.concealed_kongs.add((p,len(self.melds[p])))
  self.melds[p].append([t]*4);self.hands[p].append(self.wall.pop())
  self.pay_gang(p,[q for q in range(4) if q!=p and self.active[q]],self.config.concealed_kong_fee);self.check()
 def discard_win(self,winners,payments=None):
  if self.phase!='claims' or not self.pending or not winners or len(set(winners))!=len(winners):raise ValueError('win phase')
  payer,t=self.pending
  for p in winners:
   self.seat(p)
   if p==payer or not winning(self.hands[p]+[t],self.missing[p],len(self.melds[p]),self.melds[p]):raise ValueError('illegal win')
  from rules.core import score
  expected=[score(self.hands[p]+[t],self.missing[p],self.melds[p],self.config)["payment"] for p in winners]
  if payments is not None and list(payments)!=expected:raise ValueError("incorrect payment")
  updated=transfer(self.scores,payer,winners,expected)
  self.discards.pop();self.wins.append((payer,t,list(winners)));self.pending=None;self.scores=updated
  for p in winners:self.active[p]=False
  self.phase='ended' if sum(self.active)<=1 else 'advance'
  self.check()
 def draw(self):
  if self.phase!='draw':raise ValueError('draw phase')
  if not self.wall:self.finish();return None
  t=self.wall.pop();self.hands[self.turn].append(t);self.phase='discard';self.check();return t
 def advance(self):
  if self.phase not in ('advance','claims'):raise ValueError('advance phase')
  if self.phase=='claims':self.pending=None
  for step in range(1,5):
   p=(self.turn+step)%4
   if self.active[p]:self.turn=p;break
  self.phase='draw'
  return self.draw()
 def can_win(self,p,t=None):
  self.seat(p)
  try:return winning(self.hands[p]+([] if t is None else [t]),self.missing[p],len(self.melds[p]),self.melds[p])
  except ValueError:return False
 def self_win(self,p):
  from rules.core import score
  self.seat(p)
  if self.phase!='discard' or self.turn!=p or not self.can_win(p):raise ValueError('illegal self win')
  amount=score(self.hands[p],self.missing[p],self.melds[p],self.config)['payment']
  for q in range(4):
   if q!=p and self.active[q]:self.scores=transfer(self.scores,q,[p],[amount])
  self.active[p]=False;self.phase='ended' if sum(self.active)<=1 else 'advance';self.check()
 def added_kong(self,p,t):
  self.seat(p)
  if self.turn!=p or self.phase!='discard' or t not in self.hands[p] or not self.wall or any(x//9==self.missing[p] for x in self.hands[p]):raise ValueError('added kong')
  if [t]*3 not in self.melds[p]:raise ValueError('no peng')
  # Tile remains in hand while opponents decide whether to rob the kong.
  self.pending=(p,t);self.phase='rob_kong'
 def resolve_added_kong(self,winners=()):
  from rules.core import score
  if self.phase!='rob_kong':raise ValueError('rob kong phase')
  p,t=self.pending
  if winners:
   if len(set(winners))!=len(winners):raise ValueError('duplicate winner')
   payments=[]
   for q in winners:
    self.seat(q)
    if q==p or not self.can_win(q,t):raise ValueError('illegal rob win')
    payments.append(score(self.hands[q]+[t],self.missing[q],self.melds[q],self.config)['payment'])
   updated=transfer(self.scores,p,list(winners),payments)
   self.hands[p].remove(t);self.wins.append((p,t,list(winners)));self.scores=updated
   for q in winners:self.active[q]=False
   self.phase='ended' if sum(self.active)<=1 else 'advance'
  else:
   self.hands[p].remove(t);self.melds[p][self.melds[p].index([t]*3)].append(t)
   self.hands[p].append(self.wall.pop());self.phase='discard'
   self.pay_gang(p,[q for q in range(4) if q!=p and self.active[q]],self.config.added_kong_fee)
  self.pending=None;self.check()
 def finish(self):
  from rules.core import score
  if self.wall:raise ValueError('wall not exhausted')
  if getattr(self,'settled',False):return
  active=[p for p in range(4) if self.active[p]]
  pigs=[p for p in active if any(t//9==self.missing[p] for t in self.hands[p])]
  ready={}
  for p in active:
   if p in pigs:continue
   amounts=[score(self.hands[p]+[t],self.missing[p],self.melds[p],self.config)['payment'] for t in range(27) if self.can_win(p,t)]
   if amounts:ready[p]=max(amounts)
  for p in pigs:
   for q in active:
    if q not in pigs:self.scores=transfer(self.scores,p,[q],[2**self.config.fan_cap])
  for p in active:
   if self.config.cha_jiao_enabled and p not in pigs and p not in ready:
    for q,amount in ready.items():self.scores=transfer(self.scores,p,[q],[amount])
  if self.config.gang_payments_enabled and self.config.refund_unready_gangs:
   for receiver,payer,amount in self.gang_ledger:
    if receiver in active and receiver not in ready:self.scores=transfer(self.scores,receiver,[payer],[amount])
  self.settled=True;self.phase='ended';self.check()



 def pay_gang(self,receiver,payers,amount):
  if not self.config.gang_payments_enabled:return
  for p in payers:
   self.scores=transfer(self.scores,p,[receiver],[amount]);self.gang_ledger.append((receiver,p,amount))



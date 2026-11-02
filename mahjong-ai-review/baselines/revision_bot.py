"""Deterministic public-only baseline. Heuristics are not opponent truth."""
from collections import Counter
from rules.hand_analysis import shanten,effective_draws
from rules.core import legal_discards
def two_draw_value(hand,opened,missing,public,draw_limit=2,discard_limit=2):
 """Lower truncated improvement contribution under visible-unseen sampling.
 Two physical draws without replacement. Selected branch mass is not renormalized.
 """
 before=shanten(hand,opened,missing,public)['minimum'];total=108-len(hand)-len(public)
 if total<2 or draw_limit<1:return 0.
 value=0.
 first=sorted(effective_draws(hand,opened,missing,public),key=lambda x:(-x['remaining'],x['tile']))[:draw_limit]
 for d in first:
  h=hand+[d['tile']];post=[]
  for tile in legal_discards(h,missing):
   nxt=list(h);nxt.remove(tile);pub=public+[tile];distance=shanten(nxt,opened,missing,pub)['minimum'];post.append((distance,tile,nxt,pub))
  outcomes=[]
  for distance,tile,nxt,pub in sorted(post,key=lambda x:(x[0],x[1]))[:discard_limit]:
   second=sorted(effective_draws(nxt,opened,missing,pub),key=lambda x:(-x['remaining'],x['tile']))[:draw_limit]
   outcomes.append(sum(e['remaining']/(total-1)*max(0,before-e['shanten']) for e in second))
  value+=d['remaining']/total*max(outcomes,default=0.)
 return value

class BaselineBot:
 def __init__(self,two_step_draw_limit=2):self.limit=two_step_draw_limit;self.last_analysis=[]
 def __call__(self,o,legal):
  p=o['observer_player'];hand=o['observer_hand'];missing=o['declared_missing_suits'][p];expected=legal_discards(hand,missing)
  if sorted(legal)!=expected:raise ValueError('legal mask mismatch')
  public=[t for _,t in o['visible_discards']]+[t for ms in o['public_melds'] for m in ms for t in m if t>=0]+o.get('public_winning_tiles',[])
  opened=len(o['public_melds'][p]);rows=[]
  for tile in sorted(legal):
   h=list(hand);h.remove(tile);pub=public+[tile];s=shanten(h,opened,missing,pub);debt=sum(t//9==missing for t in h)
   rows.append(dict(tile=tile,standard=s['standard'],seven_pairs=s['seven_pairs'],structural=s['minimum'],missing_debt=debt,h=h,pub=pub))
  best=min((r['missing_debt'],r['structural']) for r in rows)
  for r in rows:
   r.update(effective=0,one_draw_value=0,two_draw_value=0,fan_cap_potential=0,public_risk=0)
   if (r['missing_debt'],r['structural'])!=best:continue
   draws=effective_draws(r['h'],opened,missing,r['pub']);r['effective']=sum(x['remaining'] for x in draws)
   # Bounded two-step structural search; truncation explicit, not full expectation.
   for draw in sorted(draws,key=lambda x:(-x['remaining'],x['tile']))[:self.limit]:
    h=r['h']+[draw['tile']];next_best=99
    for discard in legal_discards(h,missing):
     nxt=list(h);nxt.remove(discard);next_best=min(next_best,shanten(nxt,opened,missing,r['pub']+[discard])['minimum'])
    r['one_draw_value']+=draw['remaining']*(r['structural']-next_best)
   r['two_draw_value']=two_draw_value(r['h'],opened,missing,r['pub'],self.limit)
   suits={t//9 for t in r['h']}|{t//9 for m in o['public_melds'][p] for t in m if t>=0};r['fan_cap_potential']=min(4,2*int(len(suits)==1)+2*int(not opened and sum(n//2 for n in Counter(r['h']).values())>=5))
   # Missing suit rules exclude those targets; discard repetitions are only weak cues.
   eligible=sum(o['active'][q] and o['declared_missing_suits'][q]!=r['tile']//9 for q in range(4) if q!=p)
   r['public_risk']=eligible/(1+sum(t==r['tile'] for _,t in o['visible_discards']))
  chosen=min(rows,key=lambda r:(r['missing_debt'],r['structural'],-r['effective'],-r['two_draw_value'],-r['one_draw_value'],-r['fan_cap_potential'],r['public_risk'],r['tile']))['tile']
  self.last_analysis=[{k:v for k,v in r.items() if k not in ('h','pub')} for r in rows];return chosen

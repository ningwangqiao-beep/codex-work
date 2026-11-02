"""Shared linear candidate scorer. Own hand and public tiles only."""
from collections import Counter
import torch
from torch import nn
FEATURE_NAMES=['post_pairs','post_links','post_triples','post_sequences','candidate_own_count','candidate_public_count','candidate_rank','post_max_suit','post_singletons','post_missing_count','candidate_remaining_unseen','bias']
def candidate_features(o,t):
 h=list(o['observer_hand'])
 if t not in h:raise ValueError('Candidate absent')
 h.remove(t);c=Counter(h);pairs=sum(n>=2 for n in c.values());links=sum(abs(a-b) in (1,2) and a//9==b//9 for i,a in enumerate(h) for b in h[i+1:]);triples=sum(n>=3 for n in c.values());sequences=sum(min(c[i],c[i+1],c[i+2]) for i in range(27) if i%9<=6)
 public=[x for _,x in o['visible_discards']]+[x for ms in o['public_melds'] for m in ms for x in m]+o.get('public_winning_tiles',[]);missing=o['declared_missing_suits'][o['observer_player']]
 return [pairs/7,links/40,triples/4,sequences/10,o['observer_hand'].count(t)/4,public.count(t)/4,(t%9)/8,max(sum(x//9==s for x in h) for s in range(3))/14,sum(n==1 for n in c.values())/14,sum(x//9==missing for x in h)/14,max(0,4-o['observer_hand'].count(t)-public.count(t))/4,1.]
def teacher_utility(o,t):
 h=list(o['observer_hand']);h.remove(t)
 return 3*sum(h.count(x)>=2 for x in set(h))+sum(abs(a-b) in (1,2) and a//9==b//9 for i,a in enumerate(h) for b in h[i+1:])
class CandidateLinear(nn.Module):
 def __init__(self):super().__init__();self.linear=nn.Linear(len(FEATURE_NAMES),1,bias=False);nn.init.zeros_(self.linear.weight)
 def forward(self,x):return self.linear(x).squeeze(-1)

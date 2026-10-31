"""Diagnostic-only anchor replay. Some same-price TP reopens violate the
candle extreme: this version must NEVER be used for valid profitability claims.
Kept separately to explain and reproduce supplied audit anchors.
"""
import numpy as np
from numba import njit
# trade columns: bar, side(+1 long/-1 short), kind(0 open,1 add,2 TP,3 ladder,4 account,5 terminal),price,qty,notional,fee,gross,net,basket_id
@njit(cache=True)
def run(a,g=.01,mult=2.,depth=5,tp=.008,base=200.,dd=.12,reset=0,cap=4.,compound=0,stopnext=1,cooldown=1440,record=0,endclose=0):
 n=len(a);q=np.zeros(2);cost=np.zeros(2);last=np.zeros(2);fees_b=np.zeros(2);k=np.zeros(2,np.int64);ids=np.zeros(2,np.int64);pending=np.ones(2,np.int64)
 cash=10000.;prev=10000.;peak=10000.;globalpeak=10000.;maxdd=0.;halt=-1;bid=0;blown=0
 # TPcount,TPnet,laddercount,laddernet,worstbasket,fees,acctcount,skip,acctnet,terminalnet
 stats=np.zeros(12);eq=np.empty(n);logs=[(0.,0.,0.,0.,0.,0.,0.,0.,0.,0.)];logs.pop()
 for i in range(n):
  o,h,l,c=a[i,1],a[i,2],a[i,3],a[i,4]
  if i>=halt and blown==0:
   if halt>=0:
    if reset==1:peak=cash
    pending[:]=1;halt=-1
   for s in range(2):
    if pending[s]==1:
     sign=1.-2.*s;notional=base*(max(prev,0.)/10000. if compound else 1.);f=notional*.0007
     q[s]=notional/o;cost[s]=notional;last[s]=o;k[s]=0;fees_b[s]=f;cash-=f;stats[5]+=f;pending[s]=0;bid+=1;ids[s]=bid
     if record:logs.append((float(i),sign,0.,o,q[s],notional,f,0.,-f,float(bid)))
   # All additions before any take profit. Exposure measured as sum entry notionals.
   for s in range(2):
    sign=1.-2.*s
    for unused in range(depth):
     if q[s]==0. or k[s]>=depth:break
     p=last[s]*(1.-sign*g)
     if not ((l<=p) if s==0 else (h>=p)):break
     notional=base*(max(prev,0.)/10000. if compound else 1.)*mult**(k[s]+1)
     if cost[0]+cost[1]+notional>prev*cap:
      stats[7]+=1;break
     f=notional*.0007;qty=notional/p;q[s]+=qty;cost[s]+=notional;last[s]=p;k[s]+=1;cash-=f;fees_b[s]+=f;stats[5]+=f
     if record:logs.append((float(i),sign,1.,p,qty,notional,f,0.,-f,float(ids[s])))
   for s in range(2):
    if q[s]==0.:continue
    sign=1.-2.*s;p=cost[s]/q[s]*(1.+sign*tp)
    if ((h>=p) if s==0 else (l<=p)):
     notional=q[s]*p;f=notional*.0007;gross=sign*(notional-cost[s]);net=gross-f-fees_b[s];cash+=gross-f;stats[0]+=1;stats[1]+=net;stats[4]=min(stats[4],net);stats[5]+=f
     if record:logs.append((float(i),sign,2.,p,q[s],notional,f,gross,net,float(ids[s])))
     notional=base*(max(prev,0.)/10000. if compound else 1.);f=notional*.0007;q[s]=notional/p;cost[s]=notional;last[s]=p;k[s]=0;fees_b[s]=f;cash-=f;stats[5]+=f;bid+=1;ids[s]=bid
     if record:logs.append((float(i),sign,0.,p,q[s],notional,f,0.,-f,float(bid)))
   for s in range(2):
    sign=1.-2.*s;p=last[s]*(1.-sign*g)
    trigger=(l<=p if s==0 else h>=p)
    if q[s]>0. and k[s]==depth and trigger:
     notional=q[s]*c;f=notional*.0007;gross=sign*(notional-cost[s]);net=gross-f-fees_b[s];cash+=gross-f;stats[2]+=1;stats[3]+=net;stats[4]=min(stats[4],net);stats[5]+=f
     if record:logs.append((float(i),sign,3.,c,q[s],notional,f,gross,net,float(ids[s])))
     q[s]=0.;cost[s]=0.;fees_b[s]=0.;k[s]=0;pending[s]=1
     if stopnext==0:
      notional=base*(max(prev,0.)/10000. if compound else 1.);f=notional*.0007;q[s]=notional/c;cost[s]=notional;last[s]=c;fees_b[s]=f;cash-=f;stats[5]+=f;pending[s]=0;bid+=1;ids[s]=bid
      if record:logs.append((float(i),sign,0.,c,q[s],notional,f,0.,-f,float(bid)))
   equity=cash+(q[0]*c-cost[0])-(q[1]*c-cost[1]);peak=max(peak,equity)
   if equity<=peak*(1.-dd):
    stats[6]+=1
    for s in range(2):
     if q[s]==0.:continue
     sign=1.-2.*s;notional=q[s]*c;f=notional*.0007;gross=sign*(notional-cost[s]);net=gross-f-fees_b[s];cash+=gross-f;stats[8]+=net;stats[4]=min(stats[4],net);stats[5]+=f
     if record:logs.append((float(i),sign,4.,c,q[s],notional,f,gross,net,float(ids[s])))
     q[s]=0.;cost[s]=0.;fees_b[s]=0.;pending[s]=1
    halt=i+cooldown+1
  equity=cash+(q[0]*c-cost[0])-(q[1]*c-cost[1]);eq[i]=equity;prev=equity;globalpeak=max(globalpeak,equity);maxdd=max(maxdd,1.-equity/globalpeak)
  if equity<=0.:blown=1
 # Terminal liquidation charged, last close equity overwritten.
 c=a[-1,4]
 for s in range(2):
  if q[s]>0.:
   stats[10]+=(1.-2.*s)*(q[s]*c-cost[s]);stats[11]+=fees_b[s]
  if q[s]>0. and endclose:
   sign=1.-2.*s;notional=q[s]*c;f=notional*.0007;gross=sign*(notional-cost[s]);net=gross-f-fees_b[s];cash+=gross-f;stats[9]+=net;stats[4]=min(stats[4],net);stats[5]+=f
   if record:logs.append((float(n-1),sign,5.,c,q[s],notional,f,gross,net,float(ids[s])))
 if endclose:eq[-1]=cash
 maxdd=max(maxdd,1.-eq[-1]/globalpeak)
 return eq[-1]/10000.-1.,maxdd,stats,blown,eq,logs

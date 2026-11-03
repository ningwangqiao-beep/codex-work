"""Seeded full-game driver. Bulk runs require separate audit approval."""
import random
from rules.core import deal,legal_discards,waits,score,winning
from simulator.table import Table
from observations.v3_public import observe,features
from rules.v3 import V3Config,VERSION,score_v3

def sample(t,p,seed,index,history):
    opponents=[(p+i)%4 for i in (1,2,3)]
    ws=[]
    for q in opponents:
        w=[]
        if t.active[q]:
            for tile in range(27):
                try:
                    if winning(t.hands[q]+[tile],t.missing[q],len(t.melds[q]),t.melds[q]):w.append(tile)
                except ValueError:pass
        ws.append(w)
    masks=[sum((1<<i) for i,q in enumerate(opponents) if t.active[q] and tile in ws[i]) for tile in range(27)]
    losses=[]
    for tile,mask in enumerate(masks):
        losses.append(sum(score(t.hands[q]+[tile],t.missing[q],t.melds[q],t.config)['payment'] for i,q in enumerate(opponents) if mask&(1<<i)))
    o=observe(t,p,history)
    return dict(game_id=f'game-{seed}',source_group=VERSION,seed=seed,turn_index=index,observer_player=p,style=[['random','shape','pure','defensive'][(seed+q)%4] for q in opponents],policy_parameters='heldout' if seed%10==9 else 'train-v1',game_phase=min(2,int((56-len(t.wall))*3/56)),features=features(o),observation=o,tenpai=[int(bool(w)) for w in ws],waits=[[int(x in w) for x in range(27)] for w in ws],joint_outcome=masks,loss=losses,candidate_mask=[int(x in legal_discards(t.hands[p],t.missing[p])) for x in range(27)],target_active=[int(t.active[q]) for q in opponents])

def play(seed,collect=False,policy=None,policy_seat=0,exchange_offset=1):
    rng=random.Random(seed);hands,wall=deal(seed)
    if exchange_offset not in (1,2,3):raise ValueError("exchange offset")
    # Configurable simultaneous same-suit exchange, then minimum-count missing suit.
    exchanged=[]
    for h in hands:
        suit=max(range(3),key=lambda s:sum(x//9==s for x in h)); chosen=[x for x in h if x//9==suit][:3]
        for x in chosen:h.remove(x)
        exchanged.append(chosen)
    for p in range(4):hands[(p+exchange_offset)%4].extend(exchanged[p])
    missing=[min(range(3),key=lambda s:sum(x//9==s for x in h)) for h in hands]
    hands[0].append(wall.pop());t=Table(hands,missing,wall,config=V3Config(exchange_offset=exchange_offset),strict=True)
    t.exchange_records=[dict(sent=list(exchanged[p]),received=list(exchanged[(p-exchange_offset)%4]),direction=exchange_offset,source_player=(p-exchange_offset)%4) for p in range(4)]
    history=[dict(player=p,action="exchange") for p in range(4)]+[dict(player=p,action="missing_declared") for p in range(4)];rows=[];steps=0;win_events=[]
    while t.phase!='ended':
        steps+=1
        if steps>1000:raise RuntimeError('nonterminating game')
        t.check()
        if t.phase=='advance':
            drawn=t.advance()
            if drawn is not None:history.append(dict(player=t.turn,action='draw'))
            continue
        if t.phase=='discard':
            p=t.turn
            if t.can_win(p):
                win_info=score_v3(t.hands[p],t.missing[p],t.melds[p],t.config,self_draw=True)
                win_events.append(dict(seat=p,kind='self_draw',payer=None,base_fan=win_info['base_fan'],final_fan=win_info['fan'],payment=win_info['payment']))
                t.self_win(p);history.append(dict(player=p,action='self_win'));continue
            if t.wall and not any(x//9==t.missing[p] for x in t.hands[p]):
                hidden=next((x for x in set(t.hands[p]) if t.hands[p].count(x)==4),None)
                added=next((x for x in set(t.hands[p]) if [x]*3 in t.melds[p]),None)
                if hidden is not None:
                    t.concealed_kong(p,hidden);history.append(dict(player=p,action='concealed_kong'));history.append(dict(player=p,action='draw'));continue
                if added is not None:
                    t.added_kong(p,added);history.append(dict(player=p,tile=added,action='added_kong'))
                    winners=[q for q in range(4) if q!=p and t.active[q] and t.can_win(q,added)]
                    for q in winners:
                        info=score(t.hands[q]+[added],t.missing[q],t.melds[q],t.config)
                        win_events.append(dict(seat=q,kind='rob_kong_win',payer=p,base_fan=info['base_fan'],final_fan=info['fan'],payment=info['payment']))
                    t.resolve_added_kong(winners)
                    if not winners:history.append(dict(player=p,action='draw'))
                    continue
            if collect:rows.append(sample(t,p,seed,steps,history))
            choices=legal_discards(t.hands[p],t.missing[p])
            style=(seed+p)%4
            heldout=seed%10==9
            def utility(x):
                remaining=list(t.hands[p]);remaining.remove(x)
                pairs=sum(remaining.count(k)>=2 for k in set(remaining))
                links=sum(abs(a-b) in (1,2) and a//9==b//9 for i,a in enumerate(remaining) for b in remaining[i+1:])
                if style==0:return rng.random()
                if style==1:return pairs*(2.4 if heldout else 3)+links+rng.random()*.1
                if style==2:
                    suit=max(range(3),key=lambda z:sum(k//9==z for k in remaining))
                    return sum(k//9==suit for k in remaining)*4+pairs+links*.2+rng.random()*.1
                visible=sum(z==x for _,z in t.discards)
                return pairs+links*.2+visible*(2.7 if heldout else 2)+rng.random()*.1
            tile=policy(observe(t,p,history),tuple(choices)) if policy is not None and (policy_seat is None or p==policy_seat) else max(choices,key=utility)
            if tile not in choices:raise ValueError('policy returned illegal tile')
            t.discard(p,tile);history.append(dict(player=p,tile=tile,action='discard'));continue
        if t.phase=='claims':
            payer,tile=t.pending;order=[(payer+i)%4 for i in (1,2,3) if t.active[(payer+i)%4]]
            winners=[q for q in order if t.can_win(q,tile)]
            if winners:
                for q in winners:
                    info=score(t.hands[q]+[tile],t.missing[q],t.melds[q],t.config)
                    win_events.append(dict(seat=q,kind='discard_win',payer=payer,base_fan=info['base_fan'],final_fan=info['fan'],payment=info['payment']))
                t.discard_win(winners)
                for q in winners:history.append(dict(player=q,tile=tile,action='discard_win'))
                continue
            claimed=False
            for q in order:
                if any(x//9==t.missing[q] for x in t.hands[q]):continue
                n=t.hands[q].count(tile)
                if n>=2 and tile//9!=t.missing[q] and rng.random()<( .45 if seed%10==9 else .65):
                    kind='exposed_kong' if n==3 and t.wall else 'peng'
                    t.claim(q,kind);history.append(dict(player=q,tile=tile,action=kind));claimed=True;break
            if not claimed:
                drawn=t.advance()
                if drawn is not None:history.append(dict(player=t.turn,action='draw'))
            continue
        raise RuntimeError('unsupported phase '+t.phase)
    t.check()
    ledger=getattr(t,'settlement_ledger',[]);reconstructed=[0]*4
    for entry in ledger:
        reconstructed[entry['payer']]-=entry['amount'];reconstructed[entry['receiver']]+=entry['amount']
    if reconstructed!=t.scores:raise ValueError('ledger reconciliation mismatch')
    return dict(seed=seed,steps=steps,scores=t.scores,rows=rows,ledger=ledger,rule_version=VERSION,win_events=win_events,public_history=history,styles=[['random','shape','pure','defensive'][(seed+q)%4] for q in range(4)])




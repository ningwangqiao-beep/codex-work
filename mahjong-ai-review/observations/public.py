"""Causal public observation: no wall order or opponent concealed tiles."""
def observe(table, observer, history=()):
    if observer not in range(4): raise ValueError('observer')
    return {'observer_player':observer,'observer_hand':list(table.hands[observer]),
      'declared_missing_suits':list(table.missing),'visible_discards':[list(x) for x in table.discards],
      'public_melds':[[([-1]*4 if (p,i) in getattr(table,'concealed_kongs',set()) and p!=observer else list(m)) for i,m in enumerate(ms)] for p,ms in enumerate(table.melds)],
      'public_winning_tiles':[t for _,t,_ in table.wins], 'active':list(table.active),'remaining_wall_information':len(table.wall),
      'turn_index':len(history),'public_action_history':[{k:e[k] for k in ('player','tile','action') if k in e and isinstance(e[k],(int,str))} for e in history],
      'current_player':table.turn,'phase':table.phase}

def features(o):
    # 27 own counts + 27 visible physical tile counts + 12 missing + 4 active +
    # 4 meld counts + wall/time + 4 observer + 4 current player + 44 recent action.
    v=[o['observer_hand'].count(t)/4 for t in range(27)]
    public=[t for _,t in o['visible_discards']]+[t for ms in o['public_melds'] for m in ms for t in m]+o.get('public_winning_tiles',[])
    v += [public.count(t)/4 for t in range(27)]
    v += [float(s==k) for s in o['declared_missing_suits'] for k in range(3)]
    v += list(map(float,o['active']))+[len(ms)/4 for ms in o['public_melds']]
    v += [o['remaining_wall_information']/108,min(o['turn_index'],216)/216]
    v += [float(o['observer_player']==p) for p in range(4)]+[float(o['current_player']==p) for p in range(4)]
    recent=o['public_action_history'][-11:]
    recent=[{}]*(11-len(recent))+recent
    for e in recent:v += [float(e.get('player',-1)==p)*((e.get('tile',-1)+1)/27+{'discard':0,'peng':1,'exposed_kong':2}.get(e.get('action'),3))/4 for p in range(4)]
    assert len(v)==128
    return v


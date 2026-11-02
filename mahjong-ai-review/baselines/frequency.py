"""Streaming training-only smoothed empirical frequencies."""
import json,torch

def fit(paths):
    n=0;t=torch.ones(3);w=torch.ones(3,27);den=torch.ones(3)*2;j=torch.ones(27,8)
    for path in paths:
        with open(path,encoding='utf-8') as f:
            for line in f:
                r=json.loads(line);a=torch.tensor(r['tenpai']).float();t+=a;w+=torch.tensor(r['waits'])*a[:,None];den+=a
                j+=torch.nn.functional.one_hot(torch.tensor(r['joint_outcome']).long(),8);n+=1
    if not n:raise ValueError('Empty baseline training data')
    return {'tenpai':(t/(n+2)).tolist(),'conditional_wait':(w/den[:,None]).tolist(),'joint':(j/(n+8)).tolist(),'n':n}

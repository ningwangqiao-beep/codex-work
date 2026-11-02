"""Validate concrete records and content-bound audit, not just manifest booleans."""
import hashlib, json
from pathlib import Path

def fingerprint(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''): h.update(chunk)
    return h.hexdigest()

def validate_manifest(m):
    for k in ('rules_audit_passed','approval_for_training'):
        if m.get(k) is not True: raise ValueError('Training blocked: '+k)
    for k in ('dataset_version','rules_path','rules_sha256','shards','audit'):
        if not m.get(k): raise ValueError('Missing '+k)
    if fingerprint(m['rules_path'])!=m['rules_sha256']: raise ValueError('Rules fingerprint mismatch')
    hashes={str(p):fingerprint(p) for split in m['shards'].values() for p in split}
    bound=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
    if m['audit'].get('dataset_sha256')!=bound or m['audit'].get('rules_sha256')!=m['rules_sha256'] or m['audit'].get('passed') is not True:
        raise ValueError('Audit does not bind these rules and shards')
    seen_game={}; seen_source={}
    for split in ('train','validation','test'):
        count=0
        for path in m['shards'].get(split,[]):
            with open(path,encoding='utf-8') as f:
                for line in f:
                    r=json.loads(line)
                    for k in ('game_id','source_group','seed','features','tenpai','waits','joint_outcome','loss'):
                        if k not in r: raise ValueError('Missing record '+k)
                    for key, registry in ((str(r['game_id']),seen_game),(str((r['source_group'],r['seed'])),seen_source)):
                        if key in registry and registry[key]!=split: raise ValueError('Cross-split source leakage')
                        registry[key]=split
                    count+=1
        if not count: raise ValueError('Empty '+split)
    return bound

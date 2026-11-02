"""Opt-in audit helpers. No runner hooks or experiment mutations on import."""
import ast
import hashlib
import json
import os
import time
from pathlib import Path

def source_fingerprints(root, entries):
    """Collect static local imports recursively; dynamic imports are reported, not guessed.

    Returns relative POSIX paths and SHA256. Never follows a resolved path outside root.
    External installed distributions are excluded and require a separate environment lock.
    """
    root=Path(root).resolve();pending=[Path(p) for p in entries];seen={};dynamic=[]
    def local(path):
        path=path.resolve();path.relative_to(root);return path
    def candidates(base,parts):
        p=base.joinpath(*parts)
        return [p.with_suffix('.py'),p/'__init__.py']
    while pending:
        raw=pending.pop();p=local(raw if raw.is_absolute() else root/raw)
        if p in seen:continue
        data=p.read_bytes();seen[p]=hashlib.sha256(data).hexdigest()
        tree=ast.parse(data,filename=str(p))
        # Include parent package initializers, which Python executes on import.
        parent=p.parent
        while parent!=root:
            init=parent/'__init__.py'
            if init.is_file():pending.append(init)
            parent=parent.parent
        for node in ast.walk(tree):
            modules=[]
            if isinstance(node,ast.Import):modules=[(root,a.name.split('.')) for a in node.names]
            elif isinstance(node,ast.ImportFrom):
                base=root
                if node.level:
                    base=p.parent
                    for _ in range(node.level-1):base=base.parent
                    local(base)
                parts=node.module.split('.') if node.module else []
                modules=[(base,parts)]+[(base,parts+a.name.split('.')) for a in node.names if a.name!='*']
            elif isinstance(node,ast.Call) and (isinstance(node.func,ast.Name) and node.func.id=='__import__' or isinstance(node.func,ast.Attribute) and node.func.attr=='import_module'):
                dynamic.append({'file':p.relative_to(root).as_posix(),'line':node.lineno})
            for base,parts in modules:
                if not parts:continue
                for candidate in candidates(base,parts):
                    if candidate.is_file():pending.append(local(candidate))
    return {'fingerprints':{p.relative_to(root).as_posix():h for p,h in sorted(seen.items())},'dynamic_imports':dynamic,'coverage':'static local imports only; environment and runtime file reads excluded'}

def append_event(path,event):
    """Append one fsynced JSONL record. Caller must serialize multiple writers.

    Does not repair or truncate existing evidence. A partial final line after power loss
    remains visible; consumers must flag it rather than silently erase it.
    """
    record=dict(event)
    record.setdefault('time_ns',time.time_ns());record.setdefault('pid',os.getpid())
    payload=(json.dumps(record,ensure_ascii=False,sort_keys=True,allow_nan=False)+'\n').encode('utf-8')
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd=os.open(path,os.O_WRONLY|os.O_APPEND|os.O_CREAT,0o600)
    try:
        remaining=memoryview(payload)
        while remaining:
            n=os.write(fd,remaining)
            if n<=0:raise OSError('short event write')
            remaining=remaining[n:]
        os.fsync(fd)
    finally:os.close(fd)
    return record

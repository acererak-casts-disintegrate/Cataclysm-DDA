#!/usr/bin/env python3
"""Add members referencing given ids from source monster/vehicle groups into
destination groups with the same id. Usage: merge_members.py SRC_ROOT DST_ROOT ID..."""
import collections, glob, json, os, sys
OD=collections.OrderedDict
src_root,dst_root=sys.argv[1],sys.argv[2]; want=set(sys.argv[3:])
def load(p): return json.load(open(p),object_pairs_hook=OD)
def scan(root):
    g={}
    for p in glob.glob(os.path.join(root,'**','*.json'),recursive=True):
        try: d=load(p)
        except Exception: continue
        for o in d if isinstance(d,list) else [d]:
            if isinstance(o,dict) and o.get('type') in ('monstergroup','vehicle_group'):
                gid=o.get('id') or o.get('name')
                if isinstance(gid,str): g[(o['type'],gid)]=(p,o)
    return g
src=scan(src_root); dst=scan(dst_root)
def members(o):
    if o['type']=='monstergroup': return o.setdefault('monsters',[])
    return o.setdefault('vehicles',[])
def mid(m):
    if isinstance(m,list): return m[0]
    if isinstance(m,dict): return m.get('monster') or m.get('group') or m.get('vehicle')
files={}
added=[];missing=[]
for k,(p,o) in src.items():
    refs=[m for m in members(o) if mid(m) in want]
    if not refs: continue
    if k not in dst: missing.append((k,[mid(m) for m in refs])); continue
    dp,_=dst[k]
    if dp not in files: files[dp]=load(dp)
    dobj=next(x for x in files[dp] if isinstance(x,dict) and x.get('type')==k[0] and (x.get('id') or x.get('name'))==k[1])
    have={mid(m) for m in members(dobj)}
    for m in refs:
        if mid(m) not in have: members(dobj).append(m); added.append((k[1],mid(m)))
for p,d in files.items():
    json.dump(d,open(p,'w'),indent=2,ensure_ascii=False); open(p,'a').write('\n'); print('TOUCHED',os.path.relpath(p,dst_root))
print('added',added); print('groups only in source',missing)

#!/usr/bin/env python3
"""Small item-group editing helpers for porting. Import or run with a plan file.
plan JSON: {"copy": [[src_group_id, dest_rel_path]], "add": [[dest_group, entry_from_src_group_or_literal]]}
Entries: {"from": SRCGROUP, "id": ITEM_OR_GROUP} copies the source entry; or a literal entry object."""
import collections, glob, json, os, sys
OD=collections.OrderedDict
def load(p):
    with open(p,encoding='utf-8') as f: return json.load(f,object_pairs_hook=OD)
def save(p,d):
    os.makedirs(os.path.dirname(p),exist_ok=True)
    with open(p,'w',encoding='utf-8') as f: json.dump(d,f,indent=2,ensure_ascii=False); f.write('\n')
def groups(root):
    g={}
    for path in glob.glob(os.path.join(root,'**','*.json'),recursive=True):
        try: d=load(path)
        except Exception: continue
        for o in d if isinstance(d,list) else [d]:
            if isinstance(o,dict) and o.get('type')=='item_group' and isinstance(o.get('id'),str):
                g[o['id']]=(os.path.relpath(path,root),o)
    return g
def ents(o):
    for k in ('items','entries'):
        if isinstance(o.get(k),list): return o[k]
    o['entries']=[]; return o['entries']
def eid(e):
    if isinstance(e,str): return e
    if isinstance(e,list) and e: return e[0]
    if isinstance(e,dict): return e.get('item') or e.get('group')
def main():
    src_root,dst_root,plan=sys.argv[1],sys.argv[2],load(sys.argv[3])
    src=groups(src_root); dst=groups(dst_root)
    files={}
    def dfile(rel):
        if rel not in files:
            p=os.path.join(dst_root,rel); files[rel]=load(p) if os.path.exists(p) else []
        return files[rel]
    for gid,rel in plan.get('copy',[]):
        if gid in dst: print('exists',gid); continue
        o=src[gid][1]; dfile(rel).append(o); print('copied',gid,'->',rel)
        dst[gid]=(rel,o)
    for gid,spec in plan.get('add',[]):
        rel,o=dst[gid]
        # operate on the object inside the loaded file copy
        objs=dfile(rel); o=next(x for x in objs if isinstance(x,dict) and x.get('id')==gid and x.get('type')=='item_group')
        if 'from' in spec:
            e=next(x for x in ents(src[spec['from']][1]) if eid(x)==spec['id'])
        else: e=spec
        lst=ents(o)
        if eid(e) in {eid(x) for x in lst}: print('present',gid,eid(e)); continue
        lst.append(e); print('added',eid(e),'->',gid)
    for rel,d in files.items(): save(os.path.join(dst_root,rel),d); print('TOUCHED',rel)
if __name__=='__main__': main()

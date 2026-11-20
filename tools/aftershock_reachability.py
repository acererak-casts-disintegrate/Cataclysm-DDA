#!/usr/bin/env python3
"""Aftershock item reachability audit.

Lists Aftershock items that no spawn source reaches: mapgen for spawnable
overmap terrain, map extras, monster drops/harvests/broken corpses/revert items,
terrain and furniture drops, vehicles, NPC classes, dialogue, EOCs, missions,
item groups, item transforms/default magazines/built-in mods, learnable recipes
and uncrafts.  Profession start items, activation states and damage states are
reported separately.  Run from the repository root.
"""
import json,glob,os,sys,collections
ROOTS=['data/json','data/mods/Aftershock']
ITEM={'GENERIC','AMMO','GUN','GUNMOD','MAGAZINE','TOOL','TOOL_ARMOR','ARMOR','COMESTIBLE','BOOK','BIONIC_ITEM','TOOLMOD','ENGINE','WHEEL','PET_ARMOR','BATTERY','ITEM'}
ents=[]  # (type,id,entry,file)
for r in ROOTS:
    for f in sorted(glob.glob(r+'/**/*.json',recursive=True)):
        try: d=json.load(open(f,encoding='utf-8'))
        except Exception: continue
        for e in (d if isinstance(d,list) else [d]):
            if not isinstance(e,dict) or 'type' not in e: continue
            i=e.get('id') or e.get('abstract') or e.get('nested_mapgen_id') or e.get('update_mapgen_id') or e.get('name')
            ents.append((e['type'],i,e,f))
items={}; isrc={}
groups=collections.defaultdict(list)
for t,i,e,f in ents:
    if t in ITEM:
        for j in (i if isinstance(i,list) else [i]):
            if isinstance(j,str): items[j]=e; isrc[j]=f
    if t=='item_group' and isinstance(i,str): groups[i].append(e)
def chain(i):
    out=[];c=i;n=0
    while c in items and n<12:
        out.append(items[c]); c=items[c].get('copy-from'); n+=1
    return out
def strings(x,skip=('looks_like','copy-from','description','name','//','//2','//3','looks_like','symbol','color','snippet_category','conditional_names')):
    if isinstance(x,str): yield x
    elif isinstance(x,list):
        for y in x: yield from strings(y,skip)
    elif isinstance(x,dict):
        for k,v in x.items():
            if k in skip: continue
            yield from strings(v,skip)
known=set(items)|set(groups)
# overmap terrain that can spawn
oter_flags={}
for t,i,e,f in ents:
    if t=='overmap_terrain':
        for j in (i if isinstance(i,list) else [i]): oter_flags[j]=e.get('flags',[])
def omt_ok(o):
    if isinstance(o,list): return any(omt_ok(x) for x in o)
    if isinstance(o,dict): return True
    return isinstance(o,str) and 'SHOULD_NOT_SPAWN' not in oter_flags.get(o,[])
nested={};palettes={};updates={}
mapgen_roots=[]
for t,i,e,f in ents:
    if t=='mapgen':
        if 'nested_mapgen_id' in e: nested.setdefault(e['nested_mapgen_id'],[]).append(e)
        elif 'update_mapgen_id' in e: updates.setdefault(e['update_mapgen_id'],[]).append(e)
        elif 'om_terrain' in e and omt_ok(e['om_terrain']): mapgen_roots.append(e)
    if t=='palette': palettes.setdefault(i,[]).append(e)
R=set(); prof=set(); why={}
work=[]
def mark(x,reason):
    if x in R: return
    R.add(x); why[x]=reason; work.append(x)
def scan(obj,reason):
    for s in strings(obj):
        if s in known or s in nested or s in palettes or s in updates: mark(s,reason)
for e in mapgen_roots: scan(e,'mapgen')
for t,i,e,f in ents:
    if t in ('map_extra','monster','MONSTER','harvest','terrain','furniture','vehicle','npc_class','talk_topic','effect_on_condition','mission_definition','construction','trap','npc','gate','shopkeeper_consumption_rates','shopkeeper_blacklist','vehicle_group','item_action','monster_attack','SPELL','spell','bionic','mutation','martial_art','achievement','overmap_special','city_building','field_type','faction','start_location','event_transformation','ammo_effect','relic_procgen_data','jmath_function'):
        scan(e,t)
    if t in ('profession','scenario'):
        for s in strings(e):
            if s in known: prof.add(s)
# monsters: broken corpse and revert items
for t,i,e,f in ents:
    if t in ('monster','MONSTER') and isinstance(i,str):
        df=e.get('death_function') or {}
        ct=df.get('corpse_type') if isinstance(df,dict) else None
        base=i[4:] if i.startswith('mon_') else i
        if ct=='BROKEN' and 'broken_'+base in known: mark('broken_'+base,'broken:'+i)
        if e.get('revert_to_itype') in known: mark(e['revert_to_itype'],'revert:'+i)
# monsters copy-from inheritance for BROKEN
mons={i:e for t,i,e,f in ents if t in ('monster','MONSTER') and isinstance(i,str)}
def mres(i,k,n=0):
    e=mons.get(i)
    while e and n<10:
        if k in e: return e[k]
        e=mons.get(e.get('copy-from')); n+=1
for i in mons:
    df=mres(i,'death_function') or {}
    ct=df.get('corpse_type') if isinstance(df,dict) else None
    base=i[4:] if i.startswith('mon_') else i
    if ct=='BROKEN' and 'broken_'+base in known: mark('broken_'+base,'broken:'+i)
    rv=mres(i,'revert_to_itype')
    if rv in known: mark(rv,'revert:'+i)
# recipes
learn_books=set(); recipes=[]
rid={}
for t,i,e,f in ents:
    if t in ('recipe','uncraft'):
        recipes.append(e)
        r=e.get('result') or e.get('id') or e.get('abstract'); k=(r+'_'+e['id_suffix']) if (e.get('id_suffix') and isinstance(r,str)) else r
        if e.get('id'): rid[(t,e['id'])]=e
        if e.get('abstract'): rid[(t,e['abstract'])]=e
        if isinstance(k,str): rid[(t,k)]=e
def rget(r,key,n=0):
    while r is not None and n<10:
        if key in r: return r[key]
        r=rid.get((r['type'],r.get('copy-from'))); n+=1
def learnable(r):
    if rget(r,'never_learn') or rget(r,'obsolete'): return False
    if rget(r,'autolearn') or rget(r,'decomp_learn') is not None: return True
    bl=rget(r,'book_learn')
    if bl: return 'BOOK'
    return 'PROF'
changed=True
while work or changed:
    while work:
        x=work.pop()
        if x in items:
            for c in chain(x):
                for k in ('use_action','revert_to','countdown_action','drop_action','built_in_mods','default_mods','pocket_data','tick_action','transform_into','ammo_data','qualities_by_ammo','casing','non_functional','damaged_item','destroyed_item'):
                    if k in c: scan(c[k],'item:'+x)
        for g in groups.get(x,[]): scan(g,'group:'+x)
        for m in nested.get(x,[])+palettes.get(x,[])+updates.get(x,[]): scan(m,'mapgen:'+x)
    changed=False
    for r in recipes:
        res=r.get('result')
        if r['type']=='uncraft' or r.get('reversible'):
            if res in R:
                before=len(R); scan(rget(r,'components') or [],'uncraft:'+str(res));
                if len(R)>before: changed=True
        if r['type']=='recipe' and res in known and res not in R:
            l=learnable(r)
            books=rget(r,'book_learn') or {}
            bks=list(books.keys()) if isinstance(books,dict) else [b[0] if isinstance(b,list) else b for b in books]
            if l is True or (l=='BOOK' and any(b in R for b in bks)):
                mark(res,'recipe'); changed=True
                for bp in r.get('byproducts',[]): scan(bp,'byproduct')
# report AS items
afs=[i for i,f in isrc.items() if f.startswith('data/mods/Aftershock') and items[i].get('id')]
def flags(i):
    fl=set()
    for c in chain(i): fl|=set(c.get('flags',[]))
    return fl
out=collections.defaultdict(list)
for i in sorted(afs):
    if i in R: continue
    f=isrc[i]; fl=flags(i)
    if 'obsolete' in f: cat='obsolete'
    elif fl & {'PSEUDO','NO_DROP','BIONIC_WEAPON','INTEGRATED','ZERO_WEIGHT','NO_UNWIELD','NO_SALVAGE_SPAWN'} or '/mutations/' in f: cat='fake/integrated'
    elif 'CORPSE' in fl: cat='corpse'
    elif any(c.get('id') in R for c in chain(i)[1:]) and (i.endswith(('_on','_act','_music','_flashlight','_holosuite','_lit')) or i.startswith('collapsed_')): cat='state variant'
    elif i.startswith(('damaged_','destroyed_')) and any(x in R for x in (i.replace('damaged_','').replace('destroyed_',''),)): cat='damage state'
    elif i in prof: cat='profession-only'
    else: cat='UNREACHABLE'
    nm=chain(i)[0].get('name'); nm=nm.get('str',nm.get('str_sp')) if isinstance(nm,dict) else nm
    out[cat].append((i,items[i]['type'],f.replace('data/mods/Aftershock/',''),nm))
for cat in ('UNREACHABLE','profession-only','state variant','damage state','fake/integrated','corpse','obsolete'):
    print(f'== {cat}: {len(out[cat])}')
    for row in out[cat]: print('  ','\t'.join(map(str,row)))
if len(sys.argv) > 1:
    json.dump({k: [r[0] for r in v] for k, v in out.items()}, open(sys.argv[1], 'w'), indent=1)

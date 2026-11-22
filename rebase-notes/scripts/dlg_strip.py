#!/usr/bin/env python3
"""dlg_strip.py FILE [-i ID ...] [-I IDREGEX ...] [-r REGEX ...]
-i / -I : drop top-level objects whose id equals / matches (list ids are filtered).
-r      : drop any element of a "responses" list whose JSON text matches; collapse
          a conditional dynamic_line {cond..., yes, no} whose condition matches to its
          "no" branch; drop matching elements of "topic" id lists and "effect" lists."""
import json, re, sys, collections
OD = collections.OrderedDict
args = sys.argv[1:]; p = args.pop(0); ids, idrx, rx, mode = set(), [], [], None
for a in args:
    if a in ('-i', '-I', '-r'): mode = a; continue
    {'-i': lambda v: ids.add(v), '-I': lambda v: idrx.append(re.compile(v)), '-r': lambda v: rx.append(re.compile(v))}[mode](a)
d = json.load(open(p, encoding='utf-8'), object_pairs_hook=OD)
if isinstance(d, dict): d = [d]
gone, cut, coll = [], [], 0
def hit(x): t = json.dumps(x, ensure_ascii=False); return bool(rx) and any(r.search(t) for r in rx)
def idhit(i): return i in ids or any(r.search(i) for r in idrx)
def walk(x):
    global coll
    if isinstance(x, dict):
        for k, v in list(x.items()):
            if k in ('responses', 'effect', 'speaker_effect', 'true_eocs', 'false_eocs') and isinstance(v, list):
                keep = []
                for e in v:
                    if hit(e): cut.append(e.get('text', json.dumps(e)[:80]) if isinstance(e, dict) else str(e)[:80])
                    else: keep.append(e)
                x[k] = keep
            if k == 'dynamic_line':
                while isinstance(x[k], dict) and 'no' in x[k] and 'yes' in x[k] and hit({a: b for a, b in x[k].items() if a not in ('yes', 'no')}):
                    x[k] = x[k]['no']; coll += 1
            walk(x[k])
    elif isinstance(x, list):
        for e in x: walk(e)
keep = []
for o in d:
    oid = o.get('id') if isinstance(o, dict) else None
    if isinstance(oid, str) and idhit(oid): gone.append(oid); continue
    if isinstance(oid, list):
        o['id'] = [i for i in oid if not idhit(i)]
        gone += [i for i in oid if idhit(i)]
        if not o['id']: continue
        if len(o['id']) == 1: o['id'] = o['id'][0]
    walk(o); keep.append(o)
json.dump(keep, open(p, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(p, 'a').write('\n')
print(p, '\n  objects removed:', gone, '\n  missing:', sorted(i for i in ids if i not in gone), '\n  dynamic lines collapsed:', coll, '\n  cut:', cut)

#!/usr/bin/env python3
"""rm_objs.py FILE ID... : drop top-level objects whose id (or abstract) is listed."""
import json, sys, collections
p = sys.argv[1]; ids = set(sys.argv[2:])
d = json.load(open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
keep, gone = [], []
for o in d:
    oid = o.get('id', o.get('abstract')) if isinstance(o, dict) else None
    if isinstance(oid, str) and oid in ids: gone.append(oid); continue
    keep.append(o)
json.dump(keep, open(p, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
open(p, 'a').write('\n')
print(p, 'removed', gone, 'missing', sorted(ids - set(gone)))

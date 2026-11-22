#!/usr/bin/env python3
"""removed_ids.py COMMIT FILE : ids of top-level objects present in COMMIT^:FILE but not COMMIT:FILE."""
import json, subprocess, sys
c, f = sys.argv[1], sys.argv[2]
def ids(rev):
    try: d = json.loads(subprocess.check_output(['git', 'show', f'{rev}:{f}'], stderr=subprocess.DEVNULL))
    except subprocess.CalledProcessError: return set()
    return {o.get('id', o.get('abstract')) for o in d if isinstance(o, dict) and isinstance(o.get('id', o.get('abstract')), str)}
print(' '.join(sorted(ids(c + '^') - ids(c))))

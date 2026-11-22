#!/usr/bin/env python3
"""Restore a set of items from a 0.H-format tree into a 0.I tree.

For each requested id that is not live in the destination:
  * copies its definition (and any copy-from parents the destination lacks)
    from the source, converting the item type and integer prices to 0.I form,
    into the same relative file (created if missing);
  * removes the destination's MIGRATION entries and obsolete definitions for it;
  * re-adds it to destination item groups that exist in both trees and
    referenced it in the source;
  * copies source recipes and uncrafts that produce it, if the destination
    lacks them.
Everything else in the source that references the ids is reported.

Usage: restore_items.py SRC_JSON_ROOT DEST_JSON_ROOT ID [ID...]
       (ids may also be given one per line on stdin with '-')
Writes the list of touched files to stdout's last lines ("TOUCHED path").
"""
import collections
import glob
import json
import os
import re
import sys

ITEM_TYPES = {
    'GUN': ['GUN'], 'TOOL': ['TOOL'], 'GENERIC': [], 'AMMO': ['AMMO'], 'MAGAZINE': ['MAGAZINE'],
    'ARMOR': ['ARMOR'], 'COMESTIBLE': ['COMESTIBLE'], 'BIONIC_ITEM': ['BIONIC_ITEM'],
    'TOOL_ARMOR': ['TOOL', 'ARMOR'], 'GUNMOD': ['GUNMOD'], 'TOOLMOD': ['TOOLMOD'], 'BOOK': ['BOOK'],
    'PET_ARMOR': ['PET_ARMOR'], 'ENGINE': ['ENGINE'], 'WHEEL': ['WHEEL'], 'BATTERY': ['BATTERY'],
}
OD = collections.OrderedDict


def load(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f, object_pairs_hook=OD)
    except (OSError, ValueError):
        return None


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def ids_of(obj):
    for key in ('id', 'abstract'):
        val = obj.get(key)
        if isinstance(val, str):
            yield val
        elif isinstance(val, list):
            yield from (v for v in val if isinstance(v, str))


def is_item(obj):
    return obj.get('type') in ITEM_TYPES or obj.get('type') == 'ITEM'


# 0.H nested item slots -> (0.I subtype, {old key: new top-level key})
NESTED_SLOTS = {
    'relic_data': ('ARTIFACT', {}),
    'seed_data': ('SEED', {}),
    'brewable': ('BREWABLE', {'time': 'brew_time', 'results': 'brew_results'}),
    'compostable': ('COMPOSTABLE', {'time': 'compost_time', 'results': 'compost_results'}),
    'milling': ('MILLING', {}),
    'armor_data': ('ARMOR', {}),
    'pet_armor_data': ('PET_ARMOR', {}),
}


def convert(obj):
    """0.H item object -> 0.I form.

    Item type becomes ITEM with subtypes; integer prices become cent strings;
    a gunmod's nested gun_data is flattened and the item gains the GUN
    subtype; a gun's legacy "magazines" list is dropped when it already has
    magazine-well pockets (0.I reads only the pockets); a tool's "ammo"
    becomes "tool_ammo"; nested slots (relic_data, seed_data, brewable,
    compostable, milling, armor_data) are flattened behind their subtype.
    """
    new = OD()
    subs = None
    for key, val in obj.items():
        if key == 'type' and val in ITEM_TYPES:
            new['type'] = 'ITEM'
            subs = list(ITEM_TYPES[val])
            if val == 'GUNMOD' and 'gun_data' in obj:
                subs = ['GUN', 'GUNMOD']
            new['subtypes'] = subs
        elif key in ('price', 'price_postapoc') and isinstance(val, int):
            new[key] = f'{val} cent'
        elif key == 'gun_data' and isinstance(val, dict):
            for gkey, gval in val.items():
                if gkey == 'ammo' and isinstance(gval, str):
                    gval = [gval]
                if gkey in ('extend', 'delete', 'relative', 'proportional') and isinstance(gval, dict):
                    merged = new.setdefault(gkey, OD())
                    for mk, mv in gval.items():
                        merged.setdefault(mk, mv)
                    continue
                new.setdefault(gkey, gval)
            if subs is not None and 'GUN' not in subs:
                subs.append('GUN')
        elif key == 'magazines' and obj.get('pocket_data'):
            continue
        elif key == 'ammo' and obj.get('type') in ('TOOL', 'TOOL_ARMOR'):
            new['tool_ammo'] = val  # 0.I renamed a tool's ammo field
        elif key in NESTED_SLOTS and isinstance(val, dict):
            sub, renames = NESTED_SLOTS[key]
            for rkey, rval in val.items():
                new.setdefault(renames.get(rkey, rkey), rval)
            if subs is None:
                subs = new.setdefault('subtypes', [])
            if sub not in subs:
                subs.append(sub)
        elif key in ('skill', 'fun') and obj.get('type') == 'BOOK':
            new['read_' + key] = val
        else:
            new[key] = val
    if 'subtypes' in new and not new['subtypes']:
        del new['subtypes']
    elif 'subtypes' in new and 'type' in new:
        # keep "subtypes" right after "type"
        ordered = OD()
        for k, v in new.items():
            if k == 'subtypes':
                continue
            ordered[k] = v
            if k == 'type':
                ordered['subtypes'] = new['subtypes']
        new = ordered
    return new


def index(root):
    files = {}
    for path in glob.glob(os.path.join(root, '**', '*.json'), recursive=True):
        data = load(path)
        if data is None:
            continue
        files[os.path.relpath(path, root)] = data if isinstance(data, list) else [data]
    return files


def main():
    src_root, dst_root = sys.argv[1], sys.argv[2]
    wanted = set(sys.argv[3:])
    if '-' in wanted:
        wanted.discard('-')
        wanted |= {l.strip() for l in sys.stdin if l.strip()}
    src = index(src_root)
    dst = index(dst_root)
    touched = set()

    src_items = {}
    for rel, objs in src.items():
        if 'obsolet' in rel:
            continue
        for o in objs:
            if isinstance(o, dict) and is_item(o):
                for i in ids_of(o):
                    src_items[i] = (rel, o)
    dst_live = set()
    for rel, objs in dst.items():
        if 'obsolet' in rel:
            continue
        for o in objs:
            if isinstance(o, dict) and is_item(o):
                dst_live.update(ids_of(o))

    # 1. definitions (+ copy-from parents)
    todo = sorted(i for i in wanted if i not in dst_live)
    missing_src = [i for i in todo if i not in src_items]
    queue = [i for i in todo if i in src_items]
    added = []
    seen = set()
    while queue:
        i = queue.pop(0)
        if i in seen or i in dst_live:
            continue
        seen.add(i)
        rel, obj = src_items[i]
        parent = obj.get('copy-from')
        if parent and parent not in dst_live and parent in src_items and parent not in seen:
            queue.append(parent)
        dst.setdefault(rel, []).append(convert(obj))
        touched.add(rel)
        added.append(i)
    restored = set(added)

    # 2. migrations and obsolete definitions
    removed_mig, removed_obs = [], []
    for rel, objs in dst.items():
        keep = []
        changed = False
        for o in objs:
            if not isinstance(o, dict):
                keep.append(o)
                continue
            oid = o.get('id')
            if o.get('type') == 'MIGRATION':
                ids = oid if isinstance(oid, list) else [oid]
                hit = [x for x in ids if x in wanted]
                if hit:
                    removed_mig += hit
                    changed = True
                    rest = [x for x in ids if x not in wanted]
                    if not rest:
                        continue
                    o['id'] = rest if isinstance(oid, list) else rest[0]
            elif 'obsolet' in rel and is_item(o) and set(ids_of(o)) & wanted:
                removed_obs += sorted(set(ids_of(o)) & wanted)
                changed = True
                continue
            keep.append(o)
        if changed:
            dst[rel] = keep
            touched.add(rel)

    # 3. item groups present in both trees
    dst_groups = {}
    for rel, objs in dst.items():
        for o in objs:
            if isinstance(o, dict) and o.get('type') == 'item_group' and isinstance(o.get('id'), str):
                dst_groups[o['id']] = (rel, o)

    def entries(group):
        for key in ('items', 'entries'):
            if isinstance(group.get(key), list):
                return key, group[key]
        return None, None

    def entry_id(e):
        if isinstance(e, str):
            return e
        if isinstance(e, list) and e:
            return e[0]
        if isinstance(e, dict):
            return e.get('item')
        return None

    group_adds, group_missing = [], []
    for rel, objs in src.items():
        for o in objs:
            if not (isinstance(o, dict) and o.get('type') == 'item_group'):
                continue
            key, ents = entries(o)
            if not ents:
                continue
            refs = [e for e in ents if entry_id(e) in wanted]
            if not refs:
                continue
            gid = o.get('id')
            if gid not in dst_groups:
                group_missing.append((gid, [entry_id(e) for e in refs]))
                continue
            drel, dgroup = dst_groups[gid]
            dkey, dents = entries(dgroup)
            if dents is None:
                dkey, dents = (key, [])
                dgroup[dkey] = dents
            have = {entry_id(e) for e in dents}
            for e in refs:
                if entry_id(e) not in have:
                    dents.append(e)
                    group_adds.append((gid, entry_id(e)))
                    touched.add(drel)

    # 4. recipes and uncrafts producing restored ids
    def recipe_key(o):
        return (o.get('type'), o.get('result'), o.get('id_suffix'))

    dst_recipes = set()
    for rel, objs in dst.items():
        for o in objs:
            if isinstance(o, dict) and o.get('type') in ('recipe', 'uncraft'):
                dst_recipes.add(recipe_key(o))
    recipe_adds = []
    for rel, objs in src.items():
        for o in objs:
            if isinstance(o, dict) and o.get('type') in ('recipe', 'uncraft') and o.get('result') in wanted:
                if recipe_key(o) not in dst_recipes:
                    dst.setdefault(rel, []).append(o)
                    dst_recipes.add(recipe_key(o))
                    recipe_adds.append(recipe_key(o))
                    touched.add(rel)

    # 5. report other source references
    others = collections.defaultdict(set)
    pat = re.compile(r'"(%s)"' % '|'.join(re.escape(i) for i in sorted(wanted, key=len, reverse=True))) if wanted else None
    for rel, objs in src.items():
        if 'obsolet' in rel:
            continue
        for o in objs:
            if not isinstance(o, dict) or is_item(o) and set(ids_of(o)) & wanted:
                continue
            if o.get('type') in ('item_group', 'recipe', 'uncraft', 'MIGRATION'):
                continue
            text = json.dumps(o)
            for m in set(pat.findall(text)) if pat else ():
                others[m].add(f"{rel}:{o.get('type')}:{next(ids_of(o), o.get('result', '?'))}")

    for rel in sorted(touched):
        save(os.path.join(dst_root, rel), dst[rel])

    print(f'definitions added: {len(added)} {added}')
    print(f'requested but already live in destination: {sorted(wanted & dst_live)}')
    print(f'requested but not found in source: {missing_src}')
    print(f'migrations removed: {sorted(set(removed_mig))}')
    print(f'obsolete definitions removed: {sorted(set(removed_obs))}')
    print(f'item group entries added: {len(group_adds)}')
    for gid, refs in group_missing:
        print(f'  group only in source: {gid} -> {refs}')
    print(f'recipes/uncrafts added: {recipe_adds}')
    print('other source references (check by hand):')
    for i in sorted(others):
        for ref in sorted(others[i])[:12]:
            print(f'  {i}: {ref}')
    for rel in sorted(touched):
        print(f'TOUCHED {rel}')


if __name__ == '__main__':
    main()

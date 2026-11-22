#!/usr/bin/env python3
"""Aftershock-specific fixes applied after convert_mod_0I.py.

Usage: af_fixes.py AFTERSHOCK_DIR UPSTREAM_0I_AFTERSHOCK_DIR
"""
import collections
import glob
import json
import os
import sys

OD = collections.OrderedDict
A, UP = sys.argv[1], sys.argv[2]
DT = {'BASH': 'bash', 'CUT': 'cut', 'STAB': 'stab', 'BULLET': 'bullet', 'COLD': 'cold',
      'HEAT': 'heat', 'ELEC': 'electric', 'ACID': 'acid', 'BIO': 'biological'}


def ld(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f, object_pairs_hook=OD)


def sv(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def objs(data):
    return data if isinstance(data, list) else [data]


def upstream_index():
    idx = {}
    for path in glob.glob(os.path.join(UP, '**', '*.json'), recursive=True):
        try:
            data = ld(path)
        except ValueError:
            continue
        for o in objs(data):
            if isinstance(o, dict):
                i = o.get('id')
                for x in (i if isinstance(i, list) else [i]):
                    if isinstance(x, str):
                        idx[(o.get('type'), x)] = o
    return idx


UPI = upstream_index()


def fix_enchant(e):
    """ARMOR_<T>/ITEM_DAMAGE_<T> values -> incoming_damage_mod/melee_damage_bonus."""
    if not isinstance(e.get('values'), list):
        return False
    keep, changed = [], False
    for v in e['values']:
        n = v.get('value') if isinstance(v, dict) else None
        if not isinstance(n, str):
            keep.append(v)
            continue
        target = None
        if n.startswith('ARMOR_') and n[6:] in DT:
            target = ('incoming_damage_mod', DT[n[6:]])
        elif n.startswith('ITEM_DAMAGE_') and n[12:] in DT:
            target = ('melee_damage_bonus', DT[n[12:]])
        if target:
            ent = OD([('type', target[1])])
            for k in ('add', 'multiply'):
                if k in v:
                    ent[k] = v[k]
            e.setdefault(target[0], []).append(ent)
            changed = True
        elif n == 'MOTION_VISION_RANGE':
            up = UPI.get(('enchantment', e.get('id')))
            e['special_vision'] = up['special_vision']
            changed = True
        else:
            keep.append(v)
    if changed:
        if keep:
            e['values'] = keep
        else:
            del e['values']
    return changed


def walk(x, fn):
    hit = False
    if isinstance(x, dict):
        hit |= fn(x)
        for v in x.values():
            hit |= walk(v, fn)
    elif isinstance(x, list):
        for v in x:
            hit |= walk(v, fn)
    return hit


def generic(o):
    changed = False
    if isinstance(o.get('keg_capacity'), int):
        o['keg_capacity'] = f"{o['keg_capacity'] * 250} ml"
        changed = True
    if '//~' in o and o.get('type') == 'effect_type' and isinstance(o.get('desc'), list) \
            and o['desc'] and isinstance(o['desc'][0], str):
        o['desc'][0] = OD([('//~', o.pop('//~')), ('str', o['desc'][0])])
        changed = True
    if o.get('type') == 'overmap_terrain' and isinstance(o.get('see_cost'), int):
        ids = o['id'] if isinstance(o['id'], list) else [o['id']]
        vals = {UPI.get(('overmap_terrain', i), {}).get('see_cost') for i in ids} - {None}
        if len(vals) == 1:
            o['see_cost'] = vals.pop()
            changed = True
        else:
            print('see_cost unresolved', ids[0], o['see_cost'])
    return changed


for path in glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    data = ld(path)
    if walk(data, lambda o: generic(o) | fix_enchant(o)):
        sv(path, data)
        print('fixed', os.path.relpath(path, A))

# Core item groups renamed or removed in 0.I
p = os.path.join(A, 'itemgroups/item_groups.json')
d = [o for o in ld(p) if o.get('id') != 'spider']   # no core "spider" group exists
for o in d:
    if o.get('id') == 'oven':
        o.clear()
        o.update(OD([('id', 'SUS_oven'), ('type', 'item_group'), ('copy-from', 'SUS_oven'),
                     ('subtype', 'collection'), ('extend', OD([('items', [['afs_atompot', 3]])]))]))
sv(p, d)
p = os.path.join(A, 'itemgroups/earth_spawns.json')
d = ld(p)
for o in d:
    if o.get('id') == 'mags_shotgun_rare':
        o['id'] = o['copy-from'] = 'common_magazines_restricted_12'
    if o.get('id') == 'military':
        o['id'] = o['copy-from'] = 'mil_armor'
        o.pop('subtype', None)
        if 'entries' in o['extend']:
            o['extend']['items'] = o['extend'].pop('entries')
sv(p, d)
p = os.path.join(A, 'itemgroups/weapons/weapon_expansion_groups.json')
sv(p, [o for o in ld(p) if o.get('id') != 'mags_shotgun_rare'])

# Monster fields that 0.I assigns strictly: drop values equal to the parent's.
STRICT_MON_KEYS = ('luminance',)
core_mon = {}
for path in glob.glob(os.path.join(A, '..', '..', 'json', '**', '*.json'), recursive=True) + \
        glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    try:
        data = ld(path)
    except ValueError:
        continue
    for o in objs(data):
        if isinstance(o, dict) and o.get('type') == 'MONSTER':
            key = o.get('id', o.get('abstract'))
            if isinstance(key, str):
                core_mon[key] = o


def inherited(mid, key, depth=0):
    o = core_mon.get(mid)
    if not o or depth > 10:
        return None
    if key in o:
        return o[key]
    return inherited(o.get('copy-from'), key, depth + 1) if o.get('copy-from') else None


for path in glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    data = ld(path)
    changed = False
    for o in objs(data):
        if isinstance(o, dict) and o.get('type') == 'MONSTER' and o.get('copy-from'):
            for k in STRICT_MON_KEYS:
                if k in o and inherited(o['copy-from'], k) == o[k]:
                    del o[k]
                    changed = True
    if changed:
        sv(path, data)
        print('dropped inherited monster fields in', os.path.relpath(path, A))

# 0.H let the later of two same-source recipes win; 0.I rejects the pair.
p = os.path.join(A, 'recipes/recipes.json')
d = ld(p)
plut = [n for n, o in enumerate(d) if o.get('type') == 'recipe' and o.get('result') == 'plut_cell' and 'id_suffix' not in o]
if len(plut) > 1:
    for n in reversed(plut[:-1]):
        del d[n]
    sv(p, d)
    print('dropped shadowed plut_cell recipe')

# 0.H gun/ammo/mag tiers that 0.I folded into its "common" groups.
RETARGET = {
    'guns_pistol_rare': ('guns_pistol_common', {'afs_seyfert_84K': 3}),
    'guns_pistol_rare_display': ('guns_pistol_common_display', {'afs_seyfert_84K': 3}),
    'guns_pistol_obscure': (None, None),
    'guns_rifle_rare': ('guns_rifle_common', None),
    'guns_rifle_rare_display': ('guns_rifle_common_display', None),
    'mags_pistol_rare': ('mags_common', None),
    'mags_rifle_rare': ('mags_common', None),
    'ammo_pistol_rare': ('ammo_common_boxed', None),
    'ammo_rifle_rare': ('ammo_common_boxed', None),
    'ammo_shotgun_rare': ('ammo_common_boxed', None),
    'ammo_pistol_common': ('ammo_common_boxed', None),
    'ammo_rifle_common': ('ammo_common_boxed', None),
}
for rel in ('itemgroups/weapons/weapon_expansion_groups.json', 'itemgroups/weapons/energy_gun_groups.json'):
    p = os.path.join(A, rel)
    d = ld(p)
    out = []
    for o in d:
        if o.get('type') == 'item_group' and o.get('copy-from') in RETARGET and o.get('id') == o.get('copy-from'):
            target, probs = RETARGET[o['copy-from']]
            if target is None:
                continue
            o['id'] = o['copy-from'] = target
            ext = o['extend']
            ents = ext.pop('entries', None) or ext.pop('items', [])
            for e in ents:
                if isinstance(e, dict) and probs and e.get('item') in probs:
                    e['prob'] = probs[e['item']]
            ext['items'] = ents
            # distribution parents need the same subtype on the extending object
            o.pop('subtype', None)
        out.append(o)
    sv(p, out)

# copy-from targets that 0.I removed: follow its item migrations; redhawk is now a sw629 variant
CORE = os.path.join(A, '..', '..', 'json')
migr, live = {}, set()
for path in glob.glob(os.path.join(CORE, '**', '*.json'), recursive=True) + \
        glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    try:
        data = ld(path)
    except ValueError:
        continue
    for o in objs(data):
        if not isinstance(o, dict):
            continue
        i = o.get('id', o.get('abstract'))
        ids = i if isinstance(i, list) else [i]
        if o.get('type') == 'MIGRATION':
            for x in ids:
                migr[x] = o.get('replace')
        elif o.get('type') == 'ITEM':
            live.update(x for x in ids if isinstance(x, str))
migr['ruger_redhawk'] = 'sw629'
for path in glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    data = ld(path)
    changed = False
    for o in objs(data):
        if isinstance(o, dict) and o.get('type') == 'ITEM' and o.get('copy-from') and o['copy-from'] not in live:
            new = migr.get(o['copy-from'])
            if new:
                print('copy-from', o.get('id'), o['copy-from'], '->', new)
                o['copy-from'] = new
                changed = True
            else:
                print('copy-from unresolved', o.get('id'), o['copy-from'])
    if changed:
        sv(path, data)

# armour weight_capacity_bonus -> worn CARRY_WEIGHT enchantment (keeping inherited passive effects)
items = {}
for path in glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    for o in objs(ld(path)):
        if isinstance(o, dict) and o.get('type') == 'ITEM' and isinstance(o.get('id'), str):
            items[o['id']] = o
for path in glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    data = ld(path)
    changed = False
    for o in objs(data):
        if isinstance(o, dict) and 'weight_capacity_bonus' in o:
            w = o.pop('weight_capacity_bonus')
            grams = int(float(w.split()[0]) * (1000 if w.split()[1] == 'kg' else 1))
            pe = o.get('passive_effects')
            if pe is None:
                parent = items.get(o.get('copy-from'), {})
                pe = list(parent.get('passive_effects', []))
            pe.append(OD([('has', 'WORN'), ('condition', 'ALWAYS'),
                          ('values', [OD([('value', 'CARRY_WEIGHT'), ('add', grams)])])]))
            o['passive_effects'] = pe
            if 'ARTIFACT' not in o.setdefault('subtypes', []):
                o['subtypes'].append('ARTIFACT')
            changed = True
            print('carry bonus ->', o.get('id'), grams)
    if changed:
        sv(path, data)

# terrain/furniture ids 0.I dropped (0.H aliases and renamed ids)
TER_FURN = {
    'f_floor_canvas': 'f_punching_bag', 'f_small_satelitte_dish': 'f_small_satellite_dish',
    't_chainfence_h': 't_chainfence', 't_chainfence_v': 't_chainfence', 't_fence_h': 't_fence',
    't_gutter_east': 't_gutter', 't_gutter_north': 't_gutter', 't_gutter_south': 't_gutter',
    't_gutter_west': 't_gutter', 't_hole': 't_open_air',
    't_wall_clearcrete_h_alarm': 't_wall_clearcrete_alarm', 't_wall_clearcrete_v_alarm': 't_wall_clearcrete_alarm',
}
for path in glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    new = text
    for old, rep in TER_FURN.items():
        new = new.replace(f'"{old}"', f'"{rep}"')
    data = json.loads(new, object_pairs_hook=OD)
    for o in objs(data):
        if isinstance(o, dict) and o.get('type') in ('terrain', 'furniture') and 'alias' in o:
            del o['alias']
    out = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
    if out != json.dumps(ld(path), indent=2, ensure_ascii=False) + '\n':
        sv(path, data)
        print('ter/furn ids', os.path.relpath(path, A))
# t_atm became furniture on concrete
p = os.path.join(A, 'maps/mapgen/s_gas.json')
d = ld(p)
for o in d:
    ob = o.get('object', {})
    if ob.get('terrain', {}).get('T') == 't_atm':
        ob['terrain']['T'] = 't_thconc_floor'
        ob.setdefault('furniture', OD())['T'] = 'f_atm_off'
sv(p, d)

# 0.I folded house_09b (bionic decoy basement) into house_09
p = os.path.join(A, 'maps/city_buildings.json')
sv(p, [o for o in ld(p) if o.get('id') != 'house_09b'])
p = os.path.join(A, 'region_settings.json')
d = ld(p)
def fold_house(x):
    if isinstance(x, dict):
        if 'house_09b' in x and isinstance(x['house_09b'], int):
            x['house_09'] = x.get('house_09', 0) + x.pop('house_09b')
        for v in x.values():
            fold_house(v)
    elif isinstance(x, list):
        for v in x:
            fold_house(v)
fold_house(d)
sv(p, d)
# office_mess and SUPER_FANCY are gone in 0.I
for path in glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    new = text.replace('"group": "office_mess"', '"group": "SUS_office_desk"').replace('"item": "office_mess"', '"item": "SUS_office_desk"')
    if new != text:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        print('office_mess/SUPER_FANCY', os.path.relpath(path, A))

# flags 0.I removed outright
for path in glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    data = ld(path)
    changed = False
    for o in objs(data):
        if isinstance(o, dict) and isinstance(o.get('flags'), list) and 'SUPER_FANCY' in o['flags']:
            o['flags'] = [f for f in o['flags'] if f != 'SUPER_FANCY']
            changed = True
    if changed:
        sv(path, data)

# Files 0.H-custom never changed whose 0.I layout upstream already converted
# (old palettes removed in 0.I): take upstream's file as-is.
import shutil
TAKE_UPSTREAM = ['maps/mapgen/basement_bionic.json']
for rel in TAKE_UPSTREAM:
    shutil.copy(os.path.join(UP, rel), os.path.join(A, rel))
    print('upstream file', rel)

# Item ids 0.I migrated away: follow the migration wherever the mod names them.
moved = {k: v for k, v in migr.items() if k not in live and v and k != 'ruger_redhawk'}
GROUPS = {'"group": "military"': '"group": "mil_armor"', '"item": "military"': '"item": "mil_armor"',
          '"item": "trash"': '"item": "SUS_trash_floor"', '"group": "trash"': '"group": "SUS_trash_floor"',
          '"group": "guns_pistol_obscure"': '"group": "guns_pistol_common"',
          '"ammo-item": "rebreather_filter"': '"ammo-item": "rebreather_filler_soda_lime"',
          '"item": "office_paper"': '"item": "SUS_office_filing_cabinet"',
          '"group": "office_paper"': '"group": "SUS_office_filing_cabinet"'}
for path in glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    new = text
    for old, rep in GROUPS.items():
        new = new.replace(old, rep)
    base = os.path.basename(path)
    in_maps = os.sep + 'maps' + os.sep in path  # mapgen names item groups that share old item ids
    hits = [] if ('migration' in base or 'obsolete' in base or in_maps) else [k for k in moved if f'"{k}"' in new]
    for k in hits:
        new = new.replace(f'"{k}"', f'"{moved[k]}"')
    if new != text:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        print('migrated refs', os.path.relpath(path, A), hits)

# bubble_car left core in 0.I: drop it from the vehicle groups Aftershock extends
p = os.path.join(A, 'vehicles/vehicle_groups.json')
d = ld(p)
out = []
for o in d:
    if o.get('type') == 'vehicle_group':
        o['vehicles'] = [v for v in o['vehicles'] if v[0] not in ('bubble_car', 'portable_generator')]
        if not o['vehicles']:
            continue
    out.append(o)
sv(p, out)


# Containers whose pockets changed in 0.I
def fix_containers(x):
    hit = False
    if isinstance(x, list):
        for n, e in enumerate(x):
            if isinstance(e, dict) and e.get('container-item') in ('mil_mess_kit', 'survivor_mess_kit', 'water_purifier'):
                x[n] = OD([('item', 'survivor_mess_kit' if 'mess_kit' in e['container-item'] else e['container-item'])])
                hit = True
            elif isinstance(e, dict) and e.get('container-item') == 'flashlight':
                e['item'], e['charges'] = 'medium_battery_cell', 56  # 0.I flashlights take medium cells
                hit = True
            else:
                hit |= fix_containers(e)
    elif isinstance(x, dict):
        for v in x.values():
            hit |= fix_containers(v)
    return hit


for path in glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    data = ld(path)
    if fix_containers(data):
        sv(path, data)
        print('containers', os.path.relpath(path, A))

# 0.H "wreckage" left core in 0.I; Aftershock maps still scatter it
p = os.path.join(A, 'itemgroups/item_groups.json')
d = ld(p)
if not any(o.get('id') == 'wreckage' for o in d):
    d.append(OD([('type', 'item_group'), ('id', 'wreckage'), ('//', '0.H core group, removed in 0.I'),
                 ('items', [['chain', 20], ['steel_chunk', 30], ['spring', 50], ['steel_lump', 30], ['frame', 20],
                            ['hdframe', 20], ['cu_pipe', 25], ['scrap_copper', 62], ['rock', 40], ['survnote', 1]])]))
for o in d:
    if o.get('id') == 'afs_mealgrubs_wrapper_pr_5':
        o['on_overflow'] = 'spill'  # 0.I's pull-tab wrapper holds fewer grubs
sv(p, d)
# mutation categories 0.I added on replacement chains
p = os.path.join(A, 'mutations/mutations.json')
d = ld(p)
for o in d:
    if o.get('id') == 'PATCHFUR' and 'CHIROPTERAN' not in o.get('category', []):
        o['category'].append('CHIROPTERAN')
if not any(o.get('id') == 'VERY_TALL' for o in d):
    i = next(n for n, o in enumerate(d) if o.get('id') == 'LARGE')
    d.insert(i, OD([('type', 'mutation'), ('id', 'VERY_TALL'), ('copy-from', 'VERY_TALL'),
                    ('extend', OD([('category', ['MASTODON'])]))]))
sv(p, d)
# more groups 0.I renamed (in mapgen)
MAPGROUPS = {'"wreckage"': None, '"ammo_common"': '"ammo_common_boxed"', '"ammo_pistol_common"': '"ammo_common_boxed"',
             '"oven"': '"SUS_oven"', '"mags_crime"': '"mags_common"', '"mon_charred_nightmare"': '"mon_zombie_hazmat"'}
for path in glob.glob(os.path.join(A, 'maps', '**', '*.json'), recursive=True):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    new = text
    for old, rep in MAPGROUPS.items():
        if rep:
            new = new.replace(f'"item": {old}', f'"item": {rep}').replace(f'"group": {old}', f'"group": {rep}') \
                if old != '"mon_charred_nightmare"' else new.replace(old, rep)
    if new != text:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        print('map groups', os.path.relpath(path, A))
# s_gas became s_gas_1 in 0.I
p = os.path.join(A, 'maps/mapgen/s_gas.json')
d = ld(p)
for o in d:
    if o.get('om_terrain') == ['s_gas']:
        o['om_terrain'] = ['s_gas_1']
sv(p, d)
# light_plus cells in Aftershock's own obsolete items
p = os.path.join(A, 'items/obsolete.json')
d = ld(p)
txt = json.dumps(d).replace('"light_plus_battery_cell"', '"light_battery_cell"').replace('"medium_plus_battery_cell"', '"medium_battery_cell"')
sv(p, json.loads(txt, object_pairs_hook=OD))

# Aftershock's own obsolete items still name migrated cells in pocket restrictions
p = os.path.join(A, 'items/obsolete.json')
d = ld(p)
for o in d:
    if isinstance(o, dict) and o.get('type') != 'MIGRATION':
        txt = json.dumps(o)
        for k, v in moved.items():
            txt = txt.replace(f'"{k}"', f'"{v}"')
        o.clear()
        o.update(json.loads(txt, object_pairs_hook=OD))
sv(p, d)
p = os.path.join(A, 'itemgroups/food_groups.json')
d = ld(p)
for o in d:
    if o.get('id') == 'afs_mealgrubs_wrapper_pr_5':
        o['on_overflow'] = 'spill'  # 0.I's pull-tab wrapper holds fewer grubs
sv(p, d)
# 0.I's survivor mess kit is an oil-fed magazine item; kits carry the plain mess kit
p = os.path.join(A, 'itemgroups/spaceship_groups.json')
d = ld(p)
for o in d:
    for e in o.get('entries', []):
        if isinstance(e, dict) and e.get('item') == 'survivor_mess_kit':
            e['item'] = 'mess_kit'
sv(p, d)

# 0.I test thresholds: material density, calorie density, monfaction reciprocity
TWEAKS = {
    'afs_food_cube': {'volume': '170 ml'},
    'afs_food_to_go': {'volume': '170 ml'},
    'afs_escapepod_ration': {'volume': '170 ml'},
    'afs_cee_wafers': {'volume': '170 ml'},
    'afs_calorie_pill': {'weight': '50 g', 'volume': '50 ml'},
    'afs_sundew': {'weight': '125 g'},
}
for path in glob.glob(os.path.join(A, '**', '*.json'), recursive=True):
    data = ld(path)
    changed = False
    for o in objs(data):
        if isinstance(o, dict) and o.get('type') == 'ITEM' and o.get('id') in TWEAKS:
            o.update(TWEAKS[o['id']])
            if o['id'] == 'afs_calorie_pill':
                o['description'] = o['description'].replace('half the size of your thumb', 'the size of a matchbox')
            changed = True
        if isinstance(o, dict) and o.get('type') == 'MONSTER_FACTION' and o.get('name') == 'hevel':
            if 'herbivore_domestic' not in o['neutral']:
                o['neutral'].append('herbivore_domestic')  # 0.I herbivores are by-mood to it
                changed = True
    if changed:
        sv(path, data)

#!/usr/bin/env python3
"""Convert a 0.H-format mod tree to 0.I's JSON schema, in place.

Handles: item types (ITEM + subtypes), integer prices, gunmod gun_data,
gun "magazines" lists, tool "ammo" -> "tool_ammo", book skill/fun,
relic_data -> ARTIFACT subtype, ONLY_ONE -> max_worn 1, mapgen "method",
monstergroup "name" -> "id", PATH_AVOID_DANGER_1, dialogue variables with
type/context (u_has_var, u_add_var, u_lose_var, u_adjust_var,
u_compare_var), arithmetic and compare_int -> math, queue_eocs ->
run_eocs.  Numeric see_cost values are reported, not converted.

Usage: convert_mod_0I.py DIR
Prints a report; run 0.I's json_formatter.cgi on changed files afterwards.
"""
import collections
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from restore_items import convert as convert_item, is_item  # noqa: E402

OD = collections.OrderedDict
STAT_RENAMES = {'fatigue': 'sleepiness'}
# hardcoded monster attacks 0.I removed, with their JSON replacements
HARDCODED_TO_JSON = {'TENTACLE': 'tentacle', 'LONGSWIPE': 'longswipe'}
# 0.H mutation fields that 0.I reads only as enchantment values:
# field -> (enchant value, 'add'|'multiply', transform)
MUT_FIELDS = {
    'hearing_modifier': ('HEARING_MULT', 'multiply', lambda x: x - 1),
    'weight_capacity_modifier': ('CARRY_WEIGHT', 'multiply', lambda x: x - 1),
    'bodytemp_sleep': ('BODYTEMP_SLEEP', 'add', lambda x: x / 500),
    'consume_time_modifier': ('CONSUME_TIME_MOD', 'multiply', lambda x: x - 1),
    'movecost_flatground_modifier': ('MOVECOST_FLATGROUND_MOD', 'multiply', lambda x: x - 1),
    'hp_modifier': ('MAX_HP', 'multiply', lambda x: x),
    'hp_modifier_secondary': ('MAX_HP', 'multiply', lambda x: x),
    'hp_adjustment': ('MAX_HP', 'add', lambda x: x),
    'fatigue_modifier': ('SLEEPINESS', 'multiply', lambda x: x),
    'fatigue_regen_modifier': ('SLEEPINESS_REGEN', 'multiply', lambda x: x),
    'stamina_regen_modifier': ('STAMINA_REGEN_MOD', 'add', lambda x: x),
    'healing_awake': ('REGEN_HP_AWAKE', 'multiply', lambda x: x),
    'healing_multiplier': ('REGEN_HP', 'multiply', lambda x: x - 1),
    'mending_modifier': ('MENDING_MODIFIER', 'multiply', lambda x: x - 1),
    'metabolism_modifier': ('METABOLISM', 'multiply', lambda x: x),
    'thirst_modifier': ('THIRST', 'multiply', lambda x: x),
    'movecost_modifier': ('MOVE_COST', 'multiply', lambda x: x - 1),
    'movecost_obstacle_modifier': ('MOVECOST_OBSTACLE_MOD', 'multiply', lambda x: x - 1),
    'attackcost_modifier': ('ATTACK_SPEED', 'multiply', lambda x: x - 1),
    'noise_modifier': ('FOOTSTEP_NOISE', 'multiply', lambda x: x - 1),
    'skill_rust_multiplier': ('SKILL_RUST_RESIST', 'multiply', lambda x: x - 1),
    'dodge_modifier': ('DODGE_CHANCE', 'add', lambda x: x),
    'reading_speed_multiplier': ('READING_SPEED_MULTIPLIER', 'multiply', lambda x: x - 1),
    'obtain_cost_multiplier': ('OBTAIN_COST_MULTIPLIER', 'multiply', lambda x: x - 1),
    'cardio_multiplier': ('CARDIO_MULTIPLIER', 'multiply', lambda x: x - 1),
    'overmap_sight': ('OVERMAP_SIGHT', 'add', lambda x: x),
    'vomit_multiplier': ('VOMIT_MUL', 'multiply', lambda x: x - 1),
    'casting_time_multiplier': ('CASTING_TIME_MULTIPLIER', 'multiply', lambda x: x - 1),
}
PASSIVE_MODS = {'str_mod': 'STRENGTH', 'dex_mod': 'DEXTERITY', 'int_mod': 'INTELLIGENCE', 'per_mod': 'PERCEPTION'}
report = collections.Counter()
notes = []


def var_name(obj, key):
    parts = [obj.get('type'), obj.get('context'), obj[key]]
    return '_'.join(str(p) for p in parts if p)


def operand(val, where):
    """0.H arithmetic/compare_int operand -> math expression string."""
    if isinstance(val, (int, float)):
        return str(val)
    if not isinstance(val, dict):
        notes.append(f'{where}: odd operand {val!r}')
        return json.dumps(val)
    if 'const' in val:
        return str(val['const'])
    if 'time' in val:
        return f"time('{val['time']}')"
    for side, prefix in (('u_val', 'u_'), ('npc_val', 'n_'), ('global_val', '')):
        if side in val:
            what = val[side]
            if what == 'var':
                return prefix + var_name(val, 'var_name')
            what = STAT_RENAMES.get(what, what)
            if side == 'global_val':
                notes.append(f'{where}: global_val {what!r} needs checking')
                return what
            return f"{'u' if side == 'u_val' else 'n'}_val('{what}')"
    notes.append(f'{where}: unhandled operand {val!r}')
    return json.dumps(val)


def convert_dialogue(x, where):
    """Rewrite dialogue variable conditions/effects in place; returns new value."""
    if isinstance(x, list):
        return [convert_dialogue(e, where) for e in x]
    if not isinstance(x, dict):
        return x
    for side in ('u', 'npc'):
        val_key = 'u_val' if side == 'u' else 'npc_val'
        mprefix = 'u_' if side == 'u' else 'n_'
        k = f'{side}_has_var'
        if k in x and ('type' in x or 'context' in x):
            report['has_var'] += 1
            if 'value' in x:
                return OD([('compare_string', [x['value'], OD([(val_key, var_name(x, k))])])])
            notes.append(f'{where}: has_var without value {x}')
        k = f'{side}_add_var'
        if k in x and ('type' in x or 'context' in x):
            report['add_var'] += 1
            new = OD([(k, var_name(x, k))])
            for extra in ('value', 'time', 'possible_values'):
                if extra in x:
                    new[extra] = x[extra]
            return new
        k = f'{side}_lose_var'
        if k in x and ('type' in x or 'context' in x):
            report['lose_var'] += 1
            return OD([(k, var_name(x, k))])
        k = f'{side}_adjust_var'
        if k in x:
            report['adjust_var'] += 1
            adj = x.get('adjustment', 1)
            adj = operand(adj, where) if isinstance(adj, dict) else str(adj)
            return OD([('math', [f'{mprefix}{var_name(x, k)} += {adj}'])])
        k = f'{side}_compare_var'
        if k in x:
            report['compare_var'] += 1
            return OD([('math', [f"{mprefix}{var_name(x, k)} {x['op']} {x['value']}"])])
    if 'arithmetic' in x and isinstance(x['arithmetic'], list):
        report['arithmetic'] += 1
        a = x['arithmetic']
        if len(a) == 3:
            return OD([('math', [operand(a[0], where), a[1], operand(a[2], where)])])
        if len(a) == 5:
            return OD([('math', [operand(a[0], where), a[1],
                                 f'{operand(a[2], where)} {a[3]} {operand(a[4], where)}'])])
        if len(a) == 2:
            return OD([('math', [operand(a[0], where), a[1]])])
        notes.append(f'{where}: arithmetic {a}')
    if 'compare_int' in x and isinstance(x['compare_int'], list):
        report['compare_int'] += 1
        a = x['compare_int']
        return OD([('math', [f'{operand(a[0], where)} {a[1]} {operand(a[2], where)}'])])
    if 'queue_eocs' in x:
        report['queue_eocs'] += 1
        new = OD()
        for kk, vv in x.items():
            new['run_eocs' if kk == 'queue_eocs' else kk] = vv
        x = new
    for kk in list(x.keys()):
        x[kk] = convert_dialogue(x[kk], where)
    return x


def convert_obj(o, where):
    t = o.get('type')
    if t in ('GUN', 'TOOL', 'GENERIC', 'AMMO', 'MAGAZINE', 'ARMOR', 'COMESTIBLE', 'BIONIC_ITEM',
             'TOOL_ARMOR', 'GUNMOD', 'TOOLMOD', 'BOOK', 'PET_ARMOR', 'ENGINE', 'WHEEL', 'BATTERY'):
        report['item'] += 1
        o = convert_item(o)
        t = 'ITEM'
    if t == 'ITEM':
        flags = o.get('flags')
        if isinstance(flags, list) and 'ONLY_ONE' in flags:
            o['flags'] = [f for f in flags if f != 'ONLY_ONE']
            o['max_worn'] = 1
            report['only_one'] += 1
            if not o['flags']:
                del o['flags']
        for key in ('price', 'price_postapoc'):
            if isinstance(o.get(key), int):
                o[key] = f'{o[key]} cent'
                report['price'] += 1
    if t in ('terrain', 'furniture') and isinstance(o.get('symbol'), str) and o['symbol'].startswith('LINE_'):
        o['symbol'] = '#'  # 0.I draws wall lines itself (AUTO_WALL_SYMBOL)
        report['line_symbol'] += 1
    if t == 'mapgen' and 'method' in o:
        del o['method']
        report['method'] += 1
    if t == 'ITEM':
        vits = o.get('vitamins')
        if isinstance(vits, list):
            for n, v in enumerate(vits):
                if isinstance(v, list) and len(v) == 3:
                    vits[n] = [v[0], (v[1] + v[2]) // 2]  # 0.I dropped vitamin ranges
                    report['vitamin_range'] += 1
        for fk in ('faults',):
            if isinstance(o.get(fk), list) and any(isinstance(f, str) for f in o[fk]):
                o[fk] = [OD([('fault', f)]) if isinstance(f, str) else f for f in o[fk]]
                report['faults'] += 1
        ext = o.get('extend')
        if isinstance(ext, dict) and isinstance(ext.get('faults'), list):
            ext['faults'] = [OD([('fault', f)]) if isinstance(f, str) else f for f in ext['faults']]
        if 'conversion_rate' in o and 'into' in o:
            o['recipe'] = f"{o['into']}_mill_1_{o.pop('conversion_rate')}"  # as 0.I's own bones
            report['milling_recipe'] += 1
        ua = o.get('use_action')
        if isinstance(ua, list):
            new_ua = []
            for a in ua:
                a = {'EINKTABLETPC': 'E_FILE_DEVICE', 'EBOOKREAD': 'E_FILE_DEVICE',
                     'ELECTRICSTORAGE': 'E_FILE_DEVICE'}.get(a, a) if isinstance(a, str) else a
                if a not in new_ua:
                    new_ua.append(a)
            if new_ua != ua:
                o['use_action'] = new_ua
                report['efile_iuse'] += 1
        for pocket in o.get('pocket_data', []) or []:
            if isinstance(pocket, dict) and pocket.get('pocket_type') == 'EBOOK':
                pocket['pocket_type'] = 'E_FILE_STORAGE'
                pocket.setdefault('max_contains_volume', '1 ml')
                pocket.setdefault('max_contains_weight', '1 g')
                pocket.setdefault('weight_multiplier', 0)
                pocket.setdefault('ememory_max', '1 TB')
                report['efile_pocket'] += 1
    if t == 'monstergroup':
        for mon in o.get('monsters', []) or []:
            for k in ('starts', 'ends'):
                if isinstance(mon.get(k), int):
                    mon[k] = f'{mon[k]} hours'
                    report['mongroup_time'] += 1
    if t == 'bionic' and isinstance(o.get('stat_bonus'), list):
        stat = {'STR': 'STRENGTH', 'DEX': 'DEXTERITY', 'INT': 'INTELLIGENCE', 'PER': 'PERCEPTION'}
        vals = [OD([('value', stat[s]), ('add', v)]) for s, v in o.pop('stat_bonus')]
        o.setdefault('enchantments', []).append(OD([('values', vals)]))
        report['bionic_stat_bonus'] += 1
    if t == 'faction' and isinstance(o.get('food_supply'), int):
        # 0.I: calories and vitamins; scale as 0.I did for its own factions (115200 -> 2.7e9 kcal-units)
        fs = o.pop('food_supply')
        vit = int(fs * 0.75)
        o['fac_food_supply'] = [[0, OD([('calories', fs * 23437 + fs // 2),
                                        ('vitamins', OD([('iron', vit), ('calcium', vit), ('vitC', vit)]) if fs else OD())])]]
        report['faction_food'] += 1
    if t == 'mutation':
        vals = []
        for fld, (ev, op, fn) in MUT_FIELDS.items():
            if fld in o and isinstance(o[fld], (int, float)):
                x = fn(o.pop(fld))
                vals.append(OD([('value', ev), (op, round(x, 4) if isinstance(x, float) else x)]))
        if isinstance(o.get('passive_mods'), dict):
            for k, v in o.pop('passive_mods').items():
                if k in PASSIVE_MODS:
                    vals.append(OD([('value', PASSIVE_MODS[k]), ('add', v)]))
                else:
                    notes.append(f'{where}: passive_mods {k} on {o.get("id")}')
        if 'temperature_speed_modifier' in o:
            x = o.pop('temperature_speed_modifier')
            vals.append(OD([('value', 'SPEED'), ('add', OD([('math', [f'temperature_speed_mod(65, {x})'])]))]))
        if vals:
            o.setdefault('enchantments', []).append(OD([('values', vals)]))
            report['mutation_fields'] += 1
    if t == 'MONSTER':
        if o.get('luminance') == 0:
            del o['luminance']  # 0.I rejects an explicit default
            report['luminance0'] += 1
        sa = o.get('special_attacks')
        if isinstance(sa, list):
            for n, att in enumerate(sa):
                if isinstance(att, list) and att and att[0] in HARDCODED_TO_JSON:
                    new_att = OD([('id', HARDCODED_TO_JSON[att[0]])])
                    if len(att) > 1:
                        new_att['cooldown'] = att[1]
                    sa[n] = new_att
                    report['hardcoded_attack'] += 1
        for att in o.get('special_attacks', []) or []:
            if isinstance(att, dict) and att.get('type') == 'gun' and 'cooldown' not in att:
                att['cooldown'] = 1  # mandatory in 0.I
                report['gun_cooldown'] += 1
    if t == 'MONSTER' and isinstance(o.get('reproduction'), dict):
        rep = o['reproduction']
        kinds = [k for k in ('baby_monster', 'baby_monster_group', 'baby_egg', 'baby_egg_group') if k in rep]
        if kinds and 'baby_type' not in rep:
            new = OD()
            new['baby_type'] = OD((k, rep[k]) for k in kinds)
            for k, v in rep.items():
                if k not in kinds:
                    new[k] = v
            o['reproduction'] = new
            report['reproduction'] += 1
    if t == 'monstergroup' and 'name' in o and 'id' not in o:
        new = OD()
        for k, v in o.items():
            new['id' if k == 'name' else k] = v
        o = new
        report['mongroup_name'] += 1
    if t == 'overmap_terrain' and isinstance(o.get('see_cost'), int):
        notes.append(f"{where}: see_cost {o['see_cost']} on {o.get('id')}")
    text = json.dumps(o)
    if 'PATH_AVOID_DANGER_1' in text or 'PATH_AVOID_DANGER_2' in text:
        o = json.loads(text.replace('"PATH_AVOID_DANGER_1"', '"PATH_AVOID_DANGER"').replace('"PATH_AVOID_DANGER_2"', '"PATH_AVOID_DANGER"'), object_pairs_hook=OD)
        report['path_avoid'] += 1
    return convert_dialogue(o, where)


def main():
    root = sys.argv[1]
    changed = []
    for path in sorted(glob.glob(os.path.join(root, '**', '*.json'), recursive=True)):
        with open(path, encoding='utf-8') as f:
            try:
                data = json.load(f, object_pairs_hook=OD)
            except ValueError as e:
                notes.append(f'{path}: unreadable {e}')
                continue
        before = json.dumps(data)
        single = isinstance(data, dict)
        objs = [data] if single else data
        out = [convert_obj(o, os.path.relpath(path, root)) if isinstance(o, dict) else o for o in objs]
        out = out[0] if single else out
        if json.dumps(out) != before:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(out, f, indent=2, ensure_ascii=False)
                f.write('\n')
            changed.append(path)
    for k, v in sorted(report.items()):
        print(f'{k}: {v}')
    print('notes:')
    for n in notes:
        print('  ' + n)
    for p in changed:
        print('CHANGED ' + p)


if __name__ == '__main__':
    main()

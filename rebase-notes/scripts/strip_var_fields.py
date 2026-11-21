#!/usr/bin/env python3
"""Drop the "type"/"context" fields 0.I removed from dialogue variables.

Only handles the field removal. 0.I also moved value checks such as
{ "u_has_var": "x", "value": "4" } into math comparisons; those still need
converting by hand. Rewrites whole files: run 0.I's
tools/format/json_formatter.cgi on each changed file afterwards.

Usage: strip_var_fields.py FILE...
"""
import collections
import json
import sys

VAR_KEYS = {
    'u_has_var', 'npc_has_var', 'u_add_var', 'npc_add_var', 'u_lose_var',
    'npc_lose_var', 'u_adjust_var', 'npc_adjust_var', 'u_compare_var',
    'npc_compare_var', 'u_compare_time_since_var', 'npc_compare_time_since_var',
}


def strip(node):
    changed = 0
    if isinstance(node, dict):
        if VAR_KEYS & node.keys() and ('type' in node or 'context' in node):
            node.pop('type', None)
            node.pop('context', None)
            changed += 1
        for value in node.values():
            changed += strip(value)
    elif isinstance(node, list):
        for value in node:
            changed += strip(value)
    return changed


total = 0
for path in sys.argv[1:]:
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f, object_pairs_hook=collections.OrderedDict)
    except (OSError, ValueError):
        continue
    count = strip(data)
    if count:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        total += count
        print(path)
print(f'stripped {total} variable references')

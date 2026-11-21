#!/usr/bin/env python3
"""Convert 0.H item types to 0.I's single ITEM type with subtypes.

Rewrites top-level (four-space indented) "type" lines only, so diffs stay
minimal and formatting is untouched. GENERIC becomes a plain ITEM.

Usage: convert_item_types.py FILE...
"""
import re
import sys

SUBTYPES = {
    'GUN': '"GUN"', 'TOOL': '"TOOL"', 'AMMO': '"AMMO"', 'MAGAZINE': '"MAGAZINE"',
    'ARMOR': '"ARMOR"', 'COMESTIBLE': '"COMESTIBLE"', 'BIONIC_ITEM': '"BIONIC_ITEM"',
    'TOOL_ARMOR': '"TOOL", "ARMOR"', 'GUNMOD': '"GUNMOD"', 'TOOLMOD': '"TOOLMOD"',
    'BOOK': '"BOOK"', 'PET_ARMOR': '"PET_ARMOR"', 'ENGINE': '"ENGINE"',
    'WHEEL': '"WHEEL"', 'BATTERY': '"BATTERY"', 'GENERIC': None,
}
PATTERN = re.compile(r'^(    )"type": "(%s)",$' % '|'.join(SUBTYPES), re.M)


def replace(match):
    indent, old = match.group(1), match.group(2)
    line = f'{indent}"type": "ITEM",'
    if SUBTYPES[old]:
        line += f'\n{indent}"subtypes": [ {SUBTYPES[old]} ],'
    return line


total = 0
for path in sys.argv[1:]:
    with open(path, encoding='utf-8') as f:
        text = f.read()
    text, count = PATTERN.subn(replace, text)
    if count:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        total += count
print(f'converted {total} objects')

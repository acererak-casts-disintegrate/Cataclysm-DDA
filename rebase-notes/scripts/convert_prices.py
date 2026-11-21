#!/usr/bin/env python3
"""Convert 0.H integer prices (cents) to 0.I unit strings ("N cent").

Run only on files carrying fork content: 0.I itself still uses integer
prices in some non-item contexts.

Usage: convert_prices.py FILE...
"""
import re
import sys

PATTERN = re.compile(r'"(price|price_postapoc)": (-?\d+)(?=\s*[,}\n])')
total = 0
for path in sys.argv[1:]:
    with open(path, encoding='utf-8') as f:
        text = f.read()
    text, count = PATTERN.subn(lambda m: f'"{m.group(1)}": "{m.group(2)} cent"', text)
    if count:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        total += count
print(f'converted {total} prices')

#!/usr/bin/env python3
"""Apply CDDA text-style and plural lint fixes reported in a cata_test log. Usage: lintfix.py LOG MODDIR MODPREFIX"""
import re, sys, collections
log, moddir, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
L = open(log, encoding="utf-8", errors="replace").read().split("\n")
errs = collections.defaultdict(list)
for i, l in enumerate(L):
    m = re.search(r'Json error: file ' + re.escape(prefix) + r'(\S+), at line (\d+), character (\d+):', l)
    if m: errs[m.group(1)].append((int(m.group(2)), int(m.group(3)), L[i + 1]))
done = 0; skipped = []
for f, lst in errs.items():
    path = moddir + "/" + f
    lines = open(path, encoding="utf-8").read().split("\n")
    for ln, ch, kind in sorted(lst, key=lambda x: (x[0], -x[1])):
        b = lines[ln - 1].encode()
        if kind.startswith("insufficient spaces"):
            if b[ch-1:ch] in (b".", b"!", b"?") and b[ch:ch+1] == b" ": b = b[:ch] + b" " + b[ch:]
            else: skipped.append((f, ln, kind, b[max(0,ch-15):ch+10])); continue
        elif kind.startswith("excessive spaces"):
            if b[ch-1:ch] == b" ": b = b[:ch-1] + b[ch:]
            else: skipped.append((f, ln, kind)); continue
        elif kind.startswith("unnecessary spaces before"):
            j = ch
            while j > 0 and b[j-1:j] == b" ": j -= 1
            if j < ch: b = b[:j] + b[ch:]
            else: skipped.append((f, ln, kind)); continue
        elif kind.startswith("ellipsis"):
            if b[ch-3:ch] == b"...": b = b[:ch-3] + "…".encode() + b[ch:]
            else: skipped.append((f, ln, kind)); continue
        elif kind.startswith('Please use "str_sp"'):
            m = re.search(rb'\{ "str": ("[^"]*"), "str_pl": ("[^"]*") \}', b)
            if m and m.group(1) == m.group(2): b = b[:m.start()] + b'{ "str_sp": ' + m.group(1) + b' }' + b[m.end():]
            else: skipped.append((f, ln, kind)); continue
        elif kind.startswith('"str_pl" is not necessary'):
            m = re.search(rb'\{ "str": ("[^"]*"), "str_pl": "[^"]*" \}', b)
            if m: b = b[:m.start()] + b'{ "str": ' + m.group(1) + b' }' + b[m.end():]
            else: skipped.append((f, ln, kind)); continue
        else:
            skipped.append((f, ln, kind)); continue
        lines[ln - 1] = b.decode(); done += 1
    open(path, "w", encoding="utf-8").write("\n".join(lines))
print("fixed", done)
for s in skipped: print("SKIP", *s)

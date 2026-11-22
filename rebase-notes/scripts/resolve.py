#!/usr/bin/env python3
"""Resolve conflict hunks in a file. Usage: resolve.py FILE SPEC...
SPEC per hunk in order: 'ours' | 'theirs' | 'both' | 'bothc' (ours, comma, theirs) | 'file:PATH' (replacement text from file)."""
import sys,re
path=sys.argv[1]; specs=sys.argv[2:]
lines=open(path).read().split('\n')
out=[];i=0;h=0
while i<len(lines):
    l=lines[i]
    if l.startswith('<<<<<<< '):
        ours=[];theirs=[];i+=1
        while not lines[i].startswith('=======') and not lines[i].startswith('||||||| '): ours.append(lines[i]); i+=1
        if lines[i].startswith('||||||| '):
            while not lines[i].startswith('======='): i+=1
        i+=1
        while not lines[i].startswith('>>>>>>> '): theirs.append(lines[i]); i+=1
        i+=1
        s=specs[h] if h<len(specs) else None; h+=1
        if s=='ours': out+=ours
        elif s=='theirs': out+=theirs
        elif s=='both': out+=ours+theirs
        elif s=='bothc':
            o=list(ours)
            if o and not o[-1].rstrip().endswith(','): o[-1]=o[-1].rstrip()+','
            out+=o+theirs
        elif s and s.startswith('file:'): out+=open(s[5:]).read().rstrip('\n').split('\n')
        else: sys.exit(f'no spec for hunk {h} in {path}')
        continue
    out.append(l); i+=1
if h!=len(specs): sys.exit(f'{path}: {h} hunks but {len(specs)} specs')
open(path,'w').write('\n'.join(out))
print(f'{path}: resolved {h} hunks')

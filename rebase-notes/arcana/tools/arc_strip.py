#!/usr/bin/env python3
"""Audit-only: strip enchantment values 0.I lacks, logging each. Usage: arc_strip.py DIR VALUE..."""
import json, sys, glob, os, subprocess
D, vals = sys.argv[1], set(sys.argv[2:])
FMT = "/tmp/claude-0/-home-user-Cataclysm-DDA/9a359a85-62c1-52fd-8ed1-3ef1a5c89d21/scratchpad/rebase/tools/format/json_formatter.cgi"
for f in sorted(glob.glob(os.path.join(D, "**", "*.json"), recursive=True)):
    data = json.load(open(f, encoding="utf-8")); hit = []
    def walk(o, top):
        if isinstance(o, dict):
            if isinstance(o.get("values"), list):
                keep = [v for v in o["values"] if not (isinstance(v, dict) and v.get("value") in vals)]
                if len(keep) != len(o["values"]):
                    hit.append((top, [v["value"] for v in o["values"] if isinstance(v, dict) and v.get("value") in vals])); o["values"] = keep
            for v in o.values(): walk(v, top)
        elif isinstance(o, list):
            for v in o: walk(v, top)
    for obj in data: walk(obj, obj.get("id") if isinstance(obj, dict) else None)
    if hit:
        open(f, "w", encoding="utf-8").write(json.dumps(data, indent=2, ensure_ascii=False) + "\n"); subprocess.run([FMT, f], capture_output=True)
        for h in hit: print(os.path.relpath(f, D), *h)

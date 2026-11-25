#!/usr/bin/env python3
"""Mechanical 0.J -> 0.I reversions for an Arcana working copy. Usage: arc_revert.py ARCANA_DIR"""
import json, re, sys, os, glob, subprocess
D = sys.argv[1]
FMT = "/tmp/claude-0/-home-user-Cataclysm-DDA/9a359a85-62c1-52fd-8ed1-3ef1a5c89d21/scratchpad/rebase/tools/format/json_formatter.cgi"
MISSION = {"NULL": 0, "LEGACY_1": 1, "SHELTER": 2, "SHOPKEEP": 3, "LEGACY_2": 4, "LEGACY_3": 5, "GUARD_ALLY": 6,
           "GUARD": 7, "GUARD_PATROL": 8, "ACTIVITY": 9, "TRAVELLING": 10}
log = []
def walk(o, fn, path=""):
    if isinstance(o, dict):
        fn(o, path)
        for k, v in list(o.items()):
            walk(v, fn, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, fn, path + "[%d]" % i)
changed = set()
for f in sorted(glob.glob(os.path.join(D, "**", "*.json"), recursive=True)):
    txt = open(f, encoding="utf-8").read()
    try:
        data = json.loads(txt)
    except Exception as e:
        print("PARSE", f, e); continue
    before = json.dumps(data, sort_keys=True)
    def fix(o, path):
        t = o.get("type")
        # ammo_effect aoe/trail: single object in 0.I
        if t == "ammo_effect":
            for k in ("aoe", "trail"):
                if isinstance(o.get(k), list) and len(o[k]) == 1:
                    o[k] = o[k][0]; log.append((f, o.get("id"), k + " unwrapped"))
        # npc mission names -> 0.I enum numbers
        if t == "npc" and isinstance(o.get("mission"), str):
            o["mission"] = MISSION[o["mission"]]; log.append((f, o.get("id"), "mission"))
        # body part "limb_types" as a single string -> 0.I "limb_type"
        if t == "body_part" and isinstance(o.get("limb_types"), str):
            o["limb_type"] = o.pop("limb_types"); log.append((f, o.get("id"), "limb_types string -> limb_type"))
        # 0.J travel cost types basement/roof/structure: 0.I uses the default ("other")
        if t == "overmap_terrain" and o.get("travel_cost_type") in ("basement", "roof", "structure"):
            log.append((f, o.get("id"), "travel_cost_type " + o.pop("travel_cost_type") + " removed"))
        # mutation provided_qualities { BUTCHER: n } -> 0.I butchering_quality
        if t == "mutation" and isinstance(o.get("provided_qualities"), dict) and set(o["provided_qualities"]) == {"BUTCHER"}:
            o["butchering_quality"] = o.pop("provided_qualities")["BUTCHER"]; log.append((f, o.get("id"), "provided_qualities -> butchering_quality"))
        # "light": n -> LIGHT_n flag
        if t in ("ITEM", "TOOL", "GENERIC", "ARMOR", "GUN", "TOOL_ARMOR") and isinstance(o.get("light"), int):
            n = o.pop("light"); o.setdefault("flags", []).append("LIGHT_%d" % n); log.append((f, o.get("id"), "light %d" % n))
    walk(data, fix)
    s = json.dumps(data, ensure_ascii=False)
    s2 = s.replace('"pasta_ingredients"', '"pasta"')
    if s2 != s: log.append((f, "-", "pasta_ingredients->pasta"))
    if json.dumps(json.loads(s2), sort_keys=True) != before:
        open(f, "w", encoding="utf-8").write(json.dumps(json.loads(s2), indent=2, ensure_ascii=False) + "\n")
        subprocess.run([FMT, f], capture_output=True); changed.add(f)
for l in log: print(*l)
print("files changed:", len(changed))

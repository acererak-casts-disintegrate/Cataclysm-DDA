# Arcana and Magic Items in this fork

This folder holds Arcana and Magic Items by Chaosvolt, imported from
[chaosvolt/cdda-arcana-mod](https://github.com/chaosvolt/cdda-arcana-mod), folder `Arcana`, at
commit `33bfbbe` (29 April 2026). The folder was last changed upstream in `f414e2c9`
(15 February 2026). Arcana is licensed under the Creative Commons Attribution-ShareAlike 3.0
Unported licence, the same licence as Cataclysm: Dark Days Ahead.

The upstream repository is archived: its author moved Arcana into Cataclysm: Bright Nights and
no longer maintains the Dark Days Ahead version. This fork maintains its own copy from here.

Not imported: `mod_interactions/Youkai_Disco/`. Youkai Disco is not in this repository, and
`build-scripts/get_all_mods.py` reads interaction folder names as mod IDs, so the folder would
put a nonexistent mod into CI's all-mods load.

The import is committed unmodified, followed by separate commits that format it, adapt it to
0.I and integrate it with this fork. Git stores the files with LF line endings; compare them
with upstream using `diff --strip-trailing-cr` or `git diff --ignore-cr-at-eol`.

## Ported from the Bright Nights version

Chaosvolt maintains Arcana in-repo in
[Cataclysm: Bright Nights](https://github.com/cataclysmbn/Cataclysm-BN) (`data/mods/Arcana_BN`,
same licence). Some of its later fixes and additions were ported here, adapted to this game's
engine, as checked against Bright Nights `4846cb7` (25 November 2026):

* Fixes: Bright Nights #10072 (hermit mapgen z-level), #10073 (drain life on killing blows),
  #9972 (gilded aegis), #10853 (moruboru stun).
* Additions: the purifying .410 shot, skeleton master and lich drops, the moonstone scourge's belt
  clip, the distortion flow rotor and the essence focus cell from chaosvolt's own `Arcana_BN`
  folder; loot changes from #10148; visual updates from #10398; monster and material rebalancing
  from #10143 and #9878.

Not ported: anything built on Bright Nights engine features or Bright Nights-only content (spell
classes, effect enchantments, mod options, flight, its own monsters, scenarios and locations). The
commit messages give the details and the adaptations.

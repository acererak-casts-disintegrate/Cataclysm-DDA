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

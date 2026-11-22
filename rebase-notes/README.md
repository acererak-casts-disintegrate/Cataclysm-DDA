# Moving 0.H-custom onto 0.I: costing notes

This branch costs moving the fork from upstream 0.H to 0.I. It is a measuring exercise, not a finished port: do not merge it.

## Branch layout

- **Base:** upstream `0.I-branch` at `7b2efa5cea` (0.I-1, 2026-09-19).
- **32 replayed commits:** the fork's commits from `0.H-custom` (base `08f04fd07` to `9d67cf3e71`). Each was applied with conflicting hunks resolved in the fork's favour (`git cherry-pick -X theirs`). That is a stand-in for hand merging, and it reinserts 0.H syntax that 0.I rejects.
- **5 commits skipped:** these are already in 0.I.
  - 23: battery chargers outside the reality bubble.
  - 24: Godco mapgen updates.
  - 25: flatbuffers fix for GCC 15.
  - 26: `EMPTY_GROUP` initialisation.
  - 34: conditional `mod_interactions` loading.
- **7 `scratch:` commits on top:**
  1. Convert item types (`scripts/convert_item_types.py`).
  2. Keep 0.I's iteminfo test, which already has the mod-proof repair test.
  3. Convert prices in replayed files (`scripts/convert_prices.py`).
  4. Stub the removed robot attacks and drop the mapgen `method` field.
  5. Drop 0.I's obsolete copies of `rm614_lmg` and `rm88_battle_rifle`.
  6. Strip variable `type`/`context` fields (`scripts/strip_var_fields.py`).
  7. Reset every conflicted file to 0.I's version. At the tip, those files do not carry the fork's changes. The changes are in the replayed commits underneath, and the files form the hand-merge set listed in `conflicts.tsv`.

The tip builds (`make TILES=1 SOUND=1 RELEASE=1 tests`). A core-only data load still fails on the restored assets listed under "Hand fixes".

## Data files

- `replay_summary.tsv`: one row per fork commit, with result, files touched and conflict counts by kind.
- `conflicts.tsv`: every conflicted path per commit. Git status codes:
  - `UU`: both sides changed the file.
  - `UD`: the fork deletes a file that 0.I changed.
  - `DU`: the fork edits a file that 0.I moved or deleted, so the edit was dropped.
  - `AA`: both sides added the file.

## Results

| Measure | Count |
|---|---|
| Files both sides changed | 139 unique (170 across commits), 306 conflict hunks |
| Fork deletions of files 0.I changed | 58: 34 from the Aftershock setting cleanup, 18 from the Exodii removal |
| Fork edits to files moved or deleted in 0.I | 12 |
| C++ conflicts | `src/options.cpp` (skill-rust option, 2 hunks) and 3 test files |

The 139 both-changed files by area:
- Aftershock 62.
- Core data 45: dialogue 13, items 7, item groups 6, monsters 5, event scripts 4, other 10.
- Other mods 27: Xedra Evolved 14, Mind Over Matter 3, Magiclysm 3, other 7.
- `src`/`tests` 4.
- The README 1.

The 12 dropped edits sit in four places:
- 0.I reorganised `data/json/obsoletion/` into `obsoletion_and_migration_0.I/`.
- `data/json/items/ranged/energy.json` no longer exists in core.
- No Hope's `regional_map_settings.json` was moved.
- `data/mods/replacements.json` and Blaze Industries are gone.

## Format changes for carried content

| Change in 0.I | Fork content affected | Fix |
|---|---|---|
| Legacy item types (`GUN`, `TOOL`, `GENERIC`...) removed; all items are `"type": "ITEM"` plus `"subtypes"` | 101 objects | `convert_item_types.py` |
| `price` and `price_postapoc` are unit strings (`"50 cent"`, `"10 USD"`) | 171 values | `convert_prices.py` (fork files only) |
| Dialogue variables lost `type`/`context`; value checks moved into math | 39 references | `strip_var_fields.py`, then value checks by hand |
| Mapgen has no default wall/floor symbols; `method` field removed; some item groups renamed (e.g. `alcohol`) | restored `basement_bionic_decoy` (181 load errors) | hand fix |
| Vehicle part ids renamed; `minireactor` removed | `car_sports_atomic` (about 110 load errors) | hand fix |
| Hardcoded `CHICKENBOT` and `MULTI_ROBOT` attacks deleted from the engine | chicken walker, tank drone | restore the C++ or rewrite as JSON gun attacks |
| Flag `ONLY_ONE` removed | `q_solarpack`, `q_solarpack_on` | hand fix |
| Gun fields renamed | two fields in `classic_scifi.json` | hand fix |
| Monster groups use `id`, not `name` | `GROUP_Exodii_Stowaway`, `GROUP_Exodii_Scout_Small` | rename |

## Where 0.I overrides the fork's choices

- **Migrations that would convert restored items on load.** Each needs its 0.I migration entry removed:
  - `5x50_100_mag` -> `stanag100`, `5x50_50_mag` -> `stanag50`, `5x50_hull` -> `shot_hull`
  - `5x50dart` and `5x50heavy` -> `50match`, `reloaded_5x50dart` -> `reloaded_50bmg`
  - `8mm_civilian`, `8mm_fmj`, `8mm_hvp` and `8mm_inc` -> `8mm_caseless`
  - `bot_copbot`, `bot_eyebot`, `bot_riotbot` and their `broken_*` versions, plus `broken_mininuke_hack` -> `broken_science_bot`
  - `needlegun` and `needlepistol` -> `nailgun`
  - `plasma_gun` -> `exodii_plasma_projectile`
  - `rm298` -> `m240`
- **Exodii.** Upstream's footprint grew from 63 files (302 ids) in 0.H to 96 files (378 ids) in 0.I. After the replay, 70 files still mention Exodii, against 34 on `0.H-custom`, so roughly 36 files of new content need a removal pass under the scavenger-only policy.
- **Portal storms.** Three more core files mention them after the replay.
- **Aftershock.** Upstream marked it obsolete in 0.I and deleted it in 0.J. Between 0.H and 0.I it grew by 410 files (+29,785 / −5,018 lines), mostly colony-setting content the fork's Earth rework would strip: psionics, Salvor Market, UICA, Augustmoon Salvors and new maps.
- **Blaze Industries** is deleted in 0.I.

## Suggested order for a real move

1. Carry the fork's own Aftershock folder over whole, converted with the scripts, rather than reconciling with 0.I's obsolete version. Cherry-pick any 0.I Aftershock additions wanted afterwards.
2. Hand-merge the 45 core and 27 other-mod conflicts and the 12 dropped edits. Merge `options.cpp` (skill rust).
3. Fix the restored assets: the bionic basement, the atomic sports car, the robots, the solar pack and the gun fields. Delete the 0.I migrations listed above.
4. Exodii removal pass against 0.I, then portal storms.
5. Re-run the mod data fixes from commit 35 against 0.I's tests, since upstream may already have fixed some of them.

## Reproducing

```bash
git fetch --filter=blob:none upstream 0.I-branch
git worktree add -b scratch/0.I-rebase ../rebase upstream/0.I-branch
REPO=$PWD WT=../rebase OUT=/tmp/replay SKIP="23 24 25 26 34" rebase-notes/scripts/replay.sh
```

0.I's `cata_test` uses a newer Catch2, so pass `--user-dir DIR` with a space and `--drop-world`. Do not use `-D`: it now takes a value and swallows the test filter.

## Port tools

Scripts used for the real port onto `0.I-custom`, kept here because they lived in a temporary directory. Scripts that need a scratch area read it from `S`.

| Script | Purpose |
|---|---|
| `convert_mod_0I.py` | Converts a 0.H-format mod tree to 0.I: item types and subtypes, flattened nested slots, `tool_ammo`, prices, faults, vitamins, milling, e-file devices, monster and monstergroup fields, dialogue variables and math, mutation modifiers to enchantments, enchantment value renames, map `see_cost` and symbols. |
| `restore_items.py` | Restores items from a 0.H tree into a 0.I tree with their copy-from parents, recipes and item-group entries, removing 0.I's migrations and obsolete stubs for them. |
| `af_fixes.py`, `af_pipeline.sh` | Aftershock-specific fixes and the pipeline that rebuilt Aftershock from `0.H-custom`. **Do not rerun `af_pipeline.sh` on `0.I-custom`:** it regenerates the mod folder and would wipe the exoplanet imports and the `itemgroups/zz_late` spawns added after it. |
| `merge_members.py`, `groupedit.py` | Copy monster, vehicle and item group members or whole groups between trees. |
| `dlg_strip.py` | Removes dialogue responses, effects or dynamic lines by id or regex. |
| `rm_objs.py`, `removed_ids.py` | Drop top-level objects by id; list ids a commit removed from a file. |
| `resolve.py` | Resolves conflict hunks in order (`ours`, `theirs`, `both`, `bothc`, `file:PATH`). |
| `pload.sh` | Load check and filtered `cata_test` run on the port worktree; `MODS` and `N` optional. |

Item groups cannot forward-reference a group defined by `copy-from` in a file loaded later, and files load in lexicographic path order; that is why late spawn edits sit under `itemgroups/zz_late/`.

# Arcana: in-repo integration audit (Antigravity revision)

> **Author / provenance:** Antigravity's revised copy of Claude's `AUDIT.md` (at `f19b295`),
> independently sanity-checked against `0.I-custom` at `fff2ed74a1` and a clean checkout of
> `chaosvolt/cdda-arcana-mod` (`33bfbbe`) on 25 November 2026. Claude's original `AUDIT.md` is
> kept unmodified alongside this file.

Audited against `0.I-custom` at `fff2ed74a1` (release `0.I-custom-2026-11-25-1038`), 25 November 2026.
Original trial-load and `cata_test` numbers below come from Claude's runs with that commit's
`cata_test`, using CI's ordering (`--rng-seed time --order lex`, split into
`"[slow] ~starting_items"` and `"~[slow] ~[.],starting_items"`). Antigravity verified the claims
against `0.I-custom`'s C++ source, core/mod JSON, `monfaction` simulation, and patch application.

## Antigravity review summary (changes from `AUDIT.md`)

Four concrete bugs/omissions were found in `AUDIT.md` and corrected inline below:

1. **C4 #2 (Portal storms):** `chargen/scenarios.json` has a **second** dead scenario extension
   right below `strong_portal_storm` — `"copy-from": "portal_dependent"` (lines 246–252). Commit
   `4d9e07a` removed both `strong_portal_storm` and `portal_dependent`; delete both.
2. **C4 #5 (CrazyCataclysm `skeltal_drops`):** Retargeting `skeltal_drops_override` →
   `skeltal_drops` and flipping `subtype` from `collection` to `distribution` with `copy-from`
   breaks the drops semantically. Core CrazyCataclysm's `skeltal_drops` is a `distribution` with
   total weight 10 (`milk: 9`, `trumpet: 1`), while Arcana's entries already embed
   `{ "distribution": [ milk (9), trumpet (1) ] }`, a monster-part distribution, and
   `essence_blood` (6–15) — each defaulting to weight 100 in a distribution. Flipping to
   `distribution` makes Mr. Skeltal drop only **one** of those three (35% milk/trumpet, 32%
   monster part, 32% blood essence) instead of all three. Redefine `skeltal_drops` as a
   `collection` without `copy-from` (or retarget `mon_zombie_skeltal.death_drops` to a collection
   referencing `skeltal_drops`).
3. **C6 (Generic Guns `gg_ammo.json`):** `shrike_misericorde_folded` (`items/ranged.json`) uses
   `"ammo": [ "flintlock" ]` and `"ammo_restriction": { "flintlock": 2 }`. Because Generic Guns
   migrates vanilla `flintlock` ammo to `ammo_black_powder` and `gg_ammo.json` retypes
   `flintlock_shot_arcana` to `ammo_black_powder`, zero `flintlock` ammo remains under Generic
   Guns. Nothing spawns `shrike_misericorde_folded` preloaded so `--mods=Arcana,generic_guns`
   loads without error, but the weapon is completely unloadable/unfireable unless `gg_ammo.json`
   also retypes `shrike_misericorde_folded` to `ammo_black_powder`.
4. **C5 (`legacy_to_hit_ids.txt`):** `stormbringer` (`items/tools.json`, `"copy-from": "zweihander"`,
   `"to_hit": 2`) is missing from the 41-ID list despite setting an explicit integer `to_hit`
   identically to `veilblade` (which is listed) and `stormbringer_on` (also listed). Neither
   `data/mods/TEST_DATA/legacy_to_hit.json` nor `itype::load` exempts it; expect 42 IDs.

Additional minor inaccuracies / optional cleanups noted inline:

- **"`extend` without `copy-from`":** `mod_interactions/magiclysm/monster_drops.json` has 4 item
  groups (`mon_owlbear_death_drops`, `mon_krabgek_death_drops`, `mon_stirge_death_drops`,
  `mon_yulecat_death_drops`) using `"extend": { "entries": [...] }` without `"copy-from"`. This is
  harmless (Magiclysm does not define those 4 groups, so `Item_factory::load_item_group` creates
  them fresh and reads `extend`), though changing them to plain `"entries"` is cleaner.
- **Monster factions (`nether`):** Simulation against `src/monfaction.cpp` and
  `tests/monfactions_test.cpp` confirms the 292 failures → 0 fix. Adding
  `"delete": { "neutral": [ "slime", "cult" ] }` alongside `"extend": { "friendly": [...] }` is a
  minor cleanup so `slime` and `cult` are not in both lists (though `friendly` wins load order).
- **0.J-era removals in upstream `fbf61ec` whose targets still exist in `0.I-custom`:**
  - `archaeologist` is still a core profession in `data/json/professions.json`, but `fbf61ec`
    moved it out of `chargen/scenarios.json` (`arcane_urban`) into
    `mod_interactions/xedra_evolved/scenarios.json`.
  - `survivor_machete` still exists in `data/json/items/melee/swords_and_blades.json` (removed
    from `martialarts.json` in `fbf61ec`).
  - `regional_overlay.json` lowered `house_arcana` / `house_arcana_2` weights from `120` / `80` to
    `50` / `35` in `fbf61ec` (reasonable on 0.I too).
- **Upstream mapgen bug:** `Lab_arcana_warehouse` in `overmap_specials.json` places
  `arcana_warehouse_lab_north` on both `z=0` and `z=1` instead of `arcana_warehouse_lab_roof_north`
  on `z=1`, leaving `arcana_warehouse_lab_roof` unused (both still need `SHOULD_NOT_SPAWN` since
  `occurrences` is `[ 0, 0 ]`; fixing `z=1` is an optional upstream bugfix).

All other assertions in `AUDIT.md` (upstream metadata/licence, `Youkai_Disco` exclusion, clean
application and JSON validation of `c2`/`c3`/`c5`, C3 counts and 0.I feature support for
`LIGHT_n`/`SPAWN_ACTIVE`/`MISSION_ITEM`/`SINGLE_USE`/`target_timer`/`workbench.mass`, `bionics_op*`
and `bionics_apophis_*` targets, Hub 01 dialogue gating, C5 counts for overmap coverage /
mutations / turrets / vehicle parts / densities, `Cata++` interaction items, tilesets, and CI
matrix wiring) were independently verified as accurate.

## Summary

- **Upstream is archived.** chaosvolt archived
  [chaosvolt/cdda-arcana-mod](https://github.com/chaosvolt/cdda-arcana-mod) on 29 April 2026
  after moving Arcana in-repo to Bright Nights. The README says the DDA version will not be
  maintained. The last change to the DDA folder (`Arcana/`) is `f414e2c9`, 15 February 2026.
- **There are two real candidates**, and they are different mods:
  - **A. chaosvolt's final DDA release**, `33bfbbe` (folder `Arcana/`): the original Arcana and
    Magic Items. It is frozen.
  - **B. Standing-Storm's continuation**, branch `0.J-Stable` at `1024574` (23 October 2026):
    "Arcana: Strange Aeons". This is a maintained personal rebalance and redesign; see Decision 1.
  - Erin105's `0.I` branch is an older, trimmed copy of A and is not recommended (see Sources).
- **Decision (owner, 25 November 2026): A.** It needs only mechanical 0.J→0.I reversions and
  loses no features. Standing-Storm's version is not pursued for now.
  After the planned fixes, every known error and test failure has a concrete fix (listed below):
  - Before fixes it loads with 131 text lints, 1 ignored field, and no missing IDs.
  - The full suite fails 7 test cases, each with an identified cause and fix.
- **Size of A:** about the same as Cataclysm++. The work is six commits (C1–C6), almost all
  JSON. The only non-mod files touched are test data, CI and the README.

## Sources

| Source | Tip | Targets | Result on 0.I-custom |
|---|---|---|---|
| chaosvolt `master` (archived) | `33bfbbe` 2026-04-29; `Arcana/` last changed `f414e2c9` 2026-02-15 | DDA experimental, early 2026 | Fatal at first: 0.J `aoe` arrays. After the mechanical reversions it loads with 131 lints and 1 ignored field. |
| Erin105 `0.I` | `f4bbe4c` 2026-10-05 | 0.I | Loads with 131 lints. Based on chaosvolt `c4566d67` (2025-07-27) plus 5 commits. |
| Standing-Storm `0.J-Stable` | `1024574` 2026-10-23 | 0.J stable | Fatal at first. Needs 7 reversion steps plus 2 audit-only stubs; then 130 errors (101 lints, 29 others). |
| Standing-Storm `master` | `080d8e9` 2026-11-01 | post-0.J experimental | As `0.J-Stable`, plus `REGEN_WOUND` (9 uses) and bleed removal (#98, #99). |

- **Erin105 is not worth importing.** Its `0.I` branch is chaosvolt's July 2025 state with
  deletions: all of `monster_drops.json`, the item-group extensions for `hive_center`, `spider`,
  `rare`, `flt_loot_rare` and `oa_ig_sb_rare`, and `monsters/monster_drops_modcompat.json`. It also
  retargets the CBM extensions to vanilla 0.I's `Zomborg_CBM_harvest_*` groups. chaosvolt's
  `master` already makes the same group changes for DDA experimental, keeps the monster drops,
  and carries seven further months of fixes. Only 34 files differ between Erin105's base and
  `master`.
- **Standing-Storm and chaosvolt diverged** after chaosvolt's #502 (`0939b107`, 2025-06-23).
  Since then Standing-Storm has made 599 commits on `0.J-Stable` and chaosvolt 114 on `master`,
  most of them in `Arcana_BN/`.

## Decision 1: which Arcana (decided)

The owner chose **A, chaosvolt's original Arcana and Magic Items**. It is the mod as its author
designed it, loads on 0.I after mechanical reversions, loses no behaviour, and is frozen
upstream, so future syncs cost nothing. The fork maintains it from here.

Standing-Storm's "Arcana: Strange Aeons" is a maintained rebalance and redesign of Arcana that
tracks 0.J. It is not pursued for now; see "Standing-Storm (not pursued)".

## Plan for option A

The commit layout follows Cataclysm++:

- raw import first;
- then separate commits for formatting, reversions, fork integration, fixes and wiring;
- all pushed together, because CI tests only the tip.

Patches in this folder use `a/data/mods/...` paths. Apply them from the repository root with
`patch -p1`, in order. Applying `c2`, `c3` and `c5` to a fresh `git archive 33bfbbe Arcana`
reproduces the audited copy cleanly (independently verified with `patch --forward` and
`build-scripts/validate_json.py`).

### C1: raw import

- **Source:** `git archive 33bfbbe Arcana`, imported into `data/mods/Arcana/`.
- **What it contains:** 188 JSON files (187 excluding `Youkai_Disco`), 3.5 MB, no `lang/` folder.
- **Exclude** `mod_interactions/Youkai_Disco/`. Youkai_Disco is not in this repository, and
  `build-scripts/get_all_mods.py` reads interaction folder names as mod IDs. The folder puts
  `Youkai_Disco` into CI's all-mods load list, which then fails with 9 missing-group errors
  (seen in Claude's all-mods run).
- **Add `UPSTREAM.md`**, recording:
  - the source and commit;
  - the archive status;
  - the licence: CC BY-SA 3.0 Unported, the same as CDDA, so it is compatible;
  - attribution to Chaosvolt;
  - the exclusion above.

### C2: formatting only

- **Patch:** `c2_format.patch`, 46 files.
- **Why first:** `json_formatter` normalises the raw files, so the later diffs show only real
  changes. Upstream is frozen, so formatting before the reversions costs nothing for future
  syncs.

### C3: 0.J→0.I reversions

Patch: `c3_reversions.patch`, 7 files.

- **`aoe` and `trail` arrays** become single objects. There are 25; all are single-element.
- **The `light` field** becomes `LIGHT_n` flags: 9 items (4× `LIGHT_50`, plus `LIGHT_8`, 12, 45,
  60 and 240). `src/item_factory.cpp` parses arbitrary `LIGHT_<n>` flags dynamically in 0.I.
- **`pasta_ingredients`** becomes 0.I's `pasta` in two mapgen files.
- **The region settings** in `overmap_and_mapgen/regional_overlay.json` are 0.J's
  `region_settings_city` with `extend.houses`. They become a 0.I `region_overlay` with
  `"city": { "houses": { "house_arcana": 50, "house_arcana_2": 35 } }`. (Note: upstream `fbf61ec`
  also lowered the weights from `120` / `80` to `50` / `35`; `50` / `35` is reasonable on 0.I too.)
- **Move into C3 at integration:** `mutations_dragonblood.json` `ARCANA_DRAGONCLAWS` has 0.J's
  `"provided_qualities": { "BUTCHER": 9 }`; in 0.I this is `"butchering_quality": 9`. This change
  is currently inside `c5_lints_plurals_butchering.patch`.
- **Verified already supported by `0.I-custom` (no reversion needed):** `SPAWN_ACTIVE`,
  `MISSION_ITEM`, `SINGLE_USE`, `target_timer` on `transform` actions, and
  `workbench.mass: "500kg"`.
- **Optional 0.I restorations from `fbf61ec`:** `archaeologist` is still a core profession in
  `0.I-custom` (`data/json/professions.json`), and `survivor_machete` still exists
  (`data/json/items/melee/swords_and_blades.json`). Upstream `fbf61ec` moved `archaeologist` out
  of `chargen/scenarios.json` (`arcane_urban`) into `mod_interactions/xedra_evolved/scenarios.json`
  and dropped `survivor_machete` from `martialarts.json`; restore either if desired.

The tool `tools/arc_revert.py` makes the mechanical reversions; it also handles the 0.J forms
seen in Standing-Storm's copy.

### C4: fork integration

1. **CBM drops from this fork's bionic zombies.**
   - chaosvolt's `master` extends only vanilla 0.I's `Zomborg_CBM_harvest_*` groups. In this
     fork those drop only from zomborgs (`mon_zomborg`, `mon_zomborg_devourer`, the labyrinth
     zomborg).
   - The fork's bio-operator zombies drop from the restored `bionics_op*` groups, so Arcana's
     CBMs would never come from them.
   - Restore the four extensions that `c4566d67` had, as was done for Cataclysm++. Keep the
     `Zomborg` ones. All four target groups are `distribution` in this fork.

   ```json
   { "id": "bionics_op", "copy-from": "bionics_op", "type": "item_group", "subtype": "distribution",
     "extend": { "items": [ [ "bio_electrothermal_arc_projector", 1 ], [ "bio_rift_focus_projector", 1 ], [ "bio_temporal_stimulation", 2 ] ] } },
   { "id": "bionics_op2_off", "copy-from": "bionics_op2_off", "type": "item_group", "subtype": "distribution",
     "extend": { "items": [ [ "bio_electrothermal_arc_projector", 3 ], [ "bio_rift_focus_projector", 2 ] ] } },
   { "id": "bionics_op2_def", "copy-from": "bionics_op2_def", "type": "item_group", "subtype": "distribution",
     "extend": { "items": [ [ "bio_life_sign_suppression", 5 ] ] } },
   { "id": "bionics_op2_utl", "copy-from": "bionics_op2_utl", "type": "item_group", "subtype": "distribution",
     "extend": { "items": [ [ "bio_temporal_stimulation", 4 ], [ "bio_essence_surge_cell", 1 ] ] } }
   ```

2. **Portal storms.** *(Revised by Antigravity)*
   - `chargen/scenarios.json` extends **two** portal-storm scenarios removed by this fork in
     `4d9e07a`: `strong_portal_storm` (lines 230–245) and `portal_dependent` (lines 246–252). 0.I
     ignores dangling scenario `copy-from` silently, so delete **both** extensions.
   - The Veilblade's `arcana_veilblade_halt_portal_storms` effect stays. It only acts during a
     storm, which here happens only through the debug menu or mod content.
   - `npcs/TALK_ROBOFAC_INTERCOM.json` only gates on `dialogue_intercom_completed_robofac_intercom_1`
     and is unaffected by the removal of Hub 01's "Hazard Meteorology" contract in `4d9e07a`.
3. **Monster factions** (`monsters/monster_factions.json`).
   - **Problem:** Arcana redefines core's `nether`, `triffid` and `cult` without `copy-from`. That
     replaces their core relations, producing 292 failed checks in `monfactions_test`.
   - **Fix:** rewrite each as `"copy-from"` plus `"extend"` (0.I's `generic_factory` supports it
     for factions).
   - **Then make every new relation mutual:**
     - `moruboru`, `archon` ↔ `nether`;
     - `moruboru` ↔ `triffid`;
     - `archon` ↔ `cult`;
     - `nether` → `slime` and `nether` → `cult` friendly, where core has these as neutral
       (optionally add `"delete": { "neutral": [ "slime", "cult" ] }` on `nether` so they are not
       listed in both `neutral` and `friendly`, though `friendly` wins load order in
       `monfaction::load`).
4. **The Cataclysm++ interaction** extends `bionics_apophis`. Our Cataclysm++ (`46982a6`) splits
   that group into `bionics_apophis_off`, `bionics_apophis_def` and `bionics_apophis_util`.
   Spread the three Arcana CBMs over those groups:
   - `bio_temporal_stimulation` → `_util`;
   - `bio_life_sign_suppression` → `_def`;
   - `bio_kinetic_amplifier` → `_off`.
5. **The CrazyCataclysm interaction** *(Revised by Antigravity)* extends `skeltal_drops_override`,
   which is `skeltal_drops` (a `distribution` of `milk: 9`, `trumpet: 1`) in this repository.
   - **Do not** simply retarget with `"copy-from": "skeltal_drops"` and `"subtype": "distribution"`:
     Arcana's `entries` already embed `{ "distribution": [ milk (9), trumpet (1) ] }`, a
     monster-part distribution, and `essence_blood` (6–15) without `prob` (defaulting to weight
     100 each), which would turn total weight into 310 and cause Mr. Skeltal to drop only one item
     instead of all three.
   - **Fix:** either redefine `skeltal_drops` as a `collection` **without** `copy-from` (keeping
     the embedded milk/trumpet `distribution` so all three entries roll), or `copy-from`
     `mon_zombie_skeltal` to point `death_drops` at a new `collection` containing
     `{ "group": "skeltal_drops" }` plus the Arcana drops.
6. **Optional cleanup in `mod_interactions/magiclysm/monster_drops.json`** *(Added by Antigravity)*:
   - `mon_owlbear_death_drops`, `mon_krabgek_death_drops`, `mon_stirge_death_drops` and
     `mon_yulecat_death_drops` use `"extend": { "entries": [...] }` without `"copy-from"`. Because
     Magiclysm does not define those groups, `Item_factory::load_item_group` creates them fresh
     and loads from `extend` (harmless), but unwrapping them to plain `"entries"` is cleaner.

### C5: lints, test data and test fixes

- **`modinfo.json`**: strip `<color_cyan>` from the name, as for Cataclysm++.
- **Lints and plurals.** `c5_lints_plurals_butchering.patch` holds:
  - 129 automatic text-style and plural fixes, from `tools/lintfix.py`;
  - explicit plurals for `cyclopean mirror (on)` and `summoned vortex`.
- **Overmap coverage:** flag 47 overmap terrains `SHOULD_NOT_SPAWN`
  (`should_not_spawn_oters.txt`).
  - All belong to eight specials with `"occurrences": [ 0, 0 ]` or mission-placed anomalies
    (`new_anomaly_1`, `new_anomaly_2`, `new_anomaly_t`, `new_anomaly_w`):
    - `lab_arcane` (24 terrains)
    - `arcana_anomaly_resurgence`
    - `4x4_microlab_arcana`
    - `sanguine_holdout`
    - `sanguine_holdout_shrikes`
    - `Cave_arcana_caravan`
    - `Lab_arcana_warehouse` *(Note: upstream bug in `overmap_specials.json` places
      `arcana_warehouse_lab_north` on both `z=0` and `z=1` instead of
      `arcana_warehouse_lab_roof_north` on `z=1`; both still need `SHOULD_NOT_SPAWN` since
      `occurrences` is `[ 0, 0 ]`, and fixing `z=1` is an optional upstream fix.)*
    - `arcana_purifer_ambushed`
  - The natural specials (Curious Structure, groves, temples, shrines, Hermit Cabin, rural
    church) were all covered.
- **Mutation categories:** set `skip_test` on `VEIL` and `DRAGONBLOOD`.
  - Breach power with all pre-threshold traits is 20 and 45, against the minimum of 55.
  - Every pre-threshold trait in both lines (10 in `VEIL`, 11 in `DRAGONBLOOD`) has `"valid": false`.
  - The thresholds are granted by `u_add_trait` in `mutations/mutation_effect_on_condition.json`.
  - This is the same situation as Cataclysm++'s Sentinel.
- **Turrets:** add `NO_TURRET` to five pseudo guns that 0.I would otherwise turn into vehicle
  turrets: `monster_fire_fake`, `monster_lightning_fake`, `monster_hammer_fake`,
  `monster_laser_fake` and `mut_dragonfire`. Core's fake monster guns carry the same flag.
- **Vehicle parts:** six parts in `vehicleparts.json` have no category. Give them `energy`:
  - `surge_generator_part`
  - `distorion_amp_motor_part`
  - the four `essence_*surge_generator_part`, best via their abstract
    `essence_surge_generator_abstract`
- **Density:** 83 items fail, from 30 objects that set weight or volume. `density_roots.txt` has
  the table; `density_failures.tsv` has every failure.
  - The two largest causes cover 51 items:
    - `scroll_magic_base` (415 g / 250 ml paper; 30 items);
    - `arcana_note_base` (3 g / 1 ml; 21 items; the same fix as Cataclysm++'s notes, 3 ml).
  - `flintlock_shot_arcana` inherits core's `flintlock_shot`, which is already in
    `known_bad_density.json`, so list it there too.
  - The full list was taken with a test binary whose 20-failure cap was raised.
  - Verified that all 4 items defined in `mod_interactions/Cata++` (`encyclopedia_arcana`,
    `unbio_kinetic_amplifier_weapon`, `unbio_electrothermal_arc_projector`,
    `unbio_rift_focus_projector`) pass density checks.
- **Legacy `to_hit`:** *(Revised by Antigravity)* add **42** IDs — the 41 in
  `legacy_to_hit_ids.txt` **plus `stormbringer`** — as a `"//": "Arcana"` entry in
  `data/mods/TEST_DATA/legacy_to_hit.json`. `stormbringer` (`items/tools.json`,
  `"copy-from": "zweihander"`, `"to_hit": 2`) sets an explicit integer `to_hit` just like
  `veilblade` and `stormbringer_on` and is not in `legacy_to_hit.json`.

### C6: interactions, CI and README

- **Generic Guns:** *(Revised by Antigravity)* add `mod_interactions/generic_guns/gg_ammo.json`
  (extending the `mod_interactions_generic_guns/gg_ammo.json` draft here). Decided: retype
  (Decision 2).
  - Generic Guns migrates `reloaded_shot_00` → `reloaded_shot_buck` and `flintlock_shot` →
    `black_powder_shot`, and these two Arcana items inherit from them:
    - `reloaded_shot_00_arcana` keeps the real `shot` type: three load errors in professions
      and the shotgun bandolier;
    - `flintlock_shot_arcana` inherits the real black-powder type in the same way.
  - **Also retype `shrike_misericorde_folded`** (`items/ranged.json`): it uses
    `"ammo": [ "flintlock" ]` and `"ammo_restriction": { "flintlock": 2 }`. Generic Guns migrates
    all vanilla `flintlock` ammo to `ammo_black_powder` and does not auto-retype mod guns, so
    without this entry `shrike_misericorde_folded` cannot load any ammo under Generic Guns:

    ```json
    {
      "id": "shrike_misericorde_folded",
      "copy-from": "shrike_misericorde_folded",
      "type": "ITEM",
      "subtypes": [ "GUN", "ARTIFACT" ],
      "//": "Generic Guns replaces flintlock ammo with generic black powder cartridges.",
      "ammo": [ "ammo_black_powder" ],
      "pocket_data": [ { "pocket_type": "MAGAZINE", "rigid": true, "ammo_restriction": { "ammo_black_powder": 2 } } ]
    }
    ```

  - `blun_shot_arcana` needs nothing: Generic Guns keeps `blun_shot` and `blunderbuss`.
- **CI:** add an `Arcana` job to the `mod_tests` matrix in `.github/workflows/matrix.yml`, as for
  Cataclysm++.
- **README:** add an Arcana section: source, licence, and what was adapted.

### Verification

1. A clean load of `--mods=Arcana`. Then load each interaction pairing:
   - Cataclysm++
   - DinoMod
   - Aftershock
   - CrazyCataclysm
   - Magiclysm
   - Xedra Evolved
   - Generic Guns
   - Mind Over Matter
   - Bionic Professions

   In Claude's audit all were clean except the issues fixed in C4 and C6.
2. The full lex-ordered suite with `--mods=Arcana`.
3. The all-mods load through `get_all_mods.py`.
4. The core suite.
5. CI's JSON checks:
   - `validate_json.py`;
   - `make style-all-json-parallel RELEASE=1`;
   - the Generic Guns and gun-variant validators.
6. actionlint.

## Findings for option A

- **Full suite before fixes:**
  - the slow half fails 1 of 16 test cases (overmap coverage);
  - the other half fails 6 of 1131 (density, `to_hit`, monster factions, breach power, vehicle
    part categories, vehicle turrets).
- **All-mods load before fixes:** 16 errors. 9 come from the Youkai_Disco folder (C1); 2 each
  from the Cataclysm++ and CrazyCataclysm retargets (C4), duplicated because both all-mods
  sets load those mods; and 3 from Generic Guns (C6).
- **No destructive overrides of core:** *(Clarified by Antigravity)*
  - Arcana's same-ID `monstergroup`s (`"override": false`), `talk_topic`s and `requirement`s
    (`extend`) all add to what is there.
  - Magiclysm and Xedra Evolved extend the same requirements; extensions stack.
  - No object destructively wipes a core or mod item group via `extend`-without-`copy-from` (the
    Cataclysm++ pitfall). The 4 `extend`-without-`copy-from` item groups in
    `mod_interactions/magiclysm/monster_drops.json` are brand-new group IDs not defined by
    Magiclysm, so they are harmless (cleanup noted in C4 #6).
- **Fork content:** *(Revised by Antigravity)*
  - Arcana's Exodii references (salvage loot and deconstruction recipes) resolve; this fork
    keeps the Exodii items.
  - References to the fork's restored sci-fi items are cosmetic: `looks_like: plasma_rifle`
    and text mentioning the mininuke.
  - Nothing references removed content apart from `strong_portal_storm` and `portal_dependent`
    (C4 #2).
- **Tilesets:** they target `UltimateCataclysm` and `MshockXottoplus`, both shipped in `gfx/`,
  plus UndeadPeople, which simply goes unused here.

## Standing-Storm (not pursued)

Measured before the decision, on a working copy of `0.J-Stable` at `1024574`. It needed:

- six reversion steps, in `standing_storm_0J_steps.txt` and
  `standing_storm_0J_reversions_incl_audit_stubs.patch`;
- three choices between dropping and backporting 0.J features:
  - the `BLEEDING_RATE` enchantment value;
  - briar witchery's vitamin-powered `energy_source`;
  - the `forest` relic recharge type.

After those it still lacked:

- 0.J spell conditions and other fields;
- five core flags;
- a weak-point set;
- the cabin cellar mapgen;
- one item group.

Its slow test half also failed overmap coverage for 51 terrains, including naturally spawning
locations. The other half was not completed. These files are kept in case the choice is
revisited.

## Decisions

All five were decided by the owner on 25 November 2026, each as recommended.

| # | Decision | Owner's decision |
|---|---|---|
| 1 | Which Arcana | **A**, chaosvolt `33bfbbe` |
| 2 | Generic Guns: retype or migrate the two shells | **Retype**, using the included draft (plus `shrike_misericorde_folded` per this revision). Migrating, as Cataclysm++ did for its cartridges, would delete the blessed shells and their recipes under Generic Guns. |
| 3 | Restore the `bionics_op*` CBM extensions | **Yes**, for parity with Cataclysm++ |
| 4 | Drop the dead portal-storm scenario extensions (`strong_portal_storm`, `portal_dependent`) | **Yes** |
| 5 | CI job for Arcana | **Yes**, as for Cataclysm++ |

## Files in this folder

- `AUDIT.md`: Claude's original audit (left untouched).
- `AUDIT_antigravity.md`: this file (Antigravity's sanity-checked revision).
- `c2_format.patch`, `c3_reversions.patch`, `c5_lints_plurals_butchering.patch`: option A
  patches, against `33bfbbe`.
- `mod_interactions_generic_guns/gg_ammo.json`: Claude's Generic Guns interaction draft (add the
  `shrike_misericorde_folded` entry from C6 above at integration).
- `density_roots.txt`, `density_failures.tsv`: the density work list.
- `legacy_to_hit_ids.txt`: 41 IDs (add `stormbringer` for 42 total at integration).
- `should_not_spawn_oters.txt`: 47 terrains.
- `standing_storm_0J_reversions_incl_audit_stubs.patch`, `standing_storm_0J_steps.txt`: the
  Standing-Storm working copy (not pursued).
- `tools/`: `arc_revert.py` (mechanical reversions), `lintfix.py` (applies lint fixes from a
  `cata_test` log), `arc_strip.py` (audit-only enchantment stripping), and `aload.sh`,
  `awork.sh` and `arc_suite.sh` (trial-load and suite helpers; set `S` to the scratch
  directory first).

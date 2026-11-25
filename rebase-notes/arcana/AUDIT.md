# Arcana: in-repo integration audit

Audited against `0.I-custom` at `fff2ed74a1` (release `0.I-custom-2026-11-25-1038`), 25 November 2026.
Every number below comes from trial loads or test runs with that commit's `cata_test`, using CI's
ordering (`--rng-seed time --order lex`, split into `"[slow] ~starting_items"` and
`"~[slow] ~[.],starting_items"`), unless stated otherwise.

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
- **Recommendation: A.** It needs only mechanical 0.J→0.I reversions and loses no features.
  After the planned fixes, every known error and test failure has a concrete fix (listed below):
  - Before fixes it loads with 131 text lints, 1 ignored field, and no missing IDs.
  - The full suite fails 7 test cases, each with an identified cause and fix.
  - B, by contrast, needs reversions of 0.J engine features, and some of its behaviour would be
    lost or need engine backports.
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

## Decision 1: which Arcana

**A. chaosvolt's original (recommended).**

- For:
  - It is the mod as its author designed it.
  - It loads on 0.I after small, purely mechanical reversions.
  - It loses no behaviour.
  - Upstream is frozen, so future syncs cost nothing.
- Against:
  - No upstream bug fixes from here on; the fork maintains it.
  - Some of Standing-Storm's 599 commits are bug fixes that A lacks. They are mixed in with the
    rebalance and not separable without review.

**B. Standing-Storm's "Strange Aeons".** Its `Adjustments.md` lists the design changes:

- an Incantation skill for casting;
- spell failure chances;
- pattern scrolls that can fail to teach;
- essences that can no longer be converted into one another (renamed Essentia, Vitae,
  Residuum, plus a new Gramina);
- blood magic learnable by anyone, with sacrifice;
- summoning as its own magic type;
- harder healing and fewer book drops;
- magitech moved out of the base mod (it needs Magiclysm or Bionic Professions);
- briar witchery, a new magic type marked "heavily WIP".

For and against B:

- For: actively maintained, more content.
- Against:
  - It is a different game from A.
  - It tracks 0.J, and `master` already uses post-0.J mechanics, so every sync repeats the
    reversions.
  - Several features need engine backports or are lost on 0.I (see Option B costs).

## Plan for option A

The commit layout follows Cataclysm++:

- raw import first;
- then separate commits for formatting, reversions, fork integration, fixes and wiring;
- all pushed together, because CI tests only the tip.

Patches in this folder use `a/data/mods/...` paths. Apply them from the repository root with
`patch -p1`, in order. Applying `c2`, `c3` and `c5` to a fresh `git archive 33bfbbe Arcana`
reproduces the audited copy exactly (checked with `diff -r`).

### C1: raw import

- **Source:** `git archive 33bfbbe Arcana`, imported into `data/mods/Arcana/`.
- **What it contains:** 188 JSON files, 3.5 MB, no `lang/` folder.
- **Exclude** `mod_interactions/Youkai_Disco/`. Youkai_Disco is not in this repository, and
  `build-scripts/get_all_mods.py` reads interaction folder names as mod IDs. The folder puts
  `Youkai_Disco` into CI's all-mods load list, which then fails with 9 missing-group errors
  (seen in this audit's all-mods run).
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
  60 and 240).
- **`pasta_ingredients`** becomes 0.I's `pasta` in two mapgen files.
- **The region settings** in `overmap_and_mapgen/regional_overlay.json` are 0.J's
  `region_settings_city` with `extend.houses`. They become a 0.I `region_overlay` with
  `"city": { "houses": { "house_arcana": 50, "house_arcana_2": 35 } }`.
- **Move into C3 at integration:** `mutations_dragonblood.json` `ARCANA_DRAGONCLAWS` has 0.J's
  `"provided_qualities": { "BUTCHER": 9 }`; in 0.I this is `"butchering_quality": 9`. This change
  is currently inside `c5_lints_plurals_butchering.patch`.

The tool `tools/arc_revert.py` makes these changes mechanically; it also handles the 0.J forms
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

2. **Portal storms.**
   - `chargen/scenarios.json` extends `strong_portal_storm`, a scenario this fork removed. 0.I
     ignores the dangling `copy-from` silently, so delete the extension.
   - The Veilblade's `arcana_veilblade_halt_portal_storms` effect stays. It only acts during a
     storm, which here happens only through the debug menu or mod content.
3. **Monster factions** (`monsters/monster_factions.json`).
   - **Problem:** Arcana redefines core's `nether`, `triffid` and `cult` without `copy-from`. That
     replaces their core relations, producing 292 failed checks in `monfactions_test`.
   - **Fix:** rewrite each as `"copy-from"` plus `"extend"` (0.I's `generic_factory` supports it
     for factions).
   - **Then make every new relation mutual:**
     - `moruboru`, `archon` ↔ `nether`;
     - `moruboru` ↔ `triffid`;
     - `archon` ↔ `cult`;
     - `nether` → `slime` and `nether` → `cult` friendly, where core has these as neutral.
4. **The Cataclysm++ interaction** extends `bionics_apophis`. Our Cataclysm++ (`46982a6`) splits
   that group into `bionics_apophis_off`, `bionics_apophis_def` and `bionics_apophis_util`.
   Spread the three Arcana CBMs over those groups:
   - `bio_temporal_stimulation` → `_util`;
   - `bio_life_sign_suppression` → `_def`;
   - `bio_kinetic_amplifier` → `_off`.
5. **The CrazyCataclysm interaction** extends `skeltal_drops_override`, which is
   `skeltal_drops` in this repository. Retarget it and change its subtype from `collection` to
   `distribution`, to match.

### C5: lints, test data and test fixes

- **`modinfo.json`**: strip `<color_cyan>` from the name, as for Cataclysm++.
- **Lints and plurals.** `c5_lints_plurals_butchering.patch` holds:
  - 129 automatic text-style and plural fixes, from `tools/lintfix.py`;
  - explicit plurals for `cyclopean mirror (on)` and `summoned vortex`.
- **Overmap coverage:** flag 47 overmap terrains `SHOULD_NOT_SPAWN`
  (`should_not_spawn_oters.txt`).
  - All belong to eight specials with `"occurrences": [ 0, 0 ]`; missions and scenarios place
    them:
    - `lab_arcane` (24 terrains)
    - `arcana_anomaly_resurgence`
    - `4x4_microlab_arcana`
    - `sanguine_holdout`
    - `sanguine_holdout_shrikes`
    - `Cave_arcana_caravan`
    - `Lab_arcana_warehouse`
    - `arcana_purifer_ambushed`
  - The natural specials (Curious Structure, groves, temples, shrines, Hermit Cabin, rural
    church) were all covered.
- **Mutation categories:** set `skip_test` on `VEIL` and `DRAGONBLOOD`.
  - Breach power with all pre-threshold traits is 20 and 45, against the minimum of 55.
  - Every pre-threshold trait in both lines has `"valid": false`.
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
- **Legacy `to_hit`:** add 41 IDs (`legacy_to_hit_ids.txt`) as a `"//": "Arcana"` entry in
  `data/mods/TEST_DATA/legacy_to_hit.json`.

### C6: interactions, CI and README

- **Generic Guns:** add `mod_interactions/generic_guns/gg_ammo.json`
  (`mod_interactions_generic_guns/gg_ammo.json` here). See Decision 2.
  - Generic Guns migrates `reloaded_shot_00` → `reloaded_shot_buck` and `flintlock_shot` →
    `black_powder_shot`, and these two Arcana items inherit from them:
    - `reloaded_shot_00_arcana` keeps the real `shot` type: three load errors in professions
      and the shotgun bandolier;
    - `flintlock_shot_arcana` inherits the real black-powder type in the same way.
  - The draft retypes both to `ammo_shot` and `ammo_black_powder`. With it,
    `--mods=Arcana,generic_guns` loads without Arcana errors.
  - `blun_shot_arcana` needs nothing: Generic Guns keeps `blun_shot`.
- **CI:** add an `Arcana` job to the `mod_tests` matrix, as for Cataclysm++.
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

   In this audit all were clean except the three issues fixed in C4 and C6.
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
- **No destructive overrides of core:**
  - Arcana's same-ID `monstergroup`s (`"override": false`), `talk_topic`s and `requirement`s
    (`extend`) all add to what is there.
  - Magiclysm and Xedra Evolved extend the same requirements; extensions stack.
  - No object uses `extend` without `copy-from`, the mistake that wiped Cataclysm++'s item
    groups.
- **Fork content:**
  - Arcana's Exodii references (salvage loot and deconstruction recipes) resolve; this fork
    keeps the Exodii items.
  - References to the fork's restored sci-fi items are cosmetic: `looks_like: plasma_rifle`
    and text mentioning the mininuke.
  - Nothing references removed content apart from `strong_portal_storm` (C4).
- **Tilesets:** they target `UltimateCataclysm` and `MshockXottoplus`, both shipped in `gfx/`,
  plus UndeadPeople, which simply goes unused here.

## Option B costs (Standing-Storm `0.J-Stable`)

Measured on a working copy, `standing_storm_0J_reversions_incl_audit_stubs.patch` (steps in
`standing_storm_0J_steps.txt`).

**Reversions (R1–R6):**

- R1: the same mechanical set as A, but larger. 28 NPC `mission` names become 0.I enum
  numbers: `GUARD` 7, `SHOPKEEP` 3, `GUARD_PATROL` 8.
- R2: rewrite `region_overlay.json` from 0.J's `region_settings_city`, `forest_biome_mapgen`
  and eight `map_extra_collection` extensions into one 0.I `region_overlay`.
- R3: `tools_robotics` is a `distribution` in 0.I.
- R4: 0.J's string `limb_types` becomes `limb_type` on four draconic body parts.
- R5: drop three `effect_migration` entries. Rewrite the Innawood interaction's region file.
- R6: remove 40 `travel_cost_type` values (`basement`, `roof`, `structure`) that 0.I lacks.

**Decisions B would need:**

- `forest` relic recharge on two items: `periodic`, or backport 0.J's recharge types (R7 in
  the working copy used `periodic`).
- `BLEEDING_RATE` (5 uses): drop it, or backport the 0.J enchantment value (an enum entry and
  two call sites).
- Briar witchery's vitamin-powered `energy_source`: backport 0.J's object form of
  `energy_source`, or rework it (the working copy stubbed it as `NONE`).

**What 0.I would still ignore or miss after that:**

- spell `caster_condition` and `target_condition`: 8, so the casting restrictions would vanish;
- `similar_bodypart`: 6;
- `requires_any_traits`, `provided_qualities` and `stamina`: 1 each;
- `chargen_allow_npc`: 2;
- cosmetic fields: `name` ×20, `light_color` ×4, `sun_sym` ×7;
- missing core IDs:
  - monster flags `LOCKS_ON`, `INFRARED_VISION`, `UNBREAKABLE_MORALE` and `PLANT_BLOOD`;
  - item flag `LOCATION_PRECISE_CLOSEST_CITY`;
  - weak-point set `wps_eyes`;
  - nested mapgen `cabin_cellar_stairs` and palette `cabin_cellar` (used by `cabin_3` to
    `cabin_6`);
  - item group `esoteric_books`;
- 101 lints.

**Full suite:** see "Option B test results" below.

## Decisions

| # | Decision | Recommendation |
|---|---|---|
| 1 | Which Arcana | A, chaosvolt `33bfbbe` |
| 2 | Generic Guns: retype or migrate the two shells | Retype (draft included). Migrating, as Cataclysm++ did for its cartridges, would delete the blessed shells and their recipes under Generic Guns. |
| 3 | Restore the `bionics_op*` CBM extensions | Yes, for parity with Cataclysm++ |
| 4 | Drop the dead `strong_portal_storm` scenario extension | Yes |
| 5 | CI job for Arcana | Yes, as for Cataclysm++ |
| 6 | Only if B: `BLEEDING_RATE`, briar witchery energy, `forest` recharge | Decide each between dropping and backporting |

## Files in this folder

- `AUDIT.md`: this file.
- `c2_format.patch`, `c3_reversions.patch`, `c5_lints_plurals_butchering.patch`: option A
  patches, against `33bfbbe`.
- `mod_interactions_generic_guns/gg_ammo.json`: the Generic Guns interaction draft.
- `density_roots.txt`, `density_failures.tsv`: the density work list.
- `legacy_to_hit_ids.txt`: 41 IDs.
- `should_not_spawn_oters.txt`: 47 terrains.
- `standing_storm_0J_reversions_incl_audit_stubs.patch`, `standing_storm_0J_steps.txt`: the
  option B working copy.
- `tools/`: `arc_revert.py` (mechanical reversions), `lintfix.py` (applies lint fixes from a
  `cata_test` log), `arc_strip.py` (audit-only enchantment stripping), and `aload.sh`,
  `awork.sh` and `arc_suite.sh` (trial-load and suite helpers; set `S` to the scratch
  directory first).

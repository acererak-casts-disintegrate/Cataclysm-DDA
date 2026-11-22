## Final test results for 0.I-custom (3973b8f39a)

Full `cata_test` runs, one per mod set, on 2026-11-22. The `try_parse_int_locale_parsing`, `string_formatter` and `point_to_from_string` lines in the logs are warnings about locales the build container lacks, not failures.

### xedra_evolved: 1139 / 1147

| Test | Cause | Status |
|---|---|---|
| `monsters_spawn_eggs`, `monsters_spawn_egg_itemgroups`, `monsters_spawn_baby_groups`, `monsters_spawn_babies`, `limit_mod_size_bonus` | Order-dependent state leak; pure 0.I fails the same set | upstream, leave |
| `nutrients_in_food` | Ice cream iteminfo shows 51 kcal against the expected 53 | upstream test brittleness, leave |
| `All_valid_mutations_can_be_purified` | `air_sprite` is purifiable; upstream master marks it `"purifiable": false` (missed by the 366-trait pass, which only matched upper-case ids) | to fix: backport flag |
| `vehicle_parts_seats_and_beds_have_beltable_flags` | `floral_boat_hull` is a seat without `BELTABLE`/`NONBELTABLE`; upstream master adds `BELTABLE` | to fix: backport flag |

### mindovermatter: 1142 / 1147

Only the five order-dependent failures (`monsters_spawn_*` ×4, `limit_mod_size_bonus`) that pure 0.I shares. Purifier coverage, overmap coverage and the to-hit list pass.

### aftershock: 1141 / 1147

| Test | Cause | Status |
|---|---|---|
| `monsters_spawn_*` ×4, `limit_mod_size_bonus` | Order-dependent leak shared with pure 0.I | upstream, leave |
| `overmap_terrain_coverage` | `basement_bionic_decoy` never spawns: Aftershock redefines core `house_09` with its own `basement_bionic` basement, leaving the core decoy basement no other spawn path | to fix: flag it `SHOULD_NOT_SPAWN` from Aftershock (as Mind Over Matter does for its disabled lab terrains), or stop overriding `house_09`. The bionic professions package has the same override in upstream 0.I |

### magiclysm: 1141 / 1147

| Test | Cause | Status |
|---|---|---|
| `monsters_spawn_*` ×4, `limit_mod_size_bonus` | Order-dependent leak shared with pure 0.I | upstream, leave |
| `mission_goal_condition_test` (no-origin mission completes when the condition is met) | Passes in isolation on pure 0.I with Magiclysm. `game::find_npc` searches the whole overmap buffer, so an id-less NPC left by an earlier test would satisfy the mission's `npc_id != _npc_id` check (both −1). Passes in isolation on 0.I-custom with Magiclysm too, and in the full core run, so it depends on test order; the leaking test is not yet identified | investigate |

### package_bionic_professions: 1140 / 1147

| Test | Cause | Status |
|---|---|---|
| `monsters_spawn_*` ×4, `limit_mod_size_bonus` | Order-dependent leak shared with pure 0.I | upstream, leave |
| `overmap_terrain_coverage` | `basement_bionic_decoy` never spawns: the package redefines core `house_09` with its `basement_bionic`, the decoy's only spawn path. Upstream 0.I ships this override unchanged | upstream bug; to fix: flag the decoy `SHOULD_NOT_SPAWN` from the package |
| `mission_goal_condition_test` | Same as under Magiclysm | investigate |

The first run of this suite was cut off by the background time limit at test 786 and was rerun in full.

### core: 1142 / 1147

Only the five order-dependent failures (`monsters_spawn_*` ×4, `limit_mod_size_bonus`) that pure 0.I shares. The earlier 1140 / 1147 included the battery density and expected DPS regressions, both fixed in 2366109dcc. `mission_goal_condition_test` passes.

### To fix next

1. Backport `"purifiable": false` for Xedra's `air_sprite` and `BELTABLE` for `floral_boat_hull` from upstream master.
2. Flag `basement_bionic_decoy` `SHOULD_NOT_SPAWN` from Aftershock and from the bionic professions package (or drop their `house_09` overrides).
3. Find the test that leaves an id-less NPC in the overmap buffer before `mission_goal_condition_test` when Magiclysm or the bionic professions package is loaded.

Left alone: the order-dependent `monsters_spawn_*` / `limit_mod_size_bonus` failures and Xedra's `nutrients_in_food`, all present on pure 0.I.

## Follow-up fixes (e93240b09d)

| Commit | Fix |
|---|---|
| 8b83f4ac01 | Xedra `air_sprite` non-purifiable and `floral_boat_hull` `BELTABLE`, from upstream master |
| 32aef4d076 | Aftershock and the bionic professions package flag `basement_bionic_decoy` `SHOULD_NOT_SPAWN` |
| e93240b09d | `overmapbuffer::find_npc` matches no NPC for an invalid id. The leak behind `mission_goal_condition_test`: tests such as `EOC_transform_line` leave id-less NPCs in the overmap buffer, and the giverless mission then found one and completed. In core, that pair alone reproduced the failure |

Reruns on e93240b09d: magiclysm, package_bionic_professions and core each 1142 / 1147, failing only the five order-dependent tests shared with pure 0.I. Targeted reruns: Xedra purifier and beltable tests pass; overmap coverage passes with Aftershock and with the package; 143 NPC, EOC, mission and character test cases pass.

Still left alone: the five order-dependent failures and Xedra's `nutrients_in_food`, all present on pure 0.I.

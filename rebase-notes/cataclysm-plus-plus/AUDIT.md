# Cataclysm++ in-repo integration: audit of the implementation plan

Status: **plan audited, not executed.** Nothing has been added to `0.I-custom`.

- Plan under audit: [`antigravity_plan.md`](antigravity_plan.md) (written by Google Antigravity; kept verbatim).
- Source: [`Noctifer-de-Mortem/nocts_cata_mod`](https://github.com/Noctifer-de-Mortem/nocts_cata_mod), folder `nocts_cata_mod_DDA`, commit `46982a6` (9 November 2026), The Unlicense.
- Target: `0.I-custom` at `94a8e183d2`.
- Method: static checks of every factual claim against the source and `0.I-custom`, an ID collision audit, and trial loads with `0.I-custom`'s `cata_test` in a throwaway data-only worktree.

## Owner's decisions so far

| # | Decision | Owner's position |
|---|---|---|
| 1 | Generic Guns compatibility | **Undecided.** Not sure about `conflicts`; see the investigation below. |
| 2 | Delete Cataclysm++'s `mon_laserturret` override | Agrees with the plan's recommendation |
| 3 | Bionic zombie CBM drops: restore `fbd4aad` and extend the `bionics_op2_*` and `bionics_sci` groups | Agrees with the plan's recommendation |
| 4 | Add the legacy numeric `to_hit` items to `TEST_DATA/legacy_to_hit.json` | Agrees with the plan's recommendation |
| 5 | Prepper's `knife_rambo` goes in a `scabbard` | Agrees with the plan's recommendation |
| 6 | Restore the CVD machine, `atomic_lamp` and the old lab scenario extensions | Agrees with the plan's recommendation, **subject to the correction in finding 2** |
| 7 | Keep `legacy.json`; flag `b_field` `SHOULD_NOT_SPAWN` | Agrees with the plan's recommendation |
| 8 | CI coverage for Cataclysm++ | **Undecided.** See the investigation below. |

## Findings: problems the plan misses

1. **Three core item groups are wiped.** Cataclysm++ edits `antique_ammo`, `museum_guns` and `on_hand_flintlock` with `"extend"` but no `"copy-from"`. In 0.I `Item_factory::load_item_group` resets a group that has no `copy-from` ("Otherwise, unconditionally overwrite"), so each group ends up holding only `flintlock_ammo_mine`; museums would lose their guns, for example. **Fix:** add `"copy-from"` with the same id to all three. The mod's other 56 `extend` groups already use `copy-from`.
2. **Decision 6's scenario claim is false.** `lab_cargo_mutant` does not exist in 0.I; only upstream master has it. The trial load raised no error for the extension, so it would silently vanish. In 0.I the mutant lab start is `lab_chal`. **Fix:** extend `lab_chal`, `lab_staff` and `lab_cargo_staff_1`, and drop the `lab_cargo_mutant` extension. The CVD terrains (`t_cvdbody`, `t_cvdmachine`) and the `atomic_lamp` vehicle part do exist in 0.I.
3. **The density test fails on 23 items, not 20.** The plan's static audit missed `36navy_makeshift_magnum`, `44army_makeshift_magnum` and `flintlock_ammo_mine`; the test's stop after 20 failures hid them. All three are ammo, whose volume is per stack, so they need stack-aware fixes. "Zero `known_bad_density` additions" is not yet established. Full list: [`density_failures.txt`](density_failures.txt), taken from a run with the cap lifted.
4. **The legacy `to_hit` count of 93 is correct.** An earlier version of this audit said 92 because of an extraction bug: `fr_762R` contains a capital letter. Use the list in [`legacy_to_hit_ids.txt`](legacy_to_hit_ids.txt), taken from the test output.
5. **The file inventory is wrong.**
   - The import list omits the top-level `c_achievements.json`. It loads cleanly and should be kept.
   - The tileset filenames are wrong. The real files are `Ultica_Expan_{Normal,Tall,Huge}.png` and `expan_dp_{normal,large}.png`, with five JSON files: `mod_tileset_DP_{Large,Normal}.json` and `mod_tileset_Ultica_{normal,tall,huge}.json`.
   - This is harmless if the whole folder is copied. Compatibility is fine: they target `UltimateCataclysm` and `MshockXottoplus`, both in `gfx/`.
6. **"0 failures" is not attainable locally.** Five order-dependent tests (`monsters_spawn_*` ×4 and `limit_mod_size_bonus`) fail on pure 0.I when the suite runs in one process. CI's split layout passes them. Success should mean "no failures beyond the baseline in `../final_test_results.md`".
7. **Dropping `lang/` loses the mod's own translations,** including Russian. This fork deleted upstream's translation workflows, so nothing replaces them. English play is unaffected.
8. **There is no plan for future Cataclysm++ updates.** Upstream is active. Suggested layout:
   - commit the raw `46982a6` snapshot (minus the excluded paths) on its own;
   - put the 0.I reversions and fixes in separate commits;
   - record the base commit in the mod folder.

   Later upstream ranges can then be diffed and replayed.

## Verified correct

- **Component 1 (exclusions):** `Surv_help/c_override.json` and `Weapons/c_ranged_override.json` override exactly the restored `bot_laserturret`, `broken_laserturret` and `laser_cannon`. Cataclysm++'s laser cannon has armour penetration 4; ours has 15. Dropping `mod_interactions/` is right: `build-scripts/get_all_mods.py` adds each `mod_interactions/<id>` folder name as a mod id, so `doom` and `PK_REBALANCE` would break CI's all-mods load.
- **ID collisions:** of the mod's 110 ids shared with core, only four collide with content this fork restored, and they are exactly the plan's four laser entries. The other redefinitions are monster groups, vehicle groups and a talk topic, all of which merge in 0.I rather than replace. The three item groups in finding 1 are the exception. Full list: [`id_collisions.txt`](id_collisions.txt).
- **Component 2 (0.J to 0.I reversions):**
  - NPC `mission` strings map to the 0.I `npc_mission` values GUARD 7, SHOPKEEP 3 and GUARD_PATROL 8.
  - `aoe` and `trail` become single objects, as `ammo_effect.cpp` reads them.
  - `light` fields go back to `LIGHT_n` flags; 0.I has no `light` field. Upstream `8ad7f0f`'s other change, `copy-from: armor_lc_leg_guard`, is valid in 0.I and needs no reversion.
  - `pasta_ingredients` becomes `pasta`.
  - `regional_overlay.json` is restored from `02fc4e8^`.

  With these applied the mod loads, and the remaining errors are exactly the plan's lint and translation list plus the Prepper knife. The patch is [`component2_reversions.patch`](component2_reversions.patch), against the raw `46982a6` folder.
- **Component 3:** all seven target groups exist in `data/json/itemgroups/bionics.json` and are `distribution` groups. The `dissect_CBM_*` mapping is as described, and `fbd4aad` removed exactly the `bionics_op`, `bionics_tech` and `bionics_subs` extensions the plan restores.
- **Decision 2:** Cataclysm++ fully redefines `mon_laserturret` with aggression 50; ours has 100. Deleting the override is right.
- **Decision 5:** `knife_rambo` does not fit the `SHEATH_KNIFE` `sheath`; `scabbard` accepts `SHEATH_SWORD`.
- **Decision 7:** `overmap_terrain_coverage` with the mod loaded reports exactly one missing terrain, `b_field`.
- **Other claims:**
  - There are no Exodii, Rubik or portal-storm references. `mx_portal` and `mx_portal_in` are map extras, not storms.
  - The battery density test skips non-`dda` items.
  - `--check-mods` exists in 0.I.
  - The fire-mode label fix matches core's `"5 rd."` convention.

## Decision 1: Generic Guns, investigated

- **What `conflicts` does:** it is a hard block. The mod manager refuses to add the second mod ("Unable to add %s. It is incompatible with a currently active mod."). In-repo precedent: `Isolation-Protocol` and `aftershock_exoplanet` both conflict with `generic_guns`.
- **What breaks with both loaded:** the trial load produced five errors, all from two professions whose `36navy_makeshift_magnum` and `44army_makeshift_magnum` don't fit Generic Guns' `black_powder_revolver` (the migrated `colt_navy` and `colt_army`) or its `flintlock_pouch`.
- **The bigger issue:** about 15 of Cataclysm++'s 59 new guns use real calibres. These are `surv_full_{9mm,45,22,223,308,762,762R,3006,50,12}` and `surv_lmg_{223,308,762,762R,3006}`. Generic Guns converts real ammo items to generic ones, so in a Generic Guns world those guns could never be loaded.

Options:

| Option | Work | Result |
|---|---|---|
| (a) `"conflicts": [ "generic_guns" ]` | none | The two mods can't be combined; CI's all-mods load splits them automatically. |
| (b) The plan's alternative: patch the two professions only | small | The errors go away, but about 15 guns stay unusable in Generic Guns worlds. **Not recommended.** |
| (c) Compatibility layer: `data/mods/Cataclysm++/mod_interactions/generic_guns/` holding about 20 `MIGRATION` entries | small to moderate | Both mods stay usable. Mappings: the makeshift magnums to `black_powder_ball`; the survivor guns to Generic Guns' `pistol_*`, `rifle_*`, `rifle_lmg`, `rifle_huge_amr` and shotgun generics. The file loads only when Generic Guns is active, and CI's all-mods load then covers the pair. |

**Recommendation: (c), with (a) as the fallback** if the trial turns up something awkward. The `flintlock_pouch` case needs a test. Option (c) uses migrations only, which avoids the duplicate-definition limit documented in `doc/MOD_COMPATIBILITY.md`.

## Decision 8: CI, investigated

- **Cost:** standard GitHub-hosted runners are free and unlimited for public repositories; only larger runners are billed. Sources: [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) and [runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing).
- **What CI already does:** the kept Linux job in `.github/workflows/matrix.yml` has `TEST_STAGE` set. `build-scripts/gha_test_only.sh` therefore already runs `[force_load_game]` for every mod group from `get_all_mods.py`, so Cataclysm++ would be load-tested with no workflow change. The same job runs the full suite with Magiclysm only.

| Option | What it catches | Cost |
|---|---|---|
| (a) The plan's recommendation: all-mods load plus `json.yml` | Load and consistency errors only | none |
| (b) A dedicated `--mods=Cata++` full-suite job | Also behavioural failures (density, to_hit, purification, coverage, starting items) | One more parallel runner per push, about 35–40 minutes to compile plus a similar time for tests; turnaround time unchanged |
| (c) Per-mod full-suite jobs for every mod this fork maintains (Cataclysm++, Aftershock, Xedra Evolved, Mind Over Matter, bionic professions; Magiclysm is already covered) | The local six-suite baseline, automated | Several parallel runners; each compiles separately; any mod's failure turns the push red |

**Recommendation: at least (b).** Cataclysm++ tracks upstream's development branch, so it is the mod most likely to drift. Choose (c) if the whole mod baseline should run on every push.

## Resuming

1. Create a data-only worktree of `0.I-custom`:

   ```bash
   git worktree add --no-checkout --detach "$S/cpp_wt" origin/0.I-custom
   ```

   ```bash
   cd "$S/cpp_wt" && git sparse-checkout set --no-cone /data/ /tools/ /build-scripts/ /Makefile && git checkout
   ```
2. Copy `nocts_cata_mod_DDA` at `46982a6` to `data/mods/Cataclysm++/`, without `mod_interactions/`, `lang/` and `README_DDA.md`.
3. From the worktree root, apply the Component 2 patch:

   ```bash
   patch -p1 < component2_reversions.patch
   ```
4. Trial-load with [`cload.sh`](cload.sh). It uses a `cata_test` built from `0.I-custom`; set `S` to the scratch directory and edit the binary path inside if needed.

Then apply findings 1–3 and Decisions 1–8 as decided.

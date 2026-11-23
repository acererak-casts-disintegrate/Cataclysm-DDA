# Cataclysm++ in-repo integration: audit of the implementation plan

Status: **plan audited, not executed.** Nothing has been added to `0.I-custom`.

- Plan under audit: [`antigravity_plan.md`](antigravity_plan.md) (written by Google Antigravity; kept verbatim).
- Source: [`Noctifer-de-Mortem/nocts_cata_mod`](https://github.com/Noctifer-de-Mortem/nocts_cata_mod), folder `nocts_cata_mod_DDA`, commit `46982a6` (9 November 2026), The Unlicense.
- Target: `0.I-custom` at `94a8e183d2`.
- Method: static checks of every factual claim against the source and `0.I-custom`, an ID collision audit, and trial loads with `0.I-custom`'s `cata_test` in a throwaway data-only worktree.

**Revision 2.** Antigravity reviewed revision 1 of this audit. Each of its points was re-checked against `0.I-custom`'s source or by trial load. This revision keeps what held up, corrects what didn't (marked *Corrected*), and adds what both reviews missed (marked *New*).

## Owner's decisions so far

| # | Decision | Owner's position |
|---|---|---|
| 1 | Generic Guns compatibility | **Undecided.** Revised options below. |
| 2 | Delete Cataclysm++'s `mon_laserturret` override | Agrees with the plan's recommendation |
| 3 | Bionic zombie CBM drops: restore `fbd4aad` and extend the `bionics_op2_*` and `bionics_sci` groups | Agrees with the plan's recommendation |
| 4 | Add the 93 legacy numeric `to_hit` items to `TEST_DATA/legacy_to_hit.json` | Agrees with the plan's recommendation |
| 5 | Prepper's `knife_rambo` goes in a `scabbard` | Agrees with the plan's recommendation |
| 6 | Restore the CVD machine, `atomic_lamp` and the old lab scenario extensions | Agrees with the plan's recommendation, **subject to finding 2** |
| 7 | Keep `legacy.json`; flag `b_field` `SHOULD_NOT_SPAWN` | Agrees with the plan's recommendation |
| 8 | CI coverage for Cataclysm++ | **Undecided.** Revised options below. |

## Findings: problems the plan misses

1. **Four objects use `extend` without `copy-from`, and 0.I mishandles both kinds.** A full scan of the mod finds exactly four such objects.
   - **Item groups `antique_ammo`, `museum_guns` and `on_hand_flintlock`.** `Item_factory::load_item_group` resets any group that has no `copy-from` ("Otherwise, unconditionally overwrite") before applying `extend`. Each core group would end up holding only `flintlock_ammo_mine`; museums would lose their guns, for example. **Fix:** add `"copy-from"` with the same id to all three.
   - *New (found by Antigravity):* **`flamethrower_surv`** in `Weapons/c_ranged.json` has its own `"flags"` plus `"extend": { "flags": [ "FIRE_TWOHAND", "STR_RELOAD", "NON_FOULING" ] }`. The generic reader in `generic_factory.h` takes the explicit member and only applies `extend` to objects with a `copy-from`, so the three flags are silently dropped. **Fix:** merge them into `"flags"`.
2. **Decision 6's scenario claim is false.** `lab_cargo_mutant` does not exist in 0.I; only upstream master has it. The trial load raised no error for the extension, so it would silently vanish. In 0.I the mutant lab start is `lab_chal`. **Fix:** extend `lab_chal`, `lab_staff` and `lab_cargo_staff_1`, and drop the `lab_cargo_mutant` extension. The CVD terrains and the `atomic_lamp` vehicle part do exist in 0.I.
3. **The density test fails on 23 items, not 20.** The plan's static audit missed `36navy_makeshift_magnum`, `44army_makeshift_magnum` and `flintlock_ammo_mine`; the test's stop after 20 failures hid them. Full list: [`density_failures.txt`](density_failures.txt), taken from a run with the cap lifted. *Corrected remedy (Antigravity's, verified):* list all three in `known_bad_density.json`. Their core parents `36navy`, `44army` and `flintlock_ammo` are already listed there. The two magnums inherit their parents' weight and volume unchanged, and `flintlock_ammo_mine` changes only its weight, so a volume fix would make them needlessly bulkier than the ammo they copy.
4. **The legacy `to_hit` count of 93 is correct.** Revision 1 first said 92 because of an extraction bug: `fr_762R` contains a capital letter. Use [`legacy_to_hit_ids.txt`](legacy_to_hit_ids.txt), taken from the test output. It excludes `bot_laserturret` and `laser_cannon`.
5. **The file inventory is wrong.**
   - The import list omits the top-level `c_achievements.json`. It loads cleanly and should be kept.
   - The tileset filenames are wrong. The real files are `Ultica_Expan_{Normal,Tall,Huge}.png` and `expan_dp_{normal,large}.png`, with five JSON files: `mod_tileset_DP_{Large,Normal}.json` and `mod_tileset_Ultica_{normal,tall,huge}.json`.
   - This is harmless if the whole folder is copied. Compatibility is fine: they target `UltimateCataclysm` and `MshockXottoplus`, both in `gfx/`.
6. *Corrected:* **"0 failures" is achievable, but only with CI's test ordering.** Revision 1 said it wasn't, because five tests (`monsters_spawn_*` ×4 and `limit_mod_size_bonus`) fail locally. Those runs used Catch2's default declaration order, where `limit_mod_size_bonus` runs immediately before the `monsters_spawn_*` tests and leaves state behind for them. `build-scripts/gha_test_only.sh` runs with `--rng-seed time --order lex` and splits the suite into `"[slow] ~starting_items"` and `"~[slow] ~[.],starting_items"`. Run that way, core's non-slow half (which contains all five tests) passes all 1131 test cases. **However, the plan's verification commands omit `--order lex`**, so as written they would hit the five failures. Add `--order lex`, or run the suites through `gha_test_only.sh`.
7. *Corrected:* **Dropping `lang/` is right, and it costs nothing.** Revision 1 said dropping it loses the mod's translations. In fact 0.I's `TranslationManager::Impl::ScanTranslationDocuments` reads mod `.mo` files only from the user mods directory (`PATH_INFO::user_moddir()`), never from `data/mods`. A `lang/` folder in the repo would never load. The translations are unavailable to an in-repo mod either way, unless they were merged into the core catalogue, which this fork doesn't maintain.
8. **There is no plan for future Cataclysm++ updates.** Upstream is active. Suggested layout:
   - commit the raw `46982a6` snapshot (minus the excluded paths) on its own;
   - put the 0.I reversions and fixes in separate commits;
   - record the base commit in the mod folder.

   Later upstream ranges can then be diffed and replayed. Push the series in one go: CI tests only the pushed tip, and the intermediate commits would not pass on their own.

## Verified correct

- **Component 1 (exclusions):** `Surv_help/c_override.json` and `Weapons/c_ranged_override.json` override exactly the restored `bot_laserturret`, `broken_laserturret` and `laser_cannon`. Cataclysm++'s laser cannon has armour penetration 4; ours has 15. Dropping `mod_interactions/` (`doom`, `PK_REBALANCE`) is right: `build-scripts/get_all_mods.py` adds each `mod_interactions/<id>` folder name as a mod id, so those two would break CI's all-mods load.
- **ID collisions:** of the mod's 110 ids shared with core, only four collide with content this fork restored, and they are exactly the plan's four laser entries. Monster groups, vehicle groups and talk topics merge in 0.I rather than replace. Full list: [`id_collisions.txt`](id_collisions.txt).
- **Component 2 (0.J to 0.I reversions):**
  - NPC `mission` strings map to the 0.I `npc_mission` values GUARD 7, SHOPKEEP 3 and GUARD_PATROL 8.
  - `aoe` and `trail` become single objects.
  - `light` fields go back to `LIGHT_n` flags.
  - `pasta_ingredients` becomes `pasta`.
  - `regional_overlay.json` is restored from `02fc4e8^`; `json_formatter` will reindent it from three spaces to two.

  Upstream `8ad7f0f`'s other change, `copy-from: armor_lc_leg_guard`, is valid in 0.I and needs no reversion. With these applied the mod loads, and the remaining errors are exactly the plan's lint and translation list plus the Prepper knife. Patch: [`component2_reversions.patch`](component2_reversions.patch), against the raw `46982a6` folder.
- **Component 3:** all seven target groups exist in `data/json/itemgroups/bionics.json` and are `distribution` groups. The `dissect_CBM_*` mapping is as described, and `fbd4aad` removed exactly the extensions the plan restores.
- **Decisions 2, 5 and 7:**
  - Cataclysm++ redefines `mon_laserturret` with aggression 50; ours has 100.
  - `knife_rambo` fits a `scabbard` (`SHEATH_SWORD`), not a `sheath` (`SHEATH_KNIFE`).
  - `b_field` is the only gap in overmap coverage.
- **Other claims:**
  - There are no Exodii, Rubik or portal-storm references.
  - The battery density test skips non-`dda` items.
  - `--check-mods` exists.
  - The fire-mode label fix matches core's `"5 rd."` convention.

## Decision 1: Generic Guns (revised)

*Corrected:* revision 1 claimed that about 15 Cataclysm++ guns could never be loaded in a Generic Guns world. That was wrong. When Generic Guns migrates an ammo type's default ammo, 0.I's `Item_factory::finalize_pre` rewrites every gun's `ammo`, every magazine's `type`, `default_ammo` and pocket `ammo_restriction`, and every gunmod's `acceptable_ammo` to the generic type. Generic Guns migrates the default ammo of every real calibre Cataclysm++ uses. So `surv_full_*`, `surv_lmg_*`, `surv_sniper`, the `22aux`/`9mmaux`/`45aux` gunmods and the `surv_*_mag`/`surv_belt_*` magazines all re-type themselves. They keep their calibre names but fire generic ammo.

Two more corrections:

- **Migrating Cataclysm++'s guns would gut its crafting.** Revision 1's option (c) migrated the guns themselves. When an item is migrated, `Item_factory` deletes every recipe whose result is that item, so the survivor gun crafting tree would go. Migrating guns is the wrong tool.
- **There is no duplicate-definition limit on 0.I.** Revision 1 cited one, but it was quoting `0.H-custom`'s backported doc. On `0.I-custom`, interaction files load with a source like `Cata++#generic_guns`, which passes the duplicate check. A mod may override its own ids in its own `mod_interactions` folder.

What actually breaks with both mods loaded, by trial load:

- Two professions start with `36navy_makeshift_magnum` and `44army_makeshift_magnum` (copied from core `36navy` and `44army`). Those don't fit Generic Guns' migrated `black_powder_revolver`, or its `flintlock_pouch`.
- `flintlock_ammo_mine` keeps the `flintlock` ammo type, so it won't fit `surv_sniper` once that is re-typed.
- *New (missed by both reviews):* `cowboy_hat_surv` has an ammo band keyed to 40 real calibres. Re-typing doesn't cover clothing pockets, so the band accepts nothing from Generic Guns.

Options:

| Option | Work | Result |
|---|---|---|
| (a) `"conflicts": [ "generic_guns" ]` | none | The mod manager refuses to enable both ("Unable to add %s. It is incompatible with a currently active mod."). CI's all-mods load splits them automatically. |
| (b) Minimal compatibility file: [`mod_interactions_generic_guns/gg_migration.json`](mod_interactions_generic_guns/gg_migration.json), installed as `data/mods/Cataclysm++/mod_interactions/generic_guns/gg_migration.json` | one small file | Both mods usable. Three `MIGRATION`s send the black-powder rounds to `black_powder_ball`, and one override re-keys the hat's band to Generic Guns' ammo types. **Verified by trial load: every Generic Guns-specific error is gone.** The survivor guns keep their real-calibre names while firing generic ammo. |
| (c) Full conversion, migrating or overriding about 45 guns, magazines, belts, gunmods and `fr_*` receivers | large | Not recommended: migration deletes the matching recipes, and auto re-typing already makes the guns usable. |

**Recommendation: (b).** It is verified, small and keeps both mods usable. The one cosmetic cost is the calibre names. A full test run with both mods loaded has not been done; CI's all-mods load would cover loading.

## Decision 8: CI (revised)

- **Cost:** standard GitHub-hosted runners are free and unlimited for public repositories; only larger runners are billed. Sources: [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) and [runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing).
- **What CI already does:** the kept Linux job sets `TEST_STAGE`, so `build-scripts/gha_test_only.sh` already runs `[force_load_game]` for every group from `get_all_mods.py`. Cataclysm++ would be load-tested with no workflow change. Run `45076698933` took 37 minutes to build and 41 minutes to test.
- *New (Antigravity found part of it; the rest verified here):* **the CI caches never work on `0.I-custom`.** This is a bug in the workflow retargeting, `3e31f6bd0d`, and is independent of Cataclysm++.
  - Both workflows treat every branch other than `0.I-branch` as a pull request.
  - `matrix.yml` runs `ccache -C` on every push.
  - Its restore key `ccache-0.I-<key>--` can never match the saved key `ccache-0.I-custom-<key>--…`.
  - `msvc-full-features.yml` also clears ccache and skips the vcpkg cache upload ("Don't upload vcpkg cache on failure or PRs").
  - Result: every build is cold, about 37 minutes on Linux and 51 on Windows.
  - **Fix:** change `0.I-branch` to `0.I-custom` in those conditions and fix the restore-key prefix.

| Option | What it catches | Cost |
|---|---|---|
| (a) Plan's recommendation: all-mods load plus `json.yml` | Load and consistency errors only | none |
| (b) A `--mods=Cata++` full-suite run | Also behavioural failures (density, to_hit, purification, coverage, starting items) | One more job. Once the cache bug is fixed, a second compile mostly hits ccache. Alternatively, build `cata_test` once, upload it as an artefact and fan out test-only jobs, with no repeated compile. |
| (c) The same for every mod this fork maintains (Cataclysm++, Aftershock, Xedra Evolved, Mind Over Matter, bionic professions; Magiclysm is already covered) | The whole mod baseline | Several parallel test jobs; best done as a build-once fan-out; any mod's failure turns the push red |

**Recommendation:** fix the cache bug first, whatever else is chosen. Then take (b), preferably as a build-once fan-out, which extends to (c) by adding entries.

## Resuming

1. Create a data-only worktree of `0.I-custom`:

   ```bash
   git worktree add --no-checkout --detach "$S/cpp_wt" origin/0.I-custom
   ```

   ```bash
   cd "$S/cpp_wt" && git sparse-checkout set --no-cone /data/ /tools/ /build-scripts/ /Makefile && git checkout
   ```
2. Copy `nocts_cata_mod_DDA` at `46982a6` to `data/mods/Cataclysm++/`, without `mod_interactions/`, `lang/` and `README_DDA.md`. Component 1 also drops `Surv_help/c_override.json` and `Weapons/c_ranged_override.json` and removes the `mon_laserturret` object. The trial copy behind this audit still contained those three; it doesn't affect the lists above.
3. From the worktree root, apply the Component 2 patch:

   ```bash
   patch -p1 < component2_reversions.patch
   ```
4. Trial-load with [`cload.sh`](cload.sh). It uses a `cata_test` built from `0.I-custom`; set `S` to the scratch directory and edit the binary path inside if needed.

Then apply findings 1–3 and Decisions 1–8 as decided.

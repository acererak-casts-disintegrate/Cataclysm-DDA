# Cataclysm++ In-Repo Integration Plan (`0.I-custom`)

## Goal Description

Integrate **Cataclysm++** ([`Noctifer-de-Mortem/nocts_cata_mod`](https://github.com/Noctifer-de-Mortem/nocts_cata_mod), subfolder `nocts_cata_mod_DDA`, upstream commit `46982a6`, licensed under [The Unlicense](https://unlicense.org/)) as a first-class in-repo mod at `data/mods/Cataclysm++/` on branch `0.I-custom`.

Core requirements:
- **Keep all `mod_tileset` assets** (all 5 PNG sprite sheets and both Ultica and DP/MshockXotto+ JSON mappings).
- **Drop Cataclysm++'s laser overrides** so `0.I-custom`'s restored classic sci-fi items and monsters (`laser_cannon`, `bot_laserturret`, `broken_laserturret`, `mon_laserturret`) remain authoritative.
- **Restore bionic zombie CBM drops** removed by upstream commit `fbd4aad`, aligning Cataclysm++'s CBMs with `0.I-custom`'s restored classic CBM ecosystem (`9131c37`).
- **Pass the full `cata_test` suite** with `--mods=Cata++`, plus CI's `all_mods` (`[force_load_game]`) matrix, core `cata_test` without `Cata++`, and `make style-all-json-parallel`.

---

## User Review Required

> [!IMPORTANT]
> Please review the design decisions below before execution. Each item lists a **Recommended** default that will be used if you approve as-is.

| # | Decision | Recommended Option | Alternative |
|---|---|---|---|
| **1** | **`Generic_Guns` compatibility** (`all_mods` CI fails when `Cata++` and `generic_guns` load together due to black-powder revolvers, and Cata++ adds 19 real-caliber firearms) | Add `"conflicts": [ "generic_guns" ]` to `modinfo.json` (matches `Isolation-Protocol` and `aftershock_exoplanet`; `get_all_mods.py` splits them cleanly in CI). | Add a small `mod_interactions/generic_guns/` override patching the 2 black-powder professions (leaves 19 real-caliber guns alongside Generic Guns). |
| **2** | **`mon_laserturret` in `Monsters/c_monster_override.json`** (`0.I-custom` restores [`mon_laserturret`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/monsters/classic_robots.json#L85-L118) with `aggression: 100`) | **Delete the `mon_laserturret` entry completely** so `0.I-custom`'s restored turret is untouched. | Replace the full definition with the same 5-line `copy-from` block (`aggression: 50`, `anger_triggers`) used on the other 7 military turrets in that file. |
| **3** | **Bionic zombie CBM drop scope** (see Component 3) | Restore all 3 groups deleted in upstream `fbd4aad` (`bionics_op`, `bionics_tech`, `bionics_subs`) **and** extend `bionics_op2_off` / `bionics_op2_def` / `bionics_op2_utl` (Elite Zombie Bio-Operators) and `bionics_sci` (Zombie Scientists) so every relevant `0.I-custom` dissection table drops Cata++ CBMs. | Strict `fbd4aad` restoration only (`bionics_op`, `bionics_tech`, `bionics_subs`). |
| **4** | **93 legacy numeric `to_hit` items** (`item_new_to_hit_enforcement`) | Add a `"//": "Cataclysm++"` section to [`data/mods/TEST_DATA/legacy_to_hit.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/mods/TEST_DATA/legacy_to_hit.json) (matches how `0.I-custom` handled Aftershock, Mind Over Matter, and Xedra Evolved in `cb63a4e` / `9dffb31`; zero melee balance drift). | Convert all 91 active items to modern `{ "grip", "length", "surface", "balance" }` objects (only keeping or pruning the 2 `legacy.json` items). |
| **5** | **`prepper` profession `knife_rambo` in `sheath`** (`Char_creation/c_classes_r.json:51` fails consistency check because `knife_rambo` is `SHEATH_SWORD`, not `SHEATH_KNIFE`) | Change `"container-item": "sheath"` → `"scabbard"` (keeps the Prepper's signature Rambo knife). | Change `"item": "knife_rambo"` → `"knife_combat"` (keeps `"sheath"`). |
| **6** | **Optional `0.I` content restorations** (3 upstream `0.J` removals whose targets still exist in `0.I-custom`) | Restore all 3: (a) CVD machine (`t_cvdbody`/`t_cvdmachine`) in `Terrain/Unknown_Lab.json` (`8e44613`), (b) `atomic_lamp` in `Vehicles/c_vehicles.json` (`74aed24`), and (c) classic `lab_chal`/`lab_staff` scenario extensions alongside `lab_cargo_*` in `Char_creation/c_scenarios.json` (`629e450`). | Keep `0.J` versions (only restore required `Terrain/regional_overlay.json`). |
| **7** | **`legacy.json` handling** | Keep `legacy.json`, add `"SHOULD_NOT_SPAWN"` to `b_field` (passes `overmap_terrain_coverage`), and fix its 3 lints so all `looks_like` / tileset / save-migration references remain safe. | Prune unused obsolete entries and `b_field`, retaining only the 4 `looks_like` monster stubs. |
| **8** | **GitHub Actions CI (`.github/workflows/matrix.yml`)** | Rely on automatic `all_mods` (`get_all_mods.py` `[force_load_game]`) + `json.yml` in CI, and run the full `cata_test --mods=Cata++` suite locally during verification. | Also add a dedicated `--mods=Cata++` job to [`.github/workflows/matrix.yml`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/.github/workflows/matrix.yml) (increases CI minutes per push). |

> [!NOTE]
> Cataclysm++ has **zero** Exodii / Rubik / natural portal storm references, and its `*_atomic_battery_cell_rechargeable` items are unaffected by [`tests/battery_density_test.cpp`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/tests/battery_density_test.cpp#L113-L120) (which only enforces strict energy density on `"dda"` items).

---

## Proposed Changes

### Component 1: Mod Import, Directory Layout, `modinfo.json`, & Pruning

Import `nocts_cata_mod_DDA/` from upstream `46982a6` into `data/mods/Cataclysm++/` (matching the CamelCase folder convention of existing in-repo mods like `Magiclysm`, `Aftershock`, `DinoMod`, and `MindOverMatter`) while preserving `"id": "Cata++"` for save and cross-mod compatibility.

#### [NEW] `data/mods/Cataclysm++/`
- Copy all core content JSON directories (`Char_creation/`, `Monsters/`, `Mutations/`, `Npc/`, `Recipe/`, `Surv_help/`, `Terrain/`, `Vehicles/`, `Weapons/`, `legacy.json`, `Npc/Npc_talk_help.txt`).
- **Keep `mod_tileset/` completely intact** (all 5 PNGs: `Cata++_Ultica_normal.png`, `Cata++_Ultica_large.png`, `Cata++_Ultica_tall.png`, `Cata++_DP_Normal.png`, `Cata++_DP_Large.png`, plus `mod_tileset_Ultica.json`, `mod_tileset_DP_Normal.json`, `mod_tileset_DP_Large.json`).

#### [DELETE] Excluded on Import (not copied into `data/mods/Cataclysm++/`)
- `mod_interactions/` (`doom/` and `PK_REBALANCE/`): external third-party mods not present in-repo; keeping them breaks [`build-scripts/get_all_mods.py`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/build-scripts/get_all_mods.py) in CI.
- `lang/`: standalone compiled `.mo` and `.po`/`.pot` files; in-repo mods use the repository's central translation pipeline instead.
- `Surv_help/c_override.json`: overrides `bot_laserturret` and `broken_laserturret`, which are already restored in [`data/json/items/classic_scifi.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/items/classic_scifi.json).
- `Weapons/c_ranged_override.json`: overrides `laser_cannon` (with lower AP 4 vs. `0.I-custom`'s AP 15), already restored in [`data/json/items/classic_scifi.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/items/classic_scifi.json) and already listed in [`data/mods/TEST_DATA/legacy_to_hit.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/mods/TEST_DATA/legacy_to_hit.json).
- `README_DDA.md`: external installation guide superseded by repo [`README.md`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/README.md).

#### [MODIFY] `data/mods/Cataclysm++/modinfo.json`
- Strip `<color_light_green>...</color>` tags from `"name"` to match all 41 existing in-repo mods.
- Fix two single-space sentence breaks in `"description"` (passes text-style check).
- Add `"conflicts": [ "generic_guns" ]` (per Decision #1).

```json
[
  {
    "type": "MOD_INFO",
    "id": "Cata++",
    "name": "Cataclysm++",
    "authors": [ "Noctifer" ],
    "description": "The unofficial expansion mod for Cataclysm: Dark Days Ahead.\n\nThe gigantic jabberwock of a mod that adds a lot of content to the game: new items, buildings, scenarios, monsters, etc.  It also reworks and adds alternatives to many things from recipes to scenarios.  It also adds a pseudo-story and lore on the works.\n\nThe Bio-Weapon, Super Soldier, Commandeers, Slave Fighters and the Old World Prepper NPC factions join the world.\n\nSeek the Bio-weapons, find loot, take down new monsters and invest in skills for new craftable items.",
    "category": "content",
    "dependencies": [ "dda" ],
    "conflicts": [ "generic_guns" ]
  }
]
```

#### [MODIFY] `data/mods/Cataclysm++/Monsters/c_monster_override.json`
- Remove the full `mon_laserturret` object (lines 30–66) so `0.I-custom`'s restored [`mon_laserturret`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/monsters/classic_robots.json#L85-L118) is used directly (per Decision #2). Leave the 7 other military turret `copy-from` tweaks and 6 Mi-Go harvest overrides intact.

---

### Component 2: `0.J → 0.I` Compatibility Reversions & `0.I` Restorations

Cataclysm++ upstream tracks `0.J` experimental. All **18** required mechanical reversions plus the deleted `regional_overlay.json` were verified empirically against the `0.I-custom` binary:

| File | Occurrences | Change (`0.J → 0.I`) |
|---|---|---|
| `Npc/c_npc.json` | 11 | Revert `"mission"` string to `0.I` [`npc_mission`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/src/npc.h) enum integer: `"GUARD"` → `7` (8 NPCs), `"SHOPKEEP"` → `3` (`survn`), `"GUARD_PATROL"` → `8` (`slave_fight`, `slave_fight_ally`). |
| `Weapons/c_ammo_effect.json` | 2 | On `C_DAZZLER_BURST`, unwrap single-element arrays `"aoe": [ { ... } ]` → `"aoe": { ... }` and `"trail": [ { ... } ]` → `"trail": { ... }` (matches [`src/ammo_effect.cpp`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/src/ammo_effect.cpp)). |
| `Surv_help/c_armor.json` | 1 | Line 445 (`c_mi_go_carapace_salvaged`, upstream `8ad7f0f`): remove `"light": 50`, restore `"LIGHT_25"` in `"flags"`. |
| `Surv_help/c_tools.json` | 3 | Lines 46, 117, 209 (`survivor_headlight_on`, `surv_station_t`, `solar_torch_lit`, upstream `8ad7f0f`): remove `"light": 450` / `450` / `310`, restore `"LIGHT_450"` / `"LIGHT_450"` / `"LIGHT_310"` in `"flags"`. |
| `Terrain/sketchy_cabin.json` | 1 | Line 90: replace `"pasta_ingredients"` item group with `0.I` `"pasta"`. |

#### [NEW] `data/mods/Cataclysm++/Terrain/regional_overlay.json`
Restore the 20-line region overlay deleted in upstream `02fc4e8`, which is still referenced by `Terrain/overmap_terrain.json:32` (`"extras": "surv_encamp"`):

```json
[
  {
    "type": "region_overlay",
    "regions": [ "all" ],
    "map_extras": {
      "surv_encamp": {
        "chance": 10,
        "extras": {
          "mx_crater": 25,
          "mx_portal": 15,
          "mx_portal_in": 10,
          "mx_spider": 25,
          "mx_jabberwock": 10,
          "mx_supplydrop": 3,
          "mx_helicopter": 2
        }
      }
    }
  }
]
```

#### Optional `0.I` Content Restorations (per Decision #6)
- **[MODIFY] `data/mods/Cataclysm++/Terrain/Unknown_Lab.json`**: Restore `D` (`t_cvdbody`) and `E` (`t_cvdmachine`) removed in `8e44613` (both exist in `0.I` [`terrain-manufactured.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/furniture_and_terrain/terrain-manufactured.json#L567-L592)).
- **[MODIFY] `data/mods/Cataclysm++/Vehicles/c_vehicles.json`**: Restore `"atomic_lamp"` in place of `"aisle_lights"` at line 87 (removed in `74aed24`; `atomic_lamp` exists in `0.I` [`vehicleparts/lights.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/vehicleparts/lights.json#L25); keep `74aed24`'s `turret_m134` fix since `turret_surv_lmg_762R` no longer exists).
- **[MODIFY] `data/mods/Cataclysm++/Char_creation/c_scenarios.json`**: Keep `lab_cargo_mutant` / `lab_cargo_staff_1` extensions **and** also re-add the `lab_chal` and `lab_staff` extensions removed in `629e450` (all four scenarios exist in `0.I`).

---

### Component 3: Classic Bionic Zombie CBM Drops Restoration

Cataclysm++ already extends `bionics` and `bionics_mil` in `Surv_help/c_item_groups_vanilla.json` with its 8 general-pool CBMs (`bio_laser_armgun`, `bio_sword`, `bio_flamethrower`, `bio_plasma_cell`, `bio_atomic_battery`, `bio_hazard_shield`, `bio_animal_empathy`, `bio_cutting_torch`). Its 9th CBM (`bio_power_storage_sentinel`) drops exclusively from Cata++'s own augmented super-soldiers via `Monsters/c_monster_harvest_dissect.json`.

In `0.I-custom`, [`data/json/harvest_dissect.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/harvest_dissect.json#L782-L900) maps bionic zombies to [`data/json/itemgroups/bionics.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/itemgroups/bionics.json#L208-L395) as follows:
- `dissect_CBM_OP` (Zombie Bio-Operator) → `bionics_op`
- `dissect_CBM_OP2` (Elite Zombie Bio-Operator) → `bionics_op2_off`, `bionics_op2_def`, `bionics_op2_utl`
- `dissect_CBM_TECH` (Zombie Technician) → `bionics_tech`
- `dissect_CBM_SUBS` (Shockers / Shocker Brute) → `bionics_subs`
- `dissect_CBM_SCI` (Zombie Scientist) → `bionics_sci`
- `dissect_CBM_CIV` (Civilian bionic zombies) → `bionics_common`

#### [MODIFY] `data/mods/Cataclysm++/Surv_help/c_item_groups_vanilla.json`
Restore the 3 exact extensions deleted in upstream commit `fbd4aad` (`bionics_op`, `bionics_tech`, `bionics_subs`), and (per Decision #3) extend `bionics_op2_off`, `bionics_op2_def`, `bionics_op2_utl`, and `bionics_sci` with thematically matched Cata++ CBMs (keeping civilian `bionics_common` clean of military weapons):

```json
  {
    "type": "item_group",
    "id": "bionics_op",
    "copy-from": "bionics_op",
    "subtype": "distribution",
    "//": "What the commandos get.",
    "extend": {
      "items": [
        [ "bio_laser_armgun", 5 ],
        [ "bio_sword", 5 ],
        [ "bio_flamethrower", 5 ],
        [ "bio_plasma_cell", 20 ],
        [ "bio_atomic_battery", 5 ],
        [ "bio_hazard_shield", 5 ],
        [ "bio_animal_empathy", 10 ],
        [ "bio_cutting_torch", 5 ]
      ]
    }
  },
  {
    "type": "item_group",
    "id": "bionics_op2_off",
    "copy-from": "bionics_op2_off",
    "subtype": "distribution",
    "//": "Elite zombie bio-operator offense CBMs.",
    "extend": { "items": [ [ "bio_laser_armgun", 5 ], [ "bio_sword", 5 ], [ "bio_flamethrower", 5 ] ] }
  },
  {
    "type": "item_group",
    "id": "bionics_op2_def",
    "copy-from": "bionics_op2_def",
    "subtype": "distribution",
    "//": "Elite zombie bio-operator defense CBMs.",
    "extend": { "items": [ [ "bio_hazard_shield", 5 ] ] }
  },
  {
    "type": "item_group",
    "id": "bionics_op2_utl",
    "copy-from": "bionics_op2_utl",
    "subtype": "distribution",
    "//": "Elite zombie bio-operator utility CBMs.",
    "extend": {
      "items": [ [ "bio_plasma_cell", 10 ], [ "bio_atomic_battery", 5 ], [ "bio_animal_empathy", 5 ], [ "bio_cutting_torch", 5 ] ]
    }
  },
  {
    "type": "item_group",
    "id": "bionics_tech",
    "copy-from": "bionics_tech",
    "subtype": "distribution",
    "//": "Bionics used by technicians.",
    "extend": { "items": [ [ "bio_atomic_battery", 10 ], [ "bio_cutting_torch", 20 ] ] }
  },
  {
    "type": "item_group",
    "id": "bionics_subs",
    "copy-from": "bionics_subs",
    "subtype": "distribution",
    "//": "Bionics dropped by substation mini-boss.",
    "extend": {
      "items": [ [ "bio_atomic_battery", 5 ], [ "bio_plasma_cell", 5 ], [ "bio_hazard_shield", 5 ], [ "bio_cutting_torch", 10 ] ]
    }
  },
  {
    "type": "item_group",
    "id": "bionics_sci",
    "copy-from": "bionics_sci",
    "subtype": "distribution",
    "//": "High-tech bionics for zombie scientists.",
    "extend": { "items": [ [ "bio_atomic_battery", 5 ], [ "bio_hazard_shield", 5 ], [ "bio_animal_empathy", 5 ] ] }
  },
```

---

### Component 4: Consistency Bug Fix, Lints, Text Style, & JSON Formatting

#### [MODIFY] `data/mods/Cataclysm++/Char_creation/c_classes_r.json`
- Line 51 (`prepper` profession): change `{ "item": "knife_rambo", "container-item": "sheath" }` → `{ "item": "knife_rambo", "container-item": "scabbard" }` (per Decision #5; resolves `check_consistency` error).

#### [MODIFY] `data/mods/Cataclysm++/Weapons/c_magazines.json`
- Fix copy-paste name typo on `medium_atomic_battery_cell_rechargeable`: `"light rechargeable plutonium cell"` → `"medium rechargeable plutonium cell"`.

#### Translation Pluralization Lints (8 fixes)
All 8 flagged by `json_formatter` / `translation` checks:
- `legacy.json:124` (`stealth_cloak_on`): `{ "str": "obsolete stealth cloak (on)", "str_pl": "obsolete stealth cloaks (on)" }`
- `legacy.json:535` (`manual_pistol_surv`): `{ "str_sp": "Rebuilding Civilization: Pistols" }`
- `Monsters/c_monsters.json:100` (`mon_apophis`): `{ "str_sp": "Bio-Weapon Apophis" }`
- `Surv_help/c_armor.json:205` (`armguard_steel_surv`): `{ "str_sp": "survivor steel arm guards" }`
- `Surv_help/c_armor.json:222` (`legguard_steel_surv`): `{ "str_sp": "survivor steel leg guards" }`
- `Surv_help/c_books.json:399` (`manual_pistol_surv`): `{ "str_sp": "Rebuilding Civilization: Pistols" }`
- `Surv_help/c_tools.json:1137` (`c_mi_go_beam_broken`): `{ "str": "biological lens", "str_pl": "biological lenses" }`
- `Surv_help/c_tools.json:1257` (`surv_crank_rifle_charge`): `{ "str": "survivor's crank rifle (charge mode)", "str_pl": "survivor's crank rifles (charge mode)" }`

#### Text-Style Lints (17 remaining fixes outside `modinfo.json`)
Fix single-space after sentence punctuation / ellipsis / formatting errors reported by `json_formatter`:
- `Weapons/c_ranged.json:76,256,1444,1493`: change `"2-rd. burst"` → `"2 rd."` (matches core `0.I` fire-mode labels in [`data/json/items/gun/5x50.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/items/gun/5x50.json#L66) and resolves the period-spacing violation).
- Fix remaining double-space / punctuation lints in `legacy.json:1274`, `Char_creation/c_scenarios.json:19`, `Mutations/c_bio_mutation.json:381`, `Npc/TALK_BHUNTER.json:118`, `Npc/TALK_BIO_2.json:89,90`, `Npc/TALK_MSCI.json:222`, `Npc/c_bgss.json:84,106,117`, and `Npc/c_factions.json:42,77,179`.

#### Line Endings & Formatting
- Convert any CRLF files (`Surv_help/c_bionics.json`, `Weapons/c_magazines.json`, etc.) to LF.
- Run `make style-all-json-parallel` across `data/mods/Cataclysm++/` so all JSON files match CDDA formatting rules.

---

### Component 5: Full `cata_test` Compliance

#### 5a. Material Density Sanity Check ([`tests/item_test.cpp`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/tests/item_test.cpp#L850-L865))
Static inheritance-resolved audit identified **20** items exceeding their material density cap. All 20 have physically sensible weight/volume fixes grounded in core `0.I` item dimensions — **zero** additions to [`known_bad_density.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/mods/TEST_DATA/known_bad_density.json) are required:

| File | Item ID(s) | Current (Density / Max) | Proposed Fix (New Density) | Rationale |
|---|---|---|---|---|
| `Surv_help/c_armor.json` | `badge_bio_weapon`, `badge_bio_weapon_apophis`, `badge_bio_weapon_evy` (3) | `60 g / 5 ml` (12.00 / 10.49 `silver`) | `volume: "8 ml"` (7.50) | Matches core [`badge_abstract`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/items/armor/jewelry.json#L1805-L1811) (`60 g / 8 ml`). |
| `Surv_help/c_books.json` | `evil_invitation`, `omnitech_weapon_ups_manual` (2) | `1700 g / 500 ml` (3.40 / 1.20 `paper`) | `weight: "450 g"` (0.90) | Realistic 500 ml classified packet / technical manual. |
| `Surv_help/c_books.json` | `note_apophis`, `note_sketchy_cabin` (2) | `3 g / 1 ml` (3.00 / 1.20 `paper`) | `volume: "3 ml"` (1.00) | Matches folded sheet of paper (`3 g`). |
| `Surv_help/c_tools.json` | `recipe_surv` (1) | `1700 g / 500 ml` (3.40 / 1.20 `paper`) | `weight: "550 g"` (1.10) | Realistic 500 ml binder/cookbook. |
| `Surv_help/c_comestibles.json` | `gas_slime_scrap` (1) | `276 g / 250 ml` (1.10 / 0.70 `hydrocarbons`) | `weight: "170 g"` (0.68) | Matches gasoline-density slime glob (`250 ml`). |
| `Surv_help/c_tools.json` | `solar_torch`, `solar_torch_lit` (2) | `956 g` & `942 g / 1 L` (0.96 & 0.94 / 0.85 `wood`) | `volume: "1250 ml"` (0.76 & 0.75) | Comparable to core [`torch`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/items/tool/lighting.json#L1017-L1024) (`1089 ml`) + `gas_slime_scrap`. |
| `Surv_help/c_tools.json` | `c_mi_go_beam_broken` (1) | `3 kg / 2 L` (1.50 / 1.30 `alien_resin`+`flesh`) | `volume: "2500 ml"` (1.20) | Fits composite density without changing mass. |
| `Surv_help/c_tools.json` | `c_mi_go_extruder_broken` (1) | `750 g / 500 ml` (1.50 / 1.30 `alien_resin`+`flesh`) | `volume: "600 ml"` (1.25) | Fits composite density without changing mass. |
| `Surv_help/c_tools.json` | `c_mi_go_rifle_broken` (1) | `7 kg / 5 L` (1.40 / 1.30 `alien_resin`+`flesh`) | `volume: "5500 ml"` (1.27) | Fits composite density without changing mass. |
| `Weapons/c_magazines.json` | `light_atomic_battery_cell_rechargeable` (1) | `160 g / 35 ml` (4.57 / 4.15 `iron`+`plastic`) | `volume: "40 ml"` (4.00) | Matches `0.I-custom` [`light_atomic_battery_cell`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/json/items/battery.json#L182-L190) (`160 g / 40 ml`). |
| `Weapons/c_ranged.json` | `flesh_pistol`, `flesh_smg`, `flesh_rifle`, `flesh_lmg`, `flesh_shotgun` (5) | `850 g/500 ml` to `4750 g/2 L` (1.70–2.85 / 1.45 `flesh`+`superalloy`) | Volumes → `600 ml`, `2 L`, `2750 ml`, `3500 ml`, `2750 ml` (1.33–1.43) | Preserves `[ "flesh", "superalloy" ]` durability and matches core pistol/SMG/rifle/LMG/shotgun volumes. |

#### 5b. Legacy `to_hit` Enforcement ([`tests/item_test.cpp`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/tests/item_test.cpp#L780-L810))
#### [MODIFY] [`data/mods/TEST_DATA/legacy_to_hit.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/mods/TEST_DATA/legacy_to_hit.json)
- Per Decision #4, append a sorted `"//": "Cataclysm++"` `test_data` entry containing the **93** numeric-`to_hit` items across `Surv_help/c_armor.json` (14), `Surv_help/c_bionics.json` (1), `Surv_help/c_tools.json` (33), `Vehicles/c_vehicle_parts.json` (1), `Weapons/c_melee.json` (6), `Weapons/c_mods.json` (6), `Weapons/c_ranged.json` (30), and `legacy.json` (2: `shmap`, `surcan`).
- Because [`item_new_to_hit_enforcement`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/tests/item_test.cpp#L780-L810) skips IDs that are not currently loaded (`!id.is_valid()`), non-Cataclysm++ test runs will pass pruning cleanly.

#### 5c. Overmap Terrain Coverage ([`tests/overmap_test.cpp`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/tests/overmap_test.cpp#L392-L560))
#### [MODIFY] `data/mods/Cataclysm++/legacy.json`
- Add `"SHOULD_NOT_SPAWN"` to `b_field`'s `flags` (unreferenced obsolete `overmap_terrain` that otherwise fails `overmap_terrain_coverage`).

#### 5d. Runtime Test Discovery & Remediation
Static audits found **0** violations in `item_length_sanity_check`, `All_valid_mutations_can_be_purified`, `monfactions_reciprocate`, `rigid_armor_compliance`, and `items_spawn_in_their_default_containers`. During execution, running the compiled `tests/cata_test --mods=Cata++` binary will exercise every remaining runtime invariant (including `starting_items` encumbrance/pockets for all Cata++ professions & scenarios, `overmap_terrain_coverage` special placement, mapgen, recipes, vehicles, and NPC dialogue). Any additional runtime failures uncovered by `cata_test` will be fixed directly in `data/mods/Cataclysm++/` until 100% of test cases pass.

---

### Component 6: Documentation & Attribution

#### [MODIFY] [`README.md`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/README.md)
- Add a concise bullet under **Other in-repo mods** noting the inclusion of **Cataclysm++** (originally by Noctifer & contributors under The Unlicense), adapted for `0.I-custom` with its laser overrides dropped, bionic zombie CBM drops restored, and full test-suite data fixes applied.

---

## Verification Plan

### Automated Verification
All automated checks will be executed locally in `/home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA` after implementing the changes:

1. **JSON Formatting & Text Style (CI `json.yml` parity):**
   ```bash
   make style-all-json-parallel RELEASE=1
   ```
   Confirm `git diff` after formatting is empty and 0 lint/translation/text-style errors remain.

2. **Mod Load & 55 Consistency Checks (fast check via prebuilt `0.I-custom` binary):**
   Run `--check-mods Cata++` against the prebuilt `cataclysm-tiles` binary and verify exit code `0` with zero debug errors.

3. **Build Headless `tests/cata_test`:**
   Install missing build deps if needed (`libncursesw5-dev`, `gettext`, `parallel`, matching [`.github/workflows/matrix.yml`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/.github/workflows/matrix.yml)) and compile `tests/cata_test` (`TILES=0 SOUND=0 RELEASE=1`).

4. **Full `cata_test` Suite with `--mods=Cata++`:**
   Run the exact complete test suites from [`tests/CMakeLists.txt`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/tests/CMakeLists.txt#L36) and [`build-scripts/gha_test_only.sh`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/build-scripts/gha_test_only.sh):
   ```bash
   ./tests/cata_test --rng-seed time --mods=Cata++ "~[slow] ~[.],starting_items"
   ./tests/cata_test --rng-seed time --mods=Cata++ "[slow] ~starting_items"
   ```
   Confirm 0 failures across all test cases (including `[item]`, `[mutations]`, `[monster]`, `[overmap][slow]`, `[vehicle]`, `[npc]`, `[eoc]`, and `starting_items`).

5. **CI `all_mods` Compatibility Matrix (`TEST_STAGE=1` parity):**
   Run [`build-scripts/get_all_mods.py`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/build-scripts/get_all_mods.py) and execute `./tests/cata_test '[force_load_game]' --mods=<group>` for every returned mod group, confirming `Cata++` loads cleanly with every non-conflicting in-repo mod (Aftershock, Magiclysm, Mind Over Matter, Xedra Evolved, DinoMod, etc.) and splits cleanly from `generic_guns`.

6. **Core Regression Check (without `Cata++`):**
   Run `./tests/cata_test "[item]"` (and full default `cata_test`) without `--mods=Cata++` to verify [`legacy_to_hit.json`](file:///home/antigravity/acererak-casts-disintegrate/Cataclysm-DDA/data/mods/TEST_DATA/legacy_to_hit.json) and core tests have zero regressions.

### Manual Verification (Recommended Post-Build Smoke Check)
- Launch `cataclysm-tiles`, create a new world, and confirm **Cataclysm++** appears cleanly under Content mods without raw `<color_...>` markup.
- Inspect Cata++ items/monsters with both **Ultica** and **MshockXotto+** tilesets to verify `mod_tileset/` PNGs render properly.
- Start characters with the **Prepper** (`knife_rambo` in `scabbard`) and **Bio-Weapon** scenarios.
- Debug-spawn and dissect bionic zombies (`mon_zombie_bio_op`, `mon_zombie_bio_op2`, `mon_zombie_technician`, `mon_zombie_electric`, `mon_zombie_scientist`) to verify Cata++ CBMs appear in dissection drops.
- Debug-spawn `laser_cannon` and `mon_laserturret` to verify `0.I-custom`'s restored stats (AP 15, `aggression: 100`) are preserved.

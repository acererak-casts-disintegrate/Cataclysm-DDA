> [!IMPORTANT]
> **This is an unofficial fork.** This repository is an independent fork of
> [Cataclysm: Dark Days Ahead](https://github.com/CleverRaven/Cataclysm-DDA), based on the
> 0.H "Herbert" stable release. It is not affiliated with, endorsed by or supported by
> CleverRaven or the Cataclysm: Dark Days Ahead development team.
>
> This fork changes content and gameplay in ways the official project has not adopted and may
> never adopt. It currently offers no support channels beyond this repository, so please do not
> direct bug reports or feedback about it to the official issue tracker, forums or Discord.
> Problems introduced by these changes are this fork's responsibility alone.
>
> For the official game, releases and support, visit [cataclysmdda.org](https://cataclysmdda.org)
> or the [official repository](https://github.com/CleverRaven/Cataclysm-DDA). Cataclysm: Dark
> Days Ahead is licensed under [CC BY-SA 3.0](LICENSE.txt), and this fork is distributed under
> the same licence.

# Cataclysm: Dark Days Ahead

Cataclysm: Dark Days Ahead is a turn-based survival game set in a post-apocalyptic world. While some have described it as a "zombie game", there is far more to Cataclysm than that. Struggle to survive in a harsh, persistent, procedurally generated world. Scavenge the remnants of a dead civilization for food, equipment, or, if you are lucky, a vehicle with a full tank of gas to get you the hell out of Dodge. Fight to defeat or escape from a wide variety of powerful monstrosities, from zombies to giant insects to killer robots and things far stranger and deadlier, and against the others like yourself, who want what you have...

<p align="center">
    <img src="./data/screenshots/ultica-showcase-sep-2021.png" alt="Tileset: Ultica">
</p>

## Changes from 0.H

This fork is based on the 0.H stable branch. As of now, it differs from 0.H as follows.

**Core game**

* **Classic CBM acquisition.** Bionics turn up in loot again and can be harvested from bionic zombies, as in 0.F, instead of coming from the Exodii.
* **Exodii as a baseless scavenger faction.** Their castle, safehouse, warehouse, NPCs, trade and missions are gone. They appear only at rare crashed-pod sites in the wild.
* **No natural portal storms.** The storm-driven scenarios and the Hub 01 contract that needed a storm are removed. Storms can still be started from the debug weather menu.
* **Skill rust off by default.** The world option removed after 0.G (full, capped or off) is back, defaulting to off.
* **Rivtech content restored.** Reverts upstream's removal of the RM216 SPIW, RM232 IDW, 5x50mm flechette ammunition, RM298 HMG and 8mm ammunition variants, and its Rivtech gun nerfs.
* **Pneumatic weapons restored.** The pneumatic assault rifle, bolt driver and shotgun, with shotcanister ammunition.
* **Classic sci-fi content restored.** Robots (chicken walker, tank drone, copbot, riotbot, eyebot, laser turret, mininuke hack), the railgun, shock absorber and fusion blaster CBMs, the laser cannon, heavy rail rifle, mininuke launcher, RM99 revolver, advanced UPS, solar gear, matching vehicle turrets and the atomic sports car.
* **Unlimited atomic coffeemaker.** It heats from its own power source again, as in 0.G.
* **Military Professions mainlined.** Military Rifleman, Operator Recon and Operator CBRN are now core professions, and the obsolete mod is removed.
* **Selected upstream bug fixes** from later 0.H-branch releases: battery chargers work outside the reality bubble, Godco construction updates place correctly, and a start-up crash and a GCC 15 build failure are fixed.
* **Conditional mod-interaction loading.** Backported from later upstream: a mod's `mod_interactions/<mod_id>/` files load only when that mod is active, so Defense Mode content from other mods no longer appears in normal games. See [MOD_COMPATIBILITY.md](doc/MOD_COMPATIBILITY.md).

**Aftershock**

* **Earth setting.** The Salus IV colony, exoplanet locations, Whately family and UPLIFT content are removed. Remaining items and lore are reassigned to organisations already in the game, such as Northrop, Rivtech, Shady Hills Corporation, Hub 01, FEMA and XEDRA.
* **Fewer overrides of core content.** Aftershock no longer replaces core items, vehicles or mechanics, except the pressure tank, which its Rocket Jumper profession needs. It also drops its duplicates of restored core items.
* **New and re-homed spawns.** Its arcology now spawns as a Shady Hills corporate arcology, and items stranded by the removals spawn in Earth locations.
* **Data fixes.** Item weights, volumes and lengths, faction relations and mutation purification are corrected.

**Other in-repo mods**

* **Xedra Evolved.** Its Exodii Jotunn content is kept, in line with the scavenger Exodii, and its roadside Jotunn encounter now spawns.
* **Mind Over Matter and Xedra Evolved** lose their Exodii (Rubik) dialogue. Mind Over Matter's awakening during portal storms can no longer trigger; matrix crystals still awaken psionic powers.
* **Data fixes for Xedra Evolved, Mind Over Matter and Blaze Industries.** Faction relations are made mutual, paraclesian lineage traits can no longer be purified (as in later upstream), Mind Over Matter's concentration traits can be, and impossible item weights and volumes are corrected, mostly using upstream's later values. Xedra's Ierde, Sylph and Homullus lineages are flagged as unfinished, since this snapshot gives them too few traits to cross their thresholds.
* **Portal Storms Ignore NPCs** (`personal_portal_storms`) is marked obsolete: it only changes how storm monsters treat NPCs, and natural storms no longer happen.

## Getting the source

This fork has no prebuilt releases. Clone this repository and check out the `0.H-custom` branch, then build it as described below.

## Compile

Please read [COMPILING.md](doc/COMPILING/COMPILING.md) - it covers general information and more specific recipes for Linux, OS X, Windows and BSD. See [COMPILER_SUPPORT.md](doc/COMPILING/COMPILER_SUPPORT.md) for details on which compilers we support. And you can always dig for more information in [doc/](doc/).

We also have the following build guides:
* Building on Windows with `MSYS2` at [COMPILING-MSYS.md](doc/COMPILING/COMPILING-MSYS.md)
* Building on Windows with `vcpkg` at [COMPILING-VS-VCPKG.md](doc/COMPILING/COMPILING-VS-VCPKG.md)
* Building with `cmake` at [COMPILING-CMAKE.md](doc/COMPILING/COMPILING-CMAKE.md)  (*unofficial guide*)

## Licence and credits

Cataclysm: Dark Days Ahead is the result of contributions from over 1000 volunteers under the Creative Commons Attribution ShareAlike 3.0 license. The code and content of the game is free to use, modify, and redistribute for any purpose whatsoever. See https://creativecommons.org/licenses/by-sa/3.0/ for details.
Some code distributed with the project is not part of the project and is released under different software licenses; the files covered by different software licenses have their own license notices.

This fork exists only because of the work of those volunteers. Any changes made here are this fork's own and are not theirs.

## Frequently Asked Questions

#### Is there a tutorial?

Yes, you can find the tutorial in the **Special** menu at the main menu (be aware that due to many code changes the tutorial may not function). You can also access documentation in-game via the `?` key.

#### How can I change the key bindings?

Press the `?` key, followed by the `1` key to see the full list of key commands. Press the `+` key to add a key binding, select which action with the corresponding letter key `a-w`, and then the key you wish to assign to that action.

#### How can I start a new world?

**World** on the main menu will generate a fresh world for you. Select **Create World**.

#### I've found a bug or have a suggestion. What should I do?

This fork currently offers no support channels beyond this repository. Please do not report problems with this fork to the official Cataclysm: Dark Days Ahead project: its developers have no involvement with it.

#### Does this fork use AI-assisted development?

Yes. This fork is developed with extensive AI assistance, and that will continue. Some players object to AI-assisted development, and that is a reasonable position; if it is yours, this fork may not be for you.

The official Cataclysm: Dark Days Ahead project takes the opposite approach: since March 2025 its contributing guidelines have stated that LLM-generated contributions are not acceptable for inclusion. Nothing in this fork reflects on the official project's work or policies.

> [!IMPORTANT]
> **This is an unofficial fork.** This repository is an independent fork of
> [Cataclysm: Dark Days Ahead](https://github.com/CleverRaven/Cataclysm-DDA), based on the
> 0.I-1 stable release. It is not affiliated with, endorsed by or supported by
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

## Changes from 0.I

This fork is based on the 0.I stable branch (0.I-1). It carries forward the changes this fork made to 0.H, and differs from 0.I as follows.

**Core game**

* **Classic CBM acquisition.** Bionics turn up in loot again and can be harvested from bionic zombies, as in 0.F, instead of coming from the Exodii. Doctor's offices have autodocs, some bionic basements and bunker basements have medical bays, and black-ops zombies carry the bio-operator implants.
* **Exodii as a baseless scavenger faction.** Their castle, safehouse, warehouse, NPCs (including 0.I's weaponmaster and workers), trade, missions, warehouse search quest and castle scenario are gone. They appear only at rare crashed-pod sites in the wild.
* **No natural portal storms.** The storm-driven scenarios and the Hub 01 contract that needed a storm are removed. Storms can still be started from the debug weather menu or by mod content that causes them on purpose.
* **Skill rust off by default.** The world option removed after 0.G (full, capped or off) is back, defaulting to off.
* **Hidden world options shown.** Twelve world-generation options that 0.I hides from the options menu are visible and documented.
* **Rivtech content restored.** Reverts upstream's removal of the RM120c, RM20, RM228, RM298, RM614, RM88, RM216 SPIW and RM232 IDW, the 5x50mm and 20x66mm ammunition and magazines, the 8x40mm drums and the 8mm variants, and its Rivtech gun nerfs.
* **Pneumatic weapons restored.** The pneumatic assault rifle, bolt driver and shotgun, with shotcanister ammunition.
* **Classic sci-fi content restored.** Robots (chicken walker and tank drone with JSON attacks in place of their removed hardcoded ones, copbot, riotbot, eyebot, laser turret, mininuke hack), the railgun, shock absorber and fusion blaster CBMs, the laser cannon, heavy rail rifle, mininuke launcher, plasma gun and rifle, RM99 revolver, advanced UPS, solar gear, matching vehicle turrets and the atomic sports car with its minireactor.
* **Classic power armour.** The combat, field and heavy combat exoskeletons and their environmental helmets return beside 0.I's modular exoskeletons.
* **Atomic cells and the trickle charger.** Light-minus, light and medium atomic cells return, sized to the same energy-density limits 0.I applies to its heavy atomic cell, as does the trickle charger CBM. The engine now applies trickle charging once per turn instead of once per installed CBM.
* **Live missile silos and vault loot.** Missile silos are active, guarded sites again, and bank, industry and mall vaults hold their science and military loot.
* **Unlimited atomic coffeemaker.** It heats from its own power source again, as in 0.G.
* **Military Professions mainlined.** Military Rifleman, Operator Recon and Operator CBRN are core professions; old worlds drop the removed mod on load.
* **Explicit lengths** for long items that lacked them.

**Aftershock**

* **This fork's Aftershock, not 0.I's.** 0.I marks Aftershock obsolete; this fork carries its own 0.H-based version over, converted to 0.I's data format, and keeps it active.
* **Earth setting.** The Salus IV colony, exoplanet locations, Whately family and UPLIFT content are removed. Remaining items and lore are reassigned to organisations already in the game, such as Northrop, Rivtech, Shady Hills Corporation, Hub 01, FEMA and XEDRA.
* **Fewer overrides of core content.** Aftershock no longer replaces core items, vehicles or mechanics, except the pressure tank, which its Rocket Jumper profession needs.
* **Selected exoplanet content.** Guns, ammunition, clothing, armour, CBMs and tools from 0.I's Aftershock: Exoplanet that fit an Earth setting are imported and re-themed; that mod is marked obsolete.
* **Data fixes.** Item weights, volumes and lengths, spawns, faction relations and mutation purification are corrected.

**Cataclysm++**

* **Included as an in-repo mod.** [Cataclysm++](https://github.com/Noctifer-de-Mortem/nocts_cata_mod) by Noctifer and contributors (public domain, The Unlicense) is imported from its upstream commit `46982a6` and converted from 0.J's data format to 0.I's. [`UPSTREAM.md`](data/mods/Cataclysm++/UPSTREAM.md) records what was left out and how to take later versions.
* **Fits this fork's restored content.** It no longer overrides the laser cannon or laser turret. It keeps the 0.I content upstream dropped for 0.J: its professions in the Lab Patient and Lab Staff challenge scenarios, the CVD machine in its lab and the atomic lamp on its survivor bus. Its CBMs drop from bionic zombies as well as turning up in loot.
* **Works with Generic Guns.** Its black-powder cartridges become Generic Guns' black-powder balls, and the survivor cowboy hat's ammo band takes Generic Guns' ammunition types.
* **Data fixes.** Item groups it extended lost their core contents and the survivor's flamethrower lost three flags, both through 0.I's handling of `extend`; the Prepper's Rambo knife did not fit its sheath; and item weights, volumes and text are corrected.

**Arcana and Magic Items**

* **Included as an in-repo mod.** [Arcana and Magic Items](https://github.com/chaosvolt/cdda-arcana-mod) by Chaosvolt (CC BY-SA 3.0) is imported from the final Dark Days Ahead release in its now-archived repository (commit `33bfbbe`) and converted from DDA experimental's data format to 0.I's. [`UPSTREAM.md`](data/mods/Arcana/UPSTREAM.md) records the source and what was left out.
* **Fits this fork.** Its CBMs drop from this fork's bionic zombies as well as from zomborgs, and its extensions of the portal-storm scenarios this fork removed are dropped. Content its last update removed for 0.J, which this fork still has, is back: the archaeologist profession in Urban Awakening, the survivor machete in two martial arts' weapon lists, and the summoned shadow's removal of its parent's electric shock.
* **Works with other in-repo mods.** Its interactions with Cataclysm++ and CrazyCataclysm follow those mods' group names here, and under Generic Guns its blessed shells take Generic Guns' ammunition types.
* **Data fixes.** It extends the core nether, cult and triffid monster factions instead of replacing them, its CrazyCataclysm skeltal drops all three of its items again, its warehouse lab gets its roof, and item weights, volumes and text are corrected.

**Other in-repo mods**

* **Exodii removal** extends to Magiclysm (forge diviner mission, CBM store additions), Mind Over Matter (Rubik), Xedra Evolved, DinoMod and Translate Dialogue.
* **Xedra Evolved.** Its roadside Jotunn encounter spawns.
* **Data fixes for Xedra Evolved and Mind Over Matter.** Faction relations are made mutual, Xedra's lineage traits are non-purifiable as upstream later made them, Mind Over Matter's concentration and noetic traits can be purified, the core lab terrains Mind Over Matter disables are flagged as such, and impossible item weights and volumes are corrected.
* **Portal Storms Ignore NPCs** (`personal_portal_storms`) is marked obsolete: it only changes how storm monsters treat NPCs, and natural storms no longer happen.

## Downloads

Prebuilt packages are on the [Releases page](https://github.com/acererak-casts-disintegrate/Cataclysm-DDA/releases):

* **Windows x64**: `windows-with-graphics-and-sounds` includes the CC-Sounds soundpack; `windows-with-graphics` does not. Unzip anywhere and run `cataclysm-tiles.exe`.
* **Linux x64**: `linux-with-graphics-and-sounds`, a tarball of the tiles build with CC-Sounds.

The sound builds bundle [CC-Sounds](https://github.com/Fris0uman/CDDA-Soundpacks) by Fris0uman and contributors. **Music by CO.AG** ([YouTube](https://www.youtube.com/channel/UCcavSftXHgxLBWwLDm_bNvA), [Patreon](https://www.patreon.com/user?u=3550597)), used with their permission. Its sound effects come from [freesound.org](https://freesound.org/), credited in each sound folder's `credits.md`.

There are no macOS or Android builds. Each release is built from a commit on the `0.I-custom` branch by `.github/workflows/release.yml`; its notes link the exact commit.

## Getting the source

Clone this repository and check out the `0.I-custom` branch, then build it as described below. The previous, 0.H-based version of this fork is on the `0.H-custom` branch.

## Compile

Please read [COMPILING.md](doc/c++/COMPILING.md) - it covers general information and more specific recipes for Linux, OS X, Windows and BSD. See [COMPILER_SUPPORT.md](doc/c++/COMPILER_SUPPORT.md) for details on which compilers we support. And you can always dig for more information in [doc/](doc/).

We also have the following build guides:
* Building on Windows with `MSYS2` at [COMPILING-MSYS.md](doc/c++/COMPILING-MSYS.md)
* Building on Windows with `vcpkg` at [COMPILING-VS-VCPKG.md](doc/c++/COMPILING-VS-VCPKG.md)
* Building with `cmake` at [COMPILING-CMAKE.md](doc/c++/COMPILING-CMAKE.md)  (*unofficial guide*)

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

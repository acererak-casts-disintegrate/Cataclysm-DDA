# Changes from Cataclysm: Dark Days Ahead 0.I

This fork is based on the 0.I stable release (0.I-1). It carries forward the changes this fork made to 0.H, and differs from 0.I as set out below. The [README](README.md) has a short summary.

* [Core game](#core-game)
* [Aftershock](#aftershock)
* [Cataclysm++](#cataclysm)
* [Arcana and Magic Items](#arcana-and-magic-items)
* [Other in-repo mods](#other-in-repo-mods)
* [Builds, platforms and code](#builds-platforms-and-code)


## Core game

* **Classic CBM acquisition.** Bionics turn up in loot again and can be harvested from bionic zombies, as in 0.F, instead of coming from the Exodii. Doctor's offices have autodocs, some bionic basements and bunker basements have medical bays, and black-ops zombies carry the bio-operator implants.
* **Exodii as a baseless scavenger faction.** Their castle, safehouse, warehouse, NPCs (including 0.I's weaponmaster and workers), trade, missions, warehouse search quest and castle scenario are gone. They appear only at rare crashed-pod sites in the wild.
* **No natural portal storms.** The storm-driven scenarios and the Hub 01 contract that needed a storm are removed. Storms can still be started from the debug weather menu or by mod content that causes them on purpose.
* **Skill rust off by default.** The world option removed after 0.G (full, capped or off) is back, defaulting to off.
* **Hidden world options shown.** Twelve world-generation options that 0.I hides from the options menu are visible and documented.
* **Brand names on by default.** The "Show drug brand names" and "Show gun brand names" options default to on, so items show names such as "Adderall" and "m4a1" rather than "prescription stimulant" and "NATO assault rifle". Existing option settings are kept.
* **Rivtech content restored.** Reverts upstream's removal of the RM120c, RM20, RM228, RM298, RM614, RM88, RM216 SPIW and RM232 IDW, the 5x50mm and 20x66mm ammunition and magazines, the 8x40mm drums and the 8mm variants, and its Rivtech gun nerfs.
* **Pneumatic weapons restored.** The pneumatic assault rifle, bolt driver and shotgun, with shotcanister ammunition.
* **Classic sci-fi content restored.** Robots (chicken walker and tank drone with JSON attacks in place of their removed hardcoded ones, copbot, riotbot, eyebot, laser turret, mininuke hack), the railgun, shock absorber and fusion blaster CBMs, the laser cannon, heavy rail rifle, mininuke launcher, plasma gun and rifle, RM99 revolver, advanced UPS, solar gear, matching vehicle turrets and the atomic sports car with its minireactor.
* **Classic power armour.** The combat, field and heavy combat exoskeletons and their environmental helmets return beside 0.I's modular exoskeletons.
* **Atomic cells and the trickle charger.** Light-minus, light and medium atomic cells return, sized to the same energy-density limits 0.I applies to its heavy atomic cell, as does the trickle charger CBM. The engine now applies trickle charging once per turn instead of once per installed CBM.
* **Live missile silos and vault loot.** Missile silos are active, guarded sites again, and bank, industry and mall vaults hold their science and military loot.
* **Unlimited atomic coffeemaker.** It heats from its own power source again, as in 0.G.
* **Military Professions mainlined.** Military Rifleman, Operator Recon and Operator CBRN are core professions; old worlds drop the removed mod on load.
* **Explicit lengths** for long items that lacked them.

## Aftershock

* **This fork's Aftershock, not 0.I's.** 0.I marks Aftershock obsolete; this fork carries its own 0.H-based version over, converted to 0.I's data format, and keeps it active.
* **Earth setting.** The Salus IV colony, exoplanet locations, Whately family and UPLIFT content are removed. Remaining items and lore are reassigned to organisations already in the game, such as Northrop, Rivtech, Shady Hills Corporation, Hub 01, FEMA and XEDRA.
* **Fewer overrides of core content.** Aftershock no longer replaces core items, vehicles or mechanics, except the pressure tank, which its Rocket Jumper profession needs.
* **Selected exoplanet content.** Guns, ammunition, clothing, armour, CBMs and tools from 0.I's Aftershock: Exoplanet that fit an Earth setting are imported and re-themed; that mod is marked obsolete.
* **Data fixes.** Item weights, volumes and lengths, spawns, faction relations and mutation purification are corrected.

## Cataclysm++

* **Included as an in-repo mod.** [Cataclysm++](https://github.com/Noctifer-de-Mortem/nocts_cata_mod) by Noctifer and contributors (public domain, The Unlicense) is imported from its upstream commit `46982a6` and converted from 0.J's data format to 0.I's. [`UPSTREAM.md`](data/mods/Cataclysm++/UPSTREAM.md) records what was left out and how to take later versions.
* **Fits this fork's restored content.** It no longer overrides the laser cannon or laser turret. It keeps the 0.I content upstream dropped for 0.J: its professions in the Lab Patient and Lab Staff challenge scenarios, the CVD machine in its lab and the atomic lamp on its survivor bus. Its CBMs drop from bionic zombies as well as turning up in loot.
* **Works with Generic Guns.** Its black-powder cartridges become Generic Guns' black-powder balls, and the survivor cowboy hat's ammo band takes Generic Guns' ammunition types.
* **Data fixes.** Item groups it extended lost their core contents and the survivor's flamethrower lost three flags, both through 0.I's handling of `extend`; the Prepper's Rambo knife did not fit its sheath; and item weights, volumes and text are corrected.

## Arcana and Magic Items

* **Included as an in-repo mod.** [Arcana and Magic Items](https://github.com/chaosvolt/cdda-arcana-mod) by Chaosvolt (CC BY-SA 3.0) is imported from the final Dark Days Ahead release in its now-archived repository (commit `33bfbbe`) and converted from DDA experimental's data format to 0.I's. [`UPSTREAM.md`](data/mods/Arcana/UPSTREAM.md) records the source and what was left out.
* **Fits this fork.** Its CBMs drop from this fork's bionic zombies as well as from zomborgs, and its extensions of the portal-storm scenarios this fork removed are dropped. Content its last update removed for 0.J, which this fork still has, is back: the archaeologist profession in Urban Awakening, the survivor machete in two martial arts' weapon lists, and the summoned shadow's removal of its parent's electric shock.
* **Works with other in-repo mods.** Its interactions with Cataclysm++ and CrazyCataclysm follow those mods' group names here, and under Generic Guns its blessed shells take Generic Guns' ammunition types.
* **Data fixes.** It extends the core nether, cult and triffid monster factions instead of replacing them, its CrazyCataclysm skeltal drops all three of its items again, its warehouse lab gets its roof, and item weights, volumes and text are corrected.

## Other in-repo mods

* **Exodii removal** extends to Magiclysm (forge diviner mission, CBM store additions), Mind Over Matter (Rubik), Xedra Evolved, DinoMod and Translate Dialogue.
* **Xedra Evolved.** Its roadside Jotunn encounter spawns.
* **Data fixes for Xedra Evolved and Mind Over Matter.** Faction relations are made mutual, Xedra's lineage traits are non-purifiable as upstream later made them, Mind Over Matter's concentration and noetic traits can be purified, the core lab terrains Mind Over Matter disables are flagged as such, and impossible item weights and volumes are corrected.
* **Portal Storms Ignore NPCs** (`personal_portal_storms`) is marked obsolete and no longer in the default mod list for new worlds: it only changes how storm monsters treat NPCs, and natural storms no longer happen.

## Builds, platforms and code

* **Marked as a fork in game.** The main menu shows the build's version, with the release tag or commit, and says it is an unofficial fork of 0.I-1 in place of 0.I's fixed "Stable Release" line.
* **Prebuilt packages.** Each release has Windows (graphics, and graphics with sound), Linux (graphics with sound) and universal macOS (graphics with sound, and terminal-only) packages, built by [`.github/workflows/release.yml`](.github/workflows/release.yml). The sound builds bundle [CC-Sounds](https://github.com/Fris0uman/CDDA-Soundpacks) by Fris0uman and contributors, with music by CO.AG used with their permission. The macOS packages are not signed by Apple; the README explains how to open them.
* **Continuous integration.** Every push to `0.I-custom` builds the game on Linux and runs the full test suite for the core game and, separately, for Magiclysm, Aftershock, Xedra Evolved, Mind Over Matter, Bionic Professions, Cataclysm++ and Arcana, then checks that every mod loads, in groups of mods that work together. It also builds and tests on Windows (MSVC) and, in virtual machines, on FreeBSD, OpenBSD and NetBSD. A weekly job tries DragonFly BSD, MidnightBSD, Haiku and OmniOS.
* **Portability fixes.** Making the code build and pass its tests on those systems fixed bugs that affect every platform:
  * Several places passed bytes of UTF-8 text straight to `isspace`, `isdigit` and similar functions, which is undefined behaviour for non-ASCII characters (and aborted on NetBSD). They now convert to `unsigned char` first or check the range.
  * Unqualified `erf`, `erfc`, `sqrt` and `abs` calls could pick C's `double` or `int` versions instead of C++'s overloads; they now call the `std::` ones.
  * Range-for loops that copied each element into a `const` variable, some of them whole `unordered_set`s per entry, now bind by reference.
  * The bundled flatbuffers library reads numbers independently of the locale on OpenBSD, Haiku and illumos, which lack some of the `strto*_l` functions it used.
  * The Makefile recognises OpenBSD, builds plain archives where `ar` has no `--thin`, uses clang by default on FreeBSD, OpenBSD and MidnightBSD, and treats ncurses' headers as system headers.
  * Tests that depend on the C library's locale support (localized sorting and number grouping) skip their localized checks where the C library ignores those locale settings, as on OpenBSD and NetBSD.
* **Compiling guides.** The guides in [`doc/c++/`](doc/c++/) build this fork rather than upstream, document how the macOS packages are built, and give current FreeBSD, OpenBSD and NetBSD recipes.

# Changes from Cataclysm: Dark Days Ahead 0.I

This fork is based on the 0.I stable release (0.I-1). It carries forward the changes this fork made to 0.H, and differs from 0.I as set out below. The [README](README.md) has a short summary.

* [Core game](#core-game)
* [Aftershock](#aftershock)
* [Cataclysm++](#cataclysm)
* [Arcana and Magic Items](#arcana-and-magic-items)
* [3D Printing](#3d-printing)
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
* **Padding thin clothing works.** Clothing mods that scale with a garment's thickness, such as innawood's leather, Kevlar and steel padding and Arcana's bark weaves, gave nothing to garments under 1 mm thick, which is most clothing, and rounded thicker ones down to whole millimetres.
* **British English.** A British English language option, generated from the game's text by [`lang/en_GB/`](lang/en_GB/README.md): common *-ise* spelling (armour, colour, centre, grey) and a short list of unambiguous vocabulary (trousers, petrol, car park, tinned). Words that would clash with another item stay American, so a flashlight is not a torch. "English" is now listed as "American English". With the language set to "System language", English set to the United Kingdom, Ireland, Australia or New Zealand picks British English.

## Aftershock

* **This fork's Aftershock, not 0.I's.** 0.I marks Aftershock obsolete; this fork carries its own 0.H-based version over, converted to 0.I's data format, and keeps it active.
* **Earth setting.** The Salus IV colony, exoplanet locations, Whately family and UPLIFT content are removed. Remaining items and lore are reassigned to organisations already in the game, such as Northrop, Rivtech, Shady Hills Corporation, Hub 01, FEMA and XEDRA.
* **Fewer overrides of core content.** Aftershock no longer replaces core items, vehicles or mechanics, except the pressure tank, which its Rocket Jumper profession needs.
* **Selected exoplanet content.** Guns, ammunition, clothing, armour, CBMs and tools from 0.I's Aftershock: Exoplanet that fit an Earth setting are imported and re-themed; that mod is marked obsolete.
* **Data fixes.** Item weights, volumes and lengths, spawns, faction relations and mutation purification are corrected.
* **Electromagnetic compound bow.** A craftable compound bow with UPS-powered acceleration rails (20 kJ a shot). It fires any arrow whose shaft is metal, about two and a half times as hard as a high-draw compound bow, and is the only bow that takes the new ferromagnetic sabot arrows.

## Cataclysm++

* **Included as an in-repo mod.** [Cataclysm++](https://github.com/Noctifer-de-Mortem/nocts_cata_mod) by Noctifer and contributors (public domain, The Unlicense) is imported from its upstream commit `46982a6` and converted from 0.J's data format to 0.I's. [`UPSTREAM.md`](data/mods/Cataclysm++/UPSTREAM.md) records what was left out and how to take later versions.
* **Fits this fork's restored content.** It no longer overrides the laser cannon or laser turret. It keeps the 0.I content upstream dropped for 0.J: its professions in the Lab Patient and Lab Staff challenge scenarios, the CVD machine in its lab and the atomic lamp on its survivor bus. Its CBMs drop from bionic zombies as well as turning up in loot.
* **Works with Generic Guns.** Its black-powder cartridges become Generic Guns' black-powder balls, and the survivor cowboy hat's ammo band takes Generic Guns' ammunition types.
* **Data fixes.** Item groups it extended lost their core contents and the survivor's flamethrower lost three flags, both through 0.I's handling of `extend`; the Prepper's Rambo knife did not fit its sheath; and item weights, volumes and text are corrected.
* **The nano-mutagenic serum acts directly.** It used to apply a short marker effect that a background check looked for every second before mutating you; it now runs its mutation when injected, through 0.I's consumption effects. Saves made before the change load without side effects.

## Arcana and Magic Items

* **Included as an in-repo mod.** [Arcana and Magic Items](https://github.com/chaosvolt/cdda-arcana-mod) by Chaosvolt (CC BY-SA 3.0) is imported from the final Dark Days Ahead release in its now-archived repository (commit `33bfbbe`) and converted from DDA experimental's data format to 0.I's. [`UPSTREAM.md`](data/mods/Arcana/UPSTREAM.md) records the source and what was left out.
* **Fits this fork.** Its CBMs drop from this fork's bionic zombies as well as from zomborgs, and its extensions of the portal-storm scenarios this fork removed are dropped. Content its last update removed for 0.J, which this fork still has, is back: the archaeologist profession in Urban Awakening, the survivor machete in two martial arts' weapon lists, and the summoned shadow's removal of its parent's electric shock.
* **Works with other in-repo mods.** Its interactions with Cataclysm++ and CrazyCataclysm follow those mods' group names here, and under Generic Guns its blessed shells take Generic Guns' ammunition types.
* **Data fixes.** It extends the core nether, cult and triffid monster factions instead of replacing them, its CrazyCataclysm skeltal drops all three of its items again, its warehouse lab gets its roof, and item weights, volumes and text are corrected.
* **Mutation items act directly.** The blood effigy, refined blood offering, sacramental heart and restored ritual blade used to apply a short marker effect that a background check looked for every second before mutating you. They now run their mutation directly, through 0.I's consumption effects and item actions, with the same messages, charge costs and one-turn use. Saves made before the change load without side effects.
* **Bug fixes from the Bright Nights version.** Fixes Chaosvolt made to Arcana in Cataclysm: Bright Nights that apply here too:
  * The moruboru's stun works.
  * The hermit's map updates find the rural church from any floor.
  * The gilded aegis heals bleeding already under way.
  * Drain-life effects heal on killing blows as well as other hits.
  * Purifying shot's pellets do heat damage past point blank.
* **Additions from the Bright Nights version.**
  * Purifying .410 000 shot.
  * Drops for skeletal masters and zombie liches.
  * Silver glyphs and blank scrolls in cult crafting loot.
  * A belt clip for the moonstone scourge.
  * The distortion flow rotor, a roof-mounted motor and VTOL rotor in one. It is the only player-installable rotor, and flying still needs helicopter piloting.
  * The essence focus cell, a UPS whose built-in battery is charged by channelling dull essence into it at 5 kJ per mote.
  * Green light trails for wraithslayer bolts.
  * Refreshed sprites for the DeadPeople-based tilesets.
  * Chaosvolt's later rebalancing of several Arcana monsters and of the gold and silver in some crafted items.

## 3D Printing

* **New in-repo mod.** The 3D printers and carbon fiber crafting of Cataclysm: Bright Nights, rewritten for 0.I. [`UPSTREAM.md`](data/mods/3D_Printing/UPSTREAM.md) lists what was ported, changed and left out.
* **Printers.** The 3D printer prints plastic and carbon fiber items and repairs them. The advanced 3D printer also makes carbon fiber filament from plastic and repairs metal items. Either runs from a medium battery or a power cord, and can be placed as an appliance, mounted on a vehicle or kept in a workshop rig.
* **Metal printing.** The advanced printer sinters metal arrows, bolt points, nails, bearings, hinges, pipe fittings, lockpicks, steel magazines and the edges of carbon fiber blades from scrap. Anything with a sharp edge or point also needs filing or grinding.
* **Carbon fiber gear.** Armor, swords and other blades, a rifle, a machine pistol, a repeating crossbow, gunmods, a jerrycan, vehicle frames, walls, cargo space, plating and a bicycle, balanced against 0.I's steel equivalents. The core carbon fiber arrows, bolts, fishing spears and boat hull become printable.
* **Loot and a shop.** A 3D printing shop in towns, and printers and filament in electronics, science, lab and pawn shop loot.
* **Works with Generic Guns.** The carbon guns take generic ammunition and magazines, and the printers print Generic Guns' magazines.
* **Mounted repair tools.** Any repair tool on a vehicle, appliance or workshop rig now repairs from vehicle or grid power; the engine used to allow this for six named tools only.

## Other in-repo mods

* **Exodii removal** extends to Magiclysm (forge diviner mission, CBM store additions), Mind Over Matter (Rubik), Xedra Evolved, DinoMod and Translate Dialogue.
* **Xedra Evolved.** Its roadside Jotunn encounter spawns.
* **Data fixes for Xedra Evolved and Mind Over Matter.** Faction relations are made mutual, Xedra's lineage traits are non-purifiable as upstream later made them, Mind Over Matter's concentration and noetic traits can be purified, the core lab terrains Mind Over Matter disables are flagged as such, and impossible item weights and volumes are corrected.
* **Portal Storms Ignore NPCs** (`personal_portal_storms`) is marked obsolete and no longer in the default mod list for new worlds: it only changes how storm monsters treat NPCs, and natural storms no longer happen.

## Builds, platforms and code

* **Marked as a fork in game.** The main menu shows the build's version, with the release tag or commit, and says it is an unofficial fork of 0.I-1 in place of 0.I's fixed "Stable Release" line.
* **Prebuilt packages.** Each release has Windows (graphics, and graphics with sound), Linux (graphics with sound) and universal macOS (graphics with sound, and terminal-only) packages, built by [`.github/workflows/release.yml`](.github/workflows/release.yml). The sound builds bundle [CC-Sounds](https://github.com/Fris0uman/CDDA-Soundpacks) by Fris0uman and contributors, with music by CO.AG used with their permission. The macOS packages are not signed by Apple; the README explains how to open them.
* **Continuous integration.** Every push to `0.I-custom` builds the game on Linux and runs the full test suite for the core game and, separately, for Magiclysm, Aftershock, Xedra Evolved, Mind Over Matter, Bionic Professions, Cataclysm++, Arcana and 3D Printing, then checks that every mod loads, in groups of mods that work together. It also builds and tests on Windows (MSVC) and, in virtual machines, on FreeBSD, OpenBSD and NetBSD. A weekly job tries DragonFly BSD, MidnightBSD, Haiku and OmniOS. A separate check warns when the British English catalogue no longer matches the game's text.
* **Portability fixes.** Making the code build and pass its tests on those systems fixed bugs that affect every platform:
  * Several places passed bytes of UTF-8 text straight to `isspace`, `isdigit` and similar functions, which is undefined behaviour for non-ASCII characters (and aborted on NetBSD). They now convert to `unsigned char` first or check the range.
  * Unqualified `erf`, `erfc`, `sqrt` and `abs` calls could pick C's `double` or `int` versions instead of C++'s overloads; they now call the `std::` ones.
  * Range-for loops that copied each element into a `const` variable, some of them whole `unordered_set`s per entry, now bind by reference.
  * The bundled flatbuffers library reads numbers independently of the locale on OpenBSD, Haiku and illumos, which lack some of the `strto*_l` functions it used.
  * The Makefile recognises OpenBSD, builds plain archives where `ar` has no `--thin`, uses clang by default on FreeBSD, OpenBSD and MidnightBSD, and treats ncurses' headers as system headers.
  * Tests that depend on the C library's locale support (localized sorting and number grouping) skip their localized checks where the C library ignores those locale settings, as on OpenBSD and NetBSD.
* **Compiling guides.** The guides in [`doc/c++/`](doc/c++/) build this fork rather than upstream, document how the macOS packages are built, and give current FreeBSD, OpenBSD and NetBSD recipes.

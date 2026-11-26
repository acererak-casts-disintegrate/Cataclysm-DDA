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

This fork is based on the 0.I stable release (0.I-1) and carries forward the changes it made to 0.H. **[CHANGES.md](CHANGES.md) lists them in full.** In short:

* **Core game:** classic bionic acquisition (loot and bionic zombies, not the Exodii), the Exodii reduced to a rare scavenger faction, no natural portal storms, skill rust off by default, restored Rivtech, pneumatic, classic sci-fi, power armour and atomic-cell content, and a British English language option.
* **Aftershock:** this fork's own version, set on Earth, kept active and overriding much less of the core game.
* **Cataclysm++** and **Arcana and Magic Items:** included as in-repo mods, converted to 0.I and fitted to this fork.
* **3D Printing:** a new in-repo mod with Bright Nights' 3D printers and carbon fiber crafting, plus metal printing.
* **Other in-repo mods:** Exodii removal and data fixes for Magiclysm, Mind Over Matter, Xedra Evolved and others.
* **Builds:** prebuilt Windows, Linux and macOS packages; CI also builds and tests the game on FreeBSD, OpenBSD and NetBSD.

## Downloads

Prebuilt packages are on the [Releases page](https://github.com/acererak-casts-disintegrate/Cataclysm-DDA/releases):

* **Windows x64**: `windows-with-graphics-and-sounds` includes the CC-Sounds soundpack; `windows-with-graphics` does not. Unzip anywhere and run `cataclysm-tiles.exe`.
* **Linux x64**: `linux-with-graphics-and-sounds`, a tarball of the tiles build with CC-Sounds.
* **macOS 10.15 or later**, Intel and Apple silicon alike: `osx-with-graphics-and-sounds-universal` is the tiles build with CC-Sounds; `osx-terminal-only-universal` runs the game in Terminal. Open the `.dmg` and drag Cataclysm to Applications.

The sound builds bundle [CC-Sounds](https://github.com/Fris0uman/CDDA-Soundpacks) by Fris0uman and contributors. **Music by CO.AG** ([YouTube](https://www.youtube.com/channel/UCcavSftXHgxLBWwLDm_bNvA), [Patreon](https://www.patreon.com/user?u=3550597)), used with their permission. Its sound effects come from [freesound.org](https://freesound.org/), credited in each sound folder's `credits.md`.

The macOS builds are not signed or notarised by Apple, so macOS blocks the first launch. On macOS 15 (Sequoia) or later, try to open Cataclysm once, then go to **System Settings → Privacy & Security**, click **Open Anyway** next to the message about Cataclysm and confirm. On earlier versions, Control-click Cataclysm in Applications, choose **Open**, then **Open** again. macOS remembers the choice.

There are no Android builds. Each release is built from a commit on the `0.I-custom` branch by `.github/workflows/release.yml`; its notes link the exact commit.

## Getting the source

Clone this repository and check out the `0.I-custom` branch, then build it as described below. The previous, 0.H-based version of this fork is on the `0.H-custom` branch.

## Compile

Please read [COMPILING.md](doc/c++/COMPILING.md) - it covers general information and more specific recipes for Linux, macOS, Windows and the BSDs (FreeBSD, OpenBSD and NetBSD are built and tested by CI). The Android recipe there is untested in this fork. See [COMPILER_SUPPORT.md](doc/c++/COMPILER_SUPPORT.md) for details on which compilers we support. And you can always dig for more information in [doc/](doc/).

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

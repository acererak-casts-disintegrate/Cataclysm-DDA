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

## Getting the source

This fork has no prebuilt releases. Clone this repository and check out the `0.H-custom` branch, then build it as described below.

## Compile

Please read [COMPILING.md](doc/COMPILING/COMPILING.md) - it covers general information and more specific recipes for Linux, OS X, Windows and BSD. See [COMPILER_SUPPORT.md](doc/COMPILING/COMPILER_SUPPORT.md) for details on which compilers we support. And you can always dig for more information in [doc/](doc/).

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

# Compiling
* [General Linux Guide](#general-linux-guide)
  * [Compiler](#compiler)
  * [Tools](#tools)
  * [Dependencies](#dependencies)
  * [Make flags](#make-flags)
  * [Compiling localization files](#compiling-localization-files)
* [Fedora](#fedora)
  * [ncurses builds](#ncurses-builds)
  * [SDL builds](#sdl-builds)
* [Debian](#debian)
  * [Linux (native) ncurses builds](#linux-native-ncurses-builds)
  * [Linux (native) SDL builds](#linux-native-sdl-builds)
  * [Cross-compiling to linux 32-bit from linux 64-bit](#cross-compiling-to-linux-32-bit-from-linux-64-bit)
  * [Cross-compile to Windows from Linux](#cross-compile-to-windows-from-linux)
  * [Cross-compile to macOS from Linux](#cross-compile-to-macos-from-linux) (out of date)
  * [Cross-compile to Android from Linux](#cross-compile-to-android-from-linux) (untested in this fork)
* [macOS](#macos)
  * [Building like the release packages](#building-like-the-release-packages)
  * [Advanced info for Developers](#advanced-info-for-developers)
  * [Troubleshooting](#macos-troubleshooting)
* [Windows](#windows)
  * [Building with Visual Studio](#building-with-visual-studio)
  * [Building with MSYS2](#building-with-msys2)
  * [Building with CYGWIN](#building-with-cygwin)
  * [Building with Clang and MinGW64](#building-with-clang-and-mingw64)
* [BSDs](#bsds)
  * [FreeBSD](#freebsd)
  * [OpenBSD](#openbsd)
  * [NetBSD](#netbsd)
  * [Other systems](#other-systems)

# General Linux Guide

To build Cataclysm from source you will need at least a C++ compiler, some basic developer tools, and necessary build dependencies. The exact package names vary greatly from distro to distro, so this part of the guide is intended to give you higher-level understanding of the process.

## Compiler

You have three major choices here: GCC, Clang and MXE.

  * GCC is almost always the default on Linux systems so it's likely you already have it
  * Clang is usually faster than GCC, so it's worth installing if you plan to keep up with the latest experimentals
  * MXE is a cross-compiler, so of any importance only if you plan to compile for Windows on your Linux machine

(Note that your distro may have separate packages e.g. `gcc` only includes the C compiler and for C++ you'll need to install `g++`.)

Cataclysm is targeting the C++17 standard and that means you'll need a compiler that supports it. You can check if your C++ compiler supports the standard by reading [COMPILER_SUPPORT.md](./COMPILER_SUPPORT.md)

The general rule is the newer the compiler the better.

## Tools

Most distros seem to package essential build tools as either a single package (Debian and derivatives have `build-essential`) or a package group (Arch has `base-devel`). You should use the above if available. Otherwise you'll at least need `make` and figure out the missing dependencies as you go (if any).

Besides the essentials you will need `git`.

If you plan on keeping up with experimentals you should also install `ccache`, which  will considerably speed-up partial builds.

## Dependencies

There are some general dependencies, optional dependencies, and then specific dependencies for either curses or tiles builds. The exact package names again depend on the distro you're using, and whether your distro packages libraries and their development files separately (e.g. Debian and derivatives).

Rough list based on building on Arch:

  * General: `gcc-libs`, `glibc`, `zlib`, `bzip2`
  * Optional: `gettext`
  * Curses: `ncurses`
  * Tiles: `sdl2`, `sdl2_image`, `sdl2_ttf`, `sdl2_mixer`, `freetype2`

E.g. for curses build on Debian and derivatives you'll also need `libncurses5-dev` or `libncursesw5-dev`.

Note on optional dependencies:

  * `gettext` - for localization support; if you plan to only use English you can skip it

You should be able to figure out what you are missing by reading the compilation errors and/or the output of `ldd` for compiled binaries.

## Make flags

Given you're building from source you have a number of choices to make:

  * `NATIVE=` - you should only care about this if you're cross-compiling
  * `RELEASE=1` - without this you'll get a debug build (see note below)
  * `LTO=1` - enables link-time optimization with GCC/Clang
  * `TILES=1` - with this you'll get the tiles version, without it the curses version
  * `SOUND=1` - if you want sound
  * `LOCALIZE=0` - this disables localizations so `gettext` is not needed
  * `CLANG=1` - use Clang instead of GCC (the default on macOS, FreeBSD, OpenBSD and MidnightBSD; `CLANG=0` overrides it)
  * `CCACHE=1` - use ccache
  * `USE_LIBCXX=1` - use libc++ instead of libstdc++ with Clang (the default on macOS and the BSDs)
  * `PREFIX=DIR` - causes `make install` to place binaries and data files to DIR (see note below)

There is a couple of other possible options - feel free to read the [`Makefile`](../../Makefile).

If you have a multi-core computer you'd probably want to add `-jX` to the options, where `X` is your CPU's number of threads (generally twice the number of your CPU cores). Alternatively, you can add `-j$(nproc)` for the build to use all of your CPU processors.

Examples:
- `make -j4 CLANG=1 CCACHE=1 NATIVE=linux64 RELEASE=1 TILES=1`
- `make -j$(nproc) CLANG=1 TILES=1 SOUND=0`

The above will build a tiles release explicitly for 64 bit Linux, using Clang and ccache and 4 parallel processes.

Example: `make -j2 LOCALIZE=0`

The above will build a debug-enabled curses version for the architecture you are using, using GCC and 2 parallel processes.

**Note on debug**:
You should probably always build with `RELEASE=1` unless you experience segfaults and are willing to provide stack traces.

**Note on PREFIX**:
PREFIX specifies a directory which will be the prefix for binaries, resources, and documentation files. Compiling with PREFIX means cataclysm will read files from PREFIX directory. This can be overridden with `--datadir` (e.g. if you used `PREFIX=DIR` in earlier build, then specify `--datadir DIR/share/cataclysm-dda`).

## Compiling localization files

If you want to compile localization files for specific languages, you can add the `LANGUAGES="<lang_id_1> [lang_id_2] [...]"` option to the `make` command:

    make LANGUAGES="zh_CN zh_TW"

You can get the language ID from the filenames of `*.po` in `lang/po` directory. Setting `LOCALIZE=1` only may not tell `make` to compile those localization files for you.

# Accelerating Linux builds with llama

[llama](https://github.com/nelhage/llama) is a CLI tool for outsourcing computation to AWS Lambda.  If you want your builds to run faster and are willing to pay Amazon for the privilege, then you may be able to use it to accelerate your builds.  See [our llama README](../../tools/llama/README.md) for more details.

# Fedora
## Ncurses builds

Dependencies:

  * ncurses
  * g++ and make

Install:

    sudo dnf install astyle gcc-c++ ncurses-devel make

### Building

Run:

    make

## SDL builds

Dependencies:

  * SDL2
  * SDL2_image
  * SDL2_ttf
  * freetype
  * g++ and make
  * libsdl2-mixer-dev - Used if compiling with sound support.

Install:

    sudo dnf install astyle gcc-c++ SDL2-devel SDL2_image-devel SDL2_ttf-devel SDL2_mixer-devel freetype-devel make

### Building

A simple installation could be done by simply running:

    make TILES=1

A more comprehensive alternative is:

    make -j2 TILES=1 SOUND=1 RELEASE=1 USE_HOME_DIR=1

The -j2 flag means it will compile with two parallel processes. It can be omitted or changed to -j4 in a more modern processor. If there is no desire to have sound, those flags can also be omitted. The USE_HOME_DIR flag places the user files, like configurations and saves, into the home folder, making it easier for backups, and can also be omitted.

# Gentoo
If you want sound and graphics, make sure to emerge with the following:

```bash
USE="vorbis png" \
 emerge -1va emerge media-libs/libsdl2 media-libs/sdl2-gfx media-libs/sdl2-image media-libs/sdl2-mixer media-libs/sdl2-ttf
```

Once the above libraries are installed, compile with:

    make -j$(nproc) TILES=1 SOUND=1 RELEASE=1


# Debian

Instructions for compiling on a Debian-based system. The package names here are valid for Ubuntu 12.10 and may or may not work on your system.

The building instructions below always assume you are running them from the Cataclysm:DDA source directory.


## Linux (native) ncurses builds

Dependencies:

  * ncurses or ncursesw (for multi-byte locales)
  * build essentials

Install:

    sudo apt-get install libncurses5-dev libncursesw5-dev build-essential astyle

### Building

Run:

    make

## Linux (native) SDL builds

Dependencies:

  * SDL
  * SDL_ttf
  * freetype
  * build essentials
  * libsdl2-mixer-dev - Used if compiling with sound support.

Install:

    sudo apt-get install libsdl2-dev libsdl2-ttf-dev libsdl2-image-dev libsdl2-mixer-dev libfreetype6-dev build-essential

### Building

A simple installation could be done by simply running:

    make TILES=1

A more comprehensive alternative is:

    make -j2 TILES=1 SOUND=1 RELEASE=1 USE_HOME_DIR=1

The -j2 flag means it will compile with two parallel processes. It can be omitted or changed to -j4 in a more modern processor. If there is no desire to have sound, those flags can also be omitted. The USE_HOME_DIR flag places the user files, like configurations and saves, into the home folder, making it easier for backups, and can also be omitted.



## Cross-compiling to linux 32-bit from linux 64-bit

Dependencies:

  * 32-bit toolchain
  * 32-bit ncursesw (compatible with both multi-byte and 8-bit locales)

Install:

    sudo apt-get install libc6-dev-i386 lib32stdc++-dev g++-multilib lib32ncursesw5-dev

### Building

Run:

    make NATIVE=linux32

## Cross-compile to Windows from Linux

To cross-compile to Windows from Linux, you will need MXE, which changes your `make` command slightly. These instructions were written from Ubuntu 20.04, but should be applicable to any Debian-based environment. Please adjust all package manager instructions to match your environment.

Dependencies:

  * [MXE](http://mxe.cc)
  * [MXE Requirements](http://mxe.cc/#requirements)

Installation

<!-- astyle and lzip added to initial sudo apt install string to forestall complaints from MinGW and make -->
<!-- ncurses removed from make MXE_TARGETS because we're not gonna be cross-compiling ncurses -->

```bash
sudo apt install astyle autoconf automake autopoint bash bison bzip2 cmake flex gettext git g++ gperf intltool libffi-dev libgdk-pixbuf2.0-dev libtool libltdl-dev libssl-dev libxml-parser-perl lzip make mingw-w64 openssl p7zip-full patch perl pkg-config python3 ruby scons sed unzip wget xz-utils g++-multilib libc6-dev-i386 libtool-bin
mkdir -p ~/src/libbacktrace
cd ~/src
git clone https://github.com/acererak-casts-disintegrate/Cataclysm-DDA.git
git clone https://github.com/mxe/mxe.git
cd mxe
make -j$((`nproc`+0)) MXE_TARGETS='x86_64-w64-mingw32.static i686-w64-mingw32.static' MXE_PLUGIN_DIRS=plugins/gcc11 sdl2 sdl2_ttf sdl2_image sdl2_mixer gettext
cd ../libbacktrace/
wget https://github.com/Qrox/libbacktrace/releases/download/2020-01-03/libbacktrace-x86_64-w64-mingw32.tar.gz
wget https://github.com/Qrox/libbacktrace/releases/download/2020-01-03/libbacktrace-i686-w64-mingw32.tar.gz
tar -xzf libbacktrace-x86_64-w64-mingw32.tar.gz --exclude=LICENSE -C ~/src/mxe/usr/x86_64-w64-mingw32.static
tar -xzf libbacktrace-i686-w64-mingw32.tar.gz --exclude=LICENSE -C ~/src/mxe/usr/i686-w64-mingw32.static
```

Building all these packages from MXE might take a while, even on a fast computer. Be patient; the `-j` flag will take advantage of all your processor cores. If you are not planning on building for both 32-bit and 64-bit, you might want to adjust your MXE_TARGETS.  Additionally if not building for a particular target you can skip the curl and tar commands for the targets NOT being built.

An additional note: With C:DDA switching to gcc 11.2 with MXE (MingW), if you've previously built MXE you'll need to "make clean" and rebuild it to get gcc11.

Edit your `~/.profile` as follows:

```bash
export PLATFORM_32="~/src/mxe/usr/bin/i686-w64-mingw32.static-"
export PLATFORM_64="~/src/mxe/usr/bin/x86_64-w64-mingw32.static-"
```

This is to ensure that the variables for the `make` command will not get reset after a power cycle.

### Building (SDL)

    cd ~/src/Cataclysm-DDA

Run one of the following commands based on your targeted environment:

```bash
make -j$((`nproc`+0)) CROSS="${PLATFORM_32}" TILES=1 SOUND=1 RELEASE=1 LOCALIZE=1 bindist
make -j$((`nproc`+0)) CROSS="${PLATFORM_64}" TILES=1 SOUND=1 RELEASE=1 LOCALIZE=1 bindist
```


<!-- Building ncurses for Windows is a nonstarter, so the directions were removed. -->

## Cross-compile to macOS from Linux

**Out of date:** this section was written for a macOS 10.11 SDK, a 10.7 minimum and Ubuntu 14.04. The game now needs macOS 10.15 or later (see `-mmacosx-version-min` in the [`Makefile`](../../Makefile)), so these steps will not work as written, and nobody has tried them on this fork. To build for macOS, build on a Mac, or use the release workflow's macOS jobs.

This procedure is very much similar to cross-compilation to Windows from Linux.
It has ben tested on Ubuntu 14.04 LTS but it should work on other distros as well.

Please note that due to historical difficulties with cross-compilation errors, run-time optimizations are disabled for cross-compilation to Mac OS X targets. (`-O0` is specified as a compilation flag.) See [Pull Request #26564](https://github.com/CleverRaven/Cataclysm-DDA/pull/26564) for details.
### Dependencies

  * OSX cross-compiling toolchain [osxcross](https://github.com/tpoechtrager/osxcross)

  * `genisoimage` and [libdmg-hfsplus](https://github.com/planetbeing/libdmg-hfsplus.git) to create dmg distributions

Make sure that all dependency tools are in search `PATH` before compiling.

### Setup

To set up the compiling environment execute the following commands:
`git clone https://github.com/tpoechtrager/osxcross.git` to clone the toolchain
`cd osxcross`
`cp ~/MacOSX10.11.sdk.tar.bz2 ./tarballs/` to copy prepared MacOSX SDK tarball on place. [Read more about it](https://github.com/tpoechtrager/osxcross/blob/master/README.md#packaging-the-sdk)
`OSX_VERSION_MIN=10.7 ./build.sh` to build everything.
Note the targeted minimum supported version of OSX.

Have a prepackaged set of libs and frameworks in place since compiling with `osxcross` built-in MacPorts is rather difficult and not supported at the moment.
Your directory tree should look like:

    ~/
    ├── Frameworks
    │   ├── SDL2.framework
    │   ├── SDL2_image.framework
    │   ├── SDL2_mixer.framework
    │   └── SDL2_ttf.framework
    └── libs
        ├── gettext
        │   ├── include
        │   └── lib
        └── ncurses
            ├── include
            └── lib

Populated with respective frameworks, dylibs and headers.
Tested lib versions are libintl.8.dylib for gettext and libncurses.5.4.dylib for ncurses.
These libs were obtained from `homebrew` binary distribution at OS X 10.11.
Frameworks were obtained from the SDL official website as described in the next [section](#sdl).

### Building (SDL)

To build the full feature tiles and sound enabled version with localizations enabled:

```bash
make dmgdist CROSS=x86_64-apple-darwin15- NATIVE=osx USE_HOME_DIR=1 CLANG=1 \
  RELEASE=1 LOCALIZE=1 LANGUAGES=all TILES=1 SOUND=1 FRAMEWORK=1 \
  OSXCROSS=1 LIBSDIR=../libs FRAMEWORKSDIR=../Frameworks
```

Make sure that `x86_64-apple-darwin15-clang++` is in `PATH` environment variable.

### Building (ncurses)

To build the full curses version with localizations enabled:

```bash
make dmgdist CROSS=x86_64-apple-darwin15- NATIVE=osx USE_HOME_DIR=1 CLANG=1 \
  RELEASE=1 LOCALIZE=1 LANGUAGES=all OSXCROSS=1 LIBSDIR=../libs FRAMEWORKSDIR=../Frameworks
```

Make sure that `x86_64-apple-darwin15-clang++` is in `PATH` environment variable.

## Cross-compile to Android from Linux

**Untested in this fork:** this section is upstream's. This fork publishes no Android builds and its CI does not build the Android project, so expect to fix things along the way.

The Android build uses [Gradle](https://gradle.org/) to compile the java and native C++ code, and is based heavily off SDL's [Android project template](https://hg.libsdl.org/SDL/file/f1084c419f33/android-project). See the official SDL documentation [README-android.md](https://hg.libsdl.org/SDL/file/f1084c419f33/docs/README-android.md) for further information.

The Gradle project lives in the repository under `android/`. You can build it via the command line or open it in [Android Studio](https://developer.android.com/studio/). For simplicity, it only builds the SDL version with all features enabled, including tiles, sound and localization.

### Dependencies

  * Java JDK 8
  * SDL2 (tested with 2.0.8, though a custom fork is recommended with project-specific bugfixes)
  * SDL2_ttf (tested with 2.0.14)
  * SDL2_mixer (tested with 2.0.2)
  * SDL2_image (tested with 2.0.3)

The Gradle build process automatically installs dependencies from [deps.zip](/android/app/deps.zip).

### Setup

Install Linux dependencies. For a desktop Ubuntu installation:

    sudo apt-get install openjdk-8-jdk-headless

Install Android SDK and NDK:

```bash
wget https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip
unzip sdk-tools-linux-4333796.zip -d ~/android-sdk
rm sdk-tools-linux-4333796.zip
~/android-sdk/tools/bin/sdkmanager --update
~/android-sdk/tools/bin/sdkmanager "tools" "platform-tools" "ndk-bundle"
~/android-sdk/tools/bin/sdkmanager --licenses
```

Export Android environment variables (you can add these to the end of `~/.bashrc`):

```bash
export ANDROID_SDK_ROOT=~/android-sdk
export ANDROID_HOME=~/android-sdk
export ANDROID_NDK_ROOT=~/android-sdk/ndk-bundle
export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools
export PATH=$PATH:$ANDROID_SDK_ROOT/tools
export PATH=$PATH:$ANDROID_NDK_ROOT
```

You can also use these additional variables if you want to use `ccache` to speed up subsequent builds:

```bash
export USE_CCACHE=1
export NDK_CCACHE=/usr/local/bin/ccache
```

**Note:** Path to `ccache` can be different on your system.

### Android device setup

Enable [Developer options on your Android device](https://developer.android.com/studio/debug/dev-options). Connect your device to your PC via USB cable and run:

```bash
adb devices
adb connect <devicename>
```

### Building

To build an APK, use the Gradle wrapper command line tool (gradlew). The Android Studio documentation provides a good summary of how to [build your app from the command line](https://developer.android.com/studio/build/building-cmdline).

To build a debug APK, from the `android/` subfolder of the repository run:

    ./gradlew assembleDebug

This creates a debug APK in `./android/app/build/outputs/apk/` ready to be installed on your device.

To build a debug APK and immediately deploy to your connected device over adb run:

    ./gradlew installDebug

To build a signed release APK (ie. one that can be installed on a device), [build an unsigned release APK and sign it manually](https://developer.android.com/studio/publish/app-signing#signing-manually).

### Additional notes

The app stores data files on the device in `/sdcard/Android/data/com.cleverraven/cataclysmdda/files`. The data is backwards compatible with the desktop version.

# macOS

Most players should download a prebuilt `.dmg` from this fork's [Releases page](https://github.com/acererak-casts-disintegrate/Cataclysm-DDA/releases); the README explains how to open it the first time. Homebrew's `cataclysm` formula builds upstream Cataclysm: Dark Days Ahead, not this fork.

To build this fork you need the [Command Line Tools for Xcode](https://developer.apple.com/downloads/) (or Xcode itself) and the libraries described below.

## Building like the release packages

The release workflow ([`.github/workflows/release.yml`](../../.github/workflows/release.yml)) builds universal (`x86_64` and `arm64`) disk images on macOS 15 like this:

1. Put the SDL2, SDL2_image, SDL2_ttf and SDL2_mixer frameworks in `/Library/Frameworks` or `~/Library/Frameworks` (see [SDL](#sdl) below).
2. Install the other tools with [Homebrew](https://brew.sh): `brew install gettext dylibbundler`.
3. For the tiles build, install a universal FreeType with [MacPorts](https://www.macports.org): `sudo port install freetype +universal pkgconfig +universal`.
4. Install `dmgbuild` (see [dmg distribution](#dmg-distribution)).
5. Build and package:

       make -j$(sysctl -n hw.ncpu) RELEASE=1 TILES=1 SOUND=1 LOCALIZE=1 LANGUAGES=all BACKTRACE=0 PCH=0 USE_HOME_DIR=1 FRAMEWORK=1 UNIVERSAL_BINARY=1 dmgdist

   This leaves `Cataclysm.dmg` in the source folder. For the terminal-only build, use `TILES=0 SOUND=0`; it needs neither MacPorts nor FreeType. Leave out `UNIVERSAL_BINARY=1` to build for your own Mac's architecture only, and `dmgdist` to just build the game.

## Advanced info for Developers

For developers, here are some more technical details on building Cataclysm on macOS.

### SDL

SDL2, SDL2_image, and SDL2_ttf are needed for the tiles build. Optionally, you can add SDL2_mixer for sound support. Cataclysm can be built using either the SDL framework or shared libraries built from source.

The SDL framework files can be downloaded here:

* [**SDL2**](http://www.libsdl.org/download-2.0.php)
* [**SDL2_image**](http://www.libsdl.org/projects/SDL_image/)
* [**SDL2_ttf**](http://www.libsdl.org/projects/SDL_ttf/)

Copy `SDL2.framework`, `SDL2_image.framework`, and `SDL2_ttf.framework`
to `/Library/Frameworks` or `/Users/name/Library/Frameworks`.

If you want sound support, you will need an additional SDL framework:

* [**SDL2_mixer**](https://www.libsdl.org/projects/SDL_mixer/)

Copy `SDL2_mixer.framework` to `/Library/Frameworks` or `/Users/name/Library/Frameworks`.

Alternatively, SDL shared libraries can be installed using a package manager:

For Homebrew:

    brew install sdl2 sdl2_image sdl2_ttf

with sound:

    brew install sdl2_mixer libvorbis libogg

For MacPorts:

    sudo port install libsdl2 libsdl2_image libsdl2_ttf

with sound:

    sudo port install libsdl2_mixer libvorbis libogg

### ncurses and gettext

ncurses (with wide character support enabled) and gettext are needed if you want to build Cataclysm with localization.

For Homebrew:

    brew install gettext ncurses

For MacPorts:

```bash
sudo port install gettext ncurses
hash -r
```

### gcc

The Makefile uses Apple's clang on macOS, and that is what the release packages are built with. The `gcc` and `g++` that come with the Command Line Tools are clang under another name. Building with Homebrew's GCC (`CLANG=0` with `CXX` set to its `g++-NN`) is untested; CDDA needs GCC 9.3 or later (see [COMPILER_SUPPORT.md](COMPILER_SUPPORT.md)).

### Compiling

The Cataclysm source is compiled using `make`.

### Make options

* `NATIVE=osx` build for macOS. Required for all Mac builds. This is automatically set if compiling natively on macOS.
* `UNIVERSAL_BINARY=1` build `x86_64` and `arm64` dual-architecture Universal Binary; omit to build for host architecture only.
* `TILES=1` build the SDL version with graphical tiles (and graphical ASCII); omit to build with `ncurses`.
* `SOUND=1` - if you want sound; this requires `TILES=1` and the additional dependencies mentioned above.
* `FRAMEWORK=1` (tiles only) link to SDL libraries under the macOS Frameworks folders; omit to use SDL shared libraries from Homebrew or Macports.
* `LOCALIZE=0` disable localization (to get around possible `gettext` errors if it is not setup correctly); omit to use `gettext`.
* `LANGUAGES="<lang_id_1>[lang_id_2][...]"` compile localization files for specified languages. e.g. `LANGUAGES="zh_CN zh_TW"`. You can also use `LANGUAGES=all` to compile all localization files.
* `RELEASE=1` build an optimized release version; omit for debug build.
* `CLANG=1` build with [Clang](http://clang.llvm.org/), the compiler that's included with the latest Command Line Tools for Xcode; omit to build using gcc/g++. This is enabled by default.
* `MACPORTS=1` build against dependencies installed via Macports, currently only `gettext` and `ncurses`.
* `USE_HOME_DIR=1` places user files (config, saves, graveyard, etc) in the user's home directory. For curses builds, this is `/Users/<user>/.cataclysm-dda`, for tiles builds it is `/Users/<user>/Library/Application Support/Cataclysm`.
* `DEBUG_SYMBOLS=1` retains debug symbols when building an optimized release binary, making it easy for developers to spot the crash site.

In addition to the options above, there is an `app` make target which will package the tiles build into `Cataclysm.app`, a complete tiles build in a Mac application that can run without Terminal.

For more info, see the comments in the [Makefile](../../Makefile).

### Make examples

Build a release SDL version using Clang without gettext:

    make RELEASE=1 TILES=1 LOCALIZE=0

Build a release SDL version using Clang, link to libraries in the macOS Frameworks folders, don't use `gettext`, and package it into `Cataclysm.app`:

    make app RELEASE=1 TILES=1 FRAMEWORK=1 LOCALIZE=0

Build a release curses version with gettext supplied by Macports:

    make RELEASE=1 LOCALIZE=1 MACPORTS=1

### Running

For curses builds:

    ./cataclysm

For SDL:

    ./cataclysm-tiles

For `app` builds, launch Cataclysm.app from Finder.

### Test suite

The build will also generate a test executable at tests/cata_test.
Invoke it as you would any other executable and it will run the full suite of tests.
Pass the ``--help`` flag to list options.

### dmg distribution

You can build a dmg disk image with the `dmgdist` target. It needs [dmgbuild](https://pypi.org/project/dmgbuild/), plus [biplist](https://pypi.org/project/biplist/), which `build-data/osx/dmgsettings.py` imports. Current Homebrew Python refuses `pip install` into the system environment, so install them in their own environment with [pipx](https://pipx.pypa.io):

```bash
brew install pipx
pipx install dmgbuild
pipx inject dmgbuild biplist
```

Then build the image. `USE_HOME_DIR=1` matters here: it keeps the user's config and saves in their home folder, so the game can be upgraded by replacing the app.

    make dmgdist RELEASE=1 TILES=1 FRAMEWORK=1 USE_HOME_DIR=1

You should see a `Cataclysm.dmg` file. The image uses LZFSE compression, which macOS has read since 10.11.

## macOS Troubleshooting

### ISSUE: Colors don't show up correctly

Open Terminal's preferences, turn on "Use bright colors for bold text" in "Preferences -> Settings -> Text"


# Windows

## Building with Visual Studio

See [COMPILING-VS-VCPKG.md](COMPILING-VS-VCPKG.md) for instructions on how to set up and use a build environment using Visual Studio on windows.

This is probably the easiest solution for someone used to working with Visual Studio and similar IDEs.

For an alternative setup using [CMake](../../CMakeLists.txt), please read [COMPILING-CMAKE-VCPKG.md](COMPILING-CMAKE-VCPKG.md).

## Building with MSYS2

See [COMPILING-MSYS.md](COMPILING-MSYS.md) for instructions on how to set up and use a build environment using MSYS2 on windows.

MSYS2 strikes a balance between a native Windows application and a UNIX-like environment. There's some command-line tools that our project uses (notably our JSON linter) that are harder to use without a command-line environment such as what MSYS2 or CYGWIN provide.

## Building with CYGWIN

See [COMPILING-CYGWIN.md](COMPILING-CYGWIN.md) for instructions on how to set up and use a build environment using CYGWIN on windows.

CYGWIN attempts to more fully emulate a POSIX environment, to be "more unix" than MSYS2. It is a little less modern in some respects, and lacks the convenience of the MSYS2 package manager.

## Building with Clang and MinGW64

Clang by default uses MSVC on Windows, but also supports the MinGW64 library. Simply replace `CLANG=1` with `"CLANG=clang++ -target x86_64-pc-windows-gnu -pthread"` in your batch script, and make sure MinGW64 is in your path. You may also need to apply [a patch](https://sourceforge.net/p/mingw-w64/mailman/message/36386405/) to `float.h` of MinGW64 for the unit test to compile.

# BSDs

CI builds the game (tiles, sound and localization) and runs the core test suite on FreeBSD, OpenBSD and NetBSD for every push to `0.I-custom`; see [`.github/workflows/bsd.yml`](../../.github/workflows/bsd.yml). The recipes below are the ones it uses, on amd64. The Makefile recognises the BSDs by itself and uses each system's own compiler: clang on FreeBSD, OpenBSD and MidnightBSD, GCC on NetBSD and DragonFly BSD.

For a terminal-only build, leave out `TILES=1 SOUND=1` and the SDL packages. `LOCALIZE=0` removes the need for `gettext-tools`. Add `-jN` to build in parallel. CI builds with `BACKTRACE=0`; crash backtraces (the default) need `libexecinfo` and are untested on the BSDs.

## FreeBSD

Tested on FreeBSD 15.1 with the system clang:

    pkg install gmake pkgconf gettext-tools sdl2 sdl2_image sdl2_mixer sdl2_ttf
    gmake RELEASE=1 BACKTRACE=0 TILES=1 SOUND=1

## OpenBSD

Tested on OpenBSD 8.0 with the system clang:

    pkg_add gmake gettext-tools sdl2 sdl2-image sdl2-mixer sdl2-ttf
    gmake RELEASE=1 BACKTRACE=0 TILES=1 SOUND=1

You may get an out of memory error when compiling with an underprivileged user. You can fix this by running:

    usermod -L pbuild <user>

This sets the user's login class to `pbuild`, which raises the data size limit from 1GB to 8GB; it takes effect at the next login.

**Note:** don't run this command for your main user, as it is already part of the `staff` login class. Instead, increase the data limit with:

    ulimit -d 8000000

OpenBSD's C library ignores the numeric and collation locale settings, so the game sorts lists byte by byte there, and the tests that check localized sorting and number parsing skip themselves.

## NetBSD

Tested on NetBSD 11.0 with the system GCC and packages from pkgsrc:

    pkgin install gmake pkgconf gettext-tools SDL2 SDL2_image SDL2_mixer SDL2_ttf
    gmake RELEASE=1 BACKTRACE=0 TILES=1 SOUND=1

## Other systems

A weekly job, [`.github/workflows/other-os.yml`](../../.github/workflows/other-os.yml), also tries DragonFly BSD, MidnightBSD, Haiku and OmniOS (illumos), building the terminal-only version. These are experimental: that workflow lists the packages and flags each one uses, and its latest run shows whether it currently passes.

#!/bin/sh
# Regenerate lang/po/en_GB.po (British English) from the game's current text:
# rebuild the translation template, then convert it. Needs gettext and
# Python 3 with polib (pip install polib). See lang/en_GB/README.md.
set -e
cd "$(dirname "$0")/.."
lang/update_pot.sh
lang/en_GB/make_en_GB_po.py

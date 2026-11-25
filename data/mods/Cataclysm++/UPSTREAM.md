# Cataclysm++ in this fork

This folder holds Cataclysm++, imported from
[Noctifer-de-Mortem/nocts_cata_mod](https://github.com/Noctifer-de-Mortem/nocts_cata_mod),
folder `nocts_cata_mod_DDA`, at commit `46982a6` (9 November 2026).
Cataclysm++ is released into the public domain under The Unlicense.

Not imported: `mod_interactions/` (`doom`, `PK_REBALANCE`: mods that are not in this
repository), `lang/` (0.I does not load translations from `data/mods`) and `README_DDA.md`.

Git stores the files with LF line endings, so compare them with upstream using
`diff --strip-trailing-cr` or `git diff --ignore-cr-at-eol`.

The import is committed unmodified, followed by separate commits that adapt it to 0.I and to
this fork. To take a later upstream version, diff upstream from `46982a6` to the new commit
and apply that diff here, then update this file.

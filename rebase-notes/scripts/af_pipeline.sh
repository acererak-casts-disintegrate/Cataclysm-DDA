#!/bin/bash
# Rebuild data/mods/Aftershock in the 0.I worktree from 0.H-custom and convert it.
set -e
S=${S:?set S to the scratch directory holding the worktrees}
WT=$S/rebase; SRC=/home/user/Cataclysm-DDA/data/mods/Aftershock
cd $WT
rm -rf data/mods/Aftershock && cp -r $SRC data/mods/Aftershock
python3 $S/tools/convert_mod_0I.py data/mods/Aftershock > $S/conv_af.log
python3 $S/tools/af_fixes.py data/mods/Aftershock $S/af_0I > $S/fix_af.log
[ -x $S/tools/af_fixes2.sh ] && $S/tools/af_fixes2.sh
find data/mods/Aftershock -name '*.json' -print0 | xargs -0 -n1 tools/format/json_formatter.cgi > /dev/null 2>&1 || true
grep -v '^CHANGED' $S/conv_af.log | head -30; cat $S/fix_af.log | head -20

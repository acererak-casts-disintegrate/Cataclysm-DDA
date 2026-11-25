#!/bin/bash
# Trial-load an Arcana revision in the arc_wt worktree. Usage: aload.sh REF LABEL [MODS] [FILTER]
S=/tmp/claude-0/-home-user-Cataclysm-DDA/9a359a85-62c1-52fd-8ed1-3ef1a5c89d21/scratchpad
REF=$1; LABEL=$2; MODS=${3:-Arcana}; FILTER=${4:-item_new_to_hit_enforcement}
L=$S/aload_$LABEL.log
cd $S/arc_wt; rm -rf data/mods/Arcana data/cache $S/ud_a; mkdir -p $S/ud_a
git -C $S/ext/arcana archive "$REF" Arcana | tar -x -C data/mods
LANG=C.UTF-8 LC_ALL=C.UTF-8 timeout 3000 $S/rebase/tests/cata_test --user-dir $S/ud_a --drop-world --mods=$MODS "$FILTER" > $L 2>&1; rc=$?
echo "[$LABEL] exit $rc | ERROR lines $(grep -c ' ERROR ' $L) | Json errors $(grep -c '^Json error' $L)"; grep -E "test cases|All tests passed" $L | tail -1
grep -q "Fail to initialize" $L && { echo FATAL; grep -A6 "Fail to initialize" $L | head -8 | cut -c1-300; }

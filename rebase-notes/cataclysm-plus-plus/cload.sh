#!/bin/bash
# Trial load in the Cata++ scratch worktree. Usage: cload.sh MODS [filter] [log]
S=${S:?set S to the scratch directory}
L=${3:-$S/cload.log}
cd $S/cpp_wt; rm -rf data/cache $S/ud_c; mkdir -p $S/ud_c
LANG=C.UTF-8 LC_ALL=C.UTF-8 timeout 3000 $S/rebase/tests/cata_test --user-dir $S/ud_c --drop-world --mods=$1 "${2:-item_new_to_hit_enforcement}" > $L 2>&1; rc=$?
echo "exit $rc | errors $(grep -c ' ERROR ' $L)"; grep -E "test cases|All tests passed" $L | tail -1
grep -q "Fail to initialize" $L && { echo FATAL; grep -A6 "Fail to initialize" $L | head -8 | cut -c1-300; }

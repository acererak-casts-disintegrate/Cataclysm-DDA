#!/bin/bash
# Load check on the port worktree. Usage: pload.sh [filter] ; MODS env optional
S=${S:?set S to the scratch directory holding the worktrees}
cd $S/rebase; rm -rf data/cache $S/ud_p; mkdir -p $S/ud_p
LANG=C.UTF-8 LC_ALL=C.UTF-8 timeout 3000 ./tests/cata_test --user-dir $S/ud_p --drop-world ${MODS:+--mods=$MODS} "${1:-[purifier]}" > $S/pload.log 2>&1; rc=$?
echo "exit $rc | errors $(grep -c ' ERROR ' $S/pload.log)"; grep -E "test cases|All tests passed" $S/pload.log
grep -q "Fail to initialize" $S/pload.log && { echo FATAL; grep -A4 "Fail to initialize" $S/pload.log | head -6 | cut -c1-240; }
grep -E " ERROR |^Json error" $S/pload.log | sed -E 's/^[0-9:.]+ ERROR : //' | cut -c1-230 | sort | uniq -c | sort -rn | head -${N:-15}

#!/bin/bash
# CI-equivalent Arcana run in arc_wt (whatever Arcana copy is installed there). Usage: arc_suite.sh LABEL
S=/tmp/claude-0/-home-user-Cataclysm-DDA/9a359a85-62c1-52fd-8ed1-3ef1a5c89d21/scratchpad; L=$1
cd $S/arc_wt; rm -rf data/cache modded_1 modded_2 all_modded
export LANG=C.UTF-8 LC_ALL=C.UTF-8
O="--min-duration 20 --rng-seed time --order lex"
B=$S/rebase/tests/cata_test
$B $O --mods=Arcana --user-dir=modded_1 "[slow] ~starting_items" > $S/arc_${L}_slow.log 2>&1 & p1=$!
$B $O --mods=Arcana --user-dir=modded_2 "~[slow] ~[.],starting_items" > $S/arc_${L}_fast.log 2>&1 & p2=$!
wait $p1; r1=$?; wait $p2; r2=$?
echo "slow rc=$r1 | $(grep -E 'test cases' $S/arc_${L}_slow.log | tail -1)"
echo "fast rc=$r2 | $(grep -E 'test cases' $S/arc_${L}_fast.log | tail -1)"
: > $S/arc_${L}_allmods.log; ra=0
while read -r mods; do
  $B $O '[force_load_game]' --user-dir=all_modded --mods="$mods" >> $S/arc_${L}_allmods.log 2>&1 || { ra=1; echo "all-mods FAIL: $mods"; }
done < <(./build-scripts/get_all_mods.py)
echo "all-mods rc=$ra | errors $(grep -c ' ERROR ' $S/arc_${L}_allmods.log)"

#!/bin/bash
# Replay the fork's commits onto another branch, recording conflicts.
#
# Each commit is applied twice: once plainly, to record its real conflicts,
# then again with conflicting hunks resolved in the fork's favour (-X theirs)
# so that later commits have something to apply to. The second pass is a
# rough stand-in for hand merging: it can reinsert syntax the target branch
# no longer accepts.
#
# Usage (run anywhere):
#   REPO=/path/to/fork-checkout WT=/path/to/worktree-on-target \
#   SKIP="23 24 25 26 34" OUT=/path/to/output ./replay.sh
# Optional: BASE (fork's upstream base, default 08f04fd07), TIP (default 0.H-custom).
set -u
: "${REPO:?}" "${WT:?}" "${OUT:?}"
BASE=${BASE:-08f04fd07}; TIP=${TIP:-0.H-custom}; SKIP=${SKIP:-}
cd "$WT" || exit 1
rm -rf "$OUT"; mkdir -p "$OUT"
git -C "$REPO" log --format=%H --reverse "$BASE..$TIP" > "$OUT/commits.txt"
i=0
while read -r c; do
  i=$((i+1)); subj=$(git log -1 --format=%s "$c")
  if echo " $SKIP " | grep -q " $i "; then
    printf "%02d\t%s\tSKIPPED\t%s\n" $i "${c:0:10}" "$subj" >> "$OUT/summary.tsv"; continue
  fi
  nfiles=$(git diff --name-only "$c^" "$c" | wc -l)
  git cherry-pick --no-commit "$c" > "$OUT/$i.pass1.log" 2>&1
  git status --porcelain | grep -E '^(UU|AA|DU|UD|AU|UA|DD) ' > "$OUT/$i.conflicts.txt"
  hunks=0
  for f in $(grep '^UU ' "$OUT/$i.conflicts.txt" | cut -c4-); do
    n=$(grep -c '^<<<<<<< ' "$f" 2>/dev/null); hunks=$((hunks+n))
  done
  uu=$(grep -c '^UU ' "$OUT/$i.conflicts.txt"); aa=$(grep -c '^AA ' "$OUT/$i.conflicts.txt")
  du=$(grep -c '^DU ' "$OUT/$i.conflicts.txt"); ud=$(grep -c '^UD ' "$OUT/$i.conflicts.txt")
  other=$(grep -cE '^(AU|UA|DD) ' "$OUT/$i.conflicts.txt")
  git cherry-pick --abort >/dev/null 2>&1; git reset -q --hard HEAD; git clean -qfd
  git cherry-pick --no-commit -X theirs "$c" > "$OUT/$i.pass2.log" 2>&1
  while read -r st f; do
    case "$st" in
      DU) git rm -q --cached "$f" 2>/dev/null; rm -f "$f"; echo "$f" >> "$OUT/$i.lost.txt" ;;  # fork edit, file gone on target
      UD|DD) git rm -q "$f" 2>/dev/null || git rm -q --cached "$f" ;;                       # fork deletes it
      AA|UA|AU|UU) git checkout --theirs -- "$f" 2>/dev/null && git add "$f" ;;
    esac
  done < <(git status --porcelain | grep -E '^(UU|AA|DU|UD|AU|UA|DD) ')
  if git diff --cached --quiet; then status=EMPTY; git reset -q --hard HEAD
  else git commit -q -C "$c" --no-verify && status=APPLIED || status=FAILED; fi
  printf "%02d\t%s\t%s\tfiles=%d\tUU=%d(hunks=%d)\tAA=%d\tDU=%d\tUD=%d\tother=%d\t%s\n" \
    $i "${c:0:10}" $status $nfiles $uu $hunks $aa $du $ud $other "$subj" >> "$OUT/summary.tsv"
done < "$OUT/commits.txt"

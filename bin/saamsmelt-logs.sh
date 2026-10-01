#!/bin/sh
# Merge origin/main, resolving the two append-only JSONL logs by keeping every
# line from both sides. Those two files conflict on every parallel push and the
# resolution is always the same, so it does not need a person.
set -e
git fetch -q origin main
git merge origin/main --no-edit >/dev/null 2>&1 || true
konflik=$(git diff --name-only --diff-filter=U)
if [ -n "$konflik" ]; then
  ander=$(echo "$konflik" | grep -v '^logs/.*\.jsonl$' || true)
  if [ -n "$ander" ]; then
    echo "STOP: conflicts outside the append-only logs, a person must look:"
    echo "$ander"
    exit 1
  fi
  python bin/saamsmelt_logs.py $konflik
  git add $konflik
  git commit -q --no-edit
fi
git push -q origin main
git log --oneline -1

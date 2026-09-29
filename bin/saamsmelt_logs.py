# -*- coding: utf-8 -*-
"""Resolve a conflict in an append-only JSONL log by keeping every line from both
sides, in first-seen order, dropping exact duplicates and anything unparseable."""
import io, json, sys, subprocess, collections

for pad in sys.argv[1:]:
    kante = []
    for stage in (2, 3):
        kante += subprocess.check_output(
            ["git", "show", ":%d:%s" % (stage, pad)]).decode("utf-8").splitlines()
    gesien, sleg = collections.OrderedDict(), 0
    for lyn in kante:
        lyn = lyn.strip()
        if not lyn:
            continue
        try:
            json.loads(lyn)
        except ValueError:
            sleg += 1
            continue
        gesien.setdefault(lyn, None)
    io.open(pad, "w", encoding="utf-8", newline="\n").write("\n".join(gesien) + "\n")
    print("  %-26s %d lines kept%s" % (pad, len(gesien),
          ", %d unparseable dropped" % sleg if sleg else ""))

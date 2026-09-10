#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Move a draft's older provenance rounds out to a file beside the lesson.

The failure this exists for, found on 10 September 2026:

A writer records its reasoning in the draft's provenance note, and every
revision APPENDS to it. That is right -- it is how a decision survives to the
next revision, and several corrections have been saved by it. But the note
grows without limit, and it grows FASTEST on the lessons that get revised
most, which are exactly the lessons most likely to need revising again.

Grade 5 dieregeraamtes lesson 1 reached 55 KB in a single JSON string -- more
than a reading tool returns in one call, and nine tenths of the file. A writer
sent to make three one-line corrections could read every study block and every
glossary entry, and could not read that one line at all. Its only writing tool
replaces a whole file, so the only way to append three sentences was to rewrite
the lesson from what it could see, silently deleting the entire accumulated
record. It refused, correctly, and reported instead.

So the note has already stopped doing its job before anything blocks: nobody --
writer, moderator or later reviser -- can read 55 KB on one line.

This splits it. The archive is written FIRST and verified to contain the whole
original before the draft is touched, so a crash between the two steps costs
nothing. What stays in the draft:

  * the opening paragraph, always -- it is the copyright record ("no textbook
    was seen"), and that must travel with the lesson rather than sit in a
    sibling file;
  * a pointer to the archive;
  * the most recent rounds, up to --hou characters.

    python bin/herkomsargief.py --vak "<subject>" --graad 5          # report
    python bin/herkomsargief.py --vak "<subject>" --graad 5 --skryf  # do it
"""
import argparse
import glob
import io
import json
import os
import re
import sys

SEP = chr(92)

# Below this, a note is readable and is left completely alone.
DREMPEL = 18000

# How much of the tail stays in the draft. Two or three rounds, in practice.
HOU = 6000

WYSER = ("\n\n[HERKOMS-ARGIEF. Die ouer rondes van hierdie nota staan woordeliks in %s, "
         "langs die les. Niks is weggegooi nie. Die nota is geskuif omdat sy %d karakters "
         "op een reel bereik het en toe nie meer deur 'n skrywer gelees kon word nie - "
         "'n rekord wat niemand kan oopmaak nie, doen reeds nie meer sy werk nie. "
         "Lees die argief voordat jy iets in hierdie les heroorweeg.]\n\n")


# A section heading inside a note is SHOUTED. When a note has no blank lines at
# all -- and four of the biggest have none -- this is the only boundary it has.
# It matches only after a full stop, so a split never cuts a sentence in half.
KOP = re.compile(r"(?<=\.)\s+(?=[A-Z][A-Z'ÉËÓÖ]{4,})")


def paragrawe(n):
    """Blank lines first, because they are unambiguous. Where a note has none, fall
    back to the shouted section headings -- the note is one line and the headings
    are the structure a reader would use anyway."""
    dele = [p for p in n.split("\n\n") if p.strip()]
    if len(dele) >= 3:
        return dele
    dele = [p for p in KOP.split(n) if p.strip()]
    return dele


def verwerk(pad, hou, drempel, skryf):
    with io.open(pad, encoding="utf-8") as f:
        d = json.load(f)
    nota = (d.get("herkoms") or {}).get("nota")
    if not isinstance(nota, str) or len(nota) <= drempel:
        return None

    argief = pad[:-len(".json")] + ".herkoms.md"
    dele = paragrawe(nota)
    if len(dele) < 3:
        # One giant paragraph. Splitting it would cut a sentence in half, and a
        # note cut mid-sentence is worse than a note that is merely long.
        return (pad, len(nota), 0, "single paragraph -- nothing to split on")

    eerste = dele[0]
    stert, lengte = [], 0
    for p in reversed(dele[1:]):
        if lengte + len(p) > hou and stert:
            break
        stert.insert(0, p)
        lengte += len(p) + 2

    geskuif = len(dele) - 1 - len(stert)
    if geskuif <= 0:
        return (pad, len(nota), 0, "the tail alone already fits -- nothing to move")

    nuut = eerste + (WYSER % (os.path.basename(argief), len(nota))) + "\n\n".join(stert)
    if not skryf:
        return (pad, len(nota), geskuif, "%d -> %d chars" % (len(nota), len(nuut)))

    # The archive is written and verified BEFORE the draft loses anything.
    with io.open(argief, "w", encoding="utf-8") as f:
        f.write("# Herkoms-nota, volledig\n\n"
                "Hierdie leer dra die HELE nota soos sy op %s gestaan het, woordeliks.\n"
                "Die les self hou die openingsparagraaf en die jongste rondes.\n\n---\n\n"
                % "10 September 2026")
        f.write(nota)
        f.write("\n")
    with io.open(argief, encoding="utf-8") as f:
        terug = f.read()
    if nota not in terug:
        sys.exit("ABORTED: %s does not contain the note verbatim. The draft was not touched."
                 % argief)

    d["herkoms"]["nota"] = nuut
    with io.open(pad, "w", encoding="utf-8") as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    return (pad, len(nota), geskuif, "%d -> %d chars, archive %s" % (len(nota), len(nuut), os.path.basename(argief)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--vak")
    p.add_argument("--graad", type=int)
    p.add_argument("--les", help="one lesson path, instead of --vak/--graad")
    p.add_argument("--hou", type=int, default=HOU)
    p.add_argument("--drempel", type=int, default=DREMPEL)
    p.add_argument("--skryf", action="store_true", help="do it; otherwise report only")
    a = p.parse_args()

    if a.les:
        paaie = [a.les]
    else:
        if not (a.vak and a.graad):
            sys.exit("Give --les, or both --vak and --graad.")
        vakgids = a.vak.lower().replace(" ", "-")
        paaie = sorted(glob.glob(os.path.join(
            "konsepte", "gr%d" % a.graad, vakgids, "*", "les-?.json")))
        paaie = [q for q in paaie if os.path.basename(q).count(".") == 1
                 and "feite-kopie" not in q.replace(SEP, "/")]
    if not paaie:
        sys.exit("No drafts found.")

    print("%d draft(s) read, threshold %d chars, keeping the last %d\n" % (len(paaie), a.drempel, a.hou))
    raak = 0
    for q in paaie:
        r = verwerk(q, a.hou, a.drempel, a.skryf)
        if r:
            raak += 1
            print("  %-46s %s" % ("/".join(r[0].replace(SEP, "/").split("/")[-2:]), r[3]))
    if not raak:
        print("  every note is under the threshold")
    elif not a.skryf:
        print("\nNothing was written. Re-run with --skryf.")


if __name__ == "__main__":
    main()

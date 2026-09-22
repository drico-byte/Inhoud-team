#!/usr/bin/env python3
"""Regenerate the fact checker's copy of one or more drafts.

WHY THIS EXISTS. The copy handed to the fact checker — the draft with the
writer's provenance note removed — was written in only one place: inside
`hardloop.py`, as a side effect of the runner naming the fact-check step. That
is correct when every check is launched by the runner.

It is wrong the moment a check is briefed by hand, which is what happens during
a repair cycle: `hardloop.py` archives finished reports and demands the checks
again, so a second pass over already-checked lessons is briefed directly. The
copy then never moves. On 19 September 2026 thirty of thirty-two Grade 5
Lewensvaardighede copies were older than their drafts, and fact checkers spent a
full round reporting faults that had already been repaired — two of the three
findings on one lesson were its own corrections, read back from a stale copy.

A stale copy fails silently and expensively in both directions: it invents
findings that are already fixed, and it gives a clean verdict to text nobody
checked. Run this before briefing a fact checker outside the runner.

    python bin/feitekopie.py konsepte/gr5/.../les-4.json
    python bin/feitekopie.py --alles konsepte/gr5/lewensvaardighede

With --alles it walks the tree, skips report files, and reports which copies
were behind their draft, because that count is the thing worth seeing.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paaie as P

VERSLAGSTERTE = (".dekking.json", ".feite.json", ".hek.json", ".staat.json")


def is_konsep(naam):
    return naam.startswith("les-") and naam.endswith(".json") and not any(
        naam.endswith(stert) for stert in VERSLAGSTERTE
    )


def versamel(wortel):
    for gids, subgidse, lêers in os.walk(wortel):
        # the copies themselves are not drafts
        subgidse[:] = [s for s in subgidse if s not in ("feite-kopie", "spek")]
        for naam in sorted(lêers):
            if is_konsep(naam):
                yield os.path.join(gids, naam)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paaie", nargs="+", help="draft files, or a directory with --alles")
    p.add_argument("--alles", action="store_true",
                   help="treat each path as a directory and walk it")
    args = p.parse_args()

    lesse = []
    for pad in args.paaie:
        if args.alles:
            lesse.extend(versamel(pad))
        else:
            lesse.append(pad)

    verouderd = 0
    for les_pad in lesse:
        les_pad = os.path.abspath(les_pad)
        kopie = os.path.join(os.path.dirname(les_pad), "feite-kopie",
                             os.path.basename(les_pad))
        was_agter = (not os.path.exists(kopie)
                     or os.path.getmtime(kopie) < os.path.getmtime(les_pad))
        nuwe = P.skryf_feitekopie(les_pad)
        if was_agter:
            verouderd += 1
            print(f"  verouderd, nou vernuwe: {P.rel(nuwe)}")

    print(f"\n{len(lesse)} kopie(e) geskryf, waarvan {verouderd} agter die konsep was.")
    if verouderd:
        print("Enige feitetoets wat op een van daardie kopieë gebaseer is, moet oorgedoen word.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

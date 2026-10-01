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

"BEHIND" IS A QUESTION ABOUT CONTENT, NOT ABOUT MODIFICATION TIME. 1 October
2026: this script used to compare mtimes, which reports a copy stale whenever the
draft was touched -- and a revision that only appends to the writer's provenance
note changes nothing a fact checker can see, because the note is exactly what the
copy withholds. Measured over this repository's history, 46 of 1283 draft
modifications left the stripped copy byte-identical; every one of those would be
announced as behind.

That is the cry-wolf half of a failure this repository has already paid for: a
guard that kept its own copy of the rules reported three files stale for ever and
was blind to thirty that genuinely were. CLAUDE.md tells whoever runs the pipeline
to QUOTE the number this script prints, so the number has to mean something. A run
that reports none is what makes the checks after it worth having.

So the test asks the only question that matters -- is the copy on disk what the
copier would write now? -- by comparing against P.feitekopie_inhoud, the single
shared definition of what a copy contains. There is deliberately no second list
here of the fields a copy withholds. That second list IS the fault; see
P.feitekopie_inhoud for what one cost.
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


def is_agter(les_pad):
    """Is the copy on disk something other than what the copier would write now?

    Returns (behind, reason). Content, never mtime -- see the module docstring.

    The comparison is against P.feitekopie_inhoud and nothing else, so the fields
    a copy withholds are named in exactly one place in this repository. Note that
    this makes a note-only revision correctly "current", which is the point, and
    also makes a revision that ADDS a note field "behind" -- the withheld-field
    marker carries a count, so the copy genuinely changes. That is still the right
    answer to the question actually being asked.

    Missing or unreadable counts as behind. A copy that cannot be read is
    certainly not the copy a checker should be briefed on, and the safe direction
    here is to over-report: a false "behind" costs a rewrite that was going to
    happen anyway, while a false "current" hands a fact checker text nobody wrote
    and it returns a clean verdict on it. That is the 19 September 2026 failure,
    thirty of thirty-two copies behind and a whole round of checks thrown away.
    """
    kopie = P.feitekopie(les_pad)
    if not os.path.exists(kopie):
        return True, "daar was nog geen kopie nie"
    try:
        oud = P.lees_json(kopie)
    except (OSError, ValueError) as e:
        return True, "die kopie was onleesbaar (%s)" % e
    if oud == P.feitekopie_inhoud(P.lees_json(les_pad)):
        return False, ""
    return True, "die inhoud stem nie met die konsep ooreen nie"


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
        # Ask before writing: skryf_feitekopie is what makes the copy current.
        was_agter, rede = is_agter(les_pad)
        nuwe = P.skryf_feitekopie(les_pad)
        if was_agter:
            verouderd += 1
            print(f"  verouderd, nou vernuwe: {P.rel(nuwe)}  ({rede})")

    print(f"\n{len(lesse)} kopie(e) geskryf, waarvan {verouderd} agter die konsep was.")
    if verouderd:
        print("Enige feitetoets wat op een van daardie kopieë gebaseer is, moet oorgedoen word.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

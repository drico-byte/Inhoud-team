#!/usr/bin/env python3
"""
Rewrite every per-lesson spec extract from the approved specs.

`hardloop.py` writes the extract a writer and a coverage checker read -- but only
when it runs for that lesson. So editing a spec and briefing an agent straight
afterwards hands it the OLD copy, and the agent then reports, correctly, that the
fix is not in the spec. That has now happened twice in one afternoon, the second
time an hour after the first was written down, which is what a habit that needs
remembering is worth.

This does the one safe part of a runner call and nothing else: no gate, no
staleness, no archiving, no state. Run it after editing a spec and before
briefing anyone.

    python bin/vernuwe-uittreksels.py                 # all of them
    python bin/vernuwe-uittreksels.py --vak "Natuurwetenskappe en Tegnologie" --graad 4
    python bin/vernuwe-uittreksels.py --wat-sou-verander      # dry run

Only lessons that already have an extract are rewritten. A lesson nobody has
started has nothing to go stale, and writing one early would put a spec entry on
disk for a draft that does not exist.
"""

import argparse
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)
sys.path.insert(0, HIER)

import paaie as P                                          # noqa: E402
from hardloop import met_spek_konteks                      # noqa: E402


def spesifikasies(graad=None, vak=None):
    wortel = P.SPEK_GOEDGEKEUR
    for gids, _, lers in os.walk(wortel):
        for naam in sorted(lers):
            if not naam.endswith(".json") or naam.endswith(".feite.json"):
                continue
            pad = os.path.join(gids, naam)
            try:
                spek = P.lees_json(pad)
            except (OSError, ValueError) as e:
                print(f"  kon nie lees nie: {P.rel(pad)} ({e})", file=sys.stderr)
                continue
            if graad and int(spek.get("graad", 0)) != graad:
                continue
            if vak and P.slug(spek.get("vak", "")) != P.slug(vak):
                continue
            yield pad, spek


def main():
    ap = argparse.ArgumentParser(
        description="Rewrite per-lesson spec extracts from the approved specs")
    ap.add_argument("--vak")
    ap.add_argument("--graad", type=int)
    ap.add_argument("--wat-sou-verander", action="store_true", dest="droog",
                    help="say what would change and write nothing")
    a = ap.parse_args()

    geskryf = ongeraak = 0
    for spek_pad, spek in spesifikasies(a.graad, a.vak):
        vak = spek.get("vak")
        graad = int(spek["graad"])
        sub = spek.get("kaps_subonderwerp")
        for les in spek.get("lesse", []):
            nommer = les.get("nommer")
            if not nommer:
                continue
            uit_pad = P.spek_inskrywing(graad, vak, sub, nommer)
            if not os.path.exists(uit_pad):
                continue                      # nobody has started this lesson
            nuut = met_spek_konteks(spek, les)
            try:
                oud = P.lees_json(uit_pad)
            except (OSError, ValueError):
                oud = None
            if oud == nuut:
                ongeraak += 1
                continue
            print(f"  {'sou verander' if a.droog else 'vernuwe'}: {P.rel(uit_pad)}")
            if not a.droog:
                P.skryf_json(uit_pad, nuut)
            geskryf += 1

    if a.droog:
        print(f"\n{geskryf} uittreksel(s) is verouderd, {ongeraak} is reeds gelyk.")
        return 1 if geskryf else 0
    print(f"\n{geskryf} vernuwe, {ongeraak} was reeds gelyk.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

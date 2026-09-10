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
import hashlib
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)
sys.path.insert(0, HIER)

import paaie as P                                          # noqa: E402

# Key carrying the fingerprint of what this script last wrote.
STEMPEL = "_afgelei_stempel"
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



def _sonder_stempel(doc):
    return {k: v for k, v in doc.items() if k != STEMPEL} if isinstance(doc, dict) else doc


def stempel_van(doc):
    """Fingerprint of an extract's derived content, ignoring the stamp itself."""
    blob = json.dumps(_sonder_stempel(doc), ensure_ascii=False, sort_keys=True)
    return "sha256:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()[:32]


def is_met_die_hand_verander(oud):
    """True when the extract on disk no longer matches the stamp it was written with.

    An extract is DERIVED, never authored. So the only honest way to tell a hand
    edit from an ordinary source change is to ask whether the file still matches
    what this script last wrote -- comparing its text against the newly derived
    version cannot do it, because an edited source field looks exactly like an
    edited extract field. The first version of this check did that and fired on
    every normal spec edit, which would have trained everyone to ignore it.

    A writer wrote two corrections straight into an extract on 11 September 2026.
    They would have been erased by the next refresh without a trace; they were
    caught only because someone read the agent's report closely.
    """
    if not isinstance(oud, dict):
        return False
    gestempel = oud.get(STEMPEL)
    if not gestempel:
        return False                      # written before stamping existed
    return gestempel != stempel_van(oud)


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
            # Compare WITHOUT the stamp. The stamp is not derived content, so a
            # stamped file could never equal a freshly derived one, and every run
            # would rewrite every extract for ever - each rewrite also destroying
            # the evidence that the previous one was hand-edited.
            if _sonder_stempel(oud) == nuut:
                ongeraak += 1
                continue
            handgeskryf = is_met_die_hand_verander(oud)
            print(f"  {'sou verander' if a.droog else 'vernuwe'}: {P.rel(uit_pad)}")
            if handgeskryf:
                print("     LET OP: hierdie uittreksel stem nie meer ooreen met wat hierdie skrip "
                      "laas geskryf het nie - iemand het DIREK in die uittreksel geskryf.")
                if not a.droog:
                    kopie = uit_pad[:-len('.json')] + '.verlore.json'
                    P.skryf_json(kopie, _sonder_stempel(oud))
                    print(f"     Die hele ou uittreksel is gestoor: {P.rel(kopie)}")
                    print("     Dra die verandering oor na die SPEK, nie terug na die uittreksel nie, "
                          "en vee die kopie dan uit.")
            if not a.droog:
                nuut = dict(nuut)
                nuut[STEMPEL] = stempel_van(nuut)
                P.skryf_json(uit_pad, nuut)
            geskryf += 1

    if a.droog:
        print(f"\n{geskryf} uittreksel(s) is verouderd, {ongeraak} is reeds gelyk.")
        return 1 if geskryf else 0
    print(f"\n{geskryf} vernuwe, {ongeraak} was reeds gelyk.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

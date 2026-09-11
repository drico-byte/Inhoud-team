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

IT ALSO REFRESHES THE FACT CHECKER'S COPY, for the same reason and after the same
kind of failure. `feite-kopie/<lesson>.json` -- the draft with its provenance note
stripped -- is written only by a runner call too. A fact checker dispatched without
one reads whatever copy happens to be on disk, and that copy is gitignored, so
nothing shows that it is old.

It cost a whole fact check on 11 September 2026. The copy of Grade 5
`gestoorde-energie-in-brandstof` lesson 2 was written at 15:03 on 10 September, the
lesson itself changed twice later that day, and the check ran the next morning
against the eighteen-hour-old copy. Two of its four findings were about glossary
entries that had already been corrected. The writer caught it, read both entries
against the agreed list, and refused to write a third wording.

A stale DRAFT is worse than a stale spec extract. An agent reading an old spec
reports that a fix is missing, which is visibly wrong and gets checked. An agent
reading an old draft reports faults that no longer exist, and those read exactly
like real findings.
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


def _inhoud(doc):
    """Compare on lesson content only. The withheld-note marker is boilerplate the
    copier writes itself, so it must never make two copies look different -- that
    would report every copy stale on every run and train everyone to ignore it."""
    if not isinstance(doc, dict):
        return doc
    return {k: v for k, v in doc.items() if k != "herkoms"}


def vernuwe_feitekopiee(graad=None, vak=None, droog=False):
    """Rewrite every fact checker's copy that no longer matches its draft.

    Only copies that ALREADY EXIST are touched, on the same principle as the spec
    extracts: a lesson nobody has fact-checked has nothing to go stale.
    """
    aantal = verouderd = 0
    for gids, _, lers in os.walk(os.path.join(REPO, "konsepte")):
        if os.path.basename(gids) != "feite-kopie":
            continue
        for naam in sorted(lers):
            if not naam.endswith(".json"):
                continue
            kopie_pad = os.path.join(gids, naam)
            les_pad = os.path.join(os.path.dirname(gids), naam)
            if not os.path.exists(les_pad):
                print("  WEESKIND: %s het geen konsep langs hom nie" % P.rel(kopie_pad),
                      file=sys.stderr)
                continue
            try:
                les = P.lees_json(les_pad)
                oud = P.lees_json(kopie_pad)
            except (OSError, ValueError):
                continue
            if graad and int(les.get("graad", 0)) != graad:
                continue
            if vak and P.slug(les.get("vak", "")) != P.slug(vak):
                continue
            aantal += 1
            if _inhoud(oud) == _inhoud(les):
                continue
            verouderd += 1
            print("  %s feitekopie: %s" % ("sou vernuwe" if droog else "vernuwe",
                                           P.rel(kopie_pad)))
            if not droog:
                P.skryf_feitekopie(les_pad)
    return aantal, verouderd


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

    kopiee, verouderd = vernuwe_feitekopiee(a.graad, a.vak, a.droog)

    if a.droog:
        print(f"\n{geskryf} uittreksel(s) is verouderd, {ongeraak} is reeds gelyk.")
        print(f"{verouderd} van {kopiee} feitekopie(e) is verouderd.")
        return 1 if (geskryf or verouderd) else 0
    print(f"\n{geskryf} vernuwe, {ongeraak} was reeds gelyk.")
    print(f"{verouderd} van {kopiee} feitekopie(e) herskryf.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

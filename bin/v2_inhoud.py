#!/usr/bin/env python3
"""File every lesson re-signed in the Grade 4-6 language pass into 'V2 inhoud', and
write the list of what changed in each and why.

Lampies, 22 October 2026: the in-pipeline language step runs over every signed-off
Grade 4-6 lesson, and the CAPS audit's gaps are filled in the same pass. Every
lesson that comes through it is delivered again, to its own folder, laid out like
'Voltooide lesse':

    V2 inhoud/Graad 4/Lewensvaardighede/Ontwikkeling van self/Les 03 - <titel>.pdf

A lesson belongs here once it is approved AND its language step ran after the step
shipped (a `taal` event in its state after TAALSTAP_SEDERT) AND it was signed off
after that. A lesson whose language step changed nothing is listed too: it was read
and kept, which is a result.

The CAPS gaps filled in a lesson cannot be read off the lesson, so they are recorded
by hand in 'V2 inhoud/gapings.json' ({"<lesson path>": ["what was added and why"]}),
and this script merges them into the list.

    python bin/v2_inhoud.py              # every Grade 4-6 lesson that qualifies
"""

import glob
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402
import voltooide_lesse as V  # noqa: E402
from hardloop import TAALSTAP_SEDERT  # noqa: E402

V2 = os.path.join(P.REPO, "V2 inhoud")
GAPINGS = os.path.join(V2, "gapings.json")
LYS = os.path.join(V2, "Veranderinge.md")


def doel_pad(les, pad):
    return os.path.join(V2, os.path.relpath(V.doel_pad(les, pad), V.VOLTOOI))


def stand(pad):
    """(qualifies, date signed, language report) for one lesson."""
    les = P.lees_json(pad)
    if les.get("status") != "goedgekeur":
        return False, None, None
    staat_pad = P.staat_pad(pad)
    if not os.path.exists(staat_pad):
        return False, None, None
    ges = P.lees_json(staat_pad).get("geskiedenis") or []
    taal = [e.get("wanneer") for e in ges
            if e.get("gebeurtenis") == "taal" and (e.get("wanneer") or "") >= TAALSTAP_SEDERT]
    if not taal:
        return False, None, None
    goed = [e.get("wanneer") for e in ges
            if e.get("gebeurtenis") == "goedgekeur" and (e.get("wanneer") or "") >= max(taal)]
    if not goed:
        return False, None, None
    verslag = P.lees_json(P.taal_verslag(pad)) if os.path.exists(P.taal_verslag(pad)) else {}
    return True, max(goed)[:10], verslag


def main():
    gapings = P.lees_json(GAPINGS) if os.path.exists(GAPINGS) else {}
    rye, sonder_pdf = [], []
    for pad in sorted(glob.glob(os.path.join(P.KONSEPTE, "gr[456]", "*", "*", "les-*.json"))):
        if not P.is_les_konsep(pad):
            continue
        ok, datum, verslag = stand(pad)
        if not ok:
            continue
        les = P.lees_json(pad)
        bron = pad[:-len(".json")] + ".pdf"
        doel = doel_pad(les, pad)
        if not os.path.exists(bron):
            sonder_pdf.append(pad)
            continue
        os.makedirs(os.path.dirname(doel), exist_ok=True)
        gids, naam = os.path.split(doel)
        for ou in glob.glob(os.path.join(gids, naam.split(" - ")[0] + "*.pdf")):
            if os.path.abspath(ou) != os.path.abspath(doel):
                os.remove(ou)
        shutil.copy2(bron, doel)
        rel = os.path.relpath(pad, P.REPO).replace(os.sep, "/")
        rye.append((os.path.relpath(doel, V2).replace(os.sep, "/"), rel, datum,
                    len(verslag.get("toegepas") or []), gapings.get(rel) or []))

    reëls = ["# V2 inhoud: wat verander het en hoekom", "",
             "Elke les hier het deur ons eie taalstap gegaan (vinder, keurder, die hek "
             "weer, dan die dekking- en feitetoets) en is weer goedgekeur. Waar die "
             "KABV-oudit 'n gaping gevind het, is dit in dieselfde rondte gevul.", "",
             f"{len(rye)} lesse.", ""]
    vorige = None
    for doel, rel, datum, n, gaps in rye:
        groep = os.path.dirname(doel)
        if groep != vorige:
            reëls += ["", f"## {groep}", ""]
            vorige = groep
        wat = [f"{n} taalverandering(s) toegepas" if n else "taalstap: niks verander nie"]
        wat += [f"KABV-gaping: {g}" for g in gaps]
        reëls.append(f"- **{os.path.basename(doel)[:-4]}** (goedgekeur {datum}): " + "; ".join(wat))
    os.makedirs(V2, exist_ok=True)
    with open(LYS, "w", encoding="utf-8") as fh:
        fh.write("\n".join(reëls) + "\n")

    print(f"{len(rye)} lesse in '{os.path.relpath(V2, P.REPO)}', lys: {os.path.relpath(LYS, P.REPO)}")
    if sonder_pdf:
        print(f"{len(sonder_pdf)} goedgekeurde lesse het nog geen PDF nie:")
        for p in sonder_pdf:
            print("  " + os.path.relpath(p, P.REPO))
    return 1 if sonder_pdf else 0


if __name__ == "__main__":
    sys.exit(main())

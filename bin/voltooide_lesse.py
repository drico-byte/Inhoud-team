#!/usr/bin/env python3
"""File every approved lesson's PDF into 'Voltooide lesse', sorted by grade, subject
and sub-topic.

Lampies, 22 September 2026: finished lessons are output to one folder that people
browse, ordered into sensible folders:

    Voltooide lesse/Graad 6/Lewensvaardighede/Ontwikkeling van self/Les 03 - <titel>.pdf

The PDF beside the lesson stays where it is: that one is the pipeline's copy. This
folder is a delivery copy, and it is rebuilt by copying, never by editing. The sign-
off step (hardloop.pdf_langs_les) calls kopieer() after it makes the PDF, so every
lesson approved from now on lands here without anyone asking.

Backfill or refresh by hand:

    python bin/voltooide_lesse.py --vak Lewensvaardighede --graad 5 --graad 6
    python bin/voltooide_lesse.py --alles

Only APPROVED lessons are copied. A lesson that is not approved is never delivered,
and a stale delivery copy of a lesson that went back to draft is removed.
"""

import argparse
import glob
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402

VOLTOOI = os.path.join(P.REPO, "Voltooide lesse")

# Characters Windows will not accept in a file or folder name.
_ONWETTIG = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def _veilig(naam):
    naam = _ONWETTIG.sub("", str(naam)).strip().rstrip(".")
    return re.sub(r"\s{2,}", " ", naam) or "sonder-naam"


def _subonderwerp_naam(les_json_pad, les):
    """The sub-topic's human name, from the approved spec; the folder slug if none."""
    gids = os.path.basename(os.path.dirname(os.path.abspath(les_json_pad)))
    vak = les.get("vak") or ""
    graad = les.get("graad")
    kandidaat = os.path.join(P.SPEK_GOEDGEKEUR, f"gr{graad}", P.slug(vak), gids + ".json")
    if os.path.exists(kandidaat):
        try:
            naam = P.lees_json(kandidaat).get("kaps_subonderwerp")
            if naam:
                return naam
        except ValueError:
            pass
    return gids.replace("-", " ").capitalize()


def doel_pad(les, les_json_pad):
    stam = os.path.splitext(os.path.basename(les_json_pad))[0]
    try:
        nommer = int(stam.split("-")[-1])
        voor = f"Les {nommer:02d}"
    except ValueError:
        voor = stam
    titel = les.get("titel") or ""
    lêer = _veilig(f"{voor} - {titel}" if titel else voor) + ".pdf"
    return os.path.join(
        VOLTOOI,
        f"Graad {les.get('graad')}",
        _veilig(les.get("vak") or "Vak"),
        _veilig(_subonderwerp_naam(les_json_pad, les)),
        lêer,
    )


def _ou_kopieë(doel):
    """Other files for the same lesson number (the title may have changed)."""
    gids, naam = os.path.split(doel)
    voor = naam.split(" - ")[0]
    return [p for p in glob.glob(os.path.join(gids, voor + "*.pdf")) if os.path.abspath(p) != os.path.abspath(doel)]


def kopieer(les, les_json_pad, pdf_pad=None):
    """Copy one lesson's PDF into the delivery folder. Returns the destination or None."""
    pdf_pad = pdf_pad or les_json_pad[:-len(".json")] + ".pdf"
    doel = doel_pad(les, les_json_pad)
    if les.get("status") != "goedgekeur":
        for p in [doel] + _ou_kopieë(doel):
            if os.path.exists(p):
                os.remove(p)
        return None
    if not os.path.exists(pdf_pad):
        return None
    os.makedirs(os.path.dirname(doel), exist_ok=True)
    for p in _ou_kopieë(doel):
        os.remove(p)
    shutil.copy2(pdf_pad, doel)
    return doel


def _lesse(graad=None, vak=None):
    patroon = os.path.join(
        P.KONSEPTE,
        f"gr{graad}" if graad else "gr*",
        P.slug(vak) if vak else "*",
        "*",
        "les-*.json",
    )
    for pad in sorted(glob.glob(patroon)):
        stam = os.path.splitext(os.path.basename(pad))[0]
        if re.fullmatch(r"les-\d+", stam):
            yield pad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vak")
    ap.add_argument("--graad", type=int, action="append")
    ap.add_argument("--alles", action="store_true")
    a = ap.parse_args()
    if not (a.alles or a.graad or a.vak):
        ap.error("give --alles, or --graad and/or --vak")

    grade = a.graad or [None]
    gekopieer, sonder_pdf, nie_goedgekeur = [], [], 0
    for g in grade:
        for pad in _lesse(g, a.vak):
            les = P.lees_json(pad)
            if les.get("status") != "goedgekeur":
                kopieer(les, pad)  # removes a stale delivery copy
                nie_goedgekeur += 1
                continue
            doel = kopieer(les, pad)
            (gekopieer if doel else sonder_pdf).append(doel or pad)

    for d in gekopieer:
        print("  " + os.path.relpath(d, P.REPO))
    print(f"\n{len(gekopieer)} gekopieer na '{os.path.relpath(VOLTOOI, P.REPO)}'.")
    if sonder_pdf:
        print(f"{len(sonder_pdf)} goedgekeurde lesse het nog geen PDF nie:")
        for p in sonder_pdf:
            print("  " + os.path.relpath(p, P.REPO))
    if nie_goedgekeur:
        print(f"{nie_goedgekeur} lesse is nie goedgekeur nie en is nie afgelewer nie.")
    return 1 if sonder_pdf else 0


if __name__ == "__main__":
    sys.exit(main())

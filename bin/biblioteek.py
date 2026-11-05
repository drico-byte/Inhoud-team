#!/usr/bin/env python3
"""Deliver finished lessons into the shared content library.

Drico's delivery rule for all teams (AFLEWERING-REEL.md, 5 November 2026) lives in
SharePoint beside the naming rule, in `0000NUWE LESSE/`, and is not copied here. In
short: the library "Wolkskool Nuwe Inhoud V3" is the one place finished work lives,
and this team's product is each subject's `Inhoud/` folder:

    Wolkskool Nuwe Inhoud V3 - Documents/Graad 4/PSW/Inhoud/
        G4_PSW_07 - Wat voel jy.json     the lesson as data; downstream builds from it
        G4_PSW_07 - Wat voel jy.pdf      the same lesson as a document, the check and record
        manifest.json                    this subject's lessons, which issue is current

The library is a mirror of `V2 inhoud`, subject by subject: the same files, byte for
byte, so what the HTML team builds from is exactly what bin/v2_inhoud.py checked (every
learner string of the data found in the PDF). The subject's manifest is V2's entries
for that subject, with `pdf` and `json` as file names in the folder.

Sign-off calls `lewer()` in the same step as the other deliveries: it rebuilds V2 and
mirrors the lesson's subject. A lesson that is redone replaces its files, and a file of
ours that is no longer current (its label changed, or it left V2) is removed, so there
is never more than one file per ID. Only our own files in `Inhoud/` are touched.

    python bin/biblioteek.py --alles --droog     # what would change, change nothing
    python bin/biblioteek.py --alles             # mirror every subject in V2
    python bin/biblioteek.py --tel               # files per Inhoud folder, against V2

The library is found under your home folder, or set WOLKSKOOL_BIBLIOTEEK to the
synced "Wolkskool Nuwe Inhoud V3 - Documents" folder. A PC that does not sync it gets
a warning at sign-off, never a failed sign-off.
"""

import argparse
import collections
import glob
import hashlib
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402

BIBLIOTEEK_NAAM = "Wolkskool Nuwe Inhoud V3 - Documents"
PRODUK = "Inhoud"
V2 = os.path.join(P.REPO, "V2 inhoud")
V2_MANIFES = os.path.join(V2, "manifest.json")
ONS = re.compile(r"^G\d+_[A-Z]+_\d+[a-z]? - .+\.(pdf|json)$")


def biblioteek_gids():
    if os.environ.get("WOLKSKOOL_BIBLIOTEEK"):
        return os.environ["WOLKSKOOL_BIBLIOTEEK"]
    for kandidaat in glob.glob(os.path.join(os.path.expanduser("~"), "*", BIBLIOTEEK_NAAM)):
        if os.path.isdir(kandidaat):
            return kandidaat
    return None


def _sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _vakke():
    """{(grade, code): [V2 manifest entries]}, the code taken from each entry's ID."""
    uit = collections.defaultdict(list)
    for e in P.lees_json(V2_MANIFES).get("lesse") or []:
        g, kode = e["id"].split("_")[:2]
        uit[(int(g[1:]), kode)].append(e)
    return uit


def _manifes(graad, kode, rye):
    lesse = []
    for e in sorted(rye, key=lambda e: e["id"]):
        e = dict(e)
        e["pdf"], e["json"] = os.path.basename(e["pdf"]), os.path.basename(e["json"])
        lesse.append(e)
    return {
        "skema": "wolkskool-inhoud-manifes-1",
        "nota": ("Inhoud-team's lessons for this subject. Build from the .json; the .pdf is the "
                 "check and the record. status 'final' may be built, 'held' may not (see 'rede'). "
                 "json_sha256 is the content fingerprint: when it changes, the lesson was reissued "
                 "and the previous issue is listed under 'uitgawes'. ou_pdf/ou_json are the names "
                 "in V2 inhoud before the naming rule."),
        "graad": graad, "vak": kode, "lesse": lesse,
    }


def spieel(graad, kode, rye, wortel, droog=False):
    """Make one subject's Inhoud/ match V2. Returns (copied, removed, manifest changed)."""
    gids = os.path.join(wortel, f"Graad {graad}", kode, PRODUK)
    if not droog:
        os.makedirs(gids, exist_ok=True)
    behou, gekopieer = set(), 0
    for e in rye:
        for k in ("pdf", "json"):
            bron = os.path.join(V2, e[k])
            doel = os.path.join(gids, os.path.basename(e[k]))
            behou.add(os.path.basename(doel))
            if not os.path.exists(doel) or _sha(doel) != _sha(bron):
                gekopieer += 1
                if not droog:
                    shutil.copy2(bron, doel)
    weg = [f for f in (os.listdir(gids) if os.path.isdir(gids) else [])
           if ONS.match(f) and f.startswith(f"G{graad}_{kode}_") and f not in behou]
    if not droog:
        for f in weg:
            os.remove(os.path.join(gids, f))
    teks = json.dumps(_manifes(graad, kode, rye), ensure_ascii=False, indent=1) + "\n"
    mpad = os.path.join(gids, "manifest.json")
    ou = open(mpad, encoding="utf-8").read() if os.path.exists(mpad) else None
    if ou != teks and not droog:
        with open(mpad, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(teks)
    return gekopieer, weg, ou != teks


def lewer(les, les_json_pad, pdf_pad=None):
    """At sign-off: rebuild V2, then mirror this lesson's subject. (folder or None, note)."""
    wortel = biblioteek_gids()
    if not wortel:
        return None, "the content library is not synced on this PC"
    import lesregister as LR
    ry = LR.vir(les_json_pad)
    if not ry:
        return None, "no ID in the lesson register yet"
    import contextlib
    import io
    import v2_inhoud
    with contextlib.redirect_stdout(io.StringIO()) as uit:
        v2_inhoud.main()
    graad, kode = int(ry["id"].split("_")[0][1:]), ry["id"].split("_")[1]
    rye = _vakke().get((graad, kode)) or []
    if not any(e["id"] == ry["id"] for e in rye):
        laaste = [r for r in uit.getvalue().splitlines() if r.strip()][-3:]
        return None, "V2 did not take the lesson: " + " / ".join(laaste)
    spieel(graad, kode, rye, wortel)
    return os.path.join(wortel, f"Graad {graad}", kode, PRODUK), ""


def tel(wortel):
    print(f"{'folder':28} V2 lessons  .json  .pdf  manifest")
    verskil = 0
    for (g, kode), rye in sorted(_vakke().items()):
        gids = os.path.join(wortel, f"Graad {g}", kode, PRODUK)
        lers = os.listdir(gids) if os.path.isdir(gids) else []
        js = sum(1 for f in lers if ONS.match(f) and f.endswith(".json"))
        pdf = sum(1 for f in lers if ONS.match(f) and f.endswith(".pdf"))
        m = os.path.join(gids, "manifest.json")
        mn = len(P.lees_json(m).get("lesse") or []) if os.path.exists(m) else 0
        ok = js == pdf == mn == len(rye)
        verskil += not ok
        print(f"{os.path.relpath(gids, wortel):28} {len(rye):10} {js:6} {pdf:5} {mn:9}"
              + ("" if ok else "   <-- differs"))
    return 1 if verskil else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--alles", action="store_true")
    ap.add_argument("--droog", action="store_true")
    ap.add_argument("--tel", action="store_true")
    a = ap.parse_args()
    wortel = biblioteek_gids()
    if not wortel:
        raise SystemExit(f"'{BIBLIOTEEK_NAAM}' was not found under your home folder; "
                         "set WOLKSKOOL_BIBLIOTEEK.")
    if a.tel:
        return tel(wortel)
    if not a.alles:
        ap.print_help()
        return 0
    for (g, kode), rye in sorted(_vakke().items()):
        n, weg, m = spieel(g, kode, rye, wortel, droog=a.droog)
        print(f"  Graad {g}/{kode}/{PRODUK}: {len(rye)} lessons, {n} files "
              f"{'to copy' if a.droog else 'copied'}, {len(weg)} old files "
              f"{'to remove' if a.droog else 'removed'}, manifest {'changes' if m else 'unchanged'}")
    if a.droog:
        print("--droog: nothing was written")
    return 0


if __name__ == "__main__":
    sys.exit(main())

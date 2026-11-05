#!/usr/bin/env python3
"""The lesson register: every delivered lesson's ID and file label.

Drico's naming rule for all teams (5 November 2026) lives in SharePoint, in
`0000NUWE LESSE/LESNAAM-REEL.md`, and is not copied here. In short: a delivered
file is named `<ID> - <label>`, e.g. `G4_PSW_07 - Wat voel jy.pdf`; the ID never
changes; and this team writes the register every other team copies its IDs from.

The register is kept here, in `kaps/lesregister/<G4_PSW>.csv`, so every PC has it in
git and every delivery script reads one source. Beside the rule's four columns
(id, titel, tipe, ou_naam) it carries `bron`, the lesson draft the ID belongs to,
because that is how a script knows which lesson it is holding. `--publiseer` writes
the rule's four columns to SharePoint's `Lesregister/`, every row included.

A row of `tipe` `video` (a video-only lesson, e.g. the Gr 4 Nedersettings case studies
G4_GEO_07b-07e) has no draft, so its `bron` is empty. Such a row is published and kept
like any other; no delivery script looks it up, because there is nothing of ours to
deliver for it.

    python bin/lesregister.py --publiseer         # copy every register to SharePoint
    python bin/lesregister.py --wys gr5           # print one grade's IDs and labels

Never renumber. A lesson added later gets its own row here before it is delivered;
the scripts refuse, or fall back to the old name with a warning, until it has one.
"""

import argparse
import csv
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402

REGISTER = os.path.join(P.REPO, "kaps", "lesregister")
KOLOMME = ["id", "titel", "tipe", "ou_naam"]

_cache = None


def _laai():
    global _cache
    if _cache is None:
        _cache, ids = {}, set()
        for f in sorted(glob.glob(os.path.join(REGISTER, "G*.csv"))):
            with open(f, encoding="utf-8", newline="") as fh:
                for r in csv.DictReader(fh):
                    if r["id"] in ids:
                        raise SystemExit(f"{os.path.basename(f)}: the ID {r['id']} appears twice")
                    ids.add(r["id"])
                    bron = (r.get("bron") or "").replace("\\", "/")
                    if bron:
                        if bron in _cache:
                            raise SystemExit(f"{bron} has two IDs in the register: "
                                             f"{_cache[bron]['id']} and {r['id']}")
                        _cache[bron] = dict(r, bron=bron)
    return _cache


def vir(les_json_pad):
    """The register row for one lesson draft, or None if it has no ID yet.

    LESREGISTER_AF=1 makes every lesson look unregistered, so a script gives the name
    it gave before the rule. Only for working out which old file a new name replaces.
    """
    if os.environ.get("LESREGISTER_AF"):
        return None
    rel =os.path.relpath(os.path.abspath(les_json_pad), P.REPO).replace(os.sep, "/")
    return _laai().get(rel)


def lêernaam(ry, ext, deel=""):
    """`G4_PSW_07 - Wat voel jy[ - <deel>].<ext>` for a register row."""
    return f"{ry['id']} - {ry['titel']}" + (f" - {deel}" if deel else "") + ext


def sharepoint_gids():
    """The synced `0000NUWE LESSE` folder on this PC: the one that holds LESNAAM-REEL.md."""
    if os.environ.get("WOLKSKOOL_NUWE_LESSE"):
        return os.environ["WOLKSKOOL_NUWE_LESSE"]
    tuis = os.path.expanduser("~")
    for wortel in glob.glob(os.path.join(tuis, "*")):
        for kandidaat in glob.glob(os.path.join(wortel, "*", "LESNAAM-REEL.md")):
            return os.path.dirname(kandidaat)
    return None


def publiseer():
    gids = sharepoint_gids()
    if not gids:
        raise SystemExit("No folder holding LESNAAM-REEL.md was found under your home folder. "
                         "Set WOLKSKOOL_NUWE_LESSE to the synced '0000NUWE LESSE' folder.")
    uit = os.path.join(gids, "Lesregister")
    os.makedirs(uit, exist_ok=True)
    n = 0
    for f in sorted(glob.glob(os.path.join(REGISTER, "G*.csv"))):
        with open(f, encoding="utf-8", newline="") as fh:
            rye = list(csv.DictReader(fh))
        with open(os.path.join(uit, os.path.basename(f)), "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=KOLOMME, extrasaction="ignore")
            w.writeheader()
            w.writerows(rye)
        n += 1
    print(f"{n} registers written to {uit}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--publiseer", action="store_true")
    ap.add_argument("--wys")
    a = ap.parse_args()
    if a.publiseer:
        publiseer()
    if a.wys:
        for bron, r in sorted(_laai().items(), key=lambda t: t[1]["id"]):
            if bron.startswith(f"konsepte/{a.wys}/"):
                print(f"{r['id']}  {r['titel']}  ({r['tipe']})  {bron}")
    if not (a.publiseer or a.wys):
        ap.print_help()


if __name__ == "__main__":
    main()

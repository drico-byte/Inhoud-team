# -*- coding: utf-8 -*-
"""Wat is elke les se WERKLIKE stand: wag sy vir 'n regstelling, of net vir 'n nasien?

'n MENS_NODIG-verslag wat OUER as die konsep is, beskryf teks wat nie meer bestaan nie. Wie hom as
'n werklys lees, brief 'n skrywer oor foute wat al herstel is - dit het al gebeur, sewe van nege
items in een brief. En 'n les met 'n skoon verslag aan een kant en niks aan die ander, lyk in 'n
statuslys presies soos een wat nog herstel moet word.

Daarom sorteer hierdie veeg elke onafgehandelde les in een van vier hokke:

    HERSTEL     'n verslag wat NUWER as die konsep is, vra iets - dit is werk vir 'n skrywer
                of vir die spek
    NASIEN      elke verslag is ouer as die konsep, of daar is nie een nie - die konsep het
                sedertdien verander, dus is die verslag nie meer 'n bevinding oor HIERDIE teks nie
    GEREED      albei kante GOEDGEKEUR en albei nuwer as die konsep - sy kan onderteken word
    GEEN        nog nooit nagegaan nie

Die getal wat saak maak, is NASIEN: dit is hoeveel lesse net 'n nasien nodig het en nie 'n
regstelling nie, en dit is gewoonlik baie meer as wat 'n statuslys laat blyk.

    python bin/verslagstand.py --graad 7 --vak Lewensorientering
    python bin/verslagstand.py --alles
"""
from __future__ import print_function

import argparse
import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKOON = ("GOEDGEKEUR", "PASS")
# A report written in the same second as the draft is not stale; a writer and the
# runner touch both within a second of each other on a fast machine.
SPELING = 5.0


def slug(s):
    s = (s or "").lower().replace("ë", "e").replace("ê", "e").replace("ï", "i").replace("ô", "o")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def verslae(pad):
    """(soort, verdict, is_verouderd) vir elke verslag naas 'n konsep."""
    gids = os.path.dirname(pad)
    n = os.path.splitext(os.path.basename(pad))[0].split("-")[-1]
    tk = os.path.getmtime(pad)
    uit = []
    for soort in ("dekking", "feite"):
        q = os.path.join(gids, "les-%s.%s.json" % (n, soort))
        if not os.path.exists(q):
            uit.append((soort, None, None))
            continue
        try:
            verdict = json.load(open(q, encoding="utf-8")).get("verdict")
        except (OSError, ValueError):
            verdict = "ONLEESBAAR"
        uit.append((soort, verdict, os.path.getmtime(q) < tk - SPELING))
    return uit


def sorteer(pad):
    """(hok, rede) vir een konsep."""
    v = verslae(pad)
    if all(verdict is None for _, verdict, _ in v):
        return "GEEN", "nog nooit nagegaan nie"

    vra = [(s, verdict) for s, verdict, ou in v
           if verdict is not None and not ou and verdict not in SKOON]
    if vra:
        return "HERSTEL", ", ".join("%s=%s" % (s, verdict) for s, verdict in vra)

    skoon = [s for s, verdict, ou in v if verdict in SKOON and not ou]
    if len(skoon) == 2:
        return "GEREED", "albei kante skoon en nuwer as die konsep"

    redes = []
    for s, verdict, ou in v:
        if verdict is None:
            redes.append("%s ontbreek" % s)
        elif ou:
            redes.append("%s is ouer as die konsep (%s)" % (s, verdict))
    return "NASIEN", ", ".join(redes)


def lesse(graad=None, vak=None):
    patroon = os.path.join(REPO, "konsepte", "gr%s" % graad if graad else "gr*",
                           slug(vak) if vak else "*", "*", "les-*.json")
    for pad in sorted(glob.glob(patroon)):
        stam = os.path.splitext(os.path.basename(pad))[0]
        if re.fullmatch(r"les-\d+", stam):
            yield pad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--graad")
    ap.add_argument("--vak")
    ap.add_argument("--alles", action="store_true")
    a = ap.parse_args()
    if not (a.alles or a.graad or a.vak):
        ap.error("gee --alles, of --graad en/of --vak")

    hokke = {"HERSTEL": [], "NASIEN": [], "GEREED": [], "GEEN": [], "GOEDGEKEUR": []}
    for pad in lesse(a.graad, a.vak):
        try:
            les = json.load(open(pad, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        naam = "%s %s" % (os.path.basename(os.path.dirname(pad))[:22],
                          os.path.splitext(os.path.basename(pad))[0].split("-")[-1])
        if les.get("status") == "goedgekeur":
            hokke["GOEDGEKEUR"].append((naam, ""))
            continue
        hok, rede = sorteer(pad)
        hokke[hok].append((naam, rede))

    totaal = sum(len(v) for v in hokke.values())
    if not totaal:
        print("\n  geen les gevind nie\n")
        return 2

    print()
    print("  %d lesse gelees" % totaal)
    print("  %-11s %d" % ("GOEDGEKEUR", len(hokke["GOEDGEKEUR"])))
    for hok in ("GEREED", "HERSTEL", "NASIEN", "GEEN"):
        print("  %-11s %d" % (hok, len(hokke[hok])))
    print()
    for hok in ("GEREED", "HERSTEL", "NASIEN", "GEEN"):
        if not hokke[hok]:
            continue
        print("%s (%d):" % (hok, len(hokke[hok])))
        for naam, rede in hokke[hok]:
            print("  %-26s %s" % (naam, rede))
        print()
    if hokke["NASIEN"]:
        print("  Die NASIEN-hok is nie 'n werklys vir 'n skrywer nie. Daardie verslae is ouer as")
        print("  hulle konsepte, dus is hulle bevindings oor teks wat nie meer bestaan nie.")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())

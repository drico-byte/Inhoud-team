# -*- coding: utf-8 -*-
"""Vind halwe regstellings: 'n beslissing wat in feiterisiko aangeteken is NA die
laaste keer dat kern aangeraak is.

Hoekom dit bestaan
------------------
Wanneer 'n feitenasien 'n fout vind, hoort die regstelling in die veld wat die fout
BEVEEL het - gewoonlik 'n kern-item - want dekking toets teen kern en 'n skrywer lees
kern. 'n Feiterisiko-inskrywing dra die bronne en die redenasie; dit is nie 'n vereiste
nie. Om net die feiterisiko by te voeg, is 'n halwe regstelling: die spek bly die fout
beveel, 'n korrekte konsep lees as gebrekkig, en die volgende hersiening sit die fout
terug.

Dit is die mees herhaalde fout in hierdie bewaarplek. Die opgetekende reel se die
teenmiddel is om die kern-items UIT TE DRUK in dieselfde asem as wat 'n feiterisiko
bygevoeg word - en daardie reel is toe self herhaaldelik nie gevolg nie, want om aan 'n
lys te append is een reel kode en om die regte kern-item te vind is werk. So die reel
moet toetsbaar wees eerder as onthoubaar.

Wat dit meet
------------
Per les: die laaste gedateerde regstelling in feiterisiko teenoor die laaste gedateerde
regstelling in kern (en die ander veldе wat 'n opdrag dra). Is feiterisiko NUWER, is daar
'n beslissing wat die skrywer en die dekkingsnasiener nooit sien nie.

Dit is 'n VERKLIKKER, nie 'n bewys nie. 'n Nuwer feiterisiko-datum is heeltemal in orde
wanneer die bevinding niks was wat kern beveel het nie - 'n nuwe risiko, 'n bevestiging,
'n nota oor 'n woordelys-inskrywing. Die skrip se dus waar om te KYK, nie wat verkeerd is
nie.

    python bin/laat-regstellings.py
    python bin/laat-regstellings.py --vak "Sosiale Wetenskappe" --graad 4
"""
import argparse
import datetime
import glob
import io
import json
import os
import re

MAANDE = {
    "januarie": 1, "februarie": 2, "maart": 3, "april": 4, "mei": 5, "junie": 6,
    "julie": 7, "augustus": 8, "september": 9, "oktober": 10, "november": 11,
    "desember": 12,
}
DATUM = re.compile(r"\b(\d{1,2})\s+(%s)\s+(\d{4})\b" % "|".join(MAANDE), re.IGNORECASE)

# Velde wat 'n OPDRAG dra - hulle bind 'n skrywer en dekking toets teen hulle.
OPDRAGVELDE = ("kern", "aanvulling", "fokusvraag_skakel", "historiese_konsepte",
               "video_naat", "verwagte_begrippe", "titel", "moeilike_konsepte")


# Lesse noem historiese datums - 13 November 1956, 20 April 1964 - en die is GEEN
# regstellingsdatums nie. Tel net datums uit die tydperk waarin hierdie bewaarplek
# werk, anders laat 'n hofuitspraak uit 1956 'n veld onlangs gewysig lyk.
VROEGSTE_WERKJAAR = 2025


def datums(node):
    """Elke REGSTELLINGSDATUM enige plek in 'n stuk van die boom."""
    gevind = []
    if isinstance(node, str):
        for dag, maand, jaar in DATUM.findall(node):
            if int(jaar) < VROEGSTE_WERKJAAR:
                continue
            try:
                gevind.append(datetime.date(int(jaar), MAANDE[maand.lower()], int(dag)))
            except ValueError:
                pass
    elif isinstance(node, dict):
        for v in node.values():
            gevind.extend(datums(v))
    elif isinstance(node, list):
        for v in node:
            gevind.extend(datums(v))
    return gevind


def jongste(node):
    ds = datums(node)
    return max(ds) if ds else None


def keur_les(les):
    """Gee (feiterisiko_datum, opdrag_datum, watter_veld) terug, of None."""
    fr = jongste(les.get("feiterisiko"))
    if fr is None:
        return None
    beste, beste_veld = None, None
    for veld in OPDRAGVELDE:
        d = jongste(les.get(veld))
        if d and (beste is None or d > beste):
            beste, beste_veld = d, veld
    return fr, beste, beste_veld


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--vak")
    p.add_argument("--graad")
    p.add_argument("--wortel", default=os.path.join(os.path.dirname(__file__), ".."))
    a = p.parse_args()

    patroon = os.path.join(a.wortel, "spesifikasies", "goedgekeur", "**", "*.json")
    lêers = sorted(glob.glob(patroon, recursive=True))
    gekeur, gevlag = 0, 0

    for f in lêers:
        try:
            d = json.load(io.open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict) or "lesse" not in d:
            continue
        if a.vak and str(d.get("vak", "")).lower() != a.vak.lower():
            continue
        if a.graad and str(d.get("graad", "")) != str(a.graad):
            continue

        naam = os.path.splitext(os.path.basename(f))[0]
        kop_gedruk = False
        for les in d.get("lesse", []):
            gekeur += 1
            uitslag = keur_les(les)
            if not uitslag:
                continue
            fr, opdrag, veld = uitslag
            if opdrag is not None and fr <= opdrag:
                continue
            if not kop_gedruk:
                print("\n%s" % naam)
                kop_gedruk = True
            gevlag += 1
            nommer = les.get("nommer", "?")
            if opdrag is None:
                print("  les %-3s feiterisiko %s, en GEEN opdragveld dra 'n datum nie"
                      % (nommer, fr.isoformat()))
            else:
                dae = (fr - opdrag).days
                print("  les %-3s feiterisiko %s is %d dae NUWER as %s (%s)"
                      % (nommer, fr.isoformat(), dae, veld, opdrag.isoformat()))

    print("\n%d lesse gekeur, %d om na te kyk." % (gekeur, gevlag))
    if gevlag:
        print("'n Nuwer feiterisiko-datum is nie op sigself 'n fout nie - dit is reg wanneer")
        print("die bevinding niks was wat 'n opdragveld beveel het nie. Gaan elkeen na en vra:")
        print("watter veld het die fout BEVEEL, en se daardie veld se OPENINGSREEL dit nog?")
    return 1 if gevlag else 0


if __name__ == "__main__":
    raise SystemExit(main())

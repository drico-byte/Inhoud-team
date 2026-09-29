# -*- coding: utf-8 -*-
"""Vind spesifikasie-velde waar 'n BESTELLING agter 'n REKORD-merker wegkruip.

Die probleem wat hierdie skrip vang
-----------------------------------
'n Regstelling word gewoonlik so gemaak: vervang die sin wat verkeerd was, en sit
'n gedateerde nota daarby. As daardie vervanging IN DIE MIDDEL van 'n veld
gebeur, skuif al die oorspronklike teks wat daarna gekom het, agter die merker in.
Dit LYK dan soos rekord, maar dit is nog steeds 'n lewende bestelling - en dit is
die laaste ding wat 'n skrywer lees.

Op 29 September 2026 het presies dit gebeur: les 2 se kern[3] het bo-aan verbied
om die video se 'effens anders' by te skryf, en 1 050 karakters later, agter die
merker, geeindig met 'Skryf dit soos die video dit se en gaan aan.' 'n Veegskrip
wat net die EERSTE voorkoms van 'n frase toets, sien dit nooit.

Wat 'n skoon veld lyk soos
--------------------------
Die bestelling staan heel, een keer, VOOR die merker. Die merker staan onderaan.
Niks agter die merker lees soos 'n opdrag nie.


WAT HIERDIE SKRIP NIE VANG NIE, en dit is die helfte wat meer gekos het
----------------------------------------------------------------------
Die SPIEeLBEELD: 'n bewoording wat BO bestel word en ONDER teruggetrek word. Les 3
se kern[2] het bo-aan 'die appel se RONDHEID' bestel en 'n gedateerde nota onder
het dit doodgemaak; 'n dekkingsnasiener het dit gevind, nie hierdie skrip nie.

Ek het dit probeer bou en dit werk nie. Die rede is nie 'n gogga nie, dit is die
taak: die rekord herhaal byna nooit die bestelling se woorde nie. Die bestelling
se 'die appel se rondheid' en die rekord se ''n appel lyk soos 'n ronde bal' -
dieselfde saak, geen gemeenskaplike string nie. Elke passing wat wyd genoeg was om
dit te tref, het ook elke voorwerp getref wat toevallig in albei helftes voorkom.

Dit is met opset NIE hier nie. 'n Toetser wat 'skoon' rapporteer sonder dat hy
bewys is, is erger as geen toetser nie, want hy koop vertroue wat hy nie verdien
nie. Die spieelbeeld bly 'n mens of 'n dekkingsnasiener se werk, en hulle vang
dit - hierdie een het dit twee keer op een dag gevang.

Gebruik
-------
    python bin/spekbestelling.py                     # al die goedgekeurde spesifikasies
    python bin/spekbestelling.py --vak "Sosiale Wetenskappe" --graad 4
    python bin/spekbestelling.py --pad spesifikasies/goedgekeur/gr4/.../x.json

Uitset: elke veld waar 'n gebiedende vorm agter 'n merker staan, met die sin self,
sodat 'n mens kan besluit. Dit is 'n RAPPORT en nie 'n hek nie - party velde se
rekord haal heeltemal tereg 'n ou bestelling aan om te se wat teruggetrek is, en
net 'n mens kan die twee uitmekaar hou. Afsluitkode 1 as daar iets is om te sien.
"""
import argparse
import glob
import io
import json
import os
import re
import sys

# Die merkers wat 'n rekord-afdeling oopmaak, in die volgorde waarin hulle in
# hierdie repository gebruik word.
MERKERS = ("REKORD, NIE BESTELLING NIE", "REGGEMAAK", "TERUGGETREK", "BYGEVOEG",
           "OORWEEG EN BEHOU", "OORWEEG EN AFGEWYS", "AANGETEKEN", "HERSKRYF")

# Werkwoorde wat 'n aanhaling inlui: die sin HAAL 'n ou bestelling aan eerder as
# om hom te gee. 'n Rekord mag - en moet dikwels - die ou bewoording aanhaal.
WERKWOORDE = ("SKRYF", "GEBRUIK", "NOEM", "NEEM", "DRA", "HOU", "BLY", "MOENIE")

AANHALING = (
    "het gese", "het bestel", "het geskryf", "het gevra", "het beveel", "het gelui",
    "tot vandag", "hierdie item het", "hierdie veld het", "hierdie sin het",
    "is teruggetrek", "word teruggetrek", "die ou bewoording", "het gedra",
    "het bo-aan", "het aan sy einde", "sy het gelui", "teruggetrek",
)

# 'n Verbod in die bestelling-helfte.
VERBOD = re.compile("MOENIE", re.U)


def variante(frase):
    """'soms effens anders' hoort ook te tref wanneer die rekord net 'effens
    anders' se. Gee die frase en sy agtervoegsels, lank genoeg om nie raas te
    maak nie."""
    woorde = frase.split()
    uit = []
    for i in range(len(woorde)):
        v = " ".join(woorde[i:])
        if len(v) >= 10:
            uit.append(v)
    return uit or [frase]


def gehaalde_frases(sin):
    """Frases tussen enkelaanhalingstekens, wat is hoe hierdie repository 'n
    bewoording benoem: 'effens anders', 'vasteland', 'elke seilskip'."""
    return [m.group(1).strip().lower()
            for m in re.finditer(r"'([^']{3,60})'", sin)
            if m.group(1).strip()]


def sinne(teks):
    """Breek in sinne op, grof maar genoeg. Hou die posisie van elke sin."""
    uit, begin = [], 0
    for m in re.finditer(r"(?<=[.!])\s+(?=[A-Z'\"(])", teks):
        uit.append((begin, teks[begin:m.start()].strip()))
        begin = m.end()
    if begin < len(teks):
        uit.append((begin, teks[begin:].strip()))
    return uit


def loop_velde(o, pad=""):
    if isinstance(o, dict):
        for k, v in o.items():
            for r in loop_velde(v, pad + "/" + k):
                yield r
    elif isinstance(o, list):
        for i, v in enumerate(o):
            for r in loop_velde(v, pad + "[%d]" % i):
                yield r
    elif isinstance(o, str) and len(o) > 80:
        yield pad, o


def eerste_merker(teks):
    treffers = [teks.find(m) for m in MERKERS if teks.find(m) >= 0]
    return min(treffers) if treffers else -1


def is_bevel(sin):
    """Lees hierdie sin soos 'n OPDRAG, of soos 'n mededeling?

    'Skryf dit soos die video dit se' is 'n opdrag. 'Afrikaanse Wikipedia se
    kartografie-artikel gebruik landkaarte as 'n algemene woord' is 'n
    mededeling met dieselfde werkwoord in die derde persoon, en die eerste
    weergawe van hierdie skrip het albei gevang.

    Twee vorme tel as 'n opdrag, en albei is hoe hierdie repository werklik
    bestel: die werkwoord begin die sin, of hy staan in HOOFLETTERS.
    """
    kaal = sin.strip()
    for w in WERKWOORDE:
        if kaal.upper().startswith(w):
            return True
        if w in kaal:            # hoofletters presies soos die repo bestel
            return True
    return False


def keur_veld(teks):
    """Vind 'n bewoording wat VOOR die merker verbied word en AGTER hom bestel word.

    Dit is die presiese mislukking wat op 29 September 2026 deurgeglip het: die
    veld het bo-aan verbied om 'effens anders' by te skryf en 1 050 karakters
    later, agter die merker, gese 'Skryf dit soos die video dit se en gaan aan.'
    """
    i = eerste_merker(teks)
    if i < 0:
        return []

    bestelling, rekord = teks[:i], teks[i:]

    # wat word in die bestelling-helfte verbied?
    verbied = set()
    for _, sin in sinne(bestelling):
        if VERBOD.search(sin):
            for _f in gehaalde_frases(sin):
                verbied.update(variante(_f))
            # ook die hoofletter-frases, wat hierdie repo vir 'n bewoording gebruik
            for m in re.finditer(r"'([^']{3,60})'", sin):
                verbied.update(variante(m.group(1).strip().lower()))
    if not verbied:
        return []

    uit = []
    rsinne = [sin for _, sin in sinne(rekord)]
    for n, sin in enumerate(rsinne):
        laag = sin.lower()
        if any(a in laag for a in AANHALING):
            continue                      # dit haal aan, dit beveel nie
        if not is_bevel(sin):
            continue
        # Die bevel wys dikwels met 'n VOORNAAMWOORD terug na die frase in die sin
        # voor hom: "...die vae 'effens anders'. Skryf DIT soos die video dit se."
        # Daarom kyk ons na hierdie sin EN die een voor hom.
        venster = laag
        if n > 0 and not any(a in rsinne[n - 1].lower() for a in AANHALING):
            venster = rsinne[n - 1].lower() + " " + laag
        for f in verbied:
            if f in venster:
                uit.append((f, (rsinne[n - 1] + " " + sin) if venster != laag else sin))
                break
    return uit


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pad", help="een spesifikasielêer")
    p.add_argument("--vak")
    p.add_argument("--graad", type=int)
    a = p.parse_args()

    if a.pad:
        paaie = [a.pad]
    else:
        paaie = sorted(glob.glob("spesifikasies/goedgekeur/**/*.json", recursive=True))

    gevind = 0
    gelees = 0
    for pad in paaie:
        try:
            d = json.load(io.open(pad, encoding="utf-8"))
        except (ValueError, IOError) as e:
            print("  KON NIE LEES NIE: %s (%s)" % (pad, e))
            continue
        if a.vak and d.get("vak") != a.vak:
            continue
        if a.graad and d.get("graad") != a.graad:
            continue
        gelees += 1
        kop = False
        for veldpad, teks in loop_velde(d):
            bevele = [("verbied bo, bestel onder", f, s) for f, s in keur_veld(teks)]
            if not bevele:
                continue
            if not kop:
                print("\n%s" % pad)
                kop = True
            print("  %s" % veldpad)
            for soort, frase, b in bevele:
                gevind += 1
                print("      %s: '%s'" % (soort, frase))
                print("      %s" % (b if len(b) <= 260 else b[:257] + "..."))

    print("\n%d spesifikasie(s) gelees." % gelees)
    if gevind:
        print("%d keer word 'n bewoording BO verbied en ONDER bestel." % gevind)
        print("Kyk na elkeen. 'n Bestelling hoort HEEL, EEN KEER, VOOR die merker;")
        print("agter die merker hoort net rekord. Party hiervan is vals alarm -")
        print("'n rekord mag 'n ou bestelling aanhaal om te se wat teruggetrek is.")
        return 1
    print("Geen bestelling kruip agter 'n merker weg nie.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Vind elke wyser in 'n spesifikasie wat 'n item volgens sy POSISIE aanwys in plaas van sy inhoud.

'n Wyser wat van die VOORKANT af tel - 'die eerste kernitem' - bly waar wanneer 'n item bygevoeg
word. Een wat van die AGTERKANT af tel - 'die jongste kernitem', 'die laaste item' - breek stil op
die oomblik dat enigiemand iets aanheg, en aanheg is wat 'n regstellingsdag heeldag doen. Die
persoon wat hom breek, is die persoon wat hom geskryf het, een regstelling later, en hy staan in 'n
ANDER veld as die een waaraan sy werk.

Daarom soek hierdie veeg net die agterkant-vorms.

Wat die veeg NIE aanmeld nie: 'n treffer binne 'n gedateerde merker (TERUGGETREK, REGGEMAAK,
BENOEM IN PLAAS VAN, ...). Daar is die woorde 'n REKORD van wat verkeerd was, en 'n veeg wat op die
normale regstellingsvorm afgaan, word geignoreer - wat die veeg self nutteloos maak.

    python bin/wyserveeg.py --vak "Lewensorientering" --graad 7
    python bin/wyserveeg.py --patroon "spesifikasies/goedgekeur/gr7/**/*.json"
"""
from __future__ import print_function

import argparse
import glob
import json
import os
import re
import sys

# Die agterkant-vorms, en niks wat van voor af tel.
#
# 'laaste' alleen is GEEN treffer nie: 'die laaste stap', 'die laaste sin', 'die laaste skooldag'
# is gewone prosa en kom oral voor. 'n Veeg wat op hulle afgaan, word geignoreer, en dan tel die
# treffers wat saak maak ook nie meer nie. Daarom moet die woord 'n SPEK-EENHEID aanwys.
# 'veld' en 'nota' is uit: 'die veld hieronder' noem 'n BUURVELD wat sy eie naam het en nie skuif
# wanneer 'n item bygeheg word nie. En 'KABV se laaste punt' wys na die kurrikulum se lys, wat nie
# ons s'n is om by te voeg - die guard hieronder laat hom deur.
EENHEDE = r"(?:kern-?item|item|bestelling|bewoording|bracket|inskrywing|reel|reêl|punt)"
BUITE = ('KABV', 'KAPS')
VORME = [
    r"(?:jongste|nuutste|laaste|onderste|jongere|later?ste)\s+%s" % EENHEDE,
    r"die %s hieronder" % EENHEDE,
    r"die laaste een hieronder",
    r"DIE LAASTE WEN",
]

MERKERS = ('TERUGGETREK', 'REGGEMAAK', 'VERVANG', 'GEHAAL', 'VERNOU', 'BEGRENS', 'BYGEWERK',
           'BENOEM IN PLAAS VAN', 'BENOEM IN PLAAS VAN GENOMMER', 'BEPERK', 'VERBREED',
           'TOEGELAAT', 'UITGEHAAL', 'BESTEK', 'HERSKRYF', 'OPGESKORT', 'AANGEVUL')


def binne_merker(teks, j):
    """Die naam van die merker waarin posisie j val, of None as hy lewend staan."""
    diepte = 0
    begin = []
    for i, c in enumerate(teks[:j]):
        if c == '[':
            diepte += 1
            begin.append(i)
        elif c == ']' and diepte:
            diepte -= 1
            begin.pop()
    if not begin:
        return None
    binne = teks[begin[0]:j]
    for m in MERKERS:
        if m in binne:
            return m
    return None


def velde(houer):
    """(veldnaam, indeks, string) vir elke string in 'n spek-houer, sonder die lesse-lys."""
    for naam in sorted(houer.keys()):
        if naam == 'lesse':
            continue
        v = houer[naam]
        if isinstance(v, str):
            yield naam, None, v
        elif isinstance(v, list):
            for i, x in enumerate(v):
                if isinstance(x, str):
                    yield naam, i, x
        elif isinstance(v, dict):
            for k in sorted(v.keys()):
                if isinstance(v[k], str):
                    yield naam + '/' + k, None, v[k]


def veeg(paaie):
    lewend = []
    gesien = set()
    rekord = 0
    for pad in paaie:
        try:
            s = json.load(open(pad, encoding='utf-8'))
        except Exception as e:
            print('  KON NIE LEES: %s (%s)' % (pad, e))
            continue
        kort = os.path.basename(pad)
        houers = [('vakvlak', s)]
        for les in s.get('lesse', []):
            houers.append(('les %s' % les.get('nommer'), les))
        for naam, houer in houers:
            for veld, i, teks in velde(houer):
                for pat in VORME:
                    for m in re.finditer(pat, teks, re.I):
                        plek = '%s[%d]' % (veld, i) if i is not None else veld
                        # twee patrone kan dieselfde woorde tref; tel elke plek een keer
                        sleutel = (kort, naam, plek, m.start())
                        if sleutel in gesien:
                            continue
                        gesien.add(sleutel)
                        voor = teks[max(0, m.start() - 30):m.start()]
                        if any(b in voor for b in BUITE):
                            continue
                        if binne_merker(teks, m.start()):
                            rekord += 1
                            continue
                        a = max(0, m.start() - 110)
                        lewend.append((kort, naam, plek, m.group(0),
                                       teks[a:m.end() + 90].replace('\n', ' ')))
    return lewend, rekord


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--vak')
    p.add_argument('--graad')
    p.add_argument('--patroon')
    o = p.parse_args()

    if o.patroon:
        paaie = sorted(glob.glob(o.patroon))
    else:
        wortel = os.path.join('spesifikasies', 'goedgekeur')
        if o.graad:
            wortel = os.path.join(wortel, 'gr%s' % o.graad)
        paaie = sorted(glob.glob(os.path.join(wortel, '*', '*.json')) +
                       glob.glob(os.path.join(wortel, '*', '*', '*.json')))
        if o.vak:
            sleutel = o.vak.lower().replace(' ', '').replace('ë', 'e')
            gehou = []
            for pad in paaie:
                try:
                    s = json.load(open(pad, encoding='utf-8'))
                except Exception:
                    continue
                v = str(s.get('vak', '')).lower().replace(' ', '').replace('ë', 'e')
                if v == sleutel:
                    gehou.append(pad)
            paaie = gehou

    if not paaie:
        print('\n  geen spesifikasie gevind nie\n')
        return 2

    lewend, rekord = veeg(paaie)
    print()
    print('  %d spesifikasie(s) gelees' % len(paaie))
    print('  %d rangskikkende wyser(s) binne \'n gedateerde merker - dit is rekord, nie bestelling nie'
          % rekord)
    print()
    if not lewend:
        print('  GEEN LEWENDE rangskikkende wyser nie.')
        print()
        return 0
    print('  %d LEWENDE rangskikkende wyser(s):' % len(lewend))
    print()
    for kort, naam, plek, woord, frag in lewend:
        print('  %s  %s  %s  (%s)' % (kort, naam, plek, woord))
        print('      ...%s...' % frag)
        print()
    print('  Elkeen breek sodra \'n item bygeheg word. Laat hom die item BENOEM, of haal hom weg')
    print('  waar die inhoud reeds op dieselfde plek staan.')
    print()
    return 1


if __name__ == '__main__':
    sys.exit(main())

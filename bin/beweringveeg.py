#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Vee 'n bewering oor elke spesifikasie-veld en se waar sy nog LEWEND is.

Waarvoor dit bestaan
--------------------
'n Bronregstelling maak die veld reg wat die bevinding genoem het. Dieselfde bewering
staan dan nog in 'n ander veld, 'n ander les of 'n ander subonderwerp, en die volgende
revisie sit haar terug. Dit het op 29 September 2026 DRIE keer op een dag gebeur - twee
keer binne een les, een keer oor twee lesse - elke keer nadat die reel bekend was.

Wat dit doen
------------
Vir elke treffer se dit of sy binne 'n gedateerde TERUGTREKKING staan of nie. Net 'n
treffer BUITE so 'n merker is 'n probleem: 'n rekord mag die ou bewoording dra, 'n
bestelling nie.

Wat dit NIE doen nie
--------------------
Dit lees nie of die sin werklik iets bestel nie - dit kan nie. Dit wys jou waar om te
kyk, en die laaste kolom se hoe seker dit is. Hierdie skrip vervang nie 'n
dekkingsnasiener nie; dit vang net die geval waar niemand gaan kyk het.

Gebruik
-------
    python bin/beweringveeg.py --bewering "woorde wat seermaak sonder besering"
    python bin/beweringveeg.py --bewering "vir altyd" --vak Lewensorientering --graad 7
    python bin/beweringveeg.py --bewering "kennis gesneller" --alles

Die uittreksel staan by verstek OOK in die veeg, want 'n skrywer lees hom en nie die
goedgekeurde spek nie - maar 'n treffer daar beteken net dat die uittreksel nog nie
vernuwe is nie.
"""
from __future__ import unicode_literals

import argparse
import glob
import io
import json
import os
import re
import sys

# 'n Merker wat 'n bewering doodmaak. Die venster is ruim, want 'n regstellingsnota
# loop lank voor sy die ou bewoording aanhaal.
MERKERS = [
    'TERUGGETREK', 'TERUGGETROKKE', 'HERSKRYF', 'REGGEMAAK', 'OMGEKEER', 'GESNY',
    'BESTEL NIKS', 'BESTEL NIE', 'IS DIE REKORD', 'GEDATEERDE REKORD', 'BYGEWERK',
    'GESLUIT', 'OPGESKORT', 'BEPERK', 'PARAFRASEER', 'VAL WEG', 'BESLEG',
]
VENSTER = 1800

VELDE = ('kern', 'feiterisiko', 'aanvulling', 'begrotingsnota', 'kaps_leesnota',
         'buite_bestek', 'plafon_uitsondering', 'voorrang_reel', 'aanmeldplig_reel',
         'geen_skuld_reel', 'oop_vrae_vir_lampies')


def teks_van(x):
    if isinstance(x, str):
        return x
    return json.dumps(x, ensure_ascii=False)


def gedek(teks, j):
    """Staan die treffer by j binne bereik van 'n terugtrekkingsmerker?"""
    venster = teks[max(0, j - VENSTER):j]
    for m in MERKERS:
        if m in venster:
            return m
    return None


def velde_van(houer):
    """(veldnaam, indeks, teks) vir elke veld, of hy 'n lys of 'n string is."""
    for naam in VELDE:
        v = houer.get(naam)
        if v is None:
            continue
        if isinstance(v, list):
            for i, x in enumerate(v):
                yield naam, i, teks_van(x)
        else:
            yield naam, None, teks_van(v)


def vee(paaie, bewering, kas):
    treffers = []
    for pad in paaie:
        try:
            s = json.load(io.open(pad, encoding='utf-8'))
        except ValueError as e:
            print('  KON NIE LEES NIE: %s (%s)' % (pad, e))
            continue
        houers = [(None, s)]
        for les in (s.get('lesse') or []):
            houers.append((les.get('nommer'), les))
        for nommer, houer in houers:
            for naam, i, teks in velde_van(houer):
                soek = teks if kas else teks.lower()
                doel = bewering if kas else bewering.lower()
                k = 0
                while True:
                    j = soek.find(doel, k)
                    if j < 0:
                        break
                    treffers.append({
                        'pad': pad,
                        'les': nommer,
                        'veld': naam if i is None else '%s[%d]' % (naam, i),
                        'merker': gedek(teks, j),
                        'konteks': re.sub(r'\s+', ' ', teks[max(0, j - 90):j + len(doel) + 90]),
                    })
                    k = j + 1
    return treffers


def main(argv=None):
    a = argparse.ArgumentParser(description='Vee n bewering oor elke spesifikasie-veld.')
    a.add_argument('--bewering', required=True,
                   help='die frase om te soek; kies die kortste stuk wat die bewering uniek maak')
    a.add_argument('--vak', help='beperk tot een vak se gids (soos dit in die pad staan)')
    a.add_argument('--graad', help='beperk tot een graad, bv 7')
    a.add_argument('--alles', action='store_true', help='elke graad en elke vak')
    a.add_argument('--kas', action='store_true', help='kas maak saak (by verstek nie)')
    a.add_argument('--sonder-uittreksels', action='store_true',
                   help='los die spek-uittreksels uit; by verstek loop hulle saam')
    o = a.parse_args(argv)

    if not (o.alles or o.graad or o.vak):
        o.alles = True

    wortel = 'spesifikasies/goedgekeur'
    if not os.path.isdir(wortel):
        print('Die gids %s bestaan nie. Loop hierdie skrip uit die wortel van die repo.' % wortel)
        return 2
    patroon = os.path.join(wortel, 'gr%s' % o.graad if o.graad else '*', '*', '*.json')
    paaie = sorted(glob.glob(patroon))
    if o.vak:
        n = o.vak.lower().replace(' ', '-')
        paaie = [p for p in paaie if n in p.lower().replace(' ', '-')]
    if not paaie:
        print('Geen spesifikasie gevind vir daardie keuse nie (patroon: %s).' % patroon)
        return 2

    uittreksels = []
    if not o.sonder_uittreksels:
        uittreksels = sorted(glob.glob(os.path.join(
            'konsepte', 'gr%s' % o.graad if o.graad else '*', '*', 'spek', 'les-*.json')))
        if o.vak:
            n = o.vak.lower().replace(' ', '-')
            uittreksels = [p for p in uittreksels if n in p.lower().replace(' ', '-')]

    print('')
    print('Beweringveeg: %r' % o.bewering)
    print('-' * 46)
    print('  %d spesifikasie(s) en %d uittreksel(s) gelees' % (len(paaie), len(uittreksels)))

    treffers = vee(paaie, o.bewering, o.kas)
    lewend = [t for t in treffers if not t['merker']]
    gedek_ = [t for t in treffers if t['merker']]

    print('  %d treffer(s): %d LEWEND, %d binne n gedateerde merker' %
          (len(treffers), len(lewend), len(gedek_)))
    print('')

    if not treffers:
        print('  Geen treffer. Dit beteken die bewering staan nerens in hierdie')
        print('  spesifikasies nie - NIE dat sy nie in n konsep staan nie.')
    for t in lewend:
        print('  LEWEND  les %-4s %-22s %s' % (t['les'], t['veld'], os.path.basename(t['pad'])))
        print('          ...%s...' % t['konteks'])
    if gedek_:
        print('')
        print('  Binne n merker (n rekord mag die ou bewoording dra):')
        for t in gedek_:
            print('    %-10s les %-4s %-22s %s' %
                  (t['merker'][:10], t['les'], t['veld'], os.path.basename(t['pad'])))

    if uittreksels:
        u = vee(uittreksels, o.bewering, o.kas)
        u_lewend = [t for t in u if not t['merker']]
        print('')
        print('  Uittreksels: %d treffer(s), %d lewend.' % (len(u), len(u_lewend)))
        if u_lewend and not lewend:
            print('  DIE UITTREKSELS IS AGTER DIE SPEK - loop bin/vernuwe-uittreksels.py.')
        for t in u_lewend:
            print('    LEWEND  %s  %s' % (t['veld'], t['pad']))

    print('')
    if lewend:
        print('  %d LEWENDE treffer(s). Gaan elkeen na: n veld wat die bewering nog' % len(lewend))
        print('  BESTEL, moet by sy eie openingsin reggemaak word, nie met n nota bo-op.')
        return 1
    print('  Geen lewende treffer. Elke oorblywende een staan binne n gedateerde merker.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

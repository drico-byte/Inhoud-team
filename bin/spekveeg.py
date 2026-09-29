#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Vind die drie vorme waarin 'n spek-veld 'n verouderde ding bly BESTEL.

'n Nasiener vind hierdie vorme een les op 'n slag, en elke vonds kos 'n hele ronde. Hierdie
veeg lees die hele spek-boom en wys hulle saam.

DIE DRIE VORME
--------------
1  'n WAT GELD-klousule. Sy sit BINNE 'n terugtrekkingshakie en lyk soos deel van die rekord,
   maar sy is die LEWENDE vereiste - en sy verouder soos enige ander bestelling. Die veeg wys
   elkeen met sy datum, as sy een het; 'n klousule sonder 'n datum verloor onder die spek se eie
   voorrang_reel en is die gevaarlikste soort.

2  'n Terugtrekking BINNE die bestelling: 'DIE REGSTELLING: se X [X is teruggetrek]' bestel
   steeds X, want 'n reviseerder lees die imperatief en skryf X.

3  'n Bewering OOR DIE KONSEP wat verouder het - 'die konsep dra nog ...', 'dus loop hierdie
   les deur die skrywer'. Sodra die skrywer geloop het, bestel so 'n sin 'n verandering aan
   teks wat reeds reg is.

Die veeg BESLUIT niks. Sy wys plekke wat 'n mens moet lees, want of 'n klousule verouderd is,
hang af van wat sedertdien besluit is.

    python bin/spekveeg.py --graad 7 --vak Lewensorientering
    python bin/spekveeg.py --pad spesifikasies/goedgekeur/gr7/lewensorientering
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

WAT_GELD = re.compile(r'WAT (?:GELD|NOU GELD|VAN HIERDIE PUNT GELD)\b', re.I)
IMPERATIEF = re.compile(r'DIE REGSTELLING\s*:|DIE VORM\s*:|DIE OPDRAG\s*:')
OOR_KONSEP = re.compile(
    r'die konsep(?: se \w+)? dra nog|dus loop hierdie les deur die skrywer|'
    r'die konsep dra nog|lesse? \d+(?:[,\s]+(?:en\s+)?\d+)* dra nog', re.I)
DATUM = re.compile(r'\b\d{1,2} (?:Januarie|Februarie|Maart|April|Mei|Junie|Julie|Augustus|'
                   r'September|Oktober|November|Desember) 20\d\d\b')
TERUG = re.compile(r'TERUGGETREK|HERSKRYF|REGGEMAAK|BYGEWERK|UITGEHAAL|TOEGEMAAK|VERNOU|VEROUDERD')


def stukkies(node, pad=''):
    """Lewer elke string in die boom, met sy pad - ook uit geneste woordeboeke."""
    if isinstance(node, str):
        yield pad, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from stukkies(v, '%s/%s' % (pad, k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from stukkies(v, '%s[%d]' % (pad, i))


def sin_om(teks, i, voor=150, na=170):
    return ' '.join(teks[max(0, i - voor):i + na].split())


def keur(pad_glob):
    lêers = sorted(glob.glob(os.path.join(pad_glob, '*.json')))
    if not lêers:
        print('Geen spek-lêers by %s' % pad_glob)
        return 1
    tot = {1: 0, 2: 0, 3: 0}
    for lêer in lêers:
        try:
            spek = json.load(open(lêer, encoding='utf-8'))
        except Exception as e:
            print('%-40s LEESFOUT: %s' % (os.path.basename(lêer), e))
            continue
        kop = os.path.basename(lêer)[:-5]
        vonds = []
        for pad, teks in stukkies(spek):
            for m in WAT_GELD.finditer(teks):
                staart = teks[m.start():m.start() + 700]
                # 'n nota kan lank wees; die datum staan dikwels aan haar begin, ver voor die
                # klousule. Soek dus wyd genoeg om 'n hele nota te dek, anders lewer die veeg
                # valse treffers - wat sy die eerste keer 14 keer gedoen het.
                het_datum = bool(DATUM.search(teks[max(0, m.start() - 1600):m.start() + 600]))
                vonds.append((1, pad, m.start(), sin_om(teks, m.start()), het_datum))
            for m in IMPERATIEF.finditer(teks):
                # Die GEVAARLIKE geval is nie 'n regstelling NA 'n imperatief nie - dit is die
                # normale, wettige vorm. Dit is wanneer die terugtrekking die imperatief se EIE
                # sin onderbreek: 'DIE REGSTELLING: se X [X is teruggetrek]'. Vuur dus net
                # wanneer 'n hakie met 'n terugtrek-woord OPEN voor die sin eindig.
                na = teks[m.end():m.end() + 500]
                punt = na.find('. ')
                hakie = na.find('[')
                if hakie < 0:
                    continue
                if punt >= 0 and punt < hakie:
                    continue            # die sin eindig eers; die regstelling volg haar wettig
                if TERUG.search(na[hakie:hakie + 220]):
                    vonds.append((2, pad, m.start(), sin_om(teks, m.start()), True))
            gesien = []
            for m in OOR_KONSEP.finditer(teks):
                # twee patrone kan dieselfde sin tref; tel haar een keer, anders is die
                # telling nie eerlik nie
                if any(abs(m.start() - g) < 120 for g in gesien):
                    continue
                # 'n bewering wat BINNE haar eie terugtrekking staan, is 'n rekord en nie 'n
                # bestelling nie. Sonder hierdie wag vuur die veeg op elke regstelling wat
                # die ou bewering aanhaal - en 'n toets wat op sy eie herstel vuur, word
                # geignoreer.
                voor = teks[max(0, m.start() - 260):m.start()]
                if TERUG.search(voor) and '[' in voor and ']' not in voor[voor.rfind('['):]:
                    continue
                gesien.append(m.start())
                vonds.append((3, pad, m.start(), sin_om(teks, m.start()), True))
        if not vonds:
            print('%-44s  skoon' % kop)
            continue
        print('%s' % kop)
        for vorm, pad, i, uittreksel, het_datum in vonds:
            tot[vorm] += 1
            merk = '' if het_datum else '   << GEEN DATUM'
            print('   vorm %d  %-34s @%-6d%s' % (vorm, pad[1:][:34], i, merk))
            print('           %s' % uittreksel[:150])
        print()
    print('-' * 78)
    print('vorm 1  WAT GELD-klousules (lewende vereistes binne \'n hakie)   %3d' % tot[1])
    print('vorm 2  terugtrekking BINNE \'n imperatief                       %3d' % tot[2])
    print('vorm 3  verouderde bewering OOR die konsep                      %3d' % tot[3])
    print()
    print('Hierdie veeg besluit niks. Lees elke plek en vra: bestel hierdie sin nog')
    print('iets wat sedertdien verander het? \'n Klousule sonder \'n datum verloor onder')
    print('die spek se eie voorrang_reel en is die gevaarlikste soort.')
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--graad', type=int)
    p.add_argument('--vak')
    p.add_argument('--pad', help='pad na \'n gids met spek-lêers')
    a = p.parse_args()
    if a.pad:
        return keur(a.pad)
    if not (a.graad and a.vak):
        p.error('gee --pad, of --graad saam met --vak')
    vak = a.vak.lower().replace(' ', '-').replace('ë', 'e').replace('é', 'e')
    return keur(os.path.join('spesifikasies', 'goedgekeur', 'gr%d' % a.graad, vak))


if __name__ == '__main__':
    sys.exit(main())

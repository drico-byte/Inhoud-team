#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Vind 'n geen-skuld-stelling wat op 'n VOORWAARDE rus.

Waarvoor dit bestaan
--------------------
Die vak se geen-skuld-reel: die stelling word GESTEL en nooit GEMOTIVEER nie. Sodra sy aan 'n
spil hang - dat die kind gekies het, gedreig is, nie kon nie, nie geweet het nie - laat die
OMGEKEERDE van daardie spil die skuld reguit terug in. Op 29 September 2026 het dieselfde
ontwerpfout in VYF lesse in een graad opgeduik, elke keer in 'n ander gedaante, en elke keer
is sy deur 'n feitenasiener gevind eerder as deur enigiets wat ons self loop.

Hoe dit werk
------------
Dit soek elke sin in 'n konsep se studie- en lysblokke wat 'n geen-skuld-vorm dra, en wys
haar saam met die sin voor en die sin na haar. Dan merk dit die sinne waarin 'n
voorwaarde-woord BINNE die geen-skuld-sin self staan.

Wat dit NIE kan doen nie
------------------------
Dit kan nie 'n VOORWAARDE van 'n VERBREDING onderskei nie. "Dit bly so al het jy nie dadelik
gepraat nie" is 'n verbreding en volkome reg; "dit is nie jou skuld nie, want jy kon nie
kies nie" is 'n spil en verkeerd. Albei dra 'n voorwaarde-woord. Die skrip wys jou waar om
te lees; die oordeel bly 'n mens se werk, en 'n feitenasiener bly die instrument wat haar
werklik toets.

Gebruik
-------
    python bin/geenskuldveeg.py --graad 7
    python bin/geenskuldveeg.py --graad 7 --vak Lewensorientering
    python bin/geenskuldveeg.py --pad konsepte/gr7/lewensorientering/selfontwikkeling-in-die-samelewing
"""
from __future__ import unicode_literals

import argparse
import glob
import io
import json
import os
import re
import sys

# 'n Geen-skuld-vorm. Hou hulle wyd: 'n vorm wat ons mis, is 'n fout wat niemand sien.
VORMS = [
    r'nie jou skuld',
    r'nie haar skuld',
    r'nie sy skuld',
    r'niemand kry die skuld',
    r'geen skuld',
    r'nie die kind se skuld',
    r'jy het niks verkeerd gedoen',
    r'sy het niks verkeerd gedoen',
    r'dit is nie iets wat jy verkeerd',
    r'jy is nie verkeerd',
    r'hoef nie skuldig te voel',
    r'moenie skuldig voel',
    # Die vorm wat Self 11 se fout was en wat hierdie lys eers gemis het: die
    # stelling word POSITIEF gestel - die skuld le by iemand anders - en sy dra
    # dikwels 'n spil ('wat AANHOU druk'), wat die kind sonder huis vir die skuld
    # laat as die ander een net EEN keer gevra het.
    # DERDE UITBREIDING, 29 September 2026. 'n Vormlys is net so goed as die vorme wat
    # iemand aan gedink het, en hierdie een het DRIE keer in een dag 'n les gemis. Voeg
    # by sodra 'n nasiener 'n vorm vind wat hier nie staan nie.
    r'die skuld lê nie by',
    r'niemand is skuldig',
    r'is nie skuldig',
    r'dra nie die skuld',
    r'die skuld lê by',
    r'die skuld is by',
    r'die skuld lê heeltemal by',
    r'dit is die .{0,30} se skuld',
]

# 'n Woord wat 'n voorwaarde inbring. 'want' en 'omdat' MOTIVEER, wat die reel verbied;
# 'as', 'waar', 'mits', 'sodra', 'solank' stel 'n voorwaarde.
VOORWAARDES = [
    (r'\bwant\b', 'motiveer'),
    (r'\bomdat\b', 'motiveer'),
    (r'\bas\b', 'voorwaarde'),
    (r'\bwaar\b', 'voorwaarde'),
    (r'\bmits\b', 'voorwaarde'),
    (r'\bsodra\b', 'voorwaarde'),
    (r'\bsolank\b', 'voorwaarde'),
    (r'\bindien\b', 'voorwaarde'),
    (r'\btensy\b', 'voorwaarde'),
]

# 'n SPIL SONDER 'N VOEGWOORD. Self 11 se fout was "die skuld le by die een wat AANHOU
# druk": geen 'as' en geen 'want', maar die kwalifiseerder op die DADER maak die geen-skuld
# voorwaardelik - 'n meisie wat toegegee het nadat sy EEN keer gevra is, vind geen huis vir
# die skuld nie. Hierdie klas is deur 'n feitenasiener gevind en nie deur hierdie skrip nie;
# sy is nou hier omdat sy 'n vorm het wat 'n mens kan sien.
DADER_SPILLE = [r'\baanhou\b', r'\bherhaaldelik\b', r'\boor en oor\b',
                r'\belke keer\b', r'\bbly .{0,12}(druk|vra|dreig)',
                r'\bnie ophou\b', r'\btelkens\b', r'\bweer en weer\b']

# 'n Verbreding lyk soos 'n voorwaarde maar is die teenoorgestelde. Ons merk haar apart.
VERBREDINGS = [r'\bbly so\b', r'\book al\b', r'\bal het jy\b', r'\bal was\b', r'\bhoe .{0,20} ook al\b',
               r'\bselfs al\b', r'\bnog steeds\b']


def sinne(teks):
    """Breek in sinne. Ruim genoeg vir Afrikaanse lesteks; 'n hakie-nota kom nie hier voor nie."""
    dele = re.split(r'(?<=[.!?])\s+', teks.strip())
    return [d for d in dele if d]


def blok_teks(b):
    """Die KOP loop saam, want 'n geen-skuld-stelling kan die kop self wees.

    Op 29 September 2026 het hierdie skrip Gesondheid 11 as 'sonder 'n geen-skuld-sin'
    gerapporteer terwyl daardie les se blokkop letterlik 'Niemand kry die skuld vir sy
    siekte nie' is. 'n Veeg wat 'n veld nie lees nie, gee 'n valse skoon.
    """
    dele = []
    kop = b.get('kop')
    if kop:
        dele.append(kop.rstrip('.') + '.')
    if b.get('teks'):
        dele.append(b['teks'])
    items = b.get('items')
    if isinstance(items, list):
        dele.append(' '.join(str(x) for x in items))
    return ' '.join(dele)


def lees(pad):
    d = json.load(io.open(pad, encoding='utf-8'))
    ry = []
    for b in d.get('blokke', []):
        if b.get('tipe') not in ('studie', 'lys'):
            continue
        ss = sinne(blok_teks(b))
        for i, s in enumerate(ss):
            if not any(re.search(v, s, re.I) for v in VORMS):
                continue
            ry.append({
                'kop': b.get('kop') or '',
                'sin': s,
                'voor': ss[i - 1] if i else '',
                'na': ss[i + 1] if i + 1 < len(ss) else '',
            })
    return d.get('titel') or os.path.basename(pad), ry


def main(argv=None):
    a = argparse.ArgumentParser(description='Vind n geen-skuld-stelling wat op n voorwaarde rus.')
    a.add_argument('--graad', help='bv 7')
    a.add_argument('--vak', help='beperk tot een vak se gids')
    a.add_argument('--pad', help='een subonderwerp se gids in plaas van graad en vak')
    o = a.parse_args(argv)

    if o.pad:
        paaie = sorted(glob.glob(os.path.join(o.pad, 'les-*.json')))
    else:
        # konsepte/gr7/<vak>/<subonderwerp>/les-N.json - vier vlakke, nie drie nie
        paaie = sorted(glob.glob(os.path.join(
            'konsepte', 'gr%s' % o.graad if o.graad else '*', '*', '*', 'les-*.json')))
        if o.vak:
            n = o.vak.lower().replace(' ', '-')
            paaie = [p for p in paaie if n in p.lower().replace(' ', '-')]
    paaie = [p for p in paaie if re.fullmatch(r'les-\d+\.json', os.path.basename(p))]
    if not paaie:
        print('Geen konsep gevind vir daardie keuse nie.')
        return 2

    print('')
    print('Geen-skuld-veeg')
    print('-' * 46)
    print('  %d konsep(te) gelees' % len(paaie))
    spil, skoon, sonder = [], [], []
    for p in paaie:
        titel, ry = lees(p)
        if not ry:
            sonder.append(os.path.basename(os.path.dirname(p))[:12] + ' ' + os.path.basename(p)[4:-5])
            continue
        for r in ry:
            r['les'] = os.path.basename(os.path.dirname(p))[:12] + ' ' + os.path.basename(p)[4:-5]
            r['titel'] = titel
            gevind = [(naam, re.search(pat, r['sin'], re.I).group(0))
                      for pat, naam in VOORWAARDES if re.search(pat, r['sin'], re.I)]
            gevind += [('spil op die DADER', re.search(pat, r['sin'], re.I).group(0))
                       for pat in DADER_SPILLE if re.search(pat, r['sin'], re.I)]
            verbr = [re.search(pat, r['sin'], re.I).group(0)
                     for pat in VERBREDINGS if re.search(pat, r['sin'], re.I)]
            r['voorwaardes'], r['verbredings'] = gevind, verbr
            (spil if gevind else skoon).append(r)

    print('  %d geen-skuld-sin(ne) gevind: %d met n voorwaarde-woord IN die sin, %d sonder'
          % (len(spil) + len(skoon), len(spil), len(skoon)))
    print('')
    if spil:
        print('  KYK HIERNA - die voorwaarde staan BINNE die geen-skuld-sin:')
        for r in spil:
            merk = ', '.join('%s: %r' % (n, w) for n, w in r['voorwaardes'])
            if r['verbredings']:
                merk += '   [dalk n VERBREDING: %s]' % ', '.join(repr(x) for x in r['verbredings'])
            print('')
            print('    %-16s %s' % (r['les'], merk))
            print('      blok: %s' % r['kop'])
            print('      >>>  %s' % r['sin'])
    if skoon:
        print('')
        print('  Sonder n voorwaarde-woord (steeds die moeite werd om die BUURSIN te lees):')
        for r in skoon:
            print('    %-16s %s' % (r['les'], r['sin'][:110]))
    if sonder:
        print('')
        print('  GEEN geen-skuld-sin gevind in %d les(se). Dit is NIE n skoon bevinding nie -' % len(sonder))
        print('  as een van hulle n STAP van n kind vra, mis sy die sin heeltemal:')
        print('    ' + ', '.join(sonder))
    print('')
    print('  Die oordeel bly n mens se werk: n VERBREDING lyk soos n voorwaarde en is die')
    print('  teenoorgestelde. n Feitenasiener bly die instrument wat haar werklik toets.')
    return 1 if spil else 0


if __name__ == '__main__':
    sys.exit(main())

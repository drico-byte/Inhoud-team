#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Read a draft against every WITHDRAWAL its own spec entry records.

WHY THIS EXISTS. Every draft in a sub-topic is written on one day, against the spec as it
stood that day. The spec then gets corrected, many times, as fact checks come back - and a
draft that was right when written now carries withdrawn forms, one per correction it never
heard about. Our checkers find those one at a time: coverage or a fact check surfaces one,
a writer round fixes it, and the next round surfaces the next. Gr 6 SW Medisyne les 6 took
three rounds that way on 13 October 2026, each triggered by one more withdrawn form.

This sweep puts them on one page instead. On its first run over two lessons it found four
real violations, including an absolute the spec forbids in capitals which the draft broke
in its very next sentence.

WHAT IT DOES NOT DO, and this is the whole design. It does NOT decide whether a draft
violates a withdrawal - that is a question about meaning, and a generic withdrawn-wording
detector has been built and deleted twice in this repository because it cannot be made to
work. It lists each withdrawal and RANKS the draft's sentences by how much vocabulary they
share with it, so a person reads the likeliest first. Every ranking is a suggestion to
read, never a finding. The last line of each lesson says how many withdrawals were read,
because a sweep that reports nothing looks exactly like a sweep that read nothing.
"""
import argparse
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402

# A sentence that withdraws something, or forbids it. Measured against the 91 specs: these
# are the forms the house actually uses to retire a wording.
TERUG = re.compile(
    r"IS TERUGGETREK|TERUGGETREK EN MAG NIE|MAG NIE TERUGKOM|mag nie terugkom"
    r"|IS VERBODE|IS VERBIED|DIE ABSOLUTE VORM IS|MOENIE\b|MAG NIE\b",
    re.IGNORECASE)

# Words too common to carry signal when matching a withdrawal to a sentence.
STOP = set("""die n en van in is wat 'n om te nie dit hy sy hulle was het word kan moet
ons jy jou se vir met op as deur ook maar of daar hier toe nou al by uit oor na voor
een twee drie elke geen baie meer min soos dus want omdat sodat hierdie daardie
les lesse skryf sin vorm item kern graad""".split())


def woorde(t):
    return [w for w in re.findall(r"[a-zA-ZÀ-ſ]{4,}", t.lower()) if w not in STOP]


def sinne(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if len(s.strip()) > 12]


def sin_om(t, i, j):
    a = t.rfind(".", 0, i) + 1
    b = t.find(".", j)
    return " ".join(t[a:(b + 1) if b >= 0 else len(t)].split())


def les_sinne(les):
    """Every sentence a learner reads, with where it sits."""
    uit = []
    for i, b in enumerate(les.get("blokke") or []):
        waar = "blok %d %s" % (i, (b.get("kop") or b.get("tipe") or "")[:28])
        for t in [(b.get("teks") or "")] + list(b.get("items") or []):
            for s in sinne(t):
                uit.append((waar, s))
    return uit


def terugtrekkings(inskrywing):
    """Every withdrawal/prohibition sentence in the entry's ORDERING halves."""
    uit = []
    for k, v in inskrywing.items():
        for idx, t in enumerate(v if isinstance(v, list) else [v]):
            if not isinstance(t, str):
                continue
            g = P.eerste_rekordmerker(t)
            bo = t if g < 0 else t[:g]
            naam = k + ("[%d]" % idx if isinstance(v, list) else "")
            gesien = set()
            for m in TERUG.finditer(bo):
                s = sin_om(bo, m.start(), m.end())
                if len(s) < 30 or s in gesien:
                    continue
                gesien.add(s)
                uit.append((naam, s))
    return uit


# The house QUOTES the form it withdraws -- 'so bleek', 'nie dalk sommer daar hoort nie',
# 'suurvas', 'KIEMPIE'. That quotation is almost the whole signal, and matching the
# withdrawal sentence's general vocabulary instead is what made the first version useless:
# on one approved lesson it offered thirty pairs sharing only 'ander', 'mense', 'vallei'.
AANHALING = re.compile(r"'([^']{4,90})'|‘([^’]{4,90})’|\"([^\"]{4,90})\"")


ARTIKEL = re.compile("['\u2019]n(?=[\\s\u00a0])")
MASKER = "\u0001n"


def aanhalings(terug):
    """The forms a withdrawal quotes, which is what it is actually retiring.

    AFRIKAANS BITES HERE, TWICE, and both halves come from the indefinite article being
    written 'n with an apostrophe.

    One: a single-quote scan treats every article as an OPENING quote and returns a fragment
    beginning one word later -- "'n plek, mens of saak" came back as the quoted form 'n plek,'
    and then matched any sentence containing "'n plek". Every fragment that starts with the
    article is that artefact, never a quotation.

    Two, and worse: an article INSIDE a quoted form closes the fragment early, leaving its
    PREFIX. The withdrawn form 'die eerste antibiotikum UIT 'n LEWENDE DING wat wyd as
    medisyne gebruik is' came back as "die eerste antibiotikum UIT" -- which the CORRECTED
    sentence ("die eerste antibiotikum uit 'n skimmel ...") also carries, word for word, since
    a narrowed claim always shares its opening with the form it replaced. The sweep reported
    its strongest signal, WOORDELIK, against the one sentence that was right. So the article
    is masked before scanning and restored inside each fragment afterwards.
    """
    gemasker = ARTIKEL.sub(MASKER, terug)
    uit = []
    for m in AANHALING.finditer(gemasker):
        frag = next(g for g in m.groups() if g).strip().replace(MASKER, "'n")
        if re.match(r"^'?n\s", frag):        # the 'n article, not a quotation
            continue
        if frag.lower().strip(" .,:;") in STOP:
            continue
        if len(frag) < 5 and not frag.isupper():
            continue
        uit.append(frag)
    return uit


def rangskik(terug, kandidate, hoeveel, min_gedeel):
    """Rank draft sentences against a withdrawal. Quotations first, vocabulary only after.

    Returns (punt, waar, sin, waarom) with waarom naming WHY it is being shown, so a
    person can see at a glance whether the suggestion is worth reading.
    """
    punte = []
    frase = aanhalings(terug)
    for waar, s in kandidate:
        lae = s.lower()
        beste = None
        for f in frase:
            fl = f.lower().strip(" .,:;")
            if len(fl) < 4:
                continue
            if fl in lae:
                beste = (100 + len(fl), "dra die aangehaalde vorm WOORDELIKS: %r" % f)
                break
            fw = set(woorde(f))
            if fw:
                gedeel = fw & set(woorde(s))
                if len(gedeel) >= max(2, len(fw) - 1):
                    beste = (50 + len(gedeel),
                             "deel %d van %d woorde met die aangehaalde vorm %r"
                             % (len(gedeel), len(fw), f))
        if beste is None and not frase:
            # no quotation to go on: fall back to rare-word overlap, higher bar
            gedeel = set(woorde(terug)) & set(woorde(s))
            if len(gedeel) >= min_gedeel:
                beste = (len(gedeel), "deel %d woorde met die verbod: %s"
                         % (len(gedeel), ", ".join(sorted(gedeel)[:6])))
        if beste:
            punte.append((beste[0], waar, s, beste[1]))
    punte.sort(key=lambda r: -r[0])
    return punte[:hoeveel]


def main():
    a = argparse.ArgumentParser(
        description="Read each draft against the withdrawals its own spec records.")
    a.add_argument("--vak", required=True)
    a.add_argument("--graad", type=int, required=True)
    a.add_argument("--subonderwerp")
    a.add_argument("--les", type=int)
    a.add_argument("--kandidate", type=int, default=3,
                   help="how many draft sentences to rank per withdrawal (default 3)")
    a.add_argument("--min", type=int, default=4,
                   help="fallback only: minimum shared words when a withdrawal quotes nothing")
    g = a.parse_args()

    spesse = sorted(glob.glob(os.path.join(
        "spesifikasies", "goedgekeur", "gr%d" % g.graad, "*", "*.json")))
    gelees_spes = 0
    gelees_les = 0
    tot_terug = 0
    tot_rang = 0

    for sp_pad in spesse:
        try:
            spek = json.loads(io.open(sp_pad, encoding="utf-8").read())
        except Exception as exc:
            print("KON NIE LEES NIE: %s (%s)" % (sp_pad, exc))
            continue
        if (spek.get("vak") or "").strip().lower() != g.vak.strip().lower():
            continue
        sub = spek.get("kaps_subonderwerp") or ""
        # Match on the slug, not the raw string: the runner prints the FOLDER name
        # ('medisyne-oor-tyd-heen') and a person types that, while the spec holds the CAPS
        # wording ('Medisyne oor tyd heen'). A raw compare made this sweep read nothing at
        # all, which looks exactly like a clean sweep.
        if g.subonderwerp and P.slug(sub) != P.slug(g.subonderwerp):
            continue
        gelees_spes += 1
        for inskrywing in (spek.get("lesse") or []):
            nommer = inskrywing.get("nommer")
            if g.les and nommer != g.les:
                continue
            les_pad = None
            for kand in glob.glob(os.path.join(
                    "konsepte", "gr%d" % g.graad, "*", "*", "les-%s.json" % nommer)):
                kand = kand.replace(os.sep, "/")
                if "feite-kopie" in kand or "/spek/" in kand:
                    continue
                # the draft whose folder matches this spec's own sub-topic folder
                if os.path.basename(sp_pad)[:-5] in kand:
                    les_pad = kand
                    break
            if not les_pad or not os.path.exists(les_pad):
                continue
            les = json.loads(io.open(les_pad, encoding="utf-8").read())
            gelees_les += 1
            terugs = terugtrekkings(inskrywing)
            tot_terug += len(terugs)
            kandidate = les_sinne(les)
            print("")
            print("=" * 78)
            print("%s  les %s  status=%s" % (sub, nommer, les.get("status")))
            print("%d terugtrekking(s)/verbod(e) in die bestellende helftes, %d sin(ne) in "
                  "die konsep" % (len(terugs), len(kandidate)))
            print("=" * 78)
            stil = 0
            for naam, s in terugs:
                ranglys = rangskik(s, kandidate, g.kandidate, g.min)
                if not ranglys:
                    stil += 1
                    continue
                print("")
                print("  %s" % naam)
                print("    VERBOD/TERUGTREKKING: %s" % s[:400])
                print("    LEES HIERDIE KONSEPSINNE DAARTEEN (rangskik, nie bevind nie):")
                for n, waar, sin, waarom in ranglys:
                    tot_rang += 1
                    merk = "WOORDELIK" if n >= 100 else "dalk"
                    print("      [%-9s] %s" % (merk, waarom))
                    print("        %-26s %s" % (waar, sin[:220]))
            if stil:
                print("")
                print("  %d verbod(e) sonder enige ooreenstemmende konsepsin - hulle staan "
                      "nie hieronder nie." % stil)

    print("")
    print("-" * 78)
    print("%d spesifikasie(s) gelees, %d konsep(te) gelees, %d terugtrekking(s) gevind, "
          "%d konsepsin(ne) opgestel om te lees." % (gelees_spes, gelees_les, tot_terug,
                                                     tot_rang))
    if not gelees_les:
        print("GEEN KONSEP GELEES NIE - die veeg het niks ondersoek, en dit lyk op die oog "
              "af dieselfde as 'n skoon veeg. Gaan die --vak, --graad en --subonderwerp na.")
        return 2
    print("HIERDIE VEEG BEVIND NIKS. Sy rangskik net wat 'n mens moet lees: of 'n konsepsin")
    print("'n terugtrekking oortree, is 'n vraag oor BETEKENIS en geen patroon antwoord hom.")
    print("Lees elke verbod teen die sinne onder hom. Waar die konsep hom oortree, gaan die")
    print("regstelling deur die skrywer - en maak die hele les se lys in EEN rondte reg,")
    print("want die rede hierdie veeg bestaan, is dat hulle een-vir-een gevind is.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

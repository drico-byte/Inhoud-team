#!/usr/bin/env python3
"""
Find glossary terms that a subject defines more than one way.

A definition repeated across lessons must be repeated word for word. Two
lessons that define the same term differently teach two different things, and
neither lesson is wrong on its own -- which is why nothing catches it. The gate
reads one lesson, and the coverage checker reads one lesson against one spec
entry. Drift only exists between files, so only a sweep across files can see it.

    python bin/woordelysdrif.py
    python bin/woordelysdrif.py --vak "Natuurwetenskappe en Tegnologie" --graad 4
    python bin/woordelysdrif.py --json

The exit code is 1 when drift is found, so this can gate a commit.

It prints how many lesson files it read. That number is the claim's scope: a
clean result means nothing without it, because a sweep that reads three files
looks exactly like a sweep that found nothing.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)
sys.path.insert(0, HIER)

LES_NAAM = re.compile(r"les-\d+\.json$")


def slug(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s


def lesse(wortel):
    """Every lesson draft under a root, in path order.

    A spec extract is named `spek/les-3.json` -- the same file name as the draft
    it belongs to -- so walking for `les-<n>.json` picked up both and the count
    this tool prints came out at exactly double: 50 where 25 lessons existed.
    The comparison itself was unharmed, because an extract carries no `blokke`
    and contributed no wording to it. The number was the damage. This tool
    prints that number precisely so a reader knows how wide the claim is, and a
    doubled scope is the same lie as a narrow sweep reported as a clean one.
    """
    for gids, _, lers in os.walk(wortel):
        if os.path.basename(gids) == "spek":
            continue
        for naam in sorted(lers):
            if LES_NAAM.fullmatch(naam):
                yield os.path.join(gids, naam)


def jaarnommers():
    """(subject-slug, sub-topic-slug, lesson number) -> year number.

    A lesson draft does not carry its own place in the year; only the approved
    spec does. Without it the report cannot say which wording came first, and
    that is usually the whole argument about which one should win.
    """
    uit = {}

    # The lesson index first. Specs written before the year-numbering ruling have
    # no jaarnommer at all, and those are most of Terms 1 and 2 -- exactly the
    # lessons a drift report is about. Without this the report says "les ?" for
    # the ones it is asking someone to go and fix.
    for naam in sorted(os.listdir(os.path.join(REPO, "kaps", "lesindeks"))
                       if os.path.isdir(os.path.join(REPO, "kaps", "lesindeks")) else []):
        if not naam.endswith(".json"):
            continue
        try:
            with open(os.path.join(REPO, "kaps", "lesindeks", naam), encoding="utf-8") as fh:
                idx = json.load(fh)
        except (OSError, ValueError):
            continue
        vak = slug(idx.get("vak") or "")
        for e in idx.get("lesse", []):
            if e.get("subonderwerp") and e.get("les") and e.get("nommer"):
                uit[(vak, slug(e["subonderwerp"]), int(e["les"]))] = e["nommer"]

    for gids, _, lers in os.walk(os.path.join(REPO, "spesifikasies")):
        for naam in lers:
            if not naam.endswith(".json") or naam.endswith(".feite.json"):
                continue
            try:
                with open(os.path.join(gids, naam), encoding="utf-8") as fh:
                    spek = json.load(fh)
            except (OSError, ValueError):
                continue
            vak = slug(spek.get("vak") or "")
            sub = os.path.splitext(naam)[0]
            for les in spek.get("lesse", []):
                if les.get("nommer") and les.get("jaarnommer"):
                    uit[(vak, sub, int(les["nommer"]))] = les["jaarnommer"]
    return uit


def versamel(wortel, jare):
    """term -> {definition -> [(path, status, year number)]}"""
    terme = defaultdict(lambda: defaultdict(list))
    gelees = 0
    for pad in lesse(wortel):
        try:
            with open(pad, encoding="utf-8") as fh:
                les = json.load(fh)
        except (OSError, ValueError) as e:
            print(f"  kon nie lees nie: {pad} ({e})", file=sys.stderr)
            continue
        gelees += 1
        for b in les.get("blokke", []):
            if b.get("tipe") != "begrip":
                continue
            term = (b.get("term") or "").strip()
            teks = (b.get("teks") or "").strip()
            if not term or not teks:
                continue
            sleutel = (slug(les.get("vak") or ""),
                       os.path.basename(os.path.dirname(pad)),
                       int(re.search(r"les-(\d+)", os.path.basename(pad)).group(1)))
            terme[term.lower()][teks].append(
                (os.path.relpath(pad, REPO),
                 les.get("status"),
                 les.get("jaarnommer") or jare.get(sleutel)))
    return terme, gelees


def romp(teks):
    """The part of a definition before its examples.

    Drico ruled on 28 August 2026 that the examples after `soos` may differ per
    lesson -- lesson 9 gives wood, water and air because it teaches the three
    states, lesson 14 gives paper, wood and clay because it folds paper, and both
    are that lesson's own material. What must match is the sentence itself.
    """
    return re.split(r",?\s+soos\s+", teks, maxsplit=1)[0].rstrip(" .,")


def ooreengekome(vak=None, graad=None):
    """The one wording per term that a subject has settled on.

    Kept for the whole subject rather than per specification, because three of
    these terms cross sub-topics -- `materiaal` appears in lessons 8, 9 and 14,
    which are three different specifications -- and a field in one of them cannot
    state a rule about the subject.

    One file per subject-grade, matched on its own `vak` and `graad` rather than
    on its name: Natuurwetenskappe wrote kaps/gedeelde-omskrywings.json before
    there was a second subject, so the name says nothing about whose wordings are
    inside.

    Returns the terms AND which files were read. A sweep that loaded no decision
    list at all prints exactly like a sweep against a list that agreed with every
    lesson, and that is the same failure the lesson count exists to prevent.
    """
    terme, bronne = {}, []
    gids = os.path.join(REPO, "kaps")
    for naam in sorted(os.listdir(gids) if os.path.isdir(gids) else []):
        if not (naam.startswith("gedeelde-omskrywings") and naam.endswith(".json")):
            continue
        try:
            with open(os.path.join(gids, naam), encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        if vak and slug(d.get("vak") or "") != slug(vak):
            continue
        if graad and int(d.get("graad", -1)) != int(graad):
            continue
        bronne.append(f"{d.get('vak')} Gr {d.get('graad')} ({naam})")
        terme.update(d.get("terme") or {})
    return terme, bronne


def main():
    ap = argparse.ArgumentParser(
        description="Find glossary terms defined more than one way")
    ap.add_argument("--vak", help="limit to one subject")
    ap.add_argument("--graad", type=int, help="limit to one grade")
    ap.add_argument("--json", action="store_true", dest="as_json")
    a = ap.parse_args()

    wortel = os.path.join(REPO, "konsepte")
    if a.graad:
        wortel = os.path.join(wortel, f"gr{a.graad}")
    if a.vak:
        if not a.graad:
            ap.error("--vak needs --graad, because the tree is grade-first")
        wortel = os.path.join(wortel, slug(a.vak))
    if not os.path.isdir(wortel):
        sys.exit(f"no such tree: {os.path.relpath(wortel, REPO)}")

    terme, gelees = versamel(wortel, jaarnommers())
    gedeel = {t: d for t, d in terme.items() if sum(len(v) for v in d.values()) > 1}
    besluite_vroeg, besluit_bronne = ooreengekome(a.vak, a.graad)
    def eenders(term, a_, b_):
        if besluite_vroeg.get(term, {}).get("voorbeelde_mag_verskil"):
            return romp(a_) == romp(b_)
        return a_ == b_

    drif = {}
    for t, d in gedeel.items():
        vorme = list(d)
        if any(not eenders(t, vorme[0], v) for v in vorme[1:]):
            drif[t] = d

    # A settled wording turns "these two disagree" into "this one is wrong", which
    # is a different and more useful thing to be told: without it the report says
    # a term drifts and leaves the reader to work out which copy to trust, and
    # that is the step where a third wording gets invented.
    besluite = besluite_vroeg
    teen_besluit = {}
    for term, inskrywing in besluite.items():
        reg = inskrywing.get("omskrywing")
        if not reg or term not in terme:
            continue
        if inskrywing.get("voorbeelde_mag_verskil"):
            verkeerd = {teks: waar for teks, waar in terme[term].items()
                        if romp(teks) != romp(reg)}
        else:
            verkeerd = {teks: waar for teks, waar in terme[term].items() if teks != reg}
        if verkeerd:
            teen_besluit[term] = (reg, verkeerd)

    if a.as_json:
        json.dump({
            "wortel": os.path.relpath(wortel, REPO),
            "lesse_gelees": gelees,
            "terme_totaal": len(terme),
            "terme_gedeel": len(gedeel),
            "drif": {t: [{"teks": k, "lesse": [p for p, _, _ in v]}
                         for k, v in d.items()] for t, d in drif.items()},
        }, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 1 if drif else 0

    kop = f"Woordelysdrif - {os.path.relpath(wortel, REPO)}"
    print(kop)
    print("-" * len(kop))
    print(f"  {gelees} lesse gelees, {len(terme)} terme, "
          f"{len(gedeel)} daarvan in meer as een les")
    if besluit_bronne:
        print(f"  besliste bewoordings gelees uit: {'; '.join(besluit_bronne)}")
    else:
        print("  GEEN besliste-bewoordingslys gelaai nie - hierdie sweep kan net "
              "lesse teen mekaar toets,")
        print("  nie teen 'n beslissing nie.")
    print()

    if not gedeel:
        # Not a pass. Nothing was compared, and that reads the same as a pass
        # unless it says so.
        print("  Geen term kom in meer as een les voor, dus is niks vergelyk nie.")
        print("  Dit is nie 'n skoon toets nie; daar was net niks om te toets nie.")
        return 0

    # A term whose wording is still undecided is not a clean result, and it will
    # not show as drift once the lessons happen to agree on a wording that was
    # itself rejected -- which is exactly what happened to `geraamte`: both
    # candidates were wrong, one lesson was moved onto the other, and the sweep
    # went quiet. A clean report that hides an open decision is the failure this
    # whole file exists to prevent.
    oop = {t: v for t, v in besluite.items()
           if not v.get("omskrywing") and t in terme}
    if oop:
        print(f"BESLISSING NOG OOP ({len(oop)}):")
        print()
        for term in sorted(oop):
            print(f"  {term}")
            for teks, waar in sorted(terme[term].items()):
                for _, status, jaar in sorted(waar, key=lambda w: (w[2] or 10**6,)):
                    merk = "afgelewer" if status == "goedgekeur" else (status or "?")
                    print(f'     les {jaar or "?"} ({merk}) "{teks}"')
            rede = oop[term].get("WAG_OP_DRICO") or ""
            if rede:
                print(f"     -> {rede[:150]}...")
            print()

    if teen_besluit:
        print(f"TEEN 'N BESLISTE BEWOORDING ({len(teen_besluit)}):")
        print()
        for term in sorted(teen_besluit):
            reg, verkeerd = teen_besluit[term]
            print(f"  {term}")
            print(f'     REG:  "{reg}"')
            for teks, waar in sorted(verkeerd.items()):
                for pad_, status, jaar in sorted(waar, key=lambda w: (w[2] or 10**6, w[0])):
                    merk = "afgelewer" if status == "goedgekeur" else (status or "?")
                    print(f'     nie:  les {jaar or "?"} ({merk}) "{teks}"')
            print()

    if not drif:
        if not teen_besluit and not oop:
            print(f"  Geen drif. Al {len(gedeel)} gedeelde terme is woord vir woord")
            print(f"  dieselfde oor die {gelees} lesse wat gelees is.")
            return 0
        if not teen_besluit:
            print(f"Geen les weerspreek 'n ander nie, maar {len(oop)} bewoording(s) is nog nie besluit nie.")
            return 1
        print("Geen les weerspreek 'n ander nie; die bogenoemde weerspreek 'n beslissing.")
        return 1

    for term in sorted(drif):
        print(f"DRIF: {term}")
        def eerste(item):
            jare_hier = [j for _, _, j in item[1] if j]
            return (min(jare_hier) if jare_hier else 10**6, item[0])
        for teks, waar in sorted(drif[term].items(), key=eerste):
            print(f'   "{teks}"')
            for pad, status, jaar in sorted(waar, key=lambda w: (w[2] or 10**6, w[0])):
                merk = "afgelewer" if status == "goedgekeur" else (status or "?")
                nommer = f"les {jaar}" if jaar else "?"
                print(f"       {nommer:<8} {merk:<12} {pad}")
        print()

    print(f"{len(drif)} van die {len(gedeel)} gedeelde terme dryf uiteen.")
    if besluite:
        beslis = sum(1 for t in drif if t in besluite)
        print(f"{beslis} daarvan het reeds 'n besliste bewoording "
              f"(sien {'; '.join(besluit_bronne)});")
        print("vir die res moet een bewoording wen. 'n Derde bewoording maak dit erger.")
    else:
        print("Een bewoording moet wen. 'n Derde bewoording maak dit erger.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

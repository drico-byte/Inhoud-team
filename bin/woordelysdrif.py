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
    """Every lesson draft under a root, in path order."""
    for gids, _, lers in os.walk(wortel):
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
    drif = {t: d for t, d in gedeel.items() if len(d) > 1}

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
    print()

    if not gedeel:
        # Not a pass. Nothing was compared, and that reads the same as a pass
        # unless it says so.
        print("  Geen term kom in meer as een les voor, dus is niks vergelyk nie.")
        print("  Dit is nie 'n skoon toets nie; daar was net niks om te toets nie.")
        return 0

    if not drif:
        print(f"  Geen drif. Al {len(gedeel)} gedeelde terme is woord vir woord")
        print(f"  dieselfde oor die {gelees} lesse wat gelees is.")
        return 0

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
    print("Een bewoording moet wen. 'n Derde bewoording maak dit erger.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

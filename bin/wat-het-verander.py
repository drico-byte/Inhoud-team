#!/usr/bin/env python3
"""
What changed in each lesson since a given commit, in the terms a person cares about.

`git diff` shows JSON. This shows sentences: which glossary entries changed and
from what to what, and which study-text sentences moved. It exists because the
layout team already holds some of these lessons and needs a correction sheet per
lesson, not a patch.

    python bin/wat-het-verander.py --sedert fbb6916
    python bin/wat-het-verander.py --sedert fbb6916 --lesse 1-5
"""
import argparse, json, os, re, subprocess, sys, unicodedata

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)


def slug(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def by_year():
    idx = json.load(open(os.path.join(REPO, "kaps", "lesindeks",
                                      "gr4-natuurwetenskappe-en-tegnologie.json"),
                         encoding="utf-8"))
    uit = {}
    for e in idx["lesse"]:
        uit[e["nommer"]] = (
            f"konsepte/gr4/natuurwetenskappe-en-tegnologie/"
            f"{slug(e['subonderwerp'])}/les-{e['les']}.json", e["etiket"])
    return uit


def by_ref(pad, ref):
    r = subprocess.run(["git", "show", f"{ref}:{pad}"], cwd=REPO,
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except ValueError:
        return None


def begrippe(les):
    return {b["term"]: b.get("teks", "")
            for b in (les or {}).get("blokke", []) if b.get("tipe") == "begrip"}


def sinne(les):
    """Study and list sentences, keyed by the block they sit in."""
    uit = {}
    for b in (les or {}).get("blokke", []):
        if b.get("tipe") == "begrip":
            continue
        kop = b.get("kop") or b.get("vir") or b.get("tipe")
        dele = []
        if b.get("teks"):
            dele += [s.strip() for s in re.split(r"(?<=\.)\s+", b["teks"]) if s.strip()]
        dele += [i.strip() for i in (b.get("items") or []) if str(i).strip()]
        uit[kop] = dele
    return uit


def main():
    ap = argparse.ArgumentParser(description="What changed per lesson, in sentences")
    ap.add_argument("--sedert", required=True, help="baseline commit")
    ap.add_argument("--lesse", help="e.g. 1-5 or 1,4,9")
    a = ap.parse_args()

    wil = None
    if a.lesse:
        wil = set()
        for stuk in a.lesse.split(","):
            if "-" in stuk:
                lo, hi = stuk.split("-")
                wil |= set(range(int(lo), int(hi) + 1))
            else:
                wil.add(int(stuk))

    jare = by_year()
    onveranderd, verander = [], []

    for n in sorted(jare):
        if wil and n not in wil:
            continue
        pad, etiket = jare[n]
        vol = os.path.join(REPO, pad)
        if not os.path.exists(vol):
            continue
        nuut = json.load(open(vol, encoding="utf-8"))
        oud = by_ref(pad, a.sedert)
        if oud is None:
            verander.append((n, etiket, [("(nuwe leer)", "", "")], []))
            continue

        b_oud, b_nuut = begrippe(oud), begrippe(nuut)
        wysigings = []
        for term in sorted(set(b_oud) | set(b_nuut)):
            o, w = b_oud.get(term), b_nuut.get(term)
            if o != w:
                wysigings.append((term, o, w))

        s_oud, s_nuut = sinne(oud), sinne(nuut)
        sinwysigings = []
        for kop in s_nuut:
            weg = [s for s in s_oud.get(kop, []) if s not in s_nuut[kop]]
            by = [s for s in s_nuut[kop] if s not in s_oud.get(kop, [])]
            for i in range(max(len(weg), len(by))):
                sinwysigings.append((kop,
                                     weg[i] if i < len(weg) else None,
                                     by[i] if i < len(by) else None))

        (verander if (wysigings or sinwysigings) else onveranderd).append(
            (n, etiket, wysigings, sinwysigings))

    print(f"Wat het verander sedert {a.sedert}")
    print("=" * 60)
    print()
    if onveranderd:
        print(f"ONVERANDERD ({len(onveranderd)}):")
        for n, etiket, _, _ in onveranderd:
            print(f"   les {n:<3} {etiket}")
        print()
    if not verander:
        print("Niks het verander nie.")
        return 0

    print(f"VERANDER ({len(verander)}):")
    print()
    for n, etiket, wysigings, sinwysigings in verander:
        print(f"  LES {n} - {etiket}")
        for term, o, w in wysigings:
            print(f"     woordelys: {term}")
            if o is not None:
                print(f'        - "{o}"')
            if w is not None:
                print(f'        + "{w}"')
        for kop, weg, by in sinwysigings:
            print(f"     teks in blok: {kop}")
            if weg:
                print(f'        - "{weg}"')
            if by:
                print(f'        + "{by}"')
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())

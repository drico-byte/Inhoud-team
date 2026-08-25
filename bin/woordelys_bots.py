#!/usr/bin/env python3
"""Report terms that two lessons in one sub-topic define DIFFERENTLY.

    python bin/woordelys_bots.py konsepte/gr4/<vak>/<subonderwerp>
    python bin/woordelys_bots.py --alles

Repeating a definition across lessons is correct and expected: each lesson has to
stand alone as a revision instrument, so a learner revising lesson 2 must not have
to go and fetch lesson 1 for a word it uses. What is NOT correct is defining the
same word two different ways inside one sub-topic.

That happened on Term 2 lessons 14 and 15 with the word 'struktuur', and nothing
caught it. Each checker reads one lesson. The coverage checker can open a sibling
when told to, but nothing compares two finished lessons as a matter of course, so
the drift was found by accident and cost a revision round.

This does not judge which wording is right, and it is not part of the gate. It
prints what differs and leaves the decision to a person. Exit code is always 0 for
a clean read; a difference is reported, not enforced.
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def begrippe(les_pad):
    """Every term this lesson defines, as {term: text}."""
    uit = {}
    try:
        les = json.load(open(les_pad, encoding="utf-8"))
    except (OSError, ValueError):
        return uit
    for blok in les.get("blokke", []):
        if blok.get("tipe") != "begrip":
            continue
        for ins in blok.get("inskrywings") or [blok]:
            term = (ins.get("term") or "").strip()
            teks = (ins.get("teks") or "").strip()
            if term and teks:
                uit.setdefault(term, {})[os.path.basename(les_pad)] = teks
    return uit


def vergelyk(gids):
    lesse = sorted(f for f in os.listdir(gids)
                   if f.startswith("les-") and f.endswith(".json")
                   and "." not in f[len("les-"):-len(".json")])
    saam = {}
    for naam in lesse:
        for term, per_les in begrippe(os.path.join(gids, naam)).items():
            saam.setdefault(term, {}).update(per_les)

    botsings = {t: v for t, v in saam.items()
                if len(v) > 1 and len(set(v.values())) > 1}

    # A difference a person has looked at and accepted stays out of the report.
    # Two known cases would otherwise print on every run, and the whole value of
    # this check is that a real drift stands out rather than blending into a list
    # of ones already ruled on.
    for t in aanvaar_vir(os.path.basename(gids)):
        botsings.pop(t, None)
    return lesse, saam, botsings


def aanvaar_vir(subonderwerp):
    """Terms accepted as legitimately worded differently in this sub-topic."""
    pad = os.path.join(REPO, "kaps", "aanvaarde-woordelysverskille.json")
    try:
        data = json.load(open(pad, encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    return {x["term"] for x in data.get("aanvaar", [])
            if x.get("subonderwerp") == subonderwerp}


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__.strip())
        return 0

    if argv[0] == "--alles":
        gidse = []
        # Walk only directories. konsepte/ carries a .gitkeep, and any stray file
        # at any level would otherwise crash the sweep rather than be skipped.
        wortel = os.path.join(REPO, "konsepte")
        for graad in sorted(os.listdir(wortel)):
            gpad = os.path.join(wortel, graad)
            if not os.path.isdir(gpad):
                continue
            for vak in sorted(os.listdir(gpad)):
                vpad = os.path.join(gpad, vak)
                if not os.path.isdir(vpad):
                    continue
                for sub in sorted(os.listdir(vpad)):
                    if os.path.isdir(os.path.join(vpad, sub)):
                        gidse.append(os.path.join(vpad, sub))
    else:
        gidse = [os.path.abspath(argv[0])]

    totaal = 0
    for gids in gidse:
        if not os.path.isdir(gids):
            print(f"not a directory: {gids}")
            return 1
        lesse, saam, botsings = vergelyk(gids)
        if len(lesse) < 2:
            continue
        naam = os.path.relpath(gids, REPO).replace(os.sep, "/")
        if not botsings:
            gedeel = sum(1 for v in saam.values() if len(v) > 1)
            print(f"ok    {naam}  ({len(lesse)} lessons, {gedeel} term(s) shared, all worded alike)")
            continue
        totaal += len(botsings)
        print(f"DIFFERS  {naam}")
        for term, per_les in sorted(botsings.items()):
            print(f"    '{term}' is defined {len(set(per_les.values()))} different ways:")
            for les, teks in sorted(per_les.items()):
                print(f"      {les}  {teks}")
        print()

    if totaal:
        print(f"{totaal} term(s) worded differently across lessons in the same sub-topic.")
        print("Repeating a definition is correct. Disagreeing is not. Decide which")
        print("wording is right, put it in the spec, and revise both lessons.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

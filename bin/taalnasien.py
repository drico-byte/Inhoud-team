#!/usr/bin/env python3
"""
Build a paste-ready block for an outside language checker.

The language checking is done elsewhere, by a tool with better Afrikaans than
ours. That tool must not undo decisions this pipeline paid for: a word like
`energie` where `krag` reads more naturally, a spelling like `ungquphantsi` that
looks like a typo, a phrase like `die meeste` where `byna elke` is smoother. Each
of those is a correction a fluent reader would make, and each would put back an
error a fact checker found.

So this prints three things, in the order the checker needs them: what it is
being asked to do, what it may not touch and why, and the lesson itself.

Two sources of protection, and they work differently:

  * kaps/beskermde-woorde.json  -- decisions written down by hand, filtered to
    the ones whose words actually appear in this lesson, so the list stays short
    enough to be read.

  * every glossary entry this lesson shares with another lesson -- found by
    reading the other lessons, not by trusting a list. A definition repeated
    across lessons must stay identical, and a language checker improving one
    copy silently breaks the pair.

USAGE
    python bin/taalnasien.py --vak "Natuurwetenskappe en Tegnologie" --graad 4 \
        --subonderwerp "Vaste stowwe" --les 2
    python bin/taalnasien.py --les-pad konsepte/gr4/.../les-2.json
"""

import argparse, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)
sys.path.insert(0, HIER)


def lees_json(pad):
    with open(pad, encoding="utf-8") as fh:
        return json.load(fh)


def lesteks(les):
    """Every word a language checker would read, block by block."""
    dele = []
    for b in les.get("blokke", []):
        kop = (b.get("kop") or b.get("term") or b.get("vir") or "").strip()
        teks = (b.get("teks") or "").strip()
        if kop and teks:
            dele.append(f"[{b.get('tipe')}] {kop}\n{teks}")
        elif teks:
            dele.append(f"[{b.get('tipe')}]\n{teks}")
    return "\n\n".join(dele)


def beskermde_woorde(les, sub_gids):
    """Hand-recorded rulings, kept only where the word is really in this lesson."""
    pad = os.path.join(REPO, "kaps", "beskermde-woorde.json")
    if not os.path.exists(pad):
        return []
    data = lees_json(pad)
    blob = lesteks(les).lower()

    uit = []
    for inskrywing in data.get("algemeen", []):
        if inskrywing["hou"].lower() in blob:
            uit.append(inskrywing)
    for inskrywing in data.get("per_subonderwerp", {}).get(sub_gids, []):
        # A wording is kept even when only part of it appears, because the
        # protected thing is often a whole sentence the checker would reword.
        kern = inskrywing["hou"].lower().rstrip(".")
        if kern in blob or kern.split()[0] in blob:
            uit.append(inskrywing)
    return uit


def gedeelde_verklarings(les, les_pad):
    """Glossary entries this lesson shares with any other lesson in the subject.

    Read from the other lessons rather than declared anywhere, so a pair that
    was made to match yesterday is protected today without anyone listing it.
    """
    vak_wortel = os.path.dirname(os.path.dirname(les_pad))   # .../<vak>/
    myne = {b["term"]: b.get("teks", "")
            for b in les.get("blokke", []) if b.get("tipe") == "begrip"}
    if not myne:
        return []

    elders = {}
    for gids, _, lers in os.walk(vak_wortel):
        for naam in lers:
            if not re.fullmatch(r"les-\d+\.json", naam):
                continue
            ander_pad = os.path.join(gids, naam)
            if os.path.abspath(ander_pad) == os.path.abspath(les_pad):
                continue
            try:
                ander = lees_json(ander_pad)
            except Exception:
                continue
            for b in ander.get("blokke", []):
                if b.get("tipe") == "begrip" and b.get("term") in myne:
                    elders.setdefault(b["term"], set()).add(
                        os.path.basename(os.path.dirname(ander_pad)))

    return [(t, myne[t], sorted(waar)) for t, waar in sorted(elders.items())]


OPDRAG = """Jy doen 'n TAALNASIEN op 'n Afrikaanse Graad 4-les. Jou werk is grammatika,
idioom en direkte-vertaling-foute. Die inhoud, die feite en die struktuur is
klaar nagegaan deur ander nasieners en is nie jou werk nie.

Twee reels:

1. Moenie 'n woord verander wat hieronder as BESKERM gelys is nie. Elkeen van
   hulle lees soos gewone Afrikaans wat verbeter kan word, en elkeen is 'n
   besluit wat iewers geld gekos het. Die rede staan daarby. As jy meen 'n
   beskermde woord is werklik verkeerd, SE dit apart eerder as om dit te
   verander.

2. Verander niks aan die betekenis nie. As 'n sin taalkundig lam is omdat hy
   feitelik presies moet wees, se dit eerder as om hom gladder te maak.

Gee jou antwoord as 'n lys veranderings - ou sin, nuwe sin - nie as 'n
herskrewe les nie."""


def bou(les_pad):
    les = lees_json(les_pad)
    sub_gids = os.path.basename(os.path.dirname(les_pad))

    reels = []
    reels.append(OPDRAG)
    reels.append("")
    reels.append("=" * 72)
    reels.append(f"LES: {les.get('titel')}   ({les.get('vak')}, Graad {les.get('graad')})")
    reels.append("=" * 72)

    woorde = beskermde_woorde(les, sub_gids)
    gedeel = gedeelde_verklarings(les, les_pad)

    if woorde or gedeel:
        reels.append("")
        reels.append("BESKERM - moenie hierdie verander nie")
        reels.append("-" * 72)

    for w in woorde:
        nie = ", ".join(w["nie"])
        reels.append("")
        reels.append(f"  HOU:  {w['hou']}")
        if nie:
            reels.append(f"  NIE:  {nie}")
        reels.append(f"  Waarom: {w['rede']}")

    for term, teks, waar in gedeel:
        reels.append("")
        reels.append(f"  HOU WOORD VIR WOORD:  {term} - \"{teks}\"")
        reels.append(f"  Waarom: dieselfde verklaring staan ook in {', '.join(waar)}. "
                     f"'n Verbetering aan een van hulle breek die paar, en 'n toets "
                     f"oor die hele vak sal dit vlag.")

    reels.append("")
    reels.append("=" * 72)
    reels.append("DIE LES")
    reels.append("=" * 72)
    reels.append("")
    reels.append(lesteks(les))
    return "\n".join(reels)


def main():
    ap = argparse.ArgumentParser(description="Paste-ready block for an outside language checker")
    ap.add_argument("--les-pad")
    ap.add_argument("--vak")
    ap.add_argument("--graad", type=int)
    ap.add_argument("--subonderwerp")
    ap.add_argument("--les", type=int)
    ap.add_argument("--uit", help="write to this file instead of the screen")
    a = ap.parse_args()

    if a.les_pad:
        pad = a.les_pad
    else:
        if not (a.vak and a.graad and a.subonderwerp and a.les):
            ap.error("give --les-pad, or all of --vak --graad --subonderwerp --les")
        import paaie as P                                    # noqa: E402
        pad = P.les_konsep(a.graad, a.vak, a.subonderwerp, a.les)

    if not os.path.exists(pad):
        sys.exit(f"no lesson at {pad}")

    blok = bou(pad)
    if a.uit:
        with open(a.uit, "w", encoding="utf-8") as fh:
            fh.write(blok)
        print(f"written to {a.uit}")
    else:
        print(blok)


if __name__ == "__main__":
    main()

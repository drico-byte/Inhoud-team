#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Find spec fields that still prescribe a wording the grade has since replaced.

The failure this exists for, three times in one day:

A term is defined in the previous grade and inherited. A fact check contradicts
that inherited sentence, so the grade gets its own wording and the specs are
swept. But a spec states the same rule in several fields -- the wording itself,
a status line under it, a note to the person who owns the work, a glossary-
density note, a kern item -- and the sweep reaches one of them. Every other
field still orders the contradicted sentence, word for word, and the next
revision brings it back. Nothing in the per-lesson pipeline can see this: the
gate reads one lesson, coverage reads one lesson against one spec entry, and the
drift sweep only compares lessons to each other, so it goes quiet the moment the
lessons agree -- including when they agree on the wording that was rejected.

So: for every term where this grade's agreed wording differs from the previous
grade's, search every spec for the OLD sentence and report each field that still
carries it without a dated correction on its opening line.

It reports; it does not edit. What to do about each hit is a judgement -- a field
QUOTING the old wording as history is right to keep it, and a field ORDERING it
is not, and only a person reading the sentence can tell those apart.

    python bin/ouwoordveeg.py --vak "<subject>" --graad 5
"""
import argparse
import glob
import io
import json
import os
import re
import sys

# A dated correction always opens with one of these.
GEMERK = ("REGGEMAAK", "HERSKRYF", "BYGEVOEG", "UITGEBREI", "LET WEL",
          "GEMERK", "GEOPEN", "HERBEVESTIG", "VERSKUIF", "OORTREFDE")

# A field may instead say inline that it is holding the old wording on purpose.
INLYN = re.compile(r"VERVANG VIR GRAAD|MOENIE HIERDIE BEWOORDING|REKORD, NIE 'N BESTELLING|"
                   r"as GESKIEDENIS|as rekord|OORTREFDE TEKS", re.I)


def lees(pad):
    with io.open(pad, encoding="utf-8") as f:
        return json.load(f)


def lyste_vir(vak, graad):
    """This grade's agreed-wordings file and the previous grade's, found by their
    own vak/graad fields rather than by filename -- the first subject to be written
    named its file before there was a second subject."""
    hierdie = vorige = None
    for pad in glob.glob(os.path.join("kaps", "gedeelde-omskrywings*.json")):
        try:
            d = lees(pad)
        except Exception:
            continue
        if str(d.get("vak", "")).lower() not in (vak.lower(), ""):
            continue
        if d.get("graad") == graad:
            hierdie = (pad, d)
        elif d.get("graad") == graad - 1:
            vorige = (pad, d)
    return hierdie, vorige


def velde(node, pad=""):
    if isinstance(node, dict):
        for k, v in node.items():
            for r in velde(v, pad + "." + k):
                yield r
    elif isinstance(node, list):
        for i, v in enumerate(node):
            for r in velde(v, "%s[%d]" % (pad, i)):
                yield r
    elif isinstance(node, str):
        yield pad.lstrip("."), node


def normaliseer(s):
    s = s.replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", s).strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--vak", required=True)
    p.add_argument("--graad", type=int, required=True)
    a = p.parse_args()

    hierdie, vorige = lyste_vir(a.vak, a.graad)
    if not hierdie:
        sys.exit("No agreed-wordings file for %s Gr %d. A subject needs its own file, "
                 "with an empty 'terme', before its first lesson is drafted." % (a.vak, a.graad))
    if not vorige:
        print("No Grade %d list found, so there is no inherited wording to have replaced. "
              "Nothing to sweep." % (a.graad - 1))
        return

    print("this grade:     %s" % hierdie[0].replace("\\", "/"))
    print("previous grade: %s" % vorige[0].replace("\\", "/"))

    nuut = hierdie[1].get("terme", {})
    oud = vorige[1].get("terme", {})
    vervang = {}
    for term, e in nuut.items():
        if term.startswith("_"):
            continue
        nuwe_sin = normaliseer(str(e.get("omskrywing") or ""))
        ou_sin = normaliseer(str((oud.get(term) or {}).get("omskrywing") or ""))
        if nuwe_sin and ou_sin and nuwe_sin != ou_sin:
            vervang[term] = ou_sin

    if not vervang:
        print("\nNo term in this grade replaces a Grade %d wording. Nothing to sweep."
              % (a.graad - 1))
        return

    print("\n%d term(s) whose Grade %d wording this grade replaced: %s"
          % (len(vervang), a.graad - 1, ", ".join(sorted(vervang))))

    vakgids = a.vak.lower().replace(" ", "-")
    spekke = sorted(glob.glob(os.path.join(
        "spesifikasies", "goedgekeur", "gr%d" % a.graad, vakgids, "*.json")))
    if not spekke:
        sys.exit("No approved specs at spesifikasies/goedgekeur/gr%d/%s/" % (a.graad, vakgids))
    print("%d approved spec(s) read\n" % len(spekke))

    lewend = gemerk = inlyn_gemerk = 0
    for spek in spekke:
        naam = os.path.basename(spek)
        try:
            d = lees(spek)
        except Exception as e:
            print("  could not read %s: %s" % (naam, e))
            continue
        for pad, teks in velde(d):
            n = normaliseer(teks)
            for term, ou_sin in sorted(vervang.items()):
                if ou_sin not in n:
                    continue
                if teks.lstrip().startswith(GEMERK):
                    gemerk += 1
                elif INLYN.search(teks):
                    # The marker is not always at the opening line. Several fields
                    # record the previous grade's wording deliberately and say so
                    # inline -- "[VERVANG VIR GRAAD 5 ...]", "REKORD, NIE 'N
                    # BESTELLING NIE". Reporting those as live buries the real
                    # faults in noise, which is how a sweep stops being read.
                    inlyn_gemerk += 1
                else:
                    lewend += 1
                    print("  LIVE  %-28s %-46s [%s]" % (naam[:28], pad[:46], term))
    print("\n%d field(s) still carry a replaced wording with no correction; "
          "%d corrected at the opening line, %d marked inline as a record."
          % (lewend, gemerk, inlyn_gemerk))
    if lewend:
        print("Read each one. A field QUOTING the old wording as history is right to keep\n"
              "it; a field ORDERING it is a spec fault that will reinstate the wording at\n"
              "the next revision. Only reading the sentence tells you which.")


if __name__ == "__main__":
    main()

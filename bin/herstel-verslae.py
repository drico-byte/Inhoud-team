#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Restore archived checker reports that still describe the current draft.

The runner archives a lesson's reports as outdated whenever it is asked about
that lesson again -- which happens every time we gate a repaired draft. Most of
those reports are then re-run from scratch, at the cost of a full checker each,
even when the draft has not moved a word since.

An archived report carries no fingerprint of the draft it read, so there is
nothing to compare hashes against. What it does carry is QUOTATIONS: a fact
report quotes the sentence it judged, a coverage report quotes the evidence it
found. If every sentence a report quotes is still present in the draft, verbatim,
the report is describing the text that is there now. If even one has moved, the
draft has been edited underneath it and the report has to be re-run.

That is the same test the standard already prescribes by hand for a report whose
agent died mid-task: diff the report's quoted sentences against the draft.

Deliberately conservative:
  * only GOEDGEKEUR is restored. An escalation or a revision request is a piece
    of unfinished business, and resurrecting one hides work rather than saving it.
  * a quotation shorter than MIN_AANHALING characters is ignored, because a short
    fragment matches by accident and would let a stale report through.
  * a report with no usable quotations at all is never restored -- there is
    nothing to verify it against, and "no evidence of change" is not evidence of
    no change.

    python bin/herstel-verslae.py --vak "<subject>" --graad 5           # report
    python bin/herstel-verslae.py --vak "<subject>" --graad 5 --skryf   # restore
"""
import argparse
import glob
import io
import json
import os
import re
import shutil
import sys

MIN_AANHALING = 40
# Text inside quote marks, straight or curly. A coverage report puts the draft's
# actual wording here and its own commentary around it.
BINNE_AANHALINGSTEKENS = re.compile("[‘’'\"“”]([^‘’'\"“”]{%d,})[‘’'\"“”]" % MIN_AANHALING)
SOORTE = {"dekking": ".dekking.json", "feite": ".feite.json"}


def lees(pad):
    try:
        with io.open(pad, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def aanhalings(node, uit):
    """Every piece of a report that is VERBATIM lesson text.

    Two shapes, and the difference matters. A fact report's 'bewering' is the
    sentence itself, copied out of the draft. A coverage report's 'bewys' is the
    checker's own prose ABOUT the draft, with the actual wording in quote marks
    inside it -- so matching the whole field can never succeed, and an earlier
    version of this script duly reported that every quotation in every lesson
    had moved, which is a result that should never be believed.

    So: take 'bewering' whole, and from every other string take only what sits
    inside quote marks.
    """
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str):
                if k == "bewering" and len(v) >= MIN_AANHALING:
                    uit.append(v)
                else:
                    uit.extend(m for m in BINNE_AANHALINGSTEKENS.findall(v)
                               if len(m) >= MIN_AANHALING)
            else:
                aanhalings(v, uit)
    elif isinstance(node, list):
        for v in node:
            aanhalings(v, uit)
    return uit


def normaliseer(s):
    """Whitespace and quote style differ between a report and a draft; wording does not."""
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def draf_teks(les):
    """All learner-facing text in a draft, as one normalised blob.

    The provenance note is excluded on purpose: it QUOTES the report's own
    findings, so including it would let a report verify itself against the
    record of its own findings rather than against the lesson.
    """
    d = lees(les)
    if d is None:
        return None
    stukke = []
    for b in d.get("blokke", []):
        for veld in ("kop", "teks", "term", "vir"):
            if isinstance(b.get(veld), str):
                stukke.append(b[veld])
        for item in b.get("items", []) or []:
            if isinstance(item, str):
                stukke.append(item)
    for veld in ("titel", "kaps_punt", "kaps_onderwerp"):
        if isinstance(d.get(veld), str):
            stukke.append(d[veld])
    return normaliseer(" ".join(stukke))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--vak", required=True)
    p.add_argument("--graad", type=int, required=True)
    p.add_argument("--skryf", action="store_true", help="restore; otherwise report only")
    a = p.parse_args()

    vakgids = a.vak.lower().replace(" ", "-")
    wortel = os.path.join("konsepte", "gr%d" % a.graad, vakgids)
    logwortel = os.path.join("logs", "verslae", "gr%d" % a.graad, vakgids)
    if not os.path.isdir(wortel):
        sys.exit("No lessons at %s" % wortel)

    herstel = geblok = geen_bewys = reeds = 0
    for argief in sorted(glob.glob(os.path.join(logwortel, "*", "les-*", "*-verouderd.json"))):
        deel = argief.replace("\\", "/").split("/")
        sub, lesgids = deel[-3], deel[-2]
        soort = os.path.basename(argief).split("-")[1]
        if soort not in SOORTE:
            continue
        les = os.path.join(wortel, sub, lesgids + ".json")
        doel = os.path.join(wortel, sub, lesgids + SOORTE[soort])
        if not os.path.exists(les):
            continue
        if os.path.exists(doel):
            reeds += 1
            continue

        verslag = lees(argief)
        if verslag is None:
            continue
        verdict = str(verslag.get("verdict") or "")
        if verdict != "GOEDGEKEUR":
            geblok += 1
            continue

        teks = draf_teks(les)
        quotes = [q for q in aanhalings(verslag, []) if teks is not None]
        if not quotes:
            geen_bewys += 1
            print("  no quotations   %-30s %-6s %-8s - cannot verify, left for a re-check"
                  % (sub[:30], lesgids, soort))
            continue

        mis = [q for q in quotes if normaliseer(q) not in teks]
        if mis:
            geblok += 1
            print("  draft moved     %-30s %-6s %-8s - %d of %d quotations no longer in the draft"
                  % (sub[:30], lesgids, soort, len(mis), len(quotes)))
            continue

        print("  RESTORE         %-30s %-6s %-8s - all %d quotations still present, %s"
              % (sub[:30], lesgids, soort, len(quotes), verdict))
        if a.skryf:
            shutil.copy(argief, doel)
        herstel += 1

    print("\n%d restorable, %d already live, %d left for a re-check, %d unverifiable"
          % (herstel, reeds, geblok, geen_bewys))
    if herstel and not a.skryf:
        print("Nothing was written. Re-run with --skryf to restore.")


if __name__ == "__main__":
    main()

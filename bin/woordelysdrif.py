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

    IT HAPPENED AGAIN, 10 September 2026, in a new costume. `feite-kopie/les-3.json`
    is the copy handed to the fact checker with the provenance note stripped, added
    on 9 September -- same file name again, so the sweep read 42 where 29 lessons
    existed. The exclusion is now a LIST rather than one name, because the next
    directory that mirrors these file names will do this a third time.

    `feite-kopie/les-3.json` is the same fault in a different costume, and a
    worse one. That directory was added later to hand the fact checker a draft
    without its provenance note, so unlike an extract it DOES carry `blokke` --
    it is the lesson, minus one field. It therefore corrupted the comparison
    and not merely the count: the runner regenerates it, so a lesson revised
    since its last runner call has a copy of its own OLD glossary sitting
    beside it, and this tool reported the lesson as drifting against itself.
    One such phantom was reported on 16 September 2026. Skip any directory
    whose files are copies of lessons rather than lessons.
    """
    HERHALINGS = ("spek", "feite-kopie")   # both hold files named les-<n>.json
    for gids, _, lers in os.walk(wortel):
        if os.path.basename(gids) in HERHALINGS:
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


def etiket(pad, jaar):
    """A name a person can act on.

    The year number is the best label, because it says which wording came first --
    but a subject whose specs carry no `jaarnommer`, and which has no lesson index,
    then prints every row as "les ?". That is the one thing the row is for. So fall
    back to the sub-topic and the lesson's own number, taken from the path.
    """
    if jaar:
        return "les %s" % jaar
    deel = os.path.normpath(pad).split(os.sep)
    nommer = re.sub(r"^les-|\.json$", "", deel[-1]) if deel else "?"
    sub = deel[-2] if len(deel) > 1 else ""
    kort = "".join(w[0] for w in sub.split("-") if w)[:4].upper()
    return "%s les %s" % (kort, nommer) if kort else "les %s" % nommer


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


def besliste_betekenisse(inskrywing):
    """The decided sentences of a term that deliberately carries more than one.

    A `twee_betekenisse` entry records its senses one of two ways, and the
    difference decides whether a lesson can be checked against them at all:

      * STRUCTURED -- a `betekenisse` list of {"wanneer": ..., "sin": ...}, where
        each `sin` is a wording a lesson must reproduce verbatim, exactly as a
        single-meaning entry's `omskrywing` is. `hof` in Sosiale Wetenskappe Gr 6
        is written this way: a law court and a ruler's court, two list entries.
      * PROSE ONLY -- the senses are quoted inside a free `nota`, which is how
        `konflik`, `verhouding` and `as` are written. There is no field there a
        comparison could stand on: the note runs the wordings together with the
        reason, the ruling, the history and sometimes a withdrawn candidate, and
        `as` even carries `nog_nie_beslis`. Pulling a sentence out of that prose
        would be guessing which quotation is the live one.

    Returns a list of (when, sentence), or None where the entry keeps its senses
    in prose. None means NOT COMPARABLE, and the report says so out loud rather
    than passing over it -- a term nothing was compared for must never print the
    same as a term that was compared and matched.
    """
    uit = []
    for b in inskrywing.get("betekenisse") or []:
        if isinstance(b, dict) and (b.get("sin") or "").strip():
            uit.append(((b.get("wanneer") or "?").strip(), b["sin"].strip()))
    return uit or None


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

    # A term marked `twee_betekenisse` is one word with two meanings that must NOT
    # be made to agree ('as': a wheel's axle, and the Earth's axis, which is a line
    # that does not exist). Drico confirmed on 18 September 2026 that each lesson
    # keeps its own. Reporting it as drift every run invites someone to "fix" it.
    twee = sorted(t for t, v in besluite_vroeg.items()
                  if v.get("twee_betekenisse") and t in gedeel)
    drif = {}
    for t, d in gedeel.items():
        if t in twee:
            continue
        vorme = list(d)
        if any(not eenders(t, vorme[0], v) for v in vorme[1:]):
            drif[t] = d

    # THE HOLE THIS CLOSED, 1 October 2026, and it had swallowed a term whole.
    # `twee_betekenisse` suppressed the term from the drift loop above, which is
    # right. But it fell out of the other two reports as well, and nobody noticed
    # that the exemption had become total:
    #
    #   * the `omskrywing` comparison below starts `if not reg ... continue`, and a
    #     two-meaning entry's `omskrywing` is ALWAYS empty -- its wordings live in
    #     `betekenisse` instead, which nothing read;
    #   * the `oop` report excludes `twee_betekenisse` by name, so it did not even
    #     show up as an open decision.
    #
    # Three paths, and the term fell through all three: NOTHING was ever compared
    # for it, while the summary said only "nie as drif getel nie" -- which a reader
    # takes for "checked, and fine". Demokrasie les 2 carried the SECOND withdrawn
    # form of `hof`, the one using `reg` in the law sense that had been ruled out
    # that same day, and the sweep printed its clean line over the top of it. A
    # writer found it by reading.
    #
    # What the exemption is FOR is legitimate: two LESSONS may use different senses
    # and must not be made to agree. What it must not do is excuse a lesson from
    # matching any decided sense at all. So a lesson's entry is now compared against
    # that term's decided senses and must reproduce ONE of them verbatim; matching
    # none is drift and is reported. A term whose senses are only in prose cannot be
    # compared, and is listed as not compared rather than counted as clean.
    #
    # A SECOND HOLE, FOUND IN THE SAME PLACE AND LEFT OPEN ON PURPOSE. `terme` is
    # keyed `term.lower()`, but a decided-list key is whatever someone typed, and
    # three are capitalised: `Hooggeregshof` (Sosiale Wetenskappe Gr 6), `MIV` and
    # `Childline` (Lewensoriëntering Gr 7). The `t not in terme` test below -- and
    # the identical test in the `omskrywing` comparison and in `oop` -- can never
    # match them, so those three are compared against nothing, exactly as a
    # two-meaning term was. On 1 October 2026 it happened to be harmless: both
    # lessons carrying `Hooggeregshof` match its wording anyway, and no lesson
    # carries the other two yet. It is still live, and the next mismatch on one of
    # them will be invisible. Not fixed here because folding the key to lower case
    # changes what the sweep says about ORDINARY terms, which this change promised
    # not to touch -- it wants its own run, with its own before/after diff.
    twee_verkeerd = {}     # term -> (senses, {text -> [(path, status, year)]})
    twee_prosa = []        # terms whose senses no comparison can reach
    for t, v in sorted(besluite_vroeg.items()):
        if not v.get("twee_betekenisse") or t not in terme:
            continue
        sinne = besliste_betekenisse(v)
        if sinne is None:
            twee_prosa.append(t)
            continue
        if v.get("voorbeelde_mag_verskil"):
            def pas(teks, sinne=sinne):
                return any(romp(teks) == romp(s) for _, s in sinne)
        else:
            def pas(teks, sinne=sinne):
                return any(teks == s for _, s in sinne)
        verkeerd = {teks: waar for teks, waar in terme[t].items() if not pas(teks)}
        if verkeerd:
            twee_verkeerd[t] = (sinne, verkeerd)

    def twee_reels(vv=""):
        """The multi-meaning lines. They must say WHICH of two things happened.

        "nie as drif getel nie" was true, and still is, and on its own it reads as
        "checked and found fine". It was not checked at all until the loop above
        existed, and a withdrawn wording sat under that line for a day.
        """
        if twee:
            print(f"{vv}{len(twee)} met opset twee betekenisse, nie teen MEKAAR vergelyk nie: "
                  f"{', '.join(twee)}")
            getoets = [t for t in twee if t not in twee_prosa]
            if getoets:
                print(f"{vv}  elke les se inskrywing is wel teen daardie term se besliste "
                      f"betekenisse getoets ({', '.join(getoets)});")
                print(f"{vv}  'n les moet EEN daarvan woordeliks dra.")
        if twee_prosa:
            print(f"{vv}NIKS VERGELYK vir {len(twee_prosa)} term(e) met twee betekenisse: "
                  f"{', '.join(twee_prosa)}.")
            print(f"{vv}  Daardie inskrywing(s) hou hul bewoordings in prosa en nie in 'n "
                  f"'betekenisse'-lys nie,")
            print(f"{vv}  dus is daar geen sin om 'n les teen te toets nie. Hierdie veeg se "
                  f"niks oor hulle nie.")

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
            # Additive, and deliberately separate from `drif`: these are lessons
            # that match NO decided sense of a two-meaning term, which is a
            # different fault from two lessons disagreeing with each other.
            "twee_betekenisse_sonder_treffer": {
                t: [{"teks": k, "lesse": [p for p, _, _ in v]}
                    for k, v in verkeerd.items()]
                for t, (_, verkeerd) in twee_verkeerd.items()},
            "twee_betekenisse_nie_vergelyk_nie": twee_prosa,
        }, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 1 if (drif or twee_verkeerd) else 0

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

    if not gedeel and not twee_verkeerd:
        # Not a pass. Nothing was compared, and that reads the same as a pass
        # unless it says so. A two-meaning term is checked against its own decided
        # senses even when it appears in only ONE lesson, so a finding there has to
        # survive this early return.
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
           if not v.get("omskrywing") and not v.get("twee_betekenisse") and t in terme}
    if oop:
        print(f"BESLISSING NOG OOP ({len(oop)}):")
        print()
        for term in sorted(oop):
            print(f"  {term}")
            for teks, waar in sorted(terme[term].items()):
                for pad_, status, jaar in sorted(waar, key=lambda w: (w[2] or 10**6, w[0])):
                    merk = "afgelewer" if status == "goedgekeur" else (status or "?")
                    print(f'     {etiket(pad_, jaar)} ({merk}) "{teks}"')
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
                    print(f'     nie:  {etiket(pad_, jaar)} ({merk}) "{teks}" -- {pad_}')
            print()

    # A two-meaning term reported in its own block, not folded into the one above:
    # there is no single REG wording to print, and a reader has to see that the
    # several right answers are right. The fault is the same severity -- a lesson
    # carrying a wording nobody decided on.
    if twee_verkeerd:
        print(f"TEEN AL DIE BESLISTE BETEKENISSE ({len(twee_verkeerd)}):")
        print()
        for term in sorted(twee_verkeerd):
            sinne, verkeerd = twee_verkeerd[term]
            print(f"  {term} - twee betekenisse met opset; 'n les moet EEN van hulle")
            print(f"  woordeliks dra. Hierdie een dra nie een van hulle nie.")
            for wanneer, sin in sinne:
                print(f'     REG ({wanneer}):')
                print(f'           "{sin}"')
            for teks, waar in sorted(verkeerd.items()):
                print(f'     NIE:  "{teks}"')
                for pad_, status, jaar in sorted(waar, key=lambda w: (w[2] or 10**6, w[0])):
                    merk = "afgelewer" if status == "goedgekeur" else (status or "?")
                    nommer = f"les {jaar}" if jaar else "?"
                    print(f"           {nommer:<8} {merk:<12} {pad_}")
            print()

    if not drif:
        if not teen_besluit and not oop and not twee_verkeerd:
            print(f"  Geen drif. Al {len(gedeel) - len(twee)} gedeelde terme is woord vir woord")
            print(f"  dieselfde oor die {gelees} lesse wat gelees is.")
            twee_reels("  ")
            return 0
        if not teen_besluit and not oop:
            print("Geen les weerspreek 'n ander nie; die bogenoemde dra nie een van sy term se")
            print("besliste betekenisse nie.")
            twee_reels()
            return 1
        if not teen_besluit:
            print(f"Geen les weerspreek 'n ander nie, maar {len(oop)} bewoording(s) is nog nie besluit nie.")
            twee_reels()
            return 1
        print("Geen les weerspreek 'n ander nie; die bogenoemde weerspreek 'n beslissing.")
        twee_reels()
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
                nommer = etiket(pad, jaar)
                print(f"       {nommer:<8} {merk:<12} {pad}")
        print()

    print(f"{len(drif)} van die {len(gedeel)} gedeelde terme dryf uiteen.")
    twee_reels()
    if besluite:
        # Membership is not settlement. An entry may be OPENED in the agreed list --
        # given a name, a note and three routes -- with its 'omskrywing' still empty,
        # precisely to record that nobody has chosen yet. Counting those as settled
        # told the reader the opposite of the truth the entry was written to record,
        # and it did so the same hour the first such entry was added.
        beslis = sum(1 for t in drif if (besluite.get(t) or {}).get("omskrywing"))
        oop_maar_gemerk = sum(1 for t in drif
                              if t in besluite and not (besluite.get(t) or {}).get("omskrywing"))
        print(f"{beslis} daarvan het reeds 'n besliste bewoording "
              f"(sien {'; '.join(besluit_bronne)});")
        if oop_maar_gemerk:
            print(f"{oop_maar_gemerk} staan in daardie lys met 'n LEE bewoording - opgeteken as oop, "
                  f"nie beslis nie.")
        print("vir die res moet een bewoording wen. 'n Derde bewoording maak dit erger.")
    else:
        print("Een bewoording moet wen. 'n Derde bewoording maak dit erger.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

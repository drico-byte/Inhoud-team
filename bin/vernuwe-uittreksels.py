#!/usr/bin/env python3
"""
Rewrite every per-lesson spec extract from the approved specs.

`hardloop.py` writes the extract a writer and a coverage checker read -- but only
when it runs for that lesson. So editing a spec and briefing an agent straight
afterwards hands it the OLD copy, and the agent then reports, correctly, that the
fix is not in the spec. That has now happened twice in one afternoon, the second
time an hour after the first was written down, which is what a habit that needs
remembering is worth.

This does the one safe part of a runner call and nothing else: no gate, no
staleness, no archiving, no state. Run it after editing a spec and before
briefing anyone.

    python bin/vernuwe-uittreksels.py                 # all of them
    python bin/vernuwe-uittreksels.py --vak "Natuurwetenskappe en Tegnologie" --graad 4
    python bin/vernuwe-uittreksels.py --wat-sou-verander      # dry run

Only lessons that already have an extract are rewritten. A lesson nobody has
started has nothing to go stale, and writing one early would put a spec entry on
disk for a draft that does not exist.

AN EXTRACT IS TWO FILES. `spek/les-3.json` holds every field cut at its record
marker -- the orders, which is what a writer reads -- and `spek/les-3.rekords.json`
holds the halves below those markers, which the coverage checker is given as well.
This script writes both, and it treats a MISSING records file as stale: an orders
file can be current while its records half was never written, by a machine whose
checkout predates the split or by a deletion, and the coverage checker would then
be sent to a path that does not exist. See P.uittreksel_helftes.

IT ALSO REFRESHES THE FACT CHECKER'S COPY, for the same reason and after the same
kind of failure. `feite-kopie/<lesson>.json` -- the draft with its provenance note
stripped -- is written only by a runner call too. A fact checker dispatched without
one reads whatever copy happens to be on disk, and that copy is gitignored, so
nothing shows that it is old.

It cost a whole fact check on 11 September 2026. The copy of Grade 5
`gestoorde-energie-in-brandstof` lesson 2 was written at 15:03 on 10 September, the
lesson itself changed twice later that day, and the check ran the next morning
against the eighteen-hour-old copy. Two of its four findings were about glossary
entries that had already been corrected. The writer caught it, read both entries
against the agreed list, and refused to write a third wording.

A stale DRAFT is worse than a stale spec extract. An agent reading an old spec
reports that a fix is missing, which is visibly wrong and gets checked. An agent
reading an old draft reports faults that no longer exist, and those read exactly
like real findings.
"""

import argparse
import json
import os
import subprocess
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)
sys.path.insert(0, HIER)

import paaie as P                                          # noqa: E402
from hardloop import met_spek_konteks                      # noqa: E402


def spesifikasies(graad=None, vak=None):
    wortel = P.SPEK_GOEDGEKEUR
    for gids, _, lers in os.walk(wortel):
        for naam in sorted(lers):
            if not naam.endswith(".json") or naam.endswith(".feite.json"):
                continue
            pad = os.path.join(gids, naam)
            try:
                spek = P.lees_json(pad)
            except (OSError, ValueError) as e:
                print(f"  kon nie lees nie: {P.rel(pad)} ({e})", file=sys.stderr)
                continue
            if graad and int(spek.get("graad", 0)) != graad:
                continue
            if vak and P.slug(spek.get("vak", "")) != P.slug(vak):
                continue
            yield pad, spek



# Why an extract's content no longer matches the stamp it was written with. One
# value rather than a boolean, because the three answers want three different
# actions and only one of them saves anything.
GELYK = "gelyk"                  # content and stamp agree; only the spec moved
SMELTSPOOR = "smeltspoor"        # a merge paired one machine's content with another's stamp
HANDGESKRYF = "handgeskryf"      # content matches no committed version: a direct edit
ONGESTEMPEL = "ongestempel"      # no stamp at all, so nothing certifies the content

# How far back ONE extract's own history is searched for a committed version of its
# content. Measured over the 48 copies in the tree on 12 October 2026: every one of
# them reproduces a committed version of its own path, the deepest 50 revisions back,
# and the search costs the same at 120 as at 60 (0.11 s per extract) because two
# process launches dominate it. So 120 is twice the deepest case ever seen, for
# nothing. Too small a window errs the safe way -- an unfound version is reported as
# a hand edit and the copy is kept -- so this bounds cost, not correctness.
GIT_WEERGAWES = 120


def _git(*args, **kw):
    """git in this repository, as bytes, or None when git cannot answer.

    None must mean "no evidence either way" and never "no merge artefact": a machine
    without git, a checkout that is not a repository and a genuine miss all land
    here, and collapsing them into the answer that throws a writer's edit away is the
    one mistake this whole check exists to avoid.
    """
    try:
        r = subprocess.run(("git", "-C", REPO) + args, capture_output=True, **kw)
    except OSError:
        return None
    return r.stdout if r.returncode == 0 else None


def _batch_inhoude(data):
    """The contents in a `git cat-file --batch` stream, in input order, None for a miss.

    Each record is `<oid> <type> <size>\\n<contents>\\n`, and a spec git cannot
    resolve prints `<spec> missing` with no contents at all. Read as BYTES: the size
    is a byte count, so decoding first would mis-slice every extract with a diacritic
    in it, and this repository is written in Afrikaans.
    """
    i = 0
    while i < len(data):
        j = data.find(b"\n", i)
        if j < 0:
            return
        kop = data[i:j].split()
        if len(kop) == 3 and kop[2].isdigit():
            n = int(kop[2])
            yield data[j + 1:j + 1 + n]
            i = j + 1 + n + 1
        else:
            yield None                    # `missing`: no such file in that commit
            i = j + 1


def bekende_weergawe(pad, inhoud, maks=GIT_WEERGAWES):
    """(short sha, date) of the newest commit holding exactly this content, else None.

    Two git calls whatever the window: the commits that touched this one path, then
    one cat-file --batch over `<rev>:<path>` for all of them. The file is read out of
    each commit's TREE and not out of a diff, so a version a merge commit itself
    introduced counts as committed too -- which is the very shape being looked for.

    --full-history on purpose. Default history simplification prunes the side of a
    merge whose content was not taken, and the other machine's commit is exactly what
    gets pruned there: it is the version we are trying to recognise.

    Documents are compared as PARSED JSON, never as bytes. core.autocrlf rewrites the
    line endings on these machines, so a committed blob and a file this pipeline wrote
    differ in bytes while saying the same thing; and the stamp is left out of both
    sides, because the stamp is precisely the half a merge replaced.
    """
    rel = P.rel(pad)
    if os.path.isabs(rel):
        return None                       # outside the repository: git cannot answer
    revs = _git("log", "--full-history", "--format=%H %ad", "--date=short",
                "--max-count=%d" % maks, "--", rel)
    if not revs:
        return None
    # Split once, and never unpack a fixed number of fields out of a git format
    # string: the sha is the part this depends on, the date only prints.
    reels = []
    for r in revs.decode("utf-8", "replace").splitlines():
        deel = r.split(None, 1)
        if deel:
            reels.append((deel[0], deel[1] if len(deel) > 1 else "?"))
    spesse = "".join("%s:%s\n" % (sha, rel) for sha, _ in reels).encode("utf-8")
    uit = _git("cat-file", "--batch", input=spesse)
    if uit is None:
        return None
    for (sha, datum), blob in zip(reels, _batch_inhoude(uit)):
        if blob is None:
            continue
        try:
            if P.sonder_uittreksel_stempel(json.loads(blob)) == inhoud:
                return sha[:8], datum
        except ValueError:
            continue                      # a version that was not valid JSON
    return None


def hoe_verander(pad, oud):
    """Why this extract no longer matches its stamp, as (verdict, committed version).

    An extract is DERIVED, never authored. So the only honest way to tell a hand edit
    from an ordinary source change is to ask whether the file still matches what the
    last write derived -- comparing its text against the newly derived version cannot
    do it, because an edited source field looks exactly like an edited extract field.
    The first version of this check did that and fired on every normal spec edit,
    which would have trained everyone to ignore it.

    A writer wrote two corrections straight into an extract on 11 September 2026.
    They would have been erased by the next refresh without a trace; they were caught
    only because someone read the agent's report closely.

    But the stamp lives inside the file it certifies, so git merges content and stamp
    as independent lines and routinely pairs one machine's content with another
    machine's stamp. ALL 48 copies saved up to 12 October 2026 were that, from three
    merges, each reproducing an approved-spec revision field for field and holding
    nothing to port. With three machines merging constantly that is not an edge case,
    so git is asked the one question that separates the two: has this exact content
    ever been committed under this path? If it has, no hand wrote it.

    The limit of the evidence runs both ways. An extract edit that was itself
    committed and then merged reads as a merge artefact here -- that one is visible
    as a diff in review, which is why these derived files are tracked at all. And
    content that no commit ever held reads as a hand edit even when no hand wrote it,
    which is what an extract derived by a version of this code that was never
    committed looks like. That is the safe direction: it keeps the copy.
    """
    inhoud = P.sonder_uittreksel_stempel(oud)
    gestempel = oud.get(P.UITTREKSEL_STEMPEL)
    if gestempel and gestempel == P.uittreksel_stempel(oud):
        return GELYK, None
    weergawe = bekende_weergawe(pad, inhoud)
    if not gestempel:
        return ONGESTEMPEL, weergawe
    return (SMELTSPOOR if weergawe else HANDGESKRYF), weergawe


def _stoor_verlore(uit_pad, oud):
    """Save the whole old extract beside itself and say what to do with it."""
    kopie = uit_pad[:-len('.json')] + '.verlore.json'
    P.skryf_json(kopie, P.sonder_uittreksel_stempel(oud))
    print(f"     Die hele ou uittreksel is gestoor: {P.rel(kopie)}")
    print("     Dra die verandering oor na die SPEK, nie terug na die uittreksel nie, "
          "en vee die kopie dan uit.")


def vernuwe_feitekopiee(graad=None, vak=None, droog=False):
    """Rewrite every fact checker's copy that no longer matches its draft.

    Only copies that ALREADY EXIST are touched, on the same principle as the spec
    extracts: a lesson nobody has fact-checked has nothing to go stale.

    7 October 2026: a copy is only a copy of a LESSON. This took every .json in
    feite-kopie/, so a stray copy of a lesson's sibling -- one was written there
    when another tool mistook the new acceptance record for a draft -- counted
    toward the "x of y feitekopie(e)" total this prints and was kept up to date
    like a lesson. The question is now asked once for every tool: P.is_les_konsep.
    """
    aantal = verouderd = 0
    for gids, _, lers in os.walk(os.path.join(REPO, "konsepte")):
        if os.path.basename(gids) != "feite-kopie":
            continue
        for naam in sorted(lers):
            if not P.is_les_konsep(naam):
                continue
            kopie_pad = os.path.join(gids, naam)
            les_pad = os.path.join(os.path.dirname(gids), naam)
            if not os.path.exists(les_pad):
                print("  WEESKIND: %s het geen konsep langs hom nie" % P.rel(kopie_pad),
                      file=sys.stderr)
                continue
            try:
                les = P.lees_json(les_pad)
                oud = P.lees_json(kopie_pad)
            except (OSError, ValueError):
                continue
            if graad and int(les.get("graad", 0)) != graad:
                continue
            if vak and P.slug(les.get("vak", "")) != P.slug(vak):
                continue
            aantal += 1
            # Compare against what the copier would write, never against a second
            # list of withheld fields -- see P.feitekopie_inhoud for what that cost.
            if oud == P.feitekopie_inhoud(les):
                continue
            verouderd += 1
            print("  %s feitekopie: %s" % ("sou vernuwe" if droog else "vernuwe",
                                           P.rel(kopie_pad)))
            if not droog:
                P.skryf_feitekopie(les_pad)
    return aantal, verouderd


def main():
    ap = argparse.ArgumentParser(
        description="Rewrite per-lesson spec extracts from the approved specs")
    ap.add_argument("--vak")
    ap.add_argument("--graad", type=int)
    ap.add_argument("--wat-sou-verander", action="store_true", dest="droog",
                    help="say what would change and write nothing")
    a = ap.parse_args()

    geskryf = ongeraak = 0
    smeltspore = handgeskrewe = ongestempeld = 0
    rekordvelde = rekordbytes = 0
    for spek_pad, spek in spesifikasies(a.graad, a.vak):
        vak = spek.get("vak")
        graad = int(spek["graad"])
        # The lesson folder is named after the spec FILE, because that is how the
        # runner finds both (--subonderwerp -> slug -> file). kaps_subonderwerp can
        # differ: Gr 4 farming's is "Voedsel en boerdery in Suid-Afrika" while its
        # folder is voedsel-en-boerdery, and every farming extract was skipped as
        # "not started" until 7 October 2026 - spec fixes silently never arrived.
        sub = os.path.splitext(os.path.basename(spek_pad))[0]
        for les in spek.get("lesse", []):
            nommer = les.get("nommer")
            if not nommer:
                continue
            uit_pad = P.spek_inskrywing(graad, vak, sub, nommer)
            if not os.path.exists(uit_pad):
                continue                      # nobody has started this lesson
            nuut = met_spek_konteks(spek, les)
            # Compare against what would be WRITTEN, which is now HALF of what is
            # derived: an extract is two files, the orders and the record halves
            # beside them. Comparing the file on disk against the whole derived
            # entry would find every extract in the repository unequal on every run
            # for ever - the same "rewrite everything, every time" failure the stamp
            # comment below is about, and it would destroy the hand-edit evidence
            # with each rewrite. See P.uittreksel_helftes.
            bestelling, rekords, rekord_pad = P.uittreksel_helftes(uit_pad, nuut)
            try:
                oud = P.lees_json(uit_pad)
            except (OSError, ValueError):
                oud = None
            # The records file is compared too, and its ABSENCE counts as stale. An
            # orders file that is already current while its records half is missing -
            # written by a machine whose checkout predates the split, or deleted -
            # would otherwise be reported "reeds gelyk" and the coverage checker's
            # second file would never appear.
            try:
                ou_rekords = P.lees_json(rekord_pad)
            except (OSError, ValueError):
                ou_rekords = None
            # Compare WITHOUT the stamp. The stamp is not derived content, so a
            # stamped file could never equal a freshly derived one, and every run
            # would rewrite every extract for ever - each rewrite also destroying
            # the evidence that the previous one was hand-edited.
            #
            # A file whose CONTENT is already current is left alone even when its
            # stamp is a merge's, which is what the short-circuit does. Rewriting it
            # for the stamp alone would put a one-line diff on a file whose content is
            # right, on all three machines, which is the very churn the artefacts come
            # out of - and the wrong stamp costs nothing, because the stamp is only
            # ever read once the content has diverged, and hoe_verander then names it.
            if P.sonder_uittreksel_stempel(oud) == bestelling and ou_rekords == rekords:
                ongeraak += 1
                continue
            agter = []
            if oud is None:
                # Unreadable - a merge that left conflict markers behind looks like
                # this. Nothing certifies it either, so say so rather than let it
                # read as an ordinary spec change.
                agter.append("kon nie gelees word")
            elif P.sonder_uittreksel_stempel(oud) != bestelling:
                agter.append("bestellings")
            if ou_rekords is None:
                agter.append("rekords ontbreek")
            elif ou_rekords != rekords:
                agter.append("rekords")
            uitspraak, weergawe = (hoe_verander(uit_pad, oud) if isinstance(oud, dict)
                                   else (GELYK, None))
            print(f"  {'sou verander' if a.droog else 'vernuwe'}: {P.rel(uit_pad)}"
                  f"  ({', '.join(agter)})")
            if uitspraak == HANDGESKRYF:
                handgeskrewe += 1
                print("     LET OP: hierdie uittreksel stem nie meer ooreen met wat hierdie skrip "
                      "laas geskryf het nie - iemand het DIREK in die uittreksel geskryf.")
                if not a.droog:
                    _stoor_verlore(uit_pad, oud)
            elif uitspraak == SMELTSPOOR:
                smeltspore += 1
                sha, datum = weergawe
                print(f"     SMELTSPOOR: die inhoud is woord vir woord die weergawe wat op "
                      f"{datum} vasgelê is ({sha}), net met 'n ander masjien se stempel langs "
                      f"dit - 'n saamsmelting kies die inhoud en die stempel as twee "
                      f"onafhanklike reëls. Niemand het hier met die hand geskryf nie; die "
                      f"uittreksel word net herskryf en niks word gestoor nie.")
            elif uitspraak == ONGESTEMPEL:
                ongestempeld += 1
                if weergawe:
                    sha, datum = weergawe
                    print(f"     ONGESTEMPEL: hierdie uittreksel dra geen stempel nie, so niks sê "
                          f"wat laas daarin geskryf het nie. Die inhoud is wel woord vir woord "
                          f"die weergawe van {datum} ({sha}), dus is niks verlore nie en hierdie "
                          f"herskryf stempel dit weer.")
                else:
                    print("     ONGESTEMPEL: hierdie uittreksel dra geen stempel nie, so niks sê "
                          "wat laas daarin geskryf het nie, en die inhoud pas by geen weergawe in "
                          "git nie. 'n Handwysiging kan dus nie uitgesluit word nie.")
                    if not a.droog:
                        _stoor_verlore(uit_pad, oud)
            rekordvelde += rekords.get("_velde_met_rekords", 0)
            # NET of the marker note the orders file keeps in each cut field, so this
            # is what a writer stops reading rather than what was moved.
            rekordbytes += max(0, len(json.dumps(nuut, ensure_ascii=False))
                               - len(json.dumps(bestelling, ensure_ascii=False)))
            if not a.droog:
                P.skryf_uittreksel(uit_pad, nuut)
            geskryf += 1

    kopiee, verouderd = vernuwe_feitekopiee(a.graad, a.vak, a.droog)

    # The field count and the KB are the numbers worth printing: a run that moved
    # nothing looks exactly like a run that read nothing, and the whole point of the
    # split is how much shorter the writer's file got.
    rekordreel = (f"{rekordvelde} veld(e) se rekordhelfte staan in die rekordlêer "
                  f"langsaan, {rekordbytes // 1024} KB wat 'n skrywer nie meer lees nie.")
    # The three verdicts are counted out beside the total, because a merge artefact
    # and a hand edit used to print the same alarm and the difference is the whole
    # point: one needs a person today, the other needs nobody ever.
    gewoon = geskryf - smeltspore - handgeskrewe - ongestempeld
    verdeling = (f"Daarvan: {gewoon} gewone spekwysiging(s), {smeltspore} smeltspoor, "
                 f"{handgeskrewe} met die hand verander, {ongestempeld} ongestempel.")
    if a.droog:
        print(f"\n{geskryf} uittreksel(s) is verouderd, {ongeraak} is reeds gelyk.")
        if geskryf:
            print(verdeling)
            print(rekordreel)
        print(f"{verouderd} van {kopiee} feitekopie(e) is verouderd.")
        return 1 if (geskryf or verouderd) else 0
    print(f"\n{geskryf} vernuwe, {ongeraak} was reeds gelyk.")
    if geskryf:
        print(verdeling)
        print(rekordreel)
    print(f"{verouderd} van {kopiee} feitekopie(e) herskryf.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

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

    Reading the other lessons is not enough on its own: the FIRST lesson to use
    a shared term has no other lesson to be found in, and would go to the
    checker unprotected -- the one moment the wording is easiest to lose,
    because nothing yet disagrees with it. So the approved specs are read too,
    for a term whose wording they prescribe.

USAGE
    python bin/taalnasien.py --vak "Natuurwetenskappe en Tegnologie" --graad 4 \
        --subonderwerp "Vaste stowwe" --les 2
    python bin/taalnasien.py --les-pad konsepte/gr4/.../les-2.json
"""

import argparse, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)
sys.path.insert(0, HIER)

# Directories that sit beside a lesson and hold files named `les-<n>.json` which
# are NOT lessons. Any walk looking for lesson drafts has to skip them by name:
#
#   spek/les-3.json        -- the spec extract, the same file name as the draft
#   feite-kopie/les-3.json -- the draft with its provenance note stripped, the
#                             copy handed to the fact checker, rewritten by the
#                             runner on every run
#
# bin/woordelysdrif.py has hit this twice and records both in `lesse()`: the
# drift sweep read 50 lessons where 25 existed because of the extract, and then
# 42 where 29 existed once feite-kopie/ was added on 9 September 2026. It keeps
# the exclusion as a LIST rather than one name, because the next directory to
# mirror these file names will do this a third time. This is the same list under
# the same name, written out rather than imported so that a reader of either
# file can see what is excluded without opening the other.
HERHALINGS = ("spek", "feite-kopie")


def lees_json(pad):
    with open(pad, encoding="utf-8") as fh:
        return json.load(fh)


def romp(teks):
    """The part of a definition before its examples.

    Drico ruled on 28 August 2026 that the examples after `soos` may differ per
    lesson -- lesson 9 gives wood, water and air because it teaches the three
    states, lesson 14 gives paper, wood and clay because it folds paper, and both
    are that lesson's own material. What must be identical is the sentence
    itself. Same split as bin/woordelysdrif.py, so the two tools agree about
    when two lessons carry one definition.
    """
    return re.split(r",?\s+soos\s+", teks, maxsplit=1)[0].rstrip(" .,")


def lesteks(les):
    """Every word a language checker would read, block by block.

    A `lys` block keeps its lines in `items` and carries no `teks` at all. This
    read only `teks`, so every list block in every lesson -- seventeen of them in
    Gr 4 NWT alone -- was dropped silently from what the checker is sent. Two
    things followed, and the second is the worse: that Afrikaans was never
    checked, and `beskermde_woorde` decides what to protect by asking whether a
    word appears in this output, so a protected wording living only in a list
    went over unprotected. The one that surfaced it carries a whole assessed
    requirement -- noise at home, at school, in the community.
    """
    dele = []
    for b in les.get("blokke", []):
        kop = (b.get("kop") or b.get("term") or b.get("vir") or "").strip()
        teks = (b.get("teks") or "").strip()
        items = [i.strip() for i in (b.get("items") or []) if str(i).strip()]
        if items:
            gelys = "\n".join(f"  - {i}" for i in items)
            teks = f"{teks}\n{gelys}" if teks else gelys
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

    WHICH FILES COUNT AS ANOTHER LESSON, 1 October 2026. This walked for
    `les-<n>.json` and skipped only the lesson itself, so it also read the two
    directories listed in HERHALINGS above -- and `feite-kopie/` is the lesson,
    minus one field, so every term this lesson defines was found "in another
    lesson": its own stripped copy. 556 (lesson, term) pairs across the
    repository were handed to the outside language checker with a shared pair
    that does not exist, and another 34 real pairs named `feite-kopie` as one of
    the places the wording also stands. Gr 6 Sosiale Wetenskappe Demokrasie les 2
    was the one that surfaced it: `landdroshof` shared with nothing but its own
    copy, `hof` shared with "feite-kopie, mapungubwe".

    That is worse here than a wrong count. This block goes to the one checker
    with no sight of our decisions, nothing re-checks its edits afterwards, and
    the reason is the whole mechanism -- a checker holds the line on a sentence
    that reads awkwardly because it is told why. A reason it cannot verify is a
    reason it may act on, and a wording may be preserved for a pair that was
    never there, or a real reason be disbelieved because the one beside it is
    plainly wrong. Spec extracts carry no `blokke` and so contributed nothing
    today; they are excluded anyway, because that is a fact about the extract
    format and not a property anyone promised to keep.

    AND THE WORDING HAS TO MATCH, NOT JUST THE TERM, 1 October 2026. The match
    was on the term NAME alone, so the reason printed "the same definition also
    stands in X" about lessons whose definitions DIFFER. 27 of the 96 printed
    reasons were false that way. 17 were ordinary drift, which the drift sweep
    does report -- so a second guard existed. The other 10 were terms the agreed
    list marks `twee_betekenisse`: one word, two meanings, each lesson keeps its
    own, and the drift sweep stays silent about them BY DESIGN. For those there
    was no second guard at all, not even in a subject swept to zero drift, and
    the false claim was the dangerous direction: it told the outside checker that
    two wordings which must NEVER be made to agree were a matched pair, and that
    "improving one breaks the pair". `as` (a wheel's axle / the Earth's axis) in
    two grades, `konflik` (people / a drama), `verhouding` (people / proportion)
    and `hof` (a law court / a ruler's court) all went over that way. Inviting
    that one edit is exactly what woordelysdrif.py refuses to do when it declines
    to report these as drift.
    """
    vak_wortel = os.path.dirname(os.path.dirname(les_pad))   # .../<vak>/
    myne = {b["term"]: b.get("teks", "")
            for b in les.get("blokke", []) if b.get("tipe") == "begrip"}
    if not myne:
        return []

    # Which terms this subject-grade lets differ in their EXAMPLES, read the way
    # bin/woordelysdrif.py reads it so that both tools call the same two lessons
    # a pair. Keyed exactly as the list types the term: the one capitalised key
    # in the repository is itself a decided wording, which `bou` suppresses from
    # this path anyway, and a flag missed this way costs a true pair rather than
    # printing a false one -- the safe direction.
    vlae = {}
    if les.get("vak") and les.get("graad"):
        try:
            import paaie as P                                # noqa: E402
            vlae = P.gedeelde_omskrywings(les["vak"], les["graad"]).get("terme") or {}
        except Exception:
            vlae = {}

    def een_omskrywing(term, myn, ander_teks):
        """Do these two lessons really carry ONE definition of this term?"""
        if (vlae.get(term) or {}).get("voorbeelde_mag_verskil"):
            return romp(myn) == romp(ander_teks)
        return myn == ander_teks

    elders = {}
    for gids, _, lers in os.walk(vak_wortel):
        if os.path.basename(gids) in HERHALINGS:
            continue        # holds copies of lessons, not other lessons
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
                if (b.get("tipe") == "begrip" and b.get("term") in myne
                        and een_omskrywing(b["term"], myne[b["term"]],
                                           b.get("teks", ""))):
                    elders.setdefault(b["term"], set()).add(
                        os.path.basename(os.path.dirname(ander_pad)))

    return [(t, myne[t], sorted(waar)) for t, waar in sorted(elders.items())]


def spek_beskermde_woorde(les_pad):
    """The rulings the lesson's OWN specification records.

    kaps/beskermde-woorde.json holds decisions that span sub-topics. Each spec
    also keeps its own, and those never reached the language checker: lesson 25
    went over with one protected word listed while its plan records ten -- volume
    against the Maths sense, hoog/laag tied to pitch alone, the wording that must
    be used about people who do not hear. Every one of them reads like ordinary
    Afrikaans a fluent checker would improve.
    """
    pad = os.path.join(os.path.dirname(les_pad), "spek",
                       os.path.basename(les_pad))
    if not os.path.exists(pad):
        return []
    try:
        spek = lees_json(pad)
    except Exception:
        return []
    uit = []
    rou = spek.get("beskermde_woorde") or []
    # Some planners wrote the field as {word: reason} instead of a list of
    # {hou, nie, rede}. Iterating that dict gave bare strings and crashed, so the
    # fuel lessons' protected words (hitte, never warmte) could not reach the
    # language checker at all. Found 18 September 2026 building the Gr 5 batch.
    if isinstance(rou, dict):
        rou = [{"hou": k, "rede": v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)}
               for k, v in rou.items()]
    for inskrywing in rou:
        if isinstance(inskrywing, str):
            inskrywing = {"hou": inskrywing}
        if isinstance(inskrywing, dict) and inskrywing.get("hou"):
            uit.append(inskrywing)
    return uit


def besliste_omskrywings(les, vak, graad):
    """Wordings the subject-grade's AGREED-WORDINGS file has settled.

    Added 29 September 2026, because this tool never read that file -- the file
    that is the authority on an agreed wording was not seen by the tool whose
    whole job is stopping the outside language check from undoing one.

    The two older paths both miss the case that matters. `gedeelde_verklarings`
    finds a wording by seeing the SAME text in another lesson, so a term settled
    for the whole subject but defined in only ONE lesson is invisible to it --
    and that is the normal shape here: Gr 6 SW settled `ontdekkingsreisiger` for
    the year, and exactly one lesson carries the glossary entry.
    `voorgeskrewe_omskrywings` reads a spec's `verwagte_begrippe`, which
    Sosiale Wetenskappe writes as a bare list of terms with no wordings at all.

    So a ruling reached the checker only by luck. It also reached it with the
    wrong reason -- "another lesson says the same" rather than "this was
    decided" -- and a checker that understands why holds the line when a
    sentence reads awkwardly.
    """
    myne = {b["term"]: b.get("teks", "")
            for b in les.get("blokke", []) if b.get("tipe") == "begrip"}
    if not myne or not vak or not graad:
        return []
    try:
        import paaie as P                                    # noqa: E402
        pad = P.gedeelde_omskrywings_pad(vak, graad)
    except Exception:
        return []
    if not pad:
        return []
    try:
        lys = lees_json(pad)
    except Exception:
        return []

    uit = []
    for term, inskrywing in (lys.get("terme") or {}).items():
        if term not in myne or not isinstance(inskrywing, dict):
            continue
        # Only where the lesson really carries one of this term's settled
        # wordings. Where it does not, the mismatch is a coverage problem and not
        # something to tell a language checker about.
        # EXACT, AND ONLY EXACT -- deliberately NOT the `voorbeelde_mag_verskil`
        # stem match that bin/woordelysdrif.py also applies. No entry in the
        # repository carries both flags (measured 2 October 2026: 6 entries marked
        # `twee_betekenisse`, 22 marked `voorbeelde_mag_verskil`, no overlap), so a
        # stem match buys this path nothing -- and it costs. Measured over all 319
        # drafts it moved 11 terms that already had a protection by the
        # shared-wording route below onto this one, replacing a reason that was
        # true ("the same wording stands in these other lessons") with one that is
        # false in its examples ("every lesson that defines the term uses these
        # words"). That is the same class of false reason this file was repaired
        # for on 1 October 2026. A wording this path declines is not unprotected:
        # the shared-wording route still carries it. Add the stem match only
        # together with a reason line that would then be true, and measure it on
        # its own.
        myn = myne[term].strip()
        wanneer, teks = "", None
        for kandidaat, sin in besliste_bewoordings(inskrywing):
            if myn == sin:
                wanneer, teks = kandidaat, sin
                break
        if teks is None:
            continue
        # The files disagree about where the reasoning lives, because they were
        # written months apart: Gr 5 Natuurwetenskappe uses `nota` and
        # `beslis_deur`, Gr 6 Sosiale Wetenskappe uses `rede` and `let_op`.
        # Reading only one shape silently drops the reason for a whole subject --
        # and a checker that is given the wording without the reason is the one
        # that "improves" it when a sentence reads awkwardly.
        rede = (inskrywing.get("rede") or inskrywing.get("nota") or "").strip()
        deur = (inskrywing.get("beslis_deur") or "").strip()
        if deur and deur.lower() not in rede.lower():
            rede = (f"{rede} Beslis deur {deur}." if rede else f"Beslis deur {deur}.")
        uit.append((term, teks, rede, (inskrywing.get("let_op") or "").strip(), wanneer))
    return sorted(uit)


def besliste_bewoordings(inskrywing):
    """Every wording this entry has SETTLED, as (which meaning, sentence) pairs.

    One pair for an ordinary term. One pair per decided meaning for a term that
    carries more than one on purpose -- which is the case this exists for.

    ADDED 2 October 2026, because a two-meaning term's reason could not reach the
    outside language checker at all. `besliste_omskrywings` read `omskrywing` and
    nothing else, and a two-meaning entry's `omskrywing` is ALWAYS null -- its
    wordings live in `betekenisse`. So the term least able to survive that checker
    was the one whose ruling never got there: each of `konflik`'s two sentences
    reads odd standing beside the other, which is exactly why a fluent reader
    reaches for the smoother one, and why the ruling says they may never be made
    to agree.

    Same test as bin/woordelysdrif.py's `besliste_betekenisse`, deliberately, so
    the two tools agree about which entries can be compared at all. An entry that
    keeps its meanings in PROSE returns nothing: there is no field a comparison
    can stand on, and pulling a sentence out of that prose would be guessing which
    quotation is the live one -- `as` in Gr 5 Natuurwetenskappe carries a note
    saying one of its own sentences is too wide and needs correcting first.
    """
    een = (inskrywing.get("omskrywing") or "").strip()
    if een:
        return [("", een)]
    if not inskrywing.get("twee_betekenisse"):
        return []
    uit = []
    for b in inskrywing.get("betekenisse") or []:
        if isinstance(b, dict) and (b.get("sin") or "").strip():
            uit.append(((b.get("wanneer") or "").strip(), b["sin"].strip()))
    return uit


def voorgeskrewe_omskrywings(les):
    """Wordings an approved spec prescribes for a term this lesson defines.

    The point is the lesson that gets there first. `gedeelde_verklarings` finds
    a shared definition by reading the other lessons; before the second lesson
    exists there is nothing to find, and the wording is unprotected exactly when
    it is newest.
    """
    myne = {b["term"]: b.get("teks", "")
            for b in les.get("blokke", []) if b.get("tipe") == "begrip"}
    if not myne:
        return []

    uit = {}
    wortel = os.path.join(REPO, "spesifikasies", "goedgekeur")
    for gids, _, lers in os.walk(wortel):
        for naam in lers:
            if not naam.endswith(".json") or naam.endswith(".feite.json"):
                continue
            try:
                spek = lees_json(os.path.join(gids, naam))
            except Exception:
                continue
            for inskrywing in spek.get("lesse", []):
                # `verwagte_begrippe` comes in two shapes. Natuurwetenskappe writes an
                # object carrying `voorgeskrewe_omskrywings`; Sosiale Wetenskappe writes
                # a bare list of the terms the lesson is expected to define, and no
                # wordings at all. Assuming the object shape crashed this whole tool on
                # the first Sosiale Wetenskappe lesson -- and it crashes at the LAST
                # step, after the lesson has passed everything, which is the worst place
                # to find out.
                vb = inskrywing.get("verwagte_begrippe")
                if not isinstance(vb, dict):
                    continue
                for term, teks in (vb.get("voorgeskrewe_omskrywings") or {}).items():
                    # A placeholder rather than a wording: some entries say the
                    # definition may only be written once a verification passes.
                    #
                    # THE LENGTH LIMIT IS GONE, 29 September 2026. It used to require
                    # 20 words or fewer, as a proxy for "this is a real wording and not
                    # a note" -- and it silently dropped every agreed wording longer
                    # than a short sentence, in every subject, with no sign that
                    # anything had been skipped. A planner found it while checking
                    # whether Gr 6 SW's `ontdekkingsreisiger` wording (25 words) would
                    # actually be protected. It would not have been, and that wording
                    # is exactly the kind at risk: "plekke wat sy eie mense nog nie ken
                    # nie" reads like something to smooth into "nuwe plekke", which is
                    # the error the wording was written to prevent. The language check
                    # runs after the fact check and nothing re-checks it.
                    #
                    # The proxy was never needed: the return below already requires the
                    # LESSON's own definition to equal the prescribed wording character
                    # for character, and no placeholder ever does that.
                    if term in myne and teks.strip().endswith("."):
                        uit.setdefault(term, set()).add(teks)

    # Only worth printing where the lesson really carries that wording, and only
    # where the spec is not itself of two minds.
    return [(t, sorted(v)[0]) for t, v in sorted(uit.items())
            if len(v) == 1 and myne[t] == sorted(v)[0]]


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

    # Both sources are read on purpose, and after a ruling is settled the SAME
    # word is in both: CLAUDE.md requires a decision to be written into
    # kaps/beskermde-woorde.json, and the spec keeps its own copy with the
    # reasoning. Concatenating them printed every settled word twice, which
    # invites a checker to wonder which of the two entries is the real one.
    # First occurrence wins, so the repository-wide entry leads.
    woorde, gesien = [], set()
    for w in beskermde_woorde(les, sub_gids) + spek_beskermde_woorde(les_pad):
        sleutel = w["hou"].strip().lower()
        if sleutel in gesien:
            continue
        gesien.add(sleutel)
        woorde.append(w)
    gedeel = gedeelde_verklarings(les, les_pad)
    gedeel_terme = {t for t, _, _ in gedeel}
    # A settled wording leads, because it is the strongest reason there is: it was
    # decided, and the reason is recorded. It also suppresses the two weaker paths
    # for the same term, so a checker is never shown one wording under two
    # different justifications and left to guess which is the real one.
    beslis = besliste_omskrywings(les, les.get("vak"), les.get("graad"))
    beslis_terme = {t for t, _, _, _, _ in beslis}
    gedeel = [(t, teks, waar) for t, teks, waar in gedeel if t not in beslis_terme]
    gedeel_terme -= beslis_terme
    voorgeskryf = [(t, teks) for t, teks in voorgeskrewe_omskrywings(les)
                   if t not in gedeel_terme and t not in beslis_terme]

    if woorde or beslis or gedeel or voorgeskryf:
        reels.append("")
        reels.append("BESKERM - moenie hierdie verander nie")
        reels.append("-" * 72)

    for w in woorde:
        nie = ", ".join(w.get("nie") or [])
        reels.append("")
        reels.append(f"  HOU:  {w['hou']}")
        if nie:
            reels.append(f"  NIE:  {nie}")
        reels.append(f"  Waarom: {w.get('rede') or ''}")

    for term, teks, rede, let_op, wanneer in beslis:
        reels.append("")
        reels.append(f'  HOU WOORD VIR WOORD:  {term} - "{teks}"')
        if wanneer:
            # A term with more than one deliberate meaning must NOT be given the
            # reason below. "every lesson that defines the term uses these words"
            # is FALSE for it -- the other meaning's lesson uses different words --
            # and a reason the checker can see is wrong is a reason it may act on,
            # or one that makes the true reason beside it look unreliable. That
            # exact fault was found in this file on 1 October 2026, when 10 of 96
            # printed reasons told the checker that two wordings which must never
            # be made to agree were a matched pair.
            reels.append(f"  Waarom: hierdie woord dra MET OPSET meer as een betekenis in "
                         f"hierdie vak-graad, en die betekenisse mag NIE ooreengestem word "
                         f"nie. Hierdie les gebruik die betekenis '{wanneer}', en hierdie sin "
                         f"is daarvoor BESLIS en in kaps/gedeelde-omskrywings vasgele. Moenie "
                         f"hom na 'n ander betekenis se sin toe skuif nie, en moenie twee "
                         f"betekenisse saamsmelt nie.")
        else:
            reels.append("  Waarom: hierdie bewoording is vir die HELE vak-graad BESLIS en in "
                         "kaps/gedeelde-omskrywings vasgele. Elke les wat die term omskryf, gebruik "
                         "hierdie woorde. 'n Verbetering aan een les skep 'n tweede omskrywing van "
                         "een woord binne een jaar, en die eksamen dek die hele jaar.")
        if rede:
            reels.append(f"  Die besluit: {rede}")
        if let_op:
            reels.append(f"  Let op: {let_op}")

    for term, teks, waar in gedeel:
        reels.append("")
        reels.append(f"  HOU WOORD VIR WOORD:  {term} - \"{teks}\"")
        reels.append(f"  Waarom: dieselfde verklaring staan ook in {', '.join(waar)}. "
                     f"'n Verbetering aan een van hulle breek die paar, en 'n toets "
                     f"oor die hele vak sal dit vlag.")

    for term, teks in voorgeskryf:
        reels.append("")
        reels.append(f'  HOU WOORD VIR WOORD:  {term} - "{teks}"')
        reels.append("  Waarom: 'n goedgekeurde spesifikasie skryf hierdie bewoording voor, en "
                     "later lesse gaan dieselfde woorde gebruik. Hierdie les is net die eerste "
                     "een wat daar kom.")

    reels.append("")
    reels.append("=" * 72)
    reels.append("DIE LES")
    reels.append("=" * 72)
    reels.append("")
    reels.append(lesteks(les))
    return "\n".join(reels)


def herinner(pad):
    """Say out loud what this block cannot know, to stderr so it is never pasted.

    1 October 2026. A writer records the words IT thinks the language checker will
    undo, in the draft's provenance note. Nothing carries them anywhere: the fact
    checker's copy strips that note on purpose, and this script reads only
    kaps/beskermde-woorde.json. On one Grade 6 lesson three of the writer's ten
    predicted protections were missing from the file -- a court's official name, a
    population term whose obvious swap reopened an ambiguity three rounds had
    closed, and one half of a pair whose swap works in both directions.

    This does NOT parse the note. A regex over Afrikaans prose that finds nothing
    reads exactly like a lesson with nothing to find, and this repository has
    already paid for that twice (see bin/verouderde-bestellings.py).
    """
    print("", file=sys.stderr)
    print("-" * 72, file=sys.stderr)
    print("VOOR JY DIT PLAK: lees die konsep se herkoms-nota.", file=sys.stderr)
    print("Die skrywer teken daarin aan watter woorde HY dink die taalnasiener sal", file=sys.stderr)
    print("omruil. Niks dra hulle hierheen - hierdie blok ken net", file=sys.stderr)
    print("kaps/beskermde-woorde.json. Elke woord in daardie nota wat nog nie in", file=sys.stderr)
    print("die lys staan nie, hoort daar MET SY REDE voordat die nasien loop.", file=sys.stderr)
    print("    %s" % pad, file=sys.stderr)
    print("-" * 72, file=sys.stderr)


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
    herinner(pad)
    if a.uit:
        with open(a.uit, "w", encoding="utf-8") as fh:
            fh.write(blok)
        print(f"written to {a.uit}")
    else:
        print(blok)


if __name__ == "__main__":
    main()

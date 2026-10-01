#!/usr/bin/env python3
"""
Lesson spec validator.

Run on the planner's output before any writing happens. Checks the arithmetic and
structural rules that a language model gets wrong reliably — budget sums, hour
allocations, missing CAPS items, unjustified Aanvulling — where they are cheap to
fix rather than twenty lessons later.

USAGE
    python3 spec_check.py spec.json
    python3 spec_check.py spec.json --json

Two budget bases live here, and a spec says which it uses.

"kaps-ure" is the CURRENT one (Drico, 29 September 2026): CAPS's printed hours for a
content cluster times the subject's own words-per-hour rate give that CLUSTER an
envelope, and the planner distributes inside it. Words never move between clusters,
the floor is 200 ("up to 200, or merge it"), a lifted lesson declares vloer_optel,
and there is no absolute per-grade ceiling.

"gemete_volume" and "vereistes" are the OLD bases, kept because every spec approved
before that date used one of them. Under those, CAPS contact hours are not used and
budgets divide evenly -- both rules were WITHDRAWN for new work on 29 September 2026.
"""
import argparse, json, re, sys

# Per-grade lesson budget band. DECIDED BY DRICO, 7 September 2026: Grade 4 caps at
# 450 study words with a floor of 350.
#
# Why a band exists at all, when the budget is supposed to be a measurement. The
# measurement was honest and the result was incoherent from a learner's seat: the
# delivered Gr 4 Natuurwetenskappe lessons run from 169 study words to 811, because
# textbook volume per sub-topic divided by lesson count is arithmetic and nobody
# chose the spread. Seventeen of twenty-five exceeded 450. A learner meeting a
# 169-word lesson one day and an 811-word one the next is the failure the band
# prevents, and the floor matters more than the ceiling.
#
# Grade 4 is also the first year learners write exams, which is Drico's own reason
# for the ceiling: the amount a nine-year-old is expected to study is small.
#
# GRADE 5 IS BANDED 300-550. DECIDED BY DRICO, 9 September 2026, and it is a wider
# band than Grade 4's on purpose, for two reasons he found by hand.
#
# First, lesson length genuinely varies. He counted a 140-word lesson and a 525-word
# one in the same Grade 5 book. A narrow band would force the short ones to pad, and
# padding is where invented claims come from -- most of the false mechanisms caught
# this year sat in text a writer had to produce to reach a number.
#
# Second, the measurement that sets a budget is inflated. profiler.py counts EVERY
# word on a page: activity boxes, question panels, captions, headings. Our lessons
# contain none of those -- activities belong to the layout team -- so we have been
# asking for a page's worth of words as pure prose. That is true of every subject
# measured so far, Grade 4 included; the delivered Grade 4 budgets stand, by his
# ruling, but nothing new should be built on the same basis.
#
# CONSEQUENCE FOR GRADE 5 SPECS: begroting_basis must be "vereistes", not
# "gemete_volume". A measured basis divides one number EVENLY and fails any lesson
# that differs from the average, which is exactly the uniformity this band exists to
# break. Under "vereistes" each lesson states its own number and a begrotingsnota
# saying where it came from -- and the band below still governs both bases.
#
# The floor is 300 rather than 140. A thin textbook page is usually one where a
# photograph does half the teaching, and our text is what a learner revises from
# alone, so it carries what the picture carried.
#
# GRADE 6 IS BANDED PER SUBJECT, because two rulings were made on the same day
# about different subjects and the table used to be per grade only.
#   * Lewensvaardighede: 450-550, decided by Lampies on 21 September 2026 -- one
#     step up from Grade 5's usual lesson, teaching lessons and reading pieces alike.
#   * Natuurwetenskappe en Tegnologie: the same 450-550, confirmed by Drico on
#     22 September 2026. His concern is the CEILING: over 550 asks for an effective
#     split, not a trim that drops content. A lesson that is short for a real reason
#     (Gr 6 NST lesson 30, the Moon) may sit below 450 with a vloer_uitsondering in
#     its spec saying why.
# LESBAND is the per-grade default; LESBAND_VAK overrides it for one subject.
#
# Grades 7-9 were decided by Lampies on 23 September 2026, for Lewensorientering:
# 350-700, and "die aantal woorde moet deur die inhoud bepaal word, moet nie
# oortollig van aard wees nie". It is a wide band on purpose: a CAPS block in the
# Senior Phase carries two to four hours of teaching, and how much a block really
# holds differs from block to block, so the content sets the number rather than an
# average. Grades 10-12 stay unbanded until someone decides them the same way,
# rather than inheriting a number that was reasoned about another grade.
LESBAND = {4: (350, 450), 5: (300, 550), 6: (450, 550), 7: (350, 700), 8: (350, 700), 9: (350, 700)}
LESBAND_VAK = {
    # Lampies, 1 Oktober 2026: Graad 7 Lewensorientering se plafon is van 700 na 750 gelig.
    # WAAROM: negentien van die sewe-en-veertig lesse het oor 700 gemeet, elkeen met 'n
    # toegestane uitsondering, en die uitsonderings het die plafon in die praktyk vervang.
    # 'n Plafon wat veertig persent van sy lesse vrystel, meet niks; 750 is wat die inhoud
    # werklik vra. Die vier lesse bokant 750 bly uitsonderings en word getel.
    # Net hierdie vak en net hierdie graad: ander Graad 7-vakke bly op 700, en Graad 4 tot 6
    # is afgelewer en word nie geraak nie.
    (7, "lewensorientering"): (350, 750),
}


def lesband_vir(graad, vak=None):
    import unicodedata
    s = unicodedata.normalize("NFKD", vak or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return LESBAND_VAK.get((int(graad), s), LESBAND.get(int(graad)))


def _kaps_ure_klusters(spec, lesse, fails, warns, notes):
    """Check the CAPS-hours budget basis (Drico, 29 September 2026).

    The envelope belongs to the CLUSTER, not the lesson: CAPS prints the hours,
    the subject's own rate turns them into words, and the planner distributes
    inside that. The one rule the arithmetic has to enforce is that WORDS NEVER
    MOVE BETWEEN CLUSTERS -- each cluster owns its allocation and can neither
    lend nor borrow. A 50-word shading across a cluster boundary was caught by
    hand on 29 September 2026, which is why this is checked and not trusted.

    A cluster whose hours are mostly PRACTICAL work is the method's one
    exception: hours times a rate over-budgets it badly (Gr 5 frame-and-shell
    structures, 8 3/4 hours of model building and short text). Such a cluster
    declares kluster_uitsondering and states what it budgeted instead.
    """
    tempo = spec.get("woorde_per_uur")
    if not isinstance(tempo, (int, float)) or tempo <= 0:
        fails.append("begroting_basis is 'kaps-ure' but woorde_per_uur is missing or not a "
                     "positive number. The rate is per SUBJECT and is not transferable — "
                     "Sosiale Wetenskappe is 250, Natuurwetenskappe nearer 125 — so it has to "
                     "be stated and sourced in begroting_basis_nota.")
        return

    klusters = {}
    for L in lesse:
        naam = (L.get("kaps_kluster") or "").strip()
        if not naam:
            fails.append(f"Lesson {L['nommer']}: begroting_basis is 'kaps-ure', so the lesson must "
                         f"name the CAPS cluster it draws from in kaps_kluster. Without it the "
                         f"envelope cannot be checked and words can drift between clusters unseen.")
            continue
        klusters.setdefault(naam, []).append(L)

    for naam, groep in sorted(klusters.items()):
        ure = {L.get("kluster_ure") for L in groep}
        if len(ure) != 1 or None in ure:
            fails.append(f"Cluster '{naam[:40]}': its {len(groep)} lesson(s) disagree about "
                         f"kluster_ure ({sorted(str(u) for u in ure)}). A cluster has one hour "
                         f"figure, printed in CAPS, and every lesson in it must repeat that figure.")
            continue
        u = ure.pop()
        if not isinstance(u, (int, float)) or u <= 0:
            fails.append(f"Cluster '{naam[:40]}': kluster_ure {u!r} is not a positive number.")
            continue
        som = sum(L["begroting"] for L in groep)
        koevert = round(u * tempo)
        # A cluster may exceed CAPS's hours by EXACTLY the floor top-ups it declares
        # and by nothing else. Drico, 29 September 2026: funding the 200-word floor by
        # shaving well-judged siblings is "a number nobody chose", which is the failure
        # the whole method was built to end -- so the envelope grows instead. It can
        # still not grow quietly: every extra word has to be named by the lesson that
        # needed it.
        optel = sum(int(L.get("vloer_optel") or 0) for L in groep)
        koevert += optel
        uitsondering = next((str(L.get("kluster_uitsondering") or "").strip() for L in groep
                             if str(L.get("kluster_uitsondering") or "").strip()), "")
        # rounding a share per lesson can move the sum by at most one word each
        if abs(som - koevert) > len(groep):
            verduidelik = (f"{u} CAPS hours x {tempo} words/hour"
                           + (f" plus {optel} declared floor top-up(s)" if optel else ""))
            boodskap = (f"Cluster '{naam[:40]}': its {len(groep)} lesson budgets sum to {som}, "
                        f"but {verduidelik} gives an envelope of {koevert}. "
                        f"Words may never move between clusters — redistribute inside this one, "
                        f"or state a kluster_uitsondering if the hours are mostly practical work.")
            (notes if uitsondering else fails).append(boodskap)
        elif uitsondering:
            notes.append(f"Cluster '{naam[:40]}' carries a stated exception and still lands on its "
                         f"envelope ({som} against {koevert}).")
        # "UP TO 200, OR MERGE IT" -- Drico, 29 September 2026. The floor is a minimum
        # and an alarm at once: a lesson that cannot honestly carry 200 words is not a
        # lesson. It is never met by padding. Filler in this pipeline becomes CLAIMS,
        # and claims are where nearly every error has come from -- a sentence written
        # to fill a gap is a sentence nobody needed to be true.
        for L in groep:
            if L["begroting"] < VLOER:
                fails.append(f"Lesson {L['nommer']}: budget {L['begroting']} is below the "
                             f"{VLOER}-word floor. Raise it to {VLOER} with a declared "
                             f"vloer_optel if the content honestly carries it, or MERGE the "
                             f"lesson into its neighbour. Never pad it to reach the floor.")
            elif L.get("vloer_optel") and L["begroting"] != VLOER:
                fails.append(f"Lesson {L['nommer']}: declares vloer_optel "
                             f"{L['vloer_optel']} but its budget is {L['begroting']}, not the "
                             f"{VLOER}-word floor. A top-up lifts a lesson TO the floor and no "
                             f"further — it is not a way to buy a cluster extra words.")
        opgetel = [L["nommer"] for L in groep if L.get("vloer_optel")]
        if opgetel:
            notes.append(f"Cluster '{naam[:40]}': lesson(s) {opgetel} lifted to the {VLOER}-word "
                         f"floor, {optel} words above CAPS's hours and declared as such.")

    if klusters:
        notes.append(f"{len(klusters)} CAPS cluster(s) at {tempo} words per hour, "
                     f"{sum(len(g) for g in klusters.values())} lessons between them.")


# The minimum a kaps-ure lesson may be budgeted at. Drico, 29 September 2026:
# "up to 200, or merge it". The text is what a learner revises from when the
# video is not in front of them, and a 120-word lesson cannot do that job.
VLOER = 200

AANVULLING_MAX_FRACTION = 0.25
# Aanvulling is capped by budget share, but a spec states items, not words. Two
# items in a 300-word lesson is already a quarter of it in practice, so the
# checker warns on count and leaves the word-level cap to the gate.
AANVULLING_ITEM_WARN = 2

REQUIRED_TOP = ["skema_weergawe", "vak", "graad", "kwartaal", "kaps_onderwerp",
                "kaps_subonderwerp", "fokusvraag", "profiel_konfig",
                "onderwerp_woorde", "totale_begroting", "lesse"]
REQUIRED_LES = ["nommer", "titel", "kaps_punt", "begroting", "kern",
                "fokusvraag_skakel"]


def split_named_items(bullet):
    """Pull explicitly named items out of a CAPS bullet.

    CAPS sometimes lists required items after a colon ('Sommige van die eerste
    seilskepe: Chinese junks, Arabiese dau(skip), ...'). Every named item is
    mandatory, so they must each appear in some kern entry.
    """
    if ":" not in bullet:
        return []
    tail = bullet.split(":", 1)[1]
    parts = [p.strip(" .") for p in tail.split(",")]
    return [p for p in parts if len(p) > 2]


def norm(s):
    """Loose comparison key — strips bracketed asides and generic filler words."""
    s = re.sub(r"\([^)]*\)", " ", s.lower())
    s = re.sub(r"[^a-zà-ÿ\s]", " ", s)
    drop = {"die", "n", "en", "van", "of", "ligte", "skip", "boot", "sommige",
            "eerste", "britse", "hoe", "maste", "met"}
    # Stem to a prefix: Afrikaans inflects freely (karveel / karvele, jonk /
    # junks), so exact word matching produces false alarms.
    return {w[:5] for w in s.split() if w and w not in drop and len(w) > 2}


# Spec fields that are read as prose. A planner that writes one as an object or a
# list used to crash the validator with AttributeError instead of failing cleanly --
# and a crash is the worst outcome here, because the runner reads this script's
# verdict to decide whether a spec may be used at all. Found 9 September 2026 by the
# Gr 5 Voedselkettings planner, which wrote a begrotingsnota as an object because the
# Grade 4 house style writes those notes that way. The path only became reachable
# with Grade 5: it runs solely under the "vereistes" budget basis.
#
# Coercing silently would be worse than crashing. An object note would read as an
# EMPTY note, and the planner would be told its note is missing while it is sitting
# right there in the wrong shape.
# CHECK ONLY WHAT IS ACTUALLY READ. The two budget-note fields are read solely under
# the "vereistes" basis; the other three are read for every spec. Checking the notes
# unconditionally failed two DELIVERED and previously valid Grade 4 specs
# (habitatte-van-diere, vaste-stowwe) whose begrotingsnota is an object in the Grade 4
# house style -- valid there precisely because a measured-volume spec never reads it.
# A validator must not invent a rule for a field its own logic ignores.
PROSA_ALTYD_SPEK = ("band_vrygestel",)
PROSA_ALTYD_LES = ("vloer_uitsondering", "plafon_uitsondering")
PROSA_VEREISTES_SPEK = ("begroting_basis_nota",)
PROSA_VEREISTES_LES = ("begrotingsnota",)


def _prosa_velde_is_teks(spec, fails):
    """Fail by name on a prose field that is not text, so nothing downstream strips it."""
    vereistes = spec.get("begroting_basis") in ("vereistes", "kaps-ure")

    def keur(houer, veld, waar):
        w = houer.get(veld)
        if w is None or isinstance(w, str):
            return
        houer[veld] = ""          # neutralise so the checks below cannot crash
        fails.append(
            f"{waar}'{veld}' is a {type(w).__name__}, but it is read as text. Write it as "
            f"one string. If it holds a breakdown, put the breakdown in a separate field "
            f"and keep this one prose — an object here would otherwise be read as an "
            f"empty note and reported as missing.")

    for veld in PROSA_ALTYD_SPEK + (PROSA_VEREISTES_SPEK if vereistes else ()):
        keur(spec, veld, "")
    for L in (spec.get("lesse") or []):
        if isinstance(L, dict):
            for veld in PROSA_ALTYD_LES + (PROSA_VEREISTES_LES if vereistes else ()):
                keur(L, veld, f"Lesson {L.get('nommer', '?')}: ")


def check(spec):
    fails, warns, notes = [], [], []
    _prosa_velde_is_teks(spec, fails)

    for f in REQUIRED_TOP:
        if f not in spec:
            fails.append(f"Missing required top-level field: {f}")
    if fails:
        return {"verdict": "FAIL", "failures": fails, "warnings": warns, "notes": notes}

    if spec["skema_weergawe"] != "1.0":
        warns.append(f"Spec schema version is {spec['skema_weergawe']}, expected 1.0")
    if not 4 <= spec["graad"] <= 12:
        fails.append(f"Grade {spec['graad']} outside 4–12")

    lesse = spec["lesse"]
    if not lesse:
        fails.append("No lessons in the spec")
        return {"verdict": "FAIL", "failures": fails, "warnings": warns, "notes": notes}

    for i, L in enumerate(lesse, 1):
        for f in REQUIRED_LES:
            if f not in L:
                fails.append(f"Lesson {i}: missing required field '{f}'")

    if any(fails):
        return {"verdict": "FAIL", "failures": fails, "warnings": warns, "notes": notes}

    # --- numbering ---
    nums = [L["nommer"] for L in lesse]
    if nums != list(range(1, len(lesse) + 1)):
        fails.append(f"Lesson numbers are {nums}, expected 1..{len(lesse)} in order")

    # --- budgets ---
    # Contact hours are deliberately NOT used. CAPS hours tell a teacher how long
    # to spend on a topic; they say nothing about how many words a learner reads,
    # because classroom time is filled with discussion, drawing and group work as
    # well as text. The budget anchor is measured textbook volume for the
    # sub-topic, divided evenly across its lessons.
    total_words = spec["onderwerp_woorde"]
    n = len(lesse)
    total = sum(L["begroting"] for L in lesse)

    # Two budget bases, declared by the spec. Added 2026-08-21.
    #
    # "gemete_volume" is the original and the default: measured textbook volume for
    # the sub-topic, divided EVENLY across its lessons. Evenness is not a style
    # preference there -- it is what dividing one measurement produces, so any
    # departure means someone typed a number instead of deriving one.
    #
    # "vereistes" exists because that assumption breaks. CAPS sometimes names a
    # topic and never specifies it: "Strukture van plante en diere" appears twice in
    # the Gr 4-6 science document, with two different spellings, and carries no
    # content section at all, while the term's assessment guidelines still require
    # plant parts and animal parts. There is no measured volume to divide, so the
    # budget comes from the number of things to be taught -- and then evenness is
    # meaningless: nine requirements about plants and thirteen about animals do not
    # want the same word count. Maths hits this too, where a textbook's word count
    # measures the prose between the diagrams rather than the teaching.
    #
    # Under "vereistes" the sum is NOT compared to onderwerp_woorde, because that
    # field is not the basis. Forcing the derived number into it to satisfy this
    # check is what made an earlier run print "measured sub-topic volume 250" for a
    # figure nobody measured -- a tool reporting an invention as a measurement.
    basis = spec.get("begroting_basis", "gemete_volume")
    if basis not in ("gemete_volume", "vereistes", "kaps-ure"):
        fails.append(f"begroting_basis '{basis}' is not one of gemete_volume, vereistes, kaps-ure")

    if basis == "gemete_volume":
        rou = round(total_words / n)
        # An exempted spec is judged by the rule that applied when it was written,
        # so the band must not clamp its expected budget either. Reporting the band
        # as notes while still failing the arithmetic would make the exemption
        # useless -- which it was, until habitatte-van-diere failed with the
        # exemption in place and every band check already downgraded.
        band = None if (spec.get("band_vrygestel") or "").strip() else lesband_vir(spec["graad"], spec.get("vak"))
        if band:
            vloer, plafon = band
            expected = max(vloer, min(plafon, rou))
        else:
            vloer = plafon = None
            expected = rou
        geklem = expected != rou

        for L in lesse:
            b = L["begroting"]
            if plafon and b > plafon:
                continue          # the ceiling is enforced below, for every basis
            if b != expected:
                verduidelik = (f"{total_words} words / {n} lessons = {rou}, clamped to {expected} "
                               f"by the Gr {spec['graad']} band {vloer}-{plafon}") if geklem else                               f"{total_words} words / {n} lessons = {expected}"
                fails.append(f"Lesson {L['nommer']} ('{L['titel'][:30]}'): budget {b} "
                             f"but {verduidelik}")

        if geklem:
            # Parity with the measurement is deliberately broken here, so checking it
            # would fail every banded spec. Say so out loud instead: a reader who
            # sees a total that is not the measured volume must be told it was chosen.
            rigting = "up to the floor" if expected > rou else "down to the ceiling"
            notes.append(
                f"Budgets are CLAMPED {rigting}: {total_words} measured / {n} lessons = {rou} "
                f"per lesson, set to {expected} by the Gr {spec['graad']} band {vloer}-{plafon}. "
                f"totale_begroting is therefore NOT the measured volume, on purpose.")
        else:
            # rounding can move the sum by at most one word per lesson
            if abs(spec["totale_begroting"] - total_words) > n:
                fails.append(f"totale_begroting {spec['totale_begroting']} differs from the measured "
                             f"sub-topic volume {total_words} by more than rounding allows")
    else:
        if not (spec.get("begroting_basis_nota") or "").strip():
            fails.append("begroting_basis is 'vereistes' but begroting_basis_nota is empty. A "
                         "budget that is not a measurement has to say where it came from.")
        for L in lesse:
            if not (L.get("begrotingsnota") or "").strip():
                fails.append(f"Lesson {L['nommer']}: begroting_basis is 'vereistes', so each "
                             f"lesson needs a begrotingsnota saying how its number was derived")
        if basis == "kaps-ure":
            notes.append(f"Budget basis is 'kaps-ure' (Drico, 29 September 2026): {n} lessons "
                         f"summing to {total} words. Each CAPS cluster's envelope is its hours "
                         f"times the subject rate, and the planner distributes inside it.")
            _kaps_ure_klusters(spec, lesse, fails, warns, notes)
        else:
            notes.append(f"Budget basis is 'vereistes': {n} lessons summing to {total} words, derived "
                         f"from requirement counts and NOT from measured volume. Even division is not "
                         f"enforced and onderwerp_woorde is not treated as the anchor.")

    if total != spec["totale_begroting"]:
        fails.append(f"Lesson budgets sum to {total}, but totale_begroting is "
                     f"{spec['totale_begroting']}")

    if basis != "kaps-ure" and ("kaps_ure" in spec or any("ure" in L for L in lesse)):
        notes.append("Hour fields present. They are informational only and are never used in "
                     "budget arithmetic.")

    # a budget too small to teach anything is a planning error, not a style choice
    # The band governs BOTH bases. Applying it only to gemete_volume left the
    # requirement-based specs -- the ones with no measurement to divide, which is
    # exactly where a number is most easily typed rather than derived -- outside the
    # only rule that constrains them.
    # Under 'kaps-ure' there is NO absolute per-grade band, by design: an absolute
    # ceiling contradicts a method whose whole point is that each lesson's length is
    # its own. A 120-word lesson and a 500-word one are both in order.
    band_hier = None if basis == "kaps-ure" else lesband_vir(spec["graad"], spec.get("vak"))
    vrygestel = (spec.get("band_vrygestel") or "").strip()
    for L in lesse:
        b = L["begroting"]
        if band_hier and b < band_hier[0]:
            # The floor has an exception too, and it needs one for the same reason the
            # ceiling does: sometimes the curriculum, not the arithmetic, decides.
            # Gr 4 Geskiedenis Kwartaal 1 is five introductory videos about what
            # history is and what a source is, and CAPS gives 7 of that term's 15
            # hours to a project rather than to content. Drico, 7 September 2026:
            # "Lets make term one 200 words, and treat it purly as an exception ...
            # there really is not that much to say here." Inflating those lessons to
            # 350 would pad them, which is the failure the floor exists to prevent
            # pointing the other way.
            if (L.get("vloer_uitsondering") or "").strip():
                notes.append(f"Lesson {L['nommer']} is under the {band_hier[0]}-word floor at "
                             f"{b}, with a stated exception.")
            else:
                boodskap = (f"Lesson {L['nommer']}: budget {b} is below the Gr {spec['graad']} "
                            f"floor of {band_hier[0]} with no vloer_uitsondering. The floor is "
                            f"the half of the band that matters most — a 169-word lesson is a "
                            f"worse failure than an 811-word one. Merge with an adjacent bullet, "
                            f"raise it to the floor, or say in writing why this content is "
                            f"genuinely thinner than a Grade 4 lesson should be.")
                (notes if vrygestel else fails).append(boodskap)
        elif band_hier and b > band_hier[1]:
            # A CAPS bullet that names items explicitly makes every one of them
            # mandatory, and that is not negotiable against a word count. Transport
            # water lesson 6 owes rafts, canoes and reed boats PLUS the five ships
            # CAPS names by name PLUS how a sail works. Such a lesson may go over the
            # ceiling, but it has to say so in writing rather than quietly.
            if (L.get("plafon_uitsondering") or "").strip():
                notes.append(f"Lesson {L['nommer']} is over the {band_hier[1]}-word ceiling at "
                             f"{b}, with a stated exception.")
            else:
                boodskap = (f"Lesson {L['nommer']} ('{L['titel'][:30]}'): budget {b} exceeds the "
                            f"Gr {spec['graad']} ceiling of {band_hier[1]} with no "
                            f"plafon_uitsondering. Only a bullet that names mandatory items "
                            f"explicitly may go over, and it must say which items force it.")
                (notes if vrygestel else fails).append(boodskap)
        elif b < 120:
            warns.append(f"Lesson {L['nommer']}: budget {b} is very small — "
                         f"consider merging with an adjacent bullet")
    if vrygestel:
        notes.append(f"BAND EXEMPT: {vrygestel}")

    # --- CAPS named items must all be covered ---
    for L in lesse:
        named = split_named_items(L["kaps_punt"])
        if not named:
            continue
        kern_keys = [norm(k) for k in L["kern"]]
        for item in named:
            key = norm(item)
            if not key:
                continue
            if not any(key & kk for kk in kern_keys):
                # Heuristic text match, so this warns rather than fails: Afrikaans
                # inflection and paraphrase make a hard verdict unsafe. A human or
                # the coverage checker confirms.
                warns.append(f"Lesson {L['nommer']}: cannot find a kern entry matching CAPS's "
                             f"named item '{item}' — explicitly named items are mandatory, "
                             f"so check this one by eye")
        if len(named) >= 4 and not L.get("termdig"):
            warns.append(f"Lesson {L['nommer']}: CAPS names {len(named)} items but termdig is "
                         f"not set — the writer will not plan for a heavy glossary")

    # --- kern sanity ---
    for L in lesse:
        if not L["kern"]:
            fails.append(f"Lesson {L['nommer']}: kern is empty — nothing for the writer to cover")
        elif len(L["kern"]) > 10:
            warns.append(f"Lesson {L['nommer']}: {len(L['kern'])} kern items in "
                         f"{L['begroting']} words is roughly "
                         f"{L['begroting'] // len(L['kern'])} words each — likely too thin per item")

    # --- aanvulling ---
    for L in lesse:
        av = L.get("aanvulling") or []
        for a in av:
            if not isinstance(a, dict) or "item" not in a or "regverdiging" not in a:
                fails.append(f"Lesson {L['nommer']}: aanvulling entries need both 'item' and "
                             f"'regverdiging'")
            elif len(a["regverdiging"].split()) < 8:
                warns.append(f"Lesson {L['nommer']}: justification for '{a['item'][:30]}' is very "
                             f"short — the test is whether the concept would be incomplete without it")
        if len(av) > AANVULLING_ITEM_WARN:
            allowance = int(L["begroting"] * AANVULLING_MAX_FRACTION)
            warns.append(f"Lesson {L['nommer']}: {len(av)} aanvulling items against a "
                         f"{allowance}-word allowance — check the 25% cap still holds")

    # --- difficult-concept flags ---
    #
    # This used to warn that no lesson flags a difficult concept, on the grounds that
    # every sub-topic usually needs an ELI10 layer. The ELI10 block was abolished, and
    # the gate now HARD-FAILS any lesson that carries one — so the advice sent whoever
    # followed it straight into a gate failure. An empty difficult-concepts field is now
    # an ordinary outcome and says nothing, so nothing is reported for it.
    # The count check below stays: it is about a flag that means nothing when everything
    # carries it, which is still true whatever the flag is used for.
    for L in lesse:
        if len(L.get("moeilike_konsepte") or []) > 3:
            warns.append(f"Lesson {L['nommer']}: {len(L['moeilike_konsepte'])} concepts flagged "
                         f"as difficult — flagging everything makes the flag meaningless")

    # --- focus question link ---
    for L in lesse:
        if len((L.get("fokusvraag_skakel") or "").split()) < 6:
            warns.append(f"Lesson {L['nommer']}: fokusvraag_skakel is very short — if it cannot "
                         f"be stated, the lesson may not serve the CAPS focus question")

    return {
        "verdict": "FAIL" if fails else "PASS",
        "vak": spec["vak"], "graad": spec["graad"],
        "subonderwerp": spec["kaps_subonderwerp"],
        "lessons": len(lesse),
        "total_budget": spec["totale_begroting"],
        "subtopic_words": spec["onderwerp_woorde"],
        "budget_basis": spec.get("begroting_basis", "gemete_volume"),
        "failures": fails, "warnings": warns, "notes": notes,
    }


def main():
    ap = argparse.ArgumentParser(description="Validate a Wolkskool lesson spec")
    ap.add_argument("spec")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    r = check(spec)

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"\n{r['verdict']}  —  {r.get('subonderwerp','(unknown)')} "
              f"(Gr {r.get('graad','?')})")
        if r["verdict"] != "FAIL" or "lessons" in r:
            # Never call a derived number a measurement. Under the "vereistes"
            # basis onderwerp_woorde is not the anchor, so printing it as
            # "measured" states something false about where the budget came from.
            if r.get("budget_basis") == "vereistes":
                herkoms = "derived from requirement counts, NOT measured"
            elif r.get("budget_basis") == "kaps-ure":
                herkoms = "from CAPS hours x the subject rate, NOT measured"
            else:
                herkoms = f"measured sub-topic volume {r.get('subtopic_words','?')}"
            print(f"\n  {r.get('lessons','?')} lessons, "
                  f"{r.get('total_budget','?')} words total ({herkoms})")
        for x in r["failures"]:
            print(f"\n  FAIL  {x}")
        for x in r["warnings"]:
            print(f"  warn  {x}")
        for x in r["notes"]:
            print(f"  note  {x}")
        print()

    sys.exit(1 if r["verdict"] == "FAIL" else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Where everything lives.

One module so that the runner, the setup script and the log reader cannot
disagree about a path. Every location that matters to the pipeline is derived
here from a subject, a grade and a CAPS sub-topic, so a path always states its
own CAPS location:

    goedgekeur/gr4/sosiale-wetenskappe/vervoer-op-water/les-3.json

Two locations are deliberately outside the repository:

  goedgekeur/   the approved-output boundary. Neither team owns it and neither
                reaches into the other's tree. The HTML team reads it; nothing
                in this repository writes to it except an approval, and nothing
                ever edits a file already in it.
  skrapruimte/  OCR scratch. Hundreds of temp files per profiler run must not
                land in the repository (a rasterised textbook page in git is the
                one thing the copyright discipline exists to prevent) and must
                not land in a synced folder such as OneDrive.
"""
import glob
import hashlib
import json
import os
import re
import unicodedata

SKILL_NAME = "wolkskool-inhoudstandaard"
SKEMA_WEERGAWE = "1.0"

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKILL = os.path.join(REPO, "skills", SKILL_NAME)
SCRIPTS = os.path.join(SKILL, "scripts")
PROMPTS = os.path.join(REPO, "prompts")
PROFIELE = os.path.join(REPO, "profiele")
KAPS = os.path.join(REPO, "kaps")
SPESIFIKASIES = os.path.join(REPO, "spesifikasies")
SPEK_KONSEP = os.path.join(SPESIFIKASIES, "konsep")
SPEK_GOEDGEKEUR = os.path.join(SPESIFIKASIES, "goedgekeur")
KONSEPTE = os.path.join(REPO, "konsepte")
LOGS = os.path.join(REPO, "logs")
GATE_LOG = os.path.join(LOGS, "gate_log.jsonl")
HARDLOOP_LOG = os.path.join(LOGS, "hardloop_log.jsonl")
VERSLAE = os.path.join(LOGS, "verslae")

# Outside the repository. Overridable so a second machine or a test run does not
# have to match this one.
SKRAPRUIMTE_DEFAULT = ("C:/temp/wolkskool-scratch" if os.name == "nt"
                       else "/tmp/wolkskool-scratch")

# Where an Afrikaans hunspell dictionary is looked for. Optional throughout:
# spelling is a warning-level check because Afrikaans compounds freely and no
# dictionary keeps up, so its absence must never stop the gate.
HUNSPELL_KANDIDATE = ["C:/hunspell/af_ZA", "/usr/share/hunspell/af_ZA"]

REVISIE_MAKS = 2          # revision cycles before the human is asked
BEGROTING_TOLERANSIE = 0.15


def skrapruimte():
    return os.environ.get("WOLKSKOOL_SCRATCH") or SKRAPRUIMTE_DEFAULT


def hunspell_pad():
    """The dictionary base path if one is installed, else None."""
    env = os.environ.get("WOLKSKOOL_HUNSPELL")
    for base in ([env] if env else HUNSPELL_KANDIDATE):
        if base and os.path.exists(base + ".aff") and os.path.exists(base + ".dic"):
            return base
    return None


# ------------------------------------------------------------------ slugs
def slug(text):
    """ASCII-safe path segment. 'Vervoer op water' -> 'vervoer-op-water'.

    Diacritics are folded rather than dropped, so 'hoë skepe' becomes
    'hoe-skepe' and not 'ho-skepe'.
    """
    s = unicodedata.normalize("NFKD", str(text))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("'", "").replace("\u2019", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-")


def kaps_pad(graad, vak, subonderwerp):
    """The shared 'gr4/sosiale-wetenskappe/vervoer-op-water' fragment."""
    return os.path.join(f"gr{int(graad)}", slug(vak), slug(subonderwerp))


# ------------------------------------------------------------------ specs
def spek_konsep(graad, vak, subonderwerp):
    """Where the planner writes. Not readable by the pipeline."""
    return os.path.join(SPEK_KONSEP, f"gr{int(graad)}", slug(vak),
                        slug(subonderwerp) + ".json")


def spek_goedgekeur(graad, vak, subonderwerp):
    """Where a human puts a spec they have read and accepted.

    Approval is a location, not a field, for the same reason it is a location for
    lessons: an agent can set a status field and cannot move a file into a folder
    a human controls.
    """
    return os.path.join(SPEK_GOEDGEKEUR, f"gr{int(graad)}", slug(vak),
                        slug(subonderwerp) + ".json")


# ------------------------------------------------------------------ drafts
def konsep_gids(graad, vak, subonderwerp):
    return os.path.join(KONSEPTE, kaps_pad(graad, vak, subonderwerp))


def les_konsep(graad, vak, subonderwerp, nommer):
    return os.path.join(konsep_gids(graad, vak, subonderwerp), f"les-{int(nommer)}.json")


# A draft is named `les-<number>.json`, and every other artifact of that lesson is
# a SIBLING built by newe() below -- les-3.hek.json, les-3.dekking.json,
# les-3.feite.json, les-3.staat.json, and since 7 October 2026 also
# les-3.aanvaardings.json, the dated record accepting one unresolvable fact.
#
# is_les_konsep is the one place that question is answered, because the answer does
# not live in a list of suffixes. bin/feitekopie.py asked it with its own list of
# the four report suffixes, the acceptance record was not on that list, and the
# script reported NINE copies for an eight-lesson sub-topic and wrote a stripped
# "fact copy" of a record. A wrong count has misled us before: a spec extract
# shares a draft's name, so a glossary sweep counted both and reported exactly
# double, and the count is the whole point of printing it.
#
# So this asks the POSITIVE question and keeps no exclusion list at all. A list of
# what to skip loses to every sibling invented after it was written; the name of a
# draft does not change, and newe() can only ever add a second dot. Four scripts
# had each written this same `les-<digits>` test for themselves and a fifth an
# equivalent one -- so the rule was already right in five places and wrong in two,
# each in its own way, which is exactly what one shared predicate prevents.
LES_KONSEP_NAAM = re.compile(r"les-\d+\.json\Z")


def is_les_konsep(pad):
    """Is this path a lesson draft, rather than one of its siblings?

    Name only. It says nothing about which directory the file is in, because a
    spec extract and a fact copy are named EXACTLY like a draft -- see
    AFGELEIDE_GIDSE, which is the part no name test can do.
    """
    return LES_KONSEP_NAAM.match(os.path.basename(pad)) is not None


# Directories under konsepte/ whose files are named like drafts without being
# drafts: the spec extract the writer reads, and the stripped copy the fact
# checker reads. Both are `les-<n>.json`, so only their location tells them apart.
AFGELEIDE_GIDSE = ("spek", "feite-kopie")


def les_konsepte(wortel):
    """Every lesson draft under a root, in path order."""
    for gids, subgidse, lers in os.walk(wortel):
        subgidse[:] = [s for s in subgidse if s not in AFGELEIDE_GIDSE]
        for naam in sorted(lers):
            if is_les_konsep(naam):
                yield os.path.join(gids, naam)


def spek_inskrywing(graad, vak, subonderwerp, nommer):
    """The one lesse entry the writer and the coverage checker are given.

    Kept in a spek/ subdirectory rather than beside the draft. The fact checker is
    handed the draft and nothing else — it must judge what the lesson says, not
    what it was meant to say — and a spec sitting next to the draft is an
    invitation. Tool permissions cannot enforce that boundary, so the layout does
    what it can and the agent prompt does the rest.
    """
    return os.path.join(konsep_gids(graad, vak, subonderwerp), "spek",
                        f"les-{int(nommer)}.json")


# What a fact checker may see of a draft's provenance. Everything else under
# `herkoms` is withheld. See skryf_feitekopie -- this is an allowlist on purpose.
HERKOMS_BEHOU = ("kaps_dokument", "skrywer_prompt", "handboek_gesien",
                 "videoskrif_gesien")

# Of the sign-off block, only what identifies the approval. `nota` narrates every
# earlier round and `nasiens` carries the previous verdicts; both are exactly what
# the fact checker must not have. Added 22 September 2026.
GOEDKEURING_BEHOU = ("datum", "deur")


def feitekopie(les_pad):
    """The copy of a draft the fact checker is given: the lesson without its
    provenance note.

    The spek/ layout above keeps the specification away from the fact checker,
    but the draft itself carries the intent. Writers record their reasoning in
    herkoms.nota — why a sentence was cut, what a requirement asked for, what
    was deliberately left out — and they are right to: it is how a decision
    survives to the next revision, and several corrections have been saved by it.

    But the fact checker is handed the draft, so it reads that reasoning, and the
    charitable-reading risk arrives through the back door. It gets worse with
    every revision, because each pass appends its own reasoning — so the
    most-corrected lessons, the ones that most need an honest check, leak most.
    Two fact checkers raised it unprompted; one said it read the note before it
    could avoid it.

    Drico's decision, 9 September 2026: strip it here rather than ask writers not
    to write it. The runner already decides what each checker sees, and this is
    the same decision.

    16 September 2026: that decision stripped one key by name, `herkoms.nota`,
    and writers also write `herkoms.hersieningsnota`, which does the identical
    job -- it quotes the requirement a revision served, in capitals, along with
    warnings lifted from the specification's own risk notes. It went straight
    through for a week. A fact checker read one and said so, exactly as two did
    about the original leak.

    So this no longer names the fields it removes. It names the ones a checker
    may keep and drops everything else under `herkoms`. A list of what to remove
    loses to every field name invented after it was written; a list of what to
    keep does not.

    18 September 2026: the leak turned up again, inside a field the allowlist
    KEEPS. `profiel_konfig` is meant to name a measurement config. Writers had
    been writing their own reasoning into it -- which config the brief named,
    what the SPECIFICATION says about the budget basis, who decided a number and
    when. Twelve lessons across four subjects, and a fact checker read one and
    said so, which is now the fourth checker to raise this unprompted.

    So `profiel_konfig` is out. Asking the allowlist question properly -- what is
    this checker ENTITLED to see? -- answers it: a fact checker verifies claims
    against outside sources and has no use for budget provenance at all. What
    remains names the curriculum document, the writer prompt and the two "did you
    look at it" records, and none of those is a place a writer reasons.

    The lesson generalises: an allowlist is only as good as the assumption that
    each kept field holds an identifier rather than prose. Check that the fields
    you keep cannot carry a sentence.
    """
    return os.path.join(os.path.dirname(les_pad), "feite-kopie",
                        os.path.basename(les_pad))


def feitekopie_inhoud(les):
    """The fact checker's copy of a draft, as data.

    Pure, and the ONLY definition of what a copy contains. 1 October 2026: the
    staleness test in vernuwe-uittreksels.py used to keep its own list of the
    fields withheld here, and the list held `herkoms` but not `goedkeuring`. So
    every signed-off lesson's copy compared unequal to its draft for ever, was
    reported stale on every run, and was rewritten byte for byte identically --
    exactly the "report every copy stale and train everyone to ignore it"
    failure that test was written to prevent. A caller that needs to know what a
    copy holds calls this; nobody keeps a second list.
    """
    weg = 0
    h = les.get("herkoms")
    if isinstance(h, dict):
        uit = [k for k in h if k not in HERKOMS_BEHOU]
        if uit:
            weg += len(uit)
            h = {k: v for k, v in h.items() if k in HERKOMS_BEHOU}
            les = dict(les, herkoms=h)

    # 22 September 2026: the same leak, through a field nobody had looked at.
    # `goedkeuring` is written at sign-off, not by the writer, so it survived a
    # rule aimed at herkoms. Its `nota` is a narrative of every earlier round --
    # what was found, what was decided, which specification fields carried a
    # claim -- and `nasiens` hands over the previous verdicts, which is direct
    # pressure to read charitably. A fact checker read one and said so, which is
    # the third time a checker has reported this leak through a new field.
    #
    # Keep only what identifies the approval. The date and the approver tell a
    # checker nothing about what the lesson is supposed to mean.
    g = les.get("goedkeuring")
    if isinstance(g, dict):
        uit = [k for k in g if k not in GOEDKEURING_BEHOU]
        if uit:
            weg += len(uit)
            les = dict(les, goedkeuring={k: v for k, v in g.items()
                                         if k in GOEDKEURING_BEHOU})

    if weg:
        h2 = dict(les.get("herkoms") or {})
        h2["nota_weerhou"] = (
            "Notas en vorige uitslae is uit hierdie kopie weerhou (%d veld(e)). Hulle dra die "
            "skrywer se redenasie, die spesifikasie se vereistes en vorige nasieners se "
            "uitslae, en die feitenasiener moet beoordeel wat die les SE, nie wat dit bedoel "
            "het nie en nie wat al voorheen goedgekeur is nie. Niks is uit die lesinhoud "
            "verwyder nie." % weg)
        les = dict(les, herkoms=h2)
    return les


def skryf_feitekopie(les_pad):
    """Write the fact checker's copy and return its path.

    Regenerated on every call, because the draft moves. The marker left behind
    is deliberate: without it a checker meets a lesson with no note and reports
    that something dropped it, which one did before this existed. The marker
    says a note was withheld and says nothing about what it contained.

    7 October 2026: it refuses anything that is not a lesson draft. A caller that
    walked for `les-*.json` handed it an acceptance record, and it dutifully wrote
    a stripped copy of one into feite-kopie/ -- debris that then counted as a
    lesson copy in the next tool's own total. Filtering in the callers leaves the
    next caller free to make the same file, so the refusal belongs here, in the
    one function that creates a copy.
    """
    if not is_les_konsep(les_pad):
        raise ValueError(
            "skryf_feitekopie is only for a lesson draft named les-<n>.json, not "
            "for %s. A sibling of a draft (a report, or the acceptance record) has "
            "no fact copy." % os.path.basename(les_pad))
    pad = feitekopie(les_pad)
    skryf_json(pad, feitekopie_inhoud(lees_json(les_pad)))
    return pad


# ------------------------------------------------- record markers in a spec field
#
# A specification field is written to be read from the top: every order first, then
# one line saying the rest is a record and orders nothing. Two sweeps have to know
# where that record half begins -- bin/verouderde-bestellings.py, which reports
# fields that have collected corrections without being rewritten, and
# bin/spekbestelling.py, which reports a wording forbidden above the marker and
# ordered below it.
#
# Until 8 October 2026 each kept its own vocabulary and neither knew the other's,
# measured that day over all 91 approved specs:
#
#   * spekbestelling knew REGGEMAAK, TERUGGETREK, BYGEVOEG, HERSKRYF, AANGETEKEN,
#     OORWEEG EN BEHOU, OORWEEG EN AFGEWYS and 'REKORD, NIE BESTELLING NIE', and did
#     NOT know the canonical line at all. 89 fields in 9 specs carry the canonical
#     line and no legacy form, so a field written in the house shape was invisible
#     to it -- including 29 of the 30 canonical markers written into
#     gr6/sosiale-wetenskappe/mapungubwe.json on 7 October 2026, which became
#     visible to the first sweep and invisible to the second in one stroke.
#   * verouderde-bestellings knew the canonical line plus REGGESTEL, REGGEMAAK,
#     TERUGGETREK, VERBREED, GEKWALIFISEER, OMVANG VERNOU, AANGEVUL, TYDGEMERK,
#     OPGEHELDER, HERBEVESTIG, TWEEDE REGSTELLING and 'Bygevoeg <digit>' -- so six
#     of spekbestelling's eight forms counted as nothing at all, and its own
#     buried-order check could only ever run on the 22 specs that use the canonical
#     line.
#
# So the vocabulary lives here once and both import it. Neither script keeps a
# second copy: a guard that paraphrases the rule it checks has cost us a check that
# cried wolf on three files for ever while being blind to thirty.
#
# THE CASE OF EVERY FORM IS LOAD-BEARING AND NOTHING HERE IS COMPILED WITH re.I. In
# these fields case IS the signal: capitals mark a structure, and the same word in
# lower case is ordinary Afrikaans prose which often means the opposite.
# 'ALLES HIERONDER' matched case-insensitively also hits 'Alles hieronder bly geld',
# which says the exact opposite -- that everything below still orders. Measured over
# the 91 specs on 8 October 2026: 'teruggetrek' appears 348 times in lower case
# against 313 in capitals, 'verbreed' 150 against 49, 'bygevoeg' 378 against 276.
REKORD_HERSKRYFLYN = "ALLES HIERONDER"

# Forms that open a record on their own. Measured 8 October 2026: none of these is
# ever written as the verb of a live order in the 91 specs. Several sit inside a
# sentence that CONTAINS a prohibition -- 'REGGEMAAK 29 SEPTEMBER 2026: MOENIE X NIE'
# is the house shape for recording a correction whose content is the new prohibition,
# 30 such sentences -- and that is a record opening with the order it replaced, which
# is exactly what the marker is for.
REKORDMERKERS = (
    REKORD_HERSKRYFLYN,
    "REKORD, NIE BESTELLING NIE",
    "REGGEMAAK", "REGGESTEL", "TERUGGETREK", "AANGETEKEN",
    "OORWEEG EN BEHOU", "OORWEEG EN AFGEWYS",
    "GEKWALIFISEER", "OMVANG VERNOU", "AANGEVUL", "TYDGEMERK", "OPGEHELDER",
    "HERBEVESTIG", "TWEEDE REGSTELLING",
)

# Forms the house ALSO writes as an ordinary verb, in capitals, inside a live order.
# These count only in their dated shape: the word, an optional comma, and a date.
# Measured 8 October 2026, and this is the one decision here that was not simply a
# union of the two old lists:
#
#   HERSKRYF   102 occurrences, 52 dated. Three of the undated ones are the verb of a
#              live prohibition -- 'MOENIE DIE ELI10 SE VUURKAS-PRENTJIE HERSKRYF
#              NIE', 'MOENIE HIERDIE BLOK WEER LAAT HERSKRYF VOORDAT ... NIE' twice.
#   BYGEVOEG   276 occurrences, 234 dated. Undated ones include "DIE OPSOMMINGSLYS SE
#              PAAR-REeL MAG NIE 'WANNEER HITTE BYGEVOEG WORD' Se NIE", an order
#              about heat. verouderde-bestellings already required a digit here, as
#              'Bygevoeg \d'; this generalises that rule rather than inventing one.
#   VERBREED   49 occurrences and only THREE dated. The rest are capitalised prose or
#              orders: 'MOENIE DIT VERBREED NIE', 'MOENIE VERDER VERBREED NIE',
#              'VERBREED DIE GROND, HOU VELKLEUR AS DIE VOORBEELD'. It was a bare
#              marker in verouderde-bestellings, which means that sweep has been
#              truncating orders at those sentences; requiring the date fixes that and
#              keeps all three real records.
#
# An order read as a record is worse than a record read as prose, because the sweeps
# then treat a live order as record text -- so a form whose undated occurrences are
# not all records belongs here, not above.
REKORDMERKERS_GEDATEER = ("BYGEVOEG", "Bygevoeg", "HERSKRYF", "VERBREED")

_GEDATEERDE_VORM = r"(?:%s),?\s+\d" % "|".join(REKORDMERKERS_GEDATEER)
REKORDMERKER_PATROON = re.compile(
    "|".join([re.escape(m) for m in REKORDMERKERS] + [_GEDATEERDE_VORM]))

# Forms this house also opens a record with, which neither list above knows. Measured
# 13 October 2026 across the 91 specs: 318 fields in 51 files hold a record opening with
# one of these INSIDE a live ordering half, so the wording each quotes as withdrawn reads
# as an order, and no sweep has ever named them.
#
# They are deliberately NOT added to the two lists above, and the reason is a measurement,
# not caution. Bare, they appear 808 times as the verb of a live order against 151 times
# dated -- 'DIE KIEME-OMSKRYWING IS REEDS BESLIS', 'DRIE DINGE WAT NIE BESLEG KON WORD
# NIE', 'LET OP DIE TWEE MANIERE WAAROP 'n REGSTELLING HIERVAN VERKEERD KAN LOOP'. A bare
# list would truncate those 808 ordering halves. And even the dated shape may not go into
# REKORDMERKERS_GEDATEER, because that list feeds REKORDMERKER_PATROON and therefore
# eerste_rekordmerker: the boundary would move in all 318 fields at once, silently
# demoting every live order standing after the first dated word in each.
#
# So these count for FINDING a field a person must read, and never for deciding where a
# field's record half begins. The boundary moves only when a person writes the canonical
# line, which is the one mark that states the author's own intent.
REKORDMERKERS_RUIM = (
    "REGSTELLINGS", "REGSTELLING", "KWANTIFISEERDER VERNOU", "BESLIS", "BESLEG",
    "NAGEGAAN", "BYGEWERK", "GEWYSIG", "VERVANG", "UITGEHAAL", "BEVESTIG",
    "OPGESKORT", "ONTTREK", "GESKRAP", "bygeskryf", "reggestel",
)

_RUIM_MAANDE = (r"Januarie|Februarie|Maart|April|Mei|Junie|Julie|Augustus|September|"
                r"Oktober|November|Desember|Jan|Feb|Mrt|Apr|Jun|Jul|Aug|Sept|Sep|"
                r"Okt|Nov|Des")
# The date is the whole discriminator, so it is required in full: a day, a month name and
# a year. 'BESLIS 3 September 2026' is a record; 'REEDS BESLIS' is an order.
RUIM_REKORD_PATROON = re.compile(
    r"(?:%s)\w*[,:]?\s+(?:op\s+)?\d{1,2}\s+(?:%s)\w*\s+\d{4}"
    % ("|".join(re.escape(w) for w in REKORDMERKERS_RUIM + REKORDMERKERS
                if w != REKORD_HERSKRYFLYN), _RUIM_MAANDE),
    re.IGNORECASE)


def ruim_rekords(teks):
    """Dated record openings the narrow vocabulary cannot see, as (index, form).

    For REPORTING only -- see REKORDMERKERS_RUIM. Never use this to split a field.
    """
    return [(m.start(), m.group(0)) for m in RUIM_REKORD_PATROON.finditer(teks)]


def ongemerkte_rekords(teks):
    """Dated records sitting in this field's ORDERING half, as (index, form).

    These are two different faults and a caller should tell them apart with
    is_rekord_herskryf, because the repair differs. Measured 13 October 2026:

      no canonical line at all -- 381 fields, and nobody has ever drawn that field's
      boundary, so every record it holds is being read as a live order right now.
      Heaviest in gr4 (142) and gr7 (100).

      canonical line present, record ABOVE it -- 88 fields. A person drew the line and
      left a record in the ordering half. eerste_rekordmerker is right not to cut
      there, since the canonical line is the author's own mark, but a writer reading
      top-down still meets that record as an order. Almost all of these are gr5 (43)
      and gr6 (43), which are the grades where the line was adopted.

    This counts dated records only, so a field it names is a field to READ, not a field
    proven broken -- whether an order above a record has gone stale is a question about
    meaning that no pattern can answer.
    """
    grens = eerste_rekordmerker(teks)
    bo = teks if grens < 0 else teks[:grens]
    return [(i, vorm) for i, vorm in ruim_rekords(bo)]


def is_rekord_herskryf(teks):
    """Does this field carry the canonical line, so somebody has read it end to end?

    This is the one question the canonical line answers and no other form does. It
    says, in the field's own words, that NOTHING below it orders anything -- which is
    why verouderde-bestellings skips these fields when it looks for orders that have
    gone stale, and why its buried-order check looks ONLY at these fields. A legacy
    marker makes no such promise: the house legitimately writes the new prohibition
    inside a dated record, so an imperative below a 'REGGEMAAK ...' line is ordinary,
    and an imperative below the canonical line is a fault. Do not widen either of
    those two tests to the whole list.
    """
    return REKORD_HERSKRYFLYN in teks


def rekordmerkers(teks):
    """Every record marker in a field, as (index, form), in the order they appear."""
    return [(m.start(), m.group(0)) for m in REKORDMERKER_PATROON.finditer(teks)]


def tel_rekordmerkers(teks):
    """How many dated records a field has collected."""
    return sum(1 for _ in REKORDMERKER_PATROON.finditer(teks))


def eerste_rekordmerker(teks):
    """Where the record half starts, or -1 when the whole field orders.

    The canonical line wins whenever it is present, even if a legacy form appears
    above it. It is the authoritative boundary a person drew after reading the field,
    and the half above it may legitimately hold earlier records as well as orders;
    cutting at the first legacy word instead would throw away everything between.
    """
    i = teks.find(REKORD_HERSKRYFLYN)
    if i >= 0:
        return i
    m = REKORDMERKER_PATROON.search(teks)
    return m.start() if m else -1


def orde_helfte(teks):
    """The part of a field that orders: everything above the first record marker."""
    i = eerste_rekordmerker(teks)
    return teks[:i] if i >= 0 else teks


def newe(les_pad, agtervoegsel):
    """A sibling artifact of a draft: les-3.json -> les-3.<agtervoegsel>.json"""
    return les_pad[:-len(".json")] + f".{agtervoegsel}.json"


def hek_verslag(les_pad):
    return newe(les_pad, "hek")


def dekking_verslag(les_pad):
    return newe(les_pad, "dekking")


def feite_verslag(les_pad):
    return newe(les_pad, "feite")


def staat_pad(les_pad):
    return newe(les_pad, "staat")


# ------------------------------------------- the two halves of a spec extract
#
# Fixing a finding at its source grows the specification, and the per-lesson extract
# grows with it. One sub-topic's spec went from 75 KB to 267 KB in three days in
# October 2026 and its extract reached 137 KB, of which about 40 per cent was record
# text standing BELOW a line that says, in its own words, that nothing beneath it
# orders anything. A writer stops reading long before that, so the orders were being
# buried under the record of orders already withdrawn -- and orders-only working
# copies were being built BY HAND for every writer round to keep them readable.
#
# So an extract is written as TWO files, on the same field paths:
#
#   spek/les-3.json           every field cut at its record marker. The writer's
#                             reading, at the path and under the name that every
#                             brief, agent and tool already names.
#   spek/les-3.rekords.json   the halves below those markers. The coverage checker
#                             is given this one as well, because finding a stale
#                             order IS reading an order against the record below it,
#                             and that comparison is its job and nobody else's.
#
# Measured over all 387 extracts on 12 October 2026: 2 268 of 67 396 string fields
# carry a record half, and 1 977 of them are split here. That moves 3.14 million of
# the 17.09 million characters in an extract's strings, 2.89 million net of the marker
# notes that stay behind -- 15 per cent off what a writer reads across the repository,
# and 46 per cent off the worst single lesson, 121 KB down to 66 KB. The other 291
# fields stay whole, for the reason in _verdeel_waarde.
#
# THE CANONICAL LINE STAYS IN THE ORDERS FILE, and that is not cosmetic.
# eerste_rekordmerker prefers that line but FALLS BACK to the legacy marker words, and
# those legitimately stand inside an ordering half: 171 of the split fields carry a
# legacy word ABOVE their canonical line. Truncate such a field and drop the line, and
# the boundary silently moves up to the first legacy word -- everything between it and
# the real cut then reads as ordering nothing, in the one file a writer obeys. An
# assertion over all 387 caught that; reading the output would not have.
REKORD_UITTREKSEL_AGTERVOEGSEL = "rekords"

# What stands where the record half was. It opens with the canonical line itself, built
# from the constant above so the line the sweeps look for and the line written here can
# never drift apart, and the note sits BELOW it. Nothing is inserted ABOVE it: the
# ordering half has to stay byte-identical to orde_helfte of the undivided field, or
# the two files no longer reconstruct it.
REKORD_VERSKUIF = (REKORD_HERSKRYFLYN + " IS 'n REKORD EN BESTEL NIKS. Die rekord self "
                   "staan op dieselfde plek in %s. Niks is weggegooi nie.")

REKORD_UITTREKSEL_NOTA = (
    "Hierdie lêer dra die REKORDHELFTES van %s se velde, elkeen gesny by sy eie "
    "rekordmerker. NIKS HIERIN BESTEL IETS NIE. Dit staan apart sodat die bestellings "
    "kort genoeg bly om van bo af gelees te word, en sodat 'n verouderde bestelling "
    "gevind kan word soos sy altyd gevind word: lees die bestelling in %s en dan die "
    "rekord op dieselfde plek hier. Die veldname en die indekse is dieselfde as daar; "
    "'n veld wat hier ontbreek, het geen rekord nie, en 'n null in 'n lys beteken "
    "daardie item het geen rekord nie.")

_GEEN_REKORD = object()      # distinct from None, which a field may legitimately be


def rekord_uittreksel(uittreksel_pad):
    """The record halves beside an extract: spek/les-3.rekords.json.

    One extra dot, like every other sibling in this repository, so is_les_konsep
    still refuses it and no tool walking for `les-<n>.json` can mistake it for a
    draft or for the extract itself. bin/beweringveeg.py globs `spek/les-*.json`
    and had to be told the difference; it is the only one that did.
    """
    return newe(uittreksel_pad, REKORD_UITTREKSEL_AGTERVOEGSEL)


def _verdeel_waarde(waarde, rekord_naam):
    """(what orders, what records) for one value of an extract.

    A list keeps its LENGTH and holds null where an item has no record, so kern[7]
    in one file is kern[7] in the other. Pruning the list would renumber the items,
    and a pointer that renumbers is worse than no pointer at all. A dict drops a key
    whose whole subtree records nothing, because a missing key cannot be misread as
    an order, and the file stays short enough to be worth opening.
    """
    if isinstance(waarde, str):
        i = eerste_rekordmerker(waarde)
        if i < 0:
            return waarde, _GEEN_REKORD
        # A FIELD THAT OPENS WITH A LEGACY MARKER IS NOT SPLIT AT ALL. This is the
        # other half of the trap described above. eerste_rekordmerker cuts such a field
        # at 0, so "the record half" is the entire field -- but 'REGGEMAAK 22 September
        # 2026: <the new requirement>' is the house shape for recording a correction
        # whose content IS the new order, and the order then stands inside or below the
        # record that replaced it. Measured over the 387 extracts on 12 October 2026:
        # 291 fields are cut at 0 by a legacy word, 329 KB of text, and they include 35
        # kern items and 34 live MOENIE prohibitions. Splitting them would have emptied
        # those fields in the one file a writer obeys, which is a lost requirement
        # rather than a long read. bin/verouderde-bestellings.py records the same blind
        # spot from a sweep's side: a field whose order opens with its own correction
        # marker is beyond both halves.
        #
        # The canonical line is the exception, because it is the only form that
        # promises that nothing below it orders anything -- a person wrote it after
        # reading the field end to end. Exactly one field in the repository is cut at 0
        # that way, 485 characters, and it does move. This is the same asymmetry the two
        # sweeps already keep between the canonical line and the legacy words: see
        # is_rekord_herskryf, and do not widen it to the whole vocabulary.
        #
        # AND THE SAME HOLDS FOR A LEGACY MARKER IN THE MIDDLE OF A FIELD. Found 16
        # October 2026: the rule above stopped at 0, so 806 fields with no canonical
        # line were still cut at the first legacy word mid-field, and in 220 of them,
        # across 65 specs, the hidden half held order-like wording. One Grade 4 water
        # lesson lost 'WAT WEL GELD: 'n kind gaan NOOIT self in die water nie ... reik
        # of gooi van droe grond af', the corrected rule itself, because it stood
        # after 'REGGEMAAK 2026-09-03'. A legacy word marks where a correction was
        # recorded, not where the orders end, so only the canonical line cuts.
        if not waarde.startswith(REKORD_HERSKRYFLYN, i):
            return waarde, _GEEN_REKORD
        return waarde[:i] + REKORD_VERSKUIF % rekord_naam, waarde[i:]
    if isinstance(waarde, dict):
        orde, rekord = {}, {}
        for k, v in waarde.items():
            o, r = _verdeel_waarde(v, rekord_naam)
            orde[k] = o
            if r is not _GEEN_REKORD:
                rekord[k] = r
        return orde, (rekord or _GEEN_REKORD)
    if isinstance(waarde, list):
        orde, rekord, iets = [], [], False
        for v in waarde:
            o, r = _verdeel_waarde(v, rekord_naam)
            orde.append(o)
            rekord.append(None if r is _GEEN_REKORD else r)
            iets = iets or r is not _GEEN_REKORD
        return orde, (rekord if iets else _GEEN_REKORD)
    return waarde, _GEEN_REKORD


def _tel_rekordvelde(waarde):
    """How many fields actually moved. Counted before the records file's own `_` keys
    are added, so the note cannot count itself -- a wrong count has misled this
    pipeline twice, and the count is the whole point of printing it."""
    if isinstance(waarde, str):
        return 1
    if isinstance(waarde, dict):
        return sum(_tel_rekordvelde(v) for v in waarde.values())
    if isinstance(waarde, list):
        return sum(_tel_rekordvelde(v) for v in waarde)
    return 0


def uittreksel_helftes(pad, doc):
    """One extract as (orders doc, records doc, records path).

    THE ONE PLACE THE CUT IS MADE. hardloop.py writes an extract twice per run and
    bin/vernuwe-uittreksels.py writes one for every lesson; a cut made at each call
    site would be three copies of one rule, which is precisely how the record
    vocabulary itself came to mean different things in two sweeps -- see
    REKORDMERKERS. The orders doc keeps every key the extract had, including the ones
    that order nothing, so a writer can never find a field missing.
    """
    rekord_pad = rekord_uittreksel(pad)
    orde, rekord = _verdeel_waarde(doc, os.path.basename(rekord_pad))
    if rekord is _GEEN_REKORD:
        rekord = {}
    naam = os.path.basename(pad)
    kop = {"_hoe_om_dit_te_lees": REKORD_UITTREKSEL_NOTA % (naam, naam),
           "_bestellings_uittreksel": naam,
           "_velde_met_rekords": _tel_rekordvelde(rekord)}
    # The fields win over the note if a spec ever names a field the same way. The
    # records file is WRITTEN EVEN WHEN IT IS EMPTY, with the count at zero: a file
    # saying "no records" is honest, and it leaves "missing" to mean the one thing it
    # should mean -- that nothing has regenerated this extract since the split.
    kop.update(rekord)
    return orde, kop, rekord_pad


# The fingerprint of the derived content a write last put on disk, carried inside
# the orders file. A leading underscore like the records file's own keys, so a spec
# field can never collide with it. It is what lets bin/vernuwe-uittreksels.py tell a
# writer's edit to an extract from an ordinary spec change -- and because it lives
# INSIDE the file it certifies, git merges content and fingerprint as independent
# lines, which is the other thing that sweep has to allow for.
UITTREKSEL_STEMPEL = "_afgelei_stempel"


def sonder_uittreksel_stempel(doc):
    """An extract's derived content: everything except the fingerprint itself."""
    return ({k: v for k, v in doc.items() if k != UITTREKSEL_STEMPEL}
            if isinstance(doc, dict) else doc)


def uittreksel_stempel(doc):
    """Fingerprint of an extract's derived content, ignoring the stamp itself."""
    blob = json.dumps(sonder_uittreksel_stempel(doc),
                      ensure_ascii=False, sort_keys=True)
    return "sha256:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()[:32]


def skryf_uittreksel(pad, doc):
    """Write a per-lesson extract as its two files; return (orders, records).

    EVERY write stamps, and the rule lives here rather than at a call site, for the
    same reason the cut does -- see uittreksel_helftes. The stamp was an optional
    callable until 12 October 2026 and only bin/vernuwe-uittreksels.py passed one, so
    the runner, which writes an extract twice per run at every pipeline step, left
    extracts unstamped most of the time. An unstamped extract is one the refresher
    cannot judge: it returns "not hand-edited" when there is no stamp, so a writer's
    edit is regenerated over silently, with no copy saved and no warning. That is why
    the absence of a saved copy was never evidence that nothing was lost.
    """
    orde, rekord, rekord_pad = uittreksel_helftes(pad, doc)
    orde = dict(orde, **{UITTREKSEL_STEMPEL: uittreksel_stempel(orde)})
    skryf_json(pad, orde)
    skryf_json(rekord_pad, rekord)
    return pad, rekord_pad


# ------------------------------------------------------------------ approved

# ------------------------------------------------------------------ profiles
def vind_profiel(vak, graad, subonderwerp=None):
    """Find the profiler config for a subject-grade.

    Matched on the config's own contents rather than on its filename, so no
    naming convention has to be remembered or enforced. Returns
    (path, config) or (None, reason).
    """
    if not os.path.isdir(PROFIELE):
        return None, f"there is no {os.path.relpath(PROFIELE, REPO)}/ directory"

    paths = sorted(glob.glob(os.path.join(PROFIELE, "*.json")))
    if not paths:
        return None, ("no profiler config in profiele/ — run the profiler once for "
                      "this subject-grade before any lesson is written")

    vak_key, wrong = slug(vak), []
    kandidate = []
    for p in paths:
        try:
            cfg = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError) as e:
            wrong.append(f"{os.path.basename(p)} is not readable JSON ({e})")
            continue
        if slug(cfg.get("vak", "")) == vak_key and int(cfg.get("graad", -1)) == int(graad):
            kandidate.append((p, cfg))

    if not kandidate:
        have = []
        for p in paths:
            try:
                c = json.load(open(p, encoding="utf-8"))
                have.append(f"{os.path.basename(p)}: {c.get('vak')} Gr {c.get('graad')}")
            except (OSError, ValueError):
                pass
        return None, ("no profiler config for {} Gr {}. profiele/ holds: {}".format(
            vak, graad, "; ".join(have) or "nothing usable"))

    if subonderwerp:
        sub_key = slug(subonderwerp)
        for p, cfg in kandidate:
            for label in (cfg.get("subonderwerpe") or {}):
                if slug(label) == sub_key:
                    return p, cfg
        names = sorted({label for _, c in kandidate
                        for label in (c.get("subonderwerpe") or {})})
        return None, ("profiler config {} covers {} Gr {} but has no sub-topic "
                      "matching '{}'. It measured: {}".format(
                          os.path.basename(kandidate[0][0]), vak, graad, subonderwerp,
                          "; ".join(names) or "nothing"))

    return kandidate[0]


def onderwerp_woorde(cfg, subonderwerp):
    """The measured textbook volume for one sub-topic, or None."""
    sub_key = slug(subonderwerp)
    for label, v in (cfg.get("subonderwerpe") or {}).items():
        if slug(label) == sub_key:
            return v
    return None


# ------------------------------------------------------------- agreed wordings
def gedeelde_omskrywings_pad(vak, graad):
    """The agreed-wordings file for one subject-grade, or None.

    One file per subject-grade under kaps/, matched on the file's own `vak` and
    `graad` rather than on its name -- the same way a profiler config is matched,
    and for the same reason. Natuurwetenskappe wrote
    kaps/gedeelde-omskrywings.json before there was a second subject, so the name
    proves nothing about whose wordings are inside. A lookup that silently hands
    back another subject's list is worse than one that hands back nothing: the
    writer would read wordings for terms this subject never agreed, and a
    coverage checker would hold the draft to them.
    """
    for p_ in sorted(glob.glob(os.path.join(KAPS, "gedeelde-omskrywings*.json"))):
        try:
            d = lees_json(p_)
        except (OSError, ValueError):
            continue
        if (slug(d.get("vak", "")) == slug(vak)
                and int(d.get("graad", -1)) == int(graad)):
            return p_
    return None


def gedeelde_omskrywings(vak, graad):
    """The whole agreed-wordings file for a subject-grade, {} when there is none."""
    p_ = gedeelde_omskrywings_pad(vak, graad)
    if not p_:
        return {}
    try:
        return lees_json(p_)
    except (OSError, ValueError):
        return {}


# ------------------------------------------------------------------ io helpers
def lees_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def skryf_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def voeg_jsonl(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def rel(path):
    """Repo-relative where possible, absolute otherwise — for readable output."""
    try:
        r = os.path.relpath(path, REPO)
    except ValueError:
        return path
    return path if r.startswith("..") else r.replace(os.sep, "/")

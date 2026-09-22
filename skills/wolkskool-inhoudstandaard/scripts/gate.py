#!/usr/bin/env python3
"""
Wolkskool content gate — deterministic register and volume check.

Runs AFTER the writer, BEFORE the review agents. Returns hard pass/fail
against measured grade-band thresholds, with numeric feedback the writer
can act on.

USAGE
    python3 gate.py lesson.json --grade 4 --budget 400
    python3 gate.py lesson.json --grade 11 --budget 700 --json
    python3 gate.py lesson.json --grade 4 --budget 400 --woordeboek C:/hunspell/af_ZA

INPUT FORMAT (lesson.json)
    {
      "titel": "Die stoomskip",
      "graad": 4,
      "vak": "Sosiale Wetenskappe",
      "blokke": [
        {"tipe": "studie",   "kop": "Wat is 'n stoomskip?", "teks": "..."},
        {"tipe": "eli10",    "vir": "Wat is 'n stoomskip?", "teks": "..."},
        {"tipe": "vraag",    "teks": "..."},
        {"tipe": "begrip",   "term": "stoomketel", "teks": "..."},
        {"tipe": "lys",      "kop": "Wat het verander?", "items": ["...", "..."]}
      ]
    }

Only blocks of tipe "studie" count toward the study-volume budget and the
curriculum register band. "eli10" blocks are checked against the flat
ELI10 band at every grade. "vraag" and "begrip" blocks are scaffolding:
counted and reported, never counted against study volume.
"""
import argparse, json, os, re, sys, statistics as st
from datetime import datetime, timezone

try:
    import pyphen
    _DIC = pyphen.Pyphen(lang='af')
except Exception:
    _DIC = None

# Afrikaans spellcheck. Optional — absence downgrades to a note, never a fail.
#
# The dictionary sits in a different place on every machine, so the location is
# configurable rather than hard-coded. Resolution order:
#
#   1. --woordeboek PATH
#   2. the WOLKSKOOL_HUNSPELL environment variable
#   3. the platform defaults below
#
# PATH is the base name shared by the .aff and .dic files (no extension), which
# is what spylls' Dictionary.from_files expects. A path ending in .aff or .dic is
# accepted and trimmed, since that is the easy mistake to make.
DICT_CANDIDATES = [
# Forward slashes throughout: Python accepts them on Windows and they keep the
# literal free of escape hazards. C:/hunspell/af_ZA is the same location as
# C:\hunspell\af_ZA.
    "C:/hunspell/af_ZA",
    "/usr/share/hunspell/af_ZA",
]

_SPELL = None
_SPELL_LOADED = False
_SPELL_PATH = None          # explicit override from --woordeboek


def set_dictionary(path):
    """Point the spellchecker at one specific dictionary base path."""
    global _SPELL_PATH, _SPELL_LOADED, _SPELL
    _SPELL_PATH, _SPELL_LOADED, _SPELL = path, False, None


def _dict_candidates():
    if _SPELL_PATH:
        return [_SPELL_PATH]
    env = os.environ.get("WOLKSKOOL_HUNSPELL")
    if env:
        return [env]
    return list(DICT_CANDIDATES)


def dictionary():
    """Load the Afrikaans dictionary once, or return None if there is none.

    Absence is a note, never a failure. Afrikaans compounds freely so spelling is
    a warning-level check throughout, and the gate must run normally without it.
    """
    global _SPELL, _SPELL_LOADED
    if _SPELL_LOADED:
        return _SPELL
    _SPELL_LOADED = True
    try:
        from spylls.hunspell import Dictionary
    except Exception:
        return None
    for path in _dict_candidates():
        base = re.sub(r"\.(aff|dic)$", "", str(path), flags=re.I)
        try:
            _SPELL = Dictionary.from_files(base)
            return _SPELL
        except Exception:
            continue
    return None


def spellcheck(text, extra=()):
    """Return unrecognised words. Warnings only: the dictionary lacks many
    legitimate compounds (Afrikaans compounds freely), so a hit is a prompt
    to look, not a verdict. Domain terms belong in the project wordlist."""
    spell = dictionary()
    if spell is None:
        return None
    allow = {w.lower() for w in extra}
    bad = []
    for w in re.findall(r"[A-Za-zÀ-ÿ']+", text):
        if len(w) < 3 or w[:1].isupper():
            continue
        if w.lower() in allow:
            continue
        if not (spell.lookup(w) or spell.lookup(w.lower())):
            bad.append(w)
    seen, out = set(), []
    for w in bad:
        if w.lower() not in seen:
            seen.add(w.lower())
            out.append(w)
    return out

# ---------------------------------------------------------------- thresholds
# Curriculum-register bands. Grade 4 row is MEASURED from a Grade 4
# Sosiale Wetenskappe textbook (25 pages, ~5000 words). Senior rows are
# provisional estimates — replace with profiler output from DBE past
# papers before relying on them in production.
BANDS = {
    (4, 6):   {"sent_min": 11.0, "sent_max": 14.5, "syl_max": 1.52, "poly_max": 13.0, "measured": True},
    (7, 9):   {"sent_min": 13.0, "sent_max": 17.5, "syl_max": 1.62, "poly_max": 17.0, "measured": False},
    (10, 12): {"sent_min": 15.0, "sent_max": 21.5, "syl_max": 1.72, "poly_max": 22.0, "measured": False},
}

# ELI10 band — deliberately FLAT across all grades. This is the constant.
ELI10 = {"sent_min": 9.0, "sent_max": 13.5, "syl_max": 1.50, "poly_max": 11.0}

# Chunking guides. The HTML layout ADAPTS to content, so these are
# comprehension guides, not layout requirements — warnings, never failures.
# A block much under the floor is a fragment; much over is an unbroken wall
# of text for the reader. The writer chunks on conceptual seams.
BLOCK_WORDS_MIN, BLOCK_WORDS_MAX = 30, 110
BLOCKS_MIN, BLOCKS_MAX = 3, 10
BUDGET_TOLERANCE = 0.15

# Per-lesson word band per grade, mirroring spec_check.py's LESBAND. spec_check
# holds the BUDGET to this band; nothing held the MEASURED draft to it, and the
# two can part company: a budget at the top of the band plus the +15% tolerance
# allows a draft well over the ceiling. A 530-word budget passed a 605-word
# Grade 5 draft on 10 September 2026, 55 words above Drico's ceiling, silently.
# It warns rather than fails: the band is Drico's planning range from his own
# count of real lessons, and delivered lessons predate it.
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
LESBAND = {4: (350, 450), 5: (300, 550), 6: (450, 550)}
LESBAND_VAK = {}
COMMA_MAX = 0.35
# List items are checked on their own terms rather than as prose.
LIST_ITEM_GUIDE, LIST_ITEM_MAX = 18, 28

# Marginal-breach tolerance. A threshold crossed by less than this fraction is
# statistical noise, not a defect — it warns instead of failing. Without this,
# an agent loop burns revision cycles on differences of 0.02 syllables.
TOLERANCE = 0.06
LONGWORD_PCT_MAX = 3.0
LONGWORD_CHARS = 10


def _vak_slug(vak):
    import unicodedata
    s = unicodedata.normalize("NFKD", vak or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def band_for(grade):
    for (lo, hi), b in BANDS.items():
        if lo <= grade <= hi:
            return b
    raise SystemExit(f"No register band defined for grade {grade}")


def syllables(word):
    if _DIC is None:
        return max(1, len(re.findall(r'[aeiouyäëïöüáéíóú]+', word.lower())))
    return max(1, len(_DIC.inserted(word).split('-')))


def measure(text):
    words = re.findall(r"[A-Za-zÀ-ÿ']+", text)
    sents = [s for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.split()]
    if not words or not sents:
        return None
    slens = [len(s.split()) for s in sents]
    syls = [syllables(w) for w in words]
    return {
        "words": len(words),
        "sentences": len(sents),
        "mean_sentence_len": round(st.mean(slens), 1),
        "median_sentence_len": round(st.median(slens), 1),
        "longest_sentence": max(slens),
        "mean_syllables": round(st.mean(syls), 2),
        "pct_polysyllabic": round(100 * sum(1 for s in syls if s >= 3) / len(syls), 1),
        "pct_long_words": round(100 * sum(1 for w in words if len(w) > LONGWORD_CHARS) / len(words), 1),
        "commas_per_sentence": round(sum(s.count(',') for s in sents) / len(sents), 2),
        "long_words": sorted({w for w in words if len(w) > LONGWORD_CHARS}),
    }


def _breach(value, limit, over=True):
    """Return None if within limit, 'marginal' if inside tolerance, else 'hard'."""
    if over:
        if value <= limit:
            return None
        return "marginal" if value <= limit * (1 + TOLERANCE) else "hard"
    if value >= limit:
        return None
    return "marginal" if value >= limit * (1 - TOLERANCE) else "hard"


def check_register(m, band, label, fails, warns):
    def report(kind, msg):
        if kind == "hard":
            fails.append(msg)
        elif kind == "marginal":
            warns.append(msg + "  [marginal — within tolerance, not blocking]")

    report(_breach(m["mean_sentence_len"], band["sent_min"], over=False),
           f"{label}: mean sentence length {m['mean_sentence_len']} below band minimum {band['sent_min']} — sentences are choppier than the grade expects")
    report(_breach(m["mean_sentence_len"], band["sent_max"]),
           f"{label}: mean sentence length {m['mean_sentence_len']} above band maximum {band['sent_max']} — shorten to one idea per sentence")
    report(_breach(m["mean_syllables"], band["syl_max"]),
           f"{label}: syllables per word {m['mean_syllables']} above maximum {band['syl_max']} — replace long words with plainer equivalents")
    report(_breach(m["pct_polysyllabic"], band["poly_max"]),
           f"{label}: 3+ syllable words {m['pct_polysyllabic']}% above maximum {band['poly_max']}%")
    report(_breach(m["commas_per_sentence"], COMMA_MAX),
           f"{label}: {m['commas_per_sentence']} commas per sentence above maximum {COMMA_MAX} — too much subordination, split into separate sentences")
    if m["pct_long_words"] > LONGWORD_PCT_MAX:
        warns.append(f"{label}: {m['pct_long_words']}% of words exceed {LONGWORD_CHARS} characters (guide {LONGWORD_PCT_MAX}%)")
    if m["longest_sentence"] > 2.2 * band["sent_max"]:
        warns.append(f"{label}: longest sentence is {m['longest_sentence']} words — check for a missing full stop")


def run(lesson, grade, budget):
    band = band_for(grade)
    blocks = lesson.get("blokke", [])
    fails, warns, notes = [], [], []

    if not band["measured"]:
        notes.append(f"Grade {grade} register band is an ESTIMATE, not measured. Profile DBE past papers to replace it.")

    by_type = {}
    for b in blocks:
        by_type.setdefault(b.get("tipe", "onbekend"), []).append(b)

    study = by_type.get("studie", [])
    lists = by_type.get("lys", [])
    eli10 = by_type.get("eli10", [])
    # A 'leesstuk' is a continuous text the learner READS, not an explanation of a
    # concept — CAPS's "lees vir genot" in Life Skills, and the core text an Afrikaans
    # Huistaal cycle is built around. It carries the lesson's volume exactly as study
    # text does and is measured for register the same way, because a learner reads it
    # the same way. What it is exempt from is the chunking guidance below, which
    # assumes explanation broken into one idea per block: a story is one continuous
    # piece and cutting it into 30-110 word chunks would be measuring it as the wrong
    # kind of thing.
    reading = by_type.get("leesstuk", [])

    if not study and not reading:
        fails.append("No blocks of tipe 'studie' or 'leesstuk' found — nothing to measure against the volume budget")
        return {"verdict": "FAIL", "titel": lesson.get("titel"), "graad": grade,
                "vak": lesson.get("vak"), "budget": budget,
                "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "study": None, "eli10": None,
                "block_counts": {k: len(v) for k, v in by_type.items()},
                "misspelled": [], "failures": fails, "warnings": warns, "notes": notes}

    # --- volume (study text and reading text) ---
    # 'lys' blocks are bullet/numbered lists. Their items are not sentences, so
    # measuring them as prose distorts mean sentence length. They COUNT toward
    # the volume budget but are EXCLUDED from register statistics.
    study_text = " ".join(b.get("teks", "") for b in study + reading)
    sm = measure(study_text)
    list_words = sum(len(re.findall(r"[A-Za-zÀ-ÿ']+", " ".join(b.get("items", []))))
                     for b in lists)
    if list_words:
        sm["words"] += list_words
        sm["list_words"] = list_words
    # Name the thing being measured after what actually carries the lesson, so a
    # reading lesson's failure does not talk about study text it never had.
    label = "Reading text" if reading and not study else "Study text"
    lo, hi = budget * (1 - BUDGET_TOLERANCE), budget * (1 + BUDGET_TOLERANCE)
    if sm["words"] < lo:
        fails.append(f"{label} {sm['words']} words, below budget floor {lo:.0f} (target {budget}) — under-supplying relative to the textbook")
    elif sm["words"] > hi:
        fails.append(f"{label} {sm['words']} words, above budget ceiling {hi:.0f} (target {budget}) — learners will revise the textbook instead")
    # NB: not named 'band' — that name holds the REGISTER band and is read below.
    lesband = LESBAND_VAK.get((grade, _vak_slug(lesson.get("vak"))), LESBAND.get(grade))
    if lesband and sm["words"] > lesband[1]:
        warns.append(f"{label} {sm['words']} words, above the Grade {grade} lesson band ceiling {lesband[1]} "
                     f"— the budget ({budget}) plus tolerance allows it, but the band does not")

    # --- chunking ---
    # Only explanatory lessons are chunked. A lesson whose volume is carried by a
    # reading piece has no study blocks to count, and warning that it has zero would
    # fire on every reading lesson ever written — which is how a guide turns into
    # noise a writer learns to ignore.
    if study and not (BLOCKS_MIN <= len(study) <= BLOCKS_MAX):
        warns.append(f"{len(study)} study blocks, outside the {BLOCKS_MIN}–{BLOCKS_MAX} comprehension guide — check the content is chunked one idea at a time")
    for i, b in enumerate(study, 1):
        w = len(re.findall(r"[A-Za-zÀ-ÿ']+", b.get("teks", "")))
        if w < BLOCK_WORDS_MIN:
            warns.append(f"Study block {i} ('{b.get('kop','—')[:32]}') only {w} words (guide {BLOCK_WORDS_MIN}–{BLOCK_WORDS_MAX})")
        elif w > BLOCK_WORDS_MAX:
            warns.append(f"Study block {i} ('{b.get('kop','—')[:32]}') {w} words (guide {BLOCK_WORDS_MIN}–{BLOCK_WORDS_MAX}) — will overflow its section")

    # --- register ---
    # A reading piece is held to the same band as study text. A learner reads both
    # the same way, and the band's floor exists to stop writing collapsing into
    # fragments, which a story can do as easily as an explanation.
    check_register(sm, band, label, fails, warns)

    # List items are excluded from prose register statistics, which would
    # otherwise let a writer park difficult prose in a 'lys' block and escape
    # the band entirely. Check them separately, on their own terms: a list item
    # is meant to be a short scannable point, not a sentence carrying clauses.
    for b in lists:
        for j, item in enumerate(b.get("items", []), 1):
            iw = len(re.findall(r"[A-Za-zÀ-ÿ']+", item))
            head = (b.get("kop") or "—")[:28]
            if iw > LIST_ITEM_MAX:
                fails.append(f"List '{head}' item {j}: {iw} words, above maximum {LIST_ITEM_MAX} — a list item should be a short scannable point, not a sentence with clauses")
            elif iw > LIST_ITEM_GUIDE:
                warns.append(f"List '{head}' item {j}: {iw} words (guide {LIST_ITEM_GUIDE}) — consider tightening")
            if item.count(',') >= 2:
                warns.append(f"List '{head}' item {j} has {item.count(',')} commas — likely too much subordination for a list point")

    # An intuition block must not outgrow the study block it explains. Measured need:
    # with no cap, one such block reached 415 words against a 389-word lesson, because
    # it sits outside the study budget and nothing pushed back. A warning rather than a
    # failure, in keeping with the rule that only volume-against-budget and
    # register-against-band are hard fails.
    if len(eli10) > 1:
        warns.append(f"{len(eli10)} eli10 blocks — the guide is zero or one per lesson, "
                     f"for the single concept that cannot be stated concretely")
    study_by_kop = {(b.get("kop") or "").strip():
                    len(re.findall(r"[A-Za-zÀ-ÿ']+", b.get("teks", "")))
                    for b in study}
    for b in eli10:
        ew = len(re.findall(r"[A-Za-zÀ-ÿ']+", b.get("teks", "")))
        vir = (b.get("vir") or "").strip()
        sw = study_by_kop.get(vir)
        if sw and ew > sw:
            warns.append(f"eli10 for '{vir[:34]}' is {ew} words against a {sw}-word study "
                         f"block — an intuition layer should not outgrow what it explains")

    em = None
    if eli10:
        em = measure(" ".join(b.get("teks", "") for b in eli10))
        if em:
            check_register(em, ELI10, "ELI10 layer", fails, warns)
    else:
        # NOT a warning. Zero intuition blocks is an accepted and common outcome: the
        # guide is zero or one per lesson, and most lessons contain no genuinely
        # abstract mechanism. This line used to read "intuition-first explanation is
        # missing", which invited a writer to add a block purely to silence it — the
        # exact behaviour the zero-or-one rule exists to stop. It is stated as a fact
        # because a human reviewer wants to know, not because anything is wrong.
        notes.append("No ELI10 layer — zero or one per lesson is the guide, and none is "
                     "a normal outcome for a lesson with no abstract mechanism")

    # ELI10 blocks should name the concept they explain, so the layout can pair
    # them and the coverage checker can verify the flagged concepts are covered.
    study_heads = {b.get("kop", "").strip() for b in study}
    for b in eli10:
        vir = (b.get("vir") or "").strip()
        if not vir:
            warns.append("An ELI10 block has no 'vir' field — cannot tell which concept it explains")
        elif vir not in study_heads:
            warns.append(f"ELI10 block points at '{vir[:40]}', which is not a study block heading")

    # --- glossing ---
    glossed = {b.get("term", "").lower() for b in by_type.get("begrip", [])}
    unglossed = [w for w in sm["long_words"]
                 if w.lower() not in glossed and not w[:1].isupper()]
    if unglossed:
        warns.append(f"Long words in {label.lower()} with no 'begrip' entry: {', '.join(unglossed[:8])}")

    # No check on 'vraag'. Lessons stopped carrying retrieval questions on 2026-08-21
    # because the layout team was told to ignore them, so they never reached a learner.
    # This used to warn on their ABSENCE, which would now fire on every lesson written.
    # It does not warn on their PRESENCE either: four lessons predate the decision and
    # their questions are legitimate content, not a defect to nag about.

    # --- spelling (warning only) ---
    all_text = " ".join(b.get("teks", "") for b in blocks)
    misspelled = spellcheck(all_text, extra=lesson.get("woordelys", []))
    if misspelled is None:
        notes.append("Afrikaans dictionary not installed — spelling not checked")
        configured = _SPELL_PATH or os.environ.get("WOLKSKOOL_HUNSPELL")
        if configured:
            notes.append(f"Configured dictionary '{configured}' could not be loaded — "
                         f"expected an .aff and a .dic file sharing that base name.")
    elif misspelled:
        warns.append(f"Possible spelling errors ({len(misspelled)}): {', '.join(misspelled[:12])}")
        notes.append("Legitimate compounds may be flagged. Add subject terms to the lesson's 'woordelys' list to silence them.")

    return {
        "verdict": "FAIL" if fails else "PASS",
        "titel": lesson.get("titel"),
        "graad": grade,
        "vak": lesson.get("vak"),
        "budget": budget,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "study": {k: v for k, v in sm.items() if k != "long_words"},
        "eli10": {k: v for k, v in em.items() if k != "long_words"} if em else None,
        "block_counts": {k: len(v) for k, v in by_type.items()},
        "misspelled": misspelled if misspelled else [],
        "failures": fails,
        "warnings": warns,
        "notes": notes,
    }


def main():
    ap = argparse.ArgumentParser(description="Wolkskool register and volume gate")
    ap.add_argument("lesson")
    ap.add_argument("--grade", type=int, required=True)
    ap.add_argument("--budget", type=int, required=True, help="target study-text word count")
    ap.add_argument("--json", action="store_true", help="emit JSON only (for orchestrator use)")
    ap.add_argument("--log", help="append result to this JSONL log")
    ap.add_argument("--woordeboek", default=None,
                    help="Afrikaans hunspell dictionary base path, without the .aff/.dic "
                         "extension. Overrides $WOLKSKOOL_HUNSPELL. Spelling is a "
                         "warning-level check, so the gate runs normally without one.")
    a = ap.parse_args()

    if a.woordeboek:
        set_dictionary(a.woordeboek)

    lesson = json.load(open(a.lesson, encoding="utf-8"))
    r = run(lesson, a.grade, a.budget)

    if a.log:
        with open(a.log, "a", encoding="utf-8") as f:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"\n{r['verdict']}  —  {r.get('titel') or '(untitled)'}  (Gr {r['graad']}, budget {r['budget']})")
        s = r.get("study")
        if s:
            # The JSON key stays 'study' — the runner and verdict_check read it — but
            # the printed label follows what the lesson actually carries.
            counts = r.get("block_counts") or {}
            shown = "reading text" if counts.get("leesstuk") and not counts.get("studie") else "study text"
            print(f"\n  {shown:<12} {s['words']} words / {s['sentences']} sentences")
            print(f"               {s['mean_sentence_len']} words per sentence, {s['mean_syllables']} syllables per word, {s['pct_polysyllabic']}% polysyllabic")
        if r["eli10"]:
            e = r["eli10"]
            print(f"  eli10 layer  {e['words']} words, {e['mean_sentence_len']} words per sentence, {e['mean_syllables']} syllables per word")
        print(f"  blocks       {r['block_counts']}")
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

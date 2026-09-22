# Register bands and calibration

## Lesson budget band — separate from register

| Grade | Floor | Ceiling |
|---|---|---|
| 4 | 350 | 450 |
| 5 | 400 | 500 |
| 6 | 450 | 550 |

Decided by Drico on 7 September 2026, after measuring the delivered Grade 4 lessons:
they ran **169 to 811 study words**, seventeen of twenty-five over 450. Register and
budget are different things — this table is about how much a lesson holds, the ones
below are about how it reads. Full reasoning in `SKILL.md` under Volume budget.

Measured at the same time, and worth keeping: **a built page runs about 1.6x the study
budget.** Across the 25 built Gr 4 lessons the page is 62.6% study text, 8.0% glossary,
5.6% block headings, 0.7% title — 77.3% ours — and 22.7% builder furniture. So a
450-word budget renders as roughly a 700-word page. Anyone judging length by looking at
a built lesson is reading a number 60% larger than the one the gate enforces.

## Current bands

| Grades | Words/sentence | Syllables/word | 3+ syllables | Status |
|---|---|---|---|---|
| 4–6 | 11.0–14.5 | ≤1.52 | ≤13% | **MEASURED** |
| 7–9 | 13.0–17.5 | ≤1.62 | ≤17% | ESTIMATE |
| 10–12 | 15.0–21.5 | ≤1.72 | ≤22% | ESTIMATE |
| ELI10, all grades | 9.0–13.5 | ≤1.50 | ≤11% | Derived |

Applies to `studie` and `lys` blocks (register measured on `studie` only).
Additional limits at every grade: commas ≤0.35 per sentence, words over 10
characters ≤3% of the study text.

Marginal breaches — within 6% of a threshold — demote to warnings. This exists
because a hard fail at 1.54 against a 1.52 ceiling sends the writer into a
revision cycle over noise.

## Where the Grade 4–6 row comes from

Measured from a Grade 4 Sosiale Wetenskappe textbook: 25 content pages sampled
across the whole book, OCR'd in Afrikaans, roughly 5 000 words. Figures held
steady between a 10-page and a 30-page sample, which indicates they describe the
book rather than the sample.

| Measure | Measured value |
|---|---|
| Mean sentence length | 12.7 words |
| Median sentence length | 10 words |
| Sentences under 12 words | 58% |
| Sentences over 20 words | 12% |
| Mean syllables/word | 1.47 |
| One-syllable words | 66% |
| 3+ syllable words | 10% |
| Words over 10 characters | 2.4% |
| Commas per sentence | 0.22 |
| Subordinators per 100 words | 0.4 |
| Questions | 13% of sentences |
| Type-token ratio | 0.22 |
| Words per content page | 199 median, 188 mean, IQR 136–247 |

The band was set wider than the measurement to allow legitimate variation. No
textbook prose was retained; only these numbers.

## What the measurements actually taught us

**Syntax is flatter than sentence length suggests.** 0.22 commas per sentence and
0.4 subordinators per 100 words means almost all main clauses, very little
*omdat* / *sodat* / *terwyl* chaining. Grade 4 register is not primarily about
short sentences — it is about **one idea per sentence**. That is the parameter
most easily missed when an adult writes "simply".

**Reading level sits around grade 6–7 on Flesch-Kincaid, not grade 4.** Normal for
a textbook: content vocabulary pushes the index up regardless of syntax. Do not
try to write *below* the book, or the content ends up thinner than the curriculum
requires.

**Afrikaans compounds inflate syllable counts independently of clarity.**
*Veiligheidsmaatreëls*, *reddingsbootreëls*, *passasierskip* are unavoidable on
some topics. This is why the syllable thresholds carry a tolerance and why
compound-heavy topics may sit marginally over without any real problem.

## Voice calibration — the human reference sample

A hand-written Grade 4 lesson by the Wolkskool author, profiled the same way:

| Measure | Author | Textbook | Verdict |
|---|---|---|---|
| Mean sentence length | 13.7 | 12.7 | In band — well calibrated |
| Syllables/word | 1.54 | 1.47 | Marginal, compound-driven |
| 3+ syllable words | 13.2% | 10% | Marginal |
| Study words for the lesson | 258 | ~300 expected | **Short by ~15%** |

**The author's sentence rhythm is the target.** It landed in band by instinct,
while a deliberate attempt to write "simply" came out at 7.5 words per sentence —
far below the floor. Imitate the author's voice, not a publisher's house style.

**The known correction is depth, not register.** The author's instinct stops at
roughly two-thirds to five-sixths of the budget, and thin blocks are where it
shows: a definition given 11 words with no elaboration, a historical figure given
19 words — a date and a fact with no story. Correct, complete, and leaving a
nine-year-old nothing to picture.

## Words per page varies by section — measure, do not derive

The book-wide median is 199 words per page. The "Vervoer op water" sub-topic
(pages 135–140) runs at **171** — it is illustration-heavy, and one of its six
pages is almost entirely a picture.

Deriving a sub-topic's volume from the book-wide median therefore overstated it by
16%, which would have inflated every water lesson. **Always measure the sub-topic's
own page range** with `skills/wolkskool-inhoudstandaard/scripts/profiler.py`, and
use the book-wide median only for setting register bands, where it is averaging
over the whole book on purpose.

Measured for CAPS Gr 4 SW Kwartaal 3, "Vervoer oor tyd heen":

| Sub-topic | Pages | Words |
|---|---|---|
| Vervoer op land | 122–133 (12) | 2 335 |
| Gevallestudie: uitlaatgasse | 134 (1) | 178 |
| Vervoer op water | 135–140 (6) | 994 |
| Vervoer in die lug | 141– | needs an end marker |

Two notes on accuracy. OCR at 150 dpi undercounts by roughly 3% against 300 dpi
(994 vs 1 028 for the water section), so run the final volume pass at 300 dpi or
accept a slightly conservative budget. And the page counts track the CAPS hour
allocations closely — about two pages per hour — which is a useful cross-check that
the section boundaries were found correctly, even though hours are not used to
derive budgets.

## Replacing the senior-grade estimates

The 7–9 and 10–12 rows are estimates and must be replaced before production use
at those grades.

**Profile DBE past exam papers, not textbooks.** Papers are public, free, and
define exactly the register a learner must be able to read by the end of a grade.
Benchmarking against the assessment instrument is more defensible than
benchmarking against a competitor's textbook, and there is no rights question at
all.

Method: two to four papers per subject-grade, OCR if needed, run the same
statistics, set the band wider than the measurement. Record the source papers in
the profiler config so the provenance is traceable.

## Per-subject onboarding routine

Run once per subject-grade, before any lesson is written:

1. Profile a textbook for register and words per page — **profiler only, numbers out**
2. Profile two to four DBE past papers for exam register
3. Extract the CAPS topic structure, bullets, and hour allocations
4. Compute per-bullet word budgets
5. Write the profiler config; record what was profiled

Steps 1 and 2 are scripted and take minutes. Everything downstream reads the
config, and no agent in the generation chain ever touches the book.

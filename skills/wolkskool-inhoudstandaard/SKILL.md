---
name: wolkskool-inhoudstandaard
description: The shared content standard for Wolkskool CAPS-aligned Afrikaans lesson content — the lesson JSON schema, register bands per grade, study-volume budgets, the Core/Aanvulling/Scaffolding content rule, the copyright discipline, and the gate script that checks compliance. Use this skill whenever writing, planning, reviewing, checking, or gating Wolkskool lesson content for any grade or subject, whenever working with lesson JSON files or CAPS topic tables, and whenever a task mentions Wolkskool, SOS lesson content, ELI10 layers, register bands, or study-volume budgets. Also use it before profiling a textbook or past paper, since the profiling rules and the rights boundary live here.
---

# Wolkskool content standard

Every agent in the Wolkskool content pipeline loads this skill. It defines what a
lesson *is*, so that the planner, writer, and checkers all mean the same thing by
it. If a rule here conflicts with an agent's own prompt, this file wins — an
agent prompt may narrow the standard but never loosen it.

## The pipeline in one view

```
Profiler (script)   textbook + past papers  ->  numbers only (config)
Planner  (agent)    CAPS topic + config     ->  lesson specs  [human approves]
Writer   (agent)    one lesson spec         ->  lesson JSON
Gate     (script)   lesson JSON             ->  PASS / FAIL + numbers
Coverage (agent)    spec + lesson           ->  present/missing checklist
Facts    (agent)    lesson + web            ->  verified/contradicted/unverifiable
                                            ->  human sign-off  ->  HTML team
```

Two revision cycles maximum, then escalate to the human. Log every gate and
checker result — the logs are how the prompts get improved.

## The copyright rule — read this before anything else

Wolkskool content must be independently created. Independent creation is a
property of the *process*, not of the output: it cannot be proven by inspecting a
page, only by showing the generation chain never had access to the source.

**Only the profiler may read a textbook. The profiler emits numbers. The planner
and writer see CAPS plus those numbers, never the book.**

This holds no matter how the request is framed. Common ways the boundary gets
crossed by accident, all of which must be refused:

- "Here is the textbook page, just use it as a reference for depth"
- "Here is the input that produced our last page" (if that input came from a book)
- "Extract the text so we can rewrite it in our own words" — rewriting a specific
  source is a derivative work; the copying step is what infringes
- "We have permission" — permission to *use* a book rarely includes the right to
  make derivative works, and those are separately granted

Facts are not copyrightable. Selection, arrangement, sequence, and expression
are. So overlap in *facts* with a textbook is unavoidable and harmless; matching
its *lesson structure* is the exposure, because structural similarity is easy to
demonstrate side by side.

Record provenance in every lesson's `herkoms` field (see schema below). Five
lines now answers any question years later.

## What a Wolkskool lesson is

A lesson maps to **one CAPS content bullet**, not to a textbook page or section.
CAPS bullets are the unit the curriculum actually specifies, and using them keeps
lesson boundaries independent of any publisher's chapter design.

Content divides into three tiers. The tier determines whether it counts against
the study budget:

| Tier | What it is | Budget |
|---|---|---|
| **Core** | Named in the CAPS document | Counts. Mandatory. |
| **Aanvulling** | Not in CAPS, but needed for the concept to make sense or to serve the CAPS focus question | Counts. Max ~25% of study budget. Needs a written justification in the lesson spec. |
| **Scaffolding** | ELI10 layer, retrieval questions, glossary entries | Does not count. Uncapped. |

This is what resolves the apparent contradiction of "give more, but not more to
study". Study text stays at textbook parity; scaffolding is free. A learner
revises `studie` blocks. Everything else reduces the effort of revising them.

**The Aanvulling test:** would the concept be incomplete or meaningless without
it? Steam power on water is meaningless without the moment someone proved a
steamboat worked commercially — so Robert Fulton passes. A dramatic shipwreck
story is colour, not mechanism — so the Titanic fails, even though a textbook
gives it a full page. Without this test the writer will justify any addition as
educational.

Note that CAPS itself names people where a person anchors a breakthrough
("Wright broers en die uitvinding van die eerste vliegtuig"). Applying that
pattern consistently to other breakthroughs is following CAPS's approach, not
departing from it — that is the strongest form of Aanvulling justification.

## Lesson specs

The planner produces a spec per CAPS sub-topic; the writer consumes one lesson
entry from it; the coverage checker checks a draft against the same entry. Schema
in `references/lesspesifikasie.md`, worked example in
`assets/voorbeeldspesifikasie.json`.

Validate specs before writing:

```bash
python3 scripts/spec_check.py spec.json
```

## The lesson JSON schema

See `references/skema.md` for the field-by-field specification and
`assets/verwysingsles.json` for a complete lesson that passes the gate. Read the
reference lesson before writing — one worked example teaches the format faster
than any description.

Minimum shape:

```json
{
  "skema_weergawe": "1.0",
  "status": "konsep",
  "titel": "Die stoomskip",
  "graad": 4,
  "vak": "Sosiale Wetenskappe",
  "kaps_onderwerp": "Vervoer op water",
  "kaps_punt": "Die eerste stoomskepe",
  "woordelys": ["stoomskepe", "skeprad"],
  "herkoms": {
    "kaps_dokument": "CAPS Gr 4 SW, Kwartaal 3, Onderwerp: Vervoer oor tyd heen",
    "profiel_konfig": "gr4-sw-2026-03.json",
    "skrywer_prompt": "skrywer-v1.2",
    "handboek_gesien": false
  },
  "blokke": [
    {"tipe": "studie", "kop": "Wat is 'n stoomskip?", "teks": "..."},
    {"tipe": "eli10",  "vir": "Wat is 'n stoomskip?", "teks": "..."},
    {"tipe": "lys",    "kop": "Wat het verander?", "items": ["...", "..."]},
    {"tipe": "begrip", "term": "stoomketel", "teks": "..."},
    {"tipe": "vraag",  "teks": "..."}
  ]
}
```

`handboek_gesien` must be `false` for any lesson produced by the writer. A `true`
value means the lesson is calibration material and must not be published.

`status` moves `konsep` -> `gated` -> `goedgekeur`. **The HTML team reads only
`goedgekeur` files.** That single rule lets the content pipeline iterate freely
without destabilising the layout pipeline.

## Register bands

Full table and calibration provenance in `references/registerbande.md`. Summary:

| Grades | Study text, words/sentence | Syllables/word | 3+ syllable words |
|---|---|---|---|
| 4–6 | 11.0–14.5 | ≤1.52 | ≤13% |
| 7–9 | 13.0–17.5 | ≤1.62 | ≤17% |
| 10–12 | 15.0–21.5 | ≤1.72 | ≤22% |
| **ELI10, all grades** | **9.0–13.5** | **≤1.50** | **≤11%** |

Only the 4–6 row is measured from real text. The senior rows are estimates and
must be replaced by profiling DBE past papers before production use. The gate
says so in its own output whenever it runs on those grades.

**The bands have a floor as well as a ceiling, and the floor matters more than
people expect.** Writing "simply" for young learners overshoots into fragments:
a first attempt at Grade 4 content came out at 7.5 words per sentence against a
floor of 11.0, well below what nine-year-olds already read comfortably. Short
sentences are not the goal. **One idea per sentence** is the goal — which is why
the comma limit (≤0.35 per sentence) does more work than the length limit.

The ELI10 band stays flat at every grade. That is deliberate: intuition gets
explained the same plain way at Grade 4 and at Grade 12, sitting beside study
text whose register climbs. At Grade 4 the two bands nearly overlap, so the ELI10
layer's value there is entirely the *analogy*, not the simpler wording.

## Volume budget

Anchored on measured volume, never guessed:

```
onderwerp_woorde = pages_for_subtopic x words_per_page    (from the profiler)
lesson_budget    = round(onderwerp_woorde / lesson_count)
```

**CAPS contact hours are deliberately not used.** They tell a teacher how long to
spend on a topic and say nothing about how much text a learner reads — lesson time
holds discussion, drawing and group work as well as reading. Treating hours as a
words-per-hour rate confuses teaching time with reading volume.

Budgets divide evenly across a sub-topic's lessons. Weighting them by judged
importance substitutes an opinion for a measurement.

Check the topic total, not just each lesson — some bullets are genuinely short.
What matters is that coverage of a whole CAPS topic is not systematically thinner
than a textbook's. Under-supply is as damaging as over-supply: if Wolkskool
covers a topic in two-thirds the depth, learners revise the textbook instead.

Gate tolerance is ±15% of the stated budget.

## Writing patterns that are known to work

These come from measuring real Grade 4 material, not from taste.

**Concept treatment — name, definition, one distinguishing detail.** Three
sentences per item. "A klipper is a ship that sails very fast. It has three or
more masts. Klippers move so fast we say they cut through the waves." Definitions
in the glossary run 8–12 words.

**Every new subject term gets a `begrip` entry.** How many that is depends on the
concept — two for a simple mechanism, six for a lesson where CAPS names five
vessel types. Do not pad to hit a number.

Note the distinction: the *rule* is "define new subject terms", and terms can be
short — *suier*, *skroef*, *ketel* are all new to a nine-year-old. The gate can
only measure word length, so it warns about words over 10 characters without
entries. That is a proxy, not the rule. A lesson can satisfy the gate and still
leave real terms undefined.

**ELI10 must contain an actual comparison, not a paraphrase.** Restating the
study text in shorter words is the most common failure and adds nothing. Compare
to something a child already handles: a kettle lid lifting, a hand pushing a
stick. Every ELI10 block names its concept in `vir`.

**Analogies are a factual risk.** They are vivid, memorable, and easy to get
subtly wrong, and then the misconception outlasts the lesson. "Steam pushes like
a hand" is safe. "Electrons orbit the nucleus like planets round the sun" is a
lie that takes years to undo. The fact checker verifies the *mapping*, not just
the stated facts.

**Retrieval questions ask for inference, not recall.** Three per lesson. The bar
is set by real Grade 4 material: "Look at this photograph. Do you think she was
rich or poor? How do you know?" — a nine-year-old reading evidence from a source.
"What burns in the fire?" is a weaker question, though one recall question per
lesson is fine as a confidence-builder.

**Every superlative gets verified or softened.** "Eerste", "oudste", "grootste"
are the highest-risk factual category in a history lesson, because the phrasing
everywhere online is looser than the truth. Fulton did not invent the steamboat;
he showed one could work commercially. Write the careful version.

**Content must be visualisable.** Every study block needs something depictable —
a physical process, a sequence, a comparison, a place, a person. Abstract
explanatory prose leaves the layout team nothing to work with. Do not specify
*how* to render anything; that is the HTML team's decision.

**The study text must stand alone.** A learner who cannot load a visual — slow
connection, low-end device, mobile data — must still be able to learn the concept
and answer the questions from the text.

## Checker reports

Both checkers emit one shared report format so the orchestrator branches on a single
contract. Schema in `references/nasienverslag.md`. Validate before acting on a
report:

```bash
python3 scripts/verdict_check.py report.json --les lesson.json --spek lesse_entry.json
```

It confirms the report is well formed and — the part that matters — that its verdict
follows from its own findings. A checker reporting three contradicted claims and then
returning `GOEDGEKEUR` would otherwise pass straight through, and these reports are
the only thing between an error and a learner.

Pass `--les` and `--spek` wherever possible. Without them only internal consistency
is checkable, and a checker that examined two claims out of thirty produces a
perfectly consistent report.

Three verdicts: `GOEDGEKEUR` proceeds, `HERSIEN` goes back to the writer,
`MENS_NODIG` goes to a person. The third exists because some defects a writer cannot
fix — an unverifiable claim, a spec that makes no sense — and a writer handed one will
either invent a fix or strip the content.

## Running the gate

```bash
python3 scripts/gate.py lesson.json --grade 4 --budget 300 --log gate_log.jsonl
python3 scripts/gate.py lesson.json --grade 11 --budget 700 --json
```

Exit 0 = pass, exit 1 = fail. Use the exit code as the loop branch. Setup and
dependencies are in `references/opstelling.md`.

**Hard failures** are only volume-against-budget and register-against-band —
things that are genuinely measurable and genuinely matter. Everything else warns.
Breaches within 6% of a threshold demote to warnings automatically, because
sending a writer back to revise over 0.02 syllables per word burns cycles on
statistical noise.

**Warnings are for human judgment, not auto-rejection.** Spelling in particular:
Afrikaans compounds freely, so no dictionary keeps up, and legitimate words get
flagged. Add subject terms to the lesson's `woordelys`.

Never ask an agent to check what the script checks. Language models cannot count
reliably and will report a 780-word draft as "approximately 400 words, suitable
for the grade" with complete confidence. The division of labour is the point:
scripts measure, agents judge.

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

## Where this text sits on the platform

**A Wolkskool lesson is a video plus this text, running in parallel.** The video
explains; the text is the same lesson in readable form. One video and one text per CAPS
content heading, and they cover the same ground rather than dividing it.

Two consequences that decide how the text is written:

**The text stands alone.** A learner revising the night before a test does not rewatch a
video, they read — so this text is the revision instrument, which is why the study budget
is anchored to textbook parity rather than to something thinner. And a learner on a slow
connection or a low-end device must be able to learn the whole concept from the text with
no video and no images at all. That is not a nice-to-have in South Africa.

**The video is made after the text, and uses the text as its guide.** The person making
the video covers everything the text covers, and adds whatever else serves interest — a
demonstration, an animation, a comparison. Two things follow, and both are the reason the
video comes second: the text must never contain something the video misses, and the two
must never disagree.

So **the text is the floor, not the ceiling.** It carries the curriculum completely and
correctly. The video carries the interest.

Three consequences for how this text is written:

**Everything in the text is a commitment the video must honour.** A block that does not
need to be there is not merely page weight — it is a constraint on the person making the
video. Write what the lesson requires and nothing more.

**Correctness matters more than it would otherwise.** An error here does not stay here. It
is spoken aloud in a video and reaches a learner twice.

**The vivid comparison is the video's job, and the video does it better.** Showing a bean
swell in wet soil or water push back on a hand is exactly what video is for. So the
`eli10` layer is zero or one per lesson and **the default is none** — reserve it for a
concept that genuinely cannot be stated concretely at all, and let the video supply the
rest of the intuition. A learner who cannot load the video still learns the concept from
plain concrete description, which is what standing alone requires; it does not require the
text to be as vivid as film.


### Gr 4 Sosiale Wetenskappe runs a different process

**Drico, 7 September 2026: "this whole SW inhoud we are creating is going to be a
different process, and we must treat it as an exception to what we have been doing the
whole time."** Everything below is that exception, gathered in one place rather than
scattered as caveats on rules it does not follow. It applies to Grade 4 Sosiale
Wetenskappe and to nothing else, until someone decides otherwise for another subject.

Six departures, and the first causes the rest:

| Normal process | Sosiale Wetenskappe |
|---|---|
| Text first, video follows it | **Video already exists** and will not be remade |
| One lesson per CAPS bullet | **The video's division wins** — where it merged two bullets, the text merges too |
| Coverage comes from the CAPS content table | **Also from CAPS's skills and concepts section**, because the teacher taught beyond the content list |
| Budget is measured textbook volume | **Mostly requirement-based** — the book does not cover most of this subject |
| Grade 4 budgets sit in the 350–450 band | **Kwartaal 1 sits at 200**, by decision |
| Every CAPS bullet is covered | **The local-area anchor is dropped**, by decision |

**Why the teacher's judgement is allowed to extend coverage, which is the one that
matters most.** CAPS lists content in one place and the historical aims, skills and
concepts in another, and says following the second is critical for every content
topic. Kwartaal 1's content list is essentially one item — four ways to find out about
the past — while the teacher's five videos also teach what history is, how to place
events in time, and why any of it matters. Read against the content list alone, three
of five lessons are supplement at 60% against a 25% cap, and the plan fails. Read
against the whole document, they are CAPS delivery.

Drico's reason for taking the second reading is the principle worth keeping:
**"That's the power of having a teacher in the mix... They know whats important beyond
the caps points."** A rule that would have deleted good teaching to satisfy a cap was a
rule written before anyone had read all of CAPS.

**This does not loosen anything.** Every CAPS content bullet is still covered and every
item CAPS names explicitly is still mandatory. A lesson that serves neither the content
table nor Section 2 is still supplement, still needs a justification, and still counts
against the 25%.

### When the video was made first

Grade 4 Sosiale Wetenskappe reverses the order above. Those videos were made before
any text existed and will not be remade, so everything in this subsection applies
only where a video already exists.

**The text still comes from CAPS.** A video script is not a source for content and
not a source for structure. Letting it be either would put a video maker's coverage
decisions where the curriculum's belong, and the video was not built against the CAPS
bullets one at a time.

What a script *is* good for is three things, and they are worth a great deal:

- **the same word for the same thing.** A video that says *boggel* and a text that
  says *bult* teaches a nine-year-old two words for one idea. Terminology drift
  between media is the same failure as drift between lessons, and worse: a lesson can
  be fixed and a video cannot.
- **the same example.** A different example for the same point splits the picture the
  learner is building.
- **what the video already carried well**, so the text does not spend budget building
  a second version of it.

And one thing it is dangerous for: **a video script has been through no fact
checker.** Where a script makes a claim that is false, the text must not repeat it.
Repeating it would launder an error through a checked pipeline into something that
looks verified.

**A script reaches the pipeline as a distilled seam, never raw.** Whoever runs the
pipeline reads the script, checks its claims, and writes a `video_naat` object into
the lesson's spec entry: the words the video used, what it covered, and every claim
the text must not repeat together with the reason it is false. The planner and the
writer read that object. **The fact checker never does**, for the same reason it
never reads the spec — a checker who knows the video said something reads the lesson
charitably.

**The video's lesson division wins, not the CAPS bullet division.** Drico, 31 August
2026: where a video merges two CAPS bullets into one lesson, the text merges them too.
His reason is the whole argument — these videos were made by a teacher out of how she
actually teaches the topic, so the seams carry information a bullet list does not.

This does **not** loosen coverage. Every CAPS bullet is still covered in full and every
item CAPS names explicitly is still mandatory. Only the division changes: coverage comes
from CAPS, the seams come from the teacher.

**A merged lesson gets one lesson's budget, not two.** The sub-topic's measured volume is
divided evenly by the new, smaller lesson count — Drico: *"We treat it as one lesson,
therefore the volume should be suitable for one lesson as well."* So merging does not buy
length; it spends it. Expect the merged lesson to be the tight one in its sub-topic, and
plan for that rather than discovering it in a revision: divide its budget by its item
count before writing, and treat the three-sentence pattern as the ceiling.

**Where the video is wrong, route around it.** Do not repeat the claim, and do not
correct it in the text either. A learner who watches and then reads should not be
handed two stories; they should simply not meet the false one a second time. Then
tell the person who owns the video, because what to do about the video is a decision
about the video and not about the text.

### When the lesson is a text to be read

Some CAPS content is not an explanation of a concept but a text the learner reads.
Life Skills asks for it directly: *"Weeklikse lees deur leerders: lees vir genot"*
appears under **every** Grade 4 PSW topic, with the subject of each read named, so
half that subject's lessons are readings rather than explanations. An Afrikaans
Huistaal cycle is built around a core text the same way.

**A `leesstuk` block carries a lesson's volume in place of `studie` blocks.** It
counts against the budget and is measured against the same register band, because a
learner reads it the same way and the band's floor guards against the same collapse
into fragments. The gate fails a lesson that has neither.

**It is exempt from the chunking guidance only** — the 3–10 block count and the
30–110 words per block. Those exist for explanation broken one idea at a time. A
story is one continuous piece, and measuring it in chunks measures it as the wrong
kind of thing.

Three things do **not** change, and they are the ones a writer will assume have:

- **Everything in it is checked.** A reading is not a free space. Its claims are
  verified exactly as anywhere else.
- **Where it retells something belonging to a culture, the attribution is checked**
  against sources outside any textbook, and a detail two published sources disagree
  about is cut rather than kept. The story belongs to the people who tell it.
- **The register floor still applies.** Writing "simply" for a young reader
  collapses into fragments just as fast in a story as in an explanation.

Some readings have no video. Where that is so, the text is not merely the floor —
it is everything, and the argument for standing alone is stronger rather than
weaker.

## What a Wolkskool lesson is

A lesson maps to **one CAPS content bullet**, not to a textbook page or section.
CAPS bullets are the unit the curriculum actually specifies, and using them keeps
lesson boundaries independent of any publisher's chapter design.

One exception, and only one: where a video was made before the text and merged two
bullets, the text follows the video's division. See "When the video was made first"
above. Coverage still comes from CAPS; only the seams move.

Content divides into three tiers. The tier determines whether it counts against
the study budget:

| Tier | What it is | Budget |
|---|---|---|
| **Core** | Named in the CAPS document | Counts. Mandatory. |
| **Aanvulling** | Not in CAPS, but needed for the concept to make sense or to serve the CAPS focus question | Counts. Max ~25% of study budget. Needs a written justification in the lesson spec. |
| **Scaffolding** | ELI10 layer, glossary entries | Does not count. Uncapped. |

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
python3 skills/wolkskool-inhoudstandaard/scripts/spec_check.py spec.json
```

**Every path in this skill and its references is written from the repository
root**, which is where agents and the runner actually work. Paths relative to this
skill's own directory look shorter but resolve to nothing from where they are used,
and an agent that cannot find the validator will either skip the check or invent
one.

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
    {"tipe": "begrip", "term": "stoomketel", "teks": "..."}
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

Anchored on measured volume, never guessed, and then clamped into the grade's band:

### The band

| Grade | Floor | Ceiling | Status |
|---|---|---|---|
| 4 | **350** | **450** | decided by Drico, 7 September 2026 |
| 5 | **400** | **500** | decided by Lampies, 16 September 2026 — teaching lessons and reading pieces alike |
| 6 | **450** | **550** | decided by Lampies, 21 September 2026 — one step up from Grade 5, teaching lessons and reading pieces alike |
| others | — | — | unbanded until decided the same way |

**Why a band, when the budget is supposed to be a measurement.** The measurement was
honest and the result was incoherent from a learner's seat. The delivered Gr 4
Natuurwetenskappe lessons run from **169 study words to 811**, because textbook volume
per sub-topic divided by lesson count is arithmetic and nobody chose the spread.
Seventeen of twenty-five exceeded 450. A learner meeting a 169-word lesson one day and
an 811-word one the next is the failure this prevents.

**The floor matters more than the ceiling.** A 169-word lesson cannot be the revision
instrument the whole architecture rests on. Where the measurement lands below the
floor, the honest answer is usually to merge with an adjacent bullet rather than to
inflate.

Grade 4 is also the first year learners write exams, which is Drico's own reason for
the ceiling: what a nine-year-old is expected to study is small.

**One exception to the ceiling, and it must be written down.** Where a CAPS bullet
names items explicitly, every named item is mandatory and that is not negotiable
against a word count — transport water lesson 6 owes rafts, canoes and reed boats
*plus* the five ships CAPS names *plus* how a sail works. Such a lesson may exceed the
ceiling if its spec entry carries `plafon_uitsondering` saying which items force it.
The validator fails a spec that goes over without one.

**The floor has an exception too, and it needs one for the same reason.** Sometimes the
curriculum decides, not the arithmetic. Gr 4 Geskiedenis Kwartaal 1 is five
introductory videos about what history is and what a source is, and CAPS gives 7 of
that term's 15 hours to a project rather than to content — Drico set those lessons at
200 words with a 250 maximum, calling it purely an exception. Inflating them to 350
would pad them, which is the floor's own failure pointing the other way. A lesson under
the floor needs `vloer_uitsondering` saying why the content is genuinely thinner than a
Grade 4 lesson should be.

**A clamped budget breaks parity with the measurement on purpose**, so
`totale_begroting` is then not the measured volume and the validator says so in a note
rather than failing. Specs written before the band carry `band_vrygestel` with a
reason: their lessons were already built, and the band governs what is planned from
now on.

**The band governs both budget bases.** Applying it only to measured budgets left the
requirement-based specs outside it — and those are the ones where a number is most
easily typed rather than derived.

### The arithmetic

```
onderwerp_woorde = pages_for_subtopic x words_per_page    (from the profiler)
lesson_budget    = clamp(round(onderwerp_woorde / lesson_count), floor, ceiling)
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

**Prefer the everyday word, and keep the house list.** `references/woordkeuse.md`
records words to avoid and what to use instead. It exists because the gate measures
how *long* a word is and never whether it is *known* — `oewer` and `ranke` are both
five letters and two syllables and clear every threshold, and both had to be caught
by a person reading the first lesson. Nothing in the pipeline can do that job, so the
list is how a word gets fixed once rather than four hundred times. Add to it whenever
review flags a word.

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

**Lessons carry no retrieval questions.** They used to end with three. Drico's
layout team was told to ignore them, so they never reached a learner — the published
page for the first Grade 4 science lesson contains no question marks at all — and
they stopped being written on 2026-08-21. `vraag` remains a valid block type because
four lessons already contain them; nothing new produces one.

**What the questions used to carry, and now must live in the study text: evidence.**
A question was sometimes the only place a lesson gave a learner something observable
to reason from. One Grade 4 question set out dry yeast in warm sugar water going full
of bubbles; the study text only said that yeast "wakes up". If a lesson asserts that
something is alive, or hot, or moving, and the only proof was in a question, the proof
now belongs in the study text. This is the one way removing the questions can quietly
make a lesson worse, so it is worth checking for.

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
from the text alone.

## Checker reports

Both checkers emit one shared report format so the orchestrator branches on a single
contract. Schema in `references/nasienverslag.md`. Validate before acting on a
report:

```bash
python3 skills/wolkskool-inhoudstandaard/scripts/verdict_check.py report.json --les lesson.json --spek lesse_entry.json
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
python3 skills/wolkskool-inhoudstandaard/scripts/gate.py lesson.json --grade 4 --budget 300 --log gate_log.jsonl
python3 skills/wolkskool-inhoudstandaard/scripts/gate.py lesson.json --grade 11 --budget 700 --json
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

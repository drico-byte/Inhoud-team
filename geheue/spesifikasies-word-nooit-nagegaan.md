---
name: spesifikasies-word-nooit-nagegaan
description: "Specs are never fact-checked, only lessons are. A false mechanism in a spec plants itself in every lesson from it and survives every revision of them."
metadata:
  node_type: memory
  type: project
---

Found 2026-08-25, on Term 2 lesson 14, and it is a hole in the design rather than
an accident.

## What happened

The lesson explained that a paper pillar buckles first along its fold lines. That is
backwards — the folds are the stiffest part and fail last. **The writer did not invent
it. The spec prescribed it, nearly word for word.**

The fact checker caught it in the lesson. Then the coverage checker caught the thing
that mattered more: the lesson was now right and the spec was now wrong, so sending
the lesson back to match its spec would simply **restore the error**. The spec had to
be corrected, not the lesson.

## Why it is structural

- A planner writes a mechanism down. Nothing checks it. The fact checker never sees a
  spec, by design — it must judge what the lesson says.
- Every lesson written from that spec inherits the error.
- Every revision of those lessons reinstates it, because the spec is the authority the
  coverage checker measures against.

A three-lesson sub-topic would have planted the same false mechanism three times, each
one "corrected" and then quietly put back.

## What to do now

When a fact check corrects a **mechanism or a definition** rather than a stray fact,
always ask where it came from. If it traces to the spec, fix the spec first and record
the change in the file, then let the lesson stand. Related:
[[n-regstelling-ontwrig-sy-bure]].

**Open design question for Drico:** should specs go through the fact checker before
approval? It would be slower and it would have saved this whole cycle. Raised in the
morning report of 2026-08-25; not yet decided.

## And when you correct a spec, sweep it — do not patch one place

On 2026-08-25 the same stale wording was reported by the coverage checker on three
consecutive rounds, because each time I fixed the occurrence it named and missed its
twin elsewhere in the file. A spec repeats itself by design — the same idea appears in a
core point, in the focus-question link, and in a fact-risk note — so a single-site fix
almost always leaves a live copy behind, and the next revision brief reinstates the
fault from it.

Two things that make this worse than it sounds:

- **Search for split forms, not just the word.** Searching `uitbuig` found nothing in
  the one place that mattered, because the text read `buig ... uit`. That single miss
  cost another full round.
- **Separate prescriptions from bans.** A fact-risk note that says "never write X"
  legitimately contains X, and so do the change-notes. Only prescriptive text needs
  fixing, so dump every hit with its path and decide per hit rather than replacing
  blind.

## After editing an approved spec, run the runner before launching any agent

The spec an agent reads is not the approved file. The runner extracts a per-lesson entry
into the lesson's own folder, and agents read that copy. It refreshes on every runner
invocation — but if you edit the approved spec and launch a writer without running the
runner in between, the writer reads the **previous** entry.

That happened on 2026-08-25. The comparison block in Term 2 lesson 10 had been removed
from the approved spec, and the writer opened an entry that still demanded it. It wrote
to the brief instead and flagged the mismatch, which is the right behaviour and is the
only reason it was noticed.

**Sequence: edit the approved spec → run `bin/hardloop.py` for each affected lesson →
then launch the agent.** The runner also gates any draft it finds, so expect that as a
side effect on lessons already written.

## The fact-risk list is the spec's correction layer — but correct at source anyway

A coverage checker made the useful observation that a stale `kern` point beside a
fact-risk note that overrides it is not simply a bug: **the risk list is by design the
spec's own correction layer.** It does the same thing for the strut definition as for
the triangle test. Read that way, the writer following the risk list over the core
point is the system working.

The problem is narrower than "the spec is broken": it is that the correction only
reaches a writer who reads all the way down. Three writers did; that is reading order,
not a safeguard.

**So do both.** Keep the risk note — it carries the reasoning and the sources, which a
corrected core point cannot. And also fix the core point, the coverage measure and the
depth limit at source, so nothing depends on reading order. The note becomes the record
of why, and the prescription becomes correct on its own.

## Never edit a spec between a coverage approval and the approval step

Three times on 2026-08-25 a coverage check came back approved, mentioned a stale spec
phrase as a note for later, and I fixed it straight away — which regenerates the
per-lesson entry, invalidates the report that just approved, and sends the lesson back
to `WAG_VIR_NASIENERS`. Each time it cost a full coverage re-run for a change the
lesson already complied with.

**The order is: coverage approves → approve the lesson → then fix the spec nit.** The
nit is by definition not blocking, or the checker would have failed the lesson for it.
Record it, approve, then tidy.

The one exception is a spec error the checker *escalates on* — there the spec must be
fixed first, because the lesson cannot be approved against a prescription that is
wrong. Tell those apart by the verdict, not by how serious the note sounds.


## The safeguard you write to fix a finding is itself an unchecked mechanism

2026-09-03, Grade 4 Lewensvaardighede, the HIV lesson. A fact check found the
analogy ending in an inevitable outcome. I fixed it at source, as this note says
to — and the condition I wrote into the spec said, in as many words: *someone
puts the posts back, and that is what the medicine does.*

That is not what treatment does. Antiretrovirals stop the virus copying itself so
that **no more posts are taken out**; the body then rebuilds its own. The writer
implemented my instruction faithfully and the next fact check found it.

**A remedy is a mechanism claim, and nothing fact-checks it.** Worse than an
ordinary stale field, because of how it is written: mine was capitalised, numbered
"VYFDE VOORWAARDE", and carried its own reasoning and a WHO citation for the half
that *was* right. It read as settled. A writer has no way to tell a researched
condition from an invented one.

Two specific costs, both of which a nine-year-old would have absorbed:

- **An endless race.** One agent removing, another replacing, week after week, is
  read as *the medicine only buys time* — the single worst belief to leave with a
  child who has to take it every day.
- **A passive body.** Strangers dismantled and patched the child's fence while the
  child watched, when the rebuilding is the body's own work.

**So: when you write a fix into a spec, check the fix.** Cite the source in the
field itself, the way a fact checker would have to. If you cannot cite it, say in
the field that it is unverified, so the next reader knows which half is which.

Related: [[die-ooreengekome-bewoording-kan-self-verkeerd-wees]] — reconciling makes
two lessons agree, not right. Same shape: the authority you write to settle a
question inherits none of the checking that a lesson gets.

## A checker's "a person must decide" can be a false choice

The same round, the checker asked whether a Grade 4 lesson should carry the fact
that 10-40% of people starting treatment with a low CD4 count never reach a normal
one, and framed it as a choice between frightening a child who has HIV and telling
them something untrue.

Both horns were real and it was right to escalate rather than guess. But there was
a third option it had not considered: **state the mechanism truthfully and promise
nothing.** "The medicine stops posts being taken out and the garden builds back"
is true, is hopeful, and nowhere requires that every post returns. The statistic
stays out; so does the promise.

Before escalating a checker's dilemma, look for the option that makes the dilemma
disappear. Often it is *claim neither*, which is also [[onsekere-ekstras-word-gesnoei]].


## Correcting a false claim, I kept its over-reach and only changed its angle

7 September 2026, Gr 4 SW, the Wright brothers lesson. A fact check found the spec
crediting the engine with letting the pilot choose **where** to fly. Route-choosing
arrived in 1905, so that was wrong. I fixed it at source and wrote the replacement
myself: the engine let the aeroplane *keep flying and climb without waiting for a
wind*.

The next fact check found that too. The 1903 Flyer took off into a headwind of about
27 mph which supplied 80-90% of the airspeed it needed; its groundspeed on the first
flight was 6.8 mph, and when the brothers moved to a windless field in Ohio the next
year they had to build a catapult to get airborne at all. The engine did not end
their dependence on wind. The same sentence also said the pilot could choose how far
and how long he stayed up — the four flights lasted 12 to 59 seconds and ended when
the machine decided.

**The shape of the mistake.** I identified the false claim correctly and then reached
for the nearest true-sounding replacement, which carried the *same over-reach at a
different angle*. Both versions said the engine gave the pilot a freedom he did not
yet have; I only changed which freedom. Fixing the direction of a claim is not the
same as fixing its strength, and the strength is usually what was wrong.

**And it was true in general, false in place.** "An aeroplane with an engine does not
depend on the wind" is true of aeroplanes. It was false where it sat — immediately
after a block saying the brothers had to wait for the right wind, and immediately
before 17 December 1903. A replacement claim has to be checked *in the position it
will occupy*, not on its own. Same failure as
[[elke-sin-waar-die-prentjie-vals]], arriving through the spec instead of the draft.

**What would have caught it earlier:** the lesson's own next sentence already said
the longest flight that day was under a minute. A replacement that contradicts a
neighbouring sentence the checkers have already confirmed is wrong on the spot, with
no research needed. Read the neighbours before writing the fix, not after.

The honest contrast for that lesson turned out to be **sinking versus staying up** —
a glider must lose height continuously, a powered machine can drive itself forward —
which needs no claim about wind at all.

## The lesson's own provenance note is unchecked too, and writers trust it

8-9 September 2026. The photography lesson's provenance note misdescribed its own text
**three times** in two days:

* It said the "see it immediately" sentence "stays general" — the block opened with a
  decade marker, so everything under it read as the 1990s.
* It said that sentence was "already in the present tense about today's cameras and
  therefore safe" — it had no time marker at all, and **present tense alone is not a
  time marker**. "A camera captures one moment" reads as a claim about cameras, not
  about now.
* It ended by saying the status should be `konsep` after the gate had already passed
  the revision, so the note and the status field contradicted each other — and the
  field is what tools read.

**Why this belongs with the spec problem.** A `herkoms.nota` is written to survive to the
next revision, and it does its job — several corrections this quarter were saved because
a writer wrote down why something was cut. But it is a **claim about the text**, made by
the same pass that wrote the text, and nothing ever checks it against the text. It is the
spec problem one level down: an unchecked artefact that the next reader treats as
settled.

**How to apply.** When a note says the text does X, **read the text**. Do not carry the
note's description into a brief — quote the sentence instead. And when a fact check or a
coverage pass contradicts a note, the note is the thing that was wrong until proven
otherwise, because the checkers read the text and the note only claims to.

The related trap, from the same lesson on the same day: a *requirement* can be phrased so
that it reads as prescribed prose. A coverage checker caught "a photo is the FIRST way
that captures a moment as it really looked" sitting in a field whose own fact-risk note
forbids "first" claims — it was meant as the narrowed contrast, not as text to write.
State what a field **requires**, not how the sentence should read.

### The status field looks like it lies, and it does not — the gate moves it between passes

Two writers in a row have reported that the status field "was recorded as fixed without
being fixed": their own previous note said it had been set back to draft, and they opened
the file to find `gated`. Neither was wrong about what it saw, and there is no bug. The
sequence is:

1. the writer sets the status to draft and records that in its note;
2. **the gate runs and passes, and sets the status to gated**;
3. the next writer opens the file, sees `gated` beside a note saying draft, and reasonably
   concludes the note was false.

So it is a benign race between the writer and the gate, not a broken field — and it will
recur every time a lesson is revised and gated between two writer passes, which is most
of them. **Do not send anyone to chase it.** Say in the brief that the gate has run since
the note was written, if it has.

The writers' general lesson stands and is worth keeping separately from this: *a note
saying a field was changed is not evidence that it was; re-reading the field is the only
evidence.* That is true, and it is why both of them checked.

## Eleven faults in one pass, before a single lesson was checked

**7 October 2026.** I had one sub-topic's requirements fact-checked as a document, in
advance of any of its ten lessons entering the pipeline. Roughly **170 assertions
checked: 11 contradicted or materially wrong, 9 unsettled, 2 not reached** — seven of
the eleven being live orders. **Two were already sitting in drafts.** Not one of those
eleven could have been found by the per-lesson pipeline, because the fact checker never
sees a requirement and the draft matches its requirement perfectly.

**Do this for every remaining sub-topic before its lessons enter checking.** It is the
cheapest check we own: one agent against the requirements, versus a writer round plus a
checker round per fault discovered the other way.

**Four shapes it found that nothing else would have:**

* **A prohibition whose stated reasons were all false.** The field forbade hedging a
  superlative because three named bodies "confirm" it — two of them say a different
  word, and the third's main article does not say it at all. The prohibition, not the
  claim, was the fault.
* **"Even the opponent concedes it" as a licence.** A superlative was allowed to stand
  absolute because the dissenting scholar supposedly conceded it. He declines that
  category for *everything* — so conceding nothing. **A concession argument needs the
  opponent's own framework checked, not just his conclusion on one case.**
* **A citation that does not say the thing.** The paper cited for a claim does not
  discuss it; the claim belongs to the rival framework. The fact survived, the
  attribution and the reasoning did not.
* **Two lessons flatly contradicting each other**, both live orders, written the same
  day in different lesson entries — structurally invisible, like
  [[twee-beplanners-albei-plaaslik-reg]].

## Check for the record marker before anything else: a whole file may have none

The same pass found that specification has **no `ALLES HIERONDER` marker anywhere**.
Every dated correction sat *inside* a live ordering field, and several records issued
orders of their own. So in that file nothing could be read as record-only, and a writer
reading top-down met every old correction as a live instruction.

**That is a per-file property, and I had assumed it was a house-wide one** because the
sub-topic I had been working in uses markers throughout. The stale-order sweep cannot
tell you: it *lists* marker-less fields, which is the same output as a file that simply
has few records — see [[die-korrigeerde-opdrag-bly-in-die-veld-staan]] for the
behaviour, which I have had inverted before.

**So, on opening any specification for the first time: count the markers.** None means
every record in the file is potentially an order. And when introducing markers, the
dangerous move is **filing a record that issues a real order below the line** — that
withdraws a requirement by tidying. Lift those above it first.

## A rebuild preserves what it does not know is wrong

**8 October 2026.** A requirement field was rebuilt into the house shape that morning —
orders first, one marker, then the records — carefully, with an inventory check proving
nothing was lost. That afternoon a fact check contradicted its **closing ordering
sentence**, which had survived the rebuild untouched: the lesson's comparison of two
places was ordered to be "a comparison in TIME and nothing more", and it fails both
against the archaeology (Chinese celadon and thousands of imported glass beads reached
Mapungubwe in exactly that century) and against the lesson's own next sentence, which
makes a second, non-temporal comparison.

**The inventory check is why it survived.** That check exists to prove nothing was lost in
the restructuring — so it actively guarantees that every claim comes through. **It is a
conservation test, not a truth test**, and the two pull in opposite directions.

**So "this field has been rebuilt" means tidy, not true**, and I had been treating the two
as one. Of the two things a requirement field can be wrong about:

* **structure** — a stale order, a record that orders, a buried instruction: a rebuild
  fixes these, and the sweeps can see some of them;
* **substance** — a false claim in a live order: **only a fact check finds this**, and
  nothing in the per-lesson pipeline ever runs one against a requirement.

**How to apply.** When a field is rebuilt, say in the record that it was restructured and
**not** verified, and name what was not tested — the house rule against marking a block as
checked applies hardest right after a careful pass, because a careful pass is what makes a
field look settled. And when a sub-topic's requirements get their pre-writing fact check,
**do it after any structural rebuild rather than before**, or the rebuild hands back a
field that reads as freshly examined and is not.

Related: [[die-korrigeerde-opdrag-bly-in-die-veld-staan]] (the structural faults),
[[moenie-in-die-spek-skryf-wat-jy-nie-nagegaan-het-nie]] (my own rulings being the least
examined sentences in the repository).

## Four of seven contradictions in one lesson were the specification's, not the draft's

**8 October 2026, Graad 6 history, Mapungubwe lesson 1.** The fact check returned 39
items: 29 confirmed, **7 contradicted**, 3 tested-and-unsettled, nothing unreached. I
then read the requirement fields against the findings, and **four of the seven were
ordered by the specification in so many words**:

* the change-and-continuity ledger, enumerated in the requirement — so the draft's
  incomplete list IS the requirement's list, and narrowing only the draft would have
  failed coverage and been rebuilt next revision;
* "farming and cattle-keeping stayed the same", which is false for exactly the three
  capitals the lesson is about (the cattle byre moved outside the settlement at K2, and
  the last capital follows a different settlement pattern altogether);
* the size comparison, ordered flatly while the same lesson's fact-risk field said it
  needed verifying — see [[kern-en-feiterisiko-weerspreek-mekaar]];
* "the same valley, three centres one after another", which is the sentence that makes a
  learner read one community moving its centre, when newcomers from the south founded
  the second capital and took political control.

The remaining three were genuinely the writer's: two unsourced examples of what a leader
decided, an ambiguous time reference, and three glossary entries whose second sentence
read as part of the word's meaning.

**How to apply.** When a fact check comes back, **do not brief the writer first.** Read
each finding against the field that ordered it and sort the list in two before anything
else: what the draft did, and what the draft was told to do. They need different repairs
in different files, and a draft-only fix to a specification fault comes back — see
[[die-spek-was-die-fout-sewentien-keer]]. Roughly half, on this evidence.

## Three specifications checked as documents in one day: thirty-one false claims

**8 October 2026.** I made this the practice for every remaining Graad 6 Sosiale
Wetenskappe sub-topic and ran it on three files. The yield:

| file | wrong | contested | verified / identified |
|---|---|---|---|
| Mapungubwe | 11 | - | ~170 |
| Medisyne oor tyd heen | 9 | 2 | 58 of ~160 |
| Ontdekkingsreisigers | 11 | 5 | 55 of 169 |

**Read the last column before the first.** Two of the three checks verified only about a
third of what they had identified, and the wrong claims came out of that third. **These
are floors, not totals** - and in the medicine file the densest concentration of risk
was checked LAST, which is why its count rose from 6 to 9 when the final cluster came
in. A number from a partial pass is evidence about the part that was read and says
nothing about the rest.

**Three things the pattern shows, beyond the count.**

* **Roughly half of a lesson's contradictions are its specification's**, not its
  writer's. Measured on Mapungubwe lesson 1: four of seven.
* **The guards are as wrong as the requirements, and more dangerous.** See
  [[die-veilige-vorm-maak-die-fout]]. A fact-risk item is written as the honest form, so
  a false one is copied without question.
* **Two of the three files contained no record-marker line anywhere**, while five to
  nine fields in each embedded a dated correction - so in those fields the withdrawn
  wording quoted inside the record read as a live order. In the medicine file eight of
  nine nevertheless had the corrected form on top; the one exception was a correction
  whose own reasoning was false.

**How to apply.** Fact-check the specification **before** its lessons are drafted, not
after. The per-lesson fact check sees only finished text, by which time a false
requirement has been written, gated, and defended by the coverage check - because the
draft matches the requirement. None of these three subjects' lessons had been checked,
and medicine's had not been drafted at all, so every one of these repairs cost nothing
but the reading.

## 13 October 2026: three false claims IN SPECS in one day, each costing a writer round

All three were delivered faithfully by a writer and caught only in the lesson that wrote
them out — which is the whole mechanism of this note, measured three times in a day.

1. **Gr 6 SW Medicine 6, the dye reason.** I wrote into the spec that germs are colourless
   and must therefore be coloured before a microscope shows them, and that Koch changed the
   dye. A fact check read all eighteen pages of Koch's own 1882 paper and refuted every
   part: *"The bacilli are also observable unstained in unprepared specimens"*; several
   pathogens are named for their colour; and he changed the dye's **solution**, not the dye —
   *"it is the strongly alkaline reaction of the solution, which counts"*.
2. **Then my correction over-shot.** I had the greasy outer layer removed entirely. It is
   *why* the dye would not stick, and the dye not sticking is Koch's own explanation — so the
   next round had to put the reason back in a form he could have known.
3. **Gr 6 SW Medicine 7, the careful "first".** The spec ordered "the first antibiotic to be
   **widely used as medicine**". That hedge is what makes it false: sulfa drugs were in
   clinical use from 1935, penicillin reached a patient in February 1941, and sulfa drugs sit
   inside the lesson's *own* definition of an antibiotic. The **unhedged** form is defensible
   under the narrow microbial-origin sense, so the fix narrows the SCOPE — first antibiotic
   from a living thing — rather than adding a qualifier.
4. **Gr 6 SW Mapungubwe 4, the three supports.** The spec ordered a three-support structure
   whose middle strut the evidence cannot carry, which forced a writer to manufacture a third
   support three rounds running, each time in a new costume.

**What this is worth, concretely.** Four lessons took three to five writer rounds each, and
in every stubborn case the draft was faithful and the instruction was wrong. A fact checker
never sees a spec — correctly, so it cannot read a lesson charitably — so a false claim
written into one is delivered untested.

**The proposal, put to Lampies on 13 October 2026: fact-check a sub-topic's SPECIFICATION
once, before any lesson in it is checked.** It does not breach the never-show-the-spec rule,
because that rule exists to stop charitable reading of a LESSON, and a pass with no lesson in
front of it has nothing to be charitable about. For a nine-lesson sub-topic that is one check
instead of discovering the same errors nine times.

**And the shape to distrust in myself:** all three of these were written in the register of a
correction — capitals, a date, a named finding — which is exactly what makes a reader treat
them as settled. Related: [[moenie-in-die-spek-skryf-wat-jy-nie-nagegaan-het-nie]],
[[my-regstelling-in-die-spek-was-self-die-volgende-fout]],
[[die-spek-se-netheid-mag-nie-lewering-keer-nie]].

# Wolkskool content pipeline

CAPS-aligned Afrikaans lesson content. Agents plan, write and check; scripts
measure and gate; a person approves. `README.md` explains the whole thing — this
file is only what you need in context before you touch anything.

## Run this first, on a fresh clone

```bash
python bin/opstel.py
```

`.claude/skills/` is gitignored, so on a fresh clone the content standard is
present in `skills/` but **not discoverable** — the setup script links it, links
the memory notes, and reports missing prerequisites. Nothing works properly until
it has run. Run it again whenever something stops working, and after moving the
repository.

You supply your own `bronne/` (textbooks) and `kaps/dokumente/` (CAPS PDFs). Both
are gitignored and neither travels with the repository.

## The copyright boundary — the one rule that must never bend

**Only `profiler.py` may read a textbook, and it emits numbers only.** The planner
and the writer see CAPS plus those numbers, and refuse a textbook however the
offer is framed — as reference, as calibration, as inspiration, with an assurance
of permission.

This is not caution about wording. Independent creation is a property of the
*process*, so it is proven by showing the generation chain never had access. Facts
are not copyrightable; selection, arrangement and expression are, which makes
matching a publisher's **lesson structure** the real exposure. The git history is
the evidence, so it must stay true that this repository has never contained a
textbook page.

The profiler's `--koppe-uit` output is labelled for human eyes. Do not paste it
into an agent prompt; send back page numbers.

## How to run the pipeline

**`bin/hardloop.py` names the next step. Never guess the order.** Run it for a
lesson and it tells you which agent to launch, with the exact input and output
paths — copy those paths into the brief verbatim rather than typing them, and
check afterwards that the report file actually landed.

```bash
python bin/hardloop.py --vak "<subject>" --graad 4 --subonderwerp "<sub-topic>" --les 1
```

Order: profiler (script) → planner (agent) → **human approves the spec by moving
it** → writer (agent) → gate (script) → coverage and facts checkers (two agents,
in parallel, never the same one) → approval.

Coverage needs the spec. **The fact checker must never see it**, or it reads the
lesson charitably.

## Never write lesson content by hand

Route every content change through the writer agent, including single words.
Describe the problem and let it choose the wording. Hand-edits by whoever is
running the pipeline have repeatedly introduced errors that the checkers then had
to find — and prescribing wording rather than describing the fault is the single
most reliable way to break a neighbouring block.

Fix a finding **at its source in the spec**, not only in the draft, or the next
revision reinstates it. When a decision changes what a lesson says, the spec has
to move in the same breath.

## The Afrikaans check happens outside this pipeline

A separate tool checks grammar, idiom and direct-translation errors, and it is
better at Afrikaans than we are. It will also **undo our decisions unless it is
told not to** — every protected word reads like ordinary Afrikaans that could be
improved, which is exactly why it needs protecting. `energie` where `krag`
sounds more natural. `die meeste` where `byna elke` is smoother. `ungquphantsi`,
which looks like a typo.

```bash
python bin/taalnasien.py --vak "<subject>" --graad 4 --subonderwerp "<sub-topic>" --les 1
```

That builds the block to paste in: the instruction, the protected words with the
reason for each, then the lesson. Glossary entries shared between lessons are
protected automatically, by reading the other lessons.

**When a ruling settles a word, write it into `kaps/beskermde-woorde.json` in the
same breath.** The spec records it for our own writer; nothing carries it
downstream unless it is there. Give the reason, not just the prohibition — a
checker that understands why holds the line when a sentence reads awkwardly.

## Write the whole year before finishing any of it

**Drico's process, decided 30 August 2026, after a subject was written the other
way and had to be repaired lesson by lesson.**

1. Agree the whole year's structure first — every lesson, its budget, its
   register — and do the usual back-and-forth until it is settled.
2. **Draft every lesson in the subject-year before completing any of them.** Then
   find the terms that appear in more than one lesson and decide, once, which
   wording wins.
3. Only then run the rest of the pipeline — gate, checkers, approval — lesson by
   lesson.

The point of step 2 is that the drafts *reveal* which terms repeat, rather than a
planner predicting it, and reconciling them costs nothing while nothing is
delivered. Do it afterwards and every fix is a correction sheet for the layout
team.

**Fact-check the shared definitions as part of step 2**, not just reconcile them.
The improvements that hurt most did not come from writers — they came from fact
checks, which run *after* drafting. One asked whether crude oil is always thick
and dark; it is not, and that correction reached a delivered lesson months late.

## A term is defined once for the whole subject

Two lessons that define the same word differently teach two different things, and
nothing in the per-lesson pipeline can see it: the gate reads one lesson, and the
coverage checker reads one lesson against one spec entry. Drift only exists
between files.

**`kaps/gedeelde-omskrywings.json` holds one agreed wording per term**, for the
whole subject rather than per specification — some terms cross sub-topics, and a
field in one spec cannot state a rule about the subject. `hardloop.py` injects it
into every spec extract, so a writer and a coverage checker always read the
current list without anyone copying it anywhere.

```bash
python bin/woordelysdrif.py --vak "<subject>" --graad 4
```

Run it before saying a subject is consistent, and **quote the lesson count it
prints** — a sweep that read three files looks exactly like a sweep that found
nothing. It also reports a term whose wording is still *undecided*, because
lessons that happen to agree on a rejected wording look exactly like lessons that
are right.

**Two rulings, both Drico's:**

* **Examples after `soos` may differ per lesson.** What must be identical is the
  sentence itself. Lesson 9 gives wood, water and air because it teaches the three
  states; lesson 14 gives paper, wood and clay because it folds paper. Both are
  right.
* **A definition may not get richer as the year goes on.** The end-year exam
  covers everything, and a learner looking a word up in two lessons must get one
  answer. Always choose the best wording, not the newest.

When a wording changes, fix it in `kaps/gedeelde-omskrywings.json`, refresh the
extracts, and route every lesson through the writer. A third wording makes it
worse than leaving it alone.

```bash
python bin/vernuwe-uittreksels.py
```

**Run that after editing any spec and before briefing any agent.** The extract an
agent reads is rewritten only by a runner call, so an edit made and briefed a
minute later hands the agent the old copy — it will then report, correctly, that
your fix is not there.

## The language checker edits after the fact checker, and nothing re-checks it

This is a real hole, not a caution. The order is: fact check, then the outside
language check, then HTML. A language "improvement" that changes a claim is seen
by nobody.

```bash
python bin/htmlnasien.py --html "<folder of built lessons>"
```

Run it over built lessons to compare them against the repository and the agreed
wordings. It reports three things: shared definitions that do not match,
definitions the language checker changed on its own, and protected words it
reverted. **Check the protected-word hits by hand** — `krag` is right when it
means force, and `lug` is right when it means air.

Where the checker's version is better and the term is not shared, **the
repository adopts it**, not the other way round.

## Where the rest lives

| | |
|---|---|
| `README.md` | setup, profiling a new subject-grade, the four human approval points, the HTML team boundary |
| `skills/wolkskool-inhoudstandaard/` | the content standard: schema, register bands, budgets, gate |
| `prompts/` | versioned agent prompts — always use the newest `*-v1.x.md` and say which |
| `geheue/` | accumulated rulings and mistakes worth not repeating |
| `.claude/agents/` | the four agent definitions |

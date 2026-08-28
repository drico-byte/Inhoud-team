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

## Where the rest lives

| | |
|---|---|
| `README.md` | setup, profiling a new subject-grade, the four human approval points, the HTML team boundary |
| `skills/wolkskool-inhoudstandaard/` | the content standard: schema, register bands, budgets, gate |
| `prompts/` | versioned agent prompts — always use the newest `*-v1.x.md` and say which |
| `geheue/` | accumulated rulings and mistakes worth not repeating |
| `.claude/agents/` | the four agent definitions |

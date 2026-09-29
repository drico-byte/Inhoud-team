---
name: die-uittreksel-het-sy-eie-kruisverwysings-verloor
description: The per-lesson spec extract was written out without the 39 spec-level fields its own text refers to by name, so every cross-reference in a lesson entry pointed at nothing. Fixed. Suspect the harness before the agent when several agents report the same absence.
metadata:
  type: project
---

A lesson entry says "see `buite_bestek`" and "use the wordings in
`gedeelde_omskrywings`". Those fields live on the spec, not on the entry, and
`hardloop.py` wrote the entry out on its own. So every one of those references
pointed at nothing, in every lesson ever written. Thirty-nine fields were
missing, including `profiel_konfig`, `buite_bestek`, `gedeelde_omskrywings`,
`praktiese_werk`, `geen_vrae`, `assessering` and `verifikasie_vereis`.

**What it looked like from the outside**, over weeks, as separate problems:

* a writer refusing to guess a profiler config, which I read as the writer being
  careful — it was, but the config should have been in its hands;
* briefs that had to carry constraints by hand, inconsistently, which is how a
  brief once omitted the config entirely;
* lesson 23's writer inventing two glossary wordings and flagging that it could
  not find the shared ones. Both came out different from what three later
  lessons were going to share — the exact fault `gedeelde_omskrywings` exists to
  prevent, arriving because the field never reached the writer.

**How to apply:** when two agents report the same thing missing, look at what
the harness actually wrote before deciding the agents are wrong. Same shape as
[[staat-wat-nie-gestoor-word-nie]], where I blamed the checkers for misplacing
reports the runner had archived. An agent saying "I could not find X" is
evidence about the file, not about the agent.

**A second, smaller trap in the same place.** The extract is only rewritten when
`hardloop.py` runs for that lesson. So editing a spec and briefing a writer
straight afterwards hands it the *old* copy. It happened on lesson 24: I wrote a
new overhang measure and a whole ruling about visible-versus-audible into the
spec, briefed the writer minutes later, and it reported — correctly — that
neither field existed and that the source of the fault was still open. It wrote
from the brief instead, which was right, but the brief is not the record.
**After editing a spec, run the runner for that lesson before briefing anyone.**

**One gap left open on purpose.** The staleness hash covers the lesson entry
only, not the spec-level context now written beside it. Hashing the context
would mark every coverage report in the repository stale in one commit, for a
file that gained fields rather than changed requirements. The cost of closing it
is one re-check of every delivered lesson — Drico's call, not a code decision.
Until then, an edit to `buite_bestek` invalidates nothing, and
`bin/woordelysdrif.py` is the cheap check that catches the glossary half of it.

## A term with two deliberate meanings reached the writer as nothing

Gr 6 Social Sciences, 29 September 2026. `hof` has two real Afrikaans meanings — a court of
law and a ruler's court — so it follows the `konflik` pattern: one headword, two wordings,
deliberately not reconciled. The **drift sweep already knew about those**: it excludes them
from the comparison and reports them in their own line.

**The injector did not.** A two-meaning entry has `omskrywing: null` by design, and the
injector sent only `omskrywing`, so the extract handed the writer `null` for the term. A
wording Drico had actually settled reached the lesson **only if a planner happened to have
restated it in the spec** — a property of the briefing, not of the pipeline. That is the
identical failure the `omvang` fallback sitting three lines below it had been written to
close, for unsettled terms.

It had been live for every two-meaning term in every subject: **`konflik` in Grade 4 and
Grade 5 Life Skills, both delivered and signed off, went to their writers as nothing.** Their
lessons may still be right, because the specs did restate the wordings — but nothing in the
pipeline was making that true.

**The reusable part:** when two tools disagree about whether a piece of data exists, the one
that *reads* it is not necessarily the one that *sends* it. The sweep understood the shape and
the injector did not, and nothing compared them. So when adding a new shape to a shared data
file, walk every consumer — here, the injector, the sweep, the language checker and the gate —
rather than the one that happens to be in front of me.

Fixed by teaching the injector the shape: it now sends both sentences, each labelled with
where it belongs, plus the instruction not to reconcile them. Verified by reading it back out
of a live extract rather than trusting the patch.

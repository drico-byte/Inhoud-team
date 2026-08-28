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

**One gap left open on purpose.** The staleness hash covers the lesson entry
only, not the spec-level context now written beside it. Hashing the context
would mark every coverage report in the repository stale in one commit, for a
file that gained fields rather than changed requirements. The cost of closing it
is one re-check of every delivered lesson — Drico's call, not a code decision.
Until then, an edit to `buite_bestek` invalidates nothing, and
`bin/woordelysdrif.py` is the cheap check that catches the glossary half of it.

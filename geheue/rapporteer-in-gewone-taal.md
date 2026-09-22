---
name: rapporteer-in-gewone-taal
description: "Report to Drico in plain sentences — no file paths, field names, script names, version numbers, exit codes, or measurement tables."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8f79bbfb-d2d6-48c5-804a-7410b16958f5
  modified: 2026-09-16T13:35:34.088Z
---

Report only: what I did, in plain sentences; what went wrong and what it means for
the lessons; and what I need decided, written as a real question with the options
spelled out. A few short paragraphs. If nine of ten things went fine, report the
one that did not.

Leave out file paths, field names in backticks, script names, exit codes, prompt
version numbers, and tables of measurements. They belong in the files and logs.

Two exceptions that always stay.

**A factual error in a lesson** — say plainly what was wrong and what the correct
version is. That is the part most needed.

**A term's per-lesson word counts** — when presenting a term plan, list the estimated
length of every lesson, and say which came from measuring the book and which from
CAPS. He asked for this on Term 2 and again for Term 3: "show the estimated word
count for each lesson". It is not plumbing to him, it is the shape of the term. A
short list per lesson, not a table of pages and medians.

Decision questions look like: "The lesson says a reed boat sinks after many months.
Sources disagree — some say two weeks, some say a year. Should I remove the
timeframe, or leave it?" Not a reference to a field name and a status code.

**Why:** Drico designed how the pipeline should work but does not code, and was
having to get help translating my messages — which meant losing control of his own
project. Design vocabulary he authored (the gate, the coverage checker, the fact
checker, lessons, specs, budgets) is his and is fine to use; implementation detail
is not.

**How to apply:** assume he knows the project, not the plumbing. Never explain how
it was built unless asked. Related: [[skrywer-oorlewer-nie-onderlewer-nie]]

## 2026-08-25: report only what needs him

Drico, mid-session, while a long pipeline run was producing a message per step:
"I want to preserve the context window as much as possible. From now on, only output
messages for me to read if there are issues that need me and if there are suggestions
for a new ruling."

**So: work silently. Surface only two things.**

1. **An issue that needs his decision** — a trade-off, a curriculum call, a departure
   from CAPS, something blocked.
2. **A proposed ruling** — a pattern worth making standing policy.

Everything else — gate results, checker verdicts, revisions sent, approvals, commits,
findings I can act on myself — happens without narration. It still gets recorded in the
specs, the notes and the commit messages, so nothing is lost; it just does not spend his
context.

**Why this is not a licence to go quiet on problems.** The plain-language rule above
still holds for whatever *does* get reported, and a factual error in a lesson still gets
stated plainly. The change is about volume of routine progress reporting, not about
hiding what went wrong. A post-completion report at the end of a run is still expected —
he asked for one on 2026-08-24 and called for it to be "short but powerful".

## 2026-09-16: Lampies wants the same, shorter still

Lampies (who now runs this copy, see [[ons-werk-onafhanklik-van-drico]]): "from now on keep
the text sweet and short, no jargon." Said right after a long seven-point feedback message.

**How to apply:** every rule above applies to Lampies too. Lead with the answer, keep only
what needs a decision or is a real problem, a few short lines rather than numbered essays.
No pipeline terms like "spec", "gate", "coverage checker" unless Lampies uses them first —
say "the lesson plan", "the checks".


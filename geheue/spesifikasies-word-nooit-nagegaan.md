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


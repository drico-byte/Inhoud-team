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

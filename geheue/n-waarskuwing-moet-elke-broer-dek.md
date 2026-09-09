---
name: n-waarskuwing-moet-elke-broer-dek
description: "A spec cautioned against the video's sail-shape simplification for two ships and then required that same simplification for the third — check every sibling item, and check the spec does not demand what it forbids next door."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f21c597a-2944-4014-bf02-c866813c3fa2
  modified: 2026-09-07T16:27:03.182Z
---

7 September 2026, Gr 4 SW "Vervoer op water" lesson 1. The video described three ships by
sail shape: the Chinese junk with square sails, the caravel with triangular sails, and the
Arabian dhow with triangular sails. The spec caught two of the three. It told the writer
not to call the junk's sails square (battens hold them flat) and not to distinguish the
caravel on sail shape at all (it varies by build) — and then its own core item **required**
the dhow to be described as having a triangular sail.

A dhow's sail is a **settee**: quadrilateral, a lateen with the forward lower corner cut
off. It only looks triangular. Working Arab dhows carried settees into the twentieth
century.

**Why this is not the same as a fix that fails to sweep.** Nobody made a correction here
that missed a field. The spec was *written* this way. The planner recognised a class of
error, applied the guard to two members of the class, and then wrote the error itself into
the third — in the same list, four items apart.

**Why it was expensive.** The writer flagged it while drafting, wrote what the spec
required, and said the correction belonged in `kern` rather than only in the draft. It
still cost a revision round: the phrase reached the draft in two blocks plus a glossary
entry, and the coverage checker returned HERSIEN on a lesson whose only defect was
obedience to its own spec.

**How to apply.** When a caution names a defect in one item of a parallel list — three
ships, four sources, five leaders — **walk every sibling in that list and ask whether the
same defect is present**, including in the items the caution did not name. Then read the
requirements back the other way: for each caution, grep the spec for what it forbids and
confirm no core item, focus link or expected-term entry *demands* it. The two halves of a
spec are written in different registers and nothing checks them against each other.

The tell is a list where some items are distinguished on one axis and the rest on another.
Here the junk and caravel had been moved onto size and region while the dhow was left on
sail shape — the inconsistency was visible without knowing anything about sails.

Related: [[n-spek-se-dieselfde-ding-in-twee-velde]] (that one is about a FIX that misses a
field; this one is about a CAUTION that misses a sibling),
[[spesifikasies-word-nooit-nagegaan]], [[kern-en-feiterisiko-weerspreek-mekaar]],
[[moenie-in-die-spek-skryf-wat-jy-nie-nagegaan-het-nie]]

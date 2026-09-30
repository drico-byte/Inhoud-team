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

---

**30 September 2026, Gr 6 SW Democracy lesson 1: my correction named two of the three
places, so the absolute survived a third round.**

"Nobody can see your choice in the booth" is false — an assisted voter takes a helper of
their own choosing into the booth, and that helper sees the mark. The claim lived in three
places: a study sentence, the block heading, and the glossary entry for the booth. I wrote
the correction and listed **two** of them. The writer fixed both of the two, faithfully,
and a coverage check then found the third still standing and contradicting the repaired
sentence two blocks away.

Same lesson, earlier the same day: a second absolute in that block lived in a study
sentence and a heading, and I named only the sentence.

**What this adds.** The rule above is about a caution having to cover every sibling in the
content. This is the same failure one level up: **the correction's own list of places can
be short, and nobody downstream checks that list.** A writer treats it as complete — it is
the brief — and a coverage check only catches the remainder by luck, because its job is
matching the draft to the requirement rather than auditing my enumeration.

**How to apply.** Before sending a correction that names places, search the lesson for the
claim and count the hits. Headings and glossary entries are the two that get missed, every
time, because a sweep of the study text does not reach them: a heading is a claim, and an
entry is read alone. Then write the count into the instruction — "this claim stands in
three places and all three must change" — so the writer can tell whether it found them all.

Related: [[n-begrip-word-alleen-gelees]], [[die-korrigeerde-opdrag-bly-in-die-veld-staan]],
[[vee-die-bewering-oor-al-die-spesifikasies]].

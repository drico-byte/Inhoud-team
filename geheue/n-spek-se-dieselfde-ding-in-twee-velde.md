---
name: n-spek-se-dieselfde-ding-in-twee-velde
description: "Fixing a finding at its source in the spec means sweeping every field that repeats the claim — the core items and the focus-question field said the same thing twice."
metadata:
  type: feedback
---

31 August 2026, Gr 4 SW "Vervoer op land" lesson 1. A fact check contradicted two claims
that the specification itself had planted: that an animal carried a load **further** than
a person walks in a day, and that the journey was only as fast as the animal **walks**.

I corrected both in the spec's core items and thought the source fix was done. It was not.
The lesson's **focus-question contribution field said the same two things in its own
sentence**, and I never looked at it. The writer caught it and reported it rather than
working around it — the second time a writer has pushed back and been right.

**Why it would have been expensive.** The coverage checker holds a draft to that field and
to nothing wider. An uncorrected sentence there would have marked a correct lesson as
defective, and the obvious next move — "make the lesson match the spec" — would have put
both contradicted claims straight back in. The field also reads as settled to the next
agent that opens it.

**How to apply.** When a finding is fixed at its source, **grep the whole spec entry for
the words the finding turned on**, not just the field the finding named. A spec states the
same idea in several registers on purpose — core items as requirements, the focus link as
a promise, the fact-risk list as a warning — so a claim that is wrong is usually wrong in
more than one of them. Fix them in the same breath, then refresh the extracts.

Related: [[n-regstelling-ontwrig-sy-bure]] (that one is about what a fix BREAKS; this one is
about what it MISSES), [[spesifikasies-word-nooit-nagegaan]],
[[moenie-in-die-spek-skryf-wat-jy-nie-nagegaan-het-nie]]

## It happened again on 2 September 2026, twice in one session

Both times I fixed the field the finding named and missed the others.

* **MIV is a virus.** I amended six per-lesson fields and missed a *sub-topic-level*
  word-choice rule that banned the word `virus` outright. My sweep only walked
  the lesson entries. The writer found it.
* **Conflict is between two or more people.** I fixed the `kern` item; the
  wording survived in the sub-topic's `regverdiging` and `fokusvraag_skakel`.
  The coverage checker found it and said plainly it could be planted back by a
  later revision.

**How to apply, concretely:** do not sweep by reading the lesson entry. Walk the
**whole spec file** — every nested string, sub-topic fields included — with a
regex for the wrong phrase, and confirm the count reaches zero before moving on.
Where a correction note quotes the old wording to explain the change, that one
match is expected and is the only one allowed to remain.

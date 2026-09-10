---
name: gr5-nwt-waar-ons-is
description: "Grade 5 NWT at the end of 10 September 2026 — 29 lessons drafted and gating, checks converging, five open threads."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-09-10T18:09:54.264Z
---

All 29 Grade 5 Natuurwetenskappe en Tegnologie lessons are drafted, gating clean
and inside Drico's 300–550 band. Around 130 real errors were found and fixed on
10 September 2026 across roughly 65 checker runs, and about 20 lessons were
repaired, most of them twice.

**The counter looks worse than the work.** Only one or two lessons have BOTH
checks approved on their current text, because every repair invalidates the check
before it. They are re-check-pending, not unchecked. It is converging: second and
third passes come back with two or three findings instead of seven, and the
findings shrink from mechanisms to quantifiers (metals 7 → 3 → 1; one came back
with zero). Roughly 50 checker runs remained.

**Threads that were still open:**

* Four writers running on Drico's four rulings of that day — the slate clause, the
  electricity return path, the coin-to-nail-and-wire swap, and the pollen sweep.
* `as` deliberately carries two senses (the Earth's axis; a wheel's shaft) and the
  drift sweep will always report it.
* Three terms drift only by their examples after *soos*, which a standing ruling
  allows. That is the expected floor, not a defect.
* Lesson 13's closing block now ends on shaping, which that block never
  demonstrates — left for a moderator rather than papered over.
* The `stelsel` wording, read alone, implies every system's parts do a job, while
  the same learners meet *sonnestelsel*. Recorded for Drico, not raised again.

**The one thing to carry forward.** The dominant failure was not wrong facts — it
was fixes that did not sweep. See
[[n-reggemaakte-veld-kan-nog-n-ander-fout-dra]] and
[[n-bevinding-by-die-bron-opteken-is-nie-dit-regmaak-nie]]. Run
`bin/woordelysdrif.py` after EVERY wording change, not at the end of a session;
it is what caught two sweeps I had dropped.

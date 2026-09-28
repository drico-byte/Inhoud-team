---
name: tel-die-verslae-voor-jy-se-dit-is-nagegaan
description: Two of 45 lessons had never been fact-checked and five more had lost their reports to a legitimate re-gate; only a per-lesson completeness sweep showed it.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9cbb5026-bd75-4aa5-a144-0346fd07bf1f
  modified: 2026-09-28T10:34:07.154Z
---

Grade 7 LO, 28 September 2026. I said "all 45 lessons are now fact-checked" and it was not true. A planner noticed that **two lessons had no report at all** — one of them the heaviest in its sub-topic, covering substances, sexual pressure, HIV and bullying in one lesson. A sweep then showed twenty of the 45 with no fact report and sixteen with no coverage report.

**Why, and it is two different causes:**
1. I tracked which lessons I had *dispatched* checks for, not which lessons *had* reports. Two were simply never dispatched: I revised them in a writer batch and my attention moved on with the batch.
2. The rest is the runner working correctly. `hardloop.py` archives and deletes a finished report the moment the draft hash changes, so **every lesson I re-gated after a repair silently went back to unchecked**. "Drafted and checked" becomes "drafted" with no line of output that says so.

**How to apply:** before saying a subject-grade is checked, run the count rather than the memory — for each lesson, does `les-N.feite.json` exist and does `les-N.dekking.json` exist. It is ten lines of Python and it is the only thing that sees both causes at once. Do it after every repair round, not once at the end. And when a planner or a checker says a report is missing, believe it enough to look, even when your own record says otherwise — see [[n-verslag-bestaan-nie-omdat-die-agent-so-se]] for the opposite error, which is why the sweep and not the argument is the answer.

Related: [[moenie-die-hardloper-vra-oor-n-nagesiende-les-nie]], [[staat-wat-nie-gestoor-word-nie]], [[geen-drif-is-net-so-sterk-soos-die-besluitlys]].

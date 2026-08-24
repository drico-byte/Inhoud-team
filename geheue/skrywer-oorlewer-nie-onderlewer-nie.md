---
name: skrywer-oorlewer-nie-onderlewer-nie
description: "Budget SIZE drives over/under-supply, not the depth instruction — small budgets overshoot, a large one landed under. Four measurements."
metadata:
  node_type: memory
  type: project
  originSessionId: 8f79bbfb-d2d6-48c5-804a-7410b16958f5
  modified: 2026-08-20T21:05:03.278Z
---

Four measurements now, and the pattern is not the one the standard predicts and not the one the
depth instruction was blamed for.

- Gr 4 SW "Vervoer op water" lesson 1: **279 / 257 = 1.09x**, then 291 / 257 = 1.13x after
  revision. Old writer prompt.
- Gr 4 NWT "Lewende en nie-lewende dinge" lesson 1: **420 / 370 = 1.14x**. Lesson 2:
  **405 / 370 = 1.09x**. Both written with the depth instruction ALREADY loosened to aim at ~95%.
- Gr 4 NWT "Wat plante nodig het om te groei", 2026-08-20: **623 / 650 = 0.96x**. First
  measurement ever under budget.

**What this says.** Loosening the depth instruction did not stop the overshoot at a 370-word
budget — two lessons written under the loosened wording still came in 9% and 14% over. Then the
same loosened wording at a 650-word budget landed 4% under. So the driver looks like **budget
size, not the instruction**: the writer has a natural size per idea and per block, and a small
budget forces it over while a large one leaves room.

**Caveat, stated honestly:** the 0.96x measurement changed two things at once — a much larger
budget and a topic with only three curriculum points. One data point, confounded. Do not treat it
as settled.

**How to apply.** Stop reaching for the depth instruction when a lesson misses its budget; it has
been adjusted once and the evidence says it was not the cause. Instead expect roughly 1.1x at
budgets near 350-400 and roughly 1.0x at 650+, and treat a large miss in either direction as
information about the topic rather than the prompt. The gate's +/-15% tolerance absorbs all four
of these measurements, so nothing has actually failed on volume yet.

`references/registerbande.md` still documents the opposite prediction — that lessons come in at
two-thirds to five-sixths of budget — based on one human writing one lesson. Four agent
measurements now contradict it. Worth correcting in the standard once there is a fifth.
Related: [[profiler-300dpi-land-en-lug]], [[ses-regstellings-voor-les-2]]

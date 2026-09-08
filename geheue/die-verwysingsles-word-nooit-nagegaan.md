---
name: die-verwysingsles-word-nooit-nagegaan
description: "The standard's worked reference example is read by every writer in every subject and is never fact-checked; two false mechanisms were found in it in one day, each already copied outward."
metadata:
  type: project
---

8 September 2026. The content standard ships a worked reference example — one complete
lesson, about steamships — and **every writer in every subject reads it before writing.**
Nothing in the pipeline ever checks it. It is not a draft, so the gate never sees it; it
has no spec entry, so coverage never sees it; and no fact checker is ever pointed at it.

**Two false mechanisms were found in it on the same day, both by accident.**

1. Its glossary defined a **piston** as "a sturdy stick that moves back and forth inside
   a cylinder". A piston is a *disc* that closes the cylinder tightly and slides in it.
   A stick would let the steam straight past, which is the whole point of the part.
2. Its **boiler** entry carried the wording we rejected later that day, verbatim — "the
   big container in which water is boiled" — and its prose taught the size reasoning
   outright: *imagine a giant kettle with much more steam inside, and all that steam can
   be strong enough to turn a wheel.* A boiler does not work by being large. It works by
   being **closed**, so the pressure climbs far above atmospheric; a kettle or pot lid
   lifts precisely *because* the steam gets out. The same block also had steam lift a lid
   and then had that upward push turn a wheel, with no rod and no conversion.

**Why this is the most expensive single file in the repository.** Every other error is
scoped to one lesson. An error here is *copied outward by design* — a writer reads the
example to learn the house style and takes the wording with it. The boiler drift that
cost two lessons and a sweep this week almost certainly started here: the rejected
phrase sat in this file, in a glossary entry, being modelled as correct.

Both were found by side effects, not by looking. The piston came up while checking a
different lesson's mechanism; the boiler came up because a writer fixing a real lesson
happened to mention that the reference example teaches the opposite.

**How to apply.**

* **When a mechanism, definition or comparison is corrected anywhere, grep the reference
  example for it before closing the finding.** It is one file and it takes a moment. If
  it models the error, the correction is not finished.
* **When a term gets a settled wording, check the reference example for that term too.**
  It is not part of any subject's agreed-wordings file, so the drift sweep cannot see it
  — the sweep reads drafts, and this is not a draft. That blind spot is the mechanism of
  the failure, not an incidental detail.
* Treat a change to it as a change to the standard: correct clear factual errors, but
  keep it a clean *example* — same register, same block shapes, same modest length. It
  teaches shape as much as content, so an example bloated into a physics explanation
  does its own kind of damage.

**Still open, and worth Drico's call:** this file should be fact-checked deliberately,
once, rather than by accident. It is one lesson's worth of claims and it is the highest-
leverage check available — every finding in it is a finding in every subject.

Related: [[spesifikasies-word-nooit-nagegaan]] (the same shape: an unchecked artefact
treated as settled), [[die-ooreengekome-bewoording-kan-self-verkeerd-wees]],
[[n-clean-toets-is-so-wyd-soos-sy-omvang]] — the sweep that reads only drafts cannot see
this file at all.

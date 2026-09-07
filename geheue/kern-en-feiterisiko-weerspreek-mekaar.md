---
name: kern-en-feiterisiko-weerspreek-mekaar
description: "A spec's kern can contradict its own feiterisiko — and kern wins, because coverage tests against kern. Three writers caught this in one day."
metadata:
  type: feedback
---

7 September 2026, Gr 4 Sosiale Wetenskappe. Three separate writers reported the same
structural fault in three different specs, and none of it was visible to me.

A planner writes `kern` as the content a lesson must cover, and `feiterisiko` as warnings
about how to state it safely. **Nothing checks that the two agree**, and when they
disagree `kern` wins — because a writer is obliged to cover `kern`, and the coverage
checker tests against `kern` too. So a `feiterisiko` entry saying "do not claim X" sits
beside a `kern` item that requires exactly X.

The three:

* **Kwartaal 1 les 5.** `kern` offered *"wie die verlede verstaan, verstaan die hede
  beter"* while its own `feiterisiko` warned that reasons must read as reasons. The
  writer wrote the *helps* version and said the spec's phrase was missing on purpose.
* **Leiers les 4.** `kern` said *"In 1994 kon almal vir die eerste keer stem"* — literally
  false, since white South Africans voted in earlier elections — while the same spec's
  `feiterisiko` gave the safe form.
* **Kwartaal 1 les 4.** `kern` required *"die jare wat met 18 begin val in die 19de eeu"*
  while the seam said not to settle the century convention; the example only holds under
  the loose one.

**A fourth of the same family, worth keeping together:** the requirement that Gandhi's
lesson *show* courage lived only in a coverage table and never in `kern` — invisible to
the writer working from `kern` and to the checker testing against it.

## How to apply

**When a `feiterisiko` entry contradicts a `kern` item, fix the `kern` item.** The
warning is usually the checked half and the requirement usually the drafted half.

**And read a new spec for internal disagreement before briefing a writer** — not just for
whether each field is right. Grep the entry for the words a warning turns on and see
whether a requirement uses them. This is the same sweep as
[[n-spek-se-dieselfde-ding-in-twee-velde]], one level up: there the same claim appeared
in several fields and one was missed; here two fields say opposite things.

**Every one of these was found by a writer, not by me.** A writer told to report what it
thinks is wrong with the spec, using exact quotes, is the cheapest fact check in the
pipeline — it reads the whole entry closely because it has to write from it.
Related: [[spesifikasies-word-nooit-nagegaan]], [[n-spek-se-dieselfde-ding-in-twee-velde]]

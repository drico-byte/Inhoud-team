---
name: n-teruggetrekte-beslissing-bly-in-hoofletters-staan
description: When a ruling is reversed, sweep for the OLD RULING, not just for the old error. A superseded decision written in capitals reads exactly like a live one, and the late-corrections checker cannot see it.
metadata:
  type: feedback
---

16 September 2026. Drico settled the fourth kind of source in the morning ("leave the
name alone") and I wrote that ruling into four spec fields in capitals, as a settled
decision should be written. He reopened it that afternoon on new evidence and renamed
the category. I updated the field that *defines* the kind, the two neighbouring
lessons and the agreed-wordings file — and left all four of the morning's rulings
standing, each still saying in capitals that the name stays and that no second name
may be introduced.

A coverage checker caught it and refused to approve a draft that was already correct,
with the right reason: the next writer or checker to read those fields would put the
old name back over a lesson that is currently right.

**This is the sixth time this one specification has produced this shape**, and it is
worth separating from its cousins:

* [[n-feiterisiko-is-nie-n-regstelling-nie]] — the correction is appended while the
  opening line keeps giving the old order.
* [[n-spek-se-dieselfde-ding-in-twee-velde]] — the claim lives in several fields and
  the fix reaches one.
* **This one** — the *decision itself* was reversed, so there is no "error" to search
  for. The stale text is a correct record of a ruling that is no longer in force, and
  it is written in the confident register that settled decisions get.

**Why `bin/laat-regstellings.py` cannot help.** It compares dates: a `feiterisiko`
newer than the ordering field it contradicts. A ruling reversed the *same day* trips
nothing, and the reversal is not a fact-risk note at all. The tool finds late
*corrections*; it does not find withdrawn *decisions*.

**How to apply.** When a decision is reversed, grep the whole spec for the words of
the OLD decision before doing anything else — its distinctive phrases, the quoted
words the person used, the prohibition it carried — and count the hits. Do not patch
the fields a checker happened to name; it only saw the ones its own lesson reads.
Then leave each old ruling in place *inside a bracket* that says it was withdrawn and
when, rather than deleting it: the record of a reversal is worth keeping, and it is
the surrounding bracket, not the deletion, that stops it being read as an order.

---
name: moenie-n-regstelling-verder-vat-as-die-bevinding-nie
description: "A checker found a rule attached to one pair; I wrote it into the spec as a general rule. It isn't general, and the lesson then broke it in the next block."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9cbb5026-bd75-4aa5-a144-0346fd07bf1f
  modified: 2026-09-29T20:53:09.128Z
---

A fact checker found that the compare-equal-sized-pieces rule was hung on the
weight pair alone, and that stiffness needs it too. Correct finding. I then wrote
into the specification that it is a **general** rule for comparing materials.

That is false. Size changes the answer for weight, for stiffness and for strength.
It does not for hardness or for soaking up water — a small diamond is as hard as a
big one, a small scrap of cloth soaks up as well as a big one. The next checker
caught it, and caught the lesson breaking its own new rule one block later, where
a bundle of wool stands against a single cloth.

**Why:** the finding named two pairs. I answered with a slogan that covered five.
A slogan is easier to write into a spec than a condition, and it reads as stronger
guidance — which is exactly why it is dangerous, because the spec is the authority
and every lesson from it inherits the overreach.

**How to apply:** correct exactly as far as the finding reaches, and where a rule
is conditional, write the condition and the exceptions into the spec rather than
the slogan. Before writing any "always" or "general" into a specification, name the
cases where it does not hold — if I can't name them, I don't understand the rule
well enough to prescribe it. Related: [[n-regstelling-ontwrig-sy-bure]], and the
standing habit of describing the problem rather than prescribing the words.

**It happened twice more on the same rule.** After narrowing it, I wrote that size
does not matter for hard-or-soft — true of hardness, false of softness, because the
lesson's own test needs the cloth folded thick. And the old closing "always compare
equally sized pieces" in the weight block now contradicted the bounded version in
the opening block: correcting a rule in one place turns its unbounded twin
elsewhere into a contradiction.

The thing I kept collapsing was two different questions. Does the **property**
depend on the size of the piece — no, for hardness and absorbency. Does the **test**
have enough material to work — yes, a thin layer on a table reads as hard because
you feel the table through it. Both true, and a single sentence carrying both is
wrong every time. The specification now states them as separate halves with the
cases named.

Three rounds on one rule. The tell I missed twice: I was editing the rule's wording
instead of asking what the rule actually is.

**29 September 2026, Grade 7 LO — the same overreach with the opposite sign: a REMOVAL
that reached further than its finding.** A coverage checker found one factor had been cut
from a lesson while a register still named that lesson, so a later reviser would put it
back. Correct finding, and the register named the lesson inside a clause that covered
**three** terms at once. I removed the lesson from the clause. That silently removed it for
the other two — and the lesson's own core item *orders* the mention of one of them, so the
next coverage pass would have reported an ordered sentence as surplus and a reviser could
have cut it.

**The shape to check for: before taking an item out of a list, read what the list's clause
is actually about.** A list of lessons under one term is safe to edit; a list of lessons
under *"term A, term B and term C"* is three lists sharing one sentence, and an edit hits
all three. Splitting the clause is the fix, not narrowing it.

This also lands in the field whose whole job is to stop a coverage checker reporting an
ordered thing as unrequested — so the overreach turned the safeguard into the fault.
Related: [[n-waarskuwing-moet-elke-broer-dek]], [[vee-die-bewering-oor-al-die-spesifikasies]].

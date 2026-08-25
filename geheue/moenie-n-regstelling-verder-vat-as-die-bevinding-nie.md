---
name: moenie-n-regstelling-verder-vat-as-die-bevinding-nie
description: A checker found a rule attached to one pair; I wrote it into the spec as a general rule. It isn't general, and the lesson then broke it in the next block.
metadata:
  type: feedback
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

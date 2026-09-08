---
name: n-ruil-wat-nie-pas-nie-moet-hard-faal
description: "A scripted spec edit whose search text does not match must stop the script; three times in one day a non-matching replace did nothing, reported success, and left the error in place."
metadata:
  type: feedback
---

8 September 2026, Gr 4 SW. Three scripted edits to specification files failed on the
same day, in three different ways, and **every one of them reported success**.

1. **The match that never fired.** A fix for the pigeon requirement searched for
   `duif`. The field says `POSDUIWE`. `str.replace` found nothing, changed nothing,
   and returned the string unaltered — while the script went on to append its dated
   correction note anyway, and printed a count that had been incremented by an
   unrelated line. So the output said one field fixed. Nothing was fixed. A writer
   found it hours later, correctly reporting that the spec still ordered the error.
2. **The regex that left the old opening in place.** A substitution inserted the new
   phrase but did not consume the words before it, producing a sentence with two
   verbs whose first half still carried the forbidden claim.
3. **The blanket replace that destroyed its own guard.** Replacing a phrase
   everywhere also replaced it inside the caution quoting it *as forbidden*, so the
   caution ended up forbidding the phrase the requirement asked for.

**Why this is worse than an ordinary bug.** A specification is read as settled. A
correction note that is present, dated and sourced looks exactly like a completed
repair — so a silent no-op does not merely fail, it actively *certifies* the error
as fixed and suppresses the next look. The only reason all three were caught is that
writers and coverage checkers read the fields afterwards and said so.

**How to apply.**

* **Assert every replacement.** `assert oud in veld` before the swap, so a
  non-matching search stops the script instead of sailing past. This is not optional
  tidiness; it is the only thing standing between a typo and a false record.
* **Prefer exact-string replacement to regular expressions.** Regexes on Afrikaans
  prose have failed here repeatedly — they match too much, keep the old opening, or
  reach inside a quotation that was warning against the very phrase.
* **Never let the success count come from anywhere but the swaps themselves.** A
  counter incremented by a neighbouring append will happily report work that did not
  happen.
* **Re-read the field after editing**, not the script's own summary of what it did.

The tell: your script prints a number and you believe it without having looked at
the field.

Related: [[n-skrip-wat-parse-is-nie-n-skrip-wat-werk-nie]] (the same lesson about
code that runs without working), [[n-feiterisiko-is-nie-n-regstelling-nie]] and
[[moenie-in-die-spek-skryf-wat-jy-nie-nagegaan-het-nie]] — both about the spec being
trusted as settled, which is what makes a false repair expensive.

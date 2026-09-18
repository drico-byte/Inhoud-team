---
name: die-korrigeerde-opdrag-bly-in-die-veld-staan
description: Nine times in one day I wrote a correction into a note while the requirement's opening line kept ordering the old form. Amend the ordering field FIRST, then sweep every sibling, then run the checker — in that order, every time.
metadata:
  type: feedback
---

18 September 2026. Nine separate instances in one working day, across two sub-topics,
of a single shape:

> I learn something is wrong. I write the correction into a `feiterisiko` note, or into
> a new requirement, and move on. **The field that ORDERED the error keeps ordering it.**

Coverage tests against the requirement. So the corrected draft reads as deficient, the
obvious repair reinstates the fault, and the round costs a writer pass plus a checker
pass. Every one of the nine was caught by a checker or a writer, never by me.

**What makes this different from its cousins.** [[n-feiterisiko-is-nie-n-regstelling-nie]]
names the fault; [[n-spek-se-dieselfde-ding-in-twee-velde]] names the sweep;
[[n-teruggetrekte-beslissing-bly-in-hoofletters-staan]] names the reversed-decision case.
I have written all three down and kept doing it anyway. The notes describe the fault
correctly and do not change the behaviour, because in the moment the *finding* feels like
the work and the *field* feels like bookkeeping.

**So this note is a sequence, not a description.** When a check returns a finding:

1. **Find the field that ordered it** before writing anything. Not the field the checker
   named — the checker only sees the fields its own lesson reads.
2. **Amend that field's OPENING LINE.** The correction goes where a writer meets it
   first. Anything appended below is commentary and gets skimmed.
3. **Grep the whole spec for the old form's actual words** — the instruction sentence,
   not the ruling, not the error. Count the hits and fix them all. One sentence turned up
   in **seven** fields on 16 September; an overlap example in eight.
4. **Distinguish record from order.** Leave the old wording inside a dated bracket that
   says it is withdrawn. The bracket is what stops it reading as an instruction.
5. **Run `bin/laat-regstellings.py`.** It exists for exactly this and it is cheap. It
   cannot see a same-day reversal, so step 3 is still required.

**The tell that it has happened again:** a checker reports the draft is correct but
escalates anyway, or a writer says "the spec's core item still orders the old form".
Both happened today. When a *writer* catches your bookkeeping, the bookkeeping is the
problem.

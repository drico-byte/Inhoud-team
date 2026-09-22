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

## Step 3 is harder than it reads: grep the CLAIM, not the wording

The tenth instance, an hour after writing this note, slipped the sweep the note
prescribes. I had withdrawn every wording I could remember using for a claim —
"only for white people", "kept for white people", "in practice", "reserved" — and a
checker found an eleventh entry saying first class was **"whites-only by railway
practice rather than by law"**. Same claim, none of my words.

**So step 3 is not "grep the old form's actual words".** It is:

1. Write down the CLAIM in one sentence, as a proposition — *"that section had a
   status"* — not as a phrasing.
2. Grep for the claim's **subject matter** (here: `eersteklas`, `wit`, `blank`,
   `reserveer`, `praktyk`), not for sentences you wrote.
3. Read every hit and ask whether it asserts the proposition. Expect at least one
   paraphrase you would not have predicted.

A paraphrase is the dangerous kind, because it reads as new information rather than
as the thing you already withdrew — "whites-only **by practice**" even looks like a
correction of "whites-only", which is why it survived two sweeps.

Related: [[n-regstelde-fout-kom-in-n-ander-gedaante-terug]] says to write down the
false CONCLUSION rather than the false words. Same lesson, one level up: when
sweeping, search for the conclusion too.

## The half-amendment: the twelfth was a field I had already fixed that day

18 September 2026, twelfth instance. A requirement's opening line ordered two things:
that he "did not give up **or become full of hate**" and that he "**learned** to
forgive". A fact check killed the second. I amended the line — and changed only that
half.

So the line went on ordering the first claim, which a decision the same day forbade,
and it now also contradicted its own closing bracket, which said the quality is
carried by a choice and by deeds rather than by an inner process. A coverage checker
caught it and correctly refused to send a correct draft back to a writer.

**The trap is that the field looks done.** It carries today's date and a dated
correction, so it reads as already swept — by me most of all, because I remember
editing it. A field I amended this morning is not a field that is correct.

**So add to the sequence:** when you amend an ordering line, **re-read the whole line
afterwards as if someone else wrote it**, and check every claim it still makes against
every ruling in force — not only the claim the finding named. A line that orders three
things needs all three checked, and the one you just fixed is the one you will skip.

The same round also found the **video seam** carrying both rejected claims in one
sentence, which is where both had come from. When a claim is wrong, ask where the
writer got it: if a video seam records it, the forbidden-claims list is the fix, not
another pass over the lesson.

## Two more shapes, from the transport sub-topics

22 September 2026. Sweeping three sub-topics turned up two variants worth naming, both
of which had survived every earlier pass.

**A field that marks something "checked and correct" stops it ever being checked.** The
air-transport spec said the whole 1783 balloon material was verified. That marker is why
nobody tested the video's claim that the three animals *landed safely* — sources do not
agree they landed unharmed. The field carrying the marker records, two lines below, its
own rule that *a note saying something was checked gets read as settled and prevents the
one step that would catch it*. It caught itself. **Never mark a block as checked; mark
the specific claims, and say what was not tested.**

**A field can order the writer to KEEP content you have just removed.** After a
comparison was deleted for serving no requirement, a fact-risk note still read "HOU die
vergelyking ... verander NET die rangskikking". That is the mechanism that reinstates
deleted content on the next pass, and it is invisible because the field looks like a
correction rather than an order. **When you delete something, sweep for fields that
require it, not just for fields that describe it.**

Also from that sweep: a fact-risk note forbidding an explanation "because no requirement
asks for it" while the requirement *did* ask for it — a live contradiction between two
standing orders. A writer cannot choose, which is why the checker escalated instead of
sending the draft back. **A contradiction between two spec fields is always a person's to
resolve; never brief a writer around it.**

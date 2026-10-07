---
name: die-korrigeerde-opdrag-bly-in-die-veld-staan
description: "Nine times in one day I wrote a correction into a note while the requirement's opening line kept ordering the old form. Amend the ordering field FIRST, then sweep every sibling, then run the checker — in that order, every time."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-10-02T13:51:52.149Z
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

## Amending the opening line is not enough, and patching past the threshold is the error

**2 October 2026 — the fourth fault in ONE field, and three of the four were my
own patches.** A requirement field reached twelve dated records and two rewrites.
Each time I amended the ordering sentence a check had named, and each time the
**rest of the same point** still prescribed the superseded regime: it announced
one deliberate omission when a ruling had made it two, and it went on telling a
writer what properties the wording must carry — two sentences after saying the
wording is decided and copied verbatim. So the point ordered "copy it exactly"
and "it must contain X" at once.

**Two things to take from it.**

1. **Amending the sentence a finding named is half the job.** Afterwards read the
   whole field from the top *as prose* and ask whether every other clause still
   assumes the world before the ruling. A clause that merely *describes* the old
   regime reads as an order when the writer meets it.
2. **Once a field is past the rewrite threshold, rebuild it — do not patch it
   again, however carefully.** I kept patching precisely *because* I had warned
   each agent that the field was dangerous to touch, which is backwards: the
   danger is the reason to rebuild, not the reason to patch. The reason to rebuild
   is that corrections accumulate until the field cannot be read as prose — a
   count that no longer counts, a clause stranded behind a full stop, a pronoun
   whose antecedent has moved. None of that is findable by assertion.

## I had the sweep's logic INVERTED, and repeated it all night

**2 October 2026.** I told agents, and Lampies, that *a field with several
corrections and no record marker is where faults hide, because the sweep skips
it.* **That is the exact opposite of the code**, verified by reading `ondersoek`
in `bin/verouderde-bestellings.py`:

* `if REKORDLYN in teks: continue` — a field **with** the marker is **skipped**.
* A field **without** one is **listed**, once it holds two or more dated records
  and the text above the first is long enough to be an order.

So a marker-less field is exactly what the sweep reports — that is the sweep
working. The marker is how a field **leaves** the "a person must read this" list
and passes to the buried-order check, which the script's own notes call the
precise one. Adding a marker is still right, because it is the house shape and it
fences orders from records — but it **reduces** that field's visibility to this
sweep rather than restoring it.

**The correct behaviour was in my own context when the session began.** I had it,
inverted it, and repeated the inversion until agents wrote it into two
specification records as settled fact. Before asserting what a tool does, read
the tool — and when a brief rests on my claim about one, say in the brief that it
is my claim.

Related: [[n-laslap-binne-n-sin-breek-die-veld-as-prosa]],
[[n-reggemaakte-veld-kan-nog-n-ander-fout-dra]],
[[n-wag-wat-sy-eie-reels-naskryf]].

## A seventh costume: a PERMISSION that undoes a prohibition in the same field

**4 October 2026.** A requirement banned any claim about where some words came
from, "in either direction" — and three clauses later permitted a name to remain
in the text. The only name available was the person who wrote those words, so
exercising the permission **is** making the banned claim. A later writer with
words to spare could do it and cite the field.

The six costumes I had been briefing all describe an **order** that has gone
stale. This one is a permission, so it reads as harmless latitude rather than as
an instruction, and a reader checking "does any order here contradict a
correction?" slides straight past it.

**How to apply:** when sweeping a field, read its **permissions** against its
prohibitions as well as its orders against its records. Ask of each "may" and
each "is not needed": what is the widest thing a writer could do under this, and
does any other sentence in the field forbid that? A permission with no stated
bound is the same fault as an order with a withdrawn premise.

## An eighth costume: a REASON-clause asserting a withdrawn fact beside a live order

**4 October 2026.** A requirement ordered that an entry must not give a service to
the state alone — sound, and still met. But the same sentence gave its reason as a
**quantity**: that a large part of the service is delivered by designated bodies. A
fact check contradicted the quantity; no national source exists for it.

**What makes this one invisible to the whole pipeline.** The seven costumes before it
are orders or permissions gone stale, so a corrected draft **fails** coverage and
something reports it. Here the order itself is sound and the corrected draft satisfies
it, so **no checker will ever raise it** — while a writer reading top-down meets the
reason as a requirement and rebuilds the false quantity, able to cite the field for it.
A stale order announces itself the next time anyone runs the pipeline; a stale reason
waits silently for the next revision.

I had told the writer both of that lesson's findings were draft-only faults. **The
writer checked my claim and found the source fault I had cleared** — one more instance
of a writer correcting my reading of a requirement in this sub-topic.

**How to apply:** when a fact check kills a claim, do not only ask which sentences
*order* it. Ask which sentences **give it as a reason, an illustration or a
justification** for something else that is still true. Those survive every sweep aimed
at orders, and they read as settled precisely because the thing they support is
correct. Sweep for the claim's substance, never for the wording you remember writing.

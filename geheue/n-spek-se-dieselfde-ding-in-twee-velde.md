---
name: n-spek-se-dieselfde-ding-in-twee-velde
description: Fixing a finding at its source in the spec means sweeping every field that repeats the claim — the core items and the focus-question field said the same thing twice.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-10-02T13:52:08.602Z
---

31 August 2026, Gr 4 SW "Vervoer op land" lesson 1. A fact check contradicted two claims
that the specification itself had planted: that an animal carried a load **further** than
a person walks in a day, and that the journey was only as fast as the animal **walks**.

I corrected both in the spec's core items and thought the source fix was done. It was not.
The lesson's **focus-question contribution field said the same two things in its own
sentence**, and I never looked at it. The writer caught it and reported it rather than
working around it — the second time a writer has pushed back and been right.

**Why it would have been expensive.** The coverage checker holds a draft to that field and
to nothing wider. An uncorrected sentence there would have marked a correct lesson as
defective, and the obvious next move — "make the lesson match the spec" — would have put
both contradicted claims straight back in. The field also reads as settled to the next
agent that opens it.

**How to apply.** When a finding is fixed at its source, **grep the whole spec entry for
the words the finding turned on**, not just the field the finding named. A spec states the
same idea in several registers on purpose — core items as requirements, the focus link as
a promise, the fact-risk list as a warning — so a claim that is wrong is usually wrong in
more than one of them. Fix them in the same breath, then refresh the extracts.

Related: [[n-regstelling-ontwrig-sy-bure]] (that one is about what a fix BREAKS; this one is
about what it MISSES), [[spesifikasies-word-nooit-nagegaan]],
[[moenie-in-die-spek-skryf-wat-jy-nie-nagegaan-het-nie]]

## It happened again on 2 September 2026, twice in one session

Both times I fixed the field the finding named and missed the others.

* **MIV is a virus.** I amended six per-lesson fields and missed a *sub-topic-level*
  word-choice rule that banned the word `virus` outright. My sweep only walked
  the lesson entries. The writer found it.
* **Conflict is between two or more people.** I fixed the `kern` item; the
  wording survived in the sub-topic's `regverdiging` and `fokusvraag_skakel`.
  The coverage checker found it and said plainly it could be planted back by a
  later revision.

**How to apply, concretely:** do not sweep by reading the lesson entry. Walk the
**whole spec file** — every nested string, sub-topic fields included — with a
regex for the wrong phrase, and confirm the count reaches zero before moving on.
Where a correction note quotes the old wording to explain the change, that one
match is expected and is the only one allowed to remain.

## I did this myself, hours after quoting the rule to an agent

**2 October 2026.** A specification-level field claimed, in the present tense,
that the subject's agreed-wordings list was deliberately empty. That claim had
been withdrawn **by name** the previous day — but it stood in **two** fields. The
withdrawal swept one and left the twin, which still asserts it and has **no
record marker**, so its stale half is indistinguishable from a live order. I had
read the repair as complete.

What makes the twin dangerous: with no marker there is nothing separating its
stale half from a live order, so a writer reading top-down cannot tell which
half binds.

**I first wrote here that a marker-less field is skipped by the sweep. That was
wrong, and the inverse of the code** — `ondersoek` **skips** a field that *has*
the marker, and **lists** one that lacks it once it holds two or more dated
records. So this twin was in fact exactly the sort of field the sweep does
report; what it lacked was a reader. See
[[die-korrigeerde-opdrag-bly-in-die-veld-staan]] for the verified behaviour and
how far that inversion travelled.

**How to apply:** when a claim is withdrawn, grep the claim's *substance* across
the whole specification **before** calling the repair done. Sweep subject-level
fields first — they are injected into every lesson, so a survivor there reaches
all of them. See [[vee-die-bewering-oor-al-die-spesifikasies]]. A field needing a
fix and holding several corrections should be **rebuilt** rather than patched —
not because the sweep cannot see it, but because corrections accumulate until the
field no longer reads as prose.
## 5 October 2026: three times in one session, and the rule was already written twice

Grade 7 LO. Three source corrections, three siblings left ordering the withdrawn wording,
and **a checker found every one of them — never me.** The rule above was already in this
note and in [[vee-die-bewering-oor-al-die-spesifikasies]], so what is missing is not the
rule. It is a routine that fires without my remembering to run it.

- **Werk 6's frame.** I replaced the measure in one `kern` item. Five other places still
  ordered the old pole; after sweeping those, a second checker found two more.
- **Self 8's healthcare exception.** I corrected the exception's own item and left the
  `kern` item that orders the clinic route, plus the ceiling-exception field listing the
  revoked test as one of three live tests *under an instruction not to cut those words*.
- **Self 8's ceiling field** also still measured a block at 254 words that had since been
  split into three measuring 96, 104 and 98.

**The routine.** After every source edit, before committing: strip brackets from every
string in the lesson entry — `kern`, `feiterisiko`, `plafon_uitsondering`, the focus link,
and the sub-topic-level fields — and grep the **live** text for the old wording. Assert the
count is zero. Put that sweep in the same script as the edit, so it cannot be skipped.

**Where the misses cluster, so look there first:**

1. **Undated fields.** They lose only by the precedence rule, never by being marked, so
   they read as live. Both Self 8 misses and the Werk 6 count were undated.
2. **The ceiling-exception field**, because it enumerates the corrections as a protected
   list — so a withdrawn item sits there under "do not cut this".
3. **A later correction's own "this wins over" clause**, which names the fields it was
   written about. It does not reach a sibling it never mentioned, and I read it as if it did.
4. **Measurements**, which age the moment the text moves: see
   [[n-beskrywing-verouder-n-vereiste-nie]].

What must stay out of the sweep is the normal correction shape — a field diagnosing an old
form with the live order right after it. A sweep that fires on those gets ignored, which is
[[n-generiese-teruggetrek-speurder-kan-nie-werk-nie]].

## Two more ways the sweep goes blind, 5 October 2026

**The spec uses two bracket styles for records, and my sweep only strips one.** Square
brackets `[…]` and round parentheses `(REGGEMAAK 28 September 2026: …)` are both used for
withdrawal records in these specs. A reader that strips only square brackets both **misses**
live orders hiding in parentheses and **fires** on parenthesised history. Strip square
brackets, then also strip parentheses that open with a dated record word — REGGEMAAK,
TERUGGETREK, VERNOU, VERBREED, BYGEWERK, HERSKRYF — and leave ordinary parentheses alone.

**Appending a new requirement is not the same as replacing a sentence, and I kept treating
it as if it were.** Four times in one session I added an item stating the corrected form and
swept only for the phrases I had explicitly replaced — so the *old form of the thing I had
just newly required* stayed live somewhere else. When the fix is an addition, sweep for the
old form by name anyway.

**Look at the FIRST kern item first.** It is the original planning requirement, so it is the
oldest text in the field and the most likely to have been overtaken after many rounds — and
in these specs it often carries a marker claiming it wins over every other sentence in its
field, which makes it the worst place for a stale order to sit. In Gr 7 LO's religions
lesson the first item was still ordering, in the imperative, the exact sentence that had
been deleted hours earlier.

**And sweep for the ORDER FORM, not the phrase.** A past-tense record legitimately repeats
the wording it replaced ("the block *had to* say…"), so searching for the phrase fires on the
correction itself. Search for the imperative.

## 13 October 2026: WHY the siblings survive — no check can compare across fields

Twice in one day, in two different specs, a coverage check found my fix one field wide
when the fault was a class. Lampies decided the Grade 6 wording of `kieme`; I withdrew
the "deliver a new sentence" order from the core item, and **three** other fields still
carried it — the expected-concepts note, the budget note and the subject's
shared-definitions note. Separately, I withdrew "only the king's people had gold" from a
core item and the focus-question field still had it, in a *stronger* form.

**The mechanism, which is worth more than the two instances.** Every order/record test we
own compares an instruction against the record standing **at its own path**. A decision
recorded at one field withdraws the order at that field. An identical order at a sibling
field has no record of its own, so:

* the order/record comparison sees a field with an order and no withdrawal — normal;
* the stale-order sweep looks for fields with *several* dated records — a clean sibling has none;
* the buried-order check looks only below a canonical line — the sibling has no line.

So a sibling is invisible to all three, by construction, and it will stay invisible. One
coverage checker put it exactly right: those fields "are withdrawn only by a record at a
*different* path plus one general rule, which is why they survived the sweep."

**How to apply.** A finding names a field; treat it as naming a CLASS. When a ruling changes
the status of a term or a claim, sweep every field of that lesson entry AND the spec-level
fields for the order form, then assert zero hits before calling it done — I now do this in
the same script that makes the fix, and it is what caught that nothing remained. A general
"the injected list wins" paragraph is not a substitute: two of the three fields above sat
outside its reach, and a reviser reads top-down from the field in front of them.

Related: [[vee-die-bewering-oor-al-die-spesifikasies]],
[[die-korrigeerde-opdrag-bly-in-die-veld-staan]],
[[my-regstelling-in-die-spek-was-self-die-volgende-fout]],
[[n-gesplete-bestelling-twee-lewende-gronde]].

### The eighth instance named the mechanism: a record half describes the order it was written beside

Later on 13 October 2026, same lesson. I moved a core item's middle support from possession
to find-place and added the superseding paragraph to **that field's** record. Its sibling
field's record still ended on *"and what is now ordered: the gold was concentrated with the
king's people"* — the old frame, in the present tense, labelled as the live order.

Formally it binds nothing: the canonical line is there and so is "DIE OPDRAG STAAN HIERBO".
**It was read as live anyway.** The draft's own provenance note reported that field as still
carrying the old frame and asked a person to fix it at source — true of the record half,
false of the order half. So "a record is read as an order" stopped being a prediction and
became a measured event, in the same day it was written.

**The mechanism, and it is narrower than "sweep the siblings".** When I change an order, the
record beside it is the thing most likely to describe the order I have just replaced,
because I wrote them in the same breath. So:

* **After changing any order, read that field's own record half** and ask whether it still
  speaks in the present tense about what is ordered. A record speaks only in the past.
* **A record must never contain the phrase "what is now ordered"** or any equivalent. If it
  needs to say what the current order is, it is in the wrong half.
* **If a correction supersedes an earlier record, say so inside that record**, with the date.
  Two records in one field, one superseding the other, is normal and safe; a record that
  simply contradicts the order above it is not.

A related trap from the same pass: I had put a word-cost figure into an order ("this costs
about seventeen words more than the ceiling leaves"). A writer correctly filed the material
as *content that did not fit* rather than as evidence — so a later round with spare words
would read it as licence. **A cost is never a reason in a requirement.** State what the thing
is (evidence for a person, not content for the learner); whether it fits is the gate's
business and ages on its own ([[die-band-is-nie-die-plafon-nie]],
[[n-nota-wat-n-toestand-vasvries-verouder]]).

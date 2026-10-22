---
name: n-wag-wat-sy-eie-reels-naskryf
description: "A check that keeps its own copy of the rules of the thing it checks drifts from it silently. Compare against the producing function, not against a second list."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-10-01T07:11:13.801Z
---

1 October 2026. The guard that tells me whether a fact checker's copy is level
with its draft kept **its own list** of the fields the copier withholds. The
list held one of the two. So:

* every signed-off lesson reported its copy stale on **every** run, and the
  rewrite was byte-for-byte identical — the check's own comment says it exists
  to prevent exactly that ("would report every copy stale on every run and train
  everyone to ignore it");
* and it was **blind** to 30 copies that really were out of date, because it
  threw away the one field it did know about before comparing.

Both failures from one duplicated rule. The over-report is the one you notice
and learn to discount; the under-report is the one that matters, and it rode in
behind it.

**Why:** the number printed by that guard is the only thing that makes the fact
checks after it mean anything — "0 behind the draft" is the answer worth having.
A guard that cries wolf on the same three files for weeks gets read as noise,
and then its silence gets read as noise too.

**How to apply.** When a check asks "does this derived file still match its
source", call the function that derives it and compare the result. Never
restate its rules in the checker. I factored the copier's transform into a pure
function and had the guard call it; now a new withheld field cannot drift the
two apart, because there is only one definition.

Same family, different shape: the stale-order sweep tries to recognise an order
by a list of imperative verbs, so an order phrased as a statement is invisible
to it — and that limit is written into the script, because extending the verb
list fired on its own records. Where a check cannot call the real rule, say in
its output what it cannot see.

## And one thing no pattern can do in this repository

1 October 2026, my second attempt at mechanising that same decision. Instead of
recognising orders, look for a signature: a record says a form was withdrawn and
**quotes** it, so if a long piece of that quotation still appears in the field's
ordering half, the order is probably still giving it. Meaning-free, and it would
have caught the statement-shaped ones.

It found **zero of sixteen** known cases — and I only knew that because I ran it
against a commit that definitely carried them before believing it. One reason was
tunable (records announce a withdrawal in many more ways than a verb list holds,
sometimes with no verb at all, just a cross-reference to the new prohibition).
The other is not: **Afrikaans writes its indefinite article with an apostrophe.**
Nearly every sentence in these fields contains `'n`, so a single-quote regex
cannot delimit a quotation in this repository's prose — it truncates at the first
article inside the quoted run. There is no quoting convention here to stand on.

**How to apply:** two failed attempts at the same thing is the signal to stop.
The reliable detector for a withdrawn order left standing is an agent reading the
field from the top, which found all sixteen. The script's job is to say *where*
to look. And before trusting any new text-pattern check in this repo, test the
delimiter against a sentence containing `'n` — see
[[my-soektogte-mis-en-dan-glo-ek-hulle]].

See
[[n-skrip-wat-parse-is-nie-n-skrip-wat-werk-nie]],
[[n-ruil-wat-nie-pas-nie-moet-hard-faal]],
[[die-feitenasiener-lees-n-verouderde-konsep]].

## An exemption for a special case becomes an exemption from being checked

1 October 2026, and this is the worst one so far, because the check kept printing a
line that read as reassurance.

The glossary-drift sweep legitimately exempts a term that carries **two** agreed
meanings, so it does not complain that two lessons use different senses. Fine. But
a two-meaning entry keeps its wordings in a different field from every other
entry — and the script never read that field. So three independent paths all
dropped the term:

- the drift loop skipped it, by design;
- the comparison against the decided wording skipped it, because the field it
  reads is `null` on a two-meaning entry;
- and the report that catches an entry with no wording **excluded it by name**.

The term was compared against nothing at all. The only trace was a summary line
saying it was not counted as drift — true, and it reads as *checked, and fine*. I
quoted that line repeatedly as evidence the subject was consistent.

What was actually sitting there was the **withdrawn wording, character for
character** — the exact form thrown out that morning under a ruling of Lampies'.
A gated lesson carried it, and the sweep would have exited clean but for an
unrelated drift that happened to be live. A writer found it by reading one entry.

**How to apply.** When a check exempts something, ask what else the exemption
takes with it — an exemption written for one report can remove the thing from
every report. And look at the output line: *"not counted as drift"* is a true
sentence that answers a different question from the one I was asking it. A check
that says what it did NOT do is worth more than one that only lists what it found.
Two of my three sweeps turned out this day to be blind exactly where I was reading
them as clean — this one, and the stale-order sweep, which skips any field
containing a record separator, so the fields I had just reorganised into that shape
became invisible to it.

Related: [[n-skoon-toets-is-so-wyd-soos-sy-omvang]], [[my-soektogte-mis-en-dan-glo-ek-hulle]],
[[die-ooreengekome-bewoording-kan-self-verkeerd-wees]].

## The claim sweep read 0 of 435 extracts, and said so in a way that read as "none"

**8 October 2026.** The sweep that answers "is this withdrawn claim still alive anywhere"
reads two things: the approved specifications, and the spec EXTRACTS — the copies a
writer actually reads. Its extract pattern was one directory level too shallow, so it
matched **0 of 435** extracts on every run it had ever done.

What made it invisible was the output: *"91 specifications and 0 extracts read"*. That
reads as "there were no extracts", not as "I cannot see any of them". I had quoted this
sweep's reassurance earlier in the same week.

Fixed, it finds the claim in the approved specification AND in the extract beside it —
which is the pair that matters, because the extract is what gets handed out, and an
extract still carrying a withdrawn order is the thing that makes the fault come back.

**How to apply.**

* **Print the denominator.** Every count a guard reports should be "N of M", where M is
  what exists in scope. "0" is ambiguous; "0 of 435" cannot be misread. That one change
  would have exposed this on its first run.
* **Before trusting a sweep, make it find something I planted.** I confirmed the repair
  by sweeping a claim I already knew was live in one field. A sweep that returns nothing
  is only evidence if I have seen it return something.

## Where the shared marker vocabulary stands, and why the rest is parked

Two of the four sweeps now read the shared record-marker vocabulary; **two still keep
their own** (the claim sweep and the pointer sweep), and their private lists hold words
the shared one does not. I deliberately did NOT merge them, and the reason is worth
keeping: **a wider marker list makes MORE hits classify as "inside a dated record" and
therefore dead.** That is the direction that hides a live order, and when it was tried
on one of these checks the live list went to zero. Any merge has to be done with
before/after counts on each consumer, never as a tidy-up.

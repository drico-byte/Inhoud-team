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

## Ten more in one day, and two of them were mine to begin with

28 September 2026, Grade 7 LO. Ten instances across four sub-topics in a single day.
Eight were the familiar shape and two were not.

**The first new one: I amended the record and left the order.** I had written the
withdrawal of a comparison into the bottom of a requirement as a dated ruling — and left
the field's **opening line** saying "dit is die swaar deel", which is the same comparison
compressed. So I performed the exact inversion this note prescribes against: bottom
first, top never. A writer caught it, declined to write the sentence, and told me the
opening line is what a coverage check reads.

**The tell for this variant is the feeling of having just done it.** I edited that field
an hour earlier and remembered editing it, which is precisely what stopped me re-reading
it. Same trap as the half-amendment above, one turn tighter: it is not enough to re-read
the line you amended — you have to re-read it *from the top*, because the correction you
wrote is at the bottom and your eye starts where you were working.

**The second new one: a stale order hid in a reading note, not in a requirement.** The
sweep had cleared every `kern` item and every fact-risk field, and the retracted wording
was alive in a `kaps_leesnota` — a field whose name says *note*, which is exactly why it
was not swept. It ordered the writer, in the imperative, to say the thing that had just
been withdrawn, and two sentences above it the same field forbade the equivalence it was
ordering. A writer caught that one too.

**So step 3's sweep covers every field a writer reads, not every field named "order".**
`kaps_leesnota`, `termdig_nota`, `begrotingsnota`, `verdeling_nota` — a note a writer
reads is an order whatever it is called, and the ones with "nota" in the name are the
ones a grep of the requirements misses.

**And the overall tell holds, nine months on: a writer caught both.** When a *writer*
catches your bookkeeping, the bookkeeping is the problem — twice in one day, on fields I
had personally edited that same day.

---

**29 September 2026, and the sequence above is still not enough.** Six checkers in one
round, on six different lessons, escalated the spec rather than the draft — and every one
was me doing step 2 and skipping step 3.

**The shape has narrowed to one thing: I PREPEND.** I write the correction as a new
opening line, the field now reads correctly from the top, and the old instruction stands
untouched two paragraphs down in the *same field*. Step 2 feels like it discharges step 3,
because the field "has" the correction.

It does not. A writer or a reviser reads the field as prose. The worst instance: a Werk 1
requirement closed with **"What remains and is true: a story has no headings or bold, so
there is nothing to look over"** — labelled as what survives, sitting directly below its
own refutation in the same field. A Werk 9 field forbade, in capitals at its tail, the
quantifier its own opening line required.

**So the rule is stronger than "amend the opening line":**

> **Rewrite the sentence that ORDERS the thing. Not a line above it — the sentence
> itself.** An opening line that says "this wins over the rest of this field" is a note
> about the field, not a change to it.

Two corollaries that cost me rounds today:

- **Assert against the live text, not the field.** A withdrawal record quotes the wording
  it replaces, so `old not in field` fails on the record's own quotation. Assert that every
  occurrence sits *after* the dated withdrawal marker, or strip the record before testing.
  This fired twice in one day.
- **A field with three layers of patches is due a rewrite, and the rewrite is cheaper than
  the next round.** Werk 2's memory-aid requirement reached 5.6 KB and ended up ordering
  two aids in one paragraph and three in the next. A writer, a checker and I each read it
  and only the checker caught it.

Related: [[n-laslap-binne-n-sin-breek-die-veld-as-prosa]], [[n-ruil-wat-nie-pas-nie-moet-hard-faal]],
[[my-regstelling-in-die-spek-was-self-die-volgende-fout]].

## The marker I invented to fix this is itself read as commentary

Later the same day, 29 September 2026. Three checkers on three lessons — Self 8, Werk 4,
Werk 5 — plus a second report on Regte 10, all named the same defect, and it is the
mirror image of the prepend above: **I APPEND.**

My standard device had become a bracket placed *after* the ordering sentence:

> `<the old ordering sentence>. [TERUGGETREK <date>: <why>. WAT GELD: <the correct form>.
> NIKS IN HIERDIE VORM BESTEL NOG IETS.]`

That bracket is careful, dated, and says in capitals that it orders nothing. **It does not
work.** A writer reads the field as prose, meets the order first, and the bracket arrives
as a gloss on an instruction already received. Coverage then reports — correctly — that
the field still orders the withdrawn thing. One checker quoted this repository's own
precedence rule back at me by name to say so, twice on the same field.

**So the device is retired.** The correct move is the one this note already prescribes and
which the marker let me avoid: **replace the ordering sentence's own words**, and let the
dated explanation follow *inside* the rewritten sentence's parenthesis. The distinction is
not cosmetic — a marker leaves the false sentence grammatically intact and available to be
copied; a rewrite removes it.

**Why the marker felt sufficient, which is the part worth remembering:** it is auditable.
It preserves what was wrong and why, which is genuinely valuable, and that value disguised
the fact that it changes nothing a writer acts on. **A record and an order are different
objects, and putting a record next to an order does not demote the order.**

**And the third layer breaks the field outright.** On Regte 10 I finally rewrote in place —
and replaced *every* occurrence of the old phrase, including the one inside the correction's
own contrast ("X, not X-in-general"). The result said "a provincial department of social
development, not a provincial department of social development in general", with the dated
note nested inside itself three times, and a sibling field presenting the *correct* wording
as the error it was confessing. Both items had to be rewritten as whole prose.

**Operationally:** replace whole sentences, never substrings that also appear in a
quotation; assert the replacement count is exactly one; and when a field has three patch
layers, rewrite it and reduce the sibling that duplicated it to a record that says it
orders nothing. See [[n-laslap-binne-n-sin-breek-die-veld-as-prosa]], which predicted this
exactly and which I read after doing it.

## A "what now applies" clause is an order, and it ages like one

29 September 2026, still the same day. The retraction device I retired above had a second
half I had thought was safe: the clause inside the bracket that says **WAT GELD** — what
applies now. It reads like part of the record, so I never swept it.

It is not part of the record. It is the live requirement, in the only place a reviser will
look, and it goes stale exactly like any other order. A fact check narrowed a claim about
school programmes twice: first from "reduces use" to "belongs with the chance-reducers", and
later — from a Cochrane review of 51 studies — to "only when it also teaches the broader life
skills, and the difference is small". The first narrowing lived in three WAT GELD clauses I
had written. The second never reached them, so three of my own markers went on ordering a
form a later check had overtaken. A writer found all three and told me.

**So the sweep has to include the insides of markers.** When a claim is narrowed, grep for
the claim across the whole spec *including* every bracket, note and record, and ask of each
hit: is this describing what was wrong, or stating what is required? The second kind is an
order wherever it sits.

**And the corollary for writing them:** a WAT GELD clause should carry the claim's date, so
that a later reader can see whether it predates the newest finding. A clause without a date
loses under this repository's own precedence rule, and mine had none.

Same day, same field family: a marker can also withdraw **too much**. One of mine ended "and
not its opening line either", where the retraction covered a single wording and the opening
line carried a live coverage order — so a next revision could have deleted a required
distinction and cited the spec for it. See [[die-merker-begrawe-die-bestelling]]. Scope the
marker to the wording it retracts, never to the field.

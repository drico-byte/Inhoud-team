---
name: vee-die-bewering-oor-al-die-spesifikasies
description: "A claim refuted in one sub-topic lives on in another that nothing connects to it; sweep every spec for the claim, not just the spec the finding named."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-09-29T08:46:47.662Z
---

11 September 2026. Three times in one day a correction went into `kern` and not
into the sibling fields repeating it, and twice a **coverage check** had to find
it. So I swept all ten Grade 5 specs for every claim corrected that day.

**Five live survivals, and the one that mattered was in a different sub-topic.**
"Those properties *determine* what people use it for" was refuted by a fact check
on the metals lesson — and was sitting, live, in `verwerkte-materiale` lesson 2,
which nothing connects to metals. No per-lesson check can see that; drift only
exists between files.

**The other four are each a distinct trap:**
* my own correction's tail still ordered the false wording, *below its own*
  "everything below still applies";
* the rejected Grade 4 sentence sat alone in a `bewoording` field with only its
  sibling `status` saying not to use it;
* two hits were **verbatim CAPS quotation fields**, which carry the error
  themselves and are never edited — say so in the core item instead, or a writer
  reads the CAPS phrase as an order.

**How to apply.** After correcting a claim at source, grep every spec in the
grade for the *false wording*, reading only text above a record marker, and
discount corrections that quote it in order to reject it. Write down the false
CONCLUSION, not the words, so the sweep catches it in a new costume.

**And batch spec edits before checks.** Renaming a record marker — purely
cosmetic — changed the spec hash and cost a finished coverage check a full re-run.

**A SPEC-LEVEL field costs every lesson in the sub-topic, not one.** 29 September
2026: I added one precedence rule at spec level in four Grade 7 LO specs and
archived every in-place report across all four sub-topics in one command. A
lesson-level edit costs that lesson's two reports; a spec-level edit costs all of
them. Signed-off lessons are safe. So a spec-level field goes in **before** a
check wave or at the end of one, never in the middle — and if it must go in
mid-wave, say plainly what it cost rather than discovering the loss later.

Related: [[n-spek-se-dieselfde-ding-in-twee-velde]],
[[n-regstelde-fout-kom-in-n-ander-gedaante-terug]],
[[n-bevinding-by-die-bron-opteken-is-nie-dit-regmaak-nie]],
[[die-merker-begrawe-die-bestelling]], [[wanneer-kaps-self-verkeerd-is]].

---

**29 September 2026: the mechanism, confirmed by reading the runner rather than guessing.**

The rule of thumb above — that a spec edit costs a finished coverage check a re-run — is
real, and now it has a name. The runner writes a **`spek_hash`** into each lesson's state
file alongside the draft's own hash, and on its next call it compares that fingerprint
against the current spec entry. If they differ and a coverage report exists, the report is
treated as belonging to an older spec and archived.

Two things follow that the rule of thumb did not make obvious:

* **It is the SPEC ENTRY that is fingerprinted, not the whole file.** So editing one
  lesson's entry costs that lesson's coverage check and leaves its siblings alone.
* **The fact report is not keyed to the spec**, which makes sense — the fact checker never
  sees a spec. So a spec-only edit costs the coverage check and not the fact check.

**How to apply.** Before editing a spec entry whose coverage has already passed, decide
whether the edit is worth one coverage run. It usually is when the edit changes what is
*required*, and usually is not when it only changes wording — but batch the cosmetic ones
and let them ride along with the next substantive edit, which costs nothing extra.

And when a spec edit is genuinely worth it, **re-run coverage yourself straight away**
rather than leaving it for the runner to discover. The runner archives the stale report on
its next call, and if that call is a sign-off it demands the whole check again at exactly
the wrong moment — which is the failure
[[moenie-die-hardloper-vra-oor-n-nagesiende-les-nie]] records.

---

**30 September 2026, Gr 6 SW Democracy: the claim was alive in FIVE fields, and the last
one was another lesson's WORKED EXAMPLE.**

Lesson 4's title *Jou regte werk NET AS almal hulle deel doen* was withdrawn as false. Over
the day the same claim turned up, one field at a time, in:

1. the title (found by a fact check),
2. a study sentence in the same lesson (same check),
3. the lesson's **budget note**, stating the lesson's single idea as "elke reg het 'n
   verantwoordelikheid langs hom" — in an ordering clause, not a record,
4. the **focus-question link**, giving the rule with no quantifier at all,
5. **lesson 6's requirement for children's responsibilities**, whose two worked examples
   read "'n kind se reg om te leer werk net as ander kinders die klas nie opbreek nie".

Each time I fixed it I believed I had swept. Three of the five were found by checkers, not
by me.

**Why number five is the worst place for it.** A requirement's worked example exists to be
copied — it is the one kind of spec text a writer reproduces in shape and often in wording.
And nothing in the pipeline can see it: the fact checker never gets a specification, and
coverage tests whether the draft *matches* the requirement, never whether the requirement
is *true*. A false form sitting in an example in a different lesson from the one where it
died will be reproduced faithfully and reported as covered.

**How to apply.**

* When a claim is withdrawn, sweep **every lesson of the sub-topic**, not the lesson it was
  found in — and inside each lesson, sweep the fields that are not requirements:
  budget notes, merge rationales, focus links, scope lists, and above all **examples**.
* Sweep on the claim's shape, not its words: "werk net as", "werk die beste as", "elke X
  het 'n Y", "geld net wanneer". A quantifier and a conditional are the same claim.
* A field that *demonstrates* rather than *orders* is the highest-value target, because it
  is designed to propagate.

Related: [[n-spek-se-dieselfde-ding-in-twee-velde]],
[[n-regstelde-fout-kom-in-n-ander-gedaante-terug]],
[[die-verwysingsles-word-nooit-nagegaan]] (the same hazard in the shared reference lesson),
[[spesifikasies-word-nooit-nagegaan]].

## Sweep the SUBJECT-LEVEL fields first, and word a ban to cover parts

**1 October 2026, two instances in one evening, both found by agents after I had
named only the lesson's own fields in the brief.**

**The highest-leverage hiding place is a subject-level field**, because those are
injected into every lesson's extract. A withdrawn permission about a date was
alive in a lesson's requirement, in a neighbouring fact-risk item, **and in the
subject-level pre-write fact list** — so it was reaching all eight lessons at
once. I had named the first two. So: when a claim is withdrawn, sweep the
subject-level fields **before** the lesson's own, and say so in the brief.

**The mirror of the same point.** A prohibition written in one lesson binds one
lesson. Where a second lesson teaches the same thing, the two can produce a false
pair that nothing per-lesson can see — the gate reads one lesson and coverage
reads one lesson against one entry. The fix is to promote the prohibition to
subject level and **keep** the lesson-level one, following the precedent already
in that field.

**And a ban on a quantity must cover parts of the quantity.** The membership ban
said "no count of the people a province sends". Another lesson carried "its four
special delegates are the Premier and three members" — a *part* of the ten, which
the ban did not obviously reach. Word it to cover the total, the per-unit figure
**and any part of it**, by name. This is the quantifier version of
[[n-regstelde-fout-kom-in-n-ander-gedaante-terug]].
**Addendum, 5 October 2026: I wrote the fix and swept nothing, the same day. And the
checker's list of survivors was half the real number.**

Gr 4 Geography, map skills lesson 7. A fact check found the glossary entry for `hoofstad`
too narrow — read alone it excluded three cities the lesson's own list names. I widened it
in the requirement field and stopped there. A coverage check then named **two** other
fields still asserting the narrow form. Sweeping for the *claim* across the whole entry,
rather than working the two it named, found **four**.

So the checker's list is a floor, never the set. It reports what it tripped over while
doing a different job.

**Three shapes the survivors took, and only the first is the one this note already knew:**

1. A plain repetition — a passing gloss in a note field, narrow form, ordering nothing.
2. **A withdrawn ruling still standing in the present tense.** The entry recorded the
   narrow definition as correct Grade 4 scope, "not an error", with the widening reserved
   for a *later grade*. Every word of that was a decision, and the decision had just been
   reversed *inside* Grade 4. Annotating it was not enough; it had to be marked withdrawn.
   Same failure as [[n-teruggetrekte-beslissing-bly-in-hoofletters-staan]].
3. **A field whose ORDER was right and whose REASONING had just been falsified.** The
   Pretoria guard said the key sentence alone was enough, because a map marking provincial
   capitals marks Johannesburg and not Pretoria. The same fact check that triggered the
   widening also established that a map of South Africa normally carries **two** capital
   entries in its key. So the order ("do not add a sentence explaining this") was still
   correct while the mechanism under it was false.

The third is the one worth carrying. **A sweep that only looks for the old wording walks
straight past it** — the field never mentions the glossary entry at all. It turned up
because I was reading every field that touched the subject, not matching a string. And
[[spesifikasies-word-nooit-nagegaan]]: nothing downstream would ever have caught it, so it
would have been the premise of the next revision.

**How to apply.** When a fact check changes a claim, re-read every field in the entry that
touches the *subject*, and ask of each one separately: does it repeat the old claim, does
it record a ruling that has now been reversed, and does its reasoning still hold given what
the check established? Three questions, not one. Assert in the fix script that no live
field still carries any of them.

Related: [[n-spek-se-dieselfde-ding-in-twee-velde]],
[[n-reggemaakte-veld-kan-nog-n-ander-fout-dra]], [[die-korrigeerde-opdrag-bly-in-die-veld-staan]].

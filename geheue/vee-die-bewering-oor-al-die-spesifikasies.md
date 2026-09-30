---
name: vee-die-bewering-oor-al-die-spesifikasies
description: "A claim refuted in one sub-topic lives on in another that nothing connects to it; sweep every spec for the claim, not just the spec the finding named."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-09-11T09:22:00.519Z
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

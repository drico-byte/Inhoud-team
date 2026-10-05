---
name: n-spek-se-dieselfde-ding-in-twee-velde
description: "Fixing a finding at its source in the spec means sweeping every field that repeats the claim — the core items and the focus-question field said the same thing twice."
metadata:
  type: feedback
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

---
name: n-feiterisiko-is-nie-n-regstelling-nie
description: "Adding a fact-risk note without amending the core point it contradicts is a half-fix: coverage tests against kern, so the spec keeps ordering the error and a correct draft fails."
metadata:
  type: feedback
---

8 September 2026, Gr 4 SW Kwartaal 4. Fact checks found roughly fifty errors across
eleven lessons. I fixed each one at source, as the standing rule says — and I fixed
almost all of them **in the wrong field**.

For each finding I appended a `feiterisiko` entry explaining what was wrong, with the
sources. What I did not do was amend the `kern` item that had ordered the error in the
first place. Six of the eleven coverage re-checks came back `MENS_NODIG` for exactly
this reason, each one saying some version of: *the draft is right and the spec still
commands the error; send this to a writer and the correction is undone.*

**Why the half-fix is worse than it looks.**

* **Coverage tests against `kern`.** A `feiterisiko` note is not a requirement. So a
  correct draft that departed from `kern` reads as *defective* to the checker, and the
  obvious repair — make the lesson match its spec — reinstates the false claim.
* **`kern` wins when the two disagree.** That is already recorded in
  [[kern-en-feiterisiko-weerspreek-mekaar]]. I wrote the note that says so and then
  spent a day creating the exact contradiction it warns about.
* **The note reads as the correction being done.** Dated, sourced, emphatic — it looks
  like a completed repair, so nothing prompts a second pass.

**What it cost.** Six coverage runs on six lessons, all of which had to escalate rather
than clear, plus a sweep afterwards that touched seventeen fields across three lessons.
Every one of those runs could have cleared first time.

**How to apply.** When a fact check finds an error, ask *which field ordered it* before
writing anything. Then:

1. **Amend the ordering field in place** — `kern`, `aanvulling.item`,
   `fokusvraag_skakel`, `historiese_konsepte` — with a dated reason attached.
2. **Add the `feiterisiko` note as well**, because it carries the sources and the
   reasoning that a corrected requirement cannot.
3. **Never do only step 2.** If you find yourself appending a note and leaving the
   requirement alone, you have not fixed anything.

The tell that you are about to make this mistake: you are writing "MOENIE X SKRYF NIE"
while some other field in the same lesson still says "skryf X".

Related: [[kern-en-feiterisiko-weerspreek-mekaar]] (the same collision, seen from the
writer's side), [[n-spek-se-dieselfde-ding-in-twee-velde]] (sweep every field, not the
one the finding named), [[spesifikasies-word-nooit-nagegaan]].

---

## The correction has to go in the OPENING line, not the end

Same day, later. Two writers, independently, caught a sharper version of this.

The closing lesson of the year had a requirement that began *"from a San rock
painting to a message on a screen the purpose stays the same"*. That binding — the
San as the first point of a row that ends at a phone — had already been ruled
wrong and corrected. The correction was appended **below** the original wording,
several lines down, with its date and its reasoning.

A writer read the opening line and put the binding straight back.

That is not the writer's fault and it is not fixable by writing a better note. A
requirement field is read as an instruction, and **the instruction is its first
line**. Everything after it reads as commentary — which is exactly what a dated,
sourced correction looks like. The longer the field, the more reliably the tail
gets skimmed, and these fields are long precisely because they have been corrected
before.

**So amending in place means amending the opening.** Replace the words that give
the order. Then put the reasoning, the sources and the date below, where they
belong and where they are read by whoever is deciding rather than whoever is
executing. A field whose first line says X and whose fourth paragraph says "not X"
is a field that says X.

The same day this note was written, a digital-camera requirement failed the same
way: an earlier sweep had corrected one word in it and left both of its actual
errors in the opening sentence, and the writer refused to send the lesson onward
until the requirement was fixed. That writer was right to refuse.

**The tell:** you are appending a dated correction to a field you are not otherwise
editing. If the field's first sentence still gives the old order, you have written
a comment, not a correction.

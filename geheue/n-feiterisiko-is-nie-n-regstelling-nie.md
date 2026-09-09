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

## The reasoning below a requirement can itself read as a live order

Same day, again. Having moved the prohibition into the closing requirement's opening
line, I left its history below — and a coverage checker found that the history contained
a sentence in the **imperative**: *write that the San long ago made paintings on rock
that still speak to us.* That was the wording which had replaced an earlier error, and it
had since been superseded twice. The field now held two orders for the same sentence that
could not both be obeyed.

Everything else retrospective in that field was clearly marked as past, or quoted as the
old guidance. This one clause was not, so it read as current.

**So the rule has a second half.** Putting the correction in the opening line is
necessary but not sufficient: **the reasoning you leave below it must not be phrased as
an instruction.** Record what changed in the past tense, or bracket the old order
explicitly as replaced. A dated note that says "write X" is still a note that says
write X.

The tell: any imperative verb in the part of the field that is meant to be history.

## I have now made this mistake four times in one day, after writing this note

Recorded plainly because the pattern matters more than the instances. This note was
written in the morning of 8 September 2026. By that evening I had repeated the same
half-fix on the pigeon requirement, the digital-camera requirement, the San tense
requirements and the television balance requirement. Each time a writer or a
coverage checker caught it, not me.

**The mechanism is the script, not the intention.** Every one of those fixes was
made by a small Python script that appended a `feiterisiko` entry. Appending to a
list is one line; finding and amending the requirement that ordered the error means
reading the `kern` list, identifying the right item, and asserting a substring. So
the cheap action and the correct action are different actions, and under time
pressure the cheap one wins — reliably, even with the rule written down.

**So the fix is procedural, not a matter of remembering.** In the same script that
appends a `feiterisiko`, **print the lesson's `kern` items**. Not to satisfy a rule
— to make it impossible to finish the script without having looked at the field
that gives the order. A rule I have broken four times in a day is not a rule I can
rely on holding the fifth time; a script that shows me the requirement is.

The corollary, learned the same day: when the requirement *is* amended, the
amendment goes in its **opening line** (see above), and the reasoning left below it
must not be phrased as an instruction (see above). All three failures are the same
failure seen from different angles — the field that gives the order is the field
that must change.

## Eight times in two days, and three of them I built by appending

9 September 2026. The count is worth writing down because it is the strongest
evidence in this repository for one rule.

Requirements that ordered an error their own note forbade: the pigeon, the digital
camera, the San tenses, the television balance point, the photography closing
sentence, the traction claim (in **three** fields), the ships' propulsion frame, and
the broadcasting entry (twice).

**Three of those I created myself, by adding a later note instead of amending the
one that gives the order.** Each time I changed a decision, wrote a fresh note
recording the new ruling, and left the old note standing as a live instruction:

* the broadcasting entry, twice — first prescribing a radio-or-television signal,
  then prescribing "anyone who has such a device", each of which I had already
  overruled;
* the rock-art duration, prescribing a positive statement of duration after I had
  ruled the duration out entirely.

A writer caught every one.

**Why appending feels safe and is not.** Adding a note preserves the record, which
is a real virtue — the reasoning and the sources have to survive. But a
specification field is read as an *instruction*, and a reader who takes the first
coherent instruction has taken the old one. The record and the order are different
jobs, and only one of them can go first.

**So: the order goes in the opening, the record goes below it, and the record must
not be phrased as an instruction.** When a decision changes, the opening line
changes in the same edit. If the history is worth keeping — it usually is — it goes
under a marker that says plainly it has been superseded, quoting the old wording so
nobody restores it by accident.

The diagnostic that settles it: **the one Kwartaal 4 lesson that needed only two
rounds is the one whose correction went into the requirement's opening line.** Every
lesson that took three or four rounds had its correction appended. That is not a
coincidence about difficulty — early writing was not an easier lesson than the
others.

Related: [[n-ruil-wat-nie-pas-nie-moet-hard-faal]] (print the fields and act on the
whole print), [[n-spek-se-dieselfde-ding-in-twee-velde]] (one claim can sit in three
fields — it did), [[n-verslag-in-die-logboom-kan-verouderd-wees]].

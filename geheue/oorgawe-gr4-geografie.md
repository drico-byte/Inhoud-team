---
name: oorgawe-gr4-geografie
description: "Handover of Grade 4 Geography to another machine, 6 October 2026. What is finished, what is left, what is waiting on Drico, and the traps this sub-topic produced that the next machine will meet again."
metadata:
  type: project
---

# Handover: Grade 4 Sosiale Wetenskappe — Geografie

**Written 6 October 2026**, handing over from the machine with the smallest token
allowance. Everything below is pushed to `main`; the repository is in sync.

## Where the subject stands

Grade 4 Social Sciences is **44 of 60 lessons signed off**. The History side is
complete (30 of 30). Geography is **14 of 30**, and all 16 remaining lessons are
in this handover.

| Sub-topic | Term | Planned | Signed off | State |
|---|---|---|---|---|
| Kaartvaardighede | 2 | 8 | **8** | complete |
| Plekke waar mense woon | 1 | 7 | 6 | lesson 7 drafted and gated, coverage clean, fact check outstanding |
| Voedsel en boerdery | 3 | 6 | 0 | spec approved, nothing written |
| Water in Suid-Afrika | 4 | 9 | 0 | spec approved, nothing written |

Both unstarted sub-topics have approved specs and are ready for the writer.

## Pick up here

**1. Settlements lesson 7, "Dieselfde behoeftes, verskillende maniere".** Drafted,
gated, coverage GOEDGEKEUR. Its fact check has never completed — it was killed
twice, once at a usage limit and once at a network error. It has already been
through eight fact-check rounds, and the lesson's four place blocks (farm,
village, town, city) are a **parallel set**: say so in the brief and ask for the
set to be read as a set, or the round is wasted. See
[[toets-n-parallelle-stel-as-n-stel]].

**2. One question for Drico is open on that lesson** and blocks nothing else: the
farm block says "Op baie plase plant die mense self 'n deel van hulle kos". Eight
rounds have survived it, but no source measures own-food production by households
*living on* farms, and "the people" is ambiguous between the farmer's household
and the roughly 2.08 million farm dwellers. Keep, narrow, or cut.

**3. Then the two unstarted sub-topics**, in term order.

## Open questions waiting on Drico

- **The farm sentence**, above.
- **North America has no position in map skills lesson 8.** The lesson names seven
  continents and places five. Placing it needs a second intermediate direction
  ("noordwes") where the spec allows one, and both CAPS's bullet and the video
  name the same five. There *is* budget room — the lesson measures 327 of 400 —
  so the obstacle is scope, not cost. The promise was narrowed instead, which is
  reversible. Recorded in that lesson's fact-risk field.
- **Does any province name sit outside its own borders on the map these learners
  actually use?** Map skills lesson 7 carries a fallback step for labels printed
  outside their province with a leader line. One fact check supported it on
  general cartographic practice; another could find no map of South Africa that
  does it for a *province* name, and the one official map it reached prints all
  nine inside, Gauteng included. Not false, possibly just empty, about twenty
  words. Anyone holding the classroom map settles it in seconds.

## Rulings made during this stretch — these bind

- **Drico, 5 October: CAPS does not ask how a map marks a capital, so it is
  dropped.** The Term 2 content table puts five bullets under the
  map-of-South-Africa topic and "hoe dit aangedui word" attaches only to the
  sea-and-land bullet. Symbols and keys are a separate three-hour topic about
  large-scale maps, which lessons 4 deliver. Map skills lesson 7 now says nothing
  about how a map marks a capital.
- **Drico, 5 October: Lesotho stays unmentioned** in the province-finding method.
  The method starts from a name the learner already has, so she looks for
  "Limpopo" and never lands on Lesotho; it only bites if she uses the map to
  discover how many provinces exist, which the lesson never asks.
- **Two oceans, not three, for any lesson about the coastline** (6 October). The
  environment department and the navy's maritime doctrine say three and are
  describing the whole maritime territory, out to the Prince Edward Islands at
  about 46°S. CAPS asks for the oceans "langs die kuslyn". `twee oseane` is now
  in the protected-words file, because the department's own wording is exactly
  the improvement an outside language check would make — and it would arrive
  after the last check that could catch it.

## For the end-of-year reconciliation

- **`eiland` is worded two different ways.** Lesson 2 owns the glossary entry and
  uses "kleiner as die kleinste kontinent"; lesson 8 uses "nie een van die sewe
  kontinente nie". Both are inside the decided scope, so this is not drift — but
  **the drift sweep cannot see it**, because lesson 8 carries the rule in study
  text rather than as a glossary entry and the sweep reads glossary entries.
- **A fact checker argued the shared wording itself is wrong** — that size is the
  whole distinction and the rule should carry the Britannica form plus "there is
  water around the continents too, but we do not call them islands because they
  are so big". That argues against the subject's shared wording rather than
  against one lesson, and a third wording is worse than leaving it alone. Filed,
  not acted on.
- **A cosmetic spec cleanup** in map skills lesson 7's budget note: the removal
  explanation was patched *inside* item (f), so the line now reads as though
  "what a capital is" was struck when only the map-marking half was. Nothing is
  contradicted. Batch it with the next substantive edit to that entry rather than
  spending a coverage re-run on it.

## Traps this sub-topic produced, in the order they will bite

**The repair creates the next fault.** Map skills lesson 7 took six revision
rounds and lesson 8 took four, and in almost every case the next finding was
caused by the previous fix. Two distinct mechanisms:

- *In a parallel set, whatever appears in exactly one item reads as what makes
  that item different.* Lesson 8's five-line position list produced three
  successive faults this way — a distance word on one line, then an ocean clause
  on one line, then two lines naming water while three were silent. **Uniformity
  is the only stable state**; a better distribution of clauses is not a fix.
- *Closing a fault with an OPTION hands the writer a sound-in-isolation choice
  that is wrong inside the set it lands in.* Twice I wrote "either say nothing,
  or say X", the writer correctly took X, and X was the next finding.

**Six sweep misses in one day, every one found by a checker or a writer rather
than by me.** The mechanism is always the same: a correction lands in the field
where the *finding* was reported, and a neighbouring field still *orders* the old
form. Three things to check of every field that touches the subject, not one:
does it repeat the old claim, does it record a ruling that has now been reversed,
and does its reasoning still hold given what the check established. The worst miss
came from narrowing a sweep with a conjunction — I searched for "symbol" AND
"capital" in the same passage, and the field that escaped mentions only the first.

**Widening a definition without re-reading its article.** The glossary entry for
`hoofstad` was too narrow, so I widened its scope to cover a country as well as a
province — and the unchanged definite article then asserted that a country has
exactly one capital, which is false of the only country the lesson is about.
Narrow to false in a day, in the field I had just rewritten.

**Exact-string guards in fix scripts failed five times in one day** — on capitals,
an accent, an assumed full stop, and an en dash where the field had an em dash.
All failed loudly, which is the only reason none did damage. Anchor on the
shortest distinctive fragment either side and slice between them, so punctuation
never has to be reproduced. And remember a prohibition must quote the wording it
forbids, so a sweep asserting "the old wording is gone" fires on the fix's own
quotation — assert against the field's opening line instead.

## Tooling notes worth knowing

- **The log-merge helper assumes a clean working tree and cannot have one.**
  Running the gate writes to both append-only logs, so there is always something
  uncommitted when you come to merge; the helper aborts before reaching its own
  conflict handling. Commit the logs first, then it works exactly as designed.
- **The hand-check sign-off tool has no path for an escalation a person has
  ruled on.** It requires GOEDGEKEUR from both checks. A fact check that
  escalates one item it cannot settle is the normal end of the process — the
  human decides — and there is currently no way to record that decision and
  proceed. I resolved it by sending the ruling back to the checker that raised
  it, which is cheap and keeps the record honest, but it is a workaround.
- **Staging the outbox folder kills a commit silently-ish.** It is gitignored, so
  `git add` refuses and takes the commit with it. Check the resulting hash.
- **Agents reported as failed may have finished, and agents one step from writing
  lose everything.** Measure before re-running: today two of three killed agents
  had written complete reports, and two others died immediately before writing
  and lost a full check each. Tell fact checkers to write as soon as they have
  findings.

Related: [[gr4-geografie-besluite]], [[gr4-sw-waar-ons-is]],
[[drie-rekenaars-werk-parallel]], [[n-videofrase-beland-in-vier-plekke]].

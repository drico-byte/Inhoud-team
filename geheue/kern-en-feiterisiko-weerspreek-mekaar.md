---
name: kern-en-feiterisiko-weerspreek-mekaar
description: "A spec's kern can contradict its own feiterisiko — and kern wins, because coverage tests against kern. Three writers caught this in one day."
metadata:
  type: feedback
---

7 September 2026, Gr 4 Sosiale Wetenskappe. Three separate writers reported the same
structural fault in three different specs, and none of it was visible to me.

A planner writes `kern` as the content a lesson must cover, and `feiterisiko` as warnings
about how to state it safely. **Nothing checks that the two agree**, and when they
disagree `kern` wins — because a writer is obliged to cover `kern`, and the coverage
checker tests against `kern` too. So a `feiterisiko` entry saying "do not claim X" sits
beside a `kern` item that requires exactly X.

The three:

* **Kwartaal 1 les 5.** `kern` offered *"wie die verlede verstaan, verstaan die hede
  beter"* while its own `feiterisiko` warned that reasons must read as reasons. The
  writer wrote the *helps* version and said the spec's phrase was missing on purpose.
* **Leiers les 4.** `kern` said *"In 1994 kon almal vir die eerste keer stem"* — literally
  false, since white South Africans voted in earlier elections — while the same spec's
  `feiterisiko` gave the safe form.
* **Kwartaal 1 les 4.** `kern` required *"die jare wat met 18 begin val in die 19de eeu"*
  while the seam said not to settle the century convention; the example only holds under
  the loose one.

**A fourth of the same family, worth keeping together:** the requirement that Gandhi's
lesson *show* courage lived only in a coverage table and never in `kern` — invisible to
the writer working from `kern` and to the checker testing against it.

## How to apply

**When a `feiterisiko` entry contradicts a `kern` item, fix the `kern` item.** The
warning is usually the checked half and the requirement usually the drafted half.

**And read a new spec for internal disagreement before briefing a writer** — not just for
whether each field is right. Grep the entry for the words a warning turns on and see
whether a requirement uses them. This is the same sweep as
[[n-spek-se-dieselfde-ding-in-twee-velde]], one level up: there the same claim appeared
in several fields and one was missed; here two fields say opposite things.

**Every one of these was found by a writer, not by me.** A writer told to report what it
thinks is wrong with the spec, using exact quotes, is the cheapest fact check in the
pipeline — it reads the whole entry closely because it has to write from it.
Related: [[spesifikasies-word-nooit-nagegaan]], [[n-spek-se-dieselfde-ding-in-twee-velde]]

## The note predicted the fault correctly, and nothing makes the prediction block the writing

**8 October 2026.** A Graad 6 history lesson's fact-risk field said, before a word was
written: *the size of K2 against Schroda ("bigger") must be verified. Give no population
figure, area or number of houses for either.* Its `kern` field, three items away,
flatly ordered **"K2: a settlement that came after Schroda and was bigger"**.

`kern` won, because that is what the coverage checker tests against. The lesson said it,
the gate passed it, coverage passed it. The verification the note demanded ran a week
later, as the ordinary per-lesson fact check, and found the comparison does not hold:
Schroda is a ~15 ha site against a ~5 ha K2 capital, so on area the *earlier, smaller-
sounding* place is about three times bigger. The population half points the other way
but is itself unsettled, and the figure usually quoted could not be traced to a primary
study.

**So the planner was right, specific, and early — and the machinery had no way to act
on it.** A fact-risk note is a PREDICTION. Nothing in the pipeline turns a prediction
into a gate: the writer reads both fields and the flat order wins, and the only check
that could settle it runs after the writing.

**How to apply.**

* **Read `feiterisiko` as a work list before briefing anything**, not as commentary.
  Every item that says "verify before writing" or "cut it if it does not hold" is a
  question I must answer MYSELF, by fact-checking the specification, before the writer
  runs. That is now the practice for every remaining sub-topic — see
  [[spesifikasies-word-nooit-nagegaan]].
* **Where the note demands a check, the `kern` item must not state the thing flatly.**
  If I cannot settle it in time, the order has to be softened at source, because
  coverage will otherwise defend the unverified claim against the draft.
* **When the check finally comes back, record the ANSWER in the fact-risk item**, dated.
  Otherwise the next writer meets the same open question and resolves it the same way.

## A third shape: offering a branch a sibling forbids

**9 October 2026.** Having changed the container of a claim after three failures, I
offered the writer two permitted branches: the SUCCESSION - each centre in turn held
more people than the one before - or the VALLEY'S total population.

A writer pointed out that the first branch **is** a population comparison between the
first two centres, and that another core item and its fact-risk item forbid any size
comparison between exactly that pair, in either direction, population included, because
the sources run opposite ways on area and on population for them. So the branch could
never be written.

**This is not a contradiction, and that is what makes it hard to see.** Nothing in
either field is false, neither field orders the opposite of the other, and the sweeps
have nothing to catch: one field offers A or B, another forbids A. **The lesson came out
whole** because the writer took B and said so. Had it taken A, coverage would have
passed a draft that a different requirement prohibits - and coverage reads one lesson
against one spec entry, so nothing in the per-lesson pipeline could have objected.

**How to apply.**

* **A permitted alternative is an order too.** When a requirement offers a choice, check
  each branch against every prohibition in the entry, not just the one the branch came
  from. The cheapest version: for each branch, ask which field would stop a writer
  writing it.
* **Prefer one branch to two.** I wrote two because I was not sure which the lesson
  would need; that uncertainty is exactly what the fact check had just resolved, so the
  second branch bought nothing and cost a round.
* **This is the third time today a writer caught what no sweep of mine could** - the
  other two being an unanchored comparative inside a period, and a notice of mine that
  forbade what two other fields ordered. All three were found by reading the fields in
  order, as prose, which is what a writer does and a sweep does not.

**Fourth instance, and the worst, 14 October 2026.** On Medisyne lesson 7 the feiterisiko item ORDERED the form that the kern item, corrected the same day, declares false — and called that order the careful one. Two inverse orders, both in capitals, both live. Nothing in the repository could see it: every order/record test compares a field against the record at its own path, and these were two different paths. A writer found it by reading the entry as prose, followed the kern, and reported it. **So the rule has a corollary: after correcting a claim in kern, read every other field of the same entry that mentions the claim at all, before the next agent is briefed.** I corrected the kern and did not re-read the feiterisiko, and the sibling then contradicted it for a full day.

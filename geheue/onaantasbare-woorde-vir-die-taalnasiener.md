---
name: onaantasbare-woorde-vir-die-taalnasiener
description: Afrikaans checking happens outside this pipeline, so every word ruling has to be written into kaps/beskermde-woorde.json or the checker will quietly undo it.
metadata:
  type: project
---

The Afrikaans language check is done outside this pipeline, by a tool with
better Afrikaans than ours. It fixes grammar, idiom and direct-translation
errors, and it is good at it.

**It will also undo our decisions unless it is told not to.** Every protected
word reads like ordinary Afrikaans that could be improved — that is exactly why
it needs protecting. `energie` where `krag` sounds more natural. `die meeste`
where `byna elke` is smoother. `ungquphantsi`, which looks like a typo. `duim`
where `duimnael` seems more precise. Each of those is a correction a fluent
reader would make, and each puts back an error a fact checker found.

**How it works.** The rulings live in `kaps/beskermde-woorde.json` — the word to
keep, what it must not become, and **why**. `bin/taalnasien.py` builds the block
to paste into the checker: the instruction, that list filtered to words actually
in this lesson, then the lesson text. Glossary entries shared between lessons are
protected automatically, by reading the other lessons rather than by anyone
listing them.

**How to apply — this is the part that decays.** When a checker's finding, or one
of Drico's rulings, settles a word, **write it into that file in the same breath**.
The specification records it for our own writer; nothing carries it downstream
unless it is there. The reason field is not decoration: a checker that
understands why `krag` is wrong holds the line when a sentence reads awkwardly;
one that sees only a prohibition overrides it and believes it is helping.

**A signal worth reading.** If the checker keeps proposing the same change to the
same protected word, the word is usually not the problem — the sentence around it
is awkward, and the fix is to rewrite the sentence so the protected word sits
naturally. That goes through the writer, like any content change; see
[[moenie-self-inhoud-skryf-nie]].

## Which of our notes actually reach that checker — check, never assert

**1 October 2026.** I told agents twice in one day which glossary fields travel
to the outside checker, and I was wrong both times, in opposite directions:
first that the reason fields were "notes for humans only", then that three
particular fields were "handed over in full". Both went into briefs, and both
times the agent measured it and corrected me. The hazard ranking in a brief
depends on this, so **read `bin/taalnasien.py` before telling anyone a field's
audience.**

What was actually true on that date, in the agreed-wordings file:

* `rede` and `let_op` **do** travel, in full — but **only for a term with a
  single `omskrywing`**. The builder skips any term whose `omskrywing` is null.
* A **two-meaning term** (wordings under `betekenisse` instead) therefore gets
  **neither reason to the checker**. It reaches the block only by the weaker
  "the same definition stands in another lesson" route, which prints no reason
  at all.
* `waar` is read by **nothing** — not the injector, not the checker, not the
  drift sweep. People only.

**Why the middle one is a hole and not a detail.** A two-meaning term is exactly
the kind most likely to be "improved" wrongly, because each wording reads odd
next to the other — and it is the one term whose reason cannot reach the only
checker that will edit it. If a two-meaning ruling must hold downstream, it needs
protecting in `kaps/beskermde-woorde.json`, which does travel.

## Do not hand-protect a term whose decided wording already travels

**1 October 2026.** 41 terms are both hand-protected and a decided wording, and
most are legitimate — the hand entry protects a **word** against a named swap
(`energie` not `krag`), the agreed list protects the **definition's wording**.
Those say different things.

So the test before adding one: **does it name a swap the decided wording does not
already cover?** If not, leave it. A redundant entry makes the block print the
term twice under two different justifications, and the tool's own comment notes
that this invites the checker to wonder which is the real one. The deduplication
spans only the hand-written sources; it does not suppress a hand entry against
the decided-wording path.

**And the real silent-loss risk on that path is drift, not length.** A decided
wording is protected only where the lesson reproduces it **character for
character**; a lesson whose copy has drifted gets no protection and the block
says nothing about it. That is the drift sweep's job, not this file's — but it is
the failure mode to watch.

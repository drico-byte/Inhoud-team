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

## The ǀXam name takes the real click letter — Lampies, 7 October 2026

Two approved subjects ordered opposite spellings of one language's name, and both
orders were live:

* **Grade 4 Natuurwetenskappe en Tegnologie** (the Moon) writes **ǀXam** with the
  click letter (U+01C0) and says in terms that it is *not* a forward slash and not
  an upright bar, and may not be replaced — including by the layout team. Those
  lessons are signed off and delivered.
* **Grade 6 Sosiale Wetenskappe** (Democracy and citizenship) writes **/Xam** with
  a forward slash and ordered that the slash not be corrected. The protected-words
  list backed the slash.

**Grade 4 was right and wins.** It is a distinct letter; the slash is a typewriter
substitute. So Grade 6 changes, the protected-words entry changes with it, and the
subject gets swept for slashes.

**Why the slash looked defensible, which is the part worth remembering.** It
survives any font and any hand, and a language checker meeting `ǀXam` sees a typo —
which is exactly why the word needs protecting rather than substituting. The
substitute was a production hedge dressed as an orthographic decision, and nothing
in the pipeline could see the disagreement because **no check reads two subjects at
once.** A protected word is per-word and a sweep is per-subject; a name shared
across two subject-grades falls between them.

**How to apply:** when a ruling settles the *spelling of a name*, ask which other
subject-grades use that name before writing it down — the glossary sweep will not,
because it only reads one subject at a time.

Related: [[n-videofrase-beland-in-vier-plekke]] (one wrong form reaching four
places), [[lysblokke-het-nooit-by-die-taalnasiener-uitgekom-nie]].

## How the two scopes actually match, and the collision waiting in the narrow one

**7 October 2026**, established by reading `bin/taalnasien.py` rather than reasoning
about it. Worth having written down, because scoping a protection correctly is what
makes it safe to protect a word at all.

* **A general entry** matches its kept word as a **plain substring, across every lesson
  in every grade and every subject.** That is why a common word cannot be protected
  generally: four existing entries actively *require* `staat` in delivered Kwartaal 3
  text, so a general ban on it would have contradicted entries already in the file.
* **A per-sub-topic entry** is keyed on the sub-topic's **DIRECTORY name** — not on
  the `--subonderwerp` argument — and it fires only where the kept word is really in
  that lesson, matching the kept form **or just its first word**.
* **`nie` is advisory prose, not a mechanical ban.** It prints as "this is the swap we
  fear". That is enough, because the reason travels with it and a checker who
  understands why holds the line.

**The scope gate is what resolves an opposed pair.** `koninkryk` is protected against
`staat` inside one sub-topic, and it fires on the three lessons carrying `koninkryk` and
**never on the lesson that owns the decided `staat` entry** — so no block is ever handed
opposite instructions. Verified in a real block, on all ten lessons, not assumed.

**The collision waiting in it: the key carries no subject and no grade.** `kaartvaardighede`
exists as a sub-topic directory in **both** Grade 4 and Grade 6 Sosiale Wetenskappe, so a
section written for one already applies to the other. Nothing is written there today;
when something is, it will fire across two grades silently. Same family as
[[n-skoon-toets-is-so-wyd-soos-sy-omvang]]'s cross-subject blind spot — a scope that
looks narrower than it is.

**And the first-word fallback makes a wrong entry worse than a dead one.** An entry whose
kept form begins with an ordinary word — "eerste …" — fires on every lesson in that
sub-topic containing that ordinary word, handing the checker a protected wording that is
**not in the lesson it is reading.** Measured: three lessons would have matched, one of
them carrying no such claim at all. That is the false-reason class the file was repaired
for, and it is the reason **a wording is protected only once the sentence exists**, never
in advance of the writer.

**Two carve-outs worth keeping in mind when choosing a forbidden form:** never list a
substring of the kept word (`ryk` inside `koninkryk` fires wherever the correct word is
used), and never list a word that is correct in another sense in the same sub-topic. Put
those in the reason prose instead.

## A forbidden-form list can express a substitution but never an insertion

**8 October 2026.** Protecting a short sentence exposed a precise limit. The likeliest
edits to *"Een keer is genoeg."* — the sentence that worked example came from, since **withdrawn from every entry on 8 October 2026**, which changes nothing about the mechanism — are not replacements but **insertions** — *een
**enkele** keer*, ***selfs** een keer*, *een **ernstige** keer*, *een keer **kan** genoeg
**wees***. Every one of those **contains** the kept form, so listing it as a forbidden
form trips the substring trap in reverse: a `nie` entry that swallows its own `hou`.

**So the `nie` list can only hold forms that stand in place of the kept sentence.** An
insertion has to be forbidden in the **reason** instead, as a scoped rule — no word may be
added to this sentence, neither to strengthen it nor to soften it — naming the likely
additions. That also matches what the printed line means: `NIE` renders as alternatives to
the kept form, so an insertion listed there would read as a substitute and invite the very
confusion that a word may be swapped in.

**The same split applies to an absence.** A sentence that must *stay absent* has nothing
to keep, so it rides in the reason of an entry protecting something present nearby — best
the same glossary entry, so the checker has it open. That coupling is the honest limit: if
the carrier sentence is ever rewritten, the entry stops firing and the absence warning
leaves with it, silently.

**So, for any sentence-level protection, work out which of three things you are
defending** and place each where it can actually live:

| what you are defending | where it goes |
|---|---|
| this wording rather than another | the `hou`, with substitutes in `nie` |
| this wording unmodified | the reason, as a no-additions rule |
| the absence of a sentence | the reason of a neighbouring kept form, knowing it is coupled to it |

And note the first word of the kept form decides the noise: matching falls back to testing
it as a **plain substring**, so `een` fires inside `geen`, `kla` inside `klas` and
`klagte`, `keer` inside `verkeerd`. Pick the rarest word the ordered phrase allows, and
name the spurious lessons in the reason — half this subject's lessons are delivered, so a
spurious firing reaches a checker reading finished work.

## The six Afrikaans faults that keep reaching the specialist, and why naming them matters

**8 October 2026.** A reason written for the language checker carried a missing second
negative. I sent it back and asked, in the same breath, for **the rest of the inherited
text audited the same way** — and that found **two more faults, in the agent's own new
text**, of a class it had not been asked about:

* ***was* plus a participle for the action passive.** `HAAR EIE REDE WAS TERUGGETREK` →
  `IS TERUGGETREK`. `was` is the state passive; it is also exactly what a straight English
  rendering produces, which is why it slips through.
* ***klaar* used attributively.** `klaar werk` → `voltooide werk`. `klaar` is predicative
  in Afrikaans; in front of a noun it is marginal.

**It had audited its own sentences for the second negative and not for the passive.** That
is the right behaviour given the brief, and it is the point: **an agent audits the class
you name and no further.** Same shape as [[vee-die-bewering-oor-al-die-spesifikasies]] —
knowing the rule is not briefing it.

**So name the classes. These six have all shipped or nearly shipped this week:**

1. **The missing second negative** — `nie … nie`, `geen … nie`, `niks … nie`,
   `nooit … nie`, `moenie … nie`. The commonest by far, and it **inverts the meaning**.
2. **`was` + participle where the action passive needs `is`.**
3. **Predicative words used attributively** — `klaar werk` for `voltooide werk`.
4. **A diacritic that changes the word** — `sê`/`se`, `reël`/`reel`, `nêrens`,
   `weerlê`, `voorkom`. One pass caught nine in a single sitting, and another caught
   `nîrens` written with a circumflex.
5. **Non-words produced by string surgery** — `gefouteer`, `toegewysde`, `mocht` (Dutch),
   and a space lost mid-word (`Suider-Afrikaas`).
6. **English left in an Afrikaans field** — `narrow` inside an ordering sentence, `hero`
   in a house note.

**Where this matters most.** A reason in the protected-words file goes **verbatim** to a
specialist whose whole job is Afrikaans, inside a document asking them to trust our
judgement on Afrikaans. A fault there costs standing on every other sentence in the block
— so the audit is not pedantry, it is the thing that makes the protection believable.

**And ask for the arguable cases to be named rather than fixed.** The same pass flagged
three sentences as stiff or compressed but not wrong, and left them. That is the right
answer: a judgement call made silently inside a document addressed to someone better at
the language than we are is worse than an awkward sentence.

## 13 October 2026: measure the anchor with the collector, not with my own regex

A `per_subonderwerp` entry matches the protected phrase **or its first word**, so the first
word decides how many lessons receive the entry. I wrote five entries for Gr 6 SW Medicine
in one afternoon and got the anchor wrong twice:

* `Hy het vloeistof in glasflesse gegiet` — first word **Hy**, so it fired in **9 of 10**
  lessons. Re-anchored to `vloeistof in glasflesse gegiet`: 1 of 10.
* `daardie kiem alleen in 'n gesonde dier ingebring` — first word **daardie**, 7 of 10.

**The part worth carrying.** I then measured candidate anchors with my own
`re.search(r"\bkiem\b", teks)` and got **3 of 10** — but the real figure, from
`taalnasien.versamel`, was **5 of 10**. My regex and the collector do not agree, and the
collector is the only number that matters because it is what builds the block a checker
reads. So: **measure with `taalnasien.versamel` on the actual lesson files**, assert the
count before writing the entry, and never trust a hand-rolled word search as a proxy for
a tool's own matching.

A rough bar from the entries that look right: 1 or 2 of a sub-topic's lessons is clean,
about half is the practical ceiling (two existing entries sit at 5 of 10 because the term
genuinely runs through those lessons), and anything near every lesson is noise that
dilutes the whole list a checker is handed.

And the reason to care at all: nothing re-gates or re-checks a lesson after the outside
language check, so an entry that never fires where the sentence lives protects nothing,
while one that fires everywhere teaches the checker to skim. Related:
[[die-handwysig-wag-werk-meestal-nie]], [[n-skoon-toets-is-so-wyd-soos-sy-omvang]].

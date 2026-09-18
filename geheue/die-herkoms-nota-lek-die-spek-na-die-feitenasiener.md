---
name: die-herkoms-nota-lek-die-spek-na-die-feitenasiener
description: "The fact checker never gets the spec — but the provenance note inside the lesson file carries the spec's intent, and the checker reads it because it is in the file it was given."
metadata:
  type: project
---

8 September 2026, Gr 4 SW Kwartaal 4 lesson 11. A fact checker finished its report and
then raised something nobody had asked it about:

> The lesson's own provenance note spells out what the specification requires, which
> item was deliberately left out, and the reason behind each change. I read it because
> it is inside the lesson file, but it hands the fact checker exactly the intent the
> separation exists to withhold — it is the charitable-reading risk, arriving through
> the back door.

**Why this matters.** The whole design rests on one separation: coverage needs the spec,
and **the fact checker must never have it**, or it reads the lesson charitably — judging
what the lesson was *trying* to say rather than what it says. That is written into
CLAUDE.md and into every fact-checker brief.

But writers record their reasoning in `herkoms.nota` inside the draft, and they are right
to: it is how a decision survives to the next revision, and several corrections this
quarter were saved precisely because a writer wrote down why something was cut. The note
routinely contains the spec's requirements quoted directly, which items were deliberately
omitted, and the argument for each choice.

The fact checker is handed the lesson file. The note is in it. So the separation leaks —
not through anyone's mistake, but through the file format.

**How bad is it in practice.** Not catastrophic, and no finding this quarter was
obviously softened by it. The checkers have been sharp on lessons whose notes explained
the intent at length. But the risk is exactly the one the separation exists to prevent,
and it is invisible: a charitable reading leaves no trace, so we would not know.

**What to do about it — not yet decided, and it is Drico's call.** Three options, in
increasing cost:

1. Split the note: keep the writer-facing reasoning where it is, move the spec-facing
   part (quoted requirements, what was deliberately omitted) to a sibling file the fact
   checker is not given.
2. Have the runner strip `herkoms.nota` from the copy it hands the fact checker, the way
   it already withholds the spec extract.
3. Leave it, and tell fact checkers explicitly not to read the note — weakest, because it
   asks an agent to unsee something in a file it must otherwise read whole.

Option 2 is the one that matches how the rest of the pipeline works: the runner already
decides what each checker sees, and this is the same decision.

**Until it is decided**, do not write spec requirements verbatim into a lesson's
provenance note. Record *what changed and why* in the writer's own words; leave the
quoting of requirements to the spec, which is where a coverage checker will read it.

Related: [[spesifikasies-word-nooit-nagegaan]], [[n-feiterisiko-is-nie-n-regstelling-nie]],
[[die-textbook-kom-ook-deur-die-soekresultate]] — the same shape as that one: a boundary
we thought was closed, leaking through a route nobody designed.

## It is getting worse, and a second checker has now raised it unprompted

9 September 2026. A second fact checker raised the leak on its own, in the same terms as
the first, and added the thing that changes the picture:

> The provenance note inside the lesson now carries several pages of the specification's
> reasoning, including what a core requirement asks for. I read it before I could avoid
> it. It did not change my findings — the rock-art finding is one the note explicitly
> argues against — **but it is getting longer with each revision.**

That last clause is why this should not keep being deferred. Every revision adds its
reasoning to the note, so the leak **grows monotonically** with the number of times a
lesson is corrected — and the lessons most in need of an honest fact check are exactly
the ones that have been revised most. The mechanism gets worse precisely where it matters
most.

Two further observations from the same day, both arguing the same way:

* The Kwartaal 4 lessons carry notes of around 8KB. **Ten of the nineteen Kwartaal 1-3
  lessons have no note at all** — so the pipeline is currently inconsistent about whether
  a fact checker sees the spec's intent, and nobody chose that.
* The interim instruction in this note ("do not write spec requirements verbatim into a
  provenance note") is not holding. Writers record requirements because it is how a
  decision survives, and telling them not to is asking them to lose the thing the note
  exists for. The instruction was the wrong shape.

**Still Drico's call**, and still option 2 — have the runner strip the note from the copy
the fact checker gets. It is the only option that lets writers keep recording their
reasoning in full, which they should, while giving the checker the lesson alone. The
runner already decides what each checker sees.

## Decided, built — and then it leaked for a week under other names

Drico chose option 2 on 9 September 2026 and the runner has stripped the note since.
**It strips `herkoms.nota`, by name.** On 16 September a fact checker on Kwartaal 1
lesson 5 raised the leak again, in the same words as the first two:

> The copy withholds the provenance note, as it should. But there is another note
> beside it that came through, and that one quotes the specification's requirements
> directly — which core point asks for what, and a warning out of the spec's own risk
> notes, in capitals. I read it before I realised what it was.

Writers had invented **twelve** names for the same field: `nota`, `hersieningsnota`,
`hersiening_nota` through `hersiening_nota_6`, `nota_eli10`, `nota_feite`, `besluite`,
`kaps_punt_woordeliks`, `kaps_punt_nota`. The strip caught one. Four lessons were
leaking, one of them through six notes at once.

**The lesson is about the shape of the rule, not the bug.** A list of what to remove
loses to every name invented after it is written, and nothing fails loudly when it
does — the copy still gets made, the checker still runs, and the leak is invisible
exactly the way a charitable reading is. The strip is now an **allowlist**: the CAPS
document, the profiler config, the writer prompt, and the two "did you look at it"
records. Everything else under `herkoms` goes, and the marker says how many fields
were withheld rather than implying there was one.

**How to apply:** when a boundary is enforced by naming what may not cross it, assume
it has already been crossed under another name, and go and count. Ask the question the
other way round — what is this checker *entitled* to see? Same family as
[[n-regstelde-fout-kom-in-n-ander-gedaante-terug]] and
[[n-skoon-toets-is-so-wyd-soos-sy-omvang]], where a second directory of copies walked
past a sweep that skipped the first one by name.

Three fact checkers have now raised this unprompted, each one on its own initiative.
That is the strongest signal this project produces, and it has been right every time.

## And then it leaked through a field the allowlist keeps

18 September 2026. The allowlist held against new note names, as designed. The leak
came back anyway, through `profiel_konfig` — a field on the KEEP list, because it is
supposed to name a measurement config.

Writers had been writing sentences into it: which config the brief named, what the
**specification** says about the budget basis, who decided a number and when. Twelve
lessons across four subjects. A fact checker on Kwartaal 1 lesson 4 read one and said
so — the fourth checker to raise this unprompted, each on its own initiative.

`profiel_konfig` is now off the list. Asking the allowlist question properly answers
it: a fact checker verifies claims against outside sources and has **no use for budget
provenance at all**.

**The general lesson, which is not the same as the last one.** An allowlist is only as
good as the assumption that each kept field holds an *identifier* rather than prose.
Names were the previous failure; field *types* are this one. When you keep a field,
check it cannot carry a sentence — and if it can, either drop it or ask what the
reader is entitled to see rather than what the field is nominally for.

Four checkers, four costumes: the note itself, eleven other note names, and now a
field nobody thought of as a note at all.

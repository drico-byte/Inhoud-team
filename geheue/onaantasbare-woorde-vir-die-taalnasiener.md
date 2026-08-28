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

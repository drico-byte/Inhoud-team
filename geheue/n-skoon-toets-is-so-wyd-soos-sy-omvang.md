---
name: n-skoon-toets-is-so-wyd-soos-sy-omvang
description: I reported "zero glossary drift across the whole subject" after a check that only covered one sub-topic. A full sweep found eight drifted terms. Never state a green result more widely than the thing that was actually looked at.
metadata:
  type: feedback
---

I ran a glossary check while repairing lesson 12, saw no disagreement, and told
Drico there was **zero glossary drift across the whole subject** — adding that it
was the first time since the check was built. A proper sweep over every lesson in
Gr 4 NWT found **eight** terms defined two or three different ways: *eienskap*,
*geraamte*, *habitat*, *materiaal*, *ru-olie*, *struktuur*, *stut*, *waterdamp*.
Twenty-two terms appear in more than one lesson, so more than a third of the
shared vocabulary had drifted.

**Why it went wrong:** the check I ran compared lesson 12 against lesson 13 —
the pair I was repairing. That is a correct check of a pair. I reported it as a
check of the subject. Nothing in the output claimed the wider scope; I supplied
that myself, and a clean result is exactly the kind that never gets questioned.

**What made it worse:** the coverage checker on lesson 12 is what exposed it. It
noticed the corrected definition now leans on *eienskappe*, a word lesson 12 never
explains — and looking for where that word IS explained is what turned up two
different definitions of it in two already-delivered lessons.

**How to apply:** report the scope in the same sentence as the result — "lessons
12 and 13 agree", not "no drift". Before any claim about the subject, run the
sweep over every lesson file in the subject and say how many files it read. Same
failure as [[vra-die-hele-vak-nie-drie-lesse-nie]], one step further along: there
the shortlist was in the search, here it was in the sentence describing it.

## The scope can also be wrong in the tool, and wider is not safer

16 September 2026. The sweep itself was reading each lesson twice. It already
skips `spek/` — spec extracts share the draft's file name, and that bug is
written up in the function's own docstring. A `feite-kopie/` directory was added
later, for a good and unrelated reason, and nothing went back to the tools that
walk that tree.

**Why this one was worse than the documented bug.** An extract carries no
`blokke`, so it only inflated the count. A fact-checker copy *is* the lesson
minus one field, so it fed wording into the comparison. The runner regenerates
it, so a lesson revised since its last runner call sits next to a copy of its own
old glossary — and the tool reports the lesson as drifting **against itself**. I
was handed one such phantom and nearly went and "fixed" it.

The printed numbers were wrong in both directions at once: 51 lessons and 119
shared terms became 30 lessons and 7. Every earlier "this subject is consistent"
was measured against that.

**How to apply:** when you add a directory of derived copies, go and look at
every tool that walks the tree — the copy is indistinguishable from the original
by file name, which is the whole reason the first version of this bug existed.
And when a sweep reports drift between a lesson and something in a sibling
directory, check that the sibling is not a copy of that same lesson before
briefing anyone. Same family as
[[n-regstelde-fout-kom-in-n-ander-gedaante-terug]].

## No check reads two subjects at once, and I found that twice in one day

**7 October 2026.** Every consistency check we own is scoped to one subject-grade.
The glossary sweep takes a subject and a grade. A protected word is matched per word,
against lessons, with no notion of which subject ordered it. So **a term or a spelling
shared by two subject-grades falls between every check**, and the sweep's clean report
is not wrong — it is answering a narrower question than the one I read it as.

Two instances, both found by accident rather than by any tool:

1. **The ǀXam name was spelt two ways in two subjects**, each under a live order that
   forbade correcting it — a forward slash in Grade 6 Social Sciences, the real click
   letter in Grade 4 Natural Sciences, whose lessons were already delivered. See
   [[onaantasbare-woorde-vir-die-taalnasiener]].
2. **`verwaarlosing` is defined in three subject-grades** — Grade 6 Life Skills
   (delivered), Grade 6 Social Sciences, and Grade 7 Life Orientation (another
   machine's work). I only looked because a legal research pass made me ask where else
   the word lives.

**Of those three, two are fine and one is not, and the difference is instructive.**
The Grade 6 Life Skills entry is about an *animal* — a different referent with an
identical shape, and repetition across subjects is good, so it stands. The Grade 7
entry builds a **means test** into the definition: neglect is when the adult *has
enough to give* and does not give it. The Children's Act has no such element — neglect
is "a failure in the exercise of parental responsibilities", full stop — so that
wording would tell a neglected child whose carer is poor that her case does not count,
and it fails on a failure that costs no money at all, like not taking her to a clinic.
It reads like an attempt to carry "poverty alone is not neglect" inside the definition
instead of beside it, which is how Grade 6 does it correctly.

**How to apply:**

* **Before calling a term settled, ask which OTHER subject-grades use it** — by
  searching every subject's drafts, not by running the sweep, which cannot see them.
* **A term that crosses subjects needs a referent check, not just a wording check.**
  Same word, different thing (animal vs child) is legitimate; same word, same thing,
  different test is drift.
* **A definition that smuggles a policy carve-out into its own sentence is the shape
  to distrust.** Grade 6 states the carve-out as its own sentence and stays true;
  Grade 7 folds it into the definition and becomes false. Related:
  [[n-begrip-word-alleen-gelees]].
* **Do not fix another machine's lesson** — [[drie-rekenaars-werk-parallel]]. Flag it
  and say which lesson, which word, and why the wording is narrower than the law.

---
name: geen-vrae-in-lesse-nie
description: "Lessons carry no retrieval questions from 2026-08-21. Already done in the standard, prompts and tooling — the four older lessons keep theirs."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8f79bbfb-d2d6-48c5-804a-7410b16958f5
  modified: 2026-08-20T22:10:38.161Z
---

Drico, 2026-08-21: "i told the team to ignore the questions. ALso something i want you to take out
of future lessons your team creates please." Then, clarifying an instruction I had misread as
"change nothing": "no you can change the instructions, i just meant to say dont apply that rule to
the lessons that your team has already created (or the one in fact check now)."

**The rule: lessons have no `vraag` blocks.** Study text, lists, glossary entries, and at most one
intuition block.

**This is already implemented — do not redo it.** Changed on 2026-08-21: the standard's content
tiers and schema example, the writer prompt (now `skrywer-v1.3`), the coverage-checker prompt (now
`dekkingsnasiener-v1.4`), both agent wrappers, the schema reference, the setup notes, `gate.py`
(the warning on absent questions is gone, and it does not nag about their presence either), and the
worked example lesson the writer reads, which had three questions teaching the wrong pattern.

`vraag` **stays a valid block type** so the four existing lessons still gate and validate. Verified
after the change: all four pass, their reports still validate, and the reference lesson still
measures 381 words at 11.7 words per sentence and 1.34 syllables per word, unchanged.

**Why he decided it:** the layout team was told to ignore the questions, so they never reach a
learner. The published page for Gr 4 NWT lesson 1 contains no question marks at all.

**Not retro-applied.** Living things 1 and 2, the plant lesson and the shelter lesson keep their
questions. His explicit instruction.

**The one real loss, now written into the standard, the writer prompt and the coverage prompt so it
is not forgotten:** a question was sometimes the only place a lesson gave the *evidence* for a
claim. A Gr 4 question set out dry yeast in warm sugar water going full of bubbles, while the study
text only said yeast "wakes up". Where the observable proof of an assertion lived only in a
question, **it now belongs in the study text.** The coverage checker was given the inverse rule: if
a requirement wants a learner to be able to tell that something is true and the study text asserts
it with nothing observable to go on, that is a genuine partial-coverage finding.
Related: [[teks-loop-parallel-met-n-video]], [[wanneer-vra-en-wanneer-doen]]

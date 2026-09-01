---
name: lysblokke-het-nooit-by-die-taalnasiener-uitgekom-nie
description: taalnasien.py read only a block's `teks`, and a list block keeps its lines in `items`. Every list block in every lesson was silently dropped from the block sent to the outside Afrikaans checker, and from the protection filter with it. Fixed.
metadata:
  type: project
---

`taalnasien.py` builds the block pasted into the outside Afrikaans checker. Its
`lesteks()` read `b["teks"]` — and a `lys` block has no `teks` at all; its lines
live in `items`. So **every list block in every lesson was dropped**, silently:
seventeen of them across Gr 4 NWT, Maths and Social Sciences, in fifteen lessons.

**Two consequences, and the second is worse than the first.**

1. That Afrikaans was never checked. Lessons have already been through the
   outside checker — that is where the direct-translation errors were found — so
   their list blocks came back unexamined and nobody could tell, because a
   missing block looks exactly like a block with nothing wrong in it.
2. `beskermde_woorde()` decides what to protect by asking whether the word
   appears in `lesteks()`. A protected wording living only in a list was
   therefore handed over **unprotected** — the precise failure the whole
   protected-words file exists to prevent.

The block that surfaced it carries a whole assessed requirement: where noise
comes from at home, at school and in the community, which is half of lesson 25's
only assessment guideline.

**How it was found:** not by looking for it. A coverage checker mentioned in
passing that one word was still on a lesson's word list although only the plural
was in use — and the plural turned out to be in a list block, which a search of
`teks` could not see. The bug was in my own search before it was in the tool.

**How to apply:** when a function claims to return "everything" of something,
check it against the actual shapes in the data rather than the shape you had in
mind. One survey of every block shape in the repository would have found this in
a minute, and it is the same survey that should precede any tool that reads
lessons. Related: [[n-skoon-toets-is-so-wyd-soos-sy-omvang]] — a filter that
silently sees less than it claims reads exactly like a filter that found nothing
wrong.

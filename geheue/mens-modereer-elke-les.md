---
name: mens-modereer-elke-les
description: "Every lesson gets human moderation downstream for small readability things — so don't build automated checks for that class."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f79bbfb-d2d6-48c5-804a-7410b16958f5
  modified: 2026-08-21T08:05:18.100Z
---

Drico, 2026-08-21: "The plan is ultimatly to give all the lessons you produce to a human to
moderate (for small things such as that). So i know we will catch things like that."

**What prompted it.** He read a reading copy and stopped on `heet` in "So 'n stukkie stam met 'n
paar blare aan heet 'n steggie", asking whether it was a typo for `het`. It is not — `heet` as a
verb means *is called* and is correct — but the word a nine-year-old owns is the adjective `heet` =
**hot**, so a learner meets a temperature as the first available reading. Separately I had found a
real orthography error in the same paragraph: "Na 'n paar weke" needs the temporal accent, `Ná`.
Two different failure classes in one paragraph, neither catchable by anything in the pipeline.

**The consequence: do not build automated checks for readability.** I had proposed two things and
both are now retired or downgraded — a targeted check for Afrikaans pairs differing only by an
accent (`na`/`ná`) is not worth adding, and installing the Afrikaans hunspell dictionary drops from
worthwhile to optional. A moderator catches both classes better than a rule would, and neither of
the two words above would have been caught by a spellchecker anyway, since both exist.

**The division of labour, and the part worth defending:**

- **The pipeline owns truth, coverage and reading level.** These need sourced searching and
  measurement. A moderator would sail straight past "a plant in a dark cupboard stays small"
  (it stretches), orchid seeds having no stored food, or plastic tracing back to living things —
  all of which read perfectly well and are all false or trap-laden.
- **The moderator owns readability.** Odd word choices, missing accents, clumsy sentences. Exactly
  what Drico caught by reading.

**The risk to watch:** the assumption drifting, so that a moderator signs a lesson off feeling they
have checked it, when what they have checked is how it reads. Worth saying out loud whenever the
moderation step is set up or handed to someone new.

**Still worth doing regardless:** the house word list in
`skills/wolkskool-inhoudstandaard/references/woordkeuse.md` grows one line per flagged word, so a
word a moderator flags once never recurs across four hundred lessons. `heet` was added on
2026-08-21. Related: [[rapporteer-in-gewone-taal]], [[teks-loop-parallel-met-n-video]]

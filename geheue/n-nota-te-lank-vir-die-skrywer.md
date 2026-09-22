---
name: n-nota-te-lank-vir-die-skrywer
description: A lesson whose provenance note passes ~50KB on one line can't be read by the writer; give it a working copy and merge its blocks back by script.
metadata:
  type: feedback
---

On 21 September 2026 the Gr 5 diarrhoea lesson (GO 8) had a 54KB provenance note on one line. The writer's reader refused the file, and the writer correctly refused to overwrite a note it could not read.

What worked: copy the lesson to the scratchpad with the note cut down to its last ~6000 characters. The writer then writes ONLY the changed blocks plus a note entry to a separate file, `hersiening.json` (`{"blokke": {index: block}, "nota_byvoeging": text}`). A script asserts that the copy's blocks still equal the real file's, swaps in the changed blocks, and appends the note entry. The wording stays the writer's.

**Why:** a hand edit breaks the rule against writing content by hand; a whole-file rewrite loses the history.
**How to apply:** check note sizes with a script when a lesson has had more than about 12 revisions. See [[moenie-self-inhoud-skryf-nie]].

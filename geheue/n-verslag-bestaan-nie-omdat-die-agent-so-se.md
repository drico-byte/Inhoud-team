---
name: n-verslag-bestaan-nie-omdat-die-agent-so-se
description: Build checker paths by copying the runner's own printed paths; and a missing report is not proof the checker misplaced it.
metadata:
  type: feedback
---

Twice, a checker's report landed somewhere the runner does not look — once in a
review folder, once in a logs folder — because I typed the paths into the brief
from my own head instead of copying the ones the runner prints for every next
step. Every time I have typed them, at least one has been wrong.

**How to apply:** run the runner first, copy its printed `in` and `out` paths into
the brief verbatim, and tell the checker to confirm the file exists on that path
after writing.

**What this note used to say, and why it was wrong.** I first wrote it blaming a
third incident on the same cause: two coverage reports for one lesson had
vanished, and I assumed my paths were at fault again. They were not. The runner
was deleting them — see [[staat-wat-nie-gestoor-word-nie]]. A missing report is
not evidence that a checker misplaced it; check the archive folder and the
runner's own bookkeeping before rewriting a brief or re-running an agent.

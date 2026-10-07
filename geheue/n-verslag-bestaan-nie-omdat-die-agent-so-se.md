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

## A checker can report a clean verdict and leave an unparseable file

**4 October 2026.** A fact check handed back a full report — verdict, item
counts, three findings with sources — and the file it wrote was **invalid JSON**.
Four double quotes sat unescaped inside string values, because it quoted terms
verbatim ("Cape Coloured", "people who are different"). Nothing in its own
hand-back could have told me; it believed it had written the report.

**It was repairable, and worth repairing.** The whole 379-line report was there.
Escaping the four quotes recovered it, and the repository's own
`verdict_check.py` then passed it SOUND. Re-running would have cost another hour
of web checking for a report that already existed.

**Its prose count was also wrong**: it said 49 items where the file holds 52. The
finding count — three — was right. **The file is the artefact; the hand-back is a
summary of it.**

**How to apply:** after any checker hands back, `json.load` its report before
acting on it or counting it as done. If it fails, look before re-running — a
stray quote inside quoted source material is the likely cause, the content is
usually intact, and the repair is mechanical. Escape the quote **before** the
offset the parser reports: it ends the string early and then trips on the next
character.

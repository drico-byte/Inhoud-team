---
name: lesse-gaan-altyd-na-lees
description: "Drico, 22 Sep 2026: every finished lesson's PDF goes to lees/ as well, without being asked; Voltooide lesse is Lampies' delivery folder and does not replace it."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-09-22T20:16:53.008Z
---

**Drico, 22 September 2026: "I want my things to always be in the lees folder. Thats how I have
always done it."** He asked where the Grade 6 lessons were, because sign-off now copies PDFs to
`Voltooide lesse/Graad N/<Vak>/<Subonderwerp>/` (Lampies, 21 Sep) and nothing had reached `lees/`.

**Why:** `lees/` is his own outbox - he moves PDFs from there to the outside Afrikaans checker and
to the HTML team (see [[lees-is-n-uitbak-nie-n-argief-nie]]). A folder he did not ask for does not
replace the one he works from, and he should not have to ask each time.

**How to apply:** when a subject-grade is signed off, copy every approved PDF to
`lees/gr<N>/<vak-slug>/<subonderwerp>-les-<n>.pdf` and write `BESKERMDE-WOORDE.md` beside them
(the protected words that actually occur in those lessons, with the reason and where each one
appears - the generator lives in the scratchpad, `gr6_beskermde.py`). `lees/` is gitignored, so it
never travels with the repository. Both copies exist on purpose: `Voltooide lesse` for Lampies,
`lees/` for Drico.

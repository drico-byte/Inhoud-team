---
name: die-leeskopie-het-ons-interne-notas-uitgestuur
description: "The readable-copy script appended our review appendix — fact tallies, coverage verdicts, checker reasoning — to APPROVED lessons, so it went to the outside language checker and the HTML team. Its own docstring said it should not."
metadata:
  type: project
---

Found 23 September 2026 while replacing seven language-checked PDFs. My replacements carried
a **"Nasienbevindings"** section the originals seemed not to have — and on inspection the
originals carried it too. All 63 lessons in Drico's checked folder have it.

**The bug:** `verslae_langs` in `bin/leeskopie.py` documents itself as *"Present for a draft
under review, absent for an approved lesson."* That was never implemented — `een()` attached
the reports whenever `.dekking.json` / `.feite.json` happened to sit beside the lesson, which
for an approved lesson is always. Fixed by keying on `status == "goedgekeur"`.

**Why it matters beyond tidiness.** The appendix carries the checkers' *reasoning* — what was
contradicted, what a checker argued, what was left unrequested. That reached the outside
Afrikaans checker and the HTML team, neither of whom should be reading our internal
deliberation, and on 23 September it reached them describing an intuition block that had
just been deleted.

**How it was caught, and the lesson in that:** a word count that moved the wrong way. Removing
a 159-word block made a lesson *longer* — 804 to 875 words. I nearly wrote that off. Related:
[[n-skrip-wat-parse-is-nie-n-skrip-wat-werk-nie]] — a docstring stating intent is not the
intent being implemented, and nothing tested this one.

**Still outstanding:** the other 56 PDFs in that folder still carry the appendix and can be
reprinted whenever Drico wants.

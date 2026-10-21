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

## The appendix was fixed. The CAPS header was not, and it can carry a withdrawn claim

**8 October 2026**, established by reading `bin/leeskopie.py` rather than inferring it.

* **The review appendix is correctly gated**: `verslae = {} if les.get("status") == "goedgekeur" else verslae_langs(pad)`. An approved lesson's PDF carries no findings section. That is the repair this note records, and it holds.
* **The header is not gated at all.** It emits `CAPS: {les.get('kaps_punt')}` on **every** PDF, draft or approved. So whatever that field contains goes out with every reading copy, to the Afrikaans checker and the HTML team.

**Why that matters, concretely.** `kaps_punt` is the record of what the curriculum asks and a standing note forbids changing it — correctly. But in Grade 6 Mapungubwe it contains CAPS's own printed **"eerste staat in Suider-Afrika"** and **"Eerste klip-ommuurde paleis"**, and both of those claims have since been **withdrawn from our text**: the first replaced by a bounded kingdom claim after the reasons for it were found false, the second dropped entirely after its attribution collapsed.

So the checker reads a header asserting *first state* immediately above a text saying *kingdom*, and **the obvious thing for them to do is make the text match the header.** The header looks more authoritative than the body.

**This is not a learner leak** — the footer says in terms that the PDF is for review and that the learner's page is laid out separately by the HTML team — and the line is explicitly labelled `CAPS:`, so it reads as a citation rather than as our claim. Which is why the answer is not to strip the field.

**The answer is to say it in the protected-word reason**: the header cites the curriculum's wording, it is not our claim, where the lesson states the claim it uses the decided word, and the mismatch is deliberate. A protection that does not mention the header is arguing with a document the checker is holding.

**The general lesson.** When a ruling withdraws a claim, ask **which fields still carry its old form and which of those are rendered.** A field that is correctly frozen as a record of what someone else said can still be printed next to our corrected text, and the gating of one section of a template tells you nothing about the gating of another.

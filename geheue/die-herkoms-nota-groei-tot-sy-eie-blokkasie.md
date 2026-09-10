---
name: die-herkoms-nota-groei-tot-sy-eie-blokkasie
description: "A draft's provenance note only ever grows, fastest on the most-revised lessons; at 55 KB on one line it blocked a writer completely."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-09-10T20:48:48.328Z
---

10 September 2026. A writer sent to make three one-line corrections to Grade 5
`dieregeraamtes` lesson 1 **stopped and reported instead**. The draft's
`herkoms.nota` had reached **55 KB on a single line** — more than a reading tool
returns in one call. It could read every study block and every glossary entry,
and not that line at all. Its only writing tool replaces a whole file, so
appending three sentences meant rewriting the lesson from what it could see and
silently deleting the record. It refused. Correct: that is a trade, not a
correction.

**Why this will keep happening:** every revision appends, and the note grows
fastest on the lessons revised most — exactly the ones most likely to be revised
again. Ten Grade 5 drafts were over 20 KB, two over 50 KB.

**How to apply:** run `bin/herkomsargief.py --vak "<subject>" --graad <n>` (add
`--skryf` to act). It writes the whole note to `<lesson>.herkoms.md` beside the
lesson, verifies it verbatim **before** touching the draft, and leaves the draft
the copyright opening, a pointer, and the newest rounds. Four of the biggest
notes had no blank lines; they split on SHOUTED headings after a full stop.

**Do not solve this by asking writers to write less.** The note is what makes a
decision survive to the next revision, and it has saved several corrections.
Related: [[n-spek-so-lywig-dat-dit-nie-geskryf-kan-word-nie]],
[[n-agent-wat-halfpad-sterf-laat-die-inhoud-sonder-sy-rekord]],
[[die-herkoms-nota-lek-die-spek-na-die-feitenasiener]].

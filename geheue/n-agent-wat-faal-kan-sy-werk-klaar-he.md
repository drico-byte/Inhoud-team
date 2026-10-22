---
name: n-agent-wat-faal-kan-sy-werk-klaar-he
description: An agent the harness reports as failed may already have written its file; check the file before re-running, or you overwrite good work.
metadata:
  type: feedback
---

A subagent that dies on an API error (usage limit, rate limit) is reported to me as
**failed**, with its last partial thought as the "result". That report says nothing
about whether it wrote its output file. On 22 September 2026 a usage limit killed
fourteen agents at once; four of them — three lesson cuts and one factual fix — had
already written complete, correct files, provenance note and all. Their "result"
lines read like they had barely started ("Now the spec and the reference lesson.").

**Why:** the failure is recorded when the agent's turn ends, not when its work lands.
A writer's last tool call is the file write, so the window between "wrote the file"
and "died" is exactly where these fall.

**How to apply:** after any batch failure, MEASURE THE FILES before re-dispatching
anything. Re-running a writer over work that already landed is not neutral — it
throws away a good revision and starts a fresh round on text that was already right.
Two traps in checking:

* A substring test for the old wording hits the **provenance note**, which quotes
  every withdrawn form on purpose. Test the block text, not the whole file.
* A test for the corrected wording can match the old sentence too. "26 sekondes"
  matched both the false claim and its fix; only "in 1902" separated them.

The honest check is to read the blocks, or to re-gate and compare the word count.
See [[n-verslag-bestaan-nie-omdat-die-agent-so-se]] for the opposite error — believing
an agent that says a file exists.

## 13-14 October 2026: the weekly token limit killed three writers; two had finished

All three died inside the same minute on an HTTP 429 — "You've hit your weekly limit". Their
last reported words were "Now the reference lesson, as instructed", "Now I'll write the
revised lesson" and "Now I have what I need. Writing the revision." Two of those three had
in fact written complete, correct revisions; the first had not written anything.

**The test that works, and it is two things together:**

* `status` — a writer sets a revised draft back to `konsep`. Still `gated` means it never
  wrote.
* **the content hash against the state file** — `hardloop.konsep_hash(draft)` compared with
  `konsep_hash` in the lesson's `.staat.json`. Matching means the content is exactly what
  the last gate measured, so nothing was written. Differing means it was.

Both agreed on all three lessons, and both were necessary: status alone would not tell me
whether a `konsep` draft had been half-written.

**A test that does NOT work.** I also checked whether the provenance note mentioned
yesterday's date, expecting a killed agent to have written the lesson without its record
([[n-agent-wat-halfpad-sterf-laat-die-inhoud-sonder-sy-rekord]]). It reported one note as
stale. **The note was fine — I searched for "Oktober" and the note writes "OKTOBER".** A
case-sensitive string test on Afrikaans prose that the house writes in capitals for emphasis
will give false alarms. Compare content, not spelling, or fold case.

**How to apply:** after any agent dies, check status AND the content hash before re-briefing,
and read the actual blocks. Re-running a writer over work it already finished is how a good
revision gets overwritten by a worse one.

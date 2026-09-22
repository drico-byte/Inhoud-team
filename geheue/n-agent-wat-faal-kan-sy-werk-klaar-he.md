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

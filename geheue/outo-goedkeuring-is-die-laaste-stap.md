---
name: outo-goedkeuring-is-die-laaste-stap
description: "Sign every cleared lesson off automatically as the last step of its run — Drico reviews afterwards, so never stop and ask."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-08-28T13:22:59.329Z
---

Drico, 2026-08-28: "just auto sign off every lesson your team creates, since I give it a final look
after the langauge checker is done."

**Why.** Approval here gates nothing a person does later. The runner already stopped asking for a
typed confirmation on 2026-08-21, on his instruction, because every lesson is edited by hand
downstream and a signature at this point duplicated the later one. Approval is a status on the file,
not a move to a second place, so signing off costs nothing and un-signing costs nothing either.

**How to apply.** When a lesson comes out clear — gate PASS and both checkers GOEDGEKEUR — run the
approval step in the same breath as the run that cleared it. Do not report "waiting on sign-off" and
wait for him. Report that it is approved and what it says.

**What still stops.** Auto sign-off only ever fires on a lesson that cleared everything. An
escalation, a spent revision budget, or a checker sending the draft back still stops the lesson and
still needs him — approving is not a way past those.

**The language checker is real, and it is outside this repository.** Asked on 2026-08-28 whether he
meant a person or a pipeline step, he confirmed he runs a separate language checker of his own. So
there is nothing to build here and no step in this pipeline to wait for — do not raise it again. The
order is: pipeline signs off → his language checker → his final look.

**The thing to say out loud whenever this is set up or handed to someone new** (from
[[mens-modereer-elke-les]]): his final look owns *readability* — odd words, missing accents, clumsy
sentences. It does not own truth, coverage or reading level, and a reader sails straight past a
false claim that reads perfectly. Auto sign-off does not move that boundary, because it only fires
after the checkers that do own truth have passed. The risk is the feeling of having checked a
lesson by having read it.

Related: [[wanneer-vra-en-wanneer-doen]], [[voor-jy-stop-se-wat-loop]], [[rapporteer-in-gewone-taal]]

---
name: eli10-blok-is-afgeskaf
description: "Drico, 23 Sep 2026: the eli10 intuition block is abolished. No lesson may carry one; the gate fails any that does. Nothing of a removed block moves into the study text."
metadata:
  type: project
---

**Drico, 23 September 2026: "we need to stop with the ELI10 blocks in the lessons."**
He reversed his own first answer mid-decision — he initially said to move what mattered
into the study text, then after reading two blocks said **"we really can just strip them
without transferring its content."** That reversal is the ruling: the study text is left
word for word as it is.

**Why it was safe, and check this way if it is ever reopened.** All seventeen lessons that
carried a block were tested against their own coverage reports first. **27 requirements
cited a block in their evidence; every one was also carried by a study block. Not one
requirement lived only inside a block.** The case I had nominated as the strongest argument
for keeping them went against me: the Grade 4 sound lesson's study text already had a block
titled *"Niks vlieg van die trom af na jou toe nie"* carrying the whole mechanism, and the
intuition block merely restated it with a row of children. I told Drico it was the best case
for keeping them and it was the clearest case for stripping.

**What it cost, across all seventeen:** two ideas, neither a requirement — why a layer of
air counts as thin when it looks endless, and that we feel nothing of the Earth's movement.

**Where the ruling now lives**, because a decision only held in one place gets undone:
the content standard, the gate (a hard FAIL, which is the real backstop), new prompt
versions for all four agents, and an `eli10_afgeskaf` field on each of the **60 specs** that
still asked for one. That last one is the important bit — see
[[die-korrigeerde-opdrag-bly-in-die-veld-staan]]. Stripping 17 lessons took minutes;
**194 spec fields were still ordering the block**, and any revision of any of those lessons
would have written a fresh one and had coverage bless it.

**Do not hand this to a writer as "remove the block".** A scripted whole-block deletion
changes no wording and cannot disturb a neighbour; a writer given the whole lesson has
repeatedly tidied something it was not asked to touch. See [[moenie-self-inhoud-skryf-nie]]
— that rule is about *wording*, and a structural deletion is not wording. Re-gate and re-run
coverage afterwards; facts do not need re-running, because removing claims cannot make the
remaining ones false.

Related: [[n-regstelling-ontwrig-sy-bure]], [[elke-sin-waar-die-prentjie-vals]] — three of
the worst errors this pipeline ever produced were inside these blocks, and they were never
fact-checked as hard as study text because scaffolding never counted against the budget.

**29 September 2026 — the standard itself had lagged its own ruling for six days.** The
abolition is stated near the top of the content standard; four places *below* it still gave
live orders. The schema example still contained a block, which is the most-copied thing in
the whole document, and a bolded order — "ELI10 must contain an actual comparison... Every
ELI10 block names its concept in `vir`" — sat 430 lines below the rule that withdrew it.
By the bottom-up test the later imperative wins, because an agent reads a document as prose.

Three scripts too: the gate appended "zero or one per lesson is the guide" as a note on
every lesson; the spec checker warned a planner that a sub-topic "usually has at least one
concept that needs an ELI10 layer", which directly contradicted the current planner prompt;
and the verdict checker told a reader a flagged concept was "not checked for an eli10 block".

**The sweep that closed this was never run: the one that reads the standard itself.** The
prompts, the reference files and all 236 lessons were already clean on day one — the effort
went to the specs, which was right, and the document every agent reads was assumed correct
because the ruling had been written *into* it. Writing a ruling into a document is not the
same as sweeping that document for what the ruling withdrew. See
[[die-korrigeerde-opdrag-bly-in-die-veld-staan]] and [[n-teruggetrekte-beslissing-bly-in-hoofletters-staan]].

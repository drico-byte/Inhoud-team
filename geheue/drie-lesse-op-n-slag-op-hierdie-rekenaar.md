---
name: drie-lesse-op-n-slag-op-hierdie-rekenaar
description: "Drico, 29 Sep 2026: on THIS account, dispatch at most three lesson writers at a time — it has far fewer tokens than the other machines."
metadata:
  type: feedback
---

**Drico, 29 September 2026: "Do 3 lessons max at a time."**

**Why:** this account has far less token budget than the other two machines — his words,
*"its only for this account since it has way less tokens than the other."* The agent
concurrency cap of 20 is a harness limit, not a budget, and a writer is an expensive
agent: the Grade 4 Geography planners each burned 200–340k tokens. Fanning out ten
writers would empty the account in one pass.

**How to apply:** when dispatching lesson writers from this machine, run **at most three
concurrently**, then the next three. This is about the WRITING step specifically — it is
where the volume is — but treat it as the sensible ceiling for any expensive fan-out here
unless Drico says otherwise. It does not bind the other machines.

Do not read this as a reason to skip steps to save tokens. The pipeline still runs in
full: gate, both checkers, repair, sign-off, PDF — see
[[loop-die-hele-proses-tot-by-goedkeuring]]. Three at a time is a rate, not a discount.

Related: [[drie-rekenaars-werk-parallel]].

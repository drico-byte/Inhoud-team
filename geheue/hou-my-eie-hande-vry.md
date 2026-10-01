---
name: hou-my-eie-hande-vry
description: Lampies must be able to reach me at any moment. Push the long work to subagents and keep my own tool runs short.
metadata:
  node_type: memory
  type: feedback
---

**Lampies, 1 October 2026:** *"please make sure i can always talk to you.
Therefore makes ure that subagents are doing the work. Sometimes i find you busy
for MULTIPLE minutes"*

**Why:** he works alongside me and asks short questions as they occur to him. A
long stretch of my own tool calls makes him wait, and a question he asks mid-turn
reaches me late. Responsiveness is worth more to him than my doing a job myself.

**What was actually eating the minutes**, because it was not the agents: my own
specification surgery. Reading a 6 KB requirement field, writing a careful rewrite
script, running it, re-reading to verify. Three or four of those back to back is
ten minutes where he cannot get a word in.

**How to apply.** Delegate the long mechanical work, not just the content work:

- **Specification edits at source** go to a `general-purpose` agent with a precise
  brief — name the file and field, state the distinction that governs each decision
  (what is an order versus what is provenance), list the exact strings to change,
  say what must be asserted afterwards, and tell it to run the refresh, the sweep
  and the gate and report the numbers verbatim. It must never touch a draft or
  anything under `spek/`.
- Tell it to write its Python to a temp file rather than a shell heredoc — escapes
  get mangled here, and I have lost two edits that way.
- Keep **my** turns to a few calls: decide, dispatch, reply. The judgement of what
  to fix and whether a finding is real stays mine; the typing does not.
- When several things land at once, answer him first and dispatch second.

Related: [[drie-lesse-op-n-slag-op-hierdie-rekenaar]] (the rate limit is on lessons
in flight, and delegating does not raise it — one agent on the lesson I am already
holding is free), [[net-wat-my-oe-nodig-het]], [[voor-jy-stop-se-wat-loop]].

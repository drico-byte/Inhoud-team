---
name: n-verslag-bestaan-nie-omdat-die-agent-so-se
description: A checker saying it approved is not evidence its report was written; verify the file exists, and build the paths by copying the runner's own printed paths.
metadata:
  type: feedback
---

A checker agent reported a full, detailed approval — and the report file was never
there. The lesson could not be approved, and the runner just asked for the same
checker again as if nothing had happened. Nothing in the report told me; only
listing the folder did.

Two separate faults, and the second caused the first.

**I built the paths by hand.** I pointed the checker at paths under the memory
folder instead of the repo. The agent noticed, corrected the input paths itself,
read the right files, and reached a sound verdict — and then its write went
nowhere. So the agent silently rescued the reading and not the writing, which is
the worst of the two outcomes because the report reads as complete.

**Why:** the runner already prints the exact `in` and `out` paths for every next
step. Every time I have typed a checker's paths from my own head instead, at least
one has been wrong — the report has landed in a `nasien/` folder, a `verslae/`
folder, and now nowhere at all. My hand is the only part of this that keeps
failing.

**How to apply:** run the runner first and copy its printed paths into the brief
verbatim. Tell the checker to confirm the file exists on that path after writing.
Then, before believing a verdict, list the folder — the file's presence is the
record, not the agent's summary. Same discipline as
[[n-regstelling-ontwrig-sy-bure]]: check what the step actually left behind, not
whether it said it succeeded.

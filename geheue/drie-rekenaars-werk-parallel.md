---
name: drie-rekenaars-werk-parallel
description: "Drico, 23 Sep 2026: three PCs are creating content in parallel. Open lessons outside my own subject are probably someone else's, not idle work — and a repo-wide sweep touches their files."
metadata:
  type: project
---

**Drico, 23 September 2026: "remember that there are other pcs also creating content.
There are 3 now."**

He said it after I gave a progress report that listed every open lesson in the
repository — including eleven Grade 4 science ones — as though they were outstanding
work waiting to be picked up. They were not mine. What he actually wanted from
"progress report" was the short answer: **what is left to do in the work I am on.**
For that report it was two lines — Grade 4 Geography not started, one Grade 4 History
lesson in its final check.

**How to apply.**

*Reporting.* Report on the subject-grade I am working, not on the repository. An open
lesson elsewhere is probably someone else's in flight. If a whole-repository number is
genuinely useful, say which part is mine. See [[net-wat-my-oe-nodig-het]].

*Sweeps.* A repository-wide edit reaches into their files. On 23 September the eli10
removal touched Grade 4 and Grade 5 science, and the spelling-list sweep touched 67
lessons across every subject and grade. Every push merged cleanly and nothing was
lost, but I did not know at the time that anyone else was in those files. Before a
sweep that leaves my own subject: pull first, keep it to one mechanical change that a
merge can reconcile, push straight away rather than sitting on it, and say plainly in
the commit what was touched beyond my own work.

*Pulling.* `git pull --no-rebase` before every push is already the habit and it is what
kept this clean — the shared run logs are append-only and union-merge. Keep it.

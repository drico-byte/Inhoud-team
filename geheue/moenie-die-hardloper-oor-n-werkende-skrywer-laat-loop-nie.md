---
name: moenie-die-hardloper-oor-n-werkende-skrywer-laat-loop-nie
description: I ran the runner on a lesson while its writer was mid-revision. It gated a draft that was about to be replaced, and the writer found the status changed between its own read and write. Run the runner on a lesson only when no agent is holding it.
metadata:
  type: feedback
---

While the writer was revising lesson 23 I ran the runner on the same lesson, to
check something unrelated. The runner did what it always does: it gated the file
it found and stamped `status: gated`. The writer then went to save its revision,
saw the status had changed under it, said so, and correctly set it back to
draft — "iemand of iets het dit tussen my lees en my skryf verander".

**What it could have cost.** The gate measured a draft that was seconds from
being replaced, so the numbers described nothing. Worse, a spec change in the
same run archives the coverage and fact reports; a run at the wrong moment
therefore throws away good reports for a draft that no longer exists. A writer
that did not check the status would simply have overwritten the stamp, and the
lesson would have carried a gate result belonging to different text.

**How to apply:** before running `hardloop.py` on a lesson, ask whether an agent
is holding that lesson right now. Run it on a different lesson, or wait for the
notification. This also rules out the tempting habit of running the runner
across several lessons as a smoke test — see
[[staat-wat-nie-gestoor-word-nie]], where exactly that archived two delivered
lessons' coverage reports. They were recoverable from `logs/verslae/`, which is
worth knowing: the archive works, and a missing report is not a lost one.

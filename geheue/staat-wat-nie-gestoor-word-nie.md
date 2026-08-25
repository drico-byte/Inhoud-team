---
name: staat-wat-nie-gestoor-word-nie
description: A bookkeeping value assigned but never written to disk made the runner delete every coverage report forever; a lesson whose spec was ever edited could not be approved.
metadata:
  type: project
---

The runner deletes a coverage report when the specification entry has changed
since the report was written — correct, because coverage is judged against the
entry. It records the entry's fingerprint so it knows next time.

It recorded it in memory and never wrote it to disk. State reaches disk only when
an event is logged, and the run that reaches this point logs no event. So the new
fingerprint was forgotten on every run, the next run saw the same mismatch, and it
deleted the report the checker had just written.

**Why it stayed hidden:** the loop is invisible from the outside. The runner says
the checker still needs to run, which is exactly what it says when a checker
genuinely has not run. I read that as two agents failing to write their file, and
believed it the more readily because agents really had misplaced reports before —
so I re-ran the checker, then re-ran it again, then went looking for a filesystem
fault. Two full checker runs and a filesystem search went into a lesson that could
never have been approved. The archive folder held both reports the whole time,
with the right verdict in them.

Any lesson whose specification had ever been edited was caught by this — which,
given how often a checker's finding sends me back to the spec, is most of them.

**How to apply:** when a step insists on work that was already done, compare the
stored fingerprint against the thing it fingerprints before believing the step.
And when two agents in a row fail the same way, suspect the harness before the
agents. Same lesson as [[n-verslag-bestaan-nie-omdat-die-agent-so-se]] read from
the other side: there I trusted a report that did not exist, here I distrusted
reports that did.

---
name: n-plekhouer-verslag-lyk-soos-n-klaar-een
description: "Telling checkers to write their report early makes half-written reports that pass every freshness test; the state script must detect them, not the agent."
metadata:
  type: feedback
---

**5 October 2026.** After a network outage killed five checks mid-task, I added
"write your report early and update it as you go" to every fact brief, so an
interruption would cost a round rather than a whole check. It does that. It also
manufactures files that are indistinguishable from finished reports: valid JSON,
newer than the draft, a `verdict` field filled in.

Three agents then stalled *after* writing the skeleton and *before* doing any work. I
told Lampies their reports had landed. They were placeholders — `items` empty, summary
saying the check was still running and the file must not be used — so two lessons were
about to be filed as *having findings to act on* when neither had been checked at all.
A sweep found exactly those three and no others, so it was contained.

**Why this is worse than a missing report:** a missing report is visible. A placeholder
is invisible to the freshness test, to the verdict read, and to the state report that
tells me what still needs doing — and it reads as *work in progress on a real finding*,
which is the one state nobody re-examines.

**How to apply:** the guard goes in `verslagstand.py`, not in the brief, because it must
not depend on the agent that died being the one to clean up after itself. A report counts
as no report when `items` is an empty list, or when its summary carries a
work-in-progress marker. Keep the write-early instruction — with the guard in place it is
strictly better than losing a whole check. And when an agent dies, measuring that the
file EXISTS is not measuring that the check RAN: open it and look at `items`. Related:
[[n-verslag-bestaan-nie-omdat-die-agent-so-se]],
[[tel-die-verslae-voor-jy-se-dit-is-nagegaan]], [[n-agent-wat-faal-kan-sy-werk-klaar-he]].

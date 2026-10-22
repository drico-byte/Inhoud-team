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

**A report can validate as sound and still be mid-write, and the fingerprint is how you find out.** 14 October 2026, Mapungubwe lesson 4. I waited on the fact report file, and it arrived with 25 items, a full summary, every item carrying claim, status and sources, and the validator called it SOUND. I took the holding item fingerprint from it and wrote the acceptance record. Sign-off then refused: the agent had kept working after that point and expanded the item evidence, so the fingerprint had moved and nothing was accepted. The refusal is the mechanism working exactly as intended - the acceptance is bound to the item text, so it lapses the moment the evidence changes. **The rule: take a fingerprint only after the agent has handed back, never from a file that merely looks complete.** A validator checks internal consistency, not whether the writer has finished. See also [[n-agent-wat-faal-kan-sy-werk-klaar-he]] for the opposite error, and [[n-verslag-bestaan-nie-omdat-die-agent-so-se]].

**The runner reads a placeholder too, and escalates on it.** 15 October 2026, Gr 6 map skills 3, 5 and 6. I called `hardloop.py` for three lessons after a spec edit (the rule in [[roep-die-hardloper-na-n-spekwysiging]]) while their fact checkers were still running with write-early briefs. All three came back MENS_NODIG: the runner routed on the 2 KB skeleton reports and recorded an escalation. Nothing was archived, and `--hervat` cleared it once the real reports landed. **The rule: after a spec edit, call the runner for a lesson only when no checker for that lesson is running - otherwise wait for the checker and call it then.**

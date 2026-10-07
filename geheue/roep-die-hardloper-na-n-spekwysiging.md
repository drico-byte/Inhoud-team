---
name: roep-die-hardloper-na-n-spekwysiging
description: After a spec edit, call the runner for that lesson BEFORE briefing coverage, or the runner retires the fresh report as stale at sign-off.
metadata:
  type: feedback
---

**7 October 2026, Gr 4 farming 4.** I fixed a spec field, refreshed the extracts and briefed
a coverage re-check straight away. It came back GOEDGEKEUR against the fixed spec. At
`--keur-goed` the runner compared the spec entry's hash with the one it last recorded — the
OLD spec, since I had not called it in between — archived the clean report as
`dekking-verouderd` and demanded coverage again.

**Why:** the runner records the spec hash only when it runs. A spec edit made between two
runner calls is invisible to it until the next call, and that call is often the sign-off.

**How to apply:** after any spec edit, run `hardloop.py` once for every affected lesson
before briefing a checker. If it has already happened and the report was written against the
current spec, copying `s<N>-dekking-verouderd.json` back to `les-N.dekking.json` is right —
the runner's own comment says so — then sign off. Same family as
[[moenie-die-hardloper-vra-oor-n-nagesiende-les-nie]] and [[staat-wat-nie-gestoor-word-nie]].

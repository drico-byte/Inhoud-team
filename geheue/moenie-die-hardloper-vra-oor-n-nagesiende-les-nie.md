---
name: moenie-die-hardloper-vra-oor-n-nagesiende-les-nie
description: Running hardloop.py on a lesson whose checker reports already exist archives them as outdated and demands the checks again.
metadata:
  type: project
---

2 September 2026. Coverage and facts had both come back clean on Grade 4
Lewensvaardighede lesson 6. I ran `bin/hardloop.py` on that lesson to ask what
the next step was. It wrote a fresh state file, moved both reports into the log
tree renamed `s1-dekking-verouderd.json` / `s1-feite-verouderd.json`, and then
reported `WAG_VIR_NASIENERS` — asking for the two checks that had just finished.

Nothing was lost: the archived copies restore straight back over the originals
and both still read GOEDGEKEUR. But if I had believed the runner instead of
looking, I would have spent two more checker runs reproducing work already done.

**Why:** the state file is written by the runner, and a report that lands before
that file exists cannot be matched to a draft hash. The runner's safe default is
to treat it as stale. So the ordinary sequence — launch checkers, then ask the
runner what is next — is exactly the sequence that trips it.

**How to apply:** ask the runner for the paths **before** launching the checkers,
then do not run it again on that lesson until the reports have been acted on. If
it ever demands work that is already done, look in
`logs/verslae/<...>/les-N/` for `*-verouderd.json` before re-running anything.
Same family as [[staat-wat-nie-gestoor-word-nie]] and
[[moenie-die-hardloper-oor-n-werkende-skrywer-laat-loop-nie]]: suspect the
harness before the agents.

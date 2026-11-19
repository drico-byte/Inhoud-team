---
name: spek-wysiging-registreer-voor-dekking
description: "After editing a spec, call the runner (no flags) on the lesson BEFORE briefing coverage, or sign-off archives the fresh report as stale."
metadata:
  node_type: memory
  type: feedback
  originSessionId: deedaf1a-4546-4aae-aaae-33d049877c50
  modified: 2026-11-18T14:31:33.339Z
---

After a spec edit, refreshing the extracts is not enough. The runner records the spec entry's hash in the lesson's state only when it is called, and at sign-off it compares that against the current spec. A coverage report written before the runner has seen the new spec gets archived as `dekking-verouderd`, and the check has to be run again.

**Why:** on 18 Nov 2026 three Grade 6 climate coverage reports were thrown away this way. I had edited the spec, refreshed the extracts and briefed coverage straight away. The runner only saw the new spec hash at `--keur-goed`.

**How to apply:** spec edit → `vernuwe-uittreksels.py` → a plain `hardloop.py` call per affected lesson → only then brief coverage. Related: [[n-verslag-in-die-logboom-kan-verouderd-wees]], [[staat-wat-nie-gestoor-word-nie]]

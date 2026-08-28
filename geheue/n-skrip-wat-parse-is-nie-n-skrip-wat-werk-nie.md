---
name: n-skrip-wat-parse-is-nie-n-skrip-wat-werk-nie
description: I shipped an installer that parsed cleanly and had six bugs, every one of which only appeared when it was actually run.
metadata:
  type: feedback
---

I wrote a one-click installer, checked that it parsed, and pushed it. Drico ran
it on a colleague's laptop and it failed at the first step. Six bugs in total,
and **not one of them was visible to a syntax check**:

- Windows ships a stub `python.exe` that only advertises the Microsoft Store, so
  "does a python command exist" answers yes and every call then fails. Presence
  is not capability.
- `$ErrorActionPreference = 'Stop'` turns a native command's stderr into a
  terminating error in PowerShell 5.1, so the normal case — probing for a
  module that is not installed yet — killed the script.
- Em-dashes in a file without a byte-order mark decoded as a smart quote, which
  PowerShell treats as a string delimiter.
- A tab and a backspace character hid inside Windows paths, matching nothing.
- winget's output was piped away, so a failed install surfaced three steps later
  as a PATH problem, which is the wrong diagnosis.
- The script inherited whatever exit code the last program set and reported
  failure after succeeding.

**Why:** I treated "it parses" as evidence it works, on a script whose whole job
is to interact with an environment I was not in. Every fault lived in that
interaction.

**How to apply:** run it. On this machine first, end to end, reading the output —
not a dry run, not a lint. Where a script probes for something, make it prove
the thing works rather than that it is present, and never discard the output of
a command whose failure you will have to diagnose later. Same shape as
[[n-verslag-bestaan-nie-omdat-die-agent-so-se]]: there I believed a report that
did not exist, here I believed code that had never run.

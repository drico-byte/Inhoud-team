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

## A success test that a stale file can pass

2026-09-03. Drico noticed that every reading lesson's PDF showed a raw JSON dump
where the story should be: *Onbekende bloktipe "leesstuk"*. Two separate bugs, and
the second is the one worth remembering.

**One:** `leesstuk` was added to the schema and the renderer was never taught it.
Fourteen lessons, all of them Life Skills, and the whole point of those lessons is
the reading. Straightforward omission — when a block type is added, every consumer
of the schema has to learn it, not just the gate.

**Two, and this is the trap:** the renderer decided a PDF had been produced by
asking whether the output file now existed and was over 800 bytes. **A leftover
from an earlier run passes that test without the browser writing anything.** So a
failed render reported success and silently shipped the previous version.

That is how the first bug survived a full re-export. I fixed the renderer, re-ran
the export, swept every PDF — and eleven were still broken, with no error anywhere.
Every reading lesson had quietly kept its stale file while the tool printed its
name as though it had been written.

**The shape to watch for: a success check that an unchanged world already
satisfies.** "The file is there" is not "I wrote the file". Clear the target first,
or compare a timestamp, so that doing nothing cannot look like doing the work.

**And when a fix does not take effect, check whether the output was written at
all before re-reading your own change.** I re-read the edit twice and went looking
for a second renderer, when the answer was that the file on disk was from an hour
earlier. `find -mmin` answered in one command what code-reading did not.

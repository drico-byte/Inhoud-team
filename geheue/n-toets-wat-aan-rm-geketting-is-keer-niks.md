---
name: n-toets-wat-aan-rm-geketting-is-keer-niks
description: I chained a "is anything lost?" check to rm with &&, so it printed "6 found nowhere" and deleted anyway; and the check itself compared parsed strings against raw JSON.
metadata:
  type: feedback
---

Deleting a saved copy of a hand-edited extract, I wrote one command: a Python check that
listed every sentence in the copy absent from the specification, then `&& rm`. The check
printed **six sentences found nowhere** and the file was removed in the same breath, because
`&&` only asks whether the check EXITED cleanly, never what it SAID. The file was untracked,
so git held nothing. The six turned out to be harmless — two were the generator's own note,
two were forms I had deliberately superseded that afternoon, two were false positives — but
that was luck, not method.

**Two faults, and the second is the one I would otherwise repeat.**

A verification that cannot stop the action is not a verification. Either make the check EXIT
NON-ZERO on a finding, so `&&` has something to act on, or run it as its own step and read it
before the destructive one. Printing a number and then deleting regardless is theatre.

And the check itself was wrong in a way that would have hidden a real loss: it compared
sentences taken from PARSED json against the RAW TEXT of another json file. Escaped newlines
and quotes in the raw text never match the parsed characters, so a genuine orphan would have
looked the same as the noise. **Compare parsed to parsed, or serialise both the same way** —
and when a detector produces findings you are about to dismiss, that is the moment to ask
whether it can tell a true finding from a false one at all. A detector nobody has tried to
fool is not evidence. Related: [[n-skrip-wat-parse-is-nie-n-skrip-wat-werk-nie]],
[[my-soektogte-mis-en-dan-glo-ek-hulle]], [[n-wag-wat-sy-eie-reels-naskryf]].

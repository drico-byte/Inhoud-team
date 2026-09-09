---
name: lees-is-n-uitbak-nie-n-argief-nie
description: "The lees/ folder is an outbox. Drico moves PDFs out of it to the language check and then to the HTML team, so files missing from it is normal, not a loss."
metadata:
  node_type: memory
  type: project
---

Drico, 9 September 2026: *"i moved stuff. I move pdfs from the lees folder to the
language check, and then to the html team."*

## What this means

`lees/` is a **hand-off folder**, not a store. A PDF's life is: exported there,
moved out to the language checker, then on to the HTML team. **An approved lesson
with no file in `lees/` is the normal end state**, not a missing deliverable.

It is also gitignored, so nothing versions it and there is no history to consult.

## The false alarm this caused, so it is not repeated

On 9 September I exported 37 Life Skills PDFs, and an hour later found only 8. I
treated it as data loss: re-ran the export, tested whether signing off one lesson
wiped the folder, checked for name collisions, and reported to Drico that I could
not account for it. All of that was wasted — he had simply moved the wellbeing
ones onward.

**Before treating a gap in `lees/` as a fault, ask whether the lessons are
approved and have their PDFs beside them in `konsepte/`.** That is where the real
copy lives. `lees/` only ever holds what has not yet been sent.

## What the export check does and does not do

`leeskopie.py --alles` now verifies itself, and the distinction matters here: it
checks that **this run wrote a file for every approved lesson**, at the moment of
export. It does not audit the folder afterwards. So Drico moving files out later
cannot trigger it, and a render that silently failed still will.

Related: [[n-skrip-wat-parse-is-nie-n-skrip-wat-werk-nie]]. The check exists
because I had verified the first export by counting files rather than by checking
the work — and a count cannot tell a written file from a leftover one.

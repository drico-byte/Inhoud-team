---
name: bly-geld-onder-die-merker
description: "Old spec fields put \"ALLES HIERONDER BLY GELD\" below the record marker, which hides the live order and makes withdrawn forms read as live; sweep a subject's specs for it before its pass."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 660119b3-6d4d-4eba-855b-7949cb3ca7d5
  modified: 2026-10-23T20:37:18.857Z
---

**What happened.** On 23 October 2026, coverage held five correct Gr 5 science lessons in one evening on the same spec pattern. A field reads: correction, then `ALLES HIERONDER IS 'n REKORD EN BESTEL NIKS`, then a record half that opens "ALLES HIERONDER BLY GELD" (or "bly geld, behalwe ...").

The runner splits every field at the marker and sends the lower half to a records file marked "orders nothing". The real requirement therefore stopped binding, and the withdrawn forms beside it read as live. Twelve of the Gr 5 NW spec files had it; three Gr 6 SW files and one Gr 4 SW file have it too.

**Why:** the patch style predates the marker split. Each coverage round found one field at a time, so the cost was paid lesson by lesson.

**How to apply:**
- Before a subject's pass, `grep -c "BLY GELD"` over its approved specs.
- Have an agent rewrite every such field in this order: the live orders first, written from the corrections and the signed-off draft; then the marker; then the dated records.
- Do this before any writer runs.
- The rewrite changes the extracts, so expect the runner to archive clean coverage reports; restore or re-run them.

Related: [[n-feiterisiko-is-nie-n-regstelling-nie]], [[die-marker-begrawe-die-bestelling]], [[die-korrigeerde-opdrag-bly-in-die-veld-staan]].

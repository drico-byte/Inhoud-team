---
name: n-ongeindekseerde-nota-bestaan-nie
description: "Three notes sat on disk with no index line, so I never read them — one was a standing ruling that made me escalate a question I was told to decide. Write the pointer in the same breath as the note."
metadata:
  node_type: memory
  type: feedback
---

**8 October 2026.** Consolidating the index turned up **three notes on disk with no index
line at all**, the oldest from 28 August. The index is what loads each session, so for
weeks those three had no effect on anything I did.

**One of them was a standing ruling of Drico's**, and its absence cost real work the same
day:

> If a phrasing makes it look like it is going to be factually incorrect, change it.
> **Stop sending up questions of the form "this phrase has two readings and one is
> false"** — decide, fix, report in one line. What stays his: curriculum scope, what a
> lesson teaches, changes to the standard.

I escalated exactly that shape to Lampies — a set of glossary entries whose asymmetry
implied something false — and he declined the question. He was applying a rule I could not
see. **The second note would have saved rounds too:** when a wording fails a third time,
stop rewriting the sentence and ask whether it is the **wrong container**. A frequency
sentence failed four times and the answer in the end was to remove it and let a different
block carry the message — a change of container. I reached it by the long route.

**The index had also grown to 46 KB and was being truncated on load**, with 111 of 163
files listed twice under different hooks. So two separate failures were hiding notes:
never adding a pointer, and adding so many that the tail was cut off.

**How to apply.**

* **Write the pointer in the same breath as the note**, and then **read the index back and
  confirm the line is there.** A note without a pointer is not a slow-acting risk; it is
  simply not part of me.
* **One line per file, and never two.** When a note grows a new section, update its
  existing line rather than adding another.
* **Watch the index's size.** Past about 30 KB the tail stops loading, which silently
  drops the newest notes — the ones most likely to matter today.
* **When a session writes several notes, consolidate at the end**: deduplicate, confirm
  every file is indexed and every indexed file exists. The check costs one script.

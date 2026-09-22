---
name: n-agent-wat-halfpad-sterf-laat-die-inhoud-sonder-sy-rekord
description: "A writer killed mid-task can land its content changes and die before writing its provenance note — so the lesson looks unrevised by its note while being revised in fact; diff the draft against the report's quoted sentences, not the note."
metadata:
  type: feedback
---

9 September 2026. A usage limit killed five agents mid-task. One was a writer on the
typewriter lesson; its last words were *"I have everything I need. Writing the revision
now."*

I checked whether its work had landed by reading the lesson's **provenance note** — 203
characters, no date from that day — and concluded no writer had run. So I re-briefed a
second writer from the original reports.

The second writer opened the file and found the draft **already a step ahead of both
reports**. The sentence had already been narrowed a third time, the speed claim had
already been moved to the later decades, and both unrequested details were already gone.
The first writer had written its content changes and died before writing its record.

**So the signal I used was the wrong one.** A writer updates the lesson content and its
own note in separate steps, and death lands between them. The note is therefore evidence
of nothing about the content — in either direction:

* a note *claiming* a change is no evidence the change happened (three writers hit this
  from the other side today, over the status field);
* a note *not mentioning* a change is no evidence the change did not happen.

**What to do instead.** A report quotes the sentences it found wrong. **Diff those quoted
sentences against the draft** before re-briefing anyone. If the text no longer contains
them, the work landed and the report is a history — see
[[n-verslag-in-die-logboom-kan-verouderd-wees]], which is the same trap from the other
end. It takes one grep per finding and it is the only reliable check.

**The cost when it goes unnoticed.** Two: a second writer spends a full pass rediscovering
what the first one did, and — worse — the reasoning is lost. The first writer's *why*
died with it, so the decisions sat in the file unexplained and a later pass could have
undone them as unmotivated. The second writer restored the record, but only because it
noticed.

**One thing it surfaced that nothing else would have.** With the note missing, the second
writer read the whole block cold and found a sentence that **has never been through any
fact check** — it entered in an earlier round and every check since has been narrow. It
kept it, on the grounds that the block needs an entry point and the three confirmed
sentences after it are its evidence, and it said so plainly instead of letting it pass as
verified. That is the behaviour to want: an unverified claim flagged rather than
inherited.

**A second way it goes wrong: the file itself is cut off.** 18 September 2026. A writer
stopped by a false safety flag left the frame-structures draft at **867 bytes**, cut off
mid-string, a minute after the last commit. The next writer misread it as "one very long
line my reader cannot see" and asked for a reformat. Nothing in the pipeline parses a
draft until the gate runs. **After any agent dies, parse every draft it could have
touched** (`json.load`) before briefing anyone. If one fails, restore it from git; the
last commit is the good copy.

Related: [[voor-jy-stop-se-wat-loop]], [[n-verslag-bestaan-nie-omdat-die-agent-so-se]],
[[spesifikasies-word-nooit-nagegaan]] (its later section on the note being an unchecked
claim about the text).

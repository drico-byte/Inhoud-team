---
name: n-beskrywing-verouder-n-vereiste-nie
description: Most spec fields that went stale in one day were written as DESCRIPTIONS of the draft's state, not as requirements; a description ages the moment the writer runs, a requirement does not.
metadata:
  type: feedback
---

29 September 2026, after a day in which nearly every coverage check came back escalating the
spec rather than the draft. The shapes I catalogued — the order standing beside its retraction,
the "what now applies" clause, the retraction inside the order, the marker that withdraws too
much, the pointer that ranks instead of naming — are all symptoms. **This is the cause.**

I write findings as descriptions of the draft:

> "STANDS STILL WORD FOR WORD IN ITS WIDE FORM"
> "THE HIV TRANSMISSION SENTENCE IS STILL UNCONDITIONAL"
> "the lesson does not say that dormant germs can later …"
> "TWO ENTRIES THAT ARE NOT FAULTS"

Every one of those is **true when written and false an hour later**, because the whole point of
writing it is that a writer will then change the draft. And a false description in a spec is not
inert: the next checker hunts for faults that are already repaired, and "two entries that are not
faults", read after the repair, works as permission to narrow them back.

**The fix is a habit, not a sweep.** Write the requirement, never the state:

| ages | survives |
|---|---|
| "still stands in its wide form" | "stays in its narrowed form; the wide form may not return" |
| "is still unconditional" | "stays conditional, with all its conditions" |
| "the lesson does not say X" | "the lesson must say X" |
| "these two are not faults" | "these two were corrected and may not be narrowed back" |
| "the draft still carries the old wording, so it goes through the writer" | "the wording is X" (dispatch separately) |

**The test before saving a field:** read the sentence and ask *would this still be true after a
writer acts on it?* If not, it is a description. Rewrite it as what must be true.

Keep the description **inside a dated bracket** if it earns its place — how a fault arose is
often worth having — but the sentence a reviser meets must be the requirement.

Related: this is the root that [[die-korrigeerde-opdrag-bly-in-die-veld-staan]],
[[die-merker-begrawe-die-bestelling]] and [[n-wyser-benoem-nooit-rangskik]] all branch from. And
[[n-veeg-vir-velde-wat-nog-bestel]] can only find the explicit phrasings — the general case needs
a coverage checker, who reads the draft and the field together.

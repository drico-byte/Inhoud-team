---
name: n-wyser-benoem-nooit-rangskik
description: "Six pointers saying \"this lesson's newest core item\" broke the moment my next repair added an item after it; a pointer names an item by its content, never by its position."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9cbb5026-bd75-4aa5-a144-0346fd07bf1f
  modified: 2026-09-29T20:43:46.615Z
---

29 September 2026, Grade 7 LO. Six places in one spec entry pointed a reviser at **"this
lesson's newest core item"**. That was true when I wrote them — the route requirement stood
last. My own next repair, an hour later, recorded a separate matter as a new core item. All six
pointers then resolved to an item that says nothing about the route.

A reviser following any of them lands on the wrong item and reads the route order as **absent**.
A coverage checker found all six.

**The rule: a pointer names an item by its CONTENT, never by its POSITION.** "The newest",
"the last", "the item below", "the one at the end" all break silently the moment anyone adds
something — and adding something is what a repair day does all day. Write the item's own opening
words instead: *the item beginning "THE WHOLE ROUTE ORDER IS HEREBY REPLACED"*.

**Why this one is worth its own note.** The failure is silent in both directions. Nothing errors,
no sweep catches it, and the pointer still reads as confident and specific. And the person who
breaks it is the person who wrote it, one repair later — so the usual defence of re-reading the
field you are editing does not help, because the pointer is in a *different* field from the one
you are adding to.

**What to do when adding an item to a field-set:** grep that lesson for position words —
`jongste`, `laaste`, `hieronder`, `hierbo`, `vorige`, `volgende` — before saving. If any of them
points at what used to be last, it now points at your new item.

**Amended 29 September 2026 — the asymmetry, and there is a sweep now.** Counting from the
*front* is safe: "the FIRST core item" survives every append, because items are added at the end.
Only counting from the *back* breaks. So the rule is narrower and easier than "no positions":
**never rank from the back.**

Two more things that day. A pointer of this shape broke **four** times before I stopped patching
them one at a time, and the worst one was not a reference but an **order** — *"write the LAST point
as a consequence in practice"* — keyed to a list that can grow, so adding a point would have moved
the order onto a point it never meant. And twice the repair itself produced the next fault, because
replacing the pointer left the sentence *beside* it saying the opposite; see
[[n-regstelling-ontwrig-sy-bure]].

`bin/wyserveeg.py` now sweeps this. It ignores a hit inside a dated marker (there the words are a
record), and it had to be tightened twice before it was usable: `die laaste stap`, `die laaste sin`,
`KABV se laaste punt` and `die veld hieronder` are ordinary prose or stable references, and a sweep
that fires on them gets ignored — which is [[n-veeg-vir-velde-wat-nog-bestel]] all over again. It
reports zero across Grades 4, 5 and 6, which is what makes a Grade 7 hit mean something.

**Where the substance already stands in the same place, delete the pointer instead of renaming it.**
Half the twelve needed no replacement at all — the sentence beside them already said the thing.

Related: [[vee-die-bewering-oor-al-die-spesifikasies]] (sweep every field that repeats the claim),
[[die-korrigeerde-opdrag-bly-in-die-veld-staan]] (the order survives its own retraction).

---
name: n-weglating-verander-sy-bure
description: "Cutting a sentence changes what its neighbours mean. Twice in one day a deletion created a claim neither surviving sentence made alone."
metadata:
  node_type: memory
  type: feedback
---

2026-09-03. [[n-regstelling-ontwrig-sy-bure]] covers a correction disturbing what
sits near it. This is the narrower case that bit twice in a single day: **the
edit was a pure deletion, and the damage was done by what became adjacent.**

## The rights lesson

The block ran: *some children in our country do not get enough food or a house* →
*parents care for their children first* → *the country helps where parents cannot*
→ *the country breaks its promise when it does not do what it can.*

I cut the middle pair to get four words under the length ceiling. Both were true
and neither was asked for by any requirement, so it looked free.

It was not. The first and last sentences became neighbours, and a nine-year-old
reads them as a **conclusion**: here are children without food or housing,
therefore the country is not doing what it can, therefore it is breaking its
promise. Nothing supports that. *Grootboom* points the other way — lacking a house
is not by itself a violation. The cut pair had been the bridge that made *"what it
can"* a real limit rather than a rhetorical one.

**Neither surviving sentence changed. The claim was created by their adjacency.**

## The water-safety story

Same day, same shape but through state rather than juxtaposition: correcting the
drowning boy's eyes made him unresponsive, which orphaned a deliberate grasp four
sentences later. Recorded in [[n-regstelling-ontwrig-sy-bure]].

## What to do

**After a deletion, read the sentences that now touch.** Out loud, in order, as a
child would. Ask what the pair asserts that neither member asserted alone. This is
invisible to a diff, invisible to a keyword search, and invisible to the gate.

**And do not assume a cut is free because nothing requires the cut text.** Coverage
answers "is the requirement present", not "does the passage still mean what it
meant". A sentence can carry no requirement and still be load-bearing.

## The coverage blind spot this exposed

Worth knowing on its own. The spec's writing note asked the lesson to carry two
things: that a right is what the country **undertook** to do, and that
non-delivery is a **violation** rather than an exception. After my cut the passage
delivered only the violation half — and **coverage passed that block 10 of 10
twice**, because the requirement was being credited to the violation sentence
alone.

So a two-part requirement written as one prose note can be marked met by half of
itself. When a spec note contains an "and", check both halves land in the text,
because a coverage check may not split them.

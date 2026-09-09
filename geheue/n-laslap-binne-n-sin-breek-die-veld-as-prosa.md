---
name: n-laslap-binne-n-sin-breek-die-veld-as-prosa
description: "A scripted replacement that lands mid-sentence leaves the old tail dangling, so the requirement reads two ways and its old instruction survives inside the new one; replace whole sentences, and rewrite the field once it has three patches on it."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f21c597a-2944-4014-bf02-c866813c3fa2
  modified: 2026-09-09T11:40:05.904Z
---

9 September 2026, Gr 4 Sosiale Wetenskappe, the boats lesson. Two requirements
were left broken as prose by my own scripted fixes, and a coverage check found
them.

My swaps matched a **clause**, not a sentence. So a replacement landed in the
middle and the old sentence's tail survived after it:

> ...the push-only version therefore contradicts the lesson within the same
> block, **so a ship could now carry further than muscle and current together.**

> ...as this lesson's own raft block says **and people could travel further over
> water than before.**

Each reads two ways, and the more natural reading keeps part of what the fix was
removing. `n-ruil-wat-nie-pas-nie-moet-hard-faal` made me assert every swap on
an exact string, and the asserts all passed — the string was there, exactly once,
and replacing it still produced nonsense. **An assert proves the match, not that
the result is a sentence.**

The same field also still carried a false premise of mine in its **body** after
its closing lines retracted it: "of the three only the canoe was really
paddled". Reed boats were commonly paddled. So the field simultaneously ordered
and forbade the same thing, four patches deep.

**How to apply.**

1. Match and replace **whole sentences**, ending at the full stop. If the fix is
   a clause, rewrite the sentence around it.
2. **Print the field after every edit and read it as prose**, not as a diff. The
   printing discipline already exists; this is the part of it I skip.
3. **Once a field carries three dated corrections, rewrite it whole** and keep
   the history in one bracket at the end. A fourth patch is cheaper to write and
   more expensive than the rewrite — the rewrite is what finally surfaced the
   retracted premise still sitting in the body.

Related: [[n-ruil-wat-nie-pas-nie-moet-hard-faal]],
[[n-feiterisiko-is-nie-n-regstelling-nie]], [[kern-en-feiterisiko-weerspreek-mekaar]],
[[n-waarskuwing-moet-elke-broer-dek]].

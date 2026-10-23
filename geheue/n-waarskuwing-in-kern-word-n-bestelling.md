---
name: n-waarskuwing-in-kern-word-n-bestelling
description: A caution I write into a kern field is read by coverage as content to deliver; put cautions in feiterisiko or below the record marker.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 660119b3-6d4d-4eba-855b-7949cb3ca7d5
  modified: 2026-10-23T11:49:59.183Z
---

On 23 October 2026, I wrote "Die meeste gewone mense het nie een gesien nie" into Gr 4 Kommunikasie les 10 kern[0]. I meant it to soften an absolute claim. The next coverage run read it as an order, found the lesson didn't say it, and failed a correct draft. That cost one more spec fix and one more coverage round.

The same day, a fact-repair wording I gave a writer ("search from anywhere, at any time") went into both the spec and the lesson. The next fact check found it over-wide too.

**Why:** coverage tests the draft against every sentence in kern. Anything phrased as a statement there becomes something the lesson must say.

**How to apply:**
- When narrowing a claim in kern, rewrite the order itself, for example "EEN rekenaar kon 'n hele kamer vul".
- Put "don't say X" cautions in feiterisiko, or as a prohibition ("moenie ... skryf nie").
- Never add a new fact sentence to kern unless the lesson must teach it.
- Treat a wording I hand a writer for a fact repair as a new claim. Keep it as narrow as the fact allows.

Related: [[n-feiterisiko-is-nie-n-regstelling-nie]], [[moenie-in-die-spek-skryf-wat-jy-nie-nagegaan-het-nie]], [[n-regstelling-ontwrig-sy-bure]].

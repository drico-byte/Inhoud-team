---
name: my-soektogte-mis-en-dan-glo-ek-hulle
description: Three times in one day a search of mine came back empty and I reported the absence as a finding. The third time I was about to tell Drico an agent had fabricated quotations. A search that missed looks exactly like a search that found nothing.
metadata:
  type: feedback
---

Three times on 28 August 2026, in one afternoon:

* I checked whether every mention of a retracted phrase sat inside a correction
  note. My context window was 130 characters and the notes are longer, so the
  script printed **LOS** against six correct entries.
* I looked for the loose strut wording in a specification, found the precise one,
  and reported the file clean. Both wordings were in the same sentence; my window
  centred on one and cut off the other.
* A writer pushed back with two exact quotations. I searched for `\bente\b`,
  found neither, and started composing a message saying an agent had produced
  fabricated quotes to defend itself. **The text is in capitals — OP SY ENTE —
  and my pattern was case-sensitive.** The writer was right about all three
  occurrences, including one I had already told it did not exist.

**Why this one is worse than being wrong.** An empty result reads as evidence.
It has the shape of a finding, it costs nothing to believe, and it flatters
whatever I already thought. Twice it made me tell an agent its correct report was
mistaken. The third time it would have put a false accusation in writing about
work that was careful and right, and the pushback that saved it was the agent
declining to accept my correction.

**How to apply:** an absence is not a result until the search has been shown to
find something. Before reporting that a thing is not there, run the pattern
against a case you know is present. Search case-insensitively unless case is the
point. Widen the window past the longest thing being matched, or match on the
whole field rather than a window. And when an agent contradicts me with specifics
— quoted text, a line, a number — assume my search failed before assuming its
reading did: it read the file, and I ran a pattern over it. Same shape as
[[n-skoon-toets-is-so-wyd-soos-sy-omvang]], one level down: there the claim was
wider than the check, here the check was narrower than the file.

## A `break` in the loop, and I reported the field as clean

**2 October 2026.** I searched a specification for a claim a fact check had
withdrawn, to decide whether it was ordered at source. My probe printed the
**first** match per field and then `break`ed. The first hit in the relevant field
was an innocent one early on; **the claim itself stood in capitals further along
the same field**, in its opening order. I told the writer, in a brief and without
hedging, that neither claim was ordered. It checked, found the capitals line, and
corrected me.

**Why this one is nastier than an empty result.** An empty search at least looks
like nothing was found. A `break` returns a *plausible, relevant* excerpt, so the
output looks like a successful search of the field — and I read it as one.

**How to apply:** when the question is "does this appear anywhere", print **every**
occurrence and a total count, never the first. Say where each sits — above or
below the record marker — because that decides whether it orders anything. And
when a brief rests on my own search, say in the brief that it is my search and may
have missed: the writer's doubt is the last line of defence, and here it held.

---
name: elke-les-kry-n-eie-naam
description: "A lesson's title is the hero heading a learner reads — never the CAPS label from Drico's term plan. Required on every lesson."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8f79bbfb-d2d6-48c5-804a-7410b16958f5
  modified: 2026-08-24T13:23:02.794Z
---

Drico, 2026-08-21: "I want you to give each lesson an appropriate name. The lesson names i used in my
structure was so that you can easily match it with caps document. That will then be the name the html
team uses with the hero... Also remember it for all future lessons."

**The distinction.** The labels in his term plan ("Wat plante nodig het om te groei", "Behoefte aan
habitatte", "Diere skuilings") exist so the plan can be matched against the CAPS document. They are
**not** lesson names. The `titel` field is what the layout team puts in the hero at the top of the
page, so it is the first thing a learner reads.

**What works, from the ones he kept:** "Vlotte, kano's en rietbote" names the concrete things the
lesson is about. "Wat is 'n habitat?" asks the question the lesson answers. "Die dele van 'n plant"
says plainly what you get. Short, in a nine-year-old's words, and specific to that lesson rather than
to its topic.

**What fails:** repeating the CAPS heading; being general enough to head three different lessons;
longer than about six words; promising what the lesson does not deliver.

## A title is subject to every factual rule the lesson is

This is the part worth defending. The title is the most-read sentence on the page and **nothing checks
it the way the study text is checked** — the fact checker works through blocks, and a title is not a
block. So it is the easiest place in the whole file to reintroduce something a revision removed.

Real traps, each of which cost a revision round on 2026-08-21:

- **No count of a plant's main parts.** "Die vier hoofdele van 'n plant" is exactly the claim that was
  removed: how many main parts a plant has is a framing choice, not a fact, and a South African Grade 4
  source says five. See [[betwiste-klassifikasie-ruil-die-voorbeeld]].
- **No unhedged universal the lesson itself hedges.** If the lesson says "die meeste plante", the title
  may not say "plante" meaning all of them. See [[kaps-se-lys-wen-oor-die-handboek-se-lys]].
- **No category the lesson deliberately avoids** — the reserved term for an object's flat faces, or
  classifying a bird's nest as frame or shell.
- **No promise of questions or activities.** Lessons carry neither. See [[geen-vrae-in-lesse-nie]].

**How to apply.** Every new lesson gets a real title from the writer, not the CAPS label. Route it
through the writer rather than naming it yourself: whether an Afrikaans title reads well is a native
speaker's judgement, and an agent's ear for that is unreliable in both directions — see
[[afrikaans-wag-vir-spesialiste]] and the general point in `references/woordkeuse.md`. Then show Drico
the list, because it is his hero text.

---

**30 September 2026: a title asserts what its own spec forbids, and nothing downstream
can see it.**

Three consecutive lessons in Gr 4 Geography's map-skills sub-topic had a *planned* title
carrying a claim that same lesson's fact-risk list explicitly prohibits:

* "Klein prentjies wat 'n **hele plek** vertel" — while its own field forbids saying a
  map shows everything at that place.
* "**Letter langs die kant, nommer bo-aan**" — while its first field forbids claiming
  every map's grid is marked that way.
* "**Noord bo**, en die son wys die res" — while its second field forbids saying north is
  always at the top, and marks the hedge as load-bearing.

All three were caught by the *writer*. None by the pipeline.

**The mechanism is structural, not carelessness.** A title is written to be short and
memorable, and shortening means dropping qualifiers — and the qualifier is usually the
only thing making the claim true. "North is usually at the top" is true; "Noord bo" is
the same sentence with the one load-bearing word removed.

And the note above already says nothing checks a title the way it checks the text. This
is what that costs in practice: **the gate counts a title's words, coverage tests
requirements against the body, and the fact checker reads it as a heading.** A false
title passes every stage untouched and is the largest text on the delivered page.

**How to apply.**

* **After writing or approving a title, read the lesson's fact-risk list and ask whether
  the title says one of the forbidden things.** That is a ten-second check and it caught
  nothing three times because nobody ran it.
* **Suspect any title that is a compressed version of a hedged sentence in the body.** If
  the body needs "usually", "often" or "on many maps" to be true, the title cannot say
  the same thing without them.
* A title may name the lesson's **subject** without making a **claim**. "Vier rigtings op
  'n kaart en buite" says what the lesson is about and asserts nothing.

Recorded at spec level in that sub-topic so a planner writing the next set meets it.
Related: [[die-korrigeerde-opdrag-bly-in-die-veld-staan]], [[n-versagting-vat-die-algemene-helfte-saam]].

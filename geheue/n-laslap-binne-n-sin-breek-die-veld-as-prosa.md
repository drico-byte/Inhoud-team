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

## 6 October 2026: the assert cannot see this, so give it a check that can

It happened again, and worse, because the broken sentence said the **opposite** of the
correction. My needle ended at `...nagegaan en al` and the remaining `bei bly` fused to the
end of the bracket I inserted:

> daardie sin is nagegaan en al**[**DIE BAHA'I-VERTALING-SIN IS … GESKRAP…**]** bei bly, dus
> is dit die gevolgtrekking TUSSEN hulle wat gekeer moet word

So the living sentence still ordered that **both** language sentences stay — the very order
the fact check had reversed — and the bracket's own claim that the sentence had been *taken
out of* this field was false: it had been inserted *into* it. **The assert passed, because
the match was unique.** A coverage checker found it.

**The check that works**, now run over every string in the spec after any edit:

```python
def binne_woord(teks):
    """Any '[' with a letter immediately before, or ']' with a letter immediately after."""
    return (re.findall(r'.{0,30}\w\[.{0,30}', teks) +
            re.findall(r'.{0,30}\]\w.{0,30}', teks))
```

Assert it returns nothing. It is cheap, it has no false positives in this codebase, and it
catches the one thing an equality assert cannot: that the *result* is still prose.

**And the rule the needle must follow:** anchor it at sentence boundaries — start at a capital
or after `. `, end at the full stop — and never let a replacement begin or end inside a word.
When in doubt, locate the sentence by `index()` of its opening and of its closing phrase and
replace the whole span, which is what finally worked here.

Two neighbouring traps from the same session:

- **A record marker protects only the kind of content it names.** A marker saying "no NUMBER
  below this is a budget or a measurement" does not neutralise an order below it that contains
  no number. That order survived three sweeps because the marker looked like it covered the field.
- **A bracket that reduces a pair to one leaves the surrounding prose in the plural.** Cosmetic
  — a deleted sentence cannot return — but a list that speaks of two where one stands sends a
  reader hunting for the second.

## The family is three shapes, not one — 6 October 2026

One session, one spec, three different ways a replacement broke the prose, and **a coverage
checker found each one.** An equality assert cannot see any of them, because it proves the
match, never that the result is a sentence.

| shape | what it looked like |
|---|---|
| bracket inside a word | `al`**[**`…`**]**`bei bly` — and the living sentence then said the opposite of the correction |
| doubled phrase | `om skade te verminder` + `wat skade verminder` — my addition met the original's tail |
| headless sentence | `… en bevestig. bly om EEN rede` — the needle ate the subject |

**The three checks, run over every string in the spec after any edit:**

```python
re.findall(r'.{0,18}\w\[.{0,18}', s)            # bracket inside a word
re.findall(r'.{0,18}\]\w.{0,18}', s)
w = lewend(s).split()                            # doubled phrase: 3-5 words repeated
any(w[i:i+n] == w[i+n:i+2*n] for n in (5,4,3) for i in range(len(w)-2*n+1))
re.finditer(r'(?<![.A-Z])\. +([a-z\u00e0-\u00ff]{3,})', lewend(s))   # headless sentence
```

**The third one needs its exclusions or it is worthless.** My first version fired on every
semicolon and returned **226** hits across one spec — a check with that noise gets ignored,
the same way a sweep that fires on the normal correction shape does. A semicolon does not start
a sentence. With `(?<![.A-Z])` excluding ellipses inside quotations and capitalised
abbreviations, the same spec family returns **four**, and all four are benign: two stylistic
lowercase starts, one field name, one glossary-style term label. Four is reviewable; 226 is not.

**And the habit that caused all three:** replace a whole span, anchored at sentence boundaries,
then read the result back. Locating the sentence with `index()` of its opening phrase and of
its closing phrase, and replacing everything between, is what finally worked each time.

## 13 October 2026: an em-dash aside inside an ordering sentence reads as CONTENT

Gr 6 SW Mapungubwe lesson 4, twice in one day, in the same field.

**First time.** I wrote the evidence for "almost nowhere else" into the ordering sentence as
an em-dash aside — *"goud is bo-op die heuwel gevind en byna nerens anders nie — net 'n paar
los stukke op die Suidelike Terras en niks by die vroeer plek nie — en dit is by die hoogste
rang begrawe"*. A writer read the aside as required content, **fairly**, because that is
where required content lives, and reported it as the thing that did not fit the ceiling by
seventeen words. I fixed it by promoting it out of the parenthetical into its own sentence
marked "WAT DIE LES NIE HOEF TE SKRYF NIE".

**Second time, hours later, same field.** Rewriting the item on the place, I wrote
*"Waar die leiers gewoon het, is 'n APARTE gegewe — Mapungubwe is die oudste bekende plek in
Suider-Afrika waar leiers apart van hul mense gewoon het, en die klipmure wys dit."* A
coverage check flagged it in the position where mandatory content sits — and noted it was
also an **un-narrowed superlative** in a cluster where every superlative is narrowed, and
that the hedge "bekende" is forbidden on a neighbouring claim in lesson 3.

**The rule, and it is about position rather than wording.** In a requirement field, where a
clause sits decides whether it is read as an order. An aside inside an ordering sentence is
content; a separate sentence that says what it is, is a ground. So:

* **Never put a ground inside the sentence that orders.** Give it its own sentence and say
  in capitals what it is — evidence for a person, not content for the learner.
* **A ground that contains a superlative needs the superlative barred explicitly**, because
  a writer who decides to use the ground has no other signal that the claim is the expensive
  kind. One did leave it out and said why; that was luck in the sense that he was careful,
  not that the field told him.
* **A field's own record is where to look before writing into it.** This field's record
  documented the first instance and the fix for it, and I made the same mistake in the same
  field anyway — because I read the order half, edited it, and never read the record I had
  written that morning.

Related: [[die-merker-begrawe-die-bestelling]],
[[n-spek-se-dieselfde-ding-in-twee-velde]], [[n-beskrywing-verouder-n-vereiste-nie]].

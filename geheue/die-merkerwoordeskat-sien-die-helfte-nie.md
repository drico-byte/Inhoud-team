---
name: die-merkerwoordeskat-sien-die-helfte-nie
description: "The stale-order sweep knew 15 ways of opening a dated record; the house wrote at least 6 more, hiding 469 fields in 53 specs. Widen the DETECTOR, never the boundary."
metadata:
  node_type: memory
  type: project
---

13 October 2026. An agent repairing four Grade 6 Social Sciences specifications
reported that the sweep's own counts "understated the job by more than half" — it
named 11 records; reading the files found 28. I checked the claim instead of
believing it, and it was true and much bigger than the subject.

`bin/paaie.py` holds the record-marker vocabulary: a bare list of 15 forms, plus 4
that count only in a dated shape. The house has also been opening records with
`REGSTELLING`, `BESLIS`, `BESLEG`, `NAGEGAAN`, `BYGEWERK`, `KWANTIFISEERDER
VERNOU` and lower-case `reggestel` / `bygeskryf` — none of which either list knows.

**Measured across all 91 approved specs: 469 fields in 53 files hold a dated record
inside a live ordering half**, where a writer reads the wording it quotes as
withdrawn as a current order. Two severities, and the repair differs:

* **381 fields have no canonical line at all** — nobody ever drew that field's
  boundary. Heaviest in gr4 (142) and gr7 (100).
* **88 fields have the line but hold a record above it** — gr5 (43) and gr6 (43),
  which are exactly the grades where the line was adopted.

## The fix that looked obvious was the dangerous one

The tempting move is to add the missing words to the vocabulary. **Measure before
you do.** Bare, those words appear **808 times as the verb of a live order** against
151 times dated — "DIE KIEME-OMSKRYWING IS REEDS BESLIS", "DRIE DINGE WAT NIE
BESLEG KON WORD NIE", "LET OP DIE TWEE MANIERE WAAROP 'n REGSTELLING HIERVAN
VERKEERD KAN LOOP". A bare list truncates 808 ordering halves.

And **even the dated shape may not go into `REKORDMERKERS_GEDATEER`**, because that
list feeds `REKORDMERKER_PATROON` and therefore `eerste_rekordmerker`, which is what
splits every extract. Adding them moves the boundary in all 469 fields at once: I
measured **427 fields losing more than 200 characters each, about 528 KB of live
orders silently demoted to "orders nothing"**. The module's own docstring already
warned "Do not widen either of those two tests to the whole list", and it is right.

So the answer is two tools, not one: `REKORDMERKERS_RUIM` with
`ruim_rekords` / `ongemerkte_rekords` for **finding** a field a person must read, and
`eerste_rekordmerker` left alone for **deciding** where a record half begins. The date
is the whole discriminator, required in full — day, month name and year.

**How to apply:** an order read as a record is worse than a record read as prose,
because a demoted order stops being delivered at all and nothing reports it. So when
a boundary-finder and a fault-finder want different vocabularies, give them different
vocabularies — and the boundary moves only when a person writes the canonical line,
which is the one mark that states an author's own intent. Related:
[[die-merker-begrawe-die-bestelling]],
[[n-skoon-toets-is-so-wyd-soos-sy-omvang]], [[n-wag-wat-sy-eie-reels-naskryf]],
[[die-korrigeerde-opdrag-bly-in-die-veld-staan]].

---
name: n-veeg-vir-velde-wat-nog-bestel
description: bin/spekveeg.py finds the three shapes in which a spec field keeps ORDERING something a later decision overtook; checkers used to find these one lesson at a time, at a round each.
metadata:
  type: reference
---

29 September 2026. Built `bin/spekveeg.py` after checkers reported the same three shapes in
lesson after lesson, each costing a repair round:

```bash
python bin/spekveeg.py --graad 7 --vak Lewensorientering
python bin/spekveeg.py --pad spesifikasies/goedgekeur/gr7/lewensorientering
```

**The three shapes it finds.**

1. **A "WAT GELD" clause.** It sits inside a retraction bracket and reads like part of the
   record — but it is the LIVE requirement, and it ages like any other order. One claim was
   narrowed twice in a day; the first narrowing went into three such clauses and the second
   never reached them, so three of my own markers went on ordering an overtaken form. The sweep
   flags a clause with **no date** near it, because an undated order loses under the specs' own
   `voorrang_reel` and is the most dangerous kind.
2. **A retraction INSIDE the order.** `DIE REGSTELLING: say X [X is withdrawn]` still orders X —
   a reviser reads the imperative and writes X. The retraction has to sit outside the order, or
   the ordering sentence itself has to change.
3. **A claim ABOUT the draft that has aged** — "the draft still carries the narrower form",
   "so this lesson goes through the writer". Once the writer has run, such a sentence orders a
   change to text that is already right.

**Two things about the sweep worth knowing, because they are why it is usable.**

- **It does not fire on the normal, legitimate shape.** My first version flagged every
  correction note that followed an imperative, which is exactly how a correct repair looks — 4
  hits, all benign. It now fires only when the retraction *interrupts* the ordering sentence.
  A check that fires on ordinary work gets ignored, which is worse than no check.
- **It does not fire on a record quoting what it withdrew.** Same reason, same lesson as
  everywhere else: assert against the live requirement, not against the old words.

**It decides nothing.** Whether a clause is stale depends on what has been decided since, so it
prints places to read. Run it after a wave of fact checks and before briefing writers.

Its date window is wide (about 1600 characters back) because a long note carries its date at the
top; a narrow window produced 14 false "no date" hits. If the undated count ever reads zero
across a whole subject, test it against a deliberately undated clause before believing it — a
check that never fires may be broken.

Related: [[die-korrigeerde-opdrag-bly-in-die-veld-staan]], [[die-merker-begrawe-die-bestelling]],
[[n-skrip-wat-parse-is-nie-n-skrip-wat-werk-nie]].

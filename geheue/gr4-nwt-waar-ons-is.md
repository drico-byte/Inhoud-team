---
name: gr4-nwt-waar-ons-is
description: "Gr 4 NWT progress — Term 1 complete (lessons 1-8), Term 2 planned and cross-checked (9-16), plus the open questions."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f79bbfb-d2d6-48c5-804a-7410b16958f5
  modified: 2026-08-24T19:20:49.405Z
---

State as at 2026-08-21.

## Term 1 — "Lewe en lewende dinge" — COMPLETE, lessons 1 to 8

All eight passed the gate and both checks (`GOEDGEKEUR` on facts and coverage). Titles are the learner
hero headings; the numbered file names are Drico's CAPS index — see [[lesnommers-loop-deur-die-jaar]].

1 Lewende dinge · 2 Nie-lewende dinge · 3 Strukture van plante · 4 Strukture van diere ·
5 Wat plante benodig vir groei · 6 Verskillende habitatte · 7 Behoefte aan habitatte · 8 Diere skuilings

`bin/leeskopie.py` now emits `N_label.pdf` from `kaps/lesindeks/gr4-natuurwetenskappe-en-tegnologie.json`,
so **Drico no longer renames by hand.** Add Term 2's entries to that file.

## Term 2 — "Materie en Materiale" — PLANNED, lessons 9 to 16, nothing written

Cross-checked against all three parts of CAPS per [[kruistoets-die-termynplan-teen-kaps]]. **The plan is
clean** — content tables and overview agree at 10 weeks, and every content heading has exactly one lesson,
in CAPS's own order. Unlike Term 1, no gaps in either direction.

9 Vaste stowwe, vloeistowwe en gasse · 10 Verandering van die toestand · 11 Die watersiklus ·
12 Onverwerkte en verwerkte materiaal · 13 Eienskappe van materiaal · 14 Maniere om materiaal te versterk ·
15 Stutte en raamstrukture · 16 Inheemse strukture

**Two assessment items are out of scope, by Drico's ruling:** demonstrating how to make and join paper
struts, and designing/making/evaluating a strong structure. Practical work a text cannot deliver, same as
Term 1's shelter design task.

**Four things flagged before planning:**
- **Lesson 11 has a constraint in its own assessment wording** — CAPS asks learners to explain the water
  cycle *in terms of the change of state of water*. It must be built on lesson 10's vocabulary, not told
  as the rain story.
- **Lesson 12 teaches that coal and oil make plastic.** This is the fact that made the plastic ball a trap
  in lesson 2 — see [[nie-lewende-voorbeelde-sonder-lewensherkoms]]. Core content here.
- **Lesson 15 overlaps Term 1's lesson 8**, which already taught frame structures. Check consistency and
  accidental repetition.
- **Lesson 16 is cultural content** — Zulu (uguqa), Xhosa (rontabile, ungqu-phantsi) and Nama
  (matjieshuis) traditional houses. Needs more care than anything written so far: getting a people's own
  word for their own building wrong is a different order of error.

**A textbook trap Drico caught himself:** Platinum Gr 4 teaches metals and non-metals with four properties
each, and it is **not Grade 4 content** — CAPS puts "Metale en nie-metale" in **Grade 5 Term 2**. Grade 4's
properties are hard/soft, stiff/bendable, strong/weak, light/heavy, waterproof/absorbent. Do not let the
textbook's structure into lesson 13. This is the mirror of Term 1's problem: there CAPS assessed what it
never taught; here the book teaches what CAPS does not ask for at this grade.

## Open, unanswered

**The `goedgekeur/` folder** (outside the repo, `C:\Users\DricoSnyman\dev\goedgekeur`) is **empty and has
never been written to.** The runner has logged 64 events, all measurements, never an approval. Three tools
still point at it: `hardloop.py` (approval target and status), `leeskopie.py` (its `--alles` glob), and
`opstel.py` (recreates it). Drico asked whether it can be deleted; the deciding question — **where does the
HTML team actually read a lesson from?** — was never answered. Deleting the folder alone achieves nothing.
If nothing reads it, remove the concept properly; a second copy would go stale exactly as his PDF copies
did.

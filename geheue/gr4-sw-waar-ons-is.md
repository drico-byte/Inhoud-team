---
name: gr4-sw-waar-ons-is
description: "Gr 4 Sosiale Wetenskappe as at 9 September 2026: Kwartaal 4 is drafted and nearly through its checks; Kwartaal 1-3 is 19 lessons with 30 checks still outstanding and one lesson signed off."
metadata:
  type: project
---

State as at **9 September 2026**, counted from the report files on disk rather than by
asking the runner — the runner archives finished reports as outdated and demands the
checks again ([[moenie-die-hardloper-vra-oor-n-nagesiende-les-nie]]).

## Kwartaal 4 — `kommunikasie-oor-tyd-heen`, 11 lessons

Drafted, gated, and nearly through its second check cycle. Coverage **approved** on
lessons 1, 2, 5, 6, 8, 9, 10 and 11. Lessons 3 and 4 are the two still mid-cycle.

Signed off across the whole subject so far: **Kwartaal 1 lesson 1**, and Kwartaal 4
lessons **7** and **10**.

## Kwartaal 1-3 — 19 lessons, and this is the bulk of what remains

| Sub-topic | Lessons | Note |
|---|---|---|
| `leer-van-leiers` | 4 | no current reports at all |
| `plaaslike-geskiedenis` | 5 | lesson 1 signed off; four untouched |
| `vervoer-in-die-lug` | 3 | coverage current on all three, facts on none |
| `vervoer-op-land` | 5 | mixed; lesson 3 has coverage + comparison approved |
| `vervoer-op-water` | 2 | lesson 2 has its comparison approved |

**30 individual checks outstanding** — 13 coverage, 17 facts. One lesson
(`plaaslike-geskiedenis` 1) is signed off.

`leer-van-leiers` and `plaaslike-geskiedenis` are the two blocks with nothing current,
and they are the ones to start with: nine lessons, eighteen checks, and no partial
state to reconcile first.

## What still owes a decision, not a check

* **The provenance-note leak** — the fact checker never gets the spec, but a writer
  records requirements inside the lesson file and the checker reads that. Three options
  recorded in [[die-herkoms-nota-lek-die-spek-na-die-feitenasiener]]; option 2 (the
  runner strips the note from the checker's copy) matches how the rest of the pipeline
  works. Drico's call.
* **A deliberate fact check of the reference example.** Four boiler wordings and a false
  piston definition were found in it by accident in two days, in the one file every
  writer in every subject copies from — see
  [[die-verwysingsles-word-nooit-nagegaan]]. One lesson's worth of claims, and the
  highest-leverage check available.
* **Kwartaal 4 lesson 11 sits about 27 words over its ceiling**, inside gate tolerance.
  Every other sentence there has passed two fact checks, and trimming confirmed content
  to hit a ceiling is what caused the finding it was fixing.

## After the checks, in order

Sign-off and PDF export per lesson, then the Afrikaans check (outside this pipeline,
and it will undo decisions not written into the protected-words file — see
[[onaantasbare-woorde-vir-die-taalnasiener]]), then the HTML build and the HTML check.

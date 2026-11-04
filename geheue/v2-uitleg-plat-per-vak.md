---
name: v2-uitleg-plat-per-vak
description: "V2 inhoud is laid out Graad N / PSW|Kuns|NW en Teg|Geskiedenis|Geografie / Les NN, numbered 1-x through the year, no sub-topic folders."
metadata:
  node_type: memory
  type: project
  originSessionId: 660119b3-6d4d-4eba-855b-7949cb3ca7d5
  modified: 2026-11-04T08:03:58.901Z
---

Lampies, 4 November 2026: `V2 inhoud/` is laid out for the HTML team as
`Graad N/<PSW|Kuns|NW en Teg|Geskiedenis|Geografie>/Les NN - titel.pdf`, with no
sub-topic folders.

- Lewensvaardighede splits two ways. PSW covers ontwikkeling van self, sosiale verantwoordelikheid and gesondheids- en omgewingsverantwoordelikheid. Kuns covers uitvoerende and visuele kunste.
- Sosiale Wetenskappe splits into Geskiedenis and Geografie by the spec's `dissipline` field.
- Numbering is 1-x per grade and subject.
  - It comes from the spec's `jaarnommer` first, then Drico's index in `kaps/lesindeks/`.
  - Gr 4 NW Term 4 (26-33) was added on 4 Nov from his own outbox names.
  - Lewensvaardighede has neither, so it is ordered by term, then strand (Uitvoerende before Visuele, the CAPS order), then lesson number.
- `bin/v2_inhoud.py` builds the folders. It refuses a group where only some lessons have a year number, and it deletes any PDF under a grade that is not a current delivery.

**Why:** the HTML team works per subject-year, not per CAPS sub-topic.

**How to apply:** `Voltooide lesse/` and `lees/` keep their own layouts. Only V2 is flat. See [[voltooide-lesse-uitvoer]] and [[lees-is-n-uitbak-nie-n-argief-nie]].

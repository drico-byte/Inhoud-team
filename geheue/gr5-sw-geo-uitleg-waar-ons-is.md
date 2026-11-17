---
name: gr5-sw-geo-uitleg-waar-ons-is
description: "Gr 5 Geography layout, started 17 Nov 2026: scripts for T1-T3 only (41 clips), layout proposed at 200/CAPS hour with History's merge rule = 32 texts, 7 100 words; awaiting Lampies."
metadata:
  node_type: memory
  type: project
  originSessionId: deedaf1a-4546-4aae-aaae-33d049877c50
  modified: 2026-11-17T10:56:37.208Z
---

**17 November 2026 — layout proposed, not approved.** Videos came first, as in Gr 5 History
([[gr5-sw-gesk-uitleg-waar-ons-is]], [[video-se-lesverdeling-wen]]).

**Scripts:** SharePoint `Innovasie - 0000HTML wolkskool lesse/Dump/Graad_5_Geografie_scripts`,
three of four chapters (Term 4 mining not yet made). Extracted to
`videoskrifte/gr5-sw-geo-hfstk{1,2,3}-*.txt` (uncommitted). Clips are LONG, unlike History's:
T1 16 clips (~7 300 words), T2 11 (~7 600), T3 14 (~6 100); average ~470 words a clip.

**CAPS hours (KABV SW 4-6, printed pp 25-28):** T1 2+4+3+3 = 12; T2 2+3+3+4 = 12; T3 weather 3,
project 2 (practical, no video), rain 2, climate 3, vegetation 3 = 13; T4 4+5+3 = 12.

**Book count (Lampies' sheet, numbers only):** Geography T1 1 108, T2 998, T3 1 888, T4 1 329 =
5 323, about 111 per CAPS hour - much thinner than History's ~157.

**Proposed:** 200/CAPS hour (History's rate), words held per cluster, History's rule that one
text may support consecutive videos when the budget cannot give each 200. T1 11 texts (2 400),
T2 10 (2 400), T3 11 (2 300: the project budgeted on its reading, 100 words, carried in the
first weather text). IDs G5_GEO_01-32; Term 4 from 33. Alternative offered: one text per
video, 41 texts, ~8 800.

**Script findings so far:** T1 video misses CAPS's big cities Cairo, Lagos, Nairobi and the
Maletsunyane falls (text carries them briefly, mandatory, not supplement); T1 clip 10 teaches
contour lines, which CAPS says not to include at this grade - text omits contours; video says
Eswatini where CAPS says Swaziland - follow the video (current name). No claim check run yet.

**APPROVED by Lampies, 17 Nov 2026,** with rulings: the T3 weather project is ignored entirely
(T3 = 2 200, total 7 000); CAPS items a video misses go INTO the lesson; content in a video
beyond CAPS is fine, but contour lines stay out of the text; "Eswatini (Swaziland)" once.
Sub-topic slugs: kaartvaardighede-afrika (NOT kaartvaardighede - Gr 4 and Gr 6 share that key
in the protected-words file), fisiese-verskynsels-van-suid-afrika, weer-klimaat-en-plantegroei.
Register kaps/lesregister/G5_GEO.csv and profiele/gr5-sw-geografie-profiel.json written (not
published, not committed). Claim checks: 5 files in videoskrifte/gr5-geo-nagaan/ (h1a, h1b,
h2a, h2b, h3), 54 problem claims routed by bou_video_naat.py into video_naat-per-les.json
(inject AFTER planners; planners told not to copy). Overruled flag: wêrelderfenisterrein stays.
Cross-term terms settled by me in BEPLANNER-OPDRAG.md: seevlak (seespieël once in 07),
punthoogte, hoofrivier = main river of a system only (Vaal/Olifants are sytakke),
Oranjerivier (Gariep), uKhahlamba-Drakensberg then Drakensberg. Three planners launched
17 Nov; then spec fact-check, repair at source, inject video_naat, approval.
**Specs done 17 Nov 2026 (evening):** three specs in spesifikasies/konsep/gr5/sosiale-wetenskappe/
(kaartvaardighede-afrika, fisiese-verskynsels-van-suid-afrika, weer-klimaat-en-plantegroei), all PASS
(T1 warns: lesson 8 has 12 items in 200 words, accepted). Spec fact-checks in logs/verslae/gr5/
sosiale-wetenskappe/<slug>/spek-feite.json: T1 1 false/1 misl/2 unsure of 82; T2 1/3/1 of 82; T3 0/6/1
of 68; each repaired at source by its own planner. video_naat injected after repair. AWAITING
Lampies' approval -> then move to goedgekeur/, commit, publish register, then writers.

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
**APPROVED + committed 17 Nov 2026 (f1d6edac, pushed), register published.** Lampies at approval:
"please dont limit the lessons to only 200. So if a lesson is too tight, then expand it a bit."
Raised: 3, 4, 7 -> 250; 8 -> 350; 9 -> 300; 12 -> 250; 13 -> 275; 22-24 -> 250; 32 -> 275 (clusters
over envelope declare kluster_uitsondering). T1 2 800, T2 2 525, T3 2 425 = 7 750. Drafting started
same evening in waves of 6 writers (T1 1-6 first); draft all 32, reconcile shared terms, then pipeline.
**Drafting notes 17 Nov:** writers cannot run the gate (no shell) - the runner gates later. T1 1,3,4,5,6
drafted. Fixed at source: les 1 "not on the ground" -> nobody drew the line; video_naat no longer pushes
wêrelderfenisgebied (rebuilt + reinjected); les 4 Madagascar/Zanzibar requirement sent to T1 planner.
For reconciliation/language step: oseaan definition (Gr 4 says five oceans; this spec forbids a count);
T1 les 3 uses "grond" for ground where "land" = country - protect before the language step; Cairo is
still the capital but Egypt is moving ministries (re-check at reprint); Abuja named in les 6 text, not on map.
More for reconciliation: "dam" = wall (this spec) vs the stored water (Gr 4 delivered); "reservoir" = Gr 4's town
storage tank, so T2 les 9 uses "damkom (reservoir)" with no glossary entry; stroomop/stroomaf, mond, hoofrivier,
rivierstelsel shared by T2 les 6, 7, 9; swaartekrag may exist in Gr 5 NWT; toerisme new; nedersetting and farms.
**17 Nov late: all 32 drafted; terms reconciled** (55 decided into the Gr 5 SW agreed list; change list in
videoskrifte/gr5-geo-nagaan/versoening-17nov.json; brief HERSIENING-OPDRAG.md). Key: dam = the water (Gr 4),
wall = damwal; reservoir widened (kept, my call); hoofrivier = river tributaries flow into that itself flows
into no other river; klimaat = Gr 4's wording; aanpassing widened to plant or animal; savanne without bioom.
My call: lesson 32 may give the NWT word (herbivoor/karnivoor) once in brackets. Writers revising in 6 groups;
still to send: T2 6,7,9 (spec fixed) and T3 10,11 (spec fix pending with T3 planner). Then gate -> language -> checks.
**17 Nov (night of 17th): all 32 PASS the first gate** (18 needed a writer round: mostly commas from place-name
lists; failures in videoskrifte/gr5-geo-nagaan/hek-1.md). Drift sweep: no drift, 74 shared terms over 77 lessons.
Next: three agents add writers' protected wordings to kaps/beskermde-woorde.json (BESKERM-OPDRAG.md), then
language finder -> reviewer per lesson (runner names them), gate again, then coverage + facts. Nothing new committed
since f1d6edac (drafts, agreed wordings, protected words all uncommitted).
Protected words added 17 Nov: T1 46, T2 58, T3 63 entries (+3 hedges by me). Language finders running 3 lessons
per agent (6 agents: T1 1-11, T2 1-7); T2 8-10 and T3 1-11 next, then reviewers. Pending writer items for
after the language step: T1 les 10 "Op die platteland" -> landelike gebiede (algemeen rule); T2 les 5
Tafelberg "plat soos 'n tafel" lacks lesson 3's hedge "amper"; "bouwerkers" kept over video's word (my call).
17 Nov: language step done for T1 1-11 and T2 1-7 (finder+reviewer, 3 lessons per agent works fine). Ready for
checkers: T1 1,2,3,5,6,9,11; T2 1,2,3,5,6,7. Writer items (once): T1 4,7,8,10 and T2 4 (one writer, incl.
platteland fix). Checkers launched: facts T1 1-2, coverage T1 1-3 (facts 2 per agent, coverage 3 per agent).
Finders running: T2 8-10, T3 1-6; T3 7-11 still to launch.
**17 Nov progress:** signed off + delivered G5_GEO_01, 02 (V3 library Graad 5/GEO/Inhoud); 03, 05, 06 signing.
T1 les 9 fact fail (only three well-known waterfalls; Tugela) -> writer + spec fixed. Reprint re-checks: T1 les 6
Johannesburg vs Cape Town size, Cairo vs new administrative capital. Carried language items for a person at
sign-off: T1 les 8 kruin glossary "hoogste, boonste" tautology. Pipeline pattern: finder/reviewer 3-5 lessons
per agent, coverage 4-5 per agent, facts 2 per agent, sign-off via runner --keur-goed (~60 s each, V2 rebuild).
Signed off by 17 Nov evening: G5_GEO_01,02,03,05,06,11; 04,07,08,10 signing. Coverage clean for all 32 (T1 9 re-check).
Fact repairs: T1 9 (waterfalls), T2 1 (Karoo: escarpment splits it; spec fixed). Reprint re-check also: Kilimanjaro ice.
Still to fact-check: T2 2-10, T3 all. T3 9 "savanne veral in die noorde" is unrequested - watch its fact check.
17 Nov late: 21 signed off (all T1; T2 12,13,14,15,16,18; T3 23,24,25), 26+27 signing. Cleared, waiting to sign:
T2 8 (G5_GEO_19), T3 7 (G5_GEO_28). In repair: T2 6 (catchment ridge), T2 9 (turbine), T2 10 (tar vs gravel,
erosion not 'slow'), T3 1 (forms of precipitation, re-check running), T3 8 (winter rain incl. west coast). Facts
still running: T3 9-11. Spec fixes today at source: Hermanus, Karoo, tar/gravel, winter rain west coast.
Protected list fixed: Hermanus entry (old 'groter deel' now forbidden).

**DONE 17 Nov 2026: all 32 Terms 1-3 lessons signed off and delivered** (Voltooide lesse + V3 library Graad 5/GEO/Inhoud,
32 PDFs each). Drift sweep: no drift, 74 shared terms over 77 Gr 5 SW lessons. Fact errors fixed at lesson AND spec:
waterfalls (only three), Karoo (escarpment splits it), Hermanus 'groter deel', tributaries/ridge, turbine, tar vs gravel,
erosion 'slow', precipitation forms, clouds all-water, winter rain west coast, small fynbos leaves, savanna map.
For a person (not blocking): kruin glossary tautology (T1 les 8) and one more language note on T1 les 4; "bedompig",
"binneland", "wolkdekking" not found in an online dictionary; reprint re-checks: Johannesburg vs Cape Town size, Cairo
vs Egypt's new capital, Kilimanjaro ice. Term 4 (mining) waits for its script; IDs from G5_GEO_33.
Gr 6 SW spek extracts were refreshed locally by vernuwe-uittreksels and left uncommitted (derived; other PCs).

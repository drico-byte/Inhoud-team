---
name: gr6-nwt-waar-ons-is
description: "Grade 6 NST started 22 Sep 2026: 26-lesson division agreed with Drico, band 450-550 (short lessons may go below with a recorded exception); next is specs per sub-topic."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-09-22T08:41:30.367Z
---

22 September 2026. Grade 6 Natuurwetenskappe en Tegnologie division agreed with
Drico: **26 lessons** (7 · 8 · 6 · 5), kept in `kaps/lesindeks/gr6-nwt-lesverdeling.csv`
and as the "Finaal" sheet of his `Les verdelings\Intersen NW Graad 6 konsep.xlsx`.
Built from CAPS printed pages 47-64 only (PDF 52-69); no textbook.

**Band 450-550** (Drico, 22 Sep 2026, the same as Grade 6 Life Skills). His concern
is the CEILING: over 550 means an effective split, not a trim. A lesson short for a
real reason (lesson 30, maybe 2 and 18) may go below 450 with a `vloer_uitsondering`
in its spec. The band table is now per subject (LESBAND_VAK) in gate.py and
spec_check.py, because Lampies had set Gr 6 LV's band the day before.

Drico's calls: merges 5+6, 7+8, 12+15, 13+14, 20+21, 22+23, 26+27, 31+32, 33+34,
35+36+37. **Lesson 30 (the Moon) stays its own, deliberately very short lesson.**
Lessons 2 and 18 are thin but kept. Lesson 3 (food groups) and 25 (coal + power
station) may split if the draft passes 550.

CAPS errors to correct at planning (mechanisms, not names): moons do NOT give off
their own light (lesson 30); liquid particles described like a solid's (10); the
Moon's spin called an "omwenteling" (33+34).

**NEXT STEPS (not started as of 22 Sep 2026, nothing running):**
1. Create `kaps/gedeelde-omskrywings-natuurwetenskappe-gr6.json` (vak + graad 6, empty
   `terme`) BEFORE any drafting, or the drift sweep reports no decision list.
2. Hand-write `profiele/gr6-nwt-profiel.json` like the Gr 5 one (no textbook measured;
   `begroting_basis: vereistes`), listing the sub-topics so hardloop.py finds them.
   CAPS pages for the bron note: printed 47-64, PDF 52-69.
3. Sweep the Grade 5 agreed wordings for terms Grade 6 reuses and decide scope first.
4. Run wolkskool-beplanner once per sub-topic (about 18: Fotosintese, Voedingstowwe,
   Voedselverwerking, Ekostelsels en voedselwebbe, Vaste stowwe/vloeistowwe/gasse,
   Mengsels, Oplossings as spesiale mengsels, Oplossing (tempo), Mengsels en water
   hulpbronne, Skoon water, Elektriese stroombane, Geleiers en nie-geleiers, Stelsels
   om 'n probleem op te los, Hoofstroom elektrisiteit, Die Sonnestelsel, Bewegings van
   die Aarde, Die beweging van die Maan, Stelsels vir die ruimte). Pass each planner the
   lesson split from the CSV, the band, the CAPS errors, and the lesson-30 exception.
5. Drico approves specs by moving them; then draft ALL 26 before finishing any.
Brief agents in plain English (Afrikaans briefs tripped false safety flags on 18 Sep).

Before drafting: settle every term Grade 6 shares with Grade 5 (voedselketting,
stroombaan, sel, kragstasie, steenkool, fossielbrandstof, as) — see
[[twee-beplanners-albei-plaaslik-reg]] and [[n-omskrywing-mag-oor-grade-heen-verbreed]].

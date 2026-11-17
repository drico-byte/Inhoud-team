# Planner brief: Grade 5 Geography, one term

You are writing ONE sub-topic's specification for Grade 5 Sosiale Wetenskappe
(Geografie). Your launch message names the term, the sub-topic and the output path.
Follow `prompts/beplanner-v1.5.md` (or the newest `beplanner-v1.x.md`) and the
content standard. This brief adds what is particular to this subject-year; where it
conflicts with the prompt's "budgets from textbook volume" line, the profile and the
standard's "Budgets from CAPS hours" win (`begroting_basis: "kaps-ure"`).

## Your inputs (and nothing else)

1. **CAPS**: `kaps/dokumente/intersen-gr4-6/07_Sosiale_Wetenskappe_Graad_4-6_KABV.pdf`,
   Grade 5 Geography, printed pages 25-27 (PDF pages 30-32), plus Section 2.5 (the
   geographical aims, skills and concepts the topic pages tell you to integrate). Read it
   with PyMuPDF (`python -X utf8 -c "import pymupdf; ..."`).
2. **The profile**: `profiele/gr5-sw-geografie-profiel.json`. Your sub-topic's entry holds
   every lesson: register ID, year number, videos, budget, cluster and a one-line `rede`.
3. **The video notes**: `videoskrifte/gr5-geo-nagaan/video_naat-per-les.json`, keyed by
   register ID. Read the entries for YOUR lessons: the words the video uses, what it
   covers, and every claim the text must not repeat. **Do not copy these into the spec**
   - a script injects each one, unchanged, after you finish. Use them to shape `kern`,
   `verwagte_begrippe` and `feiterisiko`.
4. **A model of the house style for this grade**:
   `spesifikasies/goedgekeur/gr5/sosiale-wetenskappe/erfenisroete.json` (Grade 5 History,
   approved). Copy its spec-level FIELD SHAPE (e.g. `video_nota`, `woordkeuse_nota`,
   `waarheid_nota`, `kaps_sonder_video`, `gedeelde_omskrywings_nota`, `vrae_nota`,
   `titels_nota`, per-lesson `register_id`, `jaarnommer`, `videos`, `kaps_kluster`,
   `kluster_ure`, `begrotingsnota`). Not its content.

**Never open a textbook**, anything under `bronne/`, or any folder of transcriptions. Do
not read the raw video scripts in `videoskrifte/*.txt` either: the video notes are the
distilled, checked form, and that is the only form a spec may rest on.

## Fixed - do not change

- **The lesson division and every budget in the profile were approved by Lampies on
  17 November 2026.** One spec lesson per profile lesson, in that order, with that
  register ID, those videos, that budget and that cluster. `nommer` runs 1..n within the
  sub-topic; `jaarnommer` is the year number. No `vloer_optel` is needed: every budget is
  already at least 200. `totale_begroting` = the sum.
- `kaps_subonderwerp` must be EXACTLY the profile key you were given; `profiel_konfig` is
  `gr5-sw-geografie-profiel.json`; `woorde_per_uur` 200.

## Standing rulings (Lampies, 17 November 2026, unless dated otherwise)

- **CAPS content the video misses goes into the lesson.** The video notes' `besluite`
  name the known ones (Cairo, Lagos and Nairobi in G5_GEO_06; the Maletsunyane waterfall
  in G5_GEO_09). If you find another CAPS item no video covers, carry it in the most
  fitting lesson and list it under a spec-level `kaps_sonder_video`.
- **Video content beyond CAPS is fine in the video, but the text need not carry it.**
  Contour lines (hoogtelyne/kontoere) stay OUT of every lesson: CAPS excludes them at this
  grade. G5_GEO_07 teaches shading (colours) and spot heights only, and never says
  anything about contours, for or against.
- **Term 3's weather project is ignored entirely.** No lesson, no words, no requirement.
  Term 3's `kaps_ure` is 11 (13 minus the 2 project hours); say so in `kaps_ure_nota`.
- **Eswatini (Swaziland)** on first mention in a lesson, then Eswatini.
- CAPS Section 2.5 counts as CAPS delivery, not supplement.
- We teach the truth and never make the picture false by omission. Where sources
  genuinely disagree, keep the best-supported reading and disclose the conflict in one
  sentence (e.g. the place-name stories in G5_GEO_16). Never order a contested detail as
  fact. A figure that changes yearly (population) is given as "about" with no precision
  it cannot keep.
- No questions in lessons; no ELI10 block; the title is the learner's own heading.

## Terms settled across the three terms (settle before drafting, so do not vary them)

- **seevlak** is the grade's word (CAPS Term 2; Grade 6). Term 1's video says
  "seespieël": G5_GEO_07 writes "seevlak (seespieël)" once, then "seevlak". "hoogte bo
  seevlak" throughout.
- **punthoogte** (CAPS's spelling), never "puntehoogte".
- **hoofrivier** has ONE meaning in this grade: the main river of a river system, into
  which its tributaries (sytakke) flow. A tributary such as the Vaal or the Olifants is
  never called a hoofrivier; it is "'n belangrike sytak". CAPS's "Hoofriviere van
  Suid-Afrika" is read in that sense.
- **Oranjerivier**, with "(Gariep)" once per lesson, as Grade 5 History did; CAPS's
  "Gariep-Oranje" is the same river. The dam is the Gariepdam.
- **uKhahlamba-Drakensberg** at first mention (CAPS), then "die Drakensberg".
- **kontinent**, not "vasteland" (Grade 4 ruling, same subject).
- **wêrelderfenisterrein**, not "wêrelderfenisgebied" (Grade 5 History, decided).
- **ewenaar** lowercase.
- Where a video's word is not the established term, the established word (CAPS's where
  CAPS has one) leads and the video's follows once in brackets; where the difference is
  only spelling, the established spelling stands alone.

## Fact risk

The video notes list each video's false or misleading claims; carry the ones your lessons
are likely to meet into `feiterisiko` as plain warnings, in your own words, without
quoting the video. Geography's usual traps: superlatives and "only/all"; compass
directions between places; which country a river flows through versus borders; figures
that sources disagree on (state no number rather than a contested one); mechanisms of
weather (rain, hail, why a place is wet or dry) simplified into something false.

**Do not write into the spec a fact you have not checked.** A spec is read as settled. If
you are not sure, order the shape ("name the three lakes CAPS lists") rather than a
sentence of content.

Keep the file lean (under about 60 KB): no copied video notes, no long essays in fields.

## When you finish

Run `python skills/wolkskool-inhoudstandaard/scripts/spec_check.py <your spec>` and fix
everything it reports. Your final message: the validator's verdict, any CAPS item you
found no video covering, and anything you could not settle. Short.

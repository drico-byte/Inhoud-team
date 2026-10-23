---
name: taalrondte-en-gapings-gr4-6
description: Lampies 22 Oct 2026 - run our own language step over all 338 Gr 4-6 lessons and fill the CAPS-audit gaps in the same pass; 10 lessons at a time; decisions listed with Lampies' answers
metadata:
  type: project
---

**Lampies, 22 October 2026:** run the full in-pipeline language step (taalvinder,
taalkeurder, taalstap, second gate) over **every signed-off Grade 4-6 lesson, 338 in all,
starting from the repository text**, and fill the CAPS audit's gaps in the same pass, so
each lesson is checked once. Grade 7 is out of scope until it is finished. The ChatGPT
language edits in the HTML team's `2_PDF` are replaced by ours, not ported.

**Pace: up to 10 lessons at a time** (this PC's tokens reset that morning; top priority).
**Raised to 15, Lampies 23 October 2026.** Keep two lessons of one spec file out of the writer at the same time, and spread across sub-topics.
This overrides [[drie-lesse-op-n-slag-op-hierdie-rekenaar]] for this job only.

**Per lesson:** a gap -> fix the approved spec at source first, refresh extracts, writer.
Then the runner: gate, language step, gate, then coverage and facts, then sign-off and PDF.
A lesson with no gap gets the language step only. The runner SKIPS the language step for
lessons signed off before it shipped, so it needs a way to force it (tool change, before
starting).

**Order:** first the 22 lessons changed after ChatGPT's check (Gr 4 PSW self 3 body
safety first, then self 5, 11, social responsibility 5, 6; Gr 4 Science 4, 12, 15, 16;
Gr 4 Arts performing 3, 4, visual 1-4; Gr 5 PSW 7, 8, 9; Gr 6 Science 4; Gr 6 PSW 3, 5,
11) and the 13 unfinished ones (Gr 4 Science 1-5, 9, 12-16; Gr 5 PSW GO 8; Gr 6 PSW GO 5).
Then subject by subject.

**Sources:** the audit's work list is `<subject>/rapport.json` (`changes`: add / fix /
decide) in `...Innovasie - 0000HTML wolkskool lesse/Dump/CAPS-oudit/CAPS-oudit-werklêer/`;
the handover and version check sit one level up. The audit quoted language-edited text,
so find each sentence by meaning. Items marked DELIBERATE stand unless a ruling below
changes them. See [[caps-oudit-gr4-6]], [[caps-oudit-herstel-stand]].

**Decisions:** Lampies chose to decide the ~18 audit decisions themselves. Answers are
recorded below as they come.

- **3. Design tasks (Gr 4 and Gr 6 Science): NO.** Planning and judging a design (what it
  must do, what limits it, how to test it) is left to the teacher in class. No block added.
- **4. Examples CAPS names (Gr 5 Science lesson 21 and others): NO.** Examples CAPS lists are
  not forced; our own examples stand. The rubber-band aeroplane and jack-in-the-box are not
  added.
- **1. Creative Arts key terms, Gr 4-6: YES** - short definitions in the theory lessons.
- **2. Tables and graphs: YES** - one short worked example per subject-grade where CAPS asks
  (Gr 4 Geography, Gr 5 Science, Gr 6 Science, Gr 6 Geography population); a graph is a
  block saying what it must show, the HTML team draws it.
- **5. Gr 4 Science, dead things: NO** - dead and non-living differ; our lessons keep
  teaching the difference. The plan's order stands.
- **6. Gr 4 History 'geskiedenis': YES** - widen to change over time AND finding out from sources.
- **7. Gr 4 History local area: NO.** **8. Exhaust-gas case study: NO.** **9. History writing: NO.**
- **10. Gr 4 Creative Arts instrument families: YES** (on my strong recommendation) - CAPS's
  four ways of grouping, lessons 1 and 2 made to agree.
- **11. Gr 4 Geography map blocks, lessons 14 and 19: YES** - then ask the HTML team whether
  their maps already cover it.
- **12. Gr 4 Geography urban farming: YES**, one sentence. **13. Xhosa house names: KEEP.**
- **14. Gr 4 PSW morals: NO.** **15. Gr 5 PSW cultural contexts: NO.**
- **16. Gr 6 Geography population graph and city sizes: YES** (Census 2022, source and year).
- **17. Gr 6 Arts one named ritual: YES.** **18. Gr 6 Arts kwaito also a dance: YES.**

**Further rulings, Lampies 22 October 2026 (before restart):**
- **Videos.** Only Gr 4 Science 1-17 have finished videos; Lampies recreates every other
  video from the V2 PDFs. So: no change to Gr 4 Science 1-17 may contradict its video
  (scripts in `...Innovasie - 0000HTML wolkskool lesse/4_Scripts/Graad 4 NW/`, read the
  AF.docx). Arts/PSW/Gr 5 scripts are NOT videos yet - decision 10 stands; list which
  scripts the changes make outdated. Gr 4 SW keeps its teacher-made videos and video_naat.
- **Gr 4 Science 6/7 habitat:** one sentence that a school field can be a habitat too
  (fits the video: a hole is a place INSIDE the habitat; never call under-a-stone a habitat).
- **Gr 4 Science 31 and 32:** Lampies did not follow the question. Lesson 31 = the audit
  wants learners to record the Moon's shape each night with the date (classroom activity);
  lesson 32 = one closing line per Moon story on what the Moon means to people, maybe a
  South African story instead of the Maasai one (close to decision 14, which was NO).
  **Lampies: SKIP BOTH** (22 October 2026). Neither lesson changes for these points.
- **V2 folder:** every re-signed lesson's PDF goes to a new `V2 inhoud/` folder in the
  repo (same Graad/Vak/Subonderwerp layout as Voltooide lesse), plus a list of every lesson
  that changed and why.
- **Items the language check holds for a person: I settle them ALL** under existing
  rulings. Only bring Lampies something that really needs them.
- **Commit and push after each subject is finished.**
- **I take over everything created in Gr 4-6**, including lessons other sessions started
  (e.g. the uncommitted Gr 6 LV GO lesson 3 from the CAPS-audit session).
- **First step after restart:** a way to make the runner run the language step on lessons
  signed off before it shipped (it SKIPS them today: `_voor_die_taalstap` in hardloop.py).

**Progress (22 October 2026, evening).** Runner flag `--met-taal` built and tested (forces the step on pre-step lessons, remembered by hash). Batch 1 = Gr 4 PSW self 3, 5, 11, SR 5, 6; Gr 4 NW 3, 4, 12, 15, 16 (Arts performing 3 moved to an Arts batch: decisions 1 and 10 need Performing Arts 1-4 planned together). 9 of 10 signed off and in `V2 inhoud/` (list: `V2 inhoud/Veranderinge.md`, gaps by hand in `gapings.json`, script `bin/v2_inhoud.py`); NW 16 in its last round.
**What batch 1 taught:**
- Gr 4 NW specs are full of stale orders: each coverage round found a new one. Do a whole-entry stale-order sweep per spec BEFORE the writer, not piecemeal.
- Gr 4 NW videos say many over-broad things (all listed in the open-points list for Lampies). Rule used: the text ROUTES AROUND the video (narrow to the dog / your back / the adult insect; 'baie', 'party'), never "nie elke" and never correcting the video.
- Every writer bounce = a new draft = another full language round. Protect every narrowing in `kaps/beskermde-woorde.json` the moment it is made, or a language edit widens it back (happened with 'op sy ente').
- The finder used to see only the last round's applied changes; now it sees applied and dropped across all rounds (taalstap.py + hardloop.py).
- Safety fix made under ruling (b): Gr 4 self 3's other-child rule was conditional ('as 'n speletjie of 'n geheim'); now unconditional with one care exception. Tell Lampies; check Gr 5/6 body-safety lessons for the same form.
- Shared 'ru-olie' wording changed ('dik' out): year lesson 20 must go through the writer. 'stut' shared wording kept; lesson 16 calls real truss members 'dun dele' instead.

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

**Stand, 23 Oktober 2026 (aand, Lampies pak op).** V2 = 98 lesse.
- Gr 4 Lewensvaardighede: klaar, behalwe GO 5 (vraag 19) en Uitvoerende Kunste 1 (vraag 12). Gestoot (3262f6d2).
- Gr 4 NW: 26/33; die ander 7 wag op vrae 13-16, 18.
- Gr 4 SW Geografie: 24/30 herteken. Oop: kaart 2, 5, 6 (skrywer-herstelwerk; die kaartspek is reggemaak vir les 2 en 6), water 3 ('siklus'-omskrywing), water 4 (wag op vraag 21: 'stroom'), plekke 4 (teerpaaie-sin). Elkeen moet na die skrywer weer deur die hele volgorde: hek, taal, hek, nasieners.
- Gr 4 SW Geskiedenis: 6/30 herteken (vervoer-op-land 1, 2, 4, 5; kommunikasie 5, 10). Die ander 24 wag op vraag 20 (Drico se harde plafon).
- Werktuig: taalnasien.py beskerm nou video_naat se woorde outomaties (CLAUDE.md bygewerk). Nog nie gestoot nie.
- Lesse: 'n waarskuwing in kern word 'n bestelling (memory n-waarskuwing-in-kern-word-n-bestelling); 'n regstelling wat ek vir 'n skrywer bewoord, is 'n nuwe bewering; beskermde woorde wat diakritiese tekens verloor het, pas nooit (bakteriee); hou-velde met hakiesnotas pas nooit.
- Lopende notas: scratchpad oop-punte.md (VIDEO-lys vir Lampies, gr 4 SW-spek-veeg kandidate).

**Oop punte uit die sessie se notas (gekopieer 23 Oktober 2026, want die kladblok verdwyn):**
  - VIDEO (Lampies' call): Gr 4 NW 03 video says "By die meeste varings lê die stingel onder die grond, en daarom sien jy dit nie." Fact check: sources conflict on "most"; "daarom sien jy dit nie" too strong. The text now routes around it (sentence cut), neither repeating nor correcting.
  - Settled by me (minor, not worth a full round): SR 5 'preekstoel' glossary "met die mense praat"; self 11 'klik' glossary stacked om..te; self 11 Childline-flow ordering flag.
  - VIDEO (Lampies' call): Gr 4 NW 04 video says every vertebrate's skeleton is "beentjies en kraakbeen" (shark: all cartilage), "elke werwel het 'n gaatjie" (not tail), insect's "hele liggaam ... harde laag" (not larvae), dog "dra sy harde dele binne" (claws, teeth). Text routes around (tied to the dog / your back / adult insect).
  - VIDEO (Lampies' call): Gr 4 NW 16 video says every kragmas is a steel frame of triangles (Eskom uses steel and concrete poles), "die stutte van 'n geraamte staan nie in driehoeke nie" (uncertain), "jy sien die dakkap gewoonlik nie" (uncertain in SA), and uses the withdrawn geraamte wording "die harde raam binne-in 'n dier se lyf". Text routes around.
  - VIDEO (Lampies' call): Gr 4 NW 12 video says paint "is ook van ru-olie gemaak" (only the binder is) and "die koppie en die bord in julle kombuis is albei van klei gebak". Text routes around.
  - VIDEO (Lampies' call): Gr 4 NW 04 video says "Ongewerwelde diere het net een ding in gemeen: geen ruggraat nie" - false literally (all eat, grow, breathe). Text now limits it to body build. Drico's own design ruling ordered the unqualified form; spec amended 22 Oct.
  - VIDEO (Lampies' call): Gr 4 NW 13 "'n klein lappie suig water net so goed in as 'n groot lap" (over-broad; text routes around); "Jy druk nie 'n duik in droë hout nie" (balsa; low risk). Gr 4 NW 09 "En die lug, 'n gas, vul die hele bottel" said with water already in the bottle (loose); its own maker's note: the third sorting question is never answered for solids.
  - VIDEO (Lampies' call): Gr 4 NW 01 says "Elke lewende ding voer al sewe lewensprosesse uit", "Elke lewende ding word groter en sterker", "...kan nuwe lewende dinge van sy eie soort maak" (false for individuals), "...beweeg self" (bread mould does not); uses 'voortplanting' where CAPS/text say 'reproduseer'. Gr 4 NW 05 says "Lig is dus nie wat 'n saad laat ontkiem nie" (some seeds need light). Text routes around.
  - VIDEO (Lampies' call): Gr 4 NW 09 balloon "Hy voel vol en hard" (it is springy, ~5% overpressure) and "Die knoop hou die lug binne, solank die ballon toe bly" (air seeps through rubber). Gr 4 NW 13 "Glas is styf, en tog kan dit breek wanneer 'n bal daarteen slaan" as the stiff-not-strong example (glass breaks because it is brittle; by the lesson's own pull test glass is strong). Text routes around both.
  - VIDEO (Lampies' call): Gr 4 NW 13 "Droë hout is hard" (balsa dents) and "'n klein stukkie droë hout is net so hard as 'n groot plank" (kinds differ); NW 02 "die rivier maak nie sy eie kos nie" (a dog doesn't either). Text routes around.
  - VIDEO (Lampies' call, add to the page's video table): Gr 4 NW 8 video says a nest is always built from carried material (ostrich/woodpecker), a skulp is a snail's, the thorn-branch kraal is a frame (branches heaped, not joined), and a kraal is bigger than a stable. Gr 4 NW 11 video says snowmelt "fills the rivers" (Drakensberg rivers are summer-rain fed), a cloud is droplets only (ice too), and "the four changes" (sublimation/deposition exist). Text routes around all of these.
  - VIDEO Gr4 NW 08 (skuilings): fact check contradicts three things the video says: the hollow tree trunk "vorm ook 'n dop" (a hollow trunk is a thick wall, no source calls it a shell); the kennel "'n raam met 'n dop daaroor" (planks are a covering, not a shell); and the shell definition lacks "thin, strength from shape" (so a stone wall fits it). Text routes around: shell examples now snail + wasp nest, kennel = frame with a covering, definition gains "thin". Video not corrected. -> Lampies (video list).
  - Settled by me at sign-off: SR 3 'amptelike taal' definition (wat-ambiguity; natural reading clear, not shared) keep; GO 7 'skoonmaakveldtog' "Wanneer mense saamwerk..." definition style, keep. SR 3 woordelys still lists 'Maleier-kookkuns' (text now 'Kaaps-Maleise') - fix on next writer pass.
  - kaart 4 uses P for parking ('op baie kaarte'), not H for hospital (H only on road signs).
  - SW History spec sweep candidates (not done): kommunikasie 5 kern[1] (3 records no marker); vervoer-op-land 2 kern[2] (5 corrections, duplicate SOMMIGE order), vervoer 2 kern[0], vervoer 3 kern[0] (ELI10 mix). Run verouderde-bestellings.py --vak "Sosiale Wetenskappe" --graad 4 when History resumes (Q20).
  - QUEUED writers (wait until plekke 1 / water 1 writers finish): water 2 FACT: 'te min om dit te proe' -> narrow (gewoonlik); fresh water up to ~1000 mg/L, taste from ~200-300. plekke 3 FACT: 'lyk tog meestal verskillend' -> narrow to match heading (nie altyd eenders nie); standard school plans. plekke 3 spec fixed (fokusvraag_skakel, titel_nota, geografiese_konsepte[1]).
  - Settled: vervoer-op-land 5 'minibus-taxi' glossary 'teen 'n prys ry' vs 'teen betaling' (shared/protected term; style only) - keep. water 1 daily-uses "one short list sentence" note vs 7-sentence block (passed checks) - keep.
  - VIDEO list for Lampies (Gr 4 SW): kommunikasie 5 video says everything was handwritten before the typewriter, no printers, a mistake meant starting over (all false; text routes around). Plus earlier: donkey thirst + stubborn (vervoer-op-land 1), 'buitedorp' (settlements), fresh water 'no salt', hail in cold areas, 'reservoir' two senses.
  - kaartvaardighede: 16 fields corrected several times never rewritten (les 8 kern[3] x6, kern[5]; les 2 kern[0] x5 ...). Sweep later. kaart 7 kern[3] minor mismatches ('ELKEEN VERSAG', 'een kort sin' vs two).
  - kaart 4 'simbool': draft 'soos 'n prentjie, 'n letter of 'n kleur' vs agreed '...soos 'n teken of 'n woord' - check voorbeelde_mag_verskil when kaart 4 writer runs.
  - QUEUED: voedsel 4 writer (map: maize FS+NW+Mpumalanga Hoeveld; cattle EC+KZN+FS+NW; spec kaart field fixed) - start when voedsel 5 writer is done.
  - Remaining Geo gap lessons not yet written: plekke 5, 7; kaart 4, 8; water 9. (kaart 4: P for parking 'op baie kaarte'; simbool voorbeelde_mag_verskil)
  - QUEUED water 5 writer (after water 9 writer): (1) "Dit word elke maand moeiliker" -> al hoe moeiliker (month 1 still full); (2) "Ons kan nie vooraf weet wanneer of hoeveel dit gaan reën nie" -> narrow (not far ahead / not for certain; forecasts exist); (3) staafgrafiek: 'hoër' -> 'langer' staaf (horizontal bars).
  - QUEUED voedsel 5 writer (after voedsel 4 writer; language bounce, no revision): fix 'meule' entry word order ('tot meel fyngemaal word'); check: path names one 'fabriek' while next sentence says two (meule + bakkery) - make consistent; CAPS chain plaas-fabriek-winkel-huis.
  - QUEUED plekke 2 writer (after plekke 7 writer): FACT "Daarom bepaal elke plek grootliks watter soort werk die mense daar kan doen" false for cities -> narrow to 'dikwels', mainly farms/villages (spec kern[0], fokusvraag_skakel, titel_nota fixed). Optional clarity: maize reaches shop via silo/mill as maize meal.
  - Settled: 'fabriekswerkers' (AWS, with s) over the video's 'fabriekwerkers' spelling. water 9 protected sentence updated to the lesson's shorter form. water 5 spec kern[0] 'nie SEKER weet'.
  - Remaining Geo gap lesson not yet started: kaart 8 (Pasifiese Oseaan once + atlas). Start after kaart 4 is out of writer (it is now - in finder).
  - (Die QUEUED- en Remaining-reëls hierbo is almal reeds afgehandel; die huidige oop lys is die Stand-paragraaf. Die VIDEO-lys en die spek-veeg-kandidate is nog oop.)
- **Om te hervat (23 Oktober aand):** water 3 en plekke 4 is deur die skrywer (siklus-omskrywing; teerpaaie) maar NOG NIE deur die hardloper nie - begin met hardloop.py op albei. Plekke 4 se spek sê nog 'meestal' (teerpaaie) in twee velde: wysig by die bron. Kaart 2 (aardbol: mense het name EN grense bygevoeg), kaart 6 (noordpyl, nie kompasroos nie) en kaart 5 ('bo-aan die rooster') wag nog op die skrywer; die kaartspek is reeds vir 2 en 6 reggemaak - voer eers vernuwe-uittreksels.py uit. Kaartspek les 2: een veld met vier rekords sonder merker; les 6: twee velde verbied steeds om te sê waar die naald wys.

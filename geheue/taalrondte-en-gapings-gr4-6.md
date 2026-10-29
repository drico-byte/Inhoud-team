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

**Gr 5 Lewensvaardighede begin, 23 Oktober 2026 (aand).** KABV-oudit se items is in die vyf spesifikasies geskryf (GO 1, 2, 10, 13; OvS 5 'tragedie'; SR 1 vierstap-plan; UK 1-4 hoorbare kenmerke, timbila melodies, TV-tegniek, sleutelterme; VK 1-4 slotblok oor eie en 'n maat se werk, 'n gekerfde figuur, Dürer se *Stag Beetle* as kandidaat, plaaslike omgewing). Ek het besluit (onder bestaande reëls):
- 'vorm' kry GEEN 3D-betekenis nie (beslisde gedeelde bewoording, Gr 4-6; die 3D-sin hoort by KABV se praktiese onderwerp, wat ons nie skryf nie).
- Gr 5 'timbila' na 'hol dop' oorgedra, soos Gr 4 se feitetoets-regstelling van 22 Oktober.
- 'krag' as dans-element beskerm onder uitvoerende-kunste ('energie, nie krag nie' is 'n wetenskapreël).
- UK 1: die spek se nota oor waar refleksie geleer word, is genoeg; geen lessin nie (geen ruimte nie).
- VK-begrotings 1600 na 1770 aanvaar (vereistes-basis; die KABV-oudit voeg vereistes by).
- 'tragedie' en die nuwe UK-sleutelterme: na die feitetoetse in die Gr 5 gedeelde lys sit.
- Kaart 5 (ruitverwysings) beskryf 'n bepaalde kaart (skool by B2, park by C3, 'n dam, 'n kliniek, letters A-C langs die kant) maar het geen kaartblok nie. Die HTML-span se kaart moet daardie besonderhede presies dra, of die sinne word vals. Vir Lampies/die HTML-span.

**Open after Gr 5 LV (23 Oct 2026):**
- Two Grade 4 shared wordings that Grade 5 performing arts lesson 1 must use word for word are unclear when the glossary entry is read alone:
  - toonkleur "al klink dit ewe hoog en hard" has nothing to compare with;
  - hosho "met sade binne, in pare geskud" can read as the seeds shaken in pairs.

  Fix them in Grade 4 and Grade 5 together, through the writer, after the Gr 5 pass. Never fix one grade alone.
- Gr 5 health lesson 12 still spells 'damp-toestelle'. The spec and the protected list now say 'damptoestel' as one word, and lesson 12's own language pass should apply it.
- About 14 approved specs across Gr 4-6 still describe the language check as running outside the pipeline. Most of these are only reasons for a protected word, so the conclusion still holds. Sweep them when there is time.
- Gr 4 Life Skills, social responsibility, lesson 3 (signed off) uses 'manier van lewe' in its study block and its kultuur definition. Gr 5 performing arts lesson 4 now says 'leefwyse'. These are different grades and not a shared term, so the difference is allowed. Consider aligning them at the next Gr 4 reprint.
- Gr 5 health lesson 12, the dagga sentence: it is correct on 23 Oct 2026, but the 2024 cannabis act is not yet fully in force. Re-check it at every reprint, as with Childline's number.
- Gr 5 social responsibility lesson 2 (Nkosi Johnson): 'Ma's en kinders woon daar vandag nog saam' will date. Nkosi's Haven nearly closed in 2018 and 2020, and a 2024 source says it still runs. Re-check at every reprint.
- House style: a title before a name is lower case inside a sentence (tant Rosa, juffrou Mans), per the AWS. Gr 5 OvS 6 and 8 follow it; OvS 4 and SR 4, 6 (signed off) still use capitals. Fix them at their next revision; it is not worth a cycle on its own.
- Gr 5 OvS 8: 'net soos hy belowe het' refers to a promise the story never shows; Sipho only asks whether Thursday suits. The fact check passed it. Look at it at the next revision.
- Shared wording 'roep-en-antwoord' ('... 'n kort deel en 'n ander antwoord daarop') joins two full clauses without the AWS comma. Add it in the shared list and route every lesson that uses it through the writer, together with the hosho and toonkleur fix.

**Stand, 23 Oct 2026 (late).**
- **Gr 5 LV:** 35 of 40 lessons re-signed. Still in flight: SR 2, 10 and 11. Waiting on a person: GO 9 (Q1/Q2) and UK 2 (Q22, massa).
- **Gr 5 NW:** the audit orders are written into the specs. There are 7 gap lessons: Voedselkettings 1, Gebruik van metale 1, Verwerkte materiale 2, Gestoorde energie 1, Energie en elektrisiteit 2, Oppervlak 2 (the one table and graph), and Fossiele 3. The other 22 lessons are language only. Three coordinators are running 15 lessons.
- **Fact checks:** web search is capped at 200 per turn across one agent tree. A coordinator stops when its tree runs out and sends me the fact paths. I then launch fact checks from fresh agents.
- Gr 5 SR 11: "Die Adams-gesin ... hulle vas elke jaar 'n hele maand lank" may read as the whole family fasting, but only the adults fast. The fact check passed it. Also 'vollemaan' (SR 11) against 'volmaan' (SR 10). Look at both at the next revision.
- Gr 5 SR 10 spec: the note at the top still says the Gr 5 shared list is empty on purpose. The list has since been filled; correct the note at the next spec touch.
- Shared Gr 4/5 wording 'smelt' ('Wanneer 'n vaste stof warm word ...') uses an English 'is when' calque. Fix it in both grades together, with hosho, toonkleur and roep-en-antwoord, after the pass.
- Gr 5 NW reprint checks: the paraffin claim in fuel lesson 1 and the coal share in electricity lesson 2. Re-check both at every reprint.

**Stand, 24 Oct 2026 (night).**
- **Gr 5 NW:** 29/29 re-signed and pushed (cf36cf5f).
- **Gr 5 LV:** 38/40. Still waiting: GO 9 (Q1/Q2) and UK 2 (Q22).
- **V2:** 168 lessons.
- **Next:** the Gr 6 subjects. Before each subject:
  - grep its approved specs for "BLY GELD" and "[OORTREFDE" and have an agent rewrite those fields, orders first;
  - write the audit orders into the specs;
  - then run coordinators of about 5 lessons each.
- **How the fact checks run:** one coordinator agent tree has about 200 searches. When the tree runs out, I launch the fact checks myself from fresh agents.

**Gr 6 NW, 28 Oct 2026.**
- **Specs prepared.** GAP lessons: Oplossing 1 (table and bar graph) and Hoofstroom 1 (fossil fuels from plants and animals). Voedingstowwe in voedsel 1 is also a writer lesson: its spec now orders lesson 4's sorting rule (main nutrient, food goes where the list puts it), and its draft still teaches the job-based and "good source of" rules.
  - Why: this aligns the two lessons; it does not correct a fact finding. One year must give one rule. Lesson 4's rule is the one that was fact-checked.
  - Open: no shared-list entry for the sorting rule yet. It lives only in protected words.
- **Protected words.** 76 wordings were protected from writers' notes for Fotosintese 1-2, Voedselverwerking, Ekostelsels 1-2, Mengsels en water 1-2, Verwerking 1, Stroombane and Geleiers.
- **Usage limit.** The weekly limit was hit on 24 Oct and reset on 28 Oct. Six agents at once spends it fast.
- **Gr 6 LV specs prepared, 28 Oct.**
  - **GAP lessons:** GO 3, OvS 7, SR 9 and 11, all four UK and all four VK.
  - **Language only:** GO 1, 2, 4, 6-8; OvS 1, 2, 4, 6, 8-10, 12; SR 1-8, 10, 12.
  - **Wording rules for the writers:**
    - SR 9 must fit 600 and OvS 7 its 616 ceiling. If either can only fit by dropping a requirement, it is a person's call: stop and say so.
    - In the shared list, 'konflik' now has two meanings, PSW and drama; the drama one is Gr 5's checked sentence. 'ruimte' is marked with two meanings, but only the VK sentence is decided. The dance sentence is added after UK's fact check.
- **Gr 6 SW specs prepared, 28 Oct.**
  - **GAP lessons:** Kaartvaardighede 3, 7; Klimaat 8; Bevolking 2, 3, 7; Mapungubwe 1, 2, 4, 5, 8; Ontdekkers 1; Demokrasie 1, 4; Medisyne 1, 4. The other 57 lessons are language only.
  - **Before the pass:** protect about 8 wordings in Ontdekkers, 4 in Kaartvaardighede 9 and 'alleen' in Demokrasie 6. Fix the stale 'bekende dorp' entry in Mapungubwe 3.
  - **My calls under existing rulings:**
    - Audit top-ups are declared in kluster_uitsondering: fine.
    - Johannesburg stays on the Bevolking 7 city map, with no 10-million class boundary in the key.
    - Handel 2's exports and imports widen to goods AND services, because lesson 4 teaches services sold abroad. Incomplete is fine, a false contrast is not. Fix at source and send through the writer during the pass.
  - **To check in the pass, not yet decided:**
    - Whether the "reg is never the law" ruling reaches Demokrasie 5's "met die reg" and the shared 'wet' wording.
    - Medisyne 10's holistic-versus-herbal contrast.
    - Draft faults: Demokrasie 3 makes "party of onafhanklike kandidaat" exclusive; Mapungubwe 3 is missing a "nie"; Mapungubwe 2's dates disagree with its own spec note.
- **Gr 6 NW fact repairs, 28 Oct, all narrowed at source:**
  - Fotosintese 1: cheese only as gewone blokkaas.
  - Vaste stowwe 1: no claim about what a drawing shows; particles stay as many and as big; three things change.
  - Mengsels en water 1: wateroordraagbare siekte narrowed to kieme in the shared list.
  - Mengsels en water 2: "onder andere op twee maniere".
  - Verwerking 1: take, aanwysings op die pakkie, kieme without 'die'.
  - Voedselverwerking 1: the amasi heading is narrowed to its benefit, and the CAPS "voedingswaarde" frame stays.
  - Mengsel definition spelled 'saamgemeng'.
- **New question for Lampies (Q23, add to the page):** the shared lists for Gr 5 and Gr 6 define 'elektrisiteit' as "a way energy is transferred". But Gr 6's 'stroombaan', 'oop stroombaan' and 'geslote stroombaan' use it as the thing that flows ("waarlangs elektrisiteit loop"). That is two meanings in one grade. For now, Stroombane 1 was fixed narrowly: the "energy given off versus electricity goes round" contrast clause is dropped. Whether to change the definition (Gr 5 delivered) is Lampies' call.
- Oplossings 2: the count of known separation methods is cut (lesson 9 teaches five), and so is the claim about the meaning of 'herwin' (no Afrikaans dictionary reached). Ekostelsels 1: 'klipmossel' becomes 'mossels'. Ekostelsels 2: the "jy het in graad 5 geleer" framing is cut.
- **Gr 6 NW, open items for later:**
  - The glossary definitions of 'deursigtig' and 'troebel' open with "Wanneer" (adjective defined as a clause). Fix in a glossary pass.
  - Shared 'sirene' says "harde klank", while the Stroombane spec warns against loudness claims.
  - The "kan ... dra" wording for germs (finder prefers "bevat") is protected in Verwerking 1.
  - Gr 6 NW 'Sonnestelsel': the lessons capitalise it, but the shared-list headword is lowercase. Settle the AWS form once, across Gr 5-6. Until then, keep the capital in the text.
  - Gr 5 NW 'steenkool' ('n Harde swart klip...) is false for lignite. Gr 6 narrowed it on 28 Oct. Gr 5 energie-en-elektrisiteit 2 and gestoorde-energie-in-brandstof 1 still carry it and need the writer plus a reprint.
  - Gr 5 NW 'substasie' ('groot toestelle') clashes with 'toestel'. Gr 6 changed it to 'masjiene' on 28 Oct. Gr 5 energie-en-elektrisiteit 2 and 3 need the writer plus a reprint.
  - Gr 6 NW Mengsels 1: the comma before 'of' in 'Die verskil kan in hulle grootte of kleur lê, of daarin dat een van hulle sink' may break the AWS rule (the second part is not a full sentence). Fix at the next revision.
- **Gr 6 NW, 28 Oct:** the CAPS line for the Moon (p. 66) leaves out 'nie' ("mane ... gee hulle eie hitte en lig af"). It is marked [sic] in the Sonnestelsel spec.
  - Also open: the shared 'as' entry has omskrywing null, with Drico's wording only in the nota. The guard and the extract therefore don't see it as a shared definition. Moving it to omskrywing is a decision about Drico's Gr 5 open term.
  - Gr 6 NW Hoofstroom 3: 'Hulle raak nie op nie, solank ons dit ... dit' has a number clash. The protection was narrowed so the next revision can make it 'hulle ... hulle'.
  - Gr 6 LV GO 2 (621), 4 (613) and 6 (585) are reading stories over 550, signed off in September. Kept as they are; add them to question 5 on the questions page.
  - The lees/ outbox skips Gr 6 LV lessons because four sub-topics each have a 'Les 04' (name collision in the flat folder). Check how lees/ names files before the next delivery to Drico.
  - For question 5 too: Gr 6 LV OvS 8 (588), 9 (576), 10 (629), 12 (607) and GO 7 (596) are over 550 with no exception, signed off before the ceiling rule. Carried language-only.

**Where things stand, 28 Oct 2026 (end of day).**
- Gr 6 NW 26/26 done and pushed (48d0130f).
- Gr 6 LV in progress, nothing committed yet:
  - OvS 1, 2, 4, 6, 7 signed off; GO 2, 6 signed off.
  - Wound down mid-flight: GO 1 (re-run coverage on the same draft; the spec contradiction is fixed), GO 3 (checks running), GO 4 (writer check item), UK 1-4 and GO 7 (language step and writers), OvS 8, 9, 10, 12 and VK 1 (step 0 done, protections in; VK 1 writer may have run).
  - Not started: GO 8, SR 1-12, VK 2-4.
- Next session:
  1. Check each lesson's state in logs/hardloop_log.jsonl before any runner call.
  2. Run the wind-down replies' next steps.
  3. Then GO 8, SR, VK 2-4, then Gr 6 SW (73).
- Open from today: GO 1 buite_bestek[0] "Behandeling begin altyd by 'n grootmens" (does it read like "call an adult first"?). Update question 5 on the questions page with the over-length lessons. The questions page now saves answers (artifact capability); Q1 was answered and its acceptance written.
  - Gr 6 LV VK 1: the writer's new stimulus 'mense en elande op rotsskilderye in die Drakensberg' (protected) needs its fact check. The spec's opening item says 'sien feiterisiko 7' where it means the 8th item: fix. Next: call the runner with --met-taal. OvS 8, 9, 10, 12: call the runner again, then run the finders.
  - UK 1, 2 and GO 7 protections were added at the wind-down: call the runner again, then the finders. UK 3: call the runner (it registers the reports, then the writer fixes 'beweging' and the maskandi 'dikwels'). UK 4: call the runner (it applies one change), then the writer for one item. The ruimte dance sentence waits on UK 4's fact check.
  - Gr 4 LV UK 2 'beweging' ('van houding of plek verander') overlaps 'niebeweging' (moving on one spot), per a Gr 6 fact check. Gr 6 now orders 'van plek na plek'. Fix Gr 4 at its next reprint; this is related to question 11.
  - Gr 6 LV shared 'voorouers' says the same thing twice ('reeds oorlede is' and 'wat al gesterf het'), and its recorded reason mentions 'voor jou gebore is', which the wording lacks. Tidy at the year's reconciliation (several lessons use it). SV 5 'probeer ook nie om dit te keer nie': 'dit' can read as the animal; next revision.
  - Handel 2 'uitvoer'/'invoer' (goods only): left as is after all. Lesson 4 never says services are sold abroad, so there is no false contrast; incomplete is fine.
  - Gr 6 SW shared 'demokrasie' ('n Manier van regeer WAAR ...): 'waar' after a noun that is not a place. Style only; tidy at the year's reconciliation (shared across lessons).
  - Gr 6 SW 'Greenwich Meridiaan': AWS would be 'Greenwich-meridiaan'. Kept as in the shared wordings and CAPS; a decision for the whole subject (Gr 4-6) at reconciliation.
  - Gr 6 SW Kaartvaardighede 5 and 6 (signed off) spell 'lineaal'; the standard is 'liniaal' (Gr 4 uses it). Fix at its next revision.
  - Gr 6 SW 'nC' (ná Christus) is not in the shared list. Every lesson with CAPS dates uses it. Add at the year's reconciliation.
- 28 Okt 2026: Gr 6 SW Mapungubwe les 4 se aanvaardingsrekord ("eerste staat") geld volgens die hardloper vir niks meer nie; dit is Lampies se rekord, laat staan tot Lampies dit sien. Kern-item 4 en 5 van les 4 trek effens teen mekaar oor 'n afleiding uit die vindplek alleen - opruim by die volgende hersiening.
- 28 Okt 2026, Gr 6 SW Demokrasie 1-4 afgeteken, 5 wag op V25 (Fatima Meer 1952/1954). Oop: les 5 'tolk' se 'oorsê' (beteken 'weer sê') nog nie reggemaak nie; les 3 'Parlement' se inskrywing het twee gestapelde 'wat'-sinsdele; nuwe begrippe 'apartheid' (les 1) en 'burgerskap' (les 4) moet by die rekonsiliasie in die gedeelde lys kom; les 6 dra nog die ou 'wet'-bewoording.
- 28 Okt 2026, Gr 6 SW: nuwe begrip 'vloedvlakte' (Mapungubwe 1) vir die rekonsiliasie; Demokrasie 8 dra drie onbesliste gedeelde terme ('tydsorde', 'weergawe', 'navorsing').
- 28 Okt 2026, Gr 6 SW Klimaat 7-9 afgeteken; les 6 wag net op dekking ná die 'oase'-spekregstelling. Oop: 'vetplant' se komma ('dik, vlesige') by die volgende hersiening; Klimaat 8 se 'waar ... eenders lyk' kan by herdruk 'terwyl' word (beskerming vernou). Mapungubwe 6-10 en Medisyne 6-10 begin eers wanneer T en X klaar is (een skrywer per subonderwerp).
- 28 Okt 2026, Gr 6 SW Bevolking 1-8 almal afgeteken. By elke herdruk weer nagaan: Bevolking 7 se VN-syfers (2018-uitgawe; die 2025-hersiening gee Tokio 33,4 en Lagos 12,8) en Bevolking 8 se 'Kaïro is Egipte se hoofstad' (die nuwe administratiewe hoofstad).
- 28 Okt 2026: Mapungubwe les 1 se aanvaardingsrekord geld ook vir niks meer nie (soos les 4 s'n) - Lampies se rekords, laat staan tot Lampies dit sien.
- 28 Okt 2026, Gr 6 SW: gedeelde 'sekondêre bron' se voorbeelde vernou (geskiedenisboek, dokumentêr, museumuitstalling) ná Demokrasie 8 se feitetoets; Demokrasie 8 en Medisyne 4 moet dit dra (albei in hierdie rondte na die skrywer). Demokrasie 7 se 'Engelse strofe nuut geskryf' was vals (aangepas uit Die Stem se Engelse weergawe, 1997); spek reggemaak.
- 28 Okt 2026, Gr 6 SW Ontdekkers 6-8 afgeteken; 9 se 'jonk' by die bron gesny. Oop by herdruk: les 6 'Fyn stowwe soos sy' (sy = silk kan as 'she' lees); les 7 kruisboog-inskrywing se slotfrase kan aan die pyl heg; les 7 'hierdie kus'/'daardie kus' opeenvolgend (albei beskerm); les 7 spek sê geen bron bevestig die Khoikhoi het hul beeste weggedryf nie, maar die rekord van 8 Okt haal Barros aan wat dit sê - opruim; SAHO se Dias-profiel meng Da Gama in. Les 8 fokusvraag_skakel se 'daarlangs' reggemaak.
- 28 Okt 2026: Demokrasie 6 wag op V26 ('Armoede alleen is nie verwaarlosing nie' - aanvaar, vernou tot verwydering, of sny). Demokrasie 6 se begrotingsnota gee nog ~60 woorde aan 'wat 'n handves is' terwyl kern-item 1 enige algemene omskrywing verbied - opruim by die bron.
- 28 Okt 2026, Mapungubwe 2 afgeteken. Oop: 'heilige leierskap' se 'apart van ander mense gehou' teenoor die studieteks se 'afgesonderd' (een begrip, twee woorde); les-2.aanvaardings.json geld vir niks meer nie (Lampies s'n).
- 28 Okt 2026 (gebruikslimiet bereik): Demokrasie 7 afgeteken; 8 se feitetoets moet oor (soektog-limiet; dekking klaar); 6 wag op V26. Oop by die bron: Demokrasie 7 se rekord oor 'die eis dat die woorde nuut is'; die gedeelde 'sekondêre bron' se 'uitstalling in 'n museum' (die onvoltooide feitetoets het dit as onseker beskou); Mapungubwe 3 kern-item 2 se 'Mapungubwe se eie bestaan'-redenasie. Mapungubwe 1, 3, 5 en Medisyne 3-5 was nog aan die gang (koördineerders T en X). Daarna: Mapungubwe 6-10, Medisyne 6-10, drifveeg, V2-reëls, v2_inhoud.py, commit en push.
- 28 Okt 2026, Gr 6 SW Demokrasie 7 en 8 afgeteken (1-4, 7, 8 klaar; 5 wag V25, 6 wag V26). Vir rekonsiliasie: gedeelde 'primêre bron' se 'ook as sy dit jare later vertel' - 'sy' het geen antesedent as die inskrywing alleen gelees word nie; Demokrasie 7 'staatsheraldikus' se generiese 'Hy', kleursin, 'een van die Khoisantale'; Demokrasie 6 'verwaarlosing'-lys eindig op ', en skool'; Demokrasie 8 woordelys dra nog 'toespraak' en 'oorskryf'. Die gedeelde 'sekondêre bron' se museumuitstalling is uitgehaal (voorbeelde nou net geskiedenisboek of dokumentêr).
- 28 Okt 2026, Mapungubwe 5 afgeteken; 3 afgeteken maar teruggestuur vir een skrywerpas ('ander soorte mense' kan as ras lees in 'n les oor klas); 1 se kern-item 4 van bo af herskryf. Oop: ivoor 'tande' teenoor 'lang tande'; les-5.aanvaardings.json geld vir niks (Lampies s'n).
- 28 Okt 2026, Gr 6 SW Medisyne 1-6, 8-10 afgeteken; 7 by die skrywer ('niks' vir die grootste deel van die geskiedenis was vals). Vir rekonsiliasie: Medisyne 6 'een van die grootste oorsake van dood' (beskerm) - 'doodsoorsake' is beter Afrikaans; Medisyne 10 se laaste sin 'die meeste mediese skole' laat 'Westerse' weg; Medisyne 8/9 'afwys' teenoor die mediese 'afstoting'; Mapungubwe 9 karavaan 'goedere'.
- 28 Okt 2026, Mapungubwe 1, 2, 4-8, 10 afgeteken. By herdruk: les 6 'baken' se 'jou rigting te kry' (Engels 'get your bearings'; 'koers kry'); les 3 'Een leier'/'die koning' nie gekoppel nie as dit oop bly.

**Stand, 29 Oktober 2026.** Gr 6 SW 71/73 gestoot (902b002d); Demokrasie 5 en 6 wag op vrae 25 en 26. V2 = 299 lesse. Wat oorbly: Gr 4 SW Geografie water 4 (vraag 21; die ander 29 is op 23 Okt afgeteken - die blok van 23 Okt hierbo was verouderd), Gr 4 SW Geskiedenis 24 lesse (vraag 20), Gr 4 NW 7 (vrae 13-16, 18), Gr 4 LV 2 (vrae 12, 19), Gr 5 LV 2 (vrae 1-2, 22; vraag 1 beantwoord), Gr 6 LV UK 3 (vraag 24).
- Gr 4 SW: verouderde-bestellings.py wys nog bestellings onder rekords in kaartvaardighede en plekke - vee voor die volgende hersiening van daardie subonderwerpe. Kaartvaardighede 5 hang af van sy kaart (skool by B2, park by C3, dam, kliniek) - vir die HTML-span.

**Lampies se antwoorde, 29 Oktober 2026 (vraebladsy).** Ja op 1-10, 12-14, 16, 17, 19, 21-26. Anders: 15 (verstaan nie - twee dinge in een vraag; herformuleer), 18 (video is gemaak - wat nou?), 20 (hou die afgelewerde lengtes). Gedoen: 20 - gate.py/hardloop.py lees nou 'afgelewerde_lengte' uit die spek (begroting +-15% in plaas van die harde plafon), in die ses Geskiedenis-spesifikasies verklaar; koördineerders H1 en H2 loop oor die 24 lesse. Aanvaardings 13, 16, 19, 21, 22, 24 loop (agent). Nog te doen: 2 (verpleegster-sin, Gr 5 GO 9), 8 (benoemde San-rotsskildery in Gr 4 VK 3), 12 (nuwe 'familie'-bewoording, Gr 4 UK 1 en 2), 14 (nes: bewoording hou, spek aanpas, afteken), 18 (name laat val + video-raad), 25 (1954 voorop), 26 (vernou tot verwydering), 15 (herformuleer).
- 29 Okt 2026: aanvaardings 13, 16, 19, 21, 22, 24 geskryf en al ses afgeteken (Gr 4 NW energie 1 en Maan 3, Gr 4 LV GO 5, Gr 4 SW water 4, Gr 5 UK 2, Gr 6 UK 3). Wenk: 'n les met 'n ou eskalasie teken met 'hardloop.py ... --hervat --keur-goed' af sodra die aanvaarding staan; die verslae bly. Koördineerder Q doen nou vrae 2, 8, 12, 14, 18, 25, 26. Vraag 15 wag op Lampies se herformuleerde antwoord.
- 29 Okt 2026: vraag 27 beantwoord (wentelbaan woord vir woord: 'Die pad wat iets in die ruimte oor en oor om 'n ander ding volg'); aan koördineerder Q. Kommunikasie 11 kern[4] se 'iets by 'n ander mens uitkry' (= uit iemand kry) is by die bron 'oordra'. 'kommunikasie' moet op die Gr 4 SW gedeelde lys kom ná les 1 se feitetoets. HTML: 314 van 339 lesse lees anders as voor die rondte; Lampies het gesê 'finish up with everything'.
- 29 Okt 2026: SOODRA die oudit-agent klaar is met kaps/gedeelde-omskrywings-sosiale-wetenskappe-gr4.json: voeg 'kommunikasie' by ('Om 'n boodskap aan iemand anders oor te dra.', feitetoets van kommunikasie 1 geslaag) en kyk watter ander Gr 4 SW-lesse die term omskryf.
- 29 Okt 2026: Gr 4 NW les 8 (neste) afgeteken met die vernoude bewoording (vraag 14). Gr 4 'familie' verander in UK 1, 2 en 3; Gr 5 UK se 'familie'-inskrywing hou die ou bewoording (oor grade heen toegelaat) - kyk by Gr 5 se volgende hersiening of dieselfde fout (alleen gelees) daar geld.
- 29 Okt 2026: oudit-ordes in Gr 4 Geskiedenis-spesifikasies (plaaslike 1-5, leiers 1-4; kom 1, 9, 11 deur my). 'geskiedenis' verbreed; 'kommunikasie' op die gedeelde lys. Vir Lampies: plaaslike 2, 3 en 5 se begrotings (280, 320, 265) gaan bo Drico se 250-maksimum vir Kwartaal 1 weens die oudit-ordes; 'n antwoord voorstel en toets' rus op KABV 2.1 ('spekuleer') en 'stories behoort aan mense oral' op die leiers-onderwerp se agtergrondnota, nie die inhoudskolom nie.
- 29 Okt 2026: taalnasien.besliste_omskrywings beskerm nou 'n besliste bewoording ook waar dit woordeliks in die studieteks staan (nie net in begrip-blokke nie) - die taalstap het 'vanuit' na 'uit' in plaaslike 1 se 'geskiedenis'-sin verander. 40 nuwe beskermings oor 387 lesse. Gr 4 SW sign-off-lys: 'help antwoord' (Engels; 'help beantwoord') in plaaslike 1 x3; beskermde 'Soms wys hulle nie genoeg nie en die vraag bly oop.' kort sy AWS-komma.
- 29 Okt 2026 Gr 4 SW: water 1 en lug 1, 3 afgeteken. Herdruk/taal-lys: water 1 'Brittanje het baie van hulle gevaar' (oorganklike 'vaar'), 'Die vroegste seile kon net voor die wind loop' (idioom: die skip loop voor die wind), klipperboot 'om vrag gou te bring', jonk 'seile wat dun latte styf hou' (kan omgekeerd lees); lug 3 'n Satelliet kyk van bo af na die wolke' (lees as elke satelliet), opskrif 'Vrag wat haastig is'; kom 4 dubbele 'sein'.
- 29 Okt 2026 kommunikasie-spek: 162 velde herstruktureer (bestellings eerste, dan merker). Oop: les 11 eerste handfoon se gewig (1,1 kg teenoor 790 g) uit die bestelling gehaal; begrotingsnotas van les 1, 6, 9 tel een kern-punt te min; les 10 se spek-titel verskil van die afgelewerde; les 3 se moenie-herhaal-lys is leeg terwyl die nota sê dit het inskrywings.
- 29 Okt 2026: 'geskiedkundige' moontlik 'n gedeelde Gr 4 SW-term (plaaslike 1 omskryf, leiers 2 gebruik) - rekonsiliasie.
- 29 Okt 2026: Lampies het in die klets vrae 28 ('posklip') en 29 ('iqhugwane') by naam aanvaar.

**PAUSE 29 Oktober 2026 (Lampies pak op).** Lopend: koördineerders H1 (kommunikasie, vervoer-op-land), H2 (plaaslike, leiers, lug, water), Q (vrae 2, 8, 12, 14, 15/27, 18, 25, 26). Almal gevra om hul lopende kind klaar te laat, niks nuuts te begin nie, en 'n toestandnota te gee. Niks gekommit sedert 902b002d nie: Gr 4 SW Geskiedenis, die vraag-antwoorde, gate.py/hardloop.py (afgelewerde_lengte), taalnasien.py (beskerming in studieteks) en baie spekregstellings staan in die werkboom. By hervat: lees die koördineerders se notas, hervat hulle, en kommit per voltooide groep.
- 29 Okt 2026: PAUSE herroep - Lampies laat die skootrekenaar aan; werk gaan voort.
- 29 Okt 2026: Gr 4 NW planeet-omskrywing (gedeel, les 27 en 29): ''n Groot ronde wêreld wat op sy eie om 'n ster beweeg. Op sy pad beweeg geen ander groot wêreld op sy eie nie.' Les 27 se ou Drico-vraag (geslote pad) gesluit: les 27 mag sê die Aarde kom terug by dieselfde plek; 'wentelbaan', die jaar en die een rigting bly by les 29. Afgeteken: Gr 4 VK 3 (San-rotsskildery), UK 1-3 (familie), NW 17 (huise), Gr 4 SW plaaslike 2, water 2.
- 29 Okt 2026 aand: koördineerder Q klaar - vrae 2, 8, 12, 14, 18, 25, 26 en les 27 afgeteken. WAG OP FEITETOETS (soektog op): Gr 4 NW les 29 (die-aarde-en-die-son/les-1) en 31 (die-maan/les-2, reeds 2 keer teruggestuur), kommunikasie 7 en 9, plaaslike 1 en 3. Teken af met hardloop.py --keur-goed ná 'n skoon feitetoets. Oop vir 'n mens: Gr 4 VK 1, 2, 4 se 'prent of model'-bestelling teenoor die plat gedeelde 'vorm'; Gr 4 NW dop-struktuur se 'die ruimte binne' teenoor 'ruimte' = buitenste ruim; Gr 5 GO 9 se verpleegster noem die lang hoes 'n simptoom; UK 1 'gesorteer volgens hoe hulle klank maak'; Gr 6 Dem 5 se ou beskerming 'Sy het self gesê dit was 1954' onaktief.
- 29 Okt 2026 laat: WEBSOEK OP (perk CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION). Tien feitetoetse wag; elkeen het sy dekking reeds GOEDGEKEUR (leiers 4 ná sy spekregstelling): Gr 4 SW plaaslike 1, 3, 4, 5, leiers 3, 4, kommunikasie 7, 9; Gr 4 NW die-aarde-en-die-son/les-1 (jaarles 29) en die-maan/les-2 (jaarles 31, 2 keer teruggestuur). Elk: feitenasiener lees konsepte/.../feite-kopie/les-N.json, skryf konsepte/.../les-N.feite.json (roep eers hardloop.py sodat die kopie vars is), dan hardloop.py --keur-goed. Daarna: v2_inhoud.py, V2-reëls vir die Gr 4 Geskiedenis-gapingslesse, drifveeg Gr 4 SW en Gr 4 NW, kommit en stoot.

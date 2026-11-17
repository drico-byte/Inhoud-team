# Planner brief: Grade 5 Geography, Term 4 (Minerale en mynbou)

Read `videoskrifte/gr5-geo-nagaan/BEPLANNER-OPDRAG.md` first: everything in it still
binds (inputs, never a textbook, never the raw scripts, the fixed division, the standing
rulings, the settled terms, fact risk, lean file, validator). This brief adds what is
particular to Term 4 and overrides it only where it says so.

## What is different for Term 4

- **CAPS**: printed page **28** (PDF page 33, index 32), plus Section 2.5. Read the
  footnote: *"Steenkool word uit organiese plantoorblyfsels gevorm en is dus nie 'n
  mineraal."*
- **Sub-topic key** (`kaps_subonderwerp`): exactly `Minerale en mynbou`. Output:
  `spesifikasies/konsep/gr5/sosiale-wetenskappe/minerale-en-mynbou.json`. Eleven lessons,
  register IDs G5_GEO_33 to G5_GEO_43, `nommer` 1-11, `jaarnommer` 33-43.
  `kaps_ure` 12 (15 minus 3 revision hours; say so in `kaps_ure_nota`). `totale_begroting`
  2 775.
- **Field-shape models**: `spesifikasies/goedgekeur/gr5/sosiale-wetenskappe/weer-klimaat-en-plantegroei.json`
  (Grade 5 Geography Term 3, approved) for the spec and lesson fields, and the lesson with
  `buite_kaps` in `spesifikasies/goedgekeur/gr5/sosiale-wetenskappe/die-eerste-landbouers.json`
  for the extra lesson's shape. Copy field shape, not content.
- **Cluster 1** (Minerale en steenkoolhulpbronne, 4 h, envelope 800) is budgeted 950. Every
  lesson in it carries `kluster_uitsondering`: "Lampies, 17 November 2026: lesse word nie
  tot 200 beperk nie; 'n les wat te knap is, kry meer woorde. Hierdie kluster gaan daarom bo
  sy koevert van 800 uit." Clusters 2 and 3 sum exactly to their envelopes.
- **Video H4 14** (the chapter recap) has NO text lesson (register G5_GEO_44, video only).
  Nothing in the spec refers to it as a lesson.

## Lesson orders fixed by Lampies (17 November 2026)

- **G5_GEO_34** carries CAPS's eight named minerals, every one mandatory: goud, platinum,
  diamante, ystererts, chroom, koper, silwer, mangaan, each with its use(s). 300 words for
  eight items is tight: plan about two sentences per mineral and say so in
  `begrotingsnota`. CAPS names them explicitly, so none may be dropped for words.
- **G5_GEO_35** MUST say that coal forms from the remains of plants and is therefore NOT a
  mineral (CAPS's footnote). The video never says it, so list it under
  `kaps_sonder_video`. Coal is a rock (gesteente) and a fossil fuel and a non-renewable
  resource. Order the mechanism (plants in swamps, buried, pressure and heat over millions
  of years) without inventing stages you have not checked.
- **G5_GEO_36** needs a map: carry a `kaart` field saying WHAT the map must show (which
  minerals and coal, in which provinces/areas), not how to draw it. Order the link to
  settlement patterns (CAPS). Johannesburg and gold is the video's example.
- **G5_GEO_43** is an EXTRA outside CAPS: `buite_kaps: true`, with `buite_kaps_rede`
  (copy the profile's), no `kaps_kluster`, budget 225 (the gate's ceiling of 252 serves
  Lampies' ceiling of 250). The line Lampies set for Grade 5 History's extras holds:
  **we teach the truth and withhold what is not appropriate, never making the picture false
  by omission, nothing graphic.** No numbers of deaths, no description of bodies or
  violence. Order empathy for why people do it without approving it, and the dangers.
- **G5_GEO_41 and 42 are safety lessons, and safety lessons produce this pipeline's worst
  errors.** Order each rule as a rule miners must follow, never as something a miner or an
  adult may choose. Do not order a specific number (temperature, depth) unless you checked
  it; prefer the shape ("very hot deep underground"). Silicosis: order what it is in terms
  you have checked (a lung disease from breathing in fine dust of the rock mineral silica
  /quartz over a long time); do not order claims about cures or treatment you have not
  checked. CAPS names ventilation, heat, rockfalls, dust (41) and silicosis (42); all
  mandatory.

## Terms

- **nie-hernubaar / nie-hernubare** is the grade's spelling (Grade 5 and 6
  Natuurwetenskappe already use it, and the video does). CAPS's "nie-hernieubare" is a
  spelling variant, so it is not bracketed.
- CAPS: "Oopmyn/oppervlakmynbou", "Skag en ondergrondse mynbou". The video says
  "oopgroefmynbou, wat ook oppervlakmynbou genoem word" and "ondergrondse mynbou" with a
  "skag". Use the video's names where the video notes do not flag them as unestablished,
  and make sure CAPS's "oppervlakmynbou" and "skag" appear.
- Reuse the grade's decided wordings where a term recurs: `kaps/gedeelde-omskrywings-sosiale-wetenskappe-gr5.json`
  (e.g. nedersetting, kragstasie, habitat). Grade 4 SW decided "natuurlike hulpbron"
  ("Iets uit die natuur wat mense gebruik om in hulle behoeftes te voorsien.") - prefer it.
  Grade 5 Natuurwetenskappe (a different subject, same learners) defines steenkool,
  brandstof and bogrond; do not contradict them, though Geography may say more.
- The terms new to this term that more than one of your lessons will use (mineraal, erts,
  mynbou, myn, nie-hernubaar, steenkool, besoedeling, erosie, ventilasie, rotsstorting,
  mynwerker, afval) get ONE meaning across your eleven lessons: name the lesson that
  defines each in `gedeelde_omskrywings_nota`, and order later lessons to reuse it.

## What the script check found that shapes the orders (17 November 2026)

Read your lessons' video notes for the detail; these are the ones that change orders.
- **Mineral**: a definition that says only "natural substance in the earth's crust" also
  fits coal and oil, contradicting CAPS's footnote. Order a definition that excludes what
  forms from living things (G5_GEO_33 defines it; 35 builds on it).
- **Where things are mined**: do not tie a mineral to one province where it is mined in
  several (copper, diamonds and gold are each mined in more than the video's provinces).
  Order "among others"/main areas, and give `kaart` only areas you have checked.
- **No coal-reserve figure** (sources disagree widely).
- **Open-cast vs underground**: coal and diamonds are mined both ways in South Africa; do
  not tie a mineral to one method except deep gold.
- **Zama-zamas (G5_GEO_43), my call within Lampies' line:** being false by omission
  includes leaving out that criminal gangs control much illegal mining and exploit the
  miners; say so plainly, without naming any nationality (that stigmatises) and without
  deaths or graphic events. One protective line for the learner is in scope: stay away from
  old mine shafts and holes. Spelling of the plural is for the video notes and the spec
  fact-check to settle; use one form throughout.
- **Safety (41, 42)**: silicosis comes from breathing fine dust of quartz (crystalline
  silica) over a long time, and cannot be cured; a dangerous area is closed off and nobody
  goes in until it has been made safe - never "not without permission"; the mine, not only
  the worker, carries the duty to keep workers safe.

## Fact risk particular to this term

Where minerals are mainly mined (provinces), how coal forms, what ore is, how mines make
towns grow, what acid mine drainage is, how open-cast and underground mining differ (coal
and diamonds are mined both ways in South Africa), mine depths and temperatures, silicosis,
and the Zama-Zamas. Use the video notes' problem claims as warnings in your own words.

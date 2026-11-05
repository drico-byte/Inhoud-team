# V2 inhoud: for the HTML team

Every file here is written by `bin/v2_inhoud.py`, which sign-off now runs too. Each
subject is mirrored, byte for byte, into the content library ("Wolkskool Nuwe Inhoud
V3", `Graad N/<code>/Inhoud/`, with a `manifest.json` per subject); see
`AFLEWERING-REEL.md`. Do not edit anything here except
what is under `Terugvoer/`. The next run deletes any PDF or JSON in a grade folder
that is not a current delivery, and rewrites the manifest.

- **`Graad N/<vak>/G4_PSW_07 - <label>.pdf`** is the approved lesson, and the PDF is
  the authority. `<vak>` is one of PSW, Kuns, NW en Teg, Geskiedenis or Geografie.
  Since 5 November 2026 the name follows Drico's naming rule (`LESNAAM-REEL.md` in
  SharePoint's `0000NUWE LESSE/`): `G4_PSW_07` is the lesson ID from the lesson
  register in `0000NUWE LESSE/Lesregister/`, and it never changes. Its number is the
  lesson's place in the year for that subject. The label after it is a short name
  for people and may be reworded; the lesson's own title is in the JSON.
- **`... .json` beside it** holds the same lesson as data, built from the same
  approved file. Each run checks that every learner string in it appears in the
  PDF, and if one doesn't, it delivers neither file.
  - `blokke` are in page order: the body first, then `afdeling: woordelys` (the
    begrippe), then `afdeling: vrae` (only four older Gr 4 NW lessons have any).
  - `rol: leerder` is text the learner reads, word for word.
  - `rol: vir_html_span` is a `kaart` block. It says what the map must show; it is
    not text to print.
  - `produksie` is the reading copy's furniture, and none of it goes on the
    learner page.
- **`manifest.json`** has one entry per lesson.
  - `status` is `final` (build it) or `held` (don't, see `rede`).
  - `json_sha256` is the content fingerprint. When it changes, the lesson was
    reissued, and the previous issue is listed under `uitgawes`.
  - `pdf_sha256` can change when the PDF is printed again with the text unchanged.
  - `id` is the lesson ID. `ou_pdf` and `ou_json` are the file names before the
    naming rule (`Graad 4/PSW/Les 07 - <titel>.pdf`), so a record keyed on the old
    names can be matched to the lesson. Renaming changed no lesson's content or
    fingerprint.
- **`Veranderinge.md`** says, per lesson, what changed and why.
- **`teruggehou.json`** is where the content team puts a hold:
  `{"<bron>": "rede"}`.
- **`Terugvoer/`** belongs to the HTML team:
  - `HTML-span-navrae.md` for wording queries;
  - `HTML-afgelewer.json` for which fingerprint each built page came from.

To check built pages against the repository:

```bash
python bin/htmlnasien.py --html "<folder>" --vak Geografie --graad 4
```

Any file name containing the lesson ID (`G4_GEO_07`) or the older "Les NN" is read. The check reports four things:

- every approved sentence that is not on the page word for word;
- shared definitions that differ;
- glossary entries that differ from the repository;
- protected words, which it looks for only in text that already differs.

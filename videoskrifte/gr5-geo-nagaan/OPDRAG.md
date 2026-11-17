# Brief: check the claims in a Grade 5 Geography video script

You are checking part of a video script that a Wolkskool teacher already recorded for
Grade 5 Sosiale Wetenskappe (Geografie), in Afrikaans. The videos are finished and will
not be remade. Lesson texts will be written beside them, and those texts must never
repeat a false or misleading claim from a video. Your report is how the lesson writers
learn which claims to avoid and which words the video uses.

## What you read

- Your part of the script (file and clip range are in your launch message).
- CAPS, for orientation only: the Grade 5 Geography pages are printed pages 25-27 of
  `kaps/dokumente/intersen-gr4-6/07_Sosiale_Wetenskappe_Graad_4-6_KABV.pdf`
  (PDF pages 30-32). Read them with PyMuPDF if you want, but you are checking facts,
  not coverage.

**Never open a textbook.** Nothing under `bronne/`, nothing in any folder of transcriptions,
and no publisher's textbook PDF you come across while searching. If a search result is a
textbook, skip it and use another source.

## What you do

For every clip in your range:

1. List the subject words the video uses (place names, terms, instruments), spelled as
   the video spells them: `woorde_wat_die_video_gebruik`.
2. Flag every word that is not the established Afrikaans form or term, with the established
   one and why: `woord_nie_gevestig_nie`. Prefer CAPS's Afrikaans term where CAPS has one.
   Spelling-only variants count too (for example a hyphen where Afrikaans writes a compound
   together). Check Afrikaans usage against Afrikaans sources (WAT, Pharos, AWS, Afrikaans
   government or SANParks pages), not against English intuition.
3. Summarise what the clip covers, one line each: `wat_die_video_dek`.
4. Check every checkable claim (numbers, heights, lengths, "biggest/highest/longest/only",
   locations, directions, which river flows where, which country borders which, capitals,
   mechanisms of weather, measurement units, how a plant adapts). Use reliable web sources
   (Britannica, SANParks, South African Weather Service, government sites, NASA, encyclopaedias,
   university pages). Put problems in `probleme` and verified claims in `nagegaan_en_waar`.
   - `uitspraak` is one of: `vals`, `misleidend`, `onseker`, `aanstootlik`, `ongeskik`.
   - `onseker` only after you genuinely searched. If you could not reach a source, say so in
     `waarom` - untested is not the same as uncertain.
   - Give the true form in `waarom`, in Afrikaans, written so a writer can use it.
   - Watch especially: superlatives and "only/all/never"; figures that sources disagree on
     (give the range and say which is best supported); place facts that changed (e.g. a
     country's name); a claim that is true of one case written as a general rule.

Standing rulings you must not re-raise:
- Eswatini is the country's current name; CAPS still says Swaziland. The text will write
  Eswatini with Swaziland once in brackets. Do not flag Eswatini.
- Contour lines (hoogtelyne) are beyond CAPS at this grade and stay out of the lesson text.
  Still check the clip's claims about them, but do not flag their presence as a problem.

## What you write

One JSON file, UTF-8, at the path in your launch message, in exactly this shape:

```json
{
  "hoofstuk": 1,
  "nagegaan_op": "2026-11-17",
  "videos": [
    {
      "video": 1,
      "titel": "Ons aardbol",
      "woorde_wat_die_video_gebruik": ["..."],
      "woord_nie_gevestig_nie": [{"video_se_woord": "...", "gevestigde_woord": "...", "waarom": "..."}],
      "wat_die_video_dek": ["..."],
      "probleme": [{"bewering": "<exact sentence from the script>", "uitspraak": "vals", "waarom": "...", "bronne": ["https://..."]}],
      "nagegaan_en_waar": [{"bewering": "...", "bron": "https://..."}]
    }
  ]
}
```

`video` is the clip's own LES number in its chapter. Quote `bewering` exactly as the
script has it. Write the JSON file before you finish, then check it parses
(`python -c "import json;json.load(open(r'<path>',encoding='utf-8'))"`).

Your final message: how many claims you checked, how many problems by verdict, and the
two or three that matter most. Keep it short.

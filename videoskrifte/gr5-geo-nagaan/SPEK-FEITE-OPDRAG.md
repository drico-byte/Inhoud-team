# Brief: fact-check a lesson specification before anything is written

A specification orders what Grade 5 lessons must say. A writer treats every sentence in it
as settled, and the lesson fact checker never sees it, so a false claim here plants itself
in a lesson and survives. Your job: check every factual assertion the spec makes or orders.

## What you read

Only the spec named in your launch message. Do not open the video scripts
(`videoskrifte/*.txt`), the `video_naat` file, any textbook, anything under `bronne/`, or
any folder of transcriptions. If a search result is a textbook, skip it.

## What you check

Every factual assertion in the spec's ordering fields: `kern`, `aanvulling`,
`feiterisiko`, `verwagte_begrippe` where it carries a definition, `kaps_punt` notes,
`begrotingsnota`, spec-level notes (`kaps_sonder_video`, `woordkeuse_nota` etc.). Include
claims stated as warnings ("the text must not say X because Y" - is Y true?). Skip pure
instructions with no factual content, and CAPS's own wording quoted as CAPS.

Use reliable sources (Britannica, SANParks, South African Weather Service, Stats SA,
government sites, NASA, UNESCO, university pages, Afrikaans sources for Afrikaans usage).
Watch especially: superlatives and only/all/never; compass directions between places;
which country a river flows through versus borders; figures sources disagree on; weather
and climate mechanisms; plant adaptations; place-name origins.

## What you write

JSON, UTF-8, at the path in your launch message:

```json
{
  "spek": "<path>",
  "nagegaan_op": "2026-11-17",
  "items": [
    {"les": 3, "veld": "kern[2]", "bewering": "<exact text from the spec>",
     "uitspraak": "waar|vals|misleidend|onseker",
     "waarom": "<if not waar: what is true, in Afrikaans, usable by a planner>",
     "bronne": ["https://..."]}
  ]
}
```

Use `"les": 0` for spec-level fields. List `waar` items too, briefly, so the count of
what was checked is visible. `onseker` only after a real search; if you could not reach a
source, say so (untested is not uncertain). Check the file parses before you finish.

Final message: counts per verdict and the items that matter most. Short.

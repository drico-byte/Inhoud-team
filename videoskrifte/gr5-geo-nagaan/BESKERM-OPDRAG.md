# Brief: move the writers' protected wordings into the protected-words list

Before the Afrikaans language step runs, every wording a writer recorded as "must not be
changed by a language check" must be in `kaps/beskermde-woorde.json`. The language agents never
see the provenance note, so a prediction that stays only there protects nothing.

For each lesson in your launch message:

1. Read the draft `konsepte/gr5/sosiale-wetenskappe/<slug>/les-N.json`, especially
   `herkoms.nota`, and find every wording the writer says a language edit must not touch
   (hedge words that keep a sentence true, a deliberate word choice, a video word in brackets,
   a decided name).
2. Check the entry is real: the wording must actually stand in the lesson's text, and the
   reason must be true. Skip anything already in the list for that sub-topic or in `algemeen`.
3. Add an entry under `per_subonderwerp["<slug>"]`:
   `{"hou": "<the wording, as it stands in the lesson>", "nie": [<forms it must not become, if known>], "rede": "GRAAD 5 GEOGRAFIE, les N. <why, in one or two sentences>"}`.
   Every entry needs `hou`. Prefer the shortest wording that carries the protection (a phrase
   such as "die meeste lande", not a bare "die meeste" that matches everywhere), unless the
   bare word itself is what must stay.
4. Keep the file's formatting: `json.dumps(..., ensure_ascii=False, indent=1)` and its trailing
   newline. Read the file fresh right before writing; other entries may have been added.

Do not edit any lesson or spec. Report the number of entries added per lesson.

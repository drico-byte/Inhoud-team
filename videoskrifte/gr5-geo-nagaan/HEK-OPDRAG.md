# Writer brief: fix gate failures

The gate measured the Grade 5 Geography drafts. The failures per lesson are in
`videoskrifte/gr5-geo-nagaan/hek-1.md`. For EACH lesson in your launch message:

1. Read the draft `konsepte/gr5/sosiale-wetenskappe/<slug>/les-N.json` and its spec extract
   `konsepte/gr5/sosiale-wetenskappe/<slug>/spek/les-N.json`.
2. Fix exactly what the gate reported, by writing better, not by losing content:
   - **Commas per sentence too high:** most commas here come from lists of places, countries or
     provinces inside sentences. Move a list of three or more names into a list block, or split
     the sentence into two short sentences. Never drop the AWS comma that joins two full
     sentences before en/maar/want/of.
   - **Too many 3+ syllable words / syllables per word:** place names cannot change; replace the
     other long words with plainer ones, and do not repeat a long place name where "dit"/"daar"
     will do.
   - **Over the word ceiling:** cut back to the budget (the ceiling is budget x 1.12). Cut
     repetition and side details first, never a CAPS-required item, a hedge word ("die meeste",
     "dikwels", "omtrent", "deel van"), or a sentence that keeps a neighbour true.
3. Agreed glossary wordings (the injected list) stay WORD FOR WORD. Nothing the spec requires may
   go. Re-read each changed block whole: a fix disturbs its neighbours.
4. Record what you changed in the provenance note (rewrite it as a current record). Status stays
   `konsep`.

You cannot run the gate; the runner re-gates. Report one or two lines per lesson.
No textbook. Do not edit any spec.

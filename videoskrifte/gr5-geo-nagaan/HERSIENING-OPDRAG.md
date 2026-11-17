# Writer brief: bring drafted lessons in line with the agreed wordings

All 32 Grade 5 Geography lessons are drafted. On 17 November 2026 the terms that more than one
lesson defines were reconciled: one wording per term, fact-checked, now in
`kaps/gedeelde-omskrywings-sosiale-wetenskappe-gr5.json` and injected into every spec extract
(`konsepte/.../spek/les-N.json`). Several specs were also repaired at source after the drafts
were written.

For EACH lesson named in your launch message, in turn:

1. Read the current spec extract `konsepte/gr5/sosiale-wetenskappe/<slug>/spek/les-N.json`
   (it is fresh) and the draft `konsepte/gr5/sosiale-wetenskappe/<slug>/les-N.json`.
2. Read your lesson's entry in `videoskrifte/gr5-geo-nagaan/versoening-17nov.json`
   (the terms whose glossary wording must change; `moet_word` is the agreed sentence).
3. Every glossary (`begrippe`) entry whose term is in the agreed list takes the agreed sentence
   WORD FOR WORD. Where the study text restates the old definition, bring that sentence into
   line too, and check its neighbours still read true (a fix disturbs its neighbours).
4. Check the draft against the current spec entry (kern, feiterisiko, titel, kaart) and fix
   anything it no longer matches. Where the spec and your draft disagree and you believe the
   spec is wrong, keep the draft and say why in your report.
5. Keep the budget: the gate fails above budget x 1.12.
6. Record what changed and why in the provenance note. Status stays `konsep`.

No textbook. Do not edit any spec or the agreed-wordings list. Report per lesson in one or two
lines: what changed, and any spec fault.

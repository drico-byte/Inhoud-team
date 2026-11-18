# Brief: reconcile Term 4's shared terms (Grade 5 Geography, Minerale en mynbou)

Read `videoskrifte/gr5-geo-nagaan/VERSOENING-OPDRAG.md` first: its rules, inputs-to-read-not-edit,
fact-check duty and output format all bind. This brief replaces only its scope.

## Scope

- The drafts: `konsepte/gr5/sosiale-wetenskappe/minerale-en-mynbou/les-1.json` .. `les-11.json`
  (G5_GEO_33-43; only `les-N.json`). Terms 1-3 and History are DELIVERED: their decided wordings
  in `kaps/gedeelde-omskrywings-sosiale-wetenskappe-gr5.json` stand, and where a Term 4 draft
  disagrees with a delivered Grade 5 SW lesson's glossary, the delivered wording wins unless it is
  false (then say so under `let_op`; do not change it yourself).
- Run `python -X utf8 bin/woordelysdrif.py --vak "Sosiale Wetenskappe" --graad 5`. Decide every
  drifting term, AND every term that appears in more than one Term 4 lesson even where the drafts
  already agree, so a later revision cannot drift. Add only terms that are not yet in the list.
- The approved spec `spesifikasies/goedgekeur/gr5/sosiale-wetenskappe/minerale-en-mynbou.json`
  names an owning lesson per term in `gedeelde_omskrywings_nota`; prefer the owner's wording if
  true. Read the spec, but do not edit it.

## Decisions that must be explicit (one line each in `rede`)

- **mineraal**: must exclude coal BY NAME (CAPS footnote) without a universal rule that nothing
  formed from living things can be a mineral (shell minerals exist). Lesson 1 drafted "...maar nie
  steenkool nie"; decide whether the definition or the study text carries the exclusion. Read
  alone, it must be true.
- **mynbou**: must include coal mining (lessons say "steenkoolmyne"). **mynafval**: must cover coal
  mines too. **erts**, **myn**, **nie-hernubaar** (Grade 6 NWT's agreed sentence is a candidate;
  Grade 5 NWT may use the word too - check), **steenkool** (do not contradict Grade 5 NWT's
  "'n Harde swart klip uit die grond wat baie warm brand."; the spec now forbids "ALL coal is
  black": most is), **fossielbrandstof**, **ventilasie**, **rotsstorting**, **silikose**,
  **besoedeling**, **mineraalafsetting**.
- **erosie** (delivered les 21) and **turbine** (delivered les 20) and **ystererts** (delivered
  History les 14): delivered wins unless false.
- **grondwater**: lesson 39 used Grade 4's "ondergrondse water" sentence for it. Decide the Grade 5
  word and sentence.
- Lesson 3 (G5_GEO_35) study text says "'n swart gesteente wat brand"; the spec now orders "'n
  donker gesteente ... die meeste steenkool is swart". Put it in the change list for lesson 3.

## Output

1. New entries in `kaps/gedeelde-omskrywings-sosiale-wetenskappe-gr5.json` (`beslis`: today's date
   from `date`; keep the file's formatting, `indent=1`, UTF-8, no ASCII escaping, trailing newline;
   update its `status` line with one sentence).
2. `videoskrifte/gr5-geo-nagaan/versoening-kw4.json`: `{"minerale-en-mynbou": {"les-N": [{"term",
   "nou", "moet_word"}]}, "let_op": [...]}` - every lesson that must change, and anything a person
   must decide.

Edit no lesson and no spec. Never open a textbook, anything under `bronne/`, or any transcription
folder. Final message: terms decided, lessons that must change, the decisions that matter most.
Short.

# Brief: reconcile Grade 5 Geography's shared terms (drafting step 2)

All 32 Grade 5 Geography lessons (Terms 1-3) are drafted. Before any lesson goes through the
gate and checks, every term that more than one lesson defines gets ONE wording, decided once,
and written into the subject-grade's agreed-wordings list. The drafts reveal which terms
repeat; your job is to decide them and to fact-check what you decide.

## Inputs

- The drafts: `konsepte/gr5/sosiale-wetenskappe/{kaartvaardighede-afrika,fisiese-verskynsels-van-suid-afrika,weer-klimaat-en-plantegroei}/les-*.json`
  (only `les-N.json`; ignore `spek/` and any report files). Read every glossary (`begrippe`)
  entry and the study text around each term.
- The drift sweep: run `python -X utf8 bin/woordelysdrif.py --vak "Sosiale Wetenskappe" --graad 5`.
  It lists 23 terms whose wordings differ. It also counts 73 terms in more than one lesson;
  terms that already agree still need an entry, so a later revision cannot drift.
- The list you write to: `kaps/gedeelde-omskrywings-sosiale-wetenskappe-gr5.json` (key `terme`;
  each entry `{"omskrywing", "beslis": "2026-11-17", "rede"}`; `rede` names the lessons by year
  number and sub-topic and says why this wording won). Its 49 History entries are decided -
  do not change them.
- Neighbours to read, not edit: `kaps/gedeelde-omskrywings-sosiale-wetenskappe-gr4.json`
  (Grade 4 SW, delivered), `kaps/gedeelde-omskrywings-natuurwetenskappe-gr5.json` (Grade 5
  Natural Sciences), `kaps/gedeelde-omskrywings-sosiale-wetenskappe-gr6.json`.

Never open a textbook, anything under `bronne/`, or any transcription folder.

## Rules (all Drico's or Lampies', binding)

1. One wording per term within Grade 5 Social Sciences. Choose the best wording, not the newest.
2. A definition may not get richer during the year; it MAY widen across grades when CAPS widens.
3. Examples after "soos" may differ per lesson; the definition sentence itself is identical.
4. A wording already in a DELIVERED Grade 5 History lesson wins unless it is false (e.g.
   `hoofstad`: erfenisroete les 2; `besproeiing`: egipte les 2 - "Om water na gewasse te lei
   wanneer daar te min reën val."). Changing a delivered lesson means re-delivering it.
5. Prefer Grade 4 SW's delivered wording where it is true and fits, so a learner meets one
   definition across grades. Where Grade 5 must differ, say why in `rede`.
6. Natural Sciences Grade 5 terms used here (herbivoor/plantvreter, karnivoor/vleisvreter,
   swaartekrag, etc.): use its agreed sentence word for word unless it is wrong for this use.
7. A glossary entry is read ALONE: it must be true without its lesson around it.
8. Settled earlier this year (do not reopen): seevlak (not seespieël), punthoogte,
   hoofrivier = the main river of a river system (tributaries are never called hoofrivier),
   Oranjerivier (Gariep), kontinent, wêrelderfenisterrein, ewenaar lowercase, savanne.

## Decisions to make explicitly (each gets a one-line reasoning in `rede`)

- **dam**: this year's lessons describe the wall; Grade 4 delivered "the water stored behind
  the wall". **reservoir**: Grade 4 = a town's clean-water storage; Term 2's dam lesson uses
  "damkom (reservoir)" for the lake behind the wall. Pick wordings that do not teach two
  meanings for one word across grades, or explain the widening.
- **klimaat**: Grade 4 delivered "gemiddelde weerstoestande in 'n gebied oor 'n lang tydperk";
  Term 3 lesson 6 drafted "die weer wat 'n plek of gebied oor baie jare gewoonlik het".
- **weer** (Term 3 lessons 1 and 6), **oseaan** (Grade 4 says five oceans; this year's spec forbids
  a count), **gewasse**, **sleutel**, **aanpassing** (plants only, or also animals - check how the
  savanna lesson uses it), **nedersetting** vs a farm (the History wording stands; check every
  Geography use against it), **savanne** and **bioom** (Term 3 lessons 9 and 11).

## Fact-check every wording you decide

Use reliable web sources (Britannica, SA Weather Service, SANParks, dictionaries, university
pages; Afrikaans sources for Afrikaans usage). If a wording cannot be made true and short,
choose a narrower true one. Record the source in `rede` briefly.

## Output

1. The new entries in the agreed-wordings list (write the file; keep its formatting, `indent=1`,
   UTF-8, no ASCII escaping; update its `status` line with one sentence for today).
2. `videoskrifte/gr5-geo-nagaan/versoening-17nov.json`: for every lesson that must change,
   `{"sub-topic slug": {"les-N": [{"term": "...", "nou": "<current wording>", "moet_word": "<agreed>"}]}}`,
   plus a key `"let_op"` with anything a person must decide (keep it short).

Edit no lesson and no spec. Final message: how many terms decided, how many lessons must
change, and the decisions that matter most - short.

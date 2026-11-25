# Writer brief: faults the HTML team found in delivered V2 lessons (25 November 2026)

The HTML team builds every V2 lesson exactly as approved, and reports anything that looks wrong.
The items below were judged real faults. For the lesson in your launch message:

1. Read the draft (path below) and its spec extract `spek/les-N.json` beside it (plus
   `spek/les-N.rekords.json` if it exists).
2. Fix exactly the fault described. Choose the wording yourself and change nothing else. Keep the
   agreed glossary wordings (the injected list) word for word, and keep every protected wording.
3. Re-read the changed block whole, because a fix disturbs its neighbours.
4. Stay under the budget x 1.12. Record the change in the provenance note, dated 25 November 2026
   ("HTML-span navraag Nxx"). Set the status as the writer convention requires (`konsep`).

No textbook. Do not edit any spec. Report one line.

## The faults

- **N23, `konsepte/gr6/sosiale-wetenskappe/klimaat-en-plantegroei-oor-die-wereld/les-6.json`**
  (the block about the deserts on the maps).
  - The sentence "Op baie reënvalkaarte het hulle van die ligste skakerings, net soos die grootste
    deel van Antarktika." compares the deserts with Antarctica. The lesson's rainfall map cannot
    show Antarctica: no open dataset measures rainfall there reliably, so the map leaves it grey,
    and a learner who looks for the comparison finds nothing.
  - Remove the comparison with Antarctica and with the polar regions. The sentence before it
    already ties the deserts to the key's colours for little rain, so the comparison can simply
    go. Do not replace it with another place.
  - The spec order has been amended to match: it now forbids the comparison.
- **N25, `konsepte/gr5/sosiale-wetenskappe/die-eerste-landbouers/les-10.json`**: "Net soos ons,
  het die boere ook soms siek geword of seergekry." The comma separates the opening phrase from
  its own verb ("het"). AWS 2017 puts no comma there, so remove it.

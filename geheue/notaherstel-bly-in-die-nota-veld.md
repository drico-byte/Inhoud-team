---
name: notaherstel-bly-in-die-nota-veld
description: A note repair must go in herkoms.nota; the same prose in an invented note field makes the runner treat the draft as new and delete both clean reports.
metadata:
  type: feedback
---

**1 October 2026, from a measurement I commissioned to test the opposite idea.**

The runner decides a draft is new by a **content hash**, not a timestamp, and that
hash deliberately ignores `herkoms.nota` — since 10 September, because moving
notes to the archive once "threw away three sound reports in one afternoon".

**So a repair confined to `herkoms.nota` costs nothing.** The hash is unchanged,
nothing is archived, and sign-off proceeds. **The same prose written into
`hersieningsnota`, `hersiening_nota_3`, `nota_feite`, `besluite` or any of the
thirteen invented variants writers have used makes the runner decide the draft is
new and delete both clean reports.** Writers invent these fields freely, so say
in the brief: keep it in `herkoms.nota`.

**And never "tidy" the hash's own field list.** It keeps a hand-written list that
has drifted from the copier's allowlists — one drifted field sits in all 319
drafts. Deriving it from the copier would change every hash, so all 317 recorded
fingerprints would stop matching and the next runner touch of each lesson would
destroy roughly 245 fact reports, 245 coverage reports and 317 gate reports. The
drift is tolerated on purpose. Related: [[n-wag-wat-sy-eie-reels-naskryf]],
[[die-feitenasiener-lees-n-verouderde-konsep]].

## A cosmetic tidy in a hashed field costs both check reports

**2 October 2026.** I had a writer remove an inert `woordelys` entry — a
spell-checker allowlist word that reaches no learner and cannot change a gate
verdict. Both checkers had merely *observed* it as dead weight; neither called it
a defect.

But `woordelys` is **inside** the runner's freshness hash. Only `status` and
`herkoms.nota` are outside it. So that one removal would have made the runner
archive and delete the lesson's clean 35-item fact report, forcing a re-check of
thirty-five web-sourced claims none of which could have changed, because no study
block and no glossary entry had moved. On an account with far fewer tokens than
the others, that is a very large bill for a spelling entry.

**How to apply.** Before asking for a tidy in any field other than the note,
ask what it costs: a change anywhere else archives **both** checker reports.
Either batch the tidy into a pass that is already paying that price, or leave it
and record **why** it stays, so the next reader does not spend the bill on it
unknowingly. The same logic is why a stale figure should be *removed* from a note
rather than corrected — see [[n-nota-wat-n-toestand-vasvries-verouder]].

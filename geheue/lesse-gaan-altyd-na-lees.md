---
name: lesse-gaan-altyd-na-lees
description: "Drico, 22 Sep 2026: every finished lesson's PDF goes to lees/ as well, without being asked; Voltooide lesse is Lampies' delivery folder and does not replace it."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-09-22T20:16:53.008Z
---

**Drico, 22 September 2026: "I want my things to always be in the lees folder. Thats how I have
always done it."** He asked where the Grade 6 lessons were, because sign-off now copies PDFs to
`Voltooide lesse/Graad N/<Vak>/<Subonderwerp>/` (Lampies, 21 Sep) and nothing had reached `lees/`.

**Why:** `lees/` is his own outbox - he moves PDFs from there to the outside Afrikaans checker and
to the HTML team (see [[lees-is-n-uitbak-nie-n-argief-nie]]). A folder he did not ask for does not
replace the one he works from, and he should not have to ask each time.

**Naming, Drico 22 September 2026: "hou die naam van die les saam met die lesnommer".**
The number is the YEAR number, 1 to the last lesson of that grade, not a number inside a
sub-topic: `Les 01 - Verskillende plekke, verskillende plante en diere.pdf`. Year numbers come
from the approved specs (`jaarnommer`); where one is missing or wrong, take the order from CAPS
itself. Three Grade 5 specs were fixed this way on 22 Sep (geraamtes-as-strukture 6,
stelsels-om-dinge-te-beweeg 22, die-planeet-aarde 23). The renaming script is in the scratchpad,
`lees_hernoem.py`.

**How to apply:** when a subject-grade is signed off, copy every approved PDF to
`lees/gr<N>/<vak-slug>/Les NN - <titel>.pdf` and write `BESKERMDE-WOORDE.md` beside them
(the protected words that actually occur in those lessons, with the reason and where each one
appears - the generator lives in the scratchpad, `gr6_beskermde.py`). `lees/` is gitignored, so it
never travels with the repository. Both copies exist on purpose: `Voltooide lesse` for Lampies,
`lees/` for Drico.

## A stale copy in the outbox looks finished

**2 October 2026.** I reported that nothing had been reaching the outbox. **That
was wrong** — my search pattern did not match the real filenames (`Les 02 - ...`,
not `les-02`), and I passed the miss on as a fact. Three lessons were there.

What was actually wrong was worse than missing. **One of the three PDFs was from
two days earlier and carried a claim a person had since withdrawn** — the scope
qualifier on the limitation rule — plus three superseded shared definitions. Sent
on, the Afrikaans checker and the HTML team would have received a retracted claim
and three stale wordings, and nothing downstream compares an outbox PDF against the
approved lesson.

**How to apply.** Sign-off delivers to `Voltooide lesse/` automatically; **the
outbox copy is manual and therefore drifts.** So on every sign-off, do not just
check whether a file is *present* — compare it byte-for-byte against the current
approved PDF and refresh it if it differs. A file sitting there is the failure mode,
not an absent one. And the protected-words page has to be rebuilt at the same time,
because its word list depends on which lessons are being sent.

## 8 October 2026: the outbox is built by script now, and happens at sign-off

The hand-assembled page had gone stale in the way that matters: it still announced
**four** lessons beside **eight** PDFs, and four of those PDFs predated the last repair
of their drafts. So `bin/uitbak.py` now does the whole job, and sign-off calls it — a
lesson reaches the outbox without anyone remembering.

**Four things it settles, each of which had been got wrong at least once:**

* **The page is generated from the function that builds the real language-check block**,
  not from a second reading of the word lists. So it cannot claim a word is protected
  that the block never mentions, and the count on it is measured. (That function had to
  be lifted out of the block builder first; the move is proven byte-identical on every
  lesson in the repository — see [[n-module-buite-sy-boom-lees-niks]] for how nearly
  that proof went wrong.)
* **The number in the file name is the YEAR number**, from the approved spec's
  `jaarnommer`, which is Drico's own ruling and what Graad 4 Geografie on disk already
  looks like. A missing `jaarnommer` is reported, not guessed.
* **A split subject gets a split folder.** Graad 6 Sosiale Wetenskappe runs two parallel
  year numberings, so Geskiedenis 20 and Geografie 20 are different lessons with the same
  file name, and a flat copy of both would have one silently overwrite the other. The
  folder is `sosiale-wetenskappe-geskiedenis` / `-geografie`, and the collision is
  **checked** on every run rather than assumed away: if two lessons claim one number,
  neither is sent and both are named.
* **A PDF older than its draft's last content change is refused, loudly.** That is the
  real hazard, because a stale PDF in the outbox is read as the lesson. The comparison is
  against the recorded content change, not the file's clock.

**An empty outbox folder is not a gap.** `lees/` is an outbox and Drico empties it as he
collects, so a subject with 37 approved lessons and nothing in the folder is the success
state. I started to report that as a delivery failure before remembering
[[lees-is-n-uitbak-nie-n-argief-nie]]. Only NEW sign-offs need to be placed there.

---
name: n-skrywer-se-voorspelde-risiko-gaan-verlore
description: "A writer often predicts, in writing, the exact way its own fix will overshoot — and records it in the provenance note, which is stripped before the fact checker reads the lesson. Carry that prediction into the next check brief by hand, or it reaches nobody."
metadata:
  type: feedback
---

**Gr 4 Geography settlements, 29 September 2026.** The lesson-2 writer split architects
from engineers to fix a real error, and wrote in its own note: *"If a later check reads
the two sentences as implying engineers never touch buildings, that sentence is the fix,
and it costs about ten words."* It then judged the ten words not worth spending.

The next fact check found exactly that, with a legal citation: under the National
Building Regulations a building's structural design must be done by a professional
engineer. The writer had named the failure, named the fix, and priced it — a cycle
before it happened.

**Why it goes nowhere on its own.** The prediction lives in the draft's provenance note,
and `hardloop.py` strips that note from the copy the fact checker reads — deliberately,
so the checker cannot read the lesson charitably through the writer's intent. See
[[die-herkoms-nota-lek-die-spek-na-die-feitenasiener]]. So the one place a writer records
"here is how this fix might be wrong" is the one place the next checker will never look.
The coverage checker does see it, but a risk of this kind is a fact question, not a
coverage question.

**How to apply.** The writer's REPORT back is a separate channel from the note, and it
reaches the person running the pipeline. When a writer names a risk in its report,
**put it in the next check brief as something to test** — and name the direction, since
these failures are directional. It worked twice here: telling the fact checker to check
"that nothing now implies engineers have no part in buildings, which would be the
opposite error" is what produced the finding.

**The shape to watch for, because it was the same all three times it happened in this
sub-topic:** a fix that makes a true statement EXCLUSIVE. Two professions split into
lists that share nothing. A reason narrowed until it excludes the right examples for the
wrong cause. A definition tightened until the sentence beside it over-claims. Each fix
was correct in itself and each broke something adjacent. Related:
[[n-versagting-vat-die-algemene-helfte-saam]], [[n-regstelling-ontwrig-sy-bure]],
[[moenie-n-regstelling-verder-vat-as-die-bevinding-nie]].

Ask after every revision: **what did this change do to its neighbours** — not whether the
finding is gone.

## The other thing that note holds, and now gets asked for

1 October 2026. A writer also records, in the same provenance note, **which words it
expects the outside language checker to undo**. One Grade 6 lesson listed ten. Three
were not in the protected-words file — a court's official name, a population term whose
obvious swap reopened an ambiguity three rounds had closed, and one half of a pair whose
swap breaks the sentence in *both* directions.

Nothing carried them. The language-check builder reads only the protected-words file;
the fact checker's copy strips the note on purpose. So the list sat in the draft, correct
and unread, until a writer happened to mention it in its hand-back.

`bin/taalnasien.py` now prints a reminder to stderr — never into the block being pasted —
naming the draft and saying the block knows only the file. It deliberately does **not**
parse the note: a pattern over Afrikaans prose that finds nothing reads exactly like a
lesson with nothing to find, and that cost two afternoons already
([[n-wag-wat-sy-eie-reels-naskryf]]).

**How to apply:** when a writer hands back, read its provenance note for the protection
list and move anything missing into the file **with its reason** — a bare prohibition
does not hold when the sentence reads awkwardly. One of the three had a reason worth more
than the word: the obvious swap was wrong for a reason the lesson itself had spent three
rounds establishing elsewhere. See [[onaantasbare-woorde-vir-die-taalnasiener]].

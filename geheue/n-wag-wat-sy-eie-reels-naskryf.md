---
name: n-wag-wat-sy-eie-reels-naskryf
description: "A check that keeps its own copy of the rules of the thing it checks drifts from it silently. Compare against the producing function, not against a second list."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-10-01T07:11:13.801Z
---

1 October 2026. The guard that tells me whether a fact checker's copy is level
with its draft kept **its own list** of the fields the copier withholds. The
list held one of the two. So:

* every signed-off lesson reported its copy stale on **every** run, and the
  rewrite was byte-for-byte identical — the check's own comment says it exists
  to prevent exactly that ("would report every copy stale on every run and train
  everyone to ignore it");
* and it was **blind** to 30 copies that really were out of date, because it
  threw away the one field it did know about before comparing.

Both failures from one duplicated rule. The over-report is the one you notice
and learn to discount; the under-report is the one that matters, and it rode in
behind it.

**Why:** the number printed by that guard is the only thing that makes the fact
checks after it mean anything — "0 behind the draft" is the answer worth having.
A guard that cries wolf on the same three files for weeks gets read as noise,
and then its silence gets read as noise too.

**How to apply.** When a check asks "does this derived file still match its
source", call the function that derives it and compare the result. Never
restate its rules in the checker. I factored the copier's transform into a pure
function and had the guard call it; now a new withheld field cannot drift the
two apart, because there is only one definition.

Same family, different shape: the stale-order sweep tries to recognise an order
by a list of imperative verbs, so an order phrased as a statement is invisible
to it — and that limit is written into the script, because extending the verb
list fired on its own records. Where a check cannot call the real rule, say in
its output what it cannot see.

## And one thing no pattern can do in this repository

1 October 2026, my second attempt at mechanising that same decision. Instead of
recognising orders, look for a signature: a record says a form was withdrawn and
**quotes** it, so if a long piece of that quotation still appears in the field's
ordering half, the order is probably still giving it. Meaning-free, and it would
have caught the statement-shaped ones.

It found **zero of sixteen** known cases — and I only knew that because I ran it
against a commit that definitely carried them before believing it. One reason was
tunable (records announce a withdrawal in many more ways than a verb list holds,
sometimes with no verb at all, just a cross-reference to the new prohibition).
The other is not: **Afrikaans writes its indefinite article with an apostrophe.**
Nearly every sentence in these fields contains `'n`, so a single-quote regex
cannot delimit a quotation in this repository's prose — it truncates at the first
article inside the quoted run. There is no quoting convention here to stand on.

**How to apply:** two failed attempts at the same thing is the signal to stop.
The reliable detector for a withdrawn order left standing is an agent reading the
field from the top, which found all sixteen. The script's job is to say *where*
to look. And before trusting any new text-pattern check in this repo, test the
delimiter against a sentence containing `'n` — see
[[my-soektogte-mis-en-dan-glo-ek-hulle]].

See
[[n-skrip-wat-parse-is-nie-n-skrip-wat-werk-nie]],
[[n-ruil-wat-nie-pas-nie-moet-hard-faal]],
[[die-feitenasiener-lees-n-verouderde-konsep]].

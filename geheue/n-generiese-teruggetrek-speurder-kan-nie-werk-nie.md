---
name: n-generiese-teruggetrek-speurder-kan-nie-werk-nie
description: "Twice in one session I built a generic detector for \"a withdrawn wording still ordered elsewhere\" and had to delete it; the text cannot support it."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9cbb5026-bd75-4aa5-a144-0346fd07bf1f
  modified: 2026-10-01T13:42:24.563Z
---

The most expensive recurring fault in the content repository is a wording corrected in
one field while another field still orders it — a coverage checker finds it, the draft
is correct, and the round is spent. On 1 October 2026 I twice tried to automate finding
it, and deleted both attempts.

**Attempt one** scanned for a withdrawn claim near a live one by proximity: 792 hits,
71 after filtering, 28 at a tight window, with no genuine hit among them.

**Attempt two** worked from the dated markers themselves — pull each quotation that
follows a withdrawal verb inside a marker, then report that exact phrase where it
appears outside every marker. Tighter, and still unusable: 58 hits on one grade, 6
across ninety specs at a six-word minimum, and the survivors were a quotation from a
source, a correction's *own* new wording, and a field quoting the lesson sentence it
was itself diagnosing.

**Why it cannot work:** a dated marker in this repository legitimately holds three
kinds of quotation in the same punctuation — the wording it withdraws, the wording it
installs, and the lesson sentence it diagnoses. Nothing in the text distinguishes them.
Below about six words the quotations are terms, which live everywhere by design; above
it they are too rare to catch the common case. A sweep that fires on the healthy shape
gets ignored, which is worse than no sweep.

**What does work, and it is not detection:** `beweringveeg.py`, where I name the claim.
The gap was never finding the fault — it is that I write a withdrawal and do not sweep.
So the fix is procedural: **in the same script that writes a withdrawal, sweep for the
old wording by name and assert the count.** Not a later grep, not a later tool. Related:
[[die-korrigeerde-opdrag-bly-in-die-veld-staan]], [[die-spek-was-die-fout-sewentien-keer]],
[[n-skrip-wat-parse-is-nie-n-skrip-wat-werk-nie]], [[moenie-op-voorkoms-sorteer-nie]].

---
name: die-drifveeg-lees-net-woordelysinskrywings
description: "The drift sweep compares begrip blocks only. It printed 'Geen drif' while two lessons still carried the withdrawn wording in their study text."
metadata:
  node_type: memory
  type: project
---

13 October 2026. Lampies decided the Grade 6 wording of `kieme`. I wrote it into the
shared list and ran `bin/woordelysdrif.py` to confirm, and it printed:

> Geen drif. Al 39 gedeelde terme is woord vir woord dieselfde oor die 73 lesse.

**That was true and it meant almost nothing.** Medicine lessons 6 and 7 were at that
moment still carrying the *withdrawn* sentence — the one claiming a germ is visible
only under a microscope — word for word in their study text. I only caught it because
I went and grepped the drafts instead of trusting the clean line.

**The mechanism:** the sweep compares `begrip` blocks. Only lesson 5 had a `begrip`
for `kieme`; lessons 6 and 7 state the wording in prose, as a study sentence. One
glossary entry cannot disagree with itself, so the sweep reported perfect agreement
over a term that was live-wrong in two lessons.

This is why the sub-topic's own spec says lessons 6 and 7 must "reuse the sentence
word for word" — the house knows the wording travels in prose. The sweep does not.

**How to apply:** after any wording decision, the drift sweep is the *weaker* of the
two checks. Grep the subject's drafts for the withdrawn form and for the new one, in
study text and list items as well as glossary entries, and quote how many lessons
carry each. A decided wording is only delivered where it actually appears.

The same trap sits in the opposite direction: a term with no `begrip` block anywhere
is invisible to the sweep entirely, so "39 shared terms" is a count of entries, not of
shared vocabulary. Related: [[n-skoon-toets-is-so-wyd-soos-sy-omvang]],
[[geen-drif-is-net-so-sterk-soos-die-besluitlys]], [[n-begrip-word-alleen-gelees]],
[[vee-die-bewering-oor-al-die-spesifikasies]].

---
name: die-handwysig-wag-werk-meestal-nie
description: The guard that saves a writer's hand-edit to an extract is mostly inactive (the runner doesn't stamp) and its 48 alarms were all merge artefacts — absence of a saved copy proves nothing.
metadata:
  type: reference
---

The pipeline is supposed to protect a writer's hand-edit to a spec extract: a fingerprint
stored inside each extract, a check that content still matches it, and the old file saved as
`les-N.verlore.json` with an instruction to port the change to the approved spec and then
delete the copy. Investigated on 12 October 2026 because 48 such copies had accumulated.
Both halves of the mechanism are broken, in opposite directions.

**Every alarm so far was a false one.** All 48 copies came from three git merges between the
parallel machines, not from anyone editing an extract. The fingerprint lives INSIDE the file
it certifies, so git merges content and fingerprint as independent lines and pairs one
machine's content with another machine's fingerprint; the refresher then correctly observes
the mismatch and reports a direct edit. All 48 reproduce an approved-spec revision exactly,
field for field, checked three independent ways with the detector validated against planted
edits. 48 false alarms in six days, zero true ones. They hold nothing to port.

**And the guard is mostly inactive, which is the serious half.** The runner writes extracts
with NO fingerprint, and the check returns "not hand-edited" when there is no fingerprint.
The runner is called at every pipeline step, so extracts spend most of their lives unstamped
— and an edit to an unstamped extract is erased by the next refresh silently, with no copy
saved. **So the absence of a `.verlore.json` is not evidence that nothing was lost.** No copy
exists for 19 September 2026, the day a Grade 4 correction was lost exactly this way, which
fits the hole rather than the protection working.

**How to apply.** Never reassure yourself with "no saved copies, so nothing was lost". When a
writer reports fixing a requirement, ask which file it wrote to and port it yourself, the same
day — that instruction in the content standard is load-bearing precisely because the automatic
net has holes. Related: [[moenie-in-die-spek-skryf-wat-jy-nie-nagegaan-het-nie]],
[[n-wag-wat-sy-eie-reels-naskryf]], [[die-herstellus-blaas-die-spek-op]],
[[drie-rekenaars-werk-parallel]].

**12 October 2026, LATER THE SAME DAY: the code half of this note is now out of date, and I
am leaving the note because the HABIT it teaches is not.** Both faults were fixed. The runner
now stamps on every write, so the guard has continuous cover and an edit to an unstamped
extract is no longer erased in silence. And the refresher now tells four cases apart instead
of one: an ordinary spec change, a merge artefact (named, with the commit and date, saving
nothing), a genuine direct edit (the old warning, the copy saved), and an unstamped file
(split by whether git knows the content). Proved across all 387 extracts with one of each
condition planted, and the two specification sweeps byte-identical before and after.

So "the absence of a saved copy proves nothing" was true of the code as it stood and is no
longer. **What stands unchanged is the advice**: when a writer reports fixing a requirement,
ask which file it wrote to and port it yourself the same day. The automatic net is now real,
but it catches a writer's edit to a generated file — not the slower loss, which is a
correction that reaches no file at all because nobody acted on the hand-back.

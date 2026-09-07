---
name: die-spek-en-die-les-noem-dieselfde-veld-anders
description: A spec's kaps_onderwerp is the CAPS topic, a lesson's kaps_onderwerp is the sub-topic; a writer copying the field across gets it wrong.
metadata:
  type: project
---

The lesson schema says `kaps_onderwerp` holds the **sub-topic** ("Die Maan").
A spec holds **both** `kaps_onderwerp` (the broad CAPS topic, "Persoonlike en
Sosiale Welsyn") and `kaps_subonderwerp` (the sub-topic). So the field with the
same name means different things on either side, and a writer copying it across
by name puts the topic where the sub-topic belongs.

Six of seven Life Orientation writers followed the 24 delivered NWT lessons and
got it right; one copied the spec's field and did not. One writer spotted the
ambiguity and said so unprompted.

**Why:** nothing checks it. The gate does not read `kaps_onderwerp`, so a lesson
with the wrong value passes clean and reaches the layout team mislabelled. It
is invisible until someone sorts or groups by it.

**How to apply:** after a batch of drafts, compare `kaps_onderwerp` across all
of them and against the subject's existing delivered lessons. It is metadata,
not wording, so correcting it directly is fine — see
[[moenie-self-inhoud-skryf-nie]] for where that line falls. Worth fixing in the
schema reference or the writer prompt so the trap stops existing.

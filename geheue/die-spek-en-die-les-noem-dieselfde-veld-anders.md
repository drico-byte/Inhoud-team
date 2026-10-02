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

## A glossary entry: `teks` in a draft, `omskrywing` in the agreed list

**1 October 2026.** A draft's glossary block holds its definition under **`teks`**
(`{"tipe": "begrip", "term": ..., "teks": ...}`), while the agreed-wordings file
holds the same thing under **`omskrywing`**. I wrote a quick probe reading
`omskrywing` from the drafts, got empty strings, and it reported two lessons as
carrying a *different* wording — a drift finding that did not exist.

**Why this bites harder than the other pair:** reading the wrong key returns
empty rather than raising, so the probe produced confident, plausible, false
output. And it contradicted the real sweep, which had just reported zero drift
across all 73 lessons.

**How to apply:** the authoritative tools already know these names — prefer
running `bin/woordelysdrif.py` over writing a probe. If a probe must be written,
**print the values it is comparing and sanity-check one by hand** before trusting
a verdict; and when an ad-hoc check contradicts a purpose-built one, assume the
ad-hoc check is wrong. See [[my-soektogte-mis-en-dan-glo-ek-hulle]].

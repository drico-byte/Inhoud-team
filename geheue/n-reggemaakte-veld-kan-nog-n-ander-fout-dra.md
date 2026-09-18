---
name: n-reggemaakte-veld-kan-nog-n-ander-fout-dra
description: "My source sweeps skipped every field already opening with REGGEMAAK, so a field corrected for one fault kept a second, live one."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-09-10T15:42:36.031Z
---

Sweeping a spec for a false claim, I wrote `if not v.startswith('REGGEMAAK')` to
avoid stacking a correction on a correction. That silently exempted exactly the
fields most likely to be wrong. One field carried a dated correction about the
vertebrae and, three lines below it, still held up "'n skedel is 'n harde bak om
die brein" as its model of a good explanation — the image a fact check had
contradicted that same morning. My sweep reported the file clean. A writer found
it and told me; I only believed it after searching again.

**Why:** a dated correction is scoped to the fault it names, not to the field it
sits in. A long spec field usually holds several claims, and the presence of one
correction says nothing about the others. Worse, the marker makes the field look
handled, so it gets skipped by eye as well as by regex.

**How to apply:** sweep on the CLAIM, never on whether the field looks corrected.
Guard against duplicates by testing for the correction's own distinctive phrase
(`'BAK-beeld' not in v`), not for the marker. After a sweep, re-read the file and
assert that no live instance of the claim survives — the assert is what turned
this from an opinion into a fact. Related: [[n-regstelling-ontwrig-sy-bure]],
[[n-spek-se-dieselfde-ding-in-twee-velde]], [[ek-skryf-my-regstelling-bo-op-sy-weerlegging]],
[[my-soektogte-mis-en-dan-glo-ek-hulle]].

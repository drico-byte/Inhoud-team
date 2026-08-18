# Lesson JSON schema — field reference

Schema version 1.0. Bump `skema_weergawe` on any breaking change and tell the
HTML team, since the version is the contract between the two pipelines.

Keys are Afrikaans to match the content language. A complete lesson that passes
the gate is at `assets/verwysingsles.json`.

## Top-level fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `skema_weergawe` | string | yes | `"1.0"` |
| `status` | string | yes | `konsep` \| `gated` \| `goedgekeur` |
| `titel` | string | yes | Lesson title as a learner sees it |
| `graad` | integer | yes | 4–12. Selects the register band. |
| `vak` | string | yes | e.g. `"Sosiale Wetenskappe"` |
| `kaps_onderwerp` | string | yes | The CAPS sub-topic, e.g. `"Vervoer op water"` |
| `kaps_punt` | string | yes | The specific CAPS bullet this lesson covers |
| `woordelys` | array of strings | no | Subject terms to silence spellcheck warnings |
| `herkoms` | object | yes | Provenance — see below |
| `blokke` | array of objects | yes | The content. At least one `studie` block. |

## `herkoms` — provenance

Not decoration. This is the record that answers, years later, how a lesson was
made. Reconstructing it after four hundred lessons is impossible.

| Field | Notes |
|---|---|
| `kaps_dokument` | Which CAPS document and section the content came from |
| `profiel_konfig` | Which profiler config supplied the bands and budget |
| `skrywer_prompt` | Writer prompt version, e.g. `"skrywer-v1.2"` |
| `handboek_gesien` | Boolean. **Must be `false`** for anything publishable. |

`handboek_gesien: true` marks calibration material — a lesson transcribed from or
informed by a textbook, useful for measuring, never for publishing. The status
must stay `konsep` and the HTML team must never receive it.

## Block types

Every block has `tipe`. Other fields depend on it.

### `studie` — the material a learner revises

| Field | Required | Notes |
|---|---|---|
| `kop` | yes | Heading. Must be unique within the lesson — `eli10` blocks reference it. |
| `teks` | yes | Prose. Sentences ending in `.`, `!`, or `?`. |

**Counts toward the study budget. Measured against the grade's register band.**

Guide: 30–110 words per block, 3–10 blocks per lesson. These are comprehension
guides, not layout requirements — the HTML layout adapts to the content, so chunk
on conceptual seams. Warnings only.

### `eli10` — the intuition layer

| Field | Required | Notes |
|---|---|---|
| `vir` | yes | Must exactly match the `kop` of the `studie` block it explains |
| `teks` | yes | Must contain a concrete comparison, not a paraphrase |

**Does not count toward the study budget. Measured against the flat ELI10 band.**

`vir` lets the layout team place the intuition beside its concept rather than
collecting them at the end, and lets the coverage checker confirm that the
concepts the planner flagged as difficult are the ones actually covered.

### `lys` — bullet or numbered list

| Field | Required | Notes |
|---|---|---|
| `kop` | yes | Heading |
| `items` | yes | Array of strings, one per item |

**Counts toward the study budget. Excluded from prose register statistics** —
list items are not sentences, and measuring them as prose distorts mean sentence
length badly.

They are checked separately on their own terms: **28 words maximum per item**
(hard fail), 18 as a guide, and a warning at two or more commas. Without this,
excluding lists from the register check would let a writer park difficult
subordinated prose in a `lys` block and escape the band entirely. A list item is
a short scannable point, not a sentence carrying clauses.

### `begrip` — glossary entry

| Field | Required | Notes |
|---|---|---|
| `term` | yes | The word being defined |
| `teks` | yes | Definition, 8–12 words |

Does not count toward the study budget. Any word over 10 characters in the study
text that is not a proper noun should have one.

### `vraag` — retrieval question

| Field | Required | Notes |
|---|---|---|
| `teks` | yes | The question |

Does not count toward the study budget. Three per lesson. Prefer inference over
recall.

## Reserved for later

`model` — structured spatial data for 3D or diagram rendering (parts, spatial
relationships, flow, what a learner can manipulate). Needed for Life Sciences and
similar subjects where the spatial relationship *is* the learning objective. Not
implemented in schema 1.0. Bump to 1.1 when adding it, and only add it when a
subject actually needs it — 2D illustration covers everything else.

The criterion for flagging a concept as spatial: only when the spatial
relationship is the thing being learned. Cell structure, molecular geometry,
plate tectonics — yes. Photosynthesis chemistry, food webs, classification
hierarchies — no; those are flow and relationship diagrams, and 3D obscures them.
Left unbounded, "could be 3D" becomes "should be 3D" and a great deal of build
effort goes into rotating decoration.

## Handoff to the HTML pipeline

The schema is the contract. Design it as a handoff, not a conversation.

- Lesson JSONs live in a versioned folder per subject-grade in the repo. The repo
  is the queue: the content team commits, the HTML team reads on merge. Two teams
  that never call each other cannot break each other.
- The HTML team reads only `goedgekeur` files.
- The HTML team does not change wording. Spelling problems come back as a list
  for human approval, and corrections are applied **to the source JSON**, never to
  the rendered HTML — otherwise source and page drift apart and the JSON stops
  being the truth.
- `eli10` blocks need visual distinction on the page. If a learner cannot tell at
  a glance which text is intuition and which is revision material, the whole
  study-volume discipline collapses at the point of use: they revise everything,
  and the over-supply problem returns. This is the one layout requirement the
  content architecture genuinely depends on.

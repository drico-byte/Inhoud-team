# Lesson spec schema — field reference

Schema version 1.0. The planner produces one spec file per CAPS sub-topic. The
writer consumes one `lesse` entry at a time. The coverage checker checks a draft
against the same entry.

This is the contract between three agents, so changes need all three reviewed
together. A worked example is at `assets/voorbeeldspesifikasie.json`.

Validate with `scripts/spec_check.py` before handing specs to a writer — it
catches budget arithmetic errors, missing CAPS bullets and unjustified
Aanvulling, all of which are cheaper to fix here than twenty lessons later.

## Top-level fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `skema_weergawe` | string | yes | `"1.0"` |
| `vak` | string | yes | e.g. `"Sosiale Wetenskappe"` |
| `graad` | integer | yes | 4–12 |
| `kwartaal` | integer | yes | 1–4 |
| `kaps_onderwerp` | string | yes | The CAPS topic, e.g. `"Vervoer oor tyd heen"` |
| `kaps_subonderwerp` | string | yes | The sub-heading, e.g. `"Vervoer op water"` |
| `kaps_ure` | number | no | **Informational only.** Never used in arithmetic. |
| `fokusvraag` | string | yes | The CAPS focus question this sub-topic serves |
| `profiel_konfig` | string | yes | Which profiler config supplied the volume figure |
| `onderwerp_woorde` | integer | yes | Measured textbook words for this sub-topic |
| `totale_begroting` | integer | yes | Must equal the sum of lesson budgets |
| `lesse` | array | yes | One entry per lesson |

## `lesse` entries

| Field | Type | Required | Notes |
|---|---|---|---|
| `nommer` | integer | yes | Sequence within the sub-topic, from 1 |
| `titel` | string | yes | Working title. The writer may improve it. |
| `kaps_punt` | string | yes | The CAPS bullet, quoted as it appears |
| `begroting` | integer | yes | `round(onderwerp_woorde / lesson_count)` |
| `kern` | array of strings | yes | Core content items, drawn from the CAPS bullet |
| `aanvulling` | array of objects | no | Each `{item, regverdiging}` |
| `moeilike_konsepte` | array of strings | no | Concepts needing an ELI10 layer |
| `termdig` | boolean | no | `true` when the bullet names many terms |
| `fokusvraag_skakel` | string | yes | How this lesson serves the focus question |

### `kern`

The Core content, taken from what CAPS names. Where a bullet lists items
explicitly ("Chinese junks, Arabiese dau, karvele, Britse hoë skepe,
klipperboot"), every named item becomes a `kern` entry — CAPS naming them makes
them mandatory, and this is the most prescriptive CAPS gets.

Where a bullet is broad ("Die eerste stoomskepe"), the planner decides what the
concept minimally requires and lists those as `kern`. State them as *content
requirements*, not as sentences to write.

### `aanvulling`

Content not named in CAPS. Each entry needs a written justification, and the test
is: **would the concept be incomplete or meaningless without it?**

The strongest justification is consistency with CAPS's own approach. CAPS names
people where a person anchors a breakthrough ("Wright broers en die uitvinding
van die eerste vliegtuig"), so applying that pattern to another breakthrough
follows CAPS rather than departing from it.

Total Aanvulling across a lesson stays within about 25% of its budget. Without a
cap the writer will justify anything as educational.

### `moeilike_konsepte`

Concepts where a learner needs intuition before formal explanation. The writer
produces one `eli10` block per entry, and the coverage checker verifies each one
exists.

Be selective. "Vlotte is plat bote van hout" needs no intuition layer. "How steam
pressure produces movement" does. Flagging everything makes the flag meaningless.

### `termdig`

Set `true` when a bullet introduces many new subject terms — typically because
CAPS names several items. It tells the writer to expect five or six `begrip`
entries rather than two, so the glossary load is planned rather than discovered.

## Budget arithmetic

```
onderwerp_woorde = pages_for_subtopic × words_per_page    (from the profiler)
begroting        = round(onderwerp_woorde / lesson_count)
totale_begroting = sum of lesson budgets
```

**CAPS contact hours are deliberately not used.** They tell a teacher how long to
spend on a topic. They say nothing about how many words a learner reads, because
classroom time is filled with discussion, drawing, group work and practice as well
as text. Treating hours as a words-per-hour conversion rate confuses teaching time
with reading volume, and the two do not track each other.

Record `kaps_ure` if you like — it is useful provenance — but nothing derives from
it, and the validator says so whenever it appears.

**Budgets are divided evenly across the lessons in a sub-topic.** A sub-topic's
measured volume is the parity anchor; how it splits is arithmetic, not judgement.
Uneven division would mean substituting an opinion about relative importance for a
measurement, which is the kind of thing that quietly drifts over hundreds of
lessons.

Rounding can move the total by at most one word per lesson. The validator allows
that and nothing more.

## Worked example

CAPS Gr 4 SW, Kwartaal 3, "Vervoer oor tyd heen", sub-topic "Vervoer op water":

| | |
|---|---|
| CAPS bullets | 4 |
| Lessons | 4 (one per bullet) |
| Measured sub-topic volume | pages 135–140, **1 028 words** |
| Budget per lesson | 1 028 / 4 = 257 |
| `totale_begroting` | 1 028 |

Note that this volume was **measured, not derived**. An earlier version estimated
it as 6 pages × the book-wide median of 199 words = 1 194, which was 16% too high:
the section actually runs at 171 words per page because it is illustration-heavy.
Always run the profiler over the sub-topic's own page range.

A named case study is always its own lesson — CAPS lists it as its own item.

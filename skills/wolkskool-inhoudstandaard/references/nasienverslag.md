# Checker report schema — field reference

Schema version 1.0. Both checkers emit this shape so the orchestrator can branch
on one contract instead of two.

**Validation is the orchestrator's job, not a checker's.** The validator is
`skills/wolkskool-inhoudstandaard/scripts/verdict_check.py`, and it is run against
every report before anything acts on it. Neither checker is granted a shell, on
purpose: a checker that could run the validator would be tempted to edit its own
findings until the validator was happy, which is the opposite of what a check is
for. So write the report to the schema and stop — do not try to validate it, and do
not report the inability to as a problem.

## Top-level fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `skema_weergawe` | string | yes | `"1.0"` |
| `nasiener` | string | yes | `dekking` \| `feite` |
| `prompt_weergawe` | string | yes | e.g. `"feitenasiener-v1.0"` |
| `les` | string | yes | The lesson title checked |
| `kaps_punt` | string | yes | The CAPS bullet, copied from the lesson |
| `verdict` | string | yes | `GOEDGEKEUR` \| `HERSIEN` \| `MENS_NODIG` |
| `items` | array | yes | One entry per thing checked |
| `opsomming` | string | yes | One sentence. What a human needs to know. |

## The three verdicts

**`GOEDGEKEUR`** — nothing to fix. Proceed.

**`HERSIEN`** — defects the writer can act on. Back to the writer with the item
list. This is the normal failure route.

**`MENS_NODIG`** — something the writer cannot fix alone, so escalate to a person
rather than looping. Use it when:

- a claim cannot be verified either way and the lesson depends on it
- the spec itself looks wrong (a `kern` item that makes no sense for the grade, a
  budget that cannot hold the content listed)
- sources contradict each other on a substantive point

The distinction matters. A writer sent a defect it cannot resolve will either
invent a fix or strip the content, and both outcomes are worse than asking a human.
Revision loops cap at two cycles; `MENS_NODIG` is how you exit early rather than
burning both.

## `items` — coverage checker

| Field | Required | Notes |
|---|---|---|
| `tipe` | yes | `kern` \| `aanvulling` \| `vraag` \| `fokus` (`eli10` was abolished 23 September 2026) |
| `verwysing` | yes | The spec item being checked, quoted |
| `status` | yes | `teenwoordig` \| `gedeeltelik` \| `afwesig` |
| `bewys` | yes | Which block covers it, by `kop`. Empty if absent. |
| `aksie` | when not `teenwoordig` | What the writer must do |

## `items` — fact checker

| Field | Required | Notes |
|---|---|---|
| `bewering` | yes | The claim, quoted from the lesson |
| `blok` | yes | The `kop` of the block containing it |
| `status` | yes | `bevestig` \| `weerspreek` \| `onseker` |
| `bron` | when `bevestig` or `weerspreek` | Where it was checked |
| `regstelling` | when `weerspreek` | The corrected claim |
| `tipe` | no | `superlatief` \| `datum` \| `getal` \| `naam` \| `analogie` \| `algemeen` |

`onseker` is a real outcome, not a failure to try. A claim that cannot be settled
should be flagged for a person, not quietly passed or quietly deleted.

## Verdict mapping

The orchestrator derives routing from the items, so a checker cannot pass a report
whose verdict contradicts its own findings — `verdict_check.py` enforces this:

| Findings | Verdict |
|---|---|
| any `weerspreek`, or any `afwesig` `kern` item | `HERSIEN` |
| any `onseker`, or a spec problem noted | `MENS_NODIG` |
| `gedeeltelik` items only | `HERSIEN` |
| all clear | `GOEDGEKEUR` |

Where both apply, `MENS_NODIG` wins: a human should see it before the writer
touches it again.

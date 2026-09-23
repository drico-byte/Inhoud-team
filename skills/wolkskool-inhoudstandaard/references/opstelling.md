# Setup

## Dependencies

```bash
pip install pyphen spylls --break-system-packages
```

`pyphen` ships with Afrikaans hyphenation built in — nothing extra to install.
It supplies the syllable counts.

## Afrikaans spellcheck dictionary

Optional. Without it the gate still runs and reports a note.

```bash
sudo mkdir -p /usr/share/hunspell
sudo curl -sL -o /usr/share/hunspell/af_ZA.aff \
  https://raw.githubusercontent.com/LibreOffice/dictionaries/master/af_ZA/af_ZA.aff
sudo curl -sL -o /usr/share/hunspell/af_ZA.dic \
  https://raw.githubusercontent.com/LibreOffice/dictionaries/master/af_ZA/af_ZA.dic
```

## Running the profiler

Once per subject-grade, before any lesson is written. **This is the only tool
permitted to read a textbook.** It emits numbers; no prose is retained.

```bash
python3 skills/wolkskool-inhoudstandaard/scripts/profiler.py book.pdf --caps caps_subtopics.json --out gr4-sw.json \
  --first 118 --last 148 --eindmerker "Onderwerp 4"
```

`--caps` is a small JSON file listing the CAPS sub-topic labels **you** supply. The
profiler finds where each label's section begins in the book, so the structure comes
from CAPS and only page counts and word volumes come from the textbook.

`--eindmerker` is the heading that follows the topic. Without it the final section
absorbs every page up to `--last` and its volume is unreliable — the tool warns when
this happens.

Default is 150 dpi, which is fast and finds headings reliably but undercounts words
by about 3%. Use `--dpi 300` for the final volume figures.

Check the output before trusting it: page counts should roughly track the CAPS hour
allocations, and any label under `nie_gevind` means a section was missed and its
label probably needs to match the book's wording more closely.

**Send the human the page counts and volumes. Do not pass section headings to the
planner** — the planner must derive lesson structure from CAPS alone.

## Running the gate

```bash
python3 skills/wolkskool-inhoudstandaard/scripts/gate.py lesson.json --grade 4 --budget 300 --log gate_log.jsonl
python3 skills/wolkskool-inhoudstandaard/scripts/gate.py lesson.json --grade 11 --budget 700 --json
```

`--json` emits the full result for an orchestrator to parse. `--log` appends one
JSON object per run to a JSONL file.

Exit 0 = pass, exit 1 = fail.

## What fails and what warns

**Hard fail** — send back to the writer:

- study-text word count outside budget ±15%
- mean sentence length outside the grade band
- syllables per word above the band ceiling
- 3+ syllable percentage above the band ceiling
- commas per sentence above 0.35
- a `lys` item over 28 words
- no `studie` blocks at all

**Warning** — log, review, do not auto-reject:

- any of the above breached by less than 6% (marked `[marginal]`)
- block count or block size outside the comprehension guide
- a `lys` item over 18 words, or with two or more commas
- long words with no `begrip` entry
- possible spelling errors
- **any `eli10` block at all — a hard FAIL since 23 September 2026, when Drico abolished the block.** Delete it and change nothing else; its content does not move into the study text
- suspiciously long single sentence — usually a missing full stop

## Reading the log

The JSONL log is the instrument for improving prompts. After roughly twenty
lessons it will show systematic bias — whether the writer under-supplies, drifts
formal, or over-subordinates. Fix the pattern in the prompt once rather than in
twenty revision cycles.

Useful first pass:

```bash
python3 - <<'EOF'
import json
rows = [json.loads(l) for l in open('gate_log.jsonl', encoding='utf-8')]
rows = [r for r in rows if r.get('study')]
print("runs:", len(rows), " pass rate:",
      round(100*sum(r['verdict']=='PASS' for r in rows)/len(rows)), "%")
for k in ('words', 'mean_sentence_len', 'mean_syllables', 'pct_polysyllabic'):
    vals = [r['study'][k] for r in rows]
    print(f"{k:22} mean {sum(vals)/len(vals):.2f}  min {min(vals)}  max {max(vals)}")
from collections import Counter
c = Counter(f.split(':')[0].split(' — ')[0][:60] for r in rows for f in r['failures'])
for msg, n in c.most_common(8):
    print(f"{n:3}  {msg}")
EOF
```

If word count consistently sits below budget, the writer prompt needs a stronger
depth instruction. If sentence length consistently sits high, it needs a stronger
one-idea-per-sentence instruction. Both are prompt fixes, not per-lesson fixes.


## The report validator

```bash
python3 skills/wolkskool-inhoudstandaard/scripts/verdict_check.py report.json --les lesson.json --spek lesse_entry.json
```

Exit 0 = the report is sound. Exit 1 = malformed or self-contradictory. Note this
validates the **report**, not the lesson — a sound report can carry a `HERSIEN`
verdict, which is the pipeline working.

**Hard fail:**

- verdict does not follow from the report's own findings
- a fact item marked `bevestig` with no source recorded
- a fact item marked `weerspreek` with no correction
- a coverage defect with no action for the writer
- no `kern` items, or no `fokus` item, in a coverage report
- a coverage report checking fewer `kern` items than the spec contains
- empty `items`

**Warning:**

- a lesson block from which no claim was checked
- very few claims relative to block count, suggesting skimming
- no superlative among the fact items when the lesson may contain one
- a spec item whose wording does not obviously appear in the report

The split follows the same rule as the other scripts: counts and required fields are
deterministic and can fail; anything resting on string similarity can only warn,
because a checker that paraphrases a requirement should not be failed for phrasing.

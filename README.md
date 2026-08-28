# Wolkskool content pipeline

Scaffolding for producing CAPS-aligned Afrikaans lesson content. The standard
itself lives in `skills/wolkskool-inhoudstandaard/` and is authoritative; this
README is only how to drive it.

```
profiler (script, once per subject-grade)  → profiele/<config>.json
planner  (agent, once per CAPS sub-topic)  → spesifikasies/konsep/   [human approves]
writer   (agent, per lesson)               → konsepte/
gate     (script)                          → PASS, or back to the writer with numbers
coverage + facts (agents, in parallel)     → checker reports
verdict_check (script)                     → validates the reports themselves
                                           → human sign-off → goedgekeur/
```

The gate runs **before** the checkers: reviewing a draft that is about to be
rewritten for length wastes the review. Coverage and facts run in parallel and
stay separate — coverage needs the spec, facts must not have it. Two revision
cycles maximum, then a person; a `MENS_NODIG` verdict exits the loop immediately
instead of spending one.

## Copyright

Independent creation is a property of the process, not of the output, so it is
proven by showing the generation chain never had access to the source. Only the
profiler may read a textbook, and it emits numbers — page counts, word volumes,
register statistics. The planner and the writer see CAPS plus those numbers and
refuse a textbook however the offer is framed. Textbook PDFs are gitignored from
the first commit and OCR intermediates are written outside the repository
entirely, so the git history is the evidence: this repository has never contained
a textbook page. Facts are not copyrightable; selection, arrangement and
expression are, which is why matching a publisher's *lesson structure* is the real
exposure and why the planner is kept away from books rather than merely asked to
paraphrase.

## Setup

```bash
python bin/opstel.py
```

Creates the scratch directory, creates `bronne/`, links the standard into
`.claude/skills/` so Claude Code discovers it, and reports any missing
prerequisite. Run it after cloning and whenever something stops working.

Two things are configurable because they move between machines:

| | |
|---|---|
| `WOLKSKOOL_SCRATCH` | OCR scratch. Default `C:/temp/wolkskool-scratch`. Never inside the repo or OneDrive. Also `profiler.py --skrapruimte`. |
| `WOLKSKOOL_HUNSPELL` | Afrikaans dictionary base path, no extension. Tries `C:/hunspell/af_ZA` then `/usr/share/hunspell/af_ZA`. Also `gate.py --woordeboek`. |
| `WOLKSKOOL_GOEDGEKEUR` | Approved-output root. Default `../goedgekeur`. |

Spelling is a warning-level check, so everything works normally with no
dictionary installed — the gate reports a note and carries on.

## Profiling a new subject-grade

Once, before any lesson is written for that subject-grade. This is the only step
that touches a textbook.

1. Put the textbook in `bronne/` and the CAPS document in `kaps/dokumente/`.
   Both are gitignored, and stay that way. The textbook is a rights boundary — only
   the profiler may read it. CAPS is public and the planner is meant to read it; it is
   kept out of git only to keep the no-PDF rule absolute and therefore checkable.
2. Write the CAPS sub-topic labels into `kaps/`, in the shape of
   `skills/wolkskool-inhoudstandaard/assets/caps_subonderwerpe_voorbeeld.json`.
   The labels are yours: the profiler finds where each one starts in the book, so
   the structure comes from CAPS and only page counts and volumes come from the
   book.
3. Run it, over the topic's page range, with the heading that follows the topic as
   the end marker — without one the final section absorbs every page up to
   `--last` and its volume is unreliable:

```bash
python skills/wolkskool-inhoudstandaard/scripts/profiler.py bronne/boek.pdf --caps kaps/gr4-sw-kw3.json --out profiele/gr4-sw-kw3-profiel.json --first 118 --last 148 --eindmerker "Onderwerp 4" --dpi 300
```

150 dpi is fast and finds headings reliably but undercounts words by about 3%; use
300 for the volume figures you will budget from. Check the output before trusting
it — page counts should roughly track the CAPS hour allocations, and anything under
`nie_gevind` means a section was missed and its label needs to match the book's
wording more closely.

The runner finds a config by its *contents* — `vak`, `graad`, and the sub-topic —
so the filename is free. `gr4-sw-kw3-profiel.json` matches the supplied example.

Then run the planner for each sub-topic, and read what it produced.

## Running one lesson

```bash
python bin/hardloop.py --vak "Sosiale Wetenskappe" --graad 4 --subonderwerp "Vervoer op water" --les 3
```

Drop `--les` for an overview of every lesson in the sub-topic and where each one
has got to.

The runner does every deterministic step itself — the gate, both validators, the
routing, the logging — and then stops and names the one agent to invoke next, with
its exact inputs and output path. It does not invoke the agents: they are Claude
Code subagents in `.claude/agents/`, and there is no supported way to call a named
project subagent from a script. So the loop is: run it, do the step it names, run
it again. `--json` gives an orchestrating session the same thing machine-readably.

Exit codes:

| | |
|---|---|
| 0 | nothing outstanding: the approval completed, or the draft already carries
      `status: goedgekeur` and needs nothing further |
| 10 | waiting on an agent or on a person; the next action is printed |
| 1 | gate FAIL — back to the writer, with numbers |
| 2 | `MENS_NODIG` — a checker escalated |
| 3 | refused: missing profiler config, unapproved spec, bad arguments |
| 4 | a checker report is malformed or contradicts its own findings |
| 5 | revision limit reached, escalated to a person |

Every gate result appends to `logs/gate_log.jsonl`; every checker report is
archived to `logs/verslae/<les>/s<cycle>-<checker>.json`; every routing decision
appends to `logs/hardloop_log.jsonl`. These are how the prompts get improved after
twenty lessons, which is what `bin/logoorsig.py` reads:

```bash
python bin/logoorsig.py
```

It reports words against budget, mean sentence length against the band, and the
most frequent failure. A pattern there is a prompt fix; only a one-off is a lesson
fix.

### After editing a spec, refresh the extracts

The runner writes the per-lesson spec extract an agent reads, but only when it
runs for that lesson. So editing a spec and briefing a writer straight afterwards
hands it the *old* copy, and the agent reports — correctly — that the fix is not
there. Running the runner instead has a side effect you may not want: a changed
spec entry retires that lesson's coverage report.

```bash
python bin/vernuwe-uittreksels.py
```

It rewrites every extract from the approved specs and does nothing else — no
gate, no staleness, no archiving, no state. `--wat-sou-verander` says what is out
of date and writes nothing. Lessons nobody has started are skipped: there is
nothing to go stale, and writing one early would put a spec entry on disk for a
draft that does not exist.

## Checks that span lessons

The gate reads one lesson. The coverage checker reads one lesson against one spec
entry. Neither can see a fault that only exists *between* files, and the most
common one is a term that two lessons define differently — each lesson correct on
its own, the pair teaching two things.

```bash
python bin/woordelysdrif.py --vak "Natuurwetenskappe en Tegnologie" --graad 4
```

It reads every lesson draft in the tree and reports any glossary term defined more
than one way, with each wording's lessons, their status and their place in the
year. It exits 1 when it finds drift, so it can gate a commit. Run it before
claiming a subject is consistent — and quote the lesson count it prints, because
a sweep that read three files looks exactly like a sweep that found nothing.

When drift is real, one wording wins and the losers are rewritten **through the
writer**, at their source in the spec as well as in the draft. A third wording
makes it worse.

The other cross-lesson tool prepares a lesson for the outside language checker:

```bash
python bin/taalnasien.py --vak "Natuurwetenskappe en Tegnologie" --graad 4     --subonderwerp "Vaste stowwe" --les 2
```

It prints the instruction, then the words that checker may not change — the
hand-recorded rulings in `kaps/beskermde-woorde.json` filtered to those that
actually appear, plus every glossary entry this lesson shares with another, found
by reading the other lessons rather than by trusting a list — and then the lesson.
Each protected word reads like ordinary Afrikaans that could be improved, which is
exactly why the reason travels with it.

## The four human approval points

1. **The profiler's output.** Read the page counts and volumes before budgeting
   from them. Nothing checks that a section boundary was found correctly.
2. **The spec.** The planner writes to `spesifikasies/konsep/`. You read it and
   move it to `spesifikasies/goedgekeur/`. The runner refuses to write a lesson
   from an unapproved spec, and approval is a file move rather than a field
   because an agent cannot fake a move.
3. **Sign-off into `goedgekeur/`.** Only after the gate passes, both checkers
   return `GOEDGEKEUR`, and both reports validate. Then:

```bash
python bin/hardloop.py --vak "Sosiale Wetenskappe" --graad 4 --subonderwerp "Vervoer op water" --les 3 --keur-goed
```

   It shows you what will be copied where and asks you to type the lesson number.
   It refuses outright when stdin is not a terminal, so an agent running the same
   command cannot approve anything.

4. **Every escalation.** A `MENS_NODIG` verdict or a spent revision budget stops
   the lesson and records why in `konsepte/.../les-N.staat.json`. Deal with it,
   then re-run with `--hervat` to start a new cycle.

## The boundary with the HTML team

A lesson is approved **in place**. There is no second copy and no export folder,
which is the point: nothing downstream can go stale, because there is only ever
one file.

Point the HTML pipeline at the drafts tree, read-only, and take every file whose
`status` is `goedgekeur`:

```
konsepte/<graad>/<vak>/<subonderwerp>/les-<n>.json
```

The path states the CAPS location. `skema_weergawe` is the contract between the
two pipelines, so a bump gets told to them. Nothing there is ever edited by hand
downstream - a correction goes back through the pipeline and the same file is
rewritten.

`bin/leeskopie.py` also writes a human-readable PDF per approved lesson to
`lees/<graad>/<vak>/<jaarnommer>_<KABV-etiket>.pdf`, numbered by its place in the
year. Those are for reading and reviewing, not for the pipeline to consume, and
they are gitignored.

## Layout

```
skills/wolkskool-inhoudstandaard/   the standard: SKILL.md, scripts, references, assets
prompts/                           the four versioned agent prompts
.claude/agents/                     the four agents, each pointing at its prompt
bin/                               opstel.py (setup), hardloop.py (runner), logoorsig.py (logs),
                                   woordelysdrif.py and taalnasien.py (across lessons),
                                   vernuwe-uittreksels.py (after a spec edit)
profiele/                          one profiler config per subject-grade
kaps/                              CAPS sub-topic label files
kaps/dokumente/<fase>/             the CAPS documents themselves, one folder per
                                   phase: intersen-gr4-6, senior-gr7-9, fet-gr10-12.
                                   gitignored.
spesifikasies/konsep/              planner output
spesifikasies/goedgekeur/          specs a human has accepted
konsepte/                          drafts in flight, plus each one's gate result and reports
logs/                              gate_log.jsonl, hardloop_log.jsonl, verslae/
bronne/                            textbook input. gitignored.
```

`.claude/agents/*.md` are thin: each names its prompt file in `prompts/` and
requires the agent to read it, so the prompt exists once. That matters because the
version is recorded in every lesson's `herkoms`, and a second copy of a prompt is
a provenance record waiting to become false. The non-negotiables — the copyright
boundary, `handboek_gesien: false`, the fact checker not seeing the spec — are
repeated inline in each agent so that failing to read the prompt file cannot cause
the worst outcome.

All four agents run on Opus 5 (`model: opus`). To move a checker to Sonnet once it
is trusted, change that one line in its agent file.

## Later

Maths and Physical Sciences will need a variant: a maths-aware gate, worked-example
block types, and a solution verifier in place of the fact checker. Worksheets will
need their own schema. Neither is built. `skema_weergawe` is in every file the
pipeline writes, and nothing here assumes a block's content is prose beyond the
`studie` and `lys` register checks the standard defines.

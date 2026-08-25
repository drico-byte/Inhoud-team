---
name: n-regstelling-ontwrig-sy-bure
description: "The most reliable failure in this pipeline — a fix aimed at one finding activates an error somewhere else. Always ask \"what did this disturb\", not \"is it fixed\"."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8f79bbfb-d2d6-48c5-804a-7410b16958f5
  modified: 2026-08-24T19:19:58.299Z
---

The single most useful operational lesson of 2026-08-21. It happened **seven times in one day**, across
four different lessons and both checkers.

## The instances

- **Plastic ball → clay brick.** Fixing a contested origin introduced a new object needing its own origin
  check.
- **Shell definition.** Dropping the wrong phrase "een hele stuk" also dropped "om die ruimte binne",
  which was the leg that separated a shell from a solid. A brick then satisfied the definition.
- **Nest wording.** Removing "los dele" (which let a reader classify a nest off our own page) produced
  "van gras of modder", which contradicted the block's own next three sentences.
- **The shark.** Added to make a cartilage exception concrete; a shark's vertebrae are cartilage, so it
  contradicted "the backbone is made of small bones" three sentences later.
- **The fern's stem.** Correctly giving a fern a stem turned a previously safe sentence two blocks away
  ("the stem holds the leaves and flowers high above the ground") into a falsehood.
- **The zebra and the hole.** True in isolation; false by juxtaposition, because the only animal named
  before it was a zebra.
- **The habitat size sentences.** Added to fix a definition error, then flagged as unrequested content by
  the coverage checker.

## Why it happens, and why nobody is being careless

The writer is looking at one block. The checker is looking at one claim. **Nothing in the process asks
"and what does this now sit next to?"** So the fix is judged against the finding it answers, which it
always satisfies, and never against the text around it.

Three recurring shapes:
- **A named example is a new factual claim.** Every concrete thing added must be read against the whole
  lesson, not just the sentence it repairs.
- **A deletion can strand a reference.** "Hierdie geraamte" pointed at the wrong thing once the shark was
  removed; cutting a zebra sentence left "die grasveld" arriving with a definite article and no
  introduction.
- **A correction can activate a latent error.** Nothing was wrong with the stem sentence until the fern
  was given a stem.

## What to do

**Add one line to every revision brief and every re-check request: "then read the whole lesson for what
this fix disturbed — not whether the finding is gone."** That single question caught the shark, the stem,
the zebra and the meerkat before any of them shipped. It costs one sentence.

And when a checker prescribes a fix, remember it is reasoning from its own finding outward. Three times
on 2026-08-21 a checker was right that something was wrong and its suggested fix would have introduced a
new error — see [[wanneer-vra-en-wanneer-doen]] and Drico's own early instruction that a checker "needs
reading rather than obeying".

## And once ACROSS two lessons — 2026-08-24

Term 2's lessons 14 and 15 ended up making opposite claims about folds. Lesson 14,
after a fact-check correction, says the fold lines in a paper pillar are the
**stiffest** part and give way last. Lesson 15 said there is nowhere a fold where the
tube can buckle, which says a fold is the **weak** place.

Both are defensible alone. A fold running lengthwise along a column is a stiffener; a
crease across paper is a weak hinge. A nine-year-old cannot hold that distinction and
should not have to.

**Neither checker could see it. Each reads one lesson.** The coverage checker can open
a sibling when told to — it opened lesson 14 to confirm the word *stut* was absent —
but nothing checks two finished lessons against each other as a matter of course.

Resolved by putting both lessons on the **same** mechanism: flat faces bulge outward
and stop carrying, a round wall has none. Sourced, and the two lessons now reinforce
each other.

**How to apply.** When a fact check corrects a *mechanism* rather than a fact, ask
which sibling lessons teach the same mechanism, and name them in the revision brief.
The risk is highest inside one sub-topic, where lessons deliberately build on each
other. Related: [[meting-dek-minder-as-die-lesse]].

## Give sibling lessons by PATH, not by name — a writer cannot browse

2026-08-25, Term 2 lesson 16. The brief told the writer to build on lesson 15 and on
Term 1's lesson 8, naming both. It could find neither: the writer agent has Read and
Write but no shell, so it cannot list a directory to find a file it was not handed. It
searched, failed, said so, and wrote the lesson from the brief alone — which is the
right behaviour, and the only reason the gap was visible.

**So whenever a brief asks for continuity with another lesson, paste the path.** The
same applies to a checker asked to cross-check a sibling.

Grade 4 NWT paths, for reference:
`konsepte/gr4/natuurwetenskappe-en-tegnologie/<subonderwerp-slug>/les-N.json`

And when the writer could not do it, the coverage checker can — it reads whatever paths
it is given. Hand the cross-check downstream rather than losing it.

**Give the report path too.** Twice on 2026-08-25 a coverage checker had no output path
in its brief and chose one — `.../nasien/les-1-dekking.json` once and
`.../verslae/les-1-dekking.json` once. The runner reads only
`<lesson-dir>/les-N.dekking.json`, so both had to be moved by hand before the verdict
could be read. Every checker brief needs the output path spelled out, the same as the
inputs.


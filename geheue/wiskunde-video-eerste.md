---
name: wiskunde-video-eerste
description: "Maths inverts the pipeline — the videos already exist, so text fits the video. Two pieces of machinery are still missing before number topics."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f79bbfb-d2d6-48c5-804a-7410b16958f5
  modified: 2026-08-24T19:20:22.755Z
---

State of maths as at 2026-08-21. One lesson done: Gr 4 "Prismas en piramides" (Eienskappe van 3-D
voorwerpe), both checks approved.

## The order is reversed, and it changes the rules

Gr 4-6 maths videos were **remade in 2026 before any text existed**, so the text must fit the video
rather than the video honouring the text. This inverts [[teks-loop-parallel-met-n-video]] for this
subject only.

The creator deliberately did not want the text re-explaining her video — the video is the explanation and
her text only guided learners. **We know a lesson's scope from her "Wat gaan jy leer?" list**,
cross-referenced against CAPS. Her notes are saved under `skepper/<graad>-<vak>/<subonderwerp>/les-N.md`;
save every new one there the moment it arrives, because it exists nowhere else.

**Her outcomes are unusually good input** — each is a capability, not a topic label, so they convert
almost directly into `kern` items. Two of her five for the 3-D lesson were *not* CAPS content (what 3D
stands for; length/breadth/height) — they are her framing. The text must carry them, or a learner meets
something in the video the text silently drops, but they go in as `aanvulling`.

**Her 3-D content is split across four or five narrow videos**, so one lesson's outcomes are a subset of
the CAPS unit. CAPS items missing from one lesson belong to siblings and are **not** gaps.

## Two things still to build before number topics

1. **A block type for a worked example.** A calculation with steps is neither prose nor a list, and its
   "sentences" are steps, so the register band cannot apply unchanged.
2. **An arithmetic checker.** This is the good news: a script can extract every calculation and verify it
   by computing — deterministic, free, and incapable of being confidently wrong. Maths could be *cheaper
   and more reliable* to check than science.

**And one unresolved design question:** questions were removed from lessons, but practice is what a maths
lesson is. Worked examples show a method; only doing it teaches it. That needs Drico before number topics.

The 3-D lesson needed neither — no arithmetic, no method to clash with the video, no practice. It was the
easiest possible first maths lesson and should not be read as proof the subject is solved.

## Budget basis

**Not measured textbook volume.** A maths textbook teaches through diagrams and exercises; its word count
measures the prose *between* them. The Gr 4 book runs 92 words a page against the science book's 185. The
budget comes from requirement count instead — `begroting_basis: "vereistes"`, which `spec_check.py` now
supports. **Drico has been told this is a stated assumption for one test lesson and is NOT settled for
maths generally.**

## The error profile is different

11 contradictions in 258 words, nearly all one fault: **a definition true of the thing described and also
true of something else.** "Two bases of the same shape and size" is exactly a cylinder. "A 3D object is
one you can pick up" excludes the pyramids of Egypt. In prose a sentence is wrong when it misdescribes
what is in front of it; in definitions it is wrong when it misdescribes something you never mentioned,
because the learner uses the definition to sort objects the lesson never named.
Related: [[n-regstelling-ontwrig-sy-bure]], [[betwiste-klassifikasie-ruil-die-voorbeeld]]

---
name: n-module-buite-sy-boom-lees-niks
description: "A before/after harness that copies the old module somewhere else made it read NO data, so 340 of 387 comparisons differed and the refactor looked broken. Compare in place."
metadata:
  node_type: memory
  type: feedback
---

**8 October 2026.** I lifted a block out of one function so a second consumer could read
the same answer, then built the right test: run the old version and the new version over
every lesson in the repository and diff the output. It reported **340 of 387 differed**,
and every difference was the new version producing MORE protected words than the old.

For several minutes I believed I had broken it. I checked the diff against the commit
(a pure move), printed the function source from both loaded modules (identical), and
tested call order (no effect). Identical code, identical input, different answers.

**The harness was the fault.** I had written the old version to the scratchpad and loaded
it from there. The module resolves its data directory from its own `__file__`, so the
relocated copy looked for the word lists and the shared wordings *beside itself* in the
scratchpad, found nothing, and returned an empty list every time. The new version, loaded
from `bin/`, found everything. **The old version was not producing different answers; it
was producing no answers.**

Loaded from inside the tree under a temporary name, the two were byte-identical on all
387 lessons.

**How to apply.**

* **Compare in place.** To diff an old version against a new one, write the old copy
  *into the same directory* under a temporary name and delete it afterwards. Anything
  that resolves paths from `__file__`, `sys.path[0]` or the working directory changes
  meaning when you move it, and almost everything in this repository does.
* **An all-one-way diff is a harness smell.** When every single difference points the
  same direction — one side always richer, always emptier, always silent — suspect the
  rig before the change. A real logic difference is usually lumpy.
* **A zero is the loudest signal available and I keep reading past it.** Same shape as
  [[n-wag-wat-sy-eie-reels-naskryf]], where a guard read zero files forever, and as
  [[my-soektogte-mis-en-dan-glo-ek-hulle]]. The fix is the same: before trusting a
  comparison, prove each side can see something at all.

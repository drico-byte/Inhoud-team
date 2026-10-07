---
name: moenie-git-add-alles-gebruik-nie
description: "git add -A in this repo sweeps up the other parallel sessions' in-progress files; stage the pipeline paths deliberately instead."
metadata:
  type: feedback
---

**5 October 2026.** I ran `git add -A` to commit a round of Grade 7 LO work and swept
in a 402-line Grade 8 maths HTML test page another session had left in `interaktief/`.
It went to GitHub under my commit message. The other session had to write a memory note
and a removal commit, and because three machines share this repository it could not be
erased from the history — a force push across three PCs is worse than the stray file.

**Why:** three sessions work in this repository at the same time
([[drie-rekenaars-werk-parallel]]). `-A` does not distinguish my work from theirs, and
an untracked file halfway through someone else's turn looks exactly like a file I
created. The other session's own lesson from this is
[[toetsl-ers-buite-die-repo]] — keep one-off files out of the repo folder. Mine is the
mirror of it.

**How to apply:** stage deliberately. For a content round that means the paths the
pipeline touches — `spesifikasies/goedgekeur/`, `konsepte/`, `kaps/`, `logs/`,
`Voltooide lesse/`, `lees/`, and `bin/` or `skills/` when I actually changed a script —
rather than `-A`. If `git status` shows a path I cannot account for, leave it unstaged
and say so in chat instead of committing it; an addition I did not make is not mine to
publish to the shared remote.

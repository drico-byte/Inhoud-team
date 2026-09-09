---
name: n-spek-so-lywig-dat-dit-nie-geskryf-kan-word-nie
description: "Spec notes grew until a planner could not write the file — 27 minutes lost. A note earns its place by changing what a writer does."
metadata:
  type: feedback
---

7 September 2026. The Gr 4 SW Kwartaal 1 planner ran 27 minutes and produced nothing. Its
last words before I stopped it: *"The heredoc exceeds the shell's argument limit, so I'll
use the file writer."* It had been looping on trying to write the spec through shell
heredocs.

**The size was the cause, and the size was my fault.** The transport spec for the same
subject reached **49KB**, most of it prose: a `titel_nota` explaining a four-word title, a
`beskermde_woorde_nota` running to a paragraph, correction notes quoting their own history.
I had asked for the reasoning to be written down every time, and the planner obliged until
the artefact could not be produced.

**How to apply.**

* **Tell a planner to write the file with the Write tool, not a shell heredoc.** That alone
  removes the failure mode.
* **Ask for lean notes, and say what lean means: a note earns its place by changing what a
  writer does.** Five short lessons do not need an essay. The reasoning that matters
  belongs in the repository's documentation and in these memory notes, where it is read
  once, rather than copied into every spec entry where it is read never.
* Watch for it in reports too: an agent asked to explain itself thoroughly will spend its
  run explaining rather than doing.

**What NOT to conclude.** The notes that carry a *correction* still earn their place — the
ones recording why `verder` and `stap` were struck are the reason no revision reinstated
them. It is the decorative ones that cost the run.

Related: [[n-verslag-bestaan-nie-omdat-die-agent-so-se]],
[[voor-jy-stop-se-wat-loop]], [[moenie-in-die-spek-skryf-wat-jy-nie-nagegaan-het-nie]]

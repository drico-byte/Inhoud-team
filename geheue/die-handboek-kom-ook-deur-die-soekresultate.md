---
name: die-handboek-kom-ook-deur-die-soekresultate
description: The fact checker is the only agent with web access, and Grade 4 textbooks are freely online and rank for exactly its queries. Nothing said so; it worked the rule out itself and declined. Now written into its prompt.
metadata:
  type: project
---

Checking lesson 23's comparison, the fact checker hit a Siyavula Grade 4 PDF in
search and **did not open it**, saying so in its report: its findings go back to
the writer, so reading it would put textbook material into the chain that
produces the lesson.

Nothing in `prompts/feitenasiener-v1.1.md` mentioned textbooks at all. The rule
lives in CLAUDE.md and the README, framed around `bronne/` — the copy of the book
sitting on this disk. The checker generalised correctly on its own, but the whole
point of the copyright discipline is that it cannot depend on an agent working it
out each time.

**Why the web channel is the same exposure as the folder.** Facts are not
copyrightable; selection, arrangement and expression are, which makes matching a
publisher's *lesson structure* the real risk. Independent creation is a property
of the process, provable only by showing the chain never had access — and the
chain includes the fact checker, because its report returns to the writer. One
page read to settle one claim ends the proof, and nothing afterwards restores it.

**What changed:** `prompts/feitenasiener-v1.2.md` states it, and says what to do
instead — if a textbook is the only thing search returns, the claim is `onseker`,
and say that a textbook was the only source found. That is usually a real finding
in itself: it means the claim is a teaching convention rather than a fact. The
rule covers scans, worked-solution sites and teacher guides too; the test is not
the file format but whether what you are reading carries a publisher's choice of
what to teach and in what order.

**How to apply:** when a rule is enforced in one place, ask which agents could
reach the same thing by a channel nobody wrote down. Compare
[[n-verslag-bestaan-nie-omdat-die-agent-so-se]]: an agent behaving correctly is
not evidence that the instruction exists.

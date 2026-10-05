---
name: n-verslag-in-die-logboom-kan-verouderd-wees
description: "A report recovered from the log tree describes the draft as it was when the check ran; the draft may have moved since, so check the draft's own revision record before briefing anyone from an archived report."
metadata:
  type: feedback
---

9 September 2026. The log overview surfaced an unresolved escalation on the ships lesson
dated 7 September. I read both archived reports, ruled on the two open questions, amended
four requirements and briefed a writer on nine items.

**Seven of the nine had already been fixed** — later on 7 September, after those reports
were written. The draft on disk carried a revision note saying so, and the text matched
it: the dhow already named no sail shape, the raft's "over short distances" was already
gone, the canoe was already defined by what it is, the junk had already lost "big" in
both places.

The writer caught it, checked each of the nine against the actual text rather than against
my brief, and changed only what was genuinely still wrong. That is the right instinct and
it is the same rule as [[spesifikasies-word-nooit-nagegaan]] pointed the other way: **read
the text, not the description of it** — including when the description is mine.

**Why the trap is easy.** An archived report is a *snapshot*: it describes the draft as it
stood when the checker read it. Nothing in the report says so, and the log overview lists
the escalation as current because the escalation was never *closed* — not because the
findings are still live. A lesson can be revised without its escalation being marked
resolved, and then the report and the state disagree while both look authoritative.

**How to apply.** Before acting on any report you recovered from the log tree:

1. **Compare timestamps** — the report file's, and the draft's own revision record.
2. **Spot-check two or three findings against the draft text** before writing a brief. If
   they are already fixed, the report is a history, not a task list.
3. **If you brief anyway, say which findings you verified are still live**, so the writer
   knows the brief may be stale and checks rather than complies. Mine did not know, and
   only caught it because it read the text on its own initiative.

The same run also cost me a smaller version of the printing failure: `kern[0]` was
ordering the paddle-and-muscle frame the correction removes, it was visible in my own
printed output, and I amended four other fields and not that one. The writer found it.
See [[n-ruil-wat-nie-pas-nie-moet-hard-faal]] — the print is only worth its cost if you
act on the whole of it.

---

**1 October 2026: a report NEWER than its draft can still be stale — against the SPEC.**

Three Grade 7 LO lessons sat in the repair box with coverage findings dated after their
drafts, so by every freshness test they were current work. I started repairing them and
found the findings already fixed: the stale clause the report quoted was not in the spec
any more, and the six pointers it said ranked from the back had been renamed the same day.

The reason is structural. A coverage finding of "the spec is at fault" is repaired in the
spec and **never touches the draft**, so the draft's timestamp does not move and nothing
marks the report as answered. The sorting script compares report time against DRAFT time
only, which is right for a draft fault and blind to a spec fault.

**How to apply:** before briefing anything on a `spesifikasie_probleem` report, grep the
approved spec for the exact wording the report quoted. If it is gone, the finding is
answered and the lesson needs a fresh pair of checks, not a repair round. Related:
[[tel-die-verslae-voor-jy-se-dit-is-nagegaan]] — same family: the state a script
reports is not the state of the work.

---

**5 October 2026: twelve of sixteen. The scale changes the default.**

Grade 7 LO's repair box held fourteen lessons with sixteen live findings. I checked each
one's *named field* against the approved spec before touching anything — the step the
1 October entry above prescribes. **Twelve were already answered.** Four still stood.

Nine of the fourteen also had coverage reporting *nothing wrong with the draft*: the
finding was "the spec is at fault" and the text was correct. So the repair box was not a
writer's work list at all — it was a list of lessons needing a fresh pair of checks.

**How to apply.** When a repair box has more than a handful of entries, verify before
planning. One script that greps each finding's own wording out of the approved spec costs
minutes and told me which four of sixteen were real. Without it I would have briefed
twelve writers against faults that no longer existed, and each one would have "fixed"
something by changing correct text.

Two things that stayed true under that sweep and should not be swept for again:

- **Do not fire on the normal correction shape.** A field that diagnoses an old form in
  the present tense, with the live order immediately after it, is correct as written.
  A sweep that flags those gets ignored — see
  [[n-veeg-vir-velde-wat-nog-bestel]] and [[n-generiese-teruggetrek-speurder-kan-nie-werk-nie]].
- **Pull the needle from the file, never from the report's quotation of it.** One of the
  four failed to match because the spec carried a typo inside the sentence I was replacing.

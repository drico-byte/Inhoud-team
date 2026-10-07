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

**30 September 2026: I dispatched the same fact check twice, forty minutes apart, and the
second one's report was against a draft that no longer existed.**

Lesson 6 of Gr 6 SW Democracy got two round-three fact checks. I sent the first, took its
findings, ported them, sent a repair — and then sent a *second* round-three check whose
brief I had written earlier and not cancelled. It ran for thirty-one minutes and 215K
tokens against the pre-repair draft.

**What made it worth reading anyway, and the discipline that made it safe.** Two
independent checks of one draft do not find the same things, so the stale report carried
seven findings the first had missed — including that a closed six-item list under the
heading "what section 28 gives every child" claims the whole of section 28, which has nine
paragraphs, and that the omitted one that matters most to an eleven-year-old is that a
child's best interests are paramount.

But I could only use it because I diffed every finding against the current draft before
briefing anything. Three of its findings were already repaired; one had been cut entirely.
Briefing the report as it stood would have sent a writer to fix text that was gone — the
failure this note already records, arriving by a new route.

**How to apply.**

* **Before sending an agent, check what is already running on that lesson.** A brief
  written twenty minutes ago may have been overtaken by a repair you dispatched since.
  The cost is not only tokens: a second report on a dead draft looks exactly like a second
  report on the live one.
* **A stale report is still evidence, and two checks of one draft are worth more than
  one** — but every finding gets diffed against the current file before it reaches a
  writer, one at a time, by searching the draft for the claim.
* When two checkers disagree about a fact, look for the narrower claim all of them
  accept. Here one contested "the demands were submitted to the negotiations" with dates —
  CODESA II collapsed in May 1992 and the charter was adopted on 1 June — while two had
  confirmed it. "The children wanted their demands to reach the negotiations" is carried by
  every source and loses nothing.

## No report file does NOT mean never checked

**1 October 2026.** I built a status table of a sub-topic from which report files
existed, concluded two lessons had "never been checked by anything", and briefed
an agent that way. It corrected me: the draft's own working note recorded a
coverage check **and** a fact check from two days earlier plus three repair
rounds, naming findings from both, and the requirement fields repeatedly recorded
corrections made "after a coverage check".

**Why:** the runner archives reports to the log tree when a draft moves, under
`-verouderd` names. So a checked lesson whose draft was later revised has **no
report beside it** and a full history in `logs/verslae/<lesson>/`.

**How to apply:** before calling a lesson unchecked, look in the log tree and
read the draft's provenance note. Both hold prior findings worth inheriting
rather than re-deriving — and telling a checker "nothing has ever read this" when
something has invites it to re-report what was already settled.
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

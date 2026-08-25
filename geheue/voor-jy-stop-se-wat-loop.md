---
name: voor-jy-stop-se-wat-loop
description: "When Drico asks to pause or stop the agents, first report what is running and how close each is to finishing. Do not kill a long-running fact check without asking."
metadata:
  node_type: memory
  type: feedback
---

Drico, 2026-08-25, after I killed a fact check sixteen minutes in, at the moment it
said "I have enough verification. Writing the report":

"If I ask to stop again, just give me a quick report on where the current agents are
and how far from done they are so that we can prevent the loss that we just did."

## What to do

A request to pause is **not** an instruction to kill immediately. Run `ListAgents`
first and report, in one short block: what is running, what each is working on, and
how long it has been going. Then ask, or stop the ones that are clearly early and
hold the ones that are clearly close.

The judgement he needs is "how far from done", so give it in those terms rather than
as raw ages.

## Typical step durations, for estimating

- **Fact check — 10 to 20 minutes.** The long step; it searches sources. Anything past
  about twelve minutes is probably near the end. **Do not kill one of these without
  asking.**
- **Coverage check — 3 to 8 minutes.**
- **Writer, drafting or revising — 3 to 10 minutes.**
- **Gate — instant.** It is a script, not an agent.

So the cheap moment to stop is right after a gate or a coverage check. The expensive
moment is deep into a fact check.

## Why it matters

A killed agent loses everything it has not written. The report is written once at the
end, so an agent stopped just before that point has done all the work and produced
none of it. The lesson itself is unaffected — a rerun starts from the same place —
but the search time is spent again.

We considered making checkers write findings incrementally and decided against it:
the verdict has to be formed over all the findings, several findings tonight were
withdrawn on further reading, and the best ones only existed after the whole lesson
was in view. See [[spesifikasies-word-nooit-nagegaan]] for the related habit of
sweeping rather than patching.

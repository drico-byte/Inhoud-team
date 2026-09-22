---
name: die-feitenasiener-lees-n-verouderde-konsep
description: "The fact checker's stripped copy of a draft is only rewritten by a runner call, so a checker dispatched without one reports faults that were fixed hours ago."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-09-11T08:21:20.709Z
---

11 September 2026. A fact check on Grade 5 `gestoorde-energie-in-brandstof`
lesson 2 returned four contradicted claims. **Two of them did not exist.** The
checker's copy had been written at 15:03 on 10 September; the lesson changed
twice later that day, and the check ran the next morning against the
eighteen-hour-old copy. The two glossary entries it quoted had been replaced with
the agreed wordings the evening before.

**Why it is easy to hit:** `feite-kopie/<lesson>.json` is written only by a
runner call. Dispatching a checker directly — which is the right move for a
lesson whose reports the runner would otherwise archive — hands it whatever copy
is on disk. The directory is gitignored, so nothing shows the copy is old.

**Why it is worse than a stale spec extract.** An agent reading an old spec
reports that a fix is missing; that is visibly wrong and gets checked. An agent
reading an old draft reports faults that no longer exist, and those read exactly
like real findings — they come with sources.

**How to apply:** `bin/vernuwe-uittreksels.py` now refreshes the fact copies as
well as the spec extracts, so the existing habit — run it before briefing any
agent — covers both. It reports how many copies it rewrote. Nine of thirty were
stale when this was built; a screen of report against draft times showed none of
those nine had actually fed a check, so this is the only known instance.

**The writer caught it, not a checker.** It read both entries against the agreed
list and refused to write a third wording. Related:
[[n-verslag-in-die-logboom-kan-verouderd-wees]],
[[die-uittreksel-het-sy-eie-kruisverwysings-verloor]],
[[die-ooreengekome-bewoording-kan-self-verkeerd-wees]].

**22 September 2026: eighteen of thirty-one copies in one subject were behind.** One
whole fact check had to be thrown away — both its findings were about sentences
corrected hours earlier, and the writer sent to "fix" them correctly refused and
changed no text. A refresh script exists (`bin/feitekopie.py --alles`) and CLAUDE.md
says to run it before briefing any fact checker outside the runner; I briefed eleven
fact checkers by hand that day and ran it once, near the end. **Run it immediately
before each hand-briefed fact check, not once per session** — every writer round that
lands between the refresh and the brief puts another copy behind. And if a check is
already running when the refresh reports its copy was stale, message that agent to
re-read rather than letting the report land.

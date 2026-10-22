---
name: caps-oudit-gr4-6
description: "Drico wants every delivered Gr 4-6 lesson audited item by item against CAPS; all 13 subject-grades audited 21-22 Oct 2026, report URLs, method, what is still owed"
metadata:
  node_type: memory
  type: project
  originSessionId: fccc93f1-34d2-4da5-bb23-6910f798204b
  modified: 2026-10-21T11:16:19.584Z
---

Drico (20-21 Oct 2026): content must be "101% CAPS aligned"; audit ALL delivered content, no shortcuts, both blind passes for every subject. Reports in HTML. **Changes are made only after every subject is audited** (his order). Triggered by the Gr 6 exam-summary team's findings (malaria was NOT missing: Gr 5 PSW lesson 8).

**All 13 audited by 22 Oct 2026.** Reports (claude.ai/artifact/…), HTML copies, the summary, the handover brief (`CAPS-oudit - OORHANDIGING.md`) and the working files are all in `Dump/CAPS-oudit/`:
- Gr 6: PSW Y85FxKtrLvwzo9y18bLtaq · Geo BXxi4giPw5WmhUKEEfuQeF · Hist 68FhfsLjRqDiLgaSLhDefh · Science TM7gYUni6EqYnd7JyghpWf · Arts 3sezjMcguoGAqojQHKRmvo (v2 22 Oct: whole-year items had been left out by a builder bug)
- Gr 5: PSW 18MW5s1FRC5kRffFgQa2WV · Science 2FgWPX68fsvif2fdrT2fja · Arts JZZHUCp9vgLdRuz78Sa17D
- Gr 4: PSW VQe8dxChq16DXEr4dTPa5r · Hist 9TWysRaGqNtudoFoyYPU6P · Geo ViU7Be7fUgjMXKcMboHGV7 · Science QKnTwpBM3u8ab1BCxygR3P · Arts WhnffGAbJrHVQooMwZRDnu

**Summary across all 13:** https://claude.ai/artifact/NM4jPg15Xpj5JaZxEgbdzY (2840 content items: 2281 full, 373 partly, 186 not; 13 decisions listed; blind passes agreed 95%).

**Working files:** `Dump/CAPS-oudit/CAPS-oudit-werklêer/` (briefs OPDRAG-*.md; bou_rapport.py builds a report from <folder>/rapport.json; gaplys.py lists final gaps; one folder per subject with kanoniek, items, audit-*/audit2-* passes, kapsreel, rapport.json). Run python `-I -X utf8`. Max 20 agents at once.

**Method:** two blind atomisers -> reconciled checklist; two blind passes per item on the delivered 2_PDF text only; disagreements take the stricter verdict; CAPS-line check per lesson; THEN specs and memory read to mark deliberate decisions. Formal assessment rules (marks, weights) are deliberately not audited. Creative Arts: practical topics shown as "outside our lessons" by regex; key terms stay in scope.

**Big decisions waiting for Drico (from the reports):**
- Gr 4 History: three of his own rulings now conflict with "101%": local area ignored, 7-hour project out of scope, exhaust-gas case study dropped. Agreed definition of 'geskiedenis' narrower than CAPS.
- Gr 4 Science: lesson 2 makes "dead" a third group beside non-living; CAPS puts dead under non-living. The ORDER is in the approved spec, so fix the spec first.
- Creative Arts Gr 4-6: carry each term's key terms or not (20-40 per grade untaught); instrument "family" contradicts CAPS and itself in Gr 4.
- Gr 4 Geography: map blocks for lessons 14/19 + water term (written before the 7 Oct map ruling); data/graphs/tables absent from all of Gr 4 SW.

**Owed after the audits:** delivery-integrity check (Gr 4 NW 2_PDF copies are an OLD version with draft stamps; 2_PDF glossaries differ from master in places); the cross-subject summary; then changes, each through plan, writer and full checks; the process fix (item-level CAPS map before spec approval); the Claude-vs-ChatGPT Afrikaans comparison (Gr 4 PSW lessons 1-6; needs ChatGPT's prompt from Drico).

**Why:** our pipeline checks lessons against the spec, never the spec against CAPS, so a planner's omission passes every check.
**How to apply:** fix each finding at source in the spec; see [[kruistoets-die-termynplan-teen-kaps]], [[n-strepie-afgemerk-is-nie-sy-items-getel-nie]], [[verslae-in-html]].

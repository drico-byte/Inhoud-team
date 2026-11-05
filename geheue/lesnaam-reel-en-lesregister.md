---
name: lesnaam-reel-en-lesregister
description: "Drico's file naming rule for all teams (5 Nov 2026) — we write the lesson register; IDs like G4_PSW_07, short labels, never renumber"
metadata:
  node_type: memory
  type: project
  originSessionId: 03443761-3135-4339-9081-4e7807a3484d
  modified: 2026-11-05T12:52:29.847Z
---

From 5 November 2026 every delivered file is named `<ID> - <label>` (e.g. `G5_PSW_26 - TB en masels.pdf`) under Drico's rule in SharePoint `0000NUWE LESSE/LESNAAM-REEL.md` (on this PC the folder syncs as "Innovasie - 0000HTML wolkskool lesse"). Inhoud-team writes the register; the other teams (HTML, Script, Opsommings, Video) copy IDs from it.

- Register source is in the repo, `kaps/lesregister/`, with an extra `bron` column; publish with `bin/lesregister.py --publiseer`.
- Order is CAPS term order, one running number per subject. PSW = Ontwikkeling van self, then Sosiale verantwoordelikheid, then Gesondheid (CAPS confirmed). Kuns = per term, uitvoerende then visuele. The old alphabetical Gr 5-6 PSW numbering and the Script team's Kuns/Gr 5 PSW numbers were wrong.
- The user asked for labels that are "short and sweet": 2-4 words, about 25 characters max, from the lesson's own title.
- The first rename on 5 Nov 2026 covered 677 SharePoint files, V2, Voltooide lesse and lees/. Lesson content fingerprints stayed the same.

**Why:** one ID per lesson across PDF, HTML, script, recording and video; the progress dashboard reads it.
**How to apply:** a new subject-year gets register rows when its year layout is agreed, before drafting; never renumber (a later lesson becomes `07b`). The SharePoint 2_PDF copies are the pre-language-pass issues — see [[voltooide-lesse-uitvoer]].

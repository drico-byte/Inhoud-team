---
name: inhoud-biblioteek
description: "Content library \"Wolkskool Nuwe Inhoud V3\" (5 Nov 2026) — our Inhoud/ folders mirror V2 (json+pdf+manifest per subject); only Gr 4-6 are finished"
metadata:
  node_type: memory
  type: project
  originSessionId: 03443761-3135-4339-9081-4e7807a3484d
  modified: 2026-11-05T20:15:23.994Z
---

Drico's delivery rule (AFLEWERING-REEL.md, beside LESNAAM-REEL.md in 0000NUWE LESSE): finished work lives in the SharePoint library "Wolkskool Nuwe Inhoud V3". Our product is `Graad N/<code>/Inhoud/`, which holds each lesson's .json and .pdf plus the subject's manifest.json. It is a byte-for-byte mirror of V2 inhoud. Sign-off rebuilds V2 and mirrors the subject (bin/biblioteek.py). Filled on 5 Nov 2026: 338 lessons, 689 files.

- The user said only Grades 4-6 are completely redone (the post-audit pass), apart from Gr 5 SW, which is not in this repo. Gr 7 Lewensoriëntering was never part of the audit and will be redone in future. It has no register and no subject code, and it stays out of the library.
- Step 1 of the switch is to deliver to the library AND to 0000NUWE LESSE. In step 2 the rules and registers move to `_Gedeel/` and teams read their input from the library. Then lesregister.py --publiseer and the docs need repointing.

**Why:** one place for finished work; the HTML team builds from the .json and the manifest.
**How to apply:** never put review pages, drafts or outbox files in the library. Touch only our files in Inhoud/. See [[lesnaam-reel-en-lesregister]].

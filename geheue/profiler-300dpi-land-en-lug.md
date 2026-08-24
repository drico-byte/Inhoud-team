---
name: profiler-300dpi-land-en-lug
description: "The Gr4 SW Kwartaal 3 land and air sub-topics still need a real profiler run, and it must be at --dpi 300."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f79bbfb-d2d6-48c5-804a-7410b16958f5
  modified: 2026-08-18T17:57:04.285Z
---

As of 2026-08-18, `profiele/` in Inhoud-team is deliberately unseeded. The only
profiler output that exists is the supplied 150 dpi example asset
(`skills/wolkskool-inhoudstandaard/assets/gr4-sw-kw3-profiel.json`), which records
994 words for "Vervoer op water". The example spec is built on the 300 dpi figure
of 1028.

Drico's instruction: the first real profiler run — for the **land** and **air**
sub-topics of CAPS Gr 4 SW Kwartaal 3 — uses `--dpi 300`, so the volumes are
comparable with 1028 rather than with the 150 dpi undercount.

**Why:** 150 dpi undercounts by roughly 3%. Mixing the two resolutions inside one
topic would make sub-topic budgets silently inconsistent with each other.

**How to apply:** pass `--dpi 300` on that run, and do not treat the 150 dpi asset
as the live config. Note "Vervoer in die lug" also needs an `--eindmerker`, since
it is the last section and is recorded as `onbegrens` in the example asset.
Related: [[inhoud-team-runner-is-a-step-driver]]

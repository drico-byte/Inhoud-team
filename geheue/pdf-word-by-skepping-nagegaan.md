---
name: pdf-word-by-skepping-nagegaan
description: "Drico: text must never be printed over other text in a PDF; every readable PDF is now checked on creation for overlapping words and for the raw-code 'unknown block' box."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-09-18T17:24:38.870Z
---

18 September 2026, Drico: "make sure that text doesnt get printed over other text
when you make corrections in a pdf."

A scan of all 184 PDFs found no overlapping words. It did find 14 Grade 4 Life
Skills copies beside their lessons that showed a raw-code "Onbekende bloktipe" box
where the story should be. They had been built before the renderer knew the
`leesstuk` block. The copies in `lees/` were fine, which is why nobody noticed.

**Why:** a broken readable copy looks authoritative, and nothing opened it.

**How to apply:** the check now runs every time a PDF is made (`kontroleer_pdf` in
the readable-copy tool). A bad file is renamed `*.STUKKEND.pdf` and the run stops
loudly. After any renderer change, rebuild every PDF rather than only the ones you
touched. Look at a page image yourself before calling a batch done.

---
name: voltooide-lesse-uitvoer
description: Finished lesson PDFs are delivered to 'Voltooide lesse/Graad N/Vak/Subonderwerp/' - automatic at sign-off since 22 Sep 2026
metadata:
  type: feedback
---

Lampies asked on 22 September 2026 that every finished lesson be output to `Voltooide lesse/` in the project, sorted into sensible folders, PDFs only.

**Why:** that is the folder people browse. The PDFs beside the lessons are the pipeline's working copies.

**How to apply:** it is automatic. Sign-off now copies the PDF there as `Graad N/<Vak>/<Subonderwerp>/Les NN - <titel>.pdf`, and a lesson that goes back to draft loses its delivered copy. Backfill with the Voltooide-lesse script (`--vak ... --graad ...` or `--alles`). Grade 5 and 6 Life Skills (64 PDFs) were filed there on 22 Sep. Other subjects have not been backfilled; ask before doing that. PDFs are gitignored, so this folder never enters git.

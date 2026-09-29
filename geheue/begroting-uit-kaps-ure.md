---
name: begroting-uit-kaps-ure
description: "Drico, 29 Sep 2026: the new budgeting method — CAPS hours x the subject's own rate gives a CLUSTER envelope, the planner distributes inside it by content, and the ceiling is planned + 12%. No absolute ceiling, no textbook needed."
metadata:
  node_type: memory
  type: project
  originSessionId: 1551181f-ed8a-4e8a-b7bc-c8c8d51c9cda
  modified: 2026-09-29T13:47:12.858Z
---

**Drico, 29 September 2026, deciding this for everything from now on.** Grade 6 Sosiale
Wetenskappe is the first subject built this way.

**The method, in order:**

1. **CAPS states the hours** for every content cluster — it is printed in the document
   (Mapungubwe 6 uur, the national government 7 uur, the rainforest 3 uur). Revision and
   assessment hours get no lesson.
2. **The subject's own rate** turns hours into words. For Sosiale Wetenskappe it is
   **250 words per CAPS hour**, taken from Grade 4 SW's own delivered lessons (~270/hour).
   The rate is PER SUBJECT and is not transferable — Natuurwetenskappe runs near 125/hour
   because it has far more hours per lesson.
3. **Hours x rate = the CLUSTER envelope**, not the lesson budget. Mapungubwe's 6 hours buys
   1 500 words across its six lessons.
4. **The planner distributes inside the cluster** by what each lesson actually has to teach,
   and justifies each share in one line. Distribution happens INSIDE a cluster, never across
   two — each CAPS cluster owns its words and cannot lend them.
5. **The ceiling is planned + 12%**, per lesson. **There is no absolute ceiling any more** —
   an absolute one contradicts the whole idea that each lesson's length is its own. This
   replaces the old flat bands (450-550 etc.) for new work.

**Why it is trusted:** Drico hand-counted ten lessons of a Grade 6 SW textbook and gave me the
numbers only. His total was 3 042 words against my predicted 3 000 — **1.4% apart**. His book's
lesson division also matched mine seam for seam except that it merged my first two. A textbook
is not a benchmark — publishers guess from hours too — but an independent guess landing that
close means ours is calibrated.

**No textbook is needed for budgeting.** CAPS supplies the hours, our own delivered lessons
supply the rate. That takes a book out of the loop entirely, which is one less place the
copyright boundary has to hold.

**The standing arrangement:** I estimate from the hours, Drico hand-counts a textbook for the
same lessons, we compare, and then we proceed. He does the counting so nothing but numbers
ever crosses the boundary.

**Open, and I flagged it:** 12% of a 120-word lesson is fourteen words of slack, and small
budgets overshoot by about a tenth. I suggested "12% or 20 words, whichever is larger"; Drico
said 12% max and did not take up the floor, so 12% stands and short lessons will need a second
writer pass more often.

**Built into the tooling on 29 September 2026.** A spec declares `begroting_basis: "kaps-ure"`
plus `woorde_per_uur`; every lesson carries `kaps_kluster` and `kluster_ure`, and a cluster whose
hours are mostly practical states `kluster_uitsondering`. The spec checker then enforces that each
cluster's budgets sum to its hours x the rate — **that is the check that catches words shading
across a cluster boundary, which nothing else can see, because the topic total stays correct.**
The runner passes `--kaps-ure` to the gate when the spec declares it, so nothing already approved
changes. Also fixed in passing: the spec checker still advised adding an ELI10 layer, abolished
23 September.

See [[n-eie-verdeling-mag-nie-na-die-handboek-toe-skuif-nie]] for why our lesson division must
not be adjusted toward a book's, and [[kw4-begroting-uit-vereistes]] for the older
requirements-based approach this supersedes.

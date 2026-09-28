---
name: gr7-lo-waar-ons-is
description: "Gr 7 Lewensorientering, 28 Sep 2026: 1 of 45 signed off, all four specs fixed at source, 31 shared terms; what is still owed."
metadata:
  node_type: memory
  type: project
  originSessionId: 9cbb5026-bd75-4aa5-a144-0346fd07bf1f
  modified: 2026-09-28T10:01:20.627Z
---

Grade 7 Lewensoriëntering, **28 September 2026**. 45 lessons across four sub-topics. **3 signed off and delivered** (Grondwetlike regte 1, Wêreld van werk 7, Gesondheid 10) — and the bottleneck is the fact check, not the writing: 36 of 45 have clean coverage and only 3 a clean fact report. Everything else is drafted, gated, and in its repair-and-re-check round. See [[gr7-lo-besluite]] for the year's rulings.

**All four specs have now been fixed at source** from the fact checks — 55 contradicted claims in Gesondheid alone. Every correction sits at the **opening line of the field that ordered the fault**, because coverage tests against `kern` and a `feiterisiko` note withdraws nothing. Three Gesondheid corrections had landed *underneath* the old instruction, so the old one still read as live.

**The shared list is now 41 terms** (`kaps/gedeelde-omskrywings-lewensorientering-gr7.json`). Eighteen went in on 28 September, and ten of those were shared terms the decision list was holding nothing against — agreed across up to eight lessons, one across three sub-topics, **never recorded** — while three specs told writers they came "word for word from the shared list", so the drift sweep had nothing to test them against. Check that a term a spec calls shared is actually in the file.

**Cross-grade divergences recorded, all with Grade 4-6 left exactly as delivered:** `kieme` widens so a virus falls inside it (Lampies, 28 Sep); `maatskaplike werker` and `gemeenskapsgesondheidswerker` are **corrections**, not widenings — the old social-worker wording fits any trained lay counsellor and the title is legally protected; `konflik` diverges because the Grade 6 form teaches that conflict has already gone wrong, and it has not. The Grade 5/6 reprints those three imply are **parked on Lampies' instruction** to leave Grades 4-6 alone for now.

**His rulings of 28 September, all seven:**

* the epilepsy lesson takes **ten** seizure steps plus the emergency criteria (about five minutes, a second seizure before waking, does not wake, injured, struggling to breathe, or a first seizure), with "call an adult" first
* **the side position stays AFTER the seizure** — his third ruling on it, made with the split in the sources in front of him: CDC, the Epilepsy Foundation and a South African source say during if he is lying down, Epilepsy Action and Epilepsy Society UK say after. Closed, not open.
* a child who can find no adult **may call the emergency service herself**, and the lesson still gives **no number** — the gap closes without breaking the no-numbers rule
* the work lesson names **grants and remittances alongside wages**, because in the Eastern Cape and Limpopo grants are the main source for more households than salaries; the dignity sentence about unpaid work stays without a qualifier
* the water line moves from a tap **inside the dwelling to water on the property** — only 45% have an indoor tap and about 42% a yard tap, so the old form swept those households in
* a child who sent an image of herself is told **what to do, with no promise about consequences**: tell a trusted adult straight away, the sooner the more he can do. No reassurance we cannot verify, and no threat either.
* one word covers both a threatening and a dangerous situation, and the glossary entry says so

**Two tools changed on 28 September, and both close a hole the notes kept describing.**

* A spec now declares its own **record** fields in `nie_vir_die_skrywer`, and the runner leaves them out of the writer's extract. The extracts had reached 57-77 KB and a third of that was the accumulated record of retracted decisions. Nothing is deleted and the record still binds; a writer just sees only the omitted field NAMES, with a line saying it may ask. Declared per spec rather than in the runner, because the names differ in every spec.
* A lesson may be exempted from the word ceiling one lesson at a time, via `plafon_uitsondering` in its own spec entry, which the runner passes to the gate. **The reason this matters is general:** the exemption had been recorded in the spec while the gate went on printing "a person must cut it to 700 or fewer" every run. A stale instruction in a field is obeyed by the next writer; a stale instruction printed by a TOOL is obeyed by everyone, every time, because the tool runs and the field does not. The gate still measures and still reports the overrun -- it only says "allowed, and by whose decision".

**What Grade 7 has cost that is worth carrying forward:** the comma ceiling (0.35 per sentence) failed four Gesondheid lessons *because* the corrections added qualifiers — the fix is splitting sentences, bounded below by the Grade 7 sentence-length floor of 13. And two spec fields turned out to forbid what another field demanded; see [[n-waarskuwing-moet-elke-broer-dek]].

**Grades 8 and 9: nothing started.** They begin once Grade 7 is through, because these wordings and rulings are the starting point for both.

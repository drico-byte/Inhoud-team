---
name: n-les-met-n-nommer-in-verouder
description: A lesson containing a live helpline number can go stale after approval; record the checked date in the spec so it can be re-verified at reprint.
metadata:
  type: project
---

Grade 4 Life Orientation lesson 11 (bullying) names **Childline Suid-Afrika,
116** — verified 2 September 2026 against Childline's own contact page, the
government's Vuk'uzenzele, and press coverage of the change from the older 0800
number.

The writer refused to invent a number when first briefed, which was the right
call, and then flagged the real problem once it had one: this is the only fact
in the lesson that can go **wrong later without anyone touching the file**, and
it is wrong in the worst possible place — a child who cannot reach an adult
dialling a dead number.

**Why:** every other check in this pipeline asks whether a claim was true when
written. This one has to stay true. Nothing in the gate, the coverage check or
the fact check re-runs after approval.

**How to apply:** the spec's `hulpbron` object carries `nagegaan` with the date
and the sources. Re-verify the number whenever the lesson is reprinted or
re-approved, not only when it is written. If it ever changes, the lesson goes
back through the writer — see [[moenie-self-inhoud-skryf-nie]]. Any future
lesson that names a service, a number or an address inherits the same
obligation.

---
name: die-herstellus-blaas-die-spek-op
description: A day of source repairs took one spec from 179KB to 238KB and a lesson extract to 118KB, 41% of it record text; trim an orders-only working copy, and never drop the canonical line.
metadata:
  type: project
---

On 12 October 2026 one Grade 6 sub-topic's specification went from 179 KB to 238 KB in a
single day of repairing requirements at source, and one lesson's extract reached **118 KB,
of which 41 per cent was dated record text** sitting below the line that says nothing
beneath it orders anything. Two single fields passed 14 KB. A general-purpose repair agent
stalled outright on the file, writing nothing.

**The repair loop is the growth mechanism.** Every fix amends an order and appends a dated
record explaining itself — which is right, and is how a withdrawn claim stops coming back —
but the records accumulate against an extract a writer has to read end to end.

**The fix: an orders-only WORKING COPY.** Truncate every field at its record marker, keep
every order verbatim, and hand the writer that. Assert field by field that each order is
byte-identical and the key set unchanged, rather than assuming it. Leave the real extract
alone: the coverage checker reads it and finds stale orders precisely by comparing an order
against the record below it, so stripping records would blind that check. Put the copy in
the scratchpad, never in the tree. One lesson went 118 KB → 77 KB, another 69 KB → 47 KB,
with no order lost. For scale, a writer successfully read an 88 KB extract the same week.

**THE TRAP, and it is not obvious.** Do NOT drop the canonical line when you trim. Without
it, the boundary finder falls back to the legacy marker words — REGGESTEL, TERUGGETREK,
AANGETEKEN and the rest — and those legitimately appear INSIDE an ordering half, inside
sentences that order. So dropping the line promotes the first of them to the boundary and
everything after it reads as ordering nothing. The canonical line is what protects the
orders above it from the correction words written among them. Keep the line, and put the
"records trimmed" note below it. An assertion caught this; reading would not have.

Related: [[n-nota-te-lank-vir-die-skrywer]], [[n-spek-so-lywig-dat-dit-nie-geskryf-kan-word-nie]],
[[die-provenansie-nota-groei-tot-sy-eie-blokkasie]], [[die-merker-begrawe-die-bestelling]],
[[n-regstelling-te-ver-van-sy-fout]].

**THE INVERSE TRAP, 12 October 2026: appending a record to a field with NO canonical line
can put the record on the wrong side of a boundary the record itself creates.** I appended a
dated record to a fact-risk item that had never been given the canonical line. My record
contained the word `TERUGGETREK`. The boundary finder, having no canonical line to prefer,
fell back to legacy marker words and took MY OWN WORD as the boundary — so my record's
opening sentence counted as part of the ORDERING half, while the sentence I was trying to
supersede stayed above it anyway. Two faults from one append.

**So before appending a record to any field, check whether it has the canonical line. If it
does not, rebuild the field in the canonical shape instead of appending** — orders first,
then the line, then the records. And never let a legacy marker word be the first one your new
text introduces. Related: [[die-merker-begrawe-die-bestelling]], [[n-rekord-word-as-n-bestelling-gelees]].

**THE SPLIT ITSELF HAD THE TRAP, 16 October 2026.** When the orders-only copy became the
real extract (spek/les-N.json beside les-N.rekords.json), the splitter still cut a field
with no canonical line at its first legacy word mid-field. 806 fields were cut that way, and
220 of them, in 65 specs, hid order-like wording from the writer. Example: a Grade 4 water
lesson's corrected rule, reach or throw from dry ground and never go in yourself, sat after
'REGGEMAAK 2026-09-03' and vanished. Fixed in paaie._verdeel_waarde: **only the canonical
line cuts a field; every other field stays whole.** After the refresh, 0 of 690 hidden halves
start anywhere but at the canonical line.

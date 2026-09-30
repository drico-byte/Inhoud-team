#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Report spec fields that have collected corrections without being rewritten.

The failure this catches cost more rounds than any other on 30 September 2026. A
fact check finds a fault; the fault is written up in a dated record appended to the
field; and the sentence at the TOP of the field - the one a writer actually obeys -
is left saying the withdrawn thing, often in capitals. A writer reading top-down
meets the order before the withdrawal, rebuilds the fault, and can cite the field
for it. Coverage cannot object, because the draft matches the requirement. Seven
fields were found this way in one sub-topic in one day, each by a different writer
noticing it in passing.

WHAT IT CAN AND CANNOT DO. It cannot tell you that an order contradicts its own
record: that is a question about meaning. The first version of this script tried,
by looking for the withdrawn form quoted inside the record. Tested against a commit
that definitely carried the fault, it found nothing - records usually DESCRIBE the
withdrawn wording rather than quote it, and where they do quote, they quote the new
form.

So it reports the RISK, which is honestly detectable: a field carrying several
dated records whose order has never been rewritten. Rewriting a field means putting
every order first and following it with one line saying the rest is a record; that
line is what the script looks for. A field with three corrections and no such line
has had three chances to acquire a stale order and nobody has read it end to end
since.

It changes nothing, and every hit needs a person to read the field.

    python bin/verouderde-bestellings.py --vak "Sosiale Wetenskappe" --graad 6
    python bin/verouderde-bestellings.py --alles --min 3
"""
import argparse
import glob
import json
import os
import re
import sys

# The line a rewritten field carries: everything after it is a record and orders
# nothing. A field that has this has been read end to end by someone.
REKORDLYN = "ALLES HIERONDER"

# A dated record: anything marking a correction, a withdrawal or a clarification.
REKORD = re.compile(r"REGGESTEL|TERUGGETREK|VERBREED|GEKWALIFISEER|OMVANG VERNOU|"
                    r"AANGEVUL|TYDGEMERK|OPGEHELDER|HERBEVESTIG|TWEEDE REGSTELLING|"
                    r"Bygevoeg \d")


def velde(obj, pad=""):
    """Every string field in a spec or a lesson entry, with a readable path."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            for x in velde(v, "%s.%s" % (pad, k) if pad else k):
                yield x
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            for x in velde(v, "%s[%d]" % (pad, i)):
                yield x
    elif isinstance(obj, str):
        yield pad, obj


def ondersoek(pad, minimum):
    spek = json.load(open(pad, encoding="utf-8"))
    treffers = []
    dele = [("", spek)]
    for les in spek.get("lesse", []):
        dele.append(("les %s" % les.get("nommer"), les))
    for waar, obj in dele:
        bron = dict(obj)
        bron.pop("lesse", None)
        for veld, teks in velde(bron):
            if REKORDLYN in teks:
                continue
            n = len(REKORD.findall(teks))
            if n < minimum:
                continue
            m = REKORD.search(teks)
            orde = teks[:m.start()].strip()
            if len(orde) < 20:
                continue          # the whole field is a record; there is no order to go stale
            treffers.append((waar, veld, n, orde))
    treffers.sort(key=lambda x: -x[2])
    return treffers


def main():
    p = argparse.ArgumentParser(
        description="Report spec fields that have collected corrections without being rewritten")
    p.add_argument("--vak")
    p.add_argument("--graad", type=int)
    p.add_argument("--alles", action="store_true")
    p.add_argument("--min", type=int, default=2,
                   help="how many dated records before a field is worth re-reading (default 2)")
    a = p.parse_args()

    paaie = sorted(glob.glob("spesifikasies/goedgekeur/**/*.json", recursive=True))
    if not a.alles:
        if a.graad:
            paaie = [x for x in paaie if "/gr%d/" % a.graad in x.replace(os.sep, "/")]
        if a.vak:
            slak = a.vak.lower().replace(" ", "-")
            paaie = [x for x in paaie if slak in x.replace(os.sep, "/").lower()]
    if not paaie:
        print("Geen spesifikasie gevind nie. Gebruik --alles, of gee --vak en --graad.")
        return 2

    totaal = 0
    for pad in paaie:
        try:
            treffers = ondersoek(pad, a.min)
        except Exception as exc:
            print("KON NIE LEES NIE: %s (%s)" % (pad, exc))
            continue
        if treffers:
            print("")
            print(pad.replace(os.sep, "/"))
            for waar, veld, n, orde in treffers:
                ets = "%s %s" % (waar, veld) if waar else veld
                print("   %-24s %d regstellings, bestelling nooit herskryf nie" % (ets, n))
                kort = orde[:150] + ("..." if len(orde) > 150 else "")
                print("      bestelling: %s" % kort)
                totaal += 1

    print("")
    print("%d spesifikasie(s) ondersoek, %d veld(e) wat 'n mens moet lees."
          % (len(paaie), totaal))
    if totaal:
        print("Lees elke veld van bo af. Se die bestelling nog wat 'n regstelling hieronder")
        print("teruggetrek het? Herskryf dan die veld - elke bestelling eerste, dan EEN")
        print("rekordblok wat met 'ALLES HIERONDER IS 'n REKORD EN BESTEL NIKS' begin - eerder")
        print("as om nog 'n nota by te voeg. Hierdie sweep kan NIE se dat 'n veld stukkend is")
        print("nie; hy se net waar die kans die grootste is.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

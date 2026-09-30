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


def orde_van(teks):
    """The part of a field that orders: above the record line, or above the first record."""
    if REKORDLYN in teks:
        return teks[:teks.index(REKORDLYN)]
    m = REKORD.search(teks)
    return teks[:m.start()] if m else teks


# A prohibition, as the specs write them. The content between MOENIE and NIE is what
# the field forbids, and if a sibling field's order still asks for it, the two orders
# contradict each other.
# A prohibition, as the specs write them. The content between MOENIE and NIE is what
# the field forbids, and if a sibling field's order still asks for it, the two orders
# contradict each other.
VERBOD = re.compile(r"MOENIE\s+(.{12,220}?)\s+NIE[.,]", re.S)
STOPWOORDE = {"die", "dat", "van", "wat", "met", "vir", "nie", "hulle", "en", "in", "op",
              "is", "as", "aan", "moenie", "word", "hierdie", "ook", "dit", "nou", "een",
              "kan", "mag", "moet", "sonder", "eerder", "omdat", "want", "maar", "self"}

# Fields that exist to hold prohibitions, records or source quotations. A prohibition
# matching one of these is not a contradiction - it is the same topic being named in
# the place where naming it is the point. Leaving these in made the check fire on
# nearly every specification in the repository.
GERAAS = re.compile(r"moenie|verbode|verbied|let_op|_nota|nota$|kaps_punt|titel_nota|"
                    r"feiterisiko|buite_bestek|dieptegrens|verifikasie|herkoms|rede$|"
                    r"video_naat|moeilike_konsepte|nagegane|feitekontrole", re.I)

# Five words, not three. Three matched a shared topic; five matches a shared CLAIM.
SKERF = 5


def botsende_verbode(dele):
    """Prohibitions in one field that a SIBLING field's order still asks for.

    This is the case the record line cannot catch: a field is rewritten, and then a
    later correction to the field NEXT TO IT withdraws something this one still
    orders. It happened on 30 September 2026 between two core items of one lesson, an
    hour apart, and a writer found it rather than any sweep.

    It is noisy even so, which is why it is opt-in. Read every hit; most will be a
    prohibition and a legitimate mention of the same subject sitting side by side.
    """
    uit = []
    for waar, obj in dele:
        bron = dict(obj)
        bron.pop("lesse", None)
        ordes = {veld: orde_van(t) for veld, t in velde(bron)}
        for veld, orde in ordes.items():
            for m in VERBOD.finditer(orde):
                verbod = m.group(1)
                woorde = [w for w in re.findall(r"[A-Za-zÀ-ÿ']{4,}", verbod.lower())
                          if w not in STOPWOORDE]
                if len(woorde) < SKERF:
                    continue
                skerwe = {" ".join(woorde[i:i + SKERF]) for i in range(len(woorde) - SKERF + 1)}
                for ander, ander_orde in ordes.items():
                    if ander == veld or GERAAS.search(ander):
                        continue
                    # the target's own prohibitions are not orders either
                    skoon = VERBOD.sub(" ", ander_orde)
                    laag = " ".join(w for w in re.findall(
                        r"[A-Za-zÀ-ÿ']{4,}", skoon.lower()) if w not in STOPWOORDE)
                    if any(sk in laag for sk in skerwe):
                        uit.append((waar, veld, ander, verbod.strip()[:110]))
                        break
    return uit


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


# An imperative, as the specs write them. If one of these sits BELOW the record marker,
# the field is telling a writer to do something in the part that says it orders nothing.
#
# The word boundaries matter and were lost once: written through a shell heredoc, every
# \b became a literal backspace character, so the pattern matched nothing and the check
# reported a clean bill on three inputs that definitely carried the fault. Edit this file
# directly rather than generating these lines from a shell string.
BEVEL = re.compile(r"\bMOENIE\b|\bMOET\b|\bGEE\b|\bSE DAT\b|\bSKRYF\b|\bVERNOU\b|"
                   r"\bNOEM\b|\bVERANDER\b|\bLAAT VAL\b|\bVAL WEG\b|\bBLY NET SOOS\b")

# Words that make an imperative a QUOTATION of a withdrawn instruction rather than a live
# one. A record legitimately says "the old form said MOENIE ..." and that is not a buried
# order.
AANHALING = re.compile(r"teruggetrek|ou vorm|die konsep het|voorheen|vroeer|het gese|"
                       r"is vals|was vals|aangehaal", re.I)


def begrawe_bevele(dele):
    """Imperatives sitting below a field's own record marker.

    Nine fields lost an order this way on 30 September 2026, every one of them because a
    later correction was appended to a field that had already been rewritten. The marker
    is explicit that nothing below it orders anything, so a writer reading the field as
    instructed never sees the instruction - and coverage cannot object, because the draft
    matches what the field appears to require.
    """
    uit = []
    for waar, obj in dele:
        bron = dict(obj)
        bron.pop("lesse", None)
        for veld, teks in velde(bron):
            if REKORDLYN not in teks:
                continue
            rekord = teks[teks.index(REKORDLYN):]
            for m in BEVEL.finditer(rekord):
                sin_begin = max(rekord.rfind(".", 0, m.start()), 0)
                sin = rekord[sin_begin:m.end() + 160]
                if AANHALING.search(sin):
                    continue
                uit.append((waar, veld, sin.strip(" .")[:130]))
                break
    return uit


def main():
    p = argparse.ArgumentParser(
        description="Report spec fields that have collected corrections without being rewritten")
    p.add_argument("--vak")
    p.add_argument("--graad", type=int)
    p.add_argument("--alles", action="store_true")
    p.add_argument("--botsings", action="store_true",
                   help="also look for a prohibition in one field that a sibling field still "
                        "orders. Noisy: read every hit.")
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
    botsings = 0
    begrawes = 0
    for pad in paaie:
        try:
            spek0 = json.load(open(pad, encoding="utf-8"))
            dele0 = [("", spek0)] + [("les %s" % l.get("nommer"), l)
                                     for l in spek0.get("lesse", [])]
            begrawe = begrawe_bevele(dele0)
        except Exception as exc:
            print("KON NIE LEES NIE: %s (%s)" % (pad, exc))
            continue
        if begrawe:
            print("")
            print("%s  -- BEGRAWE BEVELE" % pad.replace(os.sep, "/"))
            for waar, veld, sin in begrawe:
                ets = "%s %s" % (waar, veld) if waar else veld
                print("   %-24s 'n bevel staan ONDER die rekordmerker" % ets)
                print("      %s" % sin)
                begrawes += 1
        bots = []
        if a.botsings:
            try:
                spek = json.load(open(pad, encoding="utf-8"))
                dele = [("", spek)] + [("les %s" % l.get("nommer"), l)
                                       for l in spek.get("lesse", [])]
                bots = botsende_verbode(dele)
            except Exception as exc:
                print("KON NIE LEES NIE: %s (%s)" % (pad, exc))
                continue
        if bots:
            print("")
            print("%s  -- BOTSENDE BESTELLINGS" % pad.replace(os.sep, "/"))
            for waar, veld, ander, verbod in bots:
                ets = "%s %s" % (waar, veld) if waar else veld
                print("   %-24s verbied iets wat %s nog bestel" % (ets, ander))
                print("      verbod: MOENIE %s NIE" % verbod)
                botsings += 1
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
    print("%d spesifikasie(s) ondersoek, %d veld(e) wat 'n mens moet lees, %d begrawe bevel(e), "
          "%d botsende verbod(e)." % (len(paaie), totaal, begrawes, botsings))
    if begrawes:
        print("'n BEGRAWE BEVEL is 'n opdrag wat ONDER die rekordmerker staan, waar die veld self se dat")
        print("niks bestel word nie. Skuif hom bo die merker, positief gestel. Dit is die enigste een van")
        print("hierdie drie toetse wat presies is: elke treffer is 'n egte fout, tensy dit 'n aanhaling van")
        print("'n teruggetrekte opdrag is.")
    if botsings:
        print("'n BOTSENDE VERBOD is waar een veld iets verbied wat 'n BUURVELD nog bestel. Dit is die")
        print("geval wat die rekordlyn nie kan vang nie: 'n veld word herskryf, en dan trek 'n later")
        print("regstelling aan die veld LANGSAAN iets terug wat hierdie een nog vra. Die later een wen;")
        print("maak die vroeer een reg by sy bestellende sin.")
    if totaal:
        print("Lees elke veld van bo af. Se die bestelling nog wat 'n regstelling hieronder")
        print("teruggetrek het? Herskryf dan die veld - elke bestelling eerste, dan EEN")
        print("rekordblok wat met 'ALLES HIERONDER IS 'n REKORD EN BESTEL NIKS' begin - eerder")
        print("as om nog 'n nota by te voeg. Hierdie sweep kan NIE se dat 'n veld stukkend is")
        print("nie; hy se net waar die kans die grootste is.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

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
#
# THE CASE OF THIS SUBSTRING IS LOAD-BEARING. Matched case-insensitively it would also hit
# 'Alles hieronder bly geld' - which says the exact OPPOSITE, that everything below still
# orders - and ondersoek SKIPS every field carrying this marker. Measured 1 October 2026:
# 108 fields carry the marker exactly, in capitals; a looser case-insensitive compare picks
# up 35 further fragments, and nearly every one of those is 'Alles hieronder bly geld' or
# 'Alles anders hieronder GELD STEEDS'. So a case-insensitive compare here would silently
# drop exactly the fields that announce a live order below.
REKORDLYN = "ALLES HIERONDER"

# A dated record: anything marking a correction, a withdrawal or a clarification.
#
# EVERY ALTERNATIVE IS IN CAPITALS AND THIS PATTERN IS CASE-SENSITIVE ON PURPOSE. In these
# fields case IS the signal: capitals mark a structure, and the same word in lower case is
# ordinary Afrikaans prose which often means the opposite. Measured 1 October 2026 over all
# 91 specs: 'verbreed' appears 62 times in lower case and nearly every one of them is prose
# or an ORDER ('MOENIE DIT VERBREED NIE', 'Verbreed die sin dus eerder as om hom te skrap'),
# against 16 in capitals; 'teruggetrek' 119 times, 'reggestel' 56. Compiling this with re.I
# took the list from 39 fields to 89. So do not add flags here, and do not treat a report
# that some field's marker is in lower case as a missed record - read that field first. It
# is usually prose, and an order read as a record is worse than a record read as prose,
# because orde_van then truncates the order at it.
REKORD = re.compile(r"REGGESTEL|REGGEMAAK|TERUGGETREK|VERBREED|GEKWALIFISEER|OMVANG VERNOU|"
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
#
# TRIED AND REVERTED on 30 September 2026, and worth knowing so nobody tries it again. A
# WRITER found a live order below a marker that this pattern cannot see: "DIE WOORDELYS DRA
# 'n INSKRYWING VIR 'wet'" is an order phrased as a statement. Adding \bDRA\b did catch it --
# and fired on two of my own RECORDS, one of them the sentence explaining that this pattern
# cannot see it. That is the trade this check must not make: its whole value is that every
# hit is real, so a verb which also appears inside records turns it into the noisy check the
# other two already are. AN ORDER PHRASED AS A STATEMENT IS NOT CATCHABLE BY A VERB LIST.
#
# THE SECOND DEAD END, 1 October 2026, and this one cannot be tuned into working. The idea
# was to stop recognising orders at all and look for a different signature instead: a record
# says a form was withdrawn AND quotes it, so if a long piece of that quotation still appears
# in the field's ordering half, the order is probably still giving it. Meaning-free, and it
# would have caught statement-shaped orders.
#
# It found ZERO of sixteen known cases, including on a commit that definitely carried them.
# Two reasons, and the second is fatal:
#
#   1. Records announce a withdrawal in far more ways than a verb list holds -- "is uit die
#      openingslys gehaal", or no verb at all ("die ou vorm het 'X' bestel - nou verbod (4)",
#      where the withdrawal is carried by a cross-reference).
#   2. AFRIKAANS WRITES ITS INDEFINITE ARTICLE WITH AN APOSTROPHE. Nearly every sentence in
#      these fields contains 'n, so a single-quote regex cannot delimit a quotation in this
#      repository's prose -- it truncates at the first article inside the quoted run. There is
#      no quoting convention here that a pattern could use instead.
#
# So: the reliable detector is an agent reading the field from the top, which found sixteen of
# them. This script's job is to say WHERE to look, not to decide. Do not try to mechanise the
# decision a third time without a quoting convention to stand on.
#
# THE THIRD DEAD END, 1 October 2026. BUILT, MEASURED, AND TAKEN OUT AGAIN. The idea was
# the most promising one yet, because unlike the two above it compares two NUMBERS and
# never two meanings: a field opens by announcing a count ("VIER DINGE WAT HIERDIE ITEM
# VERBIED", "SES DINGE IS GESNY"), then numbers its items (1), (2), (3); when an item is
# added later the opening line is not touched, so it announces the wrong number and a
# reader counting from the top stops early. It is a real fault - it happened at least eight
# times in two days - and it looks mechanical. It is not.
#
# WHAT WAS BUILT: a number word (EEN..TWAALF) followed by a plural noun (DINGE, VRAE,
# GROEPE, PUNTE, ITEMS, BEWERINGS, REELS, VERBODE, STAPPE) is an announcement; the span
# runs to the next announcement or the end of the field; items are "(N)" preceded by
# whitespace or start-of-string (the whitespace is essential - without it "artikel
# 28(1)(c)" and "165(6)" are counted, which was the largest single source of noise); and
# only a run starting at 1 is judged, because (0a), (0b), (0), (1) fields are deliberate.
#
# WHAT IT MEASURED. On commit 1d18e478, over the eight Gr 6 Sosiale Wetenskappe specs: 54
# announcements, 11 reported, 3 of the 11 genuine. On the whole working tree, 91 specs: 13
# reported, ONE genuine - and that one was found and fixed by a person, independently, in
# the hour this was being measured. Call it 1-in-4 at best and 1-in-13 at worst.
#
# WHY IT CANNOT BE TUNED INTO WORKING. Four separate things fool it, and they are the
# ordinary way these fields are written:
#
#   1. CROSS-REFERENCES ARE SPELT EXACTLY LIKE ITEM LABELS. "sien kern-item 4 se verbod
#      (5)", "dieselfde bevinding as punt (3)", "verbod (1) hieronder staan". They are
#      preceded by whitespace, so the guard that defeats legal citations cannot help, and
#      a field that correctly announces four gets a fifth item from a reference to its
#      neighbour. Four of the twelve false positives.
#   2. AN ANNOUNCED LIST IS USUALLY NOT NUMBERED WITH (N) AT ALL. These fields label items
#      (a)(b)(c), (i)(ii), "1." "2.", or just separate them with semicolons. The check
#      then walks past them and counts a DIFFERENT numbered list further down the span -
#      almost always one inside the field's own record block. Five of the twelve.
#   3. THE ANNOUNCEMENT PATTERN MATCHES ORDINARY PROSE, AND A SPAN STOPS AT IT. "MOENIE
#      SKRYF DAT DIE WET DIE TWEE GROEPE APART GEHOU HET NIE" and "(6) DIE BEVESTIGINGSTAP
#      DEK DRIE DINGE EN NET DRIE" are not announcements, but they end the span, so a
#      correct eight- or ten-item list is cut off at item 1 or 6 and reported as short.
#      Three of the twelve. Nested announcements ARE real, so the span cannot simply stop
#      ignoring them.
#   4. "DIE VIER GROEPE BLY RYK, ARM, BEKEND EN ONBEKEND" announces no list at all.
#
# AND THE FAILURE THAT MATTERS MOST IS THE ONE IT IS SILENT ABOUT. Of the three stale
# counts known to be live at 1d18e478, it caught ONE. The second -
# feitekontrole_voor_skryfwerk's "SES DINGE IS GESNY" holding five - it skipped without a
# word, because those five are semicolon-separated prose and it can only count "(N)". That
# is reason 2 again, and it means A CLEAN RUN SAYS NOTHING: sixteen of the 54 announcements
# were skipped silently, and one of the sixteen was a real fault. The third known case
# turned out on reading not to be a fault at all - the field announces two and holds (i)
# and (ii) - so what the check reported there was a false positive, not a catch.
#
# DO NOT REACH FOR A DISTANCE GUARD, which is the obvious next move: require the span's own
# "(1)" to follow the announcement closely, so a span that merely ran into someone else's
# list is discarded. It works on paper and it removes seven of the twelve. But the honest
# non-hits run out to 168 characters and the ONE confirmed true positive sits at 199, so the
# threshold has to be set inside a 30-character window fitted to a single example - and it
# still leaves classes 1 and 3, and still cannot see an unnumbered list.
#
# THE STANDING ANSWER IS NOT A CHECK. A person working in parallel hit this same field on
# 1 October and fixed it the right way: REMOVE the count from the opening line rather than
# correct it, and say that the points are numbered but deliberately not counted - because
# "'n getal in 'n openingsin verouder weer by die volgende byvoeging". A count that is not
# written cannot go stale. Prefer that to anything this script could report.
#
# THE RECORD VOCABULARY, MEASURED RATHER THAN GUESSED, 1 October 2026. REKORD was a list
# written from memory, so it was worth asking what the specs actually write. Method: find
# every date in every field of all 91 specs (3 065 of them), take the 75 characters before
# it, and tally the words in capitals. REGGEMAAK came out FIRST, ahead of REGGESTEL which
# was already in the list - 335 occurrences in capitals, 295 of them within 60 characters
# of a date - and it is the same act as REGGESTEL under a different verb. It is now in the
# pattern. It added 17 fields to the list; 15 of the 17 carry no marker of any kind,
# canonical or variant, and open with an order followed by two or more dated records, which
# is precisely what this check is for. It changed no field's printed order text and dropped
# no field from this list.
#
# It did drop TWO hits from the --botsings list, and that is a gain, not a loss. Both were
# the same prohibition in gr5 energie-en-elektrisiteit, and both arose because the sibling
# field OPENS with 'REGGEMAAK, 10 September 2026:'. With that word unknown, orde_van found
# no marker at all and handed the whole field back as the ordering half - including a block
# labelled '[OORTREFDE TEKS HIERONDER, AS REKORD EN NIE 'N BESTELLING NIE]', which is where
# the matching words sat. The check was reading superseded record text as a live order; the
# printed verbod even quoted that label. Note the cost, though: that field's live orders now
# sit in what orde_van calls the record half, so --botsings cannot see them either. A field
# whose order opens with its own correction marker is beyond both halves of this script.
#
# Do the same tally again before adding anything else here; the words the house uses are not
# the words a person remembers using.
#
# AFGEHANDEL: ASKED FOR, MEASURED, AND DELIBERATELY NOT ADDED, 1 October 2026. A lot of
# superseded orders were retired that day by writing AFGEHANDEL at the head of them, which
# is the house idiom for "this item no longer orders anything", and the worry was the
# reasonable one: that a field retired that way scores zero detectable records, drops below
# the two-record threshold, and so goes invisible to this list - the retirement hiding the
# field. IT DOES NOT HAPPEN, and the reason is worth keeping, because the next person to
# retire an order will have the same worry.
#
#   * 25 fields in the 91 specs contain the word in some case (18 lower, 8 capitals).
#   * 2 of the 25 are already on one of this script's lists.
#   * 0 of the 25 are held under the threshold by AFGEHANDEL being unrecognised. Adding it
#     surfaces NOTHING. The best any field manages is a count of 0 -> 1.
#
# WHY IT CANNOT WORK, which is structural and not a matter of tuning. The other words in
# REKORD mark a note APPENDED BELOW an order; AFGEHANDEL is written in the field's OPENING
# LINE to announce that the field orders nothing at all ("HIERDIE ITEM BESTEL NIKS MEER NIE
# EN DIE HELE RES VAN HAAR IS 'n REKORD, AFGEHANDEL 1 OKTOBER 2026"). One opening line can
# never reach a threshold of two, and a field that opens by withdrawing itself has no stale
# order left to hide - it is the one shape this check does not need to report. Most of the
# 25 are not markers at all: 'afgehandel' in lower case is ordinary Afrikaans, and it turns
# up as "afgehandelde geskiedenis", "nooit afgehandel nie" and "met 'n boete afgehandel".
#
# AND ADDING IT MADE THE REPORT WORSE, which is what settled it. In gr4 vervoer-op-water
# les 1 kern[8] the words sit in a DECISION at the top of the field - "DIE RANGSKIKKING VAN
# DIE VYF IS BESLIS EN AFGEHANDEL - DRICO, 22 SEPTEMBER 2026. MOENIE DIT 'n VIERDE KEER
# OOPMAAK NIE." Recognised as a record, that sentence becomes the start of the record block,
# so orde_van cuts the order at it and the "bestelling:" line this script exists to print
# degrades to the fragment "DIE RANGSKIKKING VAN DIE VYF IS BESLIS EN". Nought gained, one
# line of real output lost.
#
# WHAT THE RETIREMENT WORK ACTUALLY DID, checked against HEAD the same day: the two fields
# retired with AFGEHANDEL got an ALLES HIERONDER marker in the same breath, so they left
# this list the correct way, by being read end to end. THAT is the exit from this list, and
# AFGEHANDEL on its own is not. If you are retiring an order, write the marker too.

# What caught it was an agent reading the field from the top, which is what the report text
# below asks a person to do -- and on 30 September 2026 that was how ten of the eleven were
# found.
BEVEL = re.compile(r"\bMOENIE\b|\bMOET\b|\bGEE\b|\bSE DAT\b|\bSKRYF\b|\bVERNOU\b|"
                   r"\bNOEM\b|\bVERANDER\b|\bLAAT VAL\b|\bVAL WEG\b|\bBLY NET SOOS\b")

# Words that make an imperative a QUOTATION of a withdrawn instruction rather than a live
# one. A record legitimately says "the old form said MOENIE ..." and that is not a buried
# order.
AANHALING = re.compile(r"teruggetrek|ou vorm|ou opdrag|die konsep het|voorheen|vroeer|het gese|"
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

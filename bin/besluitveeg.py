# -*- coding: utf-8 -*-
"""Find spec fields that still route around a DECIDED agreed wording.

WHY THIS EXISTS. A term is decided in the subject-grade's agreed-wordings file, and
the runner injects that file into every spec extract -- so a writer reads the current
wording. But the SPEC still contains the sentences written before the decision:
"do not give this term an entry", "pending Drico's ruling", "write it as an
observable sentence instead". Those fields are what the coverage checker tests
against, and they are what the next revision reads. A writer then either follows the
stale instruction, or follows the ruling and gets failed by coverage.

This happened FOUR times in one day on Gr 5 Natuurwetenskappe -- geraamte,
werweldier, voortplanting and buigbaar -- every time caught by a writer rather than
by us, and every time after the ruling had been "recorded". Recording a ruling in the
wordings file is not the same as sweeping it into the specs.

    python bin/besluitveeg.py --vak "Natuurwetenskappe en Tegnologie" --graad 5

Prints, per decided term, every approved-spec field that mentions it, with the ones
carrying instruction-shaped language marked. It JUDGES NOTHING -- a hit is a field to
read, not a fault. Quoting CAPS verbatim is a legitimate hit and must stay.
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402

# Words that make a field an INSTRUCTION rather than a mention. A stale instruction is
# the thing that bites; a passing mention almost never is.
# TIGHTENED after the first run flagged nearly every field. Afrikaans uses DOUBLE
# NEGATION as ordinary grammar -- "nie ... nie" sits in almost every sentence -- so
# matching on it made the tool pure noise, which is exactly how a check becomes
# something people learn to skip. What is left can only be an instruction or an open
# question, never ordinary prose.
BEVEL = re.compile(
    r"moenie|mag nie|moet nie|"                        # a prohibition
    r"hangende|onbeslis|nog nie beslis|nog oop|"       # an unsettled marker
    r"vir drico om|beslissings_vir_drico|"             # parked for a person
    r"intussen|voorlopig|veilige roete|"               # an interim route
    r"geen (?:begrip|inskrywing|woordelys)",           # the specific omission order
    re.I)

# Words that say the field has ALREADY been brought up to date.
GEDOEN = re.compile(r"verval|beslis deur drico|besluit is geneem|nie meer oop|"
                    r"reeds beslis|geen botsing", re.I)


def wandel(o, pad=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from wandel(v, f"{pad}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from wandel(v, f"{pad}[{i}]")
    elif isinstance(o, str):
        yield pad, o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vak", required=True)
    ap.add_argument("--graad", type=int, required=True)
    ap.add_argument("--term", help="check one term instead of all decided ones")
    a = ap.parse_args()

    lys = P.gedeelde_omskrywings(a.vak, a.graad)
    if not lys:
        print(f"No agreed-wordings file for {a.vak} Gr {a.graad}. Nothing to sweep.")
        return 1
    terme = lys.get("terme") or {}
    if a.term:
        terme = {k: v for k, v in terme.items() if k == a.term}
        if not terme:
            print(f"'{a.term}' is not in that list.")
            return 1
    if not terme:
        print(f"The list for {a.vak} Gr {a.graad} is empty. Nothing decided yet.")
        return 0

    gids = os.path.join(P.SPESIFIKASIES, "goedgekeur", f"gr{a.graad}", P.slug(a.vak))
    paaie = sorted(f for f in os.listdir(gids) if f.endswith(".json")) \
        if os.path.isdir(gids) else []
    print(f"{a.vak} Gr {a.graad}: {len(terme)} decided term(s), {len(paaie)} approved spec(s)\n")

    totaal_bevel = 0
    for term, inskr in sorted(terme.items()):
        patroon = re.compile(r"\b" + re.escape(term) + r"\w*", re.I)
        print(f"=== {term} ===")
        print(f"    decided: {inskr.get('omskrywing')}")
        gevind = False
        for naam in paaie:
            spek = P.lees_json(os.path.join(gids, naam))
            for veld, teks in wandel(spek):
                if not patroon.search(teks):
                    continue
                gevind = True
                bevel = bool(BEVEL.search(teks)) and not GEDOEN.search(teks)
                merk = "  >> INSTRUCTION" if bevel else "     mention"
                totaal_bevel += bevel
                print(f"{merk}  {naam}{veld}")
                if bevel:
                    stuk = patroon.search(teks)
                    i = stuk.start()
                    print(f"                 ...{teks[max(0,i-90):i+130]}...")
        if not gevind:
            print("     (no spec mentions it)")
        print()

    if totaal_bevel:
        print(f"{totaal_bevel} field(s) look like INSTRUCTIONS mentioning a decided term.")
        print("Read each one. A field that quotes CAPS verbatim is fine and stays;")
        print("a field that tells a writer to do something the ruling overturned is not.")
        return 2
    print("No spec field carries instruction-shaped language about a decided term.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

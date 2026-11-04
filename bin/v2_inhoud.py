#!/usr/bin/env python3
"""File every lesson re-signed in the Grade 4-6 language pass into 'V2 inhoud', and
write the list of what changed in each and why.

Lampies, 22 October 2026: the in-pipeline language step runs over every signed-off
Grade 4-6 lesson, and the CAPS audit's gaps are filled in the same pass. Every
lesson that comes through it is delivered again, into one flat folder per grade and
subject, the way the HTML team works (Lampies, 4 November 2026):

    V2 inhoud/Graad 4/PSW/Les 03 - <titel>.pdf

Lewensvaardighede splits into PSW (Persoonlike en Sosiale Welstand: ontwikkeling van
self, sosiale verantwoordelikheid, gesondheids- en omgewingsverantwoordelikheid) and
Kuns (Skeppende Kunste: uitvoerende en visuele kunste). Sosiale Wetenskappe splits
into Geskiedenis and Geografie by its spec's `dissipline`. The lessons in each folder
are numbered 1 to x through the year. The number comes from the spec's `jaarnommer`
where it has one, else from Drico's index in kaps/lesindeks/. Lewensvaardighede has
neither, so it is ordered by term, then CAPS's order of the strands, then the lesson's
own number. The number is a rank over every draft in that grade and subject, not only
the delivered ones, so a lesson keeps its number while another is still in the
pipeline.

A lesson belongs here once it is approved AND its language step ran after the step
shipped (a `taal` event in its state after TAALSTAP_SEDERT) AND it was signed off
after that. A lesson whose language step changed nothing is listed too: it was read
and kept, which is a result.

The CAPS gaps filled in a lesson cannot be read off the lesson, so they are recorded
by hand in 'V2 inhoud/gapings.json' ({"<lesson path>": ["what was added and why"]}),
and this script merges them into the list.

    python bin/v2_inhoud.py              # every Grade 4-6 lesson that qualifies
"""

import glob
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402
import voltooide_lesse as V  # noqa: E402
from hardloop import TAALSTAP_SEDERT  # noqa: E402

V2 = os.path.join(P.REPO, "V2 inhoud")
GAPINGS = os.path.join(V2, "gapings.json")
LYS = os.path.join(V2, "Veranderinge.md")


# The Grade 4 Mathematics lesson was a test and is not part of the delivery (Lampies).
OOR = ("Lewensvaardighede", "Natuurwetenskappe en Tegnologie", "Sosiale Wetenskappe")
KUNS = ("uitvoerende-kunste", "visuele-kunste")   # CAPS's order inside a term
LESINDEKS = os.path.join(P.REPO, "kaps", "lesindeks")


def sub_gids(pad):
    return os.path.basename(os.path.dirname(os.path.abspath(pad)))


def les_nommer(pad):
    return int(os.path.splitext(os.path.basename(pad))[0].split("-")[-1])


def spek_van(les, pad):
    s = P.spek_goedgekeur(les.get("graad"), les.get("vak") or "", sub_gids(pad))
    return P.lees_json(s) if os.path.exists(s) else {}


def spek_les(spek, n):
    lesse = spek.get("lesse") or []
    for e in lesse:
        if isinstance(e, dict) and e.get("nommer") == n:
            return e
    return lesse[n - 1] if 1 <= n <= len(lesse) and isinstance(lesse[n - 1], dict) else {}


def v2_vak(les, pad, spek):
    vak = les.get("vak") or ""
    if vak == "Lewensvaardighede":
        return "Kuns" if sub_gids(pad) in KUNS else "PSW"
    if vak == "Natuurwetenskappe en Tegnologie":
        return "NW en Teg"
    if vak == "Sosiale Wetenskappe":
        d = spek.get("dissipline")
        if d not in ("Geskiedenis", "Geografie"):
            raise SystemExit(f"{pad}: the spec names no dissipline, so the lesson has no V2 folder")
        return d
    return vak


def _lesindeks(graad, vak):
    f = os.path.join(LESINDEKS, f"gr{graad}-{P.slug(vak)}.json")
    if not os.path.exists(f):
        return {}
    return {(P.slug(e.get("subonderwerp") or ""), e.get("les")): e.get("nommer")
            for e in P.lees_json(f).get("lesse") or [] if isinstance(e, dict)}


def jaarvolgorde(paaie):
    """{lesson path: ((grade, V2 folder), number in the year)} for every draft given.

    A group whose lessons all carry a year number is ranked by it; a group with none
    (Lewensvaardighede) by term, CAPS strand order and lesson number. A group that is
    only partly numbered stops: ranking half on one basis and half on the other is how
    two lessons swap places without anyone seeing it.
    """
    groepe, indekse = {}, {}
    for pad in paaie:
        les = P.lees_json(pad)
        spek = spek_van(les, pad)
        n = les_nommer(pad)
        e = spek_les(spek, n)
        vak = (les.get("graad"), les.get("vak"))
        if vak not in indekse:
            indekse[vak] = _lesindeks(*vak)
        jn = e.get("jaarnommer")
        if not isinstance(jn, int):
            jn = indekse[vak].get((sub_gids(pad), n))
        kw = e.get("kwartaal") or spek.get("kwartaal") or 0
        strand = KUNS.index(sub_gids(pad)) if sub_gids(pad) in KUNS else 0
        groep = (les.get("graad"), v2_vak(les, pad, spek))
        groepe.setdefault(groep, []).append((jn, (kw, spek.get("kwartaal") or 0, strand, n), pad))
    uit = {}
    for groep, rye in groepe.items():
        met = [r for r in rye if isinstance(r[0], int)]
        if met and len(met) != len(rye):
            raise SystemExit(f"Graad {groep[0]} {groep[1]}: {len(rye) - len(met)} lessons have no year number")
        rye.sort(key=lambda r: (r[0], r[2]) if met else (r[1], r[2]))
        for i, (_, _, pad) in enumerate(rye, 1):
            uit[pad] = (groep, i)
    return uit


def doel_pad(les, plek):
    (graad, vak), n = plek
    titel = les.get("titel") or ""
    naam = V._veilig(f"Les {n:02d} - {titel}" if titel else f"Les {n:02d}") + ".pdf"
    return os.path.join(V2, f"Graad {graad}", vak, naam)


def _ruim_op(behou):
    """Remove every PDF under a grade folder that is not one of this run's deliveries.

    The old layout's sub-topic folders, and a copy whose number or title has moved,
    would otherwise sit beside the new copies looking just as current. Empty folders
    go too.
    """
    behou = {os.path.normcase(os.path.abspath(p)) for p in behou}
    for g in glob.glob(os.path.join(V2, "Graad *")):
        for wortel, _, lêers in os.walk(g):
            for naam in lêers:
                f = os.path.join(wortel, naam)
                if naam.lower().endswith(".pdf") and os.path.normcase(os.path.abspath(f)) not in behou:
                    os.remove(f)
        for wortel, _, _ in sorted(os.walk(g), key=lambda t: -len(t[0])):
            if wortel != g and not os.listdir(wortel):
                os.rmdir(wortel)


def _rang(rel):
    gids, naam = os.path.split(rel)
    try:
        return gids, int(naam.split(" - ")[0].split()[-1])
    except ValueError:
        return gids, 0


def stand(pad):
    """(qualifies, date signed, language report) for one lesson."""
    les = P.lees_json(pad)
    if les.get("status") != "goedgekeur":
        return False, None, None
    staat_pad = P.staat_pad(pad)
    if not os.path.exists(staat_pad):
        return False, None, None
    ges = P.lees_json(staat_pad).get("geskiedenis") or []
    taal = [e.get("wanneer") for e in ges
            if e.get("gebeurtenis") == "taal" and (e.get("wanneer") or "") >= TAALSTAP_SEDERT]
    if not taal:
        return False, None, None
    goed = [e.get("wanneer") for e in ges
            if e.get("gebeurtenis") == "goedgekeur" and (e.get("wanneer") or "") >= max(taal)]
    if not goed:
        return False, None, None
    verslag = P.lees_json(P.taal_verslag(pad)) if os.path.exists(P.taal_verslag(pad)) else {}
    return True, max(goed)[:10], verslag


def main():
    gapings = P.lees_json(GAPINGS) if os.path.exists(GAPINGS) else {}
    rye, sonder_pdf = [], []
    alles = [p for p in sorted(glob.glob(os.path.join(P.KONSEPTE, "gr[456]", "*", "*", "les-*.json")))
             if P.is_les_konsep(p) and P.lees_json(p).get("vak") in OOR]
    plek = jaarvolgorde(alles)
    for pad in alles:
        ok, datum, verslag = stand(pad)
        if not ok:
            continue
        les = P.lees_json(pad)
        bron = pad[:-len(".json")] + ".pdf"
        doel = doel_pad(les, plek[pad])
        if not os.path.exists(bron):
            sonder_pdf.append(pad)
            continue
        os.makedirs(os.path.dirname(doel), exist_ok=True)
        shutil.copy2(bron, doel)
        rel = os.path.relpath(pad, P.REPO).replace(os.sep, "/")
        rye.append((os.path.relpath(doel, V2).replace(os.sep, "/"), rel, datum,
                    len(verslag.get("toegepas") or []), gapings.get(rel) or []))

    _ruim_op([os.path.join(V2, r[0]) for r in rye])
    rye.sort(key=lambda r: _rang(r[0]))
    reëls = ["# V2 inhoud: wat verander het en hoekom", "",
             "Elke les hier het deur ons eie taalstap gegaan (vinder, keurder, die hek "
             "weer, dan die dekking- en feitetoets) en is weer goedgekeur. Waar die "
             "KABV-oudit 'n gaping gevind het, is dit in dieselfde rondte gevul.", "",
             f"{len(rye)} lesse.", ""]
    vorige = None
    for doel, rel, datum, n, gaps in rye:
        groep = os.path.dirname(doel)
        if groep != vorige:
            reëls += ["", f"## {groep}", ""]
            vorige = groep
        wat = [f"{n} taalverandering(s) toegepas" if n else "taalstap: niks verander nie"]
        wat += list(gaps)   # each line carries its own label (KABV-gaping, Feite, Taal, ...)
        reëls.append(f"- **{os.path.basename(doel)[:-4]}** (goedgekeur {datum}): " + "; ".join(wat))
    os.makedirs(V2, exist_ok=True)
    with open(LYS, "w", encoding="utf-8") as fh:
        fh.write("\n".join(reëls) + "\n")

    print(f"{len(rye)} lesse in '{os.path.relpath(V2, P.REPO)}', lys: {os.path.relpath(LYS, P.REPO)}")
    if sonder_pdf:
        print(f"{len(sonder_pdf)} goedgekeurde lesse het nog geen PDF nie:")
        for p in sonder_pdf:
            print("  " + os.path.relpath(p, P.REPO))
    return 1 if sonder_pdf else 0


if __name__ == "__main__":
    sys.exit(main())

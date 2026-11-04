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
import hashlib
import html
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402
import voltooide_lesse as V  # noqa: E402
from hardloop import TAALSTAP_SEDERT  # noqa: E402

V2 = os.path.join(P.REPO, "V2 inhoud")
GAPINGS = os.path.join(V2, "gapings.json")
LYS = os.path.join(V2, "Veranderinge.md")
MANIFES = os.path.join(V2, "manifest.json")
# {"<lesson path>": "why"}: a lesson listed here is delivered but marked 'held', so
# the HTML team sees the hold in data instead of in a chat message.
TERUGGEHOU = os.path.join(V2, "teruggehou.json")


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
    """Remove every PDF and data file under a grade folder that is not one of this run's deliveries.

    The old layout's sub-topic folders, and a copy whose number or title has moved,
    would otherwise sit beside the new copies looking just as current. Empty folders
    go too.
    """
    behou = {os.path.normcase(os.path.abspath(p)) for p in behou}
    for g in glob.glob(os.path.join(V2, "Graad *")):
        for wortel, _, lêers in os.walk(g):
            for naam in lêers:
                f = os.path.join(wortel, naam)
                if naam.lower().endswith((".pdf", ".json")) and os.path.normcase(os.path.abspath(f)) not in behou:
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


SKEMA = "wolkskool-v2-les-1"


def _norm(t):
    """Text as the PDF's text layer gives it back, so the two can be compared."""
    t = html.unescape(str(t))
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = t.replace("\xad", "").replace("\xa0", " ")
    t = re.sub(r"\s+", " ", t).strip()
    # The browser breaks a line after a hyphen ("twee-en-|dertig", "v.C.-|jare"), and
    # the text layer gives that back as a hyphen and a space.
    return re.sub(r"(?<=\S)- (?=\w)", "-", t)


def lesdata(les, plek, rel, datum):
    """The approved lesson as the HTML team needs it: learner text, in page order.

    Built from the same approved file the PDF is printed from, and in the PDF's own
    order: the body blocks as they fall, then the Woordelys (every begrip), then the
    Vrae (only lessons older than the no-questions rule have any). `rol` says who a
    block is for: `leerder` is text the learner reads, word for word; `vir_html_span`
    is an instruction to the builder (what a map must show), never printed as it is.
    The reading copy's furniture (subject line, CAPS quotation, status stamp, footer)
    sits under `produksie`, so nothing a learner should not see is mixed in with
    what they should. The provenance note and every internal field are left out.
    """
    (graad, vak), n = plek
    lyf, woordelys, vrae = [], [], []
    for b in les.get("blokke", []):
        t = b.get("tipe")
        if t in ("studie", "leesstuk"):
            lyf.append({"afdeling": "lyf", "tipe": t, "rol": "leerder",
                        "kop": b.get("kop") or "", "teks": b.get("teks") or ""})
        elif t == "lys":
            lyf.append({"afdeling": "lyf", "tipe": t, "rol": "leerder",
                        "kop": b.get("kop") or "", "items": list(b.get("items") or [])})
        elif t == "kaart":
            lyf.append({"afdeling": "lyf", "tipe": t, "rol": "vir_html_span",
                        "vir": b.get("vir") or "", "teks": b.get("teks") or ""})
        elif t == "begrip":
            woordelys.append({"afdeling": "woordelys", "tipe": t, "rol": "leerder",
                              "term": b.get("term") or "", "teks": b.get("teks") or ""})
        elif t == "vraag":
            vrae.append({"afdeling": "vrae", "tipe": t, "rol": "leerder", "teks": b.get("teks") or ""})
        else:
            # Never drop a block: a type this tool does not know is exactly what the
            # HTML team must not lose without anyone noticing.
            raise SystemExit(f"{rel}: block type {t!r} has no place in the V2 data")
    return {
        "skema": SKEMA,
        "graad": graad, "vak": vak, "nommer": n, "titel": les.get("titel") or "",
        "goedgekeur": datum, "bron": rel,
        "blokke": lyf + woordelys + vrae,
        "produksie": {
            "nota": "Furniture on the reading copy, not for the learner page.",
            "plek": " · ".join(str(x) for x in (f"Graad {les.get('graad')}", les.get("vak"),
                                                les.get("kaps_onderwerp")) if x),
            "kaps_punt": les.get("kaps_punt") or "",
        },
    }


def pdf_ooreenstem(pdf, data):
    """Every learner string of the data, found in the PDF's text layer. [] when all are.

    The JSON and the PDF come from one approved file, but "can never differ" is a
    claim, and this is what makes it a check: a PDF printed before a later edit to
    the lesson file would otherwise ship beside data that no longer matches it.
    """
    import pymupdf
    doc = pymupdf.open(pdf)
    teks = _norm(" ".join(p.get_text() for p in doc))
    doc.close()
    stukke = [data["titel"]]
    for b in data["blokke"]:
        for k in ("kop", "term", "teks"):
            if b.get(k):
                stukke += [x for x in b[k].split("\n") if x.strip()]
        stukke += b.get("items") or []
    return [s for s in stukke if _norm(s) not in teks]


def _sha(pad):
    h = hashlib.sha256()
    with open(pad, "rb") as fh:
        for stuk in iter(lambda: fh.read(1 << 16), b""):
            h.update(stuk)
    return h.hexdigest()


def skryf_manifes(inskrywings):
    """V2 inhoud/manifest.json, keeping each lesson's earlier issues.

    A lesson whose data fingerprint changed since the last run gets its previous
    issue appended to `uitgawes`, so a reissue can be seen in the data and not only
    in a chat message a new session never reads. The PDF's fingerprint can change
    when the PDF is printed again with the text unchanged, so the JSON's is the one
    that says whether the content moved.
    """
    oud = {}
    if os.path.exists(MANIFES):
        for e in (P.lees_json(MANIFES).get("lesse") or []):
            oud[e.get("bron")] = e
    for e in inskrywings:
        vorige = oud.get(e["bron"])
        uitgawes = list((vorige or {}).get("uitgawes") or [])
        if vorige and vorige.get("json_sha256") != e["json_sha256"]:
            uitgawes.append({k: vorige.get(k) for k in ("goedgekeur", "json_sha256", "pdf_sha256", "pdf")})
        e["uitgawes"] = uitgawes
    with open(MANIFES, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"skema": "wolkskool-v2-manifes-1",
                   "nota": ("One entry per lesson in V2 inhoud. status 'final' may be built; "
                            "'held' may not (see 'rede'). json_sha256 is the content "
                            "fingerprint: when it changes, the lesson was reissued and the "
                            "previous issue is listed under 'uitgawes'."),
                   "lesse": inskrywings}, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def main():
    gapings = P.lees_json(GAPINGS) if os.path.exists(GAPINGS) else {}
    hou = P.lees_json(TERUGGEHOU) if os.path.exists(TERUGGEHOU) else {}
    rye, sonder_pdf, verskil, manifes = [], [], [], []
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
        rel = os.path.relpath(pad, P.REPO).replace(os.sep, "/")
        data = lesdata(les, plek[pad], rel, datum)
        mis = pdf_ooreenstem(bron, data)
        if mis:
            # Ship neither: a PDF and data that disagree are worse than a gap.
            verskil.append((rel, mis))
            continue
        os.makedirs(os.path.dirname(doel), exist_ok=True)
        shutil.copy2(bron, doel)
        doel_json = doel[:-4] + ".json"
        with open(doel_json, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        v2 = lambda p: os.path.relpath(p, V2).replace(os.sep, "/")  # noqa: E731
        manifes.append({
            "graad": data["graad"], "vak": data["vak"], "nommer": data["nommer"],
            "titel": data["titel"], "pdf": v2(doel), "json": v2(doel_json),
            "status": "held" if rel in hou else "final",
            **({"rede": hou[rel]} if rel in hou else {}),
            "goedgekeur": datum, "pdf_sha256": _sha(doel), "json_sha256": _sha(doel_json),
            "bron": rel,
        })
        rye.append((v2(doel), rel, datum, len(verslag.get("toegepas") or []), gapings.get(rel) or []))

    _ruim_op([os.path.join(V2, r[0]) for r in rye] + [os.path.join(V2, e["json"]) for e in manifes])
    manifes.sort(key=lambda e: (e["graad"], e["vak"], e["nommer"]))
    skryf_manifes(manifes)
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
    print(f"manifes: {os.path.relpath(MANIFES, P.REPO)} "
          f"({sum(e['status'] == 'held' for e in manifes)} teruggehou)")
    if sonder_pdf:
        print(f"{len(sonder_pdf)} goedgekeurde lesse het nog geen PDF nie:")
        for p in sonder_pdf:
            print("  " + os.path.relpath(p, P.REPO))
    if verskil:
        print(f"{len(verskil)} lesse NIE afgelewer nie: die PDF stem nie met die les ooreen nie "
              f"(druk die PDF weer met bin/leeskopie.py):")
        for rel, mis in verskil:
            print(f"  {rel}: {mis[0][:100]}")
    return 1 if sonder_pdf or verskil else 0


if __name__ == "__main__":
    sys.exit(main())

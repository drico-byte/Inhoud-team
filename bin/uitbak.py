#!/usr/bin/env python3
"""Assemble the outbox: every approved lesson's PDF plus its sub-topic's protected-
words page.

    lees/gr6/sosiale-wetenskappe/demokrasie-en-burgerskap/Les 01 - <titel>.pdf
    lees/gr6/sosiale-wetenskappe/demokrasie-en-burgerskap/BESKERMDE-WOORDE.md

`lees/` is Drico's outbox, not an archive: he moves what is in it out to the Afrikaans
language check and to the HTML team, so a lesson that is not in it has not been sent.
Both halves have to travel together -- the language checker is better at Afrikaans
than we are and will undo our decisions unless it is told which words not to touch.

    python bin/uitbak.py --vak "Sosiale Wetenskappe" --graad 6
    python bin/uitbak.py --graad 6 --subonderwerp mapungubwe
    python bin/uitbak.py --alles
    python bin/uitbak.py --alles --droog        # say what would happen, change nothing

Two things this refuses to do, because both have cost a round:

* **It will not deliver a PDF older than the draft's last content change.** The
  pipeline PDF is rebuilt at sign-off, but a hand-run repair cycle can leave it
  behind, and a stale PDF in the outbox is read as the lesson. Those are reported
  and skipped, with the lesson named, rather than copied quietly.

* **It will not write a protected-words page by hand.** The page is built from
  taalnasien.versamel -- the same function that builds the block the checker is
  actually shown -- so the page cannot claim a word is protected that the block
  never mentions. The hand-assembled page this replaces had gone stale: it still
  announced four lessons when the sub-topic had eight.
"""

import argparse
import importlib.util
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402
import taalnasien as T  # noqa: E402
import voltooide_lesse as V  # noqa: E402

LEES = os.path.join(P.REPO, "lees")
BLADSY = "BESKERMDE-WOORDE.md"


def _handnasien():
    """keur-goed-na-handnasien.py by path: its name is not an identifier.

    Imported rather than copied for laaste_inhoudverandering(), which reads when a
    draft's CONTENT last changed. The file's clock is the wrong answer -- a write
    that touches only the status field or the provenance note moves the clock
    without changing a word anybody reads, and it has refused a finished lesson
    that way.
    """
    pad = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "keur-goed-na-handnasien.py")
    spek = importlib.util.spec_from_file_location("_kgnh", pad)
    mod = importlib.util.module_from_spec(spek)
    spek.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------ where things go
#
# Drico, 22 September 2026: "hou die naam van die les saam met die lesnommer", and
# the number is the YEAR number -- 1 to the last lesson of that grade -- not a number
# inside a sub-topic. So the outbox is FLAT per subject, and the file name carries the
# year number. That is what Graad 4 Geografie on disk already looks like.
#
# Which forces the split. Graad 6 Sosiale Wetenskappe is two half-subjects with two
# parallel year numberings, so Geskiedenis 20 and Geografie 20 are different lessons
# with the same name. Flat delivery of both into one folder would have one silently
# overwrite the other. Graad 4 solved this by splitting the folder, and so does this.
HELFTES = ("geskiedenis", "geografie")


def spek_van(les, les_pad):
    """The approved spec behind a lesson, or None. Read for jaarnommer and the half."""
    pad = P.spek_goedgekeur(les.get("graad"), les.get("vak") or "", sub_gids(les_pad))
    try:
        return P.lees_json(pad) if os.path.exists(pad) else None
    except ValueError:
        return None


def helfte(spek):
    """Which half of a split subject this spec belongs to, or None.

    Graad 6 names it cleanly in profiel_konfig ('gr6-sw-geskiedenis-profiel.json').
    Graad 4 has no profiler run and says so in prose, but the prose still names the
    half. Both are read the same way, and an entry naming BOTH or NEITHER returns
    None so the subject stays unsplit -- guessing a half is worse than not splitting.
    """
    if not spek:
        return None
    bron = " ".join(str(spek.get(k) or "") for k in ("profiel_konfig", "kaps_vak"))
    gevind = [h for h in HELFTES if h in bron.lower()]
    return gevind[0] if len(gevind) == 1 else None


def sub_gids(les_pad):
    return os.path.basename(os.path.dirname(os.path.abspath(les_pad)))


def uitbak_gids(les, les_pad):
    vak = P.slug(les.get("vak") or "vak")
    h = helfte(spek_van(les, les_pad))
    return os.path.join(LEES, f"gr{les.get('graad')}", f"{vak}-{h}" if h else vak)


def jaarnommer(les, les_pad):
    """The lesson's number in its year, and whether it came from the spec.

    Returns (number, from_spec). Falling back to the file number is reported by the
    caller rather than hidden: in a flat folder the number is what keeps two lessons
    apart, so a guessed one is how a delivery copy overwrites another lesson.
    """
    stam = os.path.splitext(os.path.basename(les_pad))[0]
    try:
        binne = int(stam.split("-")[-1])
    except ValueError:
        return None, False
    spek = spek_van(les, les_pad)
    for inskrywing in (spek or {}).get("lesse", []):
        if not isinstance(inskrywing, dict):
            continue
        if inskrywing.get("lesnommer") == binne or inskrywing.get("les") == binne:
            jn = inskrywing.get("jaarnommer")
            if isinstance(jn, int):
                return jn, True
    lesse = (spek or {}).get("lesse") or []
    if 1 <= binne <= len(lesse) and isinstance(lesse[binne - 1], dict):
        jn = lesse[binne - 1].get("jaarnommer")
        if isinstance(jn, int):
            return jn, True
    return binne, False


def doel_pad(les, les_pad):
    n, uit_spek = jaarnommer(les, les_pad)
    voor = f"Les {n:02d}" if isinstance(n, int) else os.path.basename(les_pad)[:-5]
    titel = les.get("titel") or ""
    naam = V._veilig(f"{voor} - {titel}" if titel else voor) + ".pdf"
    return os.path.join(uitbak_gids(les, les_pad), naam), uit_spek


def _ou_kopiee(doel):
    """Other files for the same lesson number: the title may have changed."""
    gids, naam = os.path.split(doel)
    voor = naam.split(" - ")[0]
    if not os.path.isdir(gids):
        return []
    return [os.path.join(gids, n) for n in os.listdir(gids)
            if n.startswith(voor + " - ") and n.lower().endswith(".pdf")
            and os.path.abspath(os.path.join(gids, n)) != os.path.abspath(doel)]


def _plat_kopie(les, les_pad):
    """This lesson's copy under the oldest flat name, if one is there.

    lees/gr4/lewensvaardighede/visuele-kunste-les-1.pdf. That name carries the
    sub-topic and the lesson number, so unlike the sub-topic-folder layout it maps
    back to exactly one lesson and can be cleaned up per lesson.
    """
    stam = os.path.splitext(os.path.basename(les_pad))[0]
    vak = P.slug(les.get("vak") or "vak")
    uit = []
    for ouer in dict.fromkeys([uitbak_gids(les, les_pad),
                               os.path.join(LEES, f"gr{les.get('graad')}", vak)]):
        ou = os.path.join(ouer, f"{sub_gids(les_pad)}-{stam}.pdf")
        if os.path.exists(ou):
            uit.append(ou)
    return uit


def ou_uitleg_gids(les, les_pad):
    """A superseded sub-topic FOLDER for this lesson's sub-topic, or None.

    Removed once per run rather than once per lesson: the files in it are named by
    their sub-topic number, so no single lesson owns them, and asking each lesson to
    delete them makes the count meaningless and the blame diffuse.
    """
    vak = P.slug(les.get("vak") or "vak")
    for ouer in dict.fromkeys([uitbak_gids(les, les_pad),
                               os.path.join(LEES, f"gr{les.get('graad')}", vak)]):
        onder = os.path.join(ouer, sub_gids(les_pad))
        if os.path.isdir(onder):
            return onder
    return None


def ruim_ou_uitleg(gidse, droog=False):
    """Delete superseded sub-topic folders. Returns (folders, files) removed."""
    lere = vlakke = 0
    for gids in sorted(set(g for g in gidse if g)):
        inhoud = [n for n in os.listdir(gids)
                  if n.lower().endswith(".pdf") or n == BLADSY]
        if len(inhoud) != len(os.listdir(gids)):
            # Something else is in there. Leave it alone and say so: this function
            # deletes, and a surprise in a folder it is about to remove is exactly
            # when it should stop.
            print("NOT REMOVED, it holds something other than lesson PDFs: %s"
                  % P.rel(gids))
            continue
        vlakke += 1
        lere += len(inhoud)
        if droog:
            continue
        for n in inhoud:
            os.remove(os.path.join(gids, n))
        os.rmdir(gids)
    return vlakke, lere


def verouderd(les_pad, pdf_pad, kgnh):
    """Is the PDF older than the draft's last recorded content change?

    Returns the content-change timestamp when it is stale, else None. A lesson with
    no state file cannot be judged this way and is let through -- saying nothing is
    better than refusing on an absence.
    """
    staat_pad = P.newe(les_pad, "staat")
    if not os.path.exists(staat_pad):
        return None
    try:
        _, tyd, wanneer = kgnh.laaste_inhoudverandering(P.lees_json(staat_pad))
    except Exception:
        return None
    if not tyd:
        return None
    return wanneer if os.path.getmtime(pdf_pad) < tyd - 1 else None


# ------------------------------------------------------------------ the page
KOP = """# Beskermde woorde \u2014 Graad {graad} {vak}: {sub}

Stuur hierdie bladsy saam met die {n} les-PDF's na die taalnasiener.

## Twee re\u00ebls vir die nasiener

1. **Moenie 'n woord verander wat hieronder as BESKERM gelys is nie.** Elkeen lees
   soos gewone Afrikaans wat verbeter kan word, en elkeen is 'n besluit wat iewers
   geld gekos het. Die rede staan daarby. As jy meen 'n beskermde woord is werklik
   verkeerd, **s\u00ea dit apart** eerder as om dit te verander.

2. **Verander niks aan die betekenis nie.** As 'n sin taalkundig lam is omdat hy
   feitelik presies moet wees, s\u00ea dit eerder as om hom gladder te maak.

Gee jou antwoord as 'n lys veranderings \u2014 ou sin, nuwe sin \u2014 nie as herskrewe
lesse nie.

**Een ding oor die redes hieronder.** Elke rede begin by die les waar die
besluit geval het, en daardie les is soms in 'n ander graad of 'n ander vak as
hierdie een. Dit is die HERKOMS van die besluit en nie sy OMVANG nie: die woord
is hier net so beskerm. 'n Voorbeeld uit 'n ander vak beteken dus nie die
inskrywing hoort nie hier nie.

---
"""

# The reasons below say the same thing as the block bin/taalnasien.py hands the
# checker. They are repeated here and not imported because that function builds
# fixed-width plain text for pasting, and this is markdown for reading; what must
# never differ is WHICH words appear, and that comes from T.versamel either way.
REDE_BESLIS = (
    "Hierdie bewoording is vir die hele vak-graad BESLIS en in die vak se lys "
    "vasgel\u00ea. Elke les wat die term omskryf, gebruik hierdie woorde. 'n "
    "Verbetering aan een les skep 'n tweede omskrywing van een woord binne een "
    "jaar, en die eksamen dek die hele jaar.")
REDE_BESLIS_MEERVOUDIG = (
    "Hierdie woord dra MET OPSET meer as een betekenis in hierdie vak-graad, en "
    "die betekenisse mag NIE ooreengestem word nie. Hierdie les gebruik die "
    "betekenis '{wanneer}'. Moenie hom na 'n ander betekenis se sin toe skuif nie, "
    "en moenie twee betekenisse saamsmelt nie.")
REDE_GEDEEL = (
    "Dieselfde verklaring staan ook in {waar}. 'n Verbetering aan een van hulle "
    "breek die paar, en 'n toets oor die hele vak sal dit vlag.")
REDE_VOORGESKRYF = (
    "'n Goedgekeurde spesifikasie skryf hierdie bewoording voor, en later lesse "
    "gaan dieselfde woorde gebruik. Hierdie les is net die eerste een wat daar kom.")


def _waar(les, les_pad):
    nommer = os.path.splitext(os.path.basename(les_pad))[0]
    return f"{les.get('titel')} ({sub_gids(les_pad)} {nommer})"


def versamel_bladsy(paaie_en_lesse):
    """Build one sub-topic's page from T.versamel, lesson by lesson.

    Returns (text, counts). Every word on the page fired in at least one of these
    lessons' real language-check blocks, because this reads the same function the
    block does -- so the count printed on the page is measured, not claimed.
    """
    woorde, bewoordings = {}, {}
    for les_pad in paaie_en_lesse:
        les, ws, beslis, gedeel, voorgeskryf = T.versamel(les_pad)
        waar = _waar(les, les_pad)
        for w in ws:
            ins = woorde.setdefault(w["hou"].strip().lower(),
                                    {"hou": w["hou"], "nie": list(w.get("nie") or []),
                                     "rede": w.get("rede") or "", "waar": []})
            ins["waar"].append(waar)
            for n in (w.get("nie") or []):
                if n not in ins["nie"]:
                    ins["nie"].append(n)
        for term, teks, rede, let_op, wanneer in beslis:
            ins = bewoordings.setdefault((term, teks), {"term": term, "teks": teks,
                                                        "waar": [], "rede": [], "soort": "beslis"})
            ins["waar"].append(waar)
            ins["wanneer"] = wanneer
            for r in (rede, let_op):
                if r and r not in ins["rede"]:
                    ins["rede"].append(r)
        for term, teks, ander in gedeel:
            ins = bewoordings.setdefault((term, teks), {"term": term, "teks": teks,
                                                        "waar": [], "rede": [], "soort": "gedeel"})
            ins["waar"].append(waar)
            ins.setdefault("ander", [])
            for a in ander:
                if a not in ins["ander"]:
                    ins["ander"].append(a)
        for term, teks in voorgeskryf:
            ins = bewoordings.setdefault((term, teks), {"term": term, "teks": teks,
                                                        "waar": [], "rede": [], "soort": "voorgeskryf"})
            ins["waar"].append(waar)

    eerste = T.versamel(paaie_en_lesse[0])[0]
    subs = sorted({sub_gids(p).replace("-", " ").capitalize()
                    for p in paaie_en_lesse})
    reels = [KOP.format(graad=eerste.get("graad"), vak=eerste.get("vak"),
                        sub=", ".join(subs), n=len(paaie_en_lesse))]
    reels.append(f"**{len(woorde)} beskermde woorde en {len(bewoordings)} beslisde "
                 f"bewoordings kom in hierdie {len(paaie_en_lesse)} lesse voor.**" + chr(10))

    if woorde:
        reels.append("## Woorde wat net so moet bly\n")
    for sleutel in sorted(woorde, key=lambda s: s.lower()):
        ins = woorde[sleutel]
        reels.append(f"### `{ins['hou']}`\n")
        if ins["nie"]:
            reels.append("**Moenie verander na:** "
                         + ", ".join(f"`{n}`" for n in ins["nie"]) + "\n")
        if ins["rede"]:
            reels.append(ins["rede"] + "\n")
        reels.append("*Kom voor in:* " + "; ".join(ins["waar"]) + "\n")

    if bewoordings:
        reels.append("## Bewoordings wat woord vir woord moet bly\n")
    for sleutel in sorted(bewoordings, key=lambda s: str(s[0]).lower()):
        ins = bewoordings[sleutel]
        reels.append(f"### `{ins['term']}`\n")
        reels.append(f"> {ins['teks']}\n")
        if ins["soort"] == "beslis":
            reels.append((REDE_BESLIS_MEERVOUDIG.format(wanneer=ins["wanneer"])
                          if ins.get("wanneer") else REDE_BESLIS) + "\n")
        elif ins["soort"] == "gedeel":
            reels.append(REDE_GEDEEL.format(waar=", ".join(ins.get("ander") or [])) + "\n")
        else:
            reels.append(REDE_VOORGESKRYF + "\n")
        for r in ins["rede"]:
            reels.append(f"{r}\n")
        reels.append("*Kom voor in:* " + "; ".join(ins["waar"]) + "\n")

    return "\n".join(reels), (len(woorde), len(bewoordings))



# ------------------------------------------------------------------ one at a time
def maats_in_gids(les, les_pad):
    """Every approved lesson that belongs in the same outbox folder as this one.

    The folder, not the sub-topic: the page beside the PDFs has to describe the PDFs
    beside it, and in a flat folder those come from several sub-topics.
    """
    gids = os.path.abspath(uitbak_gids(les, les_pad))
    uit = []
    for pad in V._lesse(les.get("graad"), les.get("vak")):
        pad = pad.replace(os.sep, "/")
        ander = P.lees_json(pad)
        if ander.get("status") != "goedgekeur":
            continue
        if os.path.abspath(uitbak_gids(ander, pad)) == gids:
            uit.append((pad, ander))
    uit.sort(key=lambda pl: (jaarnommer(pl[1], pl[0])[0] or 0, pl[0]))
    return uit


def botsings(items):
    """Lessons in one folder that would deliver under the same "Les NN" prefix.

    This is the whole reason the folder is split by half-subject, so it is checked
    rather than assumed: Geskiedenis 20 and Geografie 20 are different lessons, and
    a flat copy of both would have one quietly overwrite the other. Returns
    {prefix: [paths]} for every prefix claimed more than once.
    """
    per_voor = {}
    for pad, les in items:
        doel, _ = doel_pad(les, pad)
        per_voor.setdefault(os.path.basename(doel).split(" - ")[0], []).append(pad)
    return {v: p for v, p in per_voor.items() if len(p) > 1}


def skryf_bladsy(gids, paaie):
    teks, tel = versamel_bladsy(paaie)
    bladsy = os.path.join(gids, BLADSY)
    tmp = bladsy + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline=chr(10)) as f:
        f.write(teks)
    os.replace(tmp, bladsy)
    return bladsy, tel


def lewer_een(les, les_pad, pdf_pad=None):
    """Put one approved lesson in the outbox and refresh its folder page.

    Called by sign-off, so a lesson reaches Drico without anyone remembering to run
    this script. The page is rebuilt from EVERY approved lesson in the folder, not
    just this one: a page that announces four lessons beside eight PDFs is how the
    hand-assembled one went stale, and the count on it is the whole point.

    Returns (pdf destination, page destination). The caller treats a failure as
    "not delivered", because an approval must never be blocked by a copy.
    """
    pdf_pad = pdf_pad or les_pad[:-len(".json")] + ".pdf"
    if les.get("status") != "goedgekeur" or not os.path.exists(pdf_pad):
        return None, None
    les_pad = les_pad.replace(os.sep, "/")
    gids = uitbak_gids(les, les_pad)
    doel, uit_spek = doel_pad(les, les_pad)
    items = maats_in_gids(les, les_pad)

    bots = botsings(items)
    myne = os.path.basename(doel).split(" - ")[0]
    if myne in bots:
        ander = ", ".join(P.rel(p) for p in bots[myne] if p != les_pad)
        print("NOT DELIVERED: %s would be %s, and so would %s. A flat outbox cannot "
              "hold two lessons under one number, so neither is copied."
              % (P.rel(les_pad), myne, ander))
        return None, None
    if not uit_spek:
        print("Outbox: %s has no jaarnommer in its approved spec, so the number in "
              "its name is the sub-topic's and not the year's." % P.rel(les_pad))

    os.makedirs(gids, exist_ok=True)
    for ou in _ou_kopiee(doel) + _plat_kopie(les, les_pad):
        os.remove(ou)
    ruim_ou_uitleg([ou_uitleg_gids(les, les_pad)])
    shutil.copy2(pdf_pad, doel)
    bladsy, _ = skryf_bladsy(gids, [p for p, _ in items])
    return doel, bladsy


# ------------------------------------------------------------------ doing it
def main():
    ap = argparse.ArgumentParser(description=__doc__.split(chr(10))[0])
    ap.add_argument("--vak")
    ap.add_argument("--graad", type=int, action="append")
    ap.add_argument("--subonderwerp", help="the sub-topic folder name")
    ap.add_argument("--alles", action="store_true")
    ap.add_argument("--droog", action="store_true", help="report only, change nothing")
    a = ap.parse_args()
    if not (a.alles or a.graad or a.vak):
        ap.error("give --alles, or --graad and/or --vak")

    kgnh = _handnasien()
    per_gids = {}
    sonder_pdf, verouderd_uit, sonder_jaar, nie_goedgekeur = [], [], [], 0

    for g in (a.graad or [None]):
        for pad in V._lesse(g, a.vak):
            pad = pad.replace(os.sep, "/")
            if a.subonderwerp and sub_gids(pad) != a.subonderwerp:
                continue
            les = P.lees_json(pad)
            if les.get("status") != "goedgekeur":
                nie_goedgekeur += 1
                continue
            pdf = pad[:-len(".json")] + ".pdf"
            if not os.path.exists(pdf):
                sonder_pdf.append(pad)
                continue
            wanneer = verouderd(pad, pdf, kgnh)
            if wanneer:
                verouderd_uit.append((pad, wanneer))
                continue
            per_gids.setdefault(uitbak_gids(les, pad), []).append((pad, les, pdf))

    gekopieer = oorgeslaan = opgeruim = 0
    geblokkeer = set()
    ou_gidse = set()
    for gids, items in sorted(per_gids.items()):
        bots = botsings([(p, l) for p, l, _ in items])
        if not a.droog:
            os.makedirs(gids, exist_ok=True)
        geskryf = []
        for pad, les, pdf in items:
            doel, uit_spek = doel_pad(les, pad)
            voor = os.path.basename(doel).split(" - ")[0]
            if voor in bots:
                geblokkeer.add((voor, tuple(bots[voor])))
                continue
            if not uit_spek:
                sonder_jaar.append(pad)
            ou_gidse.add(ou_uitleg_gids(les, pad))
            for ou in _ou_kopiee(doel) + _plat_kopie(les, pad):
                opgeruim += 1
                if not a.droog:
                    os.remove(ou)
            geskryf.append(pad)
            if (os.path.exists(doel) and os.path.getsize(doel) == os.path.getsize(pdf)
                    and os.path.getmtime(doel) >= os.path.getmtime(pdf)):
                oorgeslaan += 1
                continue
            gekopieer += 1
            if not a.droog:
                shutil.copy2(pdf, doel)
        if not geskryf:
            continue
        nw, nb = (versamel_bladsy(geskryf)[1] if a.droog
                  else skryf_bladsy(gids, geskryf)[1])
        print("%-48s %2d lesse, %2d woorde, %2d bewoordings"
              % (os.path.relpath(gids, P.REPO).replace(os.sep, "/"),
                 len(geskryf), nw, nb))

    print()
    vlakke, lere = ruim_ou_uitleg(ou_gidse, a.droog)
    print("copied %d, already current %d, superseded copies removed %d"
          % (gekopieer, oorgeslaan, opgeruim))
    if vlakke:
        print("superseded sub-topic folders removed: %d, holding %d files"
              % (vlakke, lere))
    if nie_goedgekeur:
        print("not approved, so not sent: %d" % nie_goedgekeur)
    for pad in sonder_pdf:
        print("NO PDF, not sent: %s" % P.rel(pad))
    for pad in sonder_jaar:
        print("NO jaarnommer in the approved spec, so the name carries the "
              "sub-topic number: %s" % P.rel(pad))
    for pad, wanneer in verouderd_uit:
        # The dangerous case, so it is loud: the lesson has been repaired since its
        # PDF was built, and a stale PDF in the outbox is read as the lesson.
        print("PDF OLDER THAN THE DRAFT, not sent: %s (content changed %s)"
              % (P.rel(pad), wanneer))
    for voor, paaie in sorted(geblokkeer):
        print("TWO LESSONS WOULD BE %s, so neither is sent: %s"
              % (voor, ", ".join(P.rel(p) for p in paaie)))
    if a.droog:
        print(chr(10) + "--droog: nothing was written")
    return 1 if (sonder_pdf or verouderd_uit or geblokkeer) else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Turn a lesson into a readable PDF for human review.

    python bin/leeskopie.py konsepte/gr4/sosiale-wetenskappe/vervoer-op-water/les-1.json
    python bin/leeskopie.py --vak "Sosiale Wetenskappe" --graad 4 \
                            --subonderwerp "Vervoer op water" --les 1
    python bin/leeskopie.py --alles          # every draft and approved lesson

THIS IS A READING COPY, NOT A RENDERING.

The HTML team owns how a lesson looks to a learner. This exists for one job: so a
person can read a lesson and judge it, instead of reading JSON. Nothing here is a
layout decision for the published page, nothing downstream consumes it, and it can
be deleted and regenerated at any time. If it ever starts to look like a second
rendering pipeline, that is a mistake — delete it rather than extend it.

It does honour the one layout requirement the content architecture genuinely
depends on: the intuition layer is visually distinct from the study text. If a
reader cannot tell at a glance which text is revision material and which is
intuition, the whole study-volume discipline collapses at the point of use — so a
review copy that blurred them would be judging something other than the lesson.

PDF generation uses headless Edge or Chrome, which is present on any Windows 11
machine. Nothing to install.
"""
import argparse
import glob
import html
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402

LEES = os.path.join(P.REPO, "lees")

BROWSERS = [
    r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    r"C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    r"C:/Program Files/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
]

STATUS_WOORDE = {
    "konsep": ("KONSEP", "Nog nie deur die hek nie."),
    "gated": ("KONSEP — GEMEET", "Lengte en register is nagegaan. Nog nie goedgekeur nie."),
    "goedgekeur": ("GOEDGEKEUR", "Hierdie les is goedgekeur."),
}

CSS = """
@page { size: A4; margin: 20mm 22mm 18mm 22mm; }
* { box-sizing: border-box; }
body {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 12pt; line-height: 1.62; color: #1a1a1a;
  margin: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
header { border-bottom: 2px solid #1a1a1a; padding-bottom: 10px; margin-bottom: 26px; }
h1 { font-family: "Segoe UI", Arial, sans-serif; font-size: 22pt; line-height: 1.2;
     margin: 0 0 8px; font-weight: 600; }
.plek { font-family: "Segoe UI", Arial, sans-serif; font-size: 9.5pt;
        color: #555; letter-spacing: .02em; }
.stempel { font-family: "Segoe UI", Arial, sans-serif; font-size: 9pt; font-weight: 600;
           display: inline-block; margin-top: 10px; padding: 3px 9px; border-radius: 3px;
           background: #f0ede4; border: 1px solid #d8d2c0; color: #5a4f2a; }
.stempel.goedgekeur { background: #eaf3ea; border-color: #c3ddc3; color: #2f5330; }
.stempel .fyn { font-weight: 400; color: #6b6b6b; }

section { margin: 0 0 22px; }
h2 { font-family: "Segoe UI", Arial, sans-serif; font-size: 13.5pt; font-weight: 600;
     margin: 26px 0 7px; page-break-after: avoid; }
p { margin: 0 0 10px; }
ul { margin: 4px 0 10px; padding-left: 22px; }
li { margin-bottom: 5px; }

/* The intuition layer must be unmistakable at a glance. */
.eli10 { border-left: 3px solid #8a9ab0; background: #f4f6f9;
         padding: 11px 15px 6px; margin: 4px 0 18px; page-break-inside: avoid; }
.eli10 .etiket { font-family: "Segoe UI", Arial, sans-serif; font-size: 8.5pt;
                 font-weight: 600; letter-spacing: .09em; text-transform: uppercase;
                 color: #4a5b70; margin-bottom: 5px; }
.eli10 p { font-size: 11.5pt; margin-bottom: 6px; }

/* A reading is the object of study, not an explanation of one. The label says so
   without changing how the prose itself is set. */
.etiket-lees { font-family: "Segoe UI", Arial, sans-serif; font-size: 8pt;
               font-weight: 600; letter-spacing: .09em; text-transform: uppercase;
               color: #6b6152; background: #f2efe8; border: 1px solid #e0d9cb;
               border-radius: 3px; padding: 2px 7px; vertical-align: middle;
               margin-left: 8px; white-space: nowrap; }

.groep { margin-top: 30px; padding-top: 14px; border-top: 1px solid #ddd;
         page-break-inside: avoid; }
.groep h2 { margin-top: 0; }
dl { margin: 0; }
dt { font-weight: 600; margin-top: 9px; }
dd { margin: 0 0 3px; }
ol { margin: 4px 0; padding-left: 22px; }
ol li { margin-bottom: 9px; }

.onbekend { border: 1px dashed #c00; padding: 9px 12px; margin: 8px 0;
            font-family: Consolas, monospace; font-size: 9.5pt; }
.bevind { page-break-before: always; }
.bevind h2 { font-size: 15pt; margin-top: 0; }
.bevind .opsom { font-style: italic; color: #444; margin: 0 0 14px; }
.bevind .telling { font-family: "Segoe UI", Arial, sans-serif; font-size: 9pt;
                   color: #555; margin: 0 0 16px; }
.vonds { border-left: 3px solid #b9552e; background: #fdf5f2; padding: 10px 14px 4px;
         margin: 0 0 13px; page-break-inside: avoid; }
.vonds.onseker { border-left-color: #a07a1e; background: #fdf9ef; }
.vonds.oortollig { border-left-color: #7a7a7a; background: #f6f6f6; }
.vonds .etiket { font-family: "Segoe UI", Arial, sans-serif; font-size: 8.5pt;
                 font-weight: 600; letter-spacing: .08em; text-transform: uppercase;
                 color: #8a3d1d; margin-bottom: 4px; }
.vonds.onseker .etiket { color: #7a5c14; }
.vonds.oortollig .etiket { color: #5a5a5a; }
.vonds p { font-size: 11pt; margin: 0 0 6px; }
.vonds .waar { font-family: "Segoe UI", Arial, sans-serif; font-size: 8.5pt;
               color: #666; }
.vonds .bron { font-size: 9.5pt; color: #555; }
.skoon { background: #f2f7f2; border-left: 3px solid #7fa87f; padding: 10px 14px;
         margin: 0 0 13px; font-size: 11pt; }
footer { margin-top: 34px; padding-top: 9px; border-top: 1px solid #ddd;
         font-family: "Segoe UI", Arial, sans-serif; font-size: 8.5pt; color: #777; }
"""


def e(s):
    return html.escape(str(s if s is not None else ""))


def paragrawe(teks):
    """Split prose into paragraphs on blank lines; single newlines are not breaks."""
    dele = [d.strip() for d in str(teks or "").split("\n\n")]
    return "".join(f"<p>{e(d)}</p>" for d in dele if d)


def verslae_langs(les_pad):
    """Any checker reports sitting beside this lesson.

    Present for a draft under review, absent for an approved lesson — so the
    appendix appears exactly where it is useful and the approved reading copy stays
    a clean lesson.
    """
    if not les_pad:
        return {}
    uit = {}
    for naam in ("feite", "dekking"):
        pad = les_pad[:-len(".json")] + f".{naam}.json"
        if os.path.exists(pad):
            try:
                uit[naam] = P.lees_json(pad)
            except (OSError, ValueError):
                pass
    return uit


def bevindings_html(verslae):
    """The findings a person needs at sign-off, and only those.

    Confirmed claims are counted, not listed: thirty-eight lines of "verified"
    teaches a reader to skim, and skimming is how the one contradicted claim gets
    missed. What is contradicted, unsettled, missing or unasked-for is shown in
    full, with its correction and its source, because the reasoning is the part a
    person has to weigh. A checker's reasoning can be wrong in ways nothing else in
    this pipeline can catch, and that only gets caught if it is read.
    """
    if not verslae:
        return ""
    dele = ['<div class="bevind"><h2>Nasienbevindings</h2>']

    f = verslae.get("feite")
    if f:
        items = f.get("items", [])
        tel = {k: sum(1 for i in items if i.get("status") == k)
               for k in ("bevestig", "weerspreek", "onseker")}
        dele.append(f'<p class="opsom">Feite: {e(f.get("opsomming"))}</p>')
        dele.append(f'<p class="telling">{len(items)} bewerings nagegaan &middot; '
                    f'{tel["bevestig"]} bevestig &middot; {tel["weerspreek"]} weerspreek '
                    f'&middot; {tel["onseker"]} onseker</p>')
        for i in items:
            st = i.get("status")
            if st not in ("weerspreek", "onseker"):
                continue
            klas = "vonds onseker" if st == "onseker" else "vonds"
            etiket = "Onseker" if st == "onseker" else "Weerspreek"
            dele.append(f'<div class="{klas}"><div class="etiket">{etiket}'
                        f'{" &middot; " + e(i["tipe"]) if i.get("tipe") else ""}</div>')
            dele.append(f'<p>{e(i.get("bewering"))}</p>')
            dele.append(f'<p class="waar">in: {e(i.get("blok"))}</p>')
            if i.get("regstelling"):
                dele.append(f'<p><strong>Regstelling:</strong> {e(i["regstelling"])}</p>')
            if i.get("bron"):
                dele.append(f'<p class="bron">{e(i["bron"])}</p>')
            dele.append("</div>")
        if not tel["weerspreek"] and not tel["onseker"]:
            dele.append('<div class="skoon">Geen feitefoute en niks onseker nie.</div>')

    d = verslae.get("dekking")
    if d:
        dele.append(f'<p class="opsom">Dekking: {e(d.get("opsomming"))}</p>')
        gebrek = [i for i in d.get("items", [])
                  if i.get("status") in ("gedeeltelik", "afwesig")]
        for i in gebrek:
            dele.append(f'<div class="vonds"><div class="etiket">'
                        f'{e(i.get("status"))} &middot; {e(i.get("tipe"))}</div>')
            dele.append(f'<p>{e(i.get("verwysing"))}</p>')
            if i.get("aksie"):
                dele.append(f'<p><strong>Aksie:</strong> {e(i["aksie"])}</p>')
            dele.append("</div>")
        if not gebrek:
            dele.append('<div class="skoon">Alles wat die spesifikasie vra is '
                        'teenwoordig.</div>')
        # The mirror question: content nothing asked for. Not a defect — a decision.
        for o in (d.get("oortollig") or []):
            dele.append('<div class="vonds oortollig"><div class="etiket">'
                        'Niks vra hiervoor nie</div>')
            dele.append(f'<p>{e(o.get("inhoud"))}</p>')
            dele.append(f'<p class="waar">in: {e(o.get("blok"))}</p>')
            if o.get("waarom"):
                dele.append(f'<p class="bron">{e(o["waarom"])}</p>')
            dele.append("</div>")

    dele.append("</div>")
    return "".join(dele)


def bou_html(les, verslae=None):
    blokke = les.get("blokke", [])

    # Each intuition block belongs beside the concept it explains, so index them by
    # the heading they point at rather than leaving them where they fall.
    eli_vir = {}
    los_eli = []
    koppe = {(b.get("kop") or "").strip() for b in blokke
             if b.get("tipe") in ("studie", "leesstuk")}
    for b in blokke:
        if b.get("tipe") != "eli10":
            continue
        vir = (b.get("vir") or "").strip()
        if vir and vir in koppe:
            eli_vir.setdefault(vir, []).append(b)
        else:
            # No target, or one that matches no heading. Show it at the end rather
            # than dropping it — a reviewer needs to see an orphaned block.
            los_eli.append(b)

    def eli_blok(b):
        return (f'<div class="eli10"><div class="etiket">Verduidelik eenvoudig</div>'
                f'{paragrawe(b.get("teks"))}</div>')

    lyf, woordelys, vrae = [], [], []
    for b in blokke:
        t = b.get("tipe")
        if t == "eli10":
            continue
        elif t in ("studie", "leesstuk"):
            # A leesstuk is the text a learner reads rather than an explanation of
            # one, but on the page it is still a heading and its prose. It carries a
            # label so a reader can tell the two apart at a glance.
            kop = (b.get("kop") or "").strip()
            if t == "leesstuk":
                lyf.append(f'<h2>{e(kop)} <span class="etiket-lees">Leesstuk</span></h2>')
            else:
                lyf.append(f"<h2>{e(kop)}</h2>")
            lyf.append(paragrawe(b.get("teks")))
            for eb in eli_vir.get(kop, []):
                lyf.append(eli_blok(eb))
        elif t == "lys":
            items = "".join(f"<li>{e(i)}</li>" for i in b.get("items", []))
            lyf.append(f"<h2>{e(b.get('kop'))}</h2><ul>{items}</ul>")
        elif t == "begrip":
            woordelys.append(f"<dt>{e(b.get('term'))}</dt><dd>{e(b.get('teks'))}</dd>")
        elif t == "vraag":
            vrae.append(f"<li>{e(b.get('teks'))}</li>")
        else:
            # Never drop a block silently: a block type this tool does not know
            # about is exactly what a reviewer needs to see.
            lyf.append(f'<div class="onbekend">Onbekende bloktipe "{e(t)}": '
                       f'{e(b)[:400]}</div>')

    for eb in los_eli:
        lyf.append(eli_blok(eb))
    if woordelys:
        lyf.append(f'<div class="groep"><h2>Woordelys</h2><dl>{"".join(woordelys)}</dl></div>')
    if vrae:
        lyf.append(f'<div class="groep"><h2>Vrae</h2><ol>{"".join(vrae)}</ol></div>')

    status = (les.get("status") or "konsep").lower()
    woord, fyn = STATUS_WOORDE.get(status, (status.upper(), ""))
    klas = "stempel goedgekeur" if status == "goedgekeur" else "stempel"
    plek = " &middot; ".join(filter(None, [
        f"Graad {e(les.get('graad'))}", e(les.get("vak")),
        e(les.get("kaps_onderwerp"))]))

    return f"""<!doctype html>
<html lang="af"><head><meta charset="utf-8">
<title>{e(les.get('titel'))}</title><style>{CSS}</style></head><body>
<header>
  <h1>{e(les.get('titel'))}</h1>
  <div class="plek">{plek}</div>
  <div class="plek">CAPS: {e(les.get('kaps_punt'))}</div>
  <div class="{klas}">{e(woord)} <span class="fyn">&nbsp;{e(fyn)}</span></div>
</header>
{''.join(lyf)}
{bevindings_html(verslae or {})}
<footer>Leeskopie vir nasien. Die bladsy wat leerders sien, word deur die
HTML-span uitgelê; hierdie dokument is net om die les te lees en te beoordeel.</footer>
</body></html>"""


def blaaiers():
    """Every browser on this machine that can print to PDF, in preference order.

    All of them, not just the first: one installation can be present but refuse to
    run headless, and falling through to the next is the difference between a PDF
    and a dead end.
    """
    gevind = [b for b in BROWSERS if os.path.exists(b)]
    for naam in ("msedge", "chrome"):
        pad = shutil.which(naam)
        if pad and pad not in gevind:
            gevind.append(pad)
    return gevind


def kontroleer_pdf(uit_pdf):
    """Refuse a PDF a reader would see as broken, and say so loudly.

    Drico, 18 September 2026: text must never be printed over other text. Two
    things are checked on the finished file: (1) words whose boxes overlap on the
    page, and (2) the renderer's own "unknown block type" box, which put raw code
    where a story should be in 14 Grade 4 Life Skills copies that nobody opened.
    A bad file is renamed to *.STUKKEND.pdf so it cannot be mistaken for a good one.
    """
    try:
        import pymupdf
    except ImportError:
        print("  (PDF check skipped: pymupdf is not installed)")
        return
    doc = pymupdf.open(uit_pdf)
    probleme = []
    for pn, page in enumerate(doc):
        if "Onbekende bloktipe" in page.get_text():
            probleme.append(f"page {pn + 1}: a block could not be rendered (raw code shown)")
        woorde = [(pymupdf.Rect(w[:4]), w[4]) for w in page.get_text("words")]
        for i in range(len(woorde)):
            a, ta = woorde[i]
            for b, tb in woorde[i + 1:i + 400]:
                x = a & b
                if not x.is_empty and x.width > 1.5 and x.height > 0.5 * min(a.height, b.height):
                    probleme.append(f"page {pn + 1}: '{ta}' overlaps '{tb}'")
                    break
            if len(probleme) > 5:
                break
    doc.close()
    if probleme:
        stukkend = uit_pdf[:-4] + ".STUKKEND.pdf"
        os.replace(uit_pdf, stukkend)
        raise SystemExit("The PDF came out wrong and was NOT kept:\n  " +
                         "\n  ".join(probleme[:6]) + f"\nInspect: {stukkend}")


def maak_pdf(html_teks, uit_pdf):
    keuses = blaaiers()
    werk = os.path.join(P.skrapruimte(), "leeskopie")
    os.makedirs(werk, exist_ok=True)
    tmp_html = os.path.join(werk, os.path.basename(uit_pdf)[:-4] + ".html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html_teks)
    os.makedirs(os.path.dirname(uit_pdf), exist_ok=True)

    if not keuses:
        raise SystemExit(
            f"No Edge or Chrome found, so no PDF could be made.\n"
            f"The readable HTML is at {tmp_html}\n"
            f"Open it in any browser and print to PDF.")

    # Clear the target first. The success test below is "a PDF is now there", and a
    # leftover from an earlier run passes that test without the browser writing a
    # thing — so a failed render used to report success and quietly ship the previous
    # version. That is how a renderer bug survived a full re-export: every reading
    # lesson kept its stale PDF and nothing said so.
    if os.path.exists(uit_pdf):
        try:
            os.remove(uit_pdf)
        except OSError as ex:
            raise SystemExit(f"Could not clear the old PDF at {uit_pdf}: {ex}\n"
                             f"Close it if it is open, then run again.")

    probeer = []
    for i, blaaier in enumerate(keuses):
        for kop in ("--headless=new", "--headless"):
            # A separate profile per browser: never touch the real one.
            profiel = os.path.join(werk, f"profiel{i}")
            cmd = [blaaier, kop, "--disable-gpu", "--no-first-run",
                   "--no-default-browser-check", f"--user-data-dir={profiel}",
                   f"--print-to-pdf={uit_pdf}", "--no-pdf-header-footer",
                   "file:///" + tmp_html.replace("\\", "/")]
            try:
                r = subprocess.run(cmd, capture_output=True, text=True,
                                   errors="replace", timeout=120)
                fout = (r.stderr or r.stdout or "").strip()[-200:]
            except (OSError, subprocess.TimeoutExpired) as ex:
                fout = str(ex)[:200]
            if os.path.exists(uit_pdf) and os.path.getsize(uit_pdf) > 800:
                kontroleer_pdf(uit_pdf)
                return uit_pdf
            probeer.append(f"  {os.path.basename(blaaier)} {kop}: {fout or 'no output'}")

    raise SystemExit("No browser produced a PDF. Tried:\n" + "\n".join(probeer) +
                     f"\nThe readable HTML is at {tmp_html} — open it and print to PDF.")


def lesindeks(graad, vak):
    """Drico's lesson numbers and his own CAPS labels, if a file exists for this
    subject and grade. Returns a dict keyed by (subonderwerp, lesson number).

    Why this exists: he indexes the output folder by HIS numbering so he can see at
    a glance that everything CAPS mentions is present. The numbers run continuously
    through the year -- Gr 4 NWT Term 1 is lessons 1 to 8, so Term 2 starts at 9 --
    and the order follows his term plan rather than the order lessons get finished.

    He used to rename every file by hand, which went wrong the ordinary way: a
    lesson gets revised three or four times before it is final, so his copies went
    stale and four of six were behind at one point. Reading the index here means the
    tool emits the name he wants on every rebuild.
    """
    pad = os.path.join(P.REPO, "kaps", "lesindeks", f"gr{int(graad)}-{P.slug(vak)}.json")
    if not os.path.exists(pad):
        return {}
    d = P.lees_json(pad)
    # Keyed on the sub-topic SLUG, which is the lesson's folder name, not on any
    # field inside the lesson. A lesson carries kaps_onderwerp, and a Technology
    # lesson correctly puts the CAPS strand there ("Tegnologie: Strukture") rather
    # than its sub-topic -- the same trap that once made two lessons overwrite each
    # other's PDF. The folder is written by paaie and is always the sub-topic.
    return {(P.slug(e["subonderwerp"]), int(e["les"])): e for e in d.get("lesse", [])}


def uitvoer_pad(les, pad):
    """Where a reading copy goes: sorted into folders by grade and subject.

    CHANGED 2026-08-21 on Drico's instruction. These used to sit in one flat
    folder with the grade and subject encoded in the filename. That reads fine at
    five files and badly at four hundred, so the folder now carries grade and
    subject and the filename carries topic and lesson number.

    The topic part comes from the lesson's own FOLDER, not from kaps_onderwerp. The
    folder is the canonical sub-topic slug written by paaie, so it is always the
    thing that distinguishes one lesson from another. kaps_onderwerp cannot do that
    job: a Technology lesson correctly sets it to the CAPS strand, which every
    Technology sub-topic in a term shares, and that silently overwrote one lesson
    with another.
    """
    graad = f"gr{les.get('graad')}"
    vak = P.slug(les.get("vak") or "vak")
    gids = os.path.basename(os.path.dirname(os.path.abspath(pad)))
    onderwerp = P.slug(gids) if gids else P.slug(les.get("kaps_onderwerp") or "onderwerp")
    stam = os.path.splitext(os.path.basename(pad))[0]

    # Prefer Drico's numbering and label when the index knows this lesson. Fall back
    # to the slug name otherwise -- a subject with no index (maths, so far) must still
    # produce a file rather than an error.
    indeks = lesindeks(les.get("graad"), les.get("vak") or "")
    sub = onderwerp
    nommer = None
    try:
        nommer = int(str(stam).split("-")[-1])
    except ValueError:
        pass
    inskrywing = indeks.get((sub, nommer))
    if inskrywing:
        naam = f"{int(inskrywing['nommer'])}_{inskrywing['etiket']}.pdf"
    else:
        naam = f"{onderwerp}-{stam}.pdf"
    return os.path.join(LEES, graad, vak, naam)


def een(pad):
    les = P.lees_json(pad)
    uit = uitvoer_pad(les, pad)
    os.makedirs(os.path.dirname(uit), exist_ok=True)
    # The appendix is for a person weighing a draft, never for a reader of an
    # approved lesson. This function used to attach it whenever the report files
    # happened to sit beside the lesson, so approved lessons went out to the
    # language checker and the HTML team carrying our own review notes - including,
    # on 23 September 2026, notes describing an eli10 block that had just been
    # deleted. The docstring above verslae_langs said all along that it should be
    # absent for an approved lesson; it simply was not implemented.
    verslae = {} if les.get("status") == "goedgekeur" else verslae_langs(pad)
    maak_pdf(bou_html(les, verslae), uit)
    print(f"  {les.get('titel','(sonder titel)')[:46]:48} {P.rel(uit)}")
    return uit


def verifieer(paaie, begin):
    """Prove the export matches the approved lessons. Returns a list of problems.

    WHY THIS EXISTS. The export folder is gitignored, so nothing versions it and
    nothing notices a loss: a PDF that was never made and one that vanished look
    identical, and both look identical to one that is three weeks stale. On
    2026-09-09 the folder held 37 Life Skills PDFs and later held 8, and because
    the run had been checked by counting rather than by verifying, the gap was
    found by accident. A count is not a check.

    So this asks the only question that matters for the deliverable: does every
    APPROVED lesson have a file that this run actually wrote?

    Three failures, and the middle one is the quiet one:

      missing    an approved lesson has no file at all
      stale      the file predates this run, so nothing was written for it now --
                 this is what a silently failed render looks like
      collision  two lessons resolve to one output name, so one overwrote the
                 other and a lesson is gone with no error anywhere. The naming
                 code already carries a comment about having done exactly this
                 once, which is reason enough to test for it rather than trust it.

    Drafts are exported too but only approved lessons are held to this: a draft
    is working material, and the folder that goes to the language checker is not.
    """
    probleme = []
    verwag = {}

    for p in paaie:
        try:
            les = P.lees_json(p)
        except Exception as e:                       # unreadable is its own answer
            probleme.append(f"could not read {P.rel(p)}: {e}")
            continue
        uit = uitvoer_pad(les, p)
        verwag.setdefault(uit, []).append((p, (les.get("status") or "").lower()))

    for uit, bronne in sorted(verwag.items()):
        if len(bronne) > 1:
            noem = ", ".join(P.rel(b) for b, _ in bronne)
            probleme.append(f"COLLISION  {len(bronne)} lessons share one output name\n"
                            f"             {P.rel(uit)}\n"
                            f"             {noem}\n"
                            f"             Only the last one survives; the rest are lost.")

    goedgekeur = [(uit, b) for uit, bronne in verwag.items()
                  for b, s in bronne if s == "goedgekeur"]
    for uit, bron in sorted(goedgekeur):
        if not os.path.exists(uit):
            probleme.append(f"MISSING    {P.rel(bron)}\n             expected {P.rel(uit)}")
        elif os.path.getsize(uit) < 4096:
            probleme.append(f"EMPTY      {P.rel(uit)} is {os.path.getsize(uit)} bytes")
        elif os.path.getmtime(uit) < begin:
            probleme.append(f"STALE      {P.rel(uit)}\n"
                            f"             left over from an earlier run; nothing was "
                            f"written for {P.rel(bron)} now")

    # Count the approved lessons that are actually sound rather than subtracting
    # problems from the total: a collision is one problem naming several lessons,
    # so subtraction would report a number that is not the number of good files.
    slegte_bronne = {ln.split()[-1] for pr in probleme for ln in pr.splitlines()
                     if ln.strip().startswith(("MISSING", "EMPTY", "STALE"))}
    goed = sum(1 for uit, _ in goedgekeur
               if os.path.exists(uit) and os.path.getsize(uit) >= 4096
               and os.path.getmtime(uit) >= begin)
    print(f"  approved lessons: {len(goedgekeur)}   "
          f"files written by this run: {goed}   "
          f"problems: {len(probleme)}")
    return probleme


def main():
    ap = argparse.ArgumentParser(description="Make a readable PDF of a lesson")
    ap.add_argument("lesson", nargs="?", help="path to a lesson JSON")
    ap.add_argument("--vak")
    ap.add_argument("--graad", type=int)
    ap.add_argument("--subonderwerp")
    ap.add_argument("--les", type=int)
    ap.add_argument("--alles", action="store_true",
                    help="every draft and every approved lesson")
    a = ap.parse_args()

    paaie = []
    if a.lesson:
        paaie = [a.lesson]
    elif a.alles:
        paaie = sorted(glob.glob(os.path.join(P.KONSEPTE, "**", "les-*.json"),
                                recursive=True))
        paaie = [p for p in paaie if os.sep + "spek" + os.sep not in p
                 and not os.path.basename(p).count(".") > 1]
    elif a.vak and a.graad and a.subonderwerp and a.les:
        p = P.les_konsep(a.graad, a.vak, a.subonderwerp, a.les)
        paaie = [p]
    else:
        ap.error("give a lesson file, or --vak --graad --subonderwerp --les, or --alles")

    if not paaie:
        print("\nNo lessons found.\n")
        return 1

    # A second's grace: a file written in the same second the run starts can carry
    # an mtime a hair below it on some filesystems, and a false stale report would
    # train people to ignore the check.
    begin = time.time() - 1

    print()
    gedoen = []
    for p in paaie:
        if not os.path.exists(p):
            print(f"  missing: {P.rel(p)}")
            continue
        een(p)
        gedoen.append(p)
    print()

    if not a.alles:
        return 0

    # --alles is the one that builds the deliverable, so it is the one that has to
    # prove it built it. A single-lesson run is a person looking at one thing.
    probleme = verifieer(gedoen, begin)
    if probleme:
        print()
        print("  THE EXPORT DOES NOT MATCH THE APPROVED LESSONS")
        print("  " + "-" * 44)
        for pr in probleme:
            print(f"  {pr}")
        print()
        print("  Do not send this folder anywhere until these are resolved.")
        print()
        return 1
    print("  Every approved lesson has a file written by this run.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

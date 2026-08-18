#!/usr/bin/env python3
"""
Wolkskool profiler — the only component permitted to read a textbook.

Emits NUMBERS. No prose from the book is written to any output file.

It is given the CAPS sub-topic labels and finds where each one begins in the
book, so the structure comes from CAPS and only the page counts and word volumes
come from the textbook. It does not discover or record the book's own
organisation.

USAGE
    python3 profiler.py book.pdf --caps caps_subtopics.json --out gr4-sw.json
    python3 profiler.py book.pdf --caps caps.json --out c.json --first 120 --last 160

caps_subtopics.json:
    {
      "vak": "Sosiale Wetenskappe",
      "graad": 4,
      "kwartaal": 3,
      "kaps_onderwerp": "Vervoer oor tyd heen",
      "subonderwerpe": ["Vervoer op land", "Gevallestudie: uitlaatgasse in 'n groot stad",
                        "Vervoer op water", "Vervoer in die lug"]
    }

OUTPUT: a profiler config consumed by the planner and the gate — per sub-topic
page counts and word volumes, plus register statistics for the grade band.

SCRATCH SPACE
    Rasterising pages writes hundreds of temporary PNG and TSV files per run.
    They go to --skrapruimte, or $WOLKSKOOL_SCRATCH, or the default below — never
    inside the repository and never inside a synced folder such as OneDrive.
"""
import argparse, csv, glob, json, os, re, shutil, statistics as st, subprocess, sys, tempfile

# Default scratch root. Overridden by --skrapruimte or $WOLKSKOOL_SCRATCH.
# Forward slashes are accepted on Windows: C:/temp/wolkskool-scratch is the same
# location as C:\temp\wolkskool-scratch.
DEFAULT_SCRATCH = "C:/temp/wolkskool-scratch" if os.name == "nt" else "/tmp/wolkskool-scratch"


def scratch_root(explicit=None):
    """Where rasterised pages and OCR intermediates go.

    Never the repository (a stray PNG of a textbook page is exactly what the
    copyright discipline exists to prevent) and never a synced folder, because
    hundreds of temp files per run will be uploaded before they are deleted.
    """
    root = explicit or os.environ.get("WOLKSKOOL_SCRATCH") or DEFAULT_SCRATCH
    os.makedirs(root, exist_ok=True)
    return root

try:
    import pyphen
    _DIC = pyphen.Pyphen(lang='af')
except Exception:
    _DIC = None

HEADING_HEIGHT_FACTOR = 1.15   # a heading's glyphs run taller than body text
HEADING_PERCENTILE = 0.90
BLOCK_GAP_FACTOR = 2.5         # lines closer than this multiple of glyph height are one heading
MIN_CONF = 40


def syllables(w):
    if _DIC is None:
        return max(1, len(re.findall(r'[aeiouyäëïöüáéíóú]+', w.lower())))
    return max(1, len(_DIC.inserted(w).split('-')))


def norm(s):
    """Loose key for matching a page heading against a CAPS label."""
    s = re.sub(r"\([^)]*\)", " ", s.lower())
    s = re.sub(r"[^a-zà-ÿ\s]", " ", s)
    drop = {"die", "n", "en", "van", "of", "in", "op", "'n"}
    return {w[:5] for w in s.split() if len(w) > 2 and w not in drop}


def page_words(rows):
    """Body-text word count for one page, excluding probable furniture."""
    text = " ".join(t for _, t, _ in rows)
    kept = []
    for tok in re.findall(r"[A-Za-zÀ-ÿ']+", text):
        if len(tok) > 1:
            kept.append(tok)
    return kept


def ocr_page(pdf, n, dpi, workdir):
    stem = os.path.join(workdir, f"p{n:04d}")
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", str(n), "-l", str(n),
                    pdf, stem], check=True, capture_output=True)
    pngs = sorted(glob.glob(stem + "*.png"))
    if not pngs:
        return None
    png = pngs[0]
    subprocess.run(["tesseract", png, png[:-4], "-l", "afr", "--psm", "3", "tsv"],
                   check=True, capture_output=True)
    tsv = png[:-4] + ".tsv"
    rows = []
    with open(tsv, encoding="utf-8", errors="ignore") as fh:
        for r in csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE):
            if r.get("level") != "5":
                continue
            try:
                h = int(r["height"]); conf = float(r["conf"]); top = int(r["top"])
            except (TypeError, ValueError):
                continue
            t = (r.get("text") or "").strip()
            if t and conf > MIN_CONF:
                rows.append((h, t, top))
    for f in glob.glob(stem + "*"):
        os.remove(f)
    return rows


def headings(rows):
    """Heading strings on a page: individual lines and contiguous blocks.

    Headings wrap, and a section banner can run to four lines ("Gevallestudie: /
    Omgewingskade: / uitlaatgasse in / 'n groot stad"). Testing single lines alone
    misses those sections entirely. Contiguous lines are therefore also joined
    into blocks — but only contiguous ones: joining every heading on a page
    invents word combinations that never appeared together and produces false
    section starts.
    """
    if not rows:
        return []
    hs = sorted(h for h, _, _ in rows)
    cut = hs[int(len(hs) * HEADING_PERCENTILE)] * HEADING_HEIGHT_FACTOR
    big = sorted([(top, h, t) for h, t, top in rows if h >= cut])
    if not big:
        return []

    # collapse tokens sharing a baseline into lines
    lines, cur, cur_h, last = [], [], 0, None
    for top, h, t in big:
        if last is not None and abs(top - last) > max(8, h * 0.6):
            lines.append((last, cur_h, " ".join(cur))); cur, cur_h = [], 0
        cur.append(t); cur_h = max(cur_h, h); last = top
    if cur:
        lines.append((last, cur_h, " ".join(cur)))

    out = [t for _, _, t in lines]

    # join vertically adjacent lines into blocks
    block, btop, bh = [], None, 0
    for top, h, t in lines:
        gap = top - btop if btop is not None else 0
        if block and gap > max(bh, h) * BLOCK_GAP_FACTOR:
            if len(block) > 1:
                out.append(" ".join(block))
            block, bh = [], 0
        block.append(t); btop, bh = top, max(bh, h)
    if len(block) > 1:
        out.append(" ".join(block))

    return out


def profile(pdf, caps, dpi, first, last, verbose, end_marker=None, scratch=None):
    total = int(re.search(r"Pages:\s+(\d+)",
                subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    first = first or 1
    last = min(last or total, total)

    labels = caps["subonderwerpe"]
    keys = [norm(x) for x in labels]
    starts = {}
    per_page = {}
    per_page_headings = {}

    work = tempfile.mkdtemp(prefix="prof-", dir=scratch_root(scratch))
    if verbose:
        print(f"  scratch: {work}", file=sys.stderr)
    try:
        for n in range(first, last + 1):
            rows = ocr_page(pdf, n, dpi, work)
            if rows is None:
                continue
            words = page_words(rows)
            per_page[n] = words
            per_page_headings[n] = headings(rows)
            # Match each heading line on its own. Joining all headings on a page
            # into one string was tried and rejected: it invents word combinations
            # that never appeared together and produces false section starts.
            for hd in headings(rows):
                hk = norm(hd)
                if not hk:
                    continue
                for i, k in enumerate(keys):
                    if not k or i in starts:
                        continue
                    # match when the heading carries most of the label's
                    # distinctive words
                    need = max(2, len(k) - 1)
                    if len(hk & k) >= need:
                        starts[i] = n
                        if verbose:
                            print(f"  page {n}: start of '{labels[i]}'", file=sys.stderr)
            if verbose and n % 10 == 0:
                print(f"  ...{n}/{last}", file=sys.stderr)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    # --- derive contiguous page ranges from the start pages ---
    # Every section is bounded by the next one's start. The LAST section has no
    # following marker, so it would silently swallow every page up to --last.
    # An end marker (the heading that follows the topic) bounds it properly.
    end_page = last
    if end_marker:
        ek = norm(end_marker)
        for n in sorted(per_page_headings):
            if n > (max(starts.values()) if starts else 0):
                for hd in per_page_headings[n]:
                    if len(norm(hd) & ek) >= max(2, round(len(ek) * 0.7)):
                        end_page = n - 1
                        break
                if end_page != last:
                    break

    found = sorted(starts.items(), key=lambda kv: kv[1])
    ranges, unbounded = {}, None
    for j, (i, start) in enumerate(found):
        if j + 1 < len(found):
            end = found[j + 1][1] - 1
        else:
            end = end_page
            if not end_marker:
                unbounded = labels[i]
        ranges[labels[i]] = (start, end)

    # --- volumes ---
    counts = [len(w) for w in per_page.values() if len(w) > 20]
    wpp = st.median(counts) if counts else 0
    subs = {}
    for label, (a, b) in ranges.items():
        pages = b - a + 1
        words = sum(len(per_page.get(p, [])) for p in range(a, b + 1))
        subs[label] = {"eerste_bladsy": a, "laaste_bladsy": b, "bladsye": pages,
                       "woorde": words,
                       "woorde_per_bladsy": round(words / pages) if pages else 0}

    # --- register statistics over the profiled range ---
    allw = [w for ws in per_page.values() for w in ws]
    reg = {}
    if allw:
        sylls = [syllables(w) for w in allw]
        reg = {"woorde_gemeet": len(allw),
               "gem_letters_per_woord": round(st.mean([len(w) for w in allw]), 2),
               "gem_sillabes_per_woord": round(st.mean(sylls), 2),
               "pct_3plus_sillabes": round(100 * sum(1 for s in sylls if s >= 3) / len(sylls), 1),
               "pct_woorde_oor_10_letters": round(100 * sum(1 for w in allw if len(w) > 10) / len(allw), 1)}

    missing = [labels[i] for i in range(len(labels)) if i not in starts]

    return {
        "vak": caps["vak"], "graad": caps["graad"], "kwartaal": caps.get("kwartaal"),
        "kaps_onderwerp": caps["kaps_onderwerp"],
        "bron": {"lees_bladsye": [first, last], "dpi": dpi,
                 "nota": "Numbers only. No textbook prose is retained by this tool."},
        "woorde_per_bladsy_mediaan": wpp,
        "subonderwerpe": subs,
        "nie_gevind": missing,
        "onbegrens": unbounded,
        "register_steekproef": reg,
    }


def main():
    ap = argparse.ArgumentParser(description="Profile a textbook for volume and register")
    ap.add_argument("pdf")
    ap.add_argument("--caps", required=True, help="JSON with the CAPS sub-topic labels")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--first", type=int, default=None)
    ap.add_argument("--last", type=int, default=None)
    ap.add_argument("--eindmerker", default=None,
                    help="heading that follows the topic, used to bound the final section")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--skrapruimte", default=None,
                    help="scratch directory for rasterised pages and OCR intermediates. "
                         "Overrides $WOLKSKOOL_SCRATCH. Default: " + DEFAULT_SCRATCH)
    a = ap.parse_args()

    caps = json.load(open(a.caps, encoding="utf-8"))
    cfg = profile(a.pdf, caps, a.dpi, a.first, a.last, not a.quiet, a.eindmerker,
                  a.skrapruimte)
    json.dump(cfg, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"\nwritten: {a.out}")
    print(f"median words per page: {cfg['woorde_per_bladsy_mediaan']}")
    for label, v in cfg["subonderwerpe"].items():
        print(f"  {label[:44]:46} p{v['eerste_bladsy']}-{v['laaste_bladsy']}  "
              f"{v['bladsye']:2} pages  {v['woorde']:5} words")
    if cfg.get("onbegrens"):
        print(f"\nWARNING: '{cfg['onbegrens']}' has no end marker, so it absorbed every page "
              f"up to --last. Its page count and volume are NOT reliable. Pass --eindmerker "
              f"with the heading that follows the topic.")
    if cfg["nie_gevind"]:
        print("\nNOT FOUND — check the labels or widen the page range:")
        for m in cfg["nie_gevind"]:
            print(f"  {m}")


if __name__ == "__main__":
    main()

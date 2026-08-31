#!/usr/bin/env python3
"""
Compare the built HTML lessons against the repository and the agreed wordings.

The HTML is made from language-checked files, and the language checker edits
outside this pipeline. So the built lessons and the repository have diverged, and
the built ones are what learners read. Three things need checking, and only the
first is what anyone set out to look for:

  1. shared definitions that do not match the subject's agreed wording;
  2. definitions the language checker changed, which is new drift nobody chose;
  3. protected words it reverted -- the most dangerous, because every one of
     them reads like ordinary Afrikaans that could be improved, and because the
     list blocks never reached that checker at all.

    python bin/htmlnasien.py --html "<folder>"
"""
import argparse, html, json, os, re, sys, unicodedata

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)


def slug(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def skoon(t):
    """HTML fragment -> plain text, with the typographic quotes normalised.

    The builder emits &rsquo; where the JSON has a plain apostrophe. Comparing
    without folding that would report every Afrikaans 'n as a difference.
    """
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    t = t.replace("\u2019", "'").replace("\u2018", "'")
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    t = t.replace("\u2013", "-").replace("\u2014", "-").replace("\xa0", " ")
    return re.sub(r"\s+", " ", t).strip()


def gloss(pad):
    s = open(pad, encoding="utf-8", errors="replace").read()
    uit = {}
    for m in re.finditer(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", s, re.S):
        uit[skoon(m.group(1))] = skoon(m.group(2))
    # The two machines emit different markup for the same thing. Matching only
    # the first returned an empty word list for half the lessons, which reads as
    # "nothing to fix" rather than "not looked at".
    for m in re.finditer(r'<p class="gword">(.*?)</p>\s*<p class="gdef">(.*?)</p>', s, re.S):
        uit[skoon(m.group(1))] = skoon(m.group(2))
    return uit, s


def lesteks(rou):
    """All readable text, for looking up whether a protected word survived."""
    s = re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>", " ", rou)
    return skoon(s)


def lesindeks_pad(vak, graad):
    return os.path.join(REPO, "kaps", "lesindeks", f"gr{int(graad)}-{slug(vak)}.json")


def repo_lesse(vak, graad):
    """Year number -> the repository's copy of that lesson.

    Keyed on the subject's lesson index, because the built HTML file names carry
    the year number and a draft on disk carries only its number within its
    sub-topic. Without the index there is no mapping at all -- and this used to be
    hardcoded to Natuurwetenskappe, so pointing it at another subject's HTML would
    have compared those pages against Natuurwetenskappe's wordings and reported
    them clean.
    """
    pad = lesindeks_pad(vak, graad)
    if not os.path.exists(pad):
        sys.exit(f"there is no lesson index at {os.path.relpath(pad, REPO)}, so the "
                 f"built pages cannot be matched to lessons. Without it this tool "
                 f"would report every page clean because it found nothing to compare.")
    idx = json.load(open(pad, encoding="utf-8"))
    uit = {}
    for e in idx["lesse"]:
        p = os.path.join(REPO, "konsepte", f"gr{int(graad)}", slug(vak),
                         slug(e["subonderwerp"]), f"les-{e['les']}.json")
        if os.path.exists(p):
            uit[e["nommer"]] = json.load(open(p, encoding="utf-8"))
    return uit


def ooreengekome(vak, graad):
    """The subject's agreed wordings, found on the file's own vak/graad."""
    gids = os.path.join(REPO, "kaps")
    for naam in sorted(os.listdir(gids)):
        if not (naam.startswith("gedeelde-omskrywings") and naam.endswith(".json")):
            continue
        try:
            d = json.load(open(os.path.join(gids, naam), encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if slug(d.get("vak") or "") == slug(vak) and int(d.get("graad", -1)) == int(graad):
            return d.get("terme") or {}, naam
    return {}, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--vak", default="Natuurwetenskappe en Tegnologie")
    ap.add_argument("--graad", type=int, default=4)
    ap.add_argument("--json", action="store_true", dest="as_json")
    a = ap.parse_args()

    kanon, kanon_naam = ooreengekome(a.vak, a.graad)
    if not kanon_naam:
        sys.exit(f"no agreed-wordings file for {a.vak} Gr {a.graad} in kaps/. "
                 f"Create one (an empty `terme` is fine) before checking built pages, "
                 f"or this tool checks the shared definitions of nothing.")
    beskerm = json.load(open(os.path.join(REPO, "kaps", "beskermde-woorde.json"),
                             encoding="utf-8"))
    repo = repo_lesse(a.vak, a.graad)

    lers = {}
    for naam in os.listdir(a.html):
        m = re.match(r"(\d+)_", naam)
        # Lesson numbers start at 1. A `0_` file is an errata sheet dropped in the
        # same folder for the layout team, and reading it as a lesson reports the
        # protected words it QUOTES as words the built pages got wrong.
        if m and int(m.group(1)) > 0 and naam.lower().endswith(".html"):
            lers[int(m.group(1))] = os.path.join(a.html, naam)

    bevindings = {}
    for n in sorted(lers):
        g, rou = gloss(lers[n])
        teks = lesteks(rou)
        r = repo.get(n)
        r_gloss = {b["term"]: b.get("teks", "")
                   for b in (r or {}).get("blokke", []) if b.get("tipe") == "begrip"}

        teen_kanon, teen_repo, ontbreek = [], [], []
        for term, teks_html in g.items():
            k = kanon.get(term.lower())
            if k and k.get("omskrywing"):
                reg = k["omskrywing"]
                if k.get("voorbeelde_mag_verskil"):
                    a_ = re.split(r",?\s+soos\s+", teks_html, 1)[0].rstrip(" .,")
                    b_ = re.split(r",?\s+soos\s+", reg, 1)[0].rstrip(" .,")
                    ok = a_ == b_
                else:
                    ok = teks_html == reg
                if not ok:
                    teen_kanon.append((term, teks_html, reg))
            if term in r_gloss and r_gloss[term] != teks_html:
                if not any(t == term for t, _, _ in teen_kanon):
                    teen_repo.append((term, teks_html, r_gloss[term]))
        for term in r_gloss:
            if term not in g:
                ontbreek.append(term)

        # Only flag where a FORBIDDEN variant is actually present. Flagging the
        # mere absence of a protected word produced a page of noise: lesson 12
        # does not use 'duim' because the hardness test belongs to lesson 13, and
        # 'ander eienskappe' is absent precisely because it is the thing being
        # corrected. An absence is not a reversion.
        weg = []
        for inskrywing in beskerm.get("algemeen", []):
            hou = inskrywing["hou"]
            for verbode in inskrywing.get("nie", []):
                if re.search(rf"\b{re.escape(verbode)}\b", teks, re.I):
                    weg.append((hou, verbode, hou.lower() in teks.lower()))
        sub = None
        if r:
            for e in json.load(open(lesindeks_pad(a.vak, a.graad),
                                    encoding="utf-8"))["lesse"]:
                if e["nommer"] == n:
                    sub = slug(e["subonderwerp"])
        for inskrywing in beskerm.get("per_subonderwerp", {}).get(sub, []):
            hou = inskrywing["hou"]
            for verbode in inskrywing.get("nie", []):
                if re.search(rf"{re.escape(verbode)}", teks, re.I):
                    weg.append((hou, verbode, hou.lower() in teks.lower()))

        bevindings[n] = {"teen_kanon": teen_kanon, "teen_repo": teen_repo,
                         "ontbreek": ontbreek, "beskerm_weg": weg,
                         "terme": len(g), "leer": os.path.basename(lers[n])}

    if a.as_json:
        json.dump(bevindings, sys.stdout, ensure_ascii=False, indent=2)
        return 0

    print(f"HTML nagegaan: {len(lers)} lesse  ({a.vak}, Graad {a.graad})")
    print(f"ooreengekome bewoordings uit {kanon_naam}: {len(kanon)} terme")
    print("=" * 62)
    for n in sorted(bevindings):
        b = bevindings[n]
        tot = len(b["teen_kanon"]) + len(b["teen_repo"]) + len(b["beskerm_weg"])
        if not tot and not b["ontbreek"]:
            print(f"\n  LES {n:<3} skoon ({b['terme']} terme)")
            continue
        print(f"\n  LES {n} - {b['leer']}")
        for term, was, moet in b["teen_kanon"]:
            print(f"     [ooreengekome] {term}")
            print(f'        HTML se:  "{was}"')
            print(f'        moet wees: "{moet}"')
        for term, was, moet in b["teen_repo"]:
            print(f"     [taalnasiener het dit verander] {term}")
            print(f'        HTML se:  "{was}"')
            print(f'        bewaarplek: "{moet}"')
        for hou, verbode, ook_daar in b["beskerm_weg"]:
            merk = "ALBEI daar - kyk konteks" if ook_daar else "BESKERMDE WOORD WEG"
            print(f"     [{merk}] verbode '{verbode}' staan in die teks; behoort '{hou}' te wees")
        if b["ontbreek"]:
            print(f"     [terme in bewaarplek maar nie in HTML nie] {', '.join(b['ontbreek'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

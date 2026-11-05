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

Since 4 November 2026 it also reads the V2 delivery. Give --vak as a V2 folder name
(PSW, Kuns, NW en Teg, Geskiedenis, Geografie) and the lessons are found through
'V2 inhoud/manifest.json', whose year numbers are the ones in the V2 file names. A
file name carrying the lesson ID (`G4_GEO_07 - ...`, Drico's naming rule of 5 November
2026) or the older "Les NN" is read, so pages named either way work as they are:

    python bin/htmlnasien.py --html "<folder>" --vak Geografie --graad 4

In that mode it adds a fourth check, the one that matters most for a rebuild: every
learner string of the approved lesson must appear in the page, word for word.
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


def verbode_vorme(inskrywing):
    """The forbidden forms of one entry, minus the elements that are not forms.

    An empty string -- or one that is only whitespace -- is not a forbidden form,
    and it must never be treated as one. An empty pattern matches EVERY string,
    and an empty pattern between two word boundaries matches every string with a
    word in it, so a single such element makes its whole entry fire on every built
    lesson in its scope and name an empty word as what the page reverted to.

    A false hit here is the expensive kind. This check is the last thing standing
    between the outside language checker's edits and delivery, and nothing
    re-checks those edits; a reader who learns to scroll past a hit that is always
    there stops seeing the ones that are real.

    Three entries in kaps/beskermde-woorde.json carried one on 2 October 2026 --
    `groot` in die-aarde-en-die-son, `sedert 2001` and `gewoonlik` in
    demokrasie-en-burgerskap. Those were removed from the data the same day; this
    is here so malformed data cannot produce it again. It also reaches the entry
    that WAS live: bin/taalnasien.py printed the forbidden forms of four lessons
    with a leading empty one, straight into the block the outside checker reads.
    """
    return [v for v in (inskrywing.get("nie") or []) if str(v).strip()]


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


V2_VAKKE = ("PSW", "Kuns", "NW en Teg", "Geskiedenis", "Geografie")
MANIFES = os.path.join(REPO, "V2 inhoud", "manifest.json")


def manifes_lesse(vak, graad):
    """Year number -> (lesson, its sub-topic slug, the V2 data) for one V2 folder."""
    if not os.path.exists(MANIFES):
        sys.exit("there is no 'V2 inhoud/manifest.json'; run bin/v2_inhoud.py first.")
    uit = {}
    for e in json.load(open(MANIFES, encoding="utf-8"))["lesse"]:
        if e["vak"] != vak or int(e["graad"]) != int(graad):
            continue
        les = json.load(open(os.path.join(REPO, e["bron"]), encoding="utf-8"))
        data = json.load(open(os.path.join(REPO, "V2 inhoud", e["json"]), encoding="utf-8"))
        uit[e["nommer"]] = (les, e["bron"].split("/")[-2], data, e)
    if not uit:
        sys.exit(f"the manifest has no lessons for {vak} Gr {graad}.")
    return uit


def leerder_stukke(data):
    """Every string a learner must see on the page, from the V2 data."""
    stukke = [data.get("titel") or ""]
    for b in data.get("blokke") or []:
        if b.get("rol") != "leerder":
            continue
        for k in ("kop", "term", "teks"):
            if b.get(k):
                stukke += [x for x in b[k].split("\n") if x.strip()]
        stukke += b.get("items") or []
    return [s for s in stukke if s.strip()]


def vorm_teenwoordig(vorm, teks, hou):
    """Is a forbidden form in the text anywhere OUTSIDE the wording being kept?

    Two classes of false hit made this check unusable, and both are handled here
    rather than by trimming the data. A forbidden form that is a substring of
    another word ('kar' in 'karretjie') is not a hit, so the form must stand as
    whole words. A forbidden form that sits INSIDE the kept wording ('tekens' in
    'tekens en simptome', 'taxi' in 'minibus-taxi') is the correct wording, not a
    reversion, so every occurrence of the kept wording is blanked first.
    """
    for h in sorted({hou}, key=len, reverse=True):
        if h.strip():
            teks = re.sub(re.escape(h), " \x00 ", teks, flags=re.I)
    return re.search(rf"(?<!\w){re.escape(vorm)}(?!\w)", teks, re.I) is not None


def oor_na_goedgekeur(rou, goedgekeur):
    """The page's text with every approved element and sentence taken away.

    Element by element: a heading, term or paragraph whose text IS an approved
    string goes whole, so a two-word heading is not left behind to trip a list.
    Inside what remains, approved strings of four words or more are blanked; shorter
    ones are not, because blanking 'lug' everywhere would also blank the very word
    a changed sentence got wrong.
    """
    las = lambda t: re.sub(r"(?<=\S)- (?=\w)", "-", t)  # noqa: E731
    stel = {las(skoon(s)) for s in goedgekeur}
    lank = sorted((s for s in stel if len(s.split()) >= 4), key=len, reverse=True)
    lyf = re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>", " ", rou)
    stukke = []
    for m in re.finditer(r"(?is)<(h[1-6]|p|li|dt|dd|td|th|figcaption|summary)\b[^>]*>(.*?)</\1>", lyf):
        t = las(skoon(m.group(2)))
        if not t or t in stel:
            continue
        for s in lank:
            t = t.replace(s, " \x00 ")
        stukke.append(t)
    return " \x00 ".join(stukke)


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
    ap.add_argument("--vak", default="Natuurwetenskappe en Tegnologie",
                    help="a V2 folder name (PSW, Kuns, NW en Teg, Geskiedenis, Geografie) "
                         "or, for the old lesson-index mode, a repository subject")
    ap.add_argument("--graad", type=int, default=4)
    ap.add_argument("--json", action="store_true", dest="as_json")
    a = ap.parse_args()

    v2 = a.vak in V2_VAKKE
    if v2:
        repo = manifes_lesse(a.vak, a.graad)
        repo_vak = next(iter(repo.values()))[0].get("vak")
    else:
        repo = {n: (les, None, None, None) for n, les in repo_lesse(a.vak, a.graad).items()}
        repo_vak = a.vak
    kanon, kanon_naam = ooreengekome(repo_vak, a.graad)
    if not kanon_naam:
        sys.exit(f"no agreed-wordings file for {repo_vak} Gr {a.graad} in kaps/. "
                 f"Create one (an empty `terme` is fine) before checking built pages, "
                 f"or this tool checks the shared definitions of nothing.")
    beskerm = json.load(open(os.path.join(REPO, "kaps", "beskermde-woorde.json"),
                             encoding="utf-8"))

    lers = {}
    for naam in os.listdir(a.html):
        if not naam.lower().endswith(".html"):
            continue
        # "G4_GEO_07 - <label>.html" (the naming rule), "Les 07 - <titel>.html",
        # "Gr4 Geografie Les 07 - ...", or the old "7_<etiket>". An ID's "_00" file is
        # not a lesson, and is skipped by the same test as a `0_` file below.
        m = (re.search(r"\bG\d+_[A-Z]+_0*(\d+)[a-z]?\b", naam)
             or re.search(r"\bLes\s*0*(\d+)\b", naam) or re.match(r"(\d+)_", naam))
        # Lesson numbers start at 1. A `0_` file is an errata sheet dropped in the
        # same folder for the layout team, and reading it as a lesson reports the
        # protected words it QUOTES as words the built pages got wrong.
        if m and int(m.group(1)) > 0:
            lers[int(m.group(1))] = os.path.join(a.html, naam)

    if not v2:
        indeks = {e["nommer"]: slug(e["subonderwerp"]) for e in
                  json.load(open(lesindeks_pad(a.vak, a.graad), encoding="utf-8"))["lesse"]}

    bevindings = {}
    for n in sorted(lers):
        g, rou = gloss(lers[n])
        teks = lesteks(rou)
        r, sub, data, _ = repo.get(n) or (None, None, None, None)
        if r and not v2:
            sub = indeks.get(n)
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
        #
        # The per-sub-topic branch matched NOTHING until 4 November 2026: its
        # pattern held two literal backspace bytes where word boundaries were meant,
        # and it had been left that way because repairing the byte alone produced
        # false hits wherever a forbidden form is part of the kept wording. It now
        # runs in V2 mode only, through vorm_teenwoordig, which handles that class.
        # The rebuild check: the approved learner text, word for word, on the page.
        las = lambda t: re.sub(r"(?<=\S)- (?=\w)", "-", t)  # noqa: E731
        teks_weg = []
        if data:
            bladsy = las(teks)
            # Sentence by sentence, so a report names the sentence that differs and a
            # page may put a picture between two sentences of one paragraph.
            zinne = [z for s in leerder_stukke(data) for z in re.split(r"(?<=[.!?])\s+", s) if z.strip()]
            teks_weg = [z for z in zinne if las(skoon(z)) not in bladsy]

        weg = []
        if not data:
            # Old mode, unchanged: the general list over the whole page.
            for inskrywing in beskerm.get("algemeen", []):
                hou = inskrywing["hou"]
                for verbode in verbode_vorme(inskrywing):
                    if re.search(rf"\b{re.escape(verbode)}\b", teks, re.I):
                        weg.append((hou, verbode, hou.lower() in teks.lower()))
        elif teks_weg:
            # V2 mode. A protected word can only have been reverted in text that
            # differs from the approved lesson, and every such difference is already
            # reported above, so the lists are read only on a page that has one --
            # and only in what is left once the approved text is taken away. Run over
            # whole pages built straight from approved text, the lists fired on 300 of
            # 326: the forbidden forms are words that are right in other sentences
            # ('lug' for air, 'kleur' for colour). Here they explain a difference;
            # they never raise one on their own.
            oor = oor_na_goedgekeur(rou, leerder_stukke(data))
            inskrywings = list(beskerm.get("algemeen", [])) + \
                list(beskerm.get("per_subonderwerp", {}).get(sub, []))
            for inskrywing in inskrywings:
                hou = inskrywing["hou"]
                for verbode in verbode_vorme(inskrywing):
                    if vorm_teenwoordig(verbode, oor, hou):
                        weg.append((hou, verbode, hou.lower() in teks.lower()))

        bevindings[n] = {"teen_kanon": teen_kanon, "teen_repo": teen_repo,
                         "ontbreek": ontbreek, "beskerm_weg": weg, "teks_weg": teks_weg,
                         "terme": len(g), "leer": os.path.basename(lers[n]),
                         "onbekend": r is None}

    if a.as_json:
        json.dump(bevindings, sys.stdout, ensure_ascii=False, indent=2)
        return 0

    print(f"HTML nagegaan: {len(lers)} lesse  ({a.vak}, Graad {a.graad})")
    print(f"ooreengekome bewoordings uit {kanon_naam}: {len(kanon)} terme")
    if v2:
        sonder = sorted(set(repo) - set(lers))
        if sonder:
            print(f"in die manifes maar geen HTML nie: les {', '.join(map(str, sonder))}")
    print("=" * 62)
    for n in sorted(bevindings):
        b = bevindings[n]
        if b["onbekend"]:
            print(f"\n  LES {n} - {b['leer']}: GEEN les met hierdie nommer nie; niks nagegaan nie")
            continue
        tot = len(b["teen_kanon"]) + len(b["teen_repo"]) + len(b["beskerm_weg"]) + len(b["teks_weg"])
        if not tot and not b["ontbreek"]:
            print(f"\n  LES {n:<3} skoon ({b['terme']} terme)")
            continue
        print(f"\n  LES {n} - {b['leer']}")
        for s in b["teks_weg"]:
            print(f'     [teks nie woordeliks op die bladsy nie] "{s[:140]}"')
        for term, was, moet in b["teen_kanon"]:
            print(f"     [ooreengekome] {term}")
            print(f'        HTML se:  "{was}"')
            print(f'        moet wees: "{moet}"')
        for term, was, moet in b["teen_repo"]:
            print(f"     [anders as die bewaarplek] {term}")
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

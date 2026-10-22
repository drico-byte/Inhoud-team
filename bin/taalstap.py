#!/usr/bin/env python3
"""The language step: two agents and a script, between the gate and the checkers.

WHY IT EXISTS. Until October 2026 the Afrikaans was checked OUTSIDE this pipeline,
by ChatGPT, after the fact checker had finished. A language change that altered a
claim was then seen by nobody. On 22 October 2026 Drico compared ChatGPT with
Claude blind on three sets of six lessons; the two-step Claude check found more
faults, made fewer bad changes, flagged withdrawn safety wording and left shared
definitions alone. He moved the language check INSIDE the pipeline and BEFORE the
fact check, so the fact checker reads the final wording.

THE ORDER (bin/hardloop.py runs it):

    writer -> gate -> wolkskool-taalvinder -> wolkskool-taalkeurder
           -> this script applies what the reviewer kept -> gate again
           -> coverage and fact check -> sign-off

The finder proposes every improvement it can find; the reviewer decides each one:
HOU (applied), LAAT VAAR (not applied), NA SKRYWER (a real fault a language agent
may not fix). Only this script edits the lesson, and only with the exact
replacements the reviewer kept, located in the ORIGINAL text, never overlapping,
and never touching a protected wording or a shared definition. Nothing here is
written by hand.

    python bin/taalstap.py --les-pad konsepte/.../les-3.json

prints the last language report for a lesson. The runner does everything else.
"""
import argparse
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P          # noqa: E402
import taalnasien          # noqa: E402

# The fields of a block that hold Afrikaans a language change may touch. `term`
# (the glossary headword) is left out on purpose: a headword is a name, and a
# language change to it would split it from every lesson and sentence that uses it.
VELDE = ("kop", "teks")
BESLUITE = ("HOU", "LAAT VAAR", "NA SKRYWER")


class Ongeldig(Exception):
    """An agent's file cannot be acted on. The runner archives it and asks again.

    `wie` names the file at fault ("taalvinder" or "taalkeurder"). The runner
    archives by this, never by the message text: the first version looked for the
    word "reviewer" in the message, five of the reviewer's errors did not contain
    it, and the runner deleted the finder's good file instead -- after which the
    bad decisions were read against a new list of proposals nobody had reviewed.
    """

    def __init__(self, boodskap, wie):
        super().__init__(boodskap)
        self.wie = wie


# ------------------------------------------------------------------ inputs
def vinder_invoer(les_pad, vorige=None):
    """The block the finder reads: protected words, then the lesson.

    Built by taalnasien.bou, the same block the outside checker used to get, minus
    its instruction to an outside tool -- the agents carry their own instructions
    in prompts/. Everything from the first rule of '=' onward is kept.

    `vorige` is the report of an earlier language round on an earlier draft of this
    lesson. Its applied changes are listed so the finder does not re-propose a
    change the writer has since reverted on purpose: without it the two steps could
    fight, round after round, over one sentence.
    """
    blok = taalnasien.bou(les_pad)
    begin = blok.find("=" * 72)
    lyf = blok[begin:] if begin >= 0 else blok
    les = P.lees_json(les_pad)
    dele = [f"Graad {les.get('graad')}-les vir die taalnasien.", "", lyf]
    if vorige and vorige.get("toegepas"):
        dele += ["", "=" * 72, "VORIGE TAALRONDE (op 'n vroeer weergawe van hierdie les)", "=" * 72,
                 "Hierdie veranderings is in 'n vorige ronde aangebring. As die les nou weer die",
                 "oorspronklike woorde het, het die skrywer dit met opset teruggesit: moenie dit",
                 "weer voorstel nie.", ""]
        for r in vorige["toegepas"]:
            dele.append(f"  - '{r['voor']}' -> '{r['na']}'")
    # The dropped ones too. Without them a second round, after a writer's repair,
    # re-proposed exactly what the reviewer had rejected a round earlier (22 October
    # 2026, three lessons in one batch) -- work for the reviewer, and a chance of a
    # different verdict on the same change.
    # Every earlier round's, not just the last: a third round re-proposed what the
    # first had dropped, because the second report only knew its own.
    verwerp = (vorige or {}).get("laat_vaar_vorige", []) + (vorige or {}).get("laat_vaar", [])
    if verwerp:
        dele += ["", "=" * 72, "IN DIE VORIGE RONDES LAAT VAAR", "=" * 72,
                 "Die keurder het hierdie voorstelle in 'n vorige ronde verwerp. Moenie dit",
                 "weer voorstel nie, tensy die sin intussen verander het.", ""]
        for r in verwerp:
            dele.append(f"  - '{r.get('voor', '')}' -> '{r.get('na', '')}'")
    return "\n".join(dele)


def keurder_invoer(les_pad, voorstelle, vorige=None):
    """The reviewer's input: the same block, then the numbered proposals.

    Proposals whose original words do not occur exactly once are marked: they
    cannot be applied, so the reviewer should send a real fault among them to the
    writer rather than keep it.
    """
    les = P.lees_json(les_pad)
    dele = [vinder_invoer(les_pad, vorige), "", "", "=" * 72, "VOORGESTELDE VERANDERINGS", "=" * 72]
    for n, c in enumerate(voorstelle, 1):
        dele.append("")
        dele.append(f"{n}. [{c.get('blok', '')}] ({c.get('soort', '')})")
        dele.append(f"   voor: {c['voor']}")
        dele.append(f"   na:   {c['na']}")
        dele.append(f"   rede: {c.get('rede', '')}")
        keer = len(vind(les, c["voor"]))
        if keer != 1:
            dele.append(f"   LET WEL: die 'voor'-woorde kom {keer} keer in die les voor, so dit kan nie "
                        f"aangebring word nie. Is dit 'n regte fout, stuur dit NA SKRYWER.")
    return "\n".join(dele)


# ------------------------------------------------------------------ reading the agents' files
def _str(x):
    return x if isinstance(x, str) else ("" if x is None else str(x))


def _vlae(rou):
    """Flags as dicts of strings, whatever shape the agent wrote them in."""
    uit = []
    for v in rou if isinstance(rou, list) else []:
        if isinstance(v, dict):
            uit.append({k: _str(val) for k, val in v.items()})
        elif v is not None:
            uit.append({"teks": _str(v), "rede": ""})
    return uit


def lees_vinder(pad):
    """The finder's file: (proposals, flags, protected-word doubts, prompt version).

    Raises Ongeldig for anything the runner cannot act on, so a malformed file is
    archived and the finder asked again rather than crashing the runner on every
    run until a person deletes it.
    """
    try:
        d = P.lees_json(pad)
    except (OSError, ValueError) as e:
        raise Ongeldig(f"the finder's file is not valid JSON: {e}", "taalvinder")
    if not isinstance(d, dict):
        raise Ongeldig("the finder's file is not a JSON object", "taalvinder")
    v = d.get("veranderings")
    if not isinstance(v, list):
        raise Ongeldig("the finder's file has no 'veranderings' list", "taalvinder")
    for n, c in enumerate(v, 1):
        if not isinstance(c, dict):
            raise Ongeldig(f"proposal {n} is not an object", "taalvinder")
        if not isinstance(c.get("voor"), str) or not c["voor"].strip():
            raise Ongeldig(f"proposal {n} has no 'voor' text", "taalvinder")
        if not isinstance(c.get("na"), str):
            raise Ongeldig(f"proposal {n} has no 'na' text", "taalvinder")
    return v, _vlae(d.get("vlae")), _vlae(d.get("beskerm_bedenkings")), _str(d.get("prompt_weergawe"))


def _normaal_besluit(x):
    s = re.sub(r"[\s_-]+", " ", _str(x)).strip().upper()
    return s if s in BESLUITE else None


def lees_besluite(pad, aantal):
    """The reviewer's decisions, one per proposal, in order: (decisions, prompt version)."""
    try:
        d = P.lees_json(pad)
    except (OSError, ValueError) as e:
        raise Ongeldig(f"the reviewer's file is not valid JSON: {e}", "taalkeurder")
    if not isinstance(d, dict):
        raise Ongeldig("the reviewer's file is not a JSON object", "taalkeurder")
    b = d.get("besluite")
    if not isinstance(b, list):
        raise Ongeldig("the reviewer's file has no 'besluite' list", "taalkeurder")
    if len(b) != aantal:
        raise Ongeldig(f"{len(b)} decisions for {aantal} proposals -- one decision per "
                       f"proposal is required", "taalkeurder")
    uit = []
    for n, x in enumerate(b, 1):
        if not isinstance(x, dict):
            raise Ongeldig(f"decision {n} is not an object", "taalkeurder")
        besluit = _normaal_besluit(x.get("besluit"))
        if not besluit:
            raise Ongeldig(f"decision {n} is '{x.get('besluit')}', not one of {', '.join(BESLUITE)}", "taalkeurder")
        nr = x.get("nr")
        try:
            nr = int(nr) if nr is not None else n
        except (TypeError, ValueError):
            raise Ongeldig(f"decision {n} has the number '{nr}', which is not a number", "taalkeurder")
        if nr != n:
            raise Ongeldig(f"decision {n} is numbered {nr} -- decisions must be in order", "taalkeurder")
        uit.append({"besluit": besluit, "fout": _str(x.get("fout")), "rede": _str(x.get("rede"))})
    return uit, _str(d.get("prompt_weergawe"))


# ------------------------------------------------------------------ where things are
def _plekke(les):
    """Every editable string in the lesson: ((block, field, item), text)."""
    for i, b in enumerate(les.get("blokke", [])):
        for veld in VELDE:
            if isinstance(b.get(veld), str):
                yield (i, veld, None), b[veld]
        for j, item in enumerate(b.get("items") or []):
            if isinstance(item, str):
                yield (i, "items", j), item


def _treffers(teks, voor, hoof_maak_nie_saak=False):
    """Start positions of `voor` in `teks`, as a whole word sequence.

    A match inside a longer word does not count: 'eers' must not match 'eerste'.
    With `hoof_maak_nie_saak`, case is ignored: the protected-word guard needs it,
    because a protected 'kieme' also stands at the start of a sentence as 'Kieme'.
    """
    if hoof_maak_nie_saak:
        teks, voor = teks.lower(), voor.lower()
    uit, begin = [], 0
    while True:
        k = teks.find(voor, begin)
        if k < 0:
            return uit
        voor_ok = not (voor[0].isalnum() and k > 0 and teks[k - 1].isalnum())
        einde = k + len(voor)
        na_ok = not (voor[-1].isalnum() and einde < len(teks) and teks[einde].isalnum())
        if voor_ok and na_ok:
            uit.append(k)
        begin = k + 1


def vind(les, voor):
    """Every (place, start) where `voor` occurs in the lesson, as whole words."""
    return [(plek, k) for plek, teks in _plekke(les) for k in _treffers(teks, voor)]


def lees_voorstelle(les, voorstelle):
    """Problems worth showing the reviewer: proposals that cannot be applied as written."""
    probleme = []
    for n, c in enumerate(voorstelle, 1):
        keer = len(vind(les, c["voor"]))
        if keer != 1:
            probleme.append(f"proposal {n}: its original words occur {keer} times in the lesson "
                            f"('{c['voor'][:60]}') -- it will not be applied even if kept")
    return probleme


# ------------------------------------------------------------------ protection
def beskerming(les_pad, les):
    """What a language change may not touch, from the same sources as the input block.

    Returns (protected texts, forbidden texts, protected glossary terms). A change
    that overlaps a protected text, brings in a forbidden one, or rewrites the
    definition of a protected term is not applied: the reviewer was told so, and
    this is the check that does not depend on it remembering.
    """
    sub_gids = os.path.basename(os.path.dirname(les_pad))
    beskermd, verbode, terme = set(), set(), set()
    for w in taalnasien.beskermde_woorde(les, sub_gids) + taalnasien.spek_beskermde_woorde(les_pad):
        if not isinstance(w, dict) or w.get("reel"):
            continue  # a ruling written as prose: the agents read it, the guard cannot
        h = w.get("hou")
        if isinstance(h, str) and h.strip():
            beskermd.add(h.strip())
        nie = w.get("nie") if isinstance(w, dict) else None
        for n in ([nie] if isinstance(nie, str) else nie or []):
            if isinstance(n, str) and n.strip():
                verbode.add(n.strip())
    for t, teks, *_ in taalnasien.besliste_omskrywings(les, les.get("vak"), les.get("graad")):
        terme.add(t)
        beskermd.add(teks)
    for t, teks, _ in taalnasien.gedeelde_verklarings(les, les_pad):
        terme.add(t)
        beskermd.add(teks)
    for t, teks in taalnasien.voorgeskrewe_omskrywings(les):
        terme.add(t)
        beskermd.add(teks)
    # A protected "wording" with no letters in it is a parsing accident, not a
    # ruling: one spec stored its protected words as a single string, it was read
    # character by character, and every change containing a comma was refused.
    beskermd = {b for b in beskermd if any(ch.isalpha() for ch in b)}
    verbode = {v for v in verbode if any(ch.isalpha() for ch in v)}
    return beskermd, verbode, {t.lower() for t in terme if isinstance(t, str) and t.strip()}


def _is_definisie(les, plek, terme):
    i, veld, _ = plek
    blok = les["blokke"][i]
    return blok.get("tipe") == "begrip" and veld == "teks" and _str(blok.get("term")).lower() in terme


def _waarom_beskermd(les, plek, begin, voor, na, beskermd, verbode, terme):
    """Why a kept change may not be applied: (reason, whose) or (None, None).

    `whose` is "mens" for a decided or shared definition -- one lesson's writer
    cannot change what every lesson says -- and "skrywer" for a protected or
    forbidden wording inside this lesson, which the writer can work around.

    A change is refused only if it REMOVES a protected wording or BRINGS IN a
    forbidden one, counted as whole words in the whole string before and after,
    ignoring case. The first version refused any change whose span merely
    overlapped a protected wording, and both second-round reviewers found good
    changes refused that way: an AWS comma placed after "die President" next to
    the protected "Nasionale Vergadering", and "Die ding dra ... kieme" ->
    "Hulle dra ... kieme".
    """
    i, veld, j = plek
    blok = les["blokke"][i]
    if _is_definisie(les, plek, terme):
        return (f"it rewrites the definition of '{blok.get('term')}', which is decided or shared "
                f"across lessons; a definition changes for every lesson at once"), "mens"
    teks = blok["items"][j] if j is not None else blok[veld]
    nuut = teks[:begin] + na + teks[begin + len(voor):]
    for b in beskermd:
        if len(_treffers(nuut, b, True)) < len(_treffers(teks, b, True)):
            return (f"it changes the protected wording '{b[:60]}', which must stay as it is; "
                    f"fix the fault without changing those words"), "skrywer"
    for v in verbode:
        if len(_treffers(nuut, v, True)) > len(_treffers(teks, v, True)):
            return (f"it brings in '{v[:60]}', a wording the protected list forbids; fix the "
                    f"fault without it"), "skrywer"
    return None, None


# ------------------------------------------------------------------ applying
def woorde(les):
    """Words the gate counts against the budget: study and reading text plus list
    items, tokenised the gate's way, so the report and the gate show the same number."""
    teks = " ".join(_str(b.get("teks")) for b in les.get("blokke", [])
                    if b.get("tipe") in ("studie", "leesstuk"))
    items = " ".join(" ".join(_str(i) for i in (b.get("items") or [])) for b in les.get("blokke", [])
                     if b.get("tipe") == "lys")
    return len(re.findall(r"[A-Za-zÀ-ÿ']+", teks + " " + items))


def pas_toe(les_pad, les, voorstelle, besluite, vlae=None, beskerm=None):
    """Apply what the reviewer kept. Returns (new lesson, report).

    Every kept change is located ONCE, in the original lesson, as whole words, and
    must occur exactly once. Changes whose spans overlap are not applied. Changes
    that touch a protected wording or a shared definition become items for the
    writer. The rest are applied together, from the end of each string backwards,
    so no change is ever applied to text another change produced.
    """
    beskermd, verbode, terme = beskerming(les_pad, les)
    verslag = {"toegepas": [], "nie_toegepas": [], "laat_vaar": [], "na_skrywer": [],
               "vlae": vlae or [], "beskerm_bedenkings": beskerm or [],
               "woorde_voor": woorde(les)}
    kandidate = []
    for n, (c, b) in enumerate(zip(voorstelle, besluite), 1):
        ry = {"nr": n, "blok": _str(c.get("blok")), "voor": c["voor"], "na": c["na"],
              "soort": _str(c.get("soort")), "rede_vinder": _str(c.get("rede")),
              "fout": b["fout"], "rede_keurder": b["rede"]}
        if b["besluit"] == "LAAT VAAR":
            verslag["laat_vaar"].append(ry)
            continue
        plekke = vind(les, c["voor"])
        if b["besluit"] == "NA SKRYWER":
            # A decided or shared definition is never one lesson's writer's to change,
            # however the reviewer routed it; the reviewer prompt itself sends such
            # definitions here, so the test has to be made here too.
            if any(_is_definisie(les, pl, terme) for pl, _ in plekke):
                verslag["na_skrywer"].append(dict(ry, beskerm=True, waarom=(
                    "a decided or shared definition: it changes for every lesson at once, "
                    "so a person decides")))
            else:
                verslag["na_skrywer"].append(dict(ry, waarom="the reviewer sent it to the writer"))
            continue
        if c["na"] == c["voor"]:
            verslag["laat_vaar"].append(dict(ry, waarom="the proposal changes nothing"))
            continue
        if len(plekke) != 1:
            verslag["nie_toegepas"].append(dict(ry, waarom=(
                f"the original words occur {len(plekke)} times in the lesson, so where to "
                f"change them is not certain")))
            continue
        plek, begin = plekke[0]
        rede, wie = _waarom_beskermd(les, plek, begin, c["voor"], c["na"], beskermd, verbode, terme)
        if rede:
            verslag["na_skrywer"].append(dict(ry, waarom=f"not applied: {rede}",
                                              beskerm=(wie == "mens")))
            continue
        kandidate.append((plek, begin, begin + len(c["voor"]), ry))

    # Overlapping spans in one string: neither is applied, because applying one
    # changes the text the other was judged against.
    oorvleuel = set()
    for a in range(len(kandidate)):
        for b in range(a + 1, len(kandidate)):
            pa, sa, ea, _ = kandidate[a]
            pb, sb, eb, _ = kandidate[b]
            if pa == pb and sa < eb and sb < ea:
                oorvleuel.update((a, b))
    nuut = json.loads(json.dumps(les, ensure_ascii=False))
    toe = [k for idx, k in enumerate(kandidate) if idx not in oorvleuel]
    for idx in sorted(oorvleuel):
        verslag["nie_toegepas"].append(dict(kandidate[idx][3], waarom=(
            "it overlaps another kept change in the same sentence, so neither was applied")))
    for (i, veld, j), begin, einde, ry in sorted(toe, key=lambda k: (k[0][0], k[0][1], k[0][2] or 0, -k[1])):
        if j is None:
            t = nuut["blokke"][i][veld]
            nuut["blokke"][i][veld] = t[:begin] + ry["na"] + t[einde:]
        else:
            t = nuut["blokke"][i]["items"][j]
            nuut["blokke"][i]["items"][j] = t[:begin] + ry["na"] + t[einde:]
    verslag["toegepas"] = sorted((k[3] for k in toe), key=lambda r: r["nr"])
    verslag["nie_toegepas"].sort(key=lambda r: r["nr"])
    verslag["na_skrywer"].sort(key=lambda r: r["nr"])
    verslag["woorde_na"] = woorde(nuut)
    return nuut, verslag


# ------------------------------------------------------------------ routing
def veiligheidsvlae(verslag):
    """Flags the finder marked as withdrawn safety wording, by their `soort` field only.

    A substring test over the whole flag fired on a reason saying "geen
    veiligheidsprobleem" and on a block called "Veiligheid in die kombuis"; only the
    structured field counts.
    """
    return [v for v in verslag.get("vlae") or []
            if _str(v.get("soort")).strip().upper() == "VEILIGHEID"]


def vir_skrywer(verslag):
    """Items the WRITER can fix in this lesson, described as faults, not as wording.

    CLAUDE.md: describe the problem and let the writer choose the wording. So a
    proposal that was kept but could not be applied is handed over as its fault,
    never as a replacement to paste in.
    """
    uit = []
    for r in verslag.get("na_skrywer", []) + verslag.get("nie_toegepas", []):
        if r.get("beskerm"):
            continue
        punt = r.get("fout") or r.get("rede_keurder") or r.get("rede_vinder")
        waarom = r.get("waarom", "")
        nota = f" ({waarom[len('not applied: '):]})" if waarom.startswith("not applied: ") else ""
        uit.append(f"fix: [taal] in '{r['voor'][:70]}': {punt}{nota}")
    # The finder's flags were judged by nobody: the reviewer decides proposals, not
    # flags. They go to the writer as things to LOOK at, never as faults to fix.
    vv = veiligheidsvlae(verslag)
    for v in verslag.get("vlae") or []:
        if v not in vv and v.get("teks"):
            uit.append(f"check (the language finder raised this; it may not be a fault): "
                       f"'{v.get('teks', '')[:70]}': {v.get('rede', '')}")
    return uit


def vir_n_mens(verslag):
    """Items no single writer should settle: shared definitions and protected words."""
    uit = []
    for r in verslag.get("na_skrywer", []):
        if r.get("beskerm"):
            uit.append(f"[taal, for a person] '{r['voor'][:70]}': {r.get('waarom')}; "
                       f"the reviewer's point: {r.get('fout') or r.get('rede_keurder')}")
    for v in verslag.get("beskerm_bedenkings") or []:
        uit.append(f"[taal, protected word] '{v.get('woord', '')[:60]}': {v.get('rede', '')}")
    # A safety flag is also kept here, so it is still printed at sign-off after a
    # person cleared the escalation with --hervat.
    for v in veiligheidsvlae(verslag):
        uit.append(f"[taal, SAFETY] '{v.get('teks', '')[:70]}': {v.get('rede', '')}")
    return uit


# ------------------------------------------------------------------ the report
_CSS = """
:root{--bg:#f6f7f5;--card:#fff;--ink:#1f2622;--muted:#5d6a63;--rule:#d8ddd8;--ok:#2d6a4f;--ok-bg:#e2efe8;--warn:#8a5a00;--warn-bg:#fbefd6;--bad:#9b2c2c;--bad-bg:#f8e1e1}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#151a17;--card:#1d2420;--ink:#e4e9e5;--muted:#9caba2;--rule:#2f3a34;--ok:#7fc8a3;--ok-bg:#213229;--warn:#f0c46a;--warn-bg:#3a2e14;--bad:#f09a9a;--bad-bg:#3d1f1f;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#151a17;--card:#1d2420;--ink:#e4e9e5;--muted:#9caba2;--rule:#2f3a34;--ok:#7fc8a3;--ok-bg:#213229;--warn:#f0c46a;--warn-bg:#3a2e14;--bad:#f09a9a;--bad-bg:#3d1f1f;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:"Segoe UI",system-ui,sans-serif;font-size:15px;line-height:1.5;margin:0}
.wrap{max-width:900px;margin:0 auto;padding-block:24px 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1{font-size:1.5rem;margin:0 0 .3rem}h2{font-size:1.1rem;margin:1.6rem 0 .5rem}
.muted{color:var(--muted)}
.tbl{overflow-x:auto}table{border-collapse:collapse;width:100%;background:var(--card)}
th,td{border:1px solid var(--rule);padding:6px 8px;vertical-align:top;text-align:left}
th{font-size:.85rem;color:var(--muted)}
.voor{background:var(--bad-bg)}.na{background:var(--ok-bg)}
.flag{background:var(--warn-bg);border:1px solid var(--rule);border-radius:6px;padding:8px 10px;margin:6px 0}
"""


def html_verslag(les, verslag):
    e = lambda x: html.escape(_str(x))  # noqa: E731
    d = [f"<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
         f"<title>Taalverslag: {e(les.get('titel'))}</title><style>{_CSS}</style><div class='wrap'>",
         f"<h1>{e(les.get('titel'))}</h1>",
         f"<p class='muted'>Graad {e(les.get('graad'))} · {e(les.get('vak'))} · "
         f"taalnasien {e(verslag.get('wanneer'))} · {e(verslag.get('prompts'))}</p>",
         f"<p>{len(verslag['toegepas'])} changes applied, {len(verslag['laat_vaar'])} dropped by the reviewer, "
         f"{len(verslag['na_skrywer'])} not applied and sent on, {len(verslag['nie_toegepas'])} kept but not "
         f"applied. Words {verslag['woorde_voor']} before, {verslag['woorde_na']} after.</p>"]
    vv = veiligheidsvlae(verslag)
    if vv:
        d.append("<h2>VEILIGHEID: withdrawn safety wording found</h2>")
        for v in vv:
            d.append(f"<div class='flag'><b>{e(v.get('teks'))}</b><br>{e(v.get('rede'))}</div>")

    def tabel(titel, rye, kolom):
        if not rye:
            return
        d.append(f"<h2>{e(titel)}</h2><div class='tbl'><table><tr><th>#</th><th>Voor</th><th>Ná</th><th>{e(kolom)}</th></tr>")
        for r in rye:
            rede = r.get("waarom") or r.get("rede_keurder") or ""
            fout = r.get("fout") or ""
            d.append(f"<tr><td>{r['nr']}</td><td class='voor'>{e(r['voor'])}</td><td class='na'>{e(r['na'])}</td>"
                     f"<td>{e(fout)}{'<br>' if fout and rede else ''}<span class='muted'>{e(rede)}</span></td></tr>")
        d.append("</table></div>")

    tabel("Applied", verslag["toegepas"], "Fault and reason")
    tabel("Not applied, sent to the writer or a person", verslag["na_skrywer"], "Why")
    tabel("Kept by the reviewer but not applied", verslag["nie_toegepas"], "Why")
    tabel("Dropped by the reviewer", verslag["laat_vaar"], "Why")
    ander = [v for v in verslag.get("vlae") or [] if v not in vv]
    if ander or verslag.get("beskerm_bedenkings"):
        d.append("<h2>Flags from the finder</h2>")
        for v in ander:
            d.append(f"<div class='flag'><b>{e(v.get('teks'))}</b><br>{e(v.get('rede'))}</div>")
        for v in verslag.get("beskerm_bedenkings") or []:
            d.append(f"<div class='flag'>Protected word <b>{e(v.get('woord'))}</b>: {e(v.get('rede'))}</div>")
    d.append("</div>")
    return "".join(d)


def main():
    ap = argparse.ArgumentParser(description="Show a lesson's last language report")
    ap.add_argument("--les-pad", required=True)
    a = ap.parse_args()
    pad = P.taal_verslag(a.les_pad)
    if not os.path.exists(pad):
        sys.exit(f"no language report at {pad}")
    v = P.lees_json(pad)
    print(f"{len(v['toegepas'])} applied, {len(v['laat_vaar'])} dropped, "
          f"{len(v['na_skrywer'])} sent on, {len(v['nie_toegepas'])} not applied; "
          f"words {v['woorde_voor']} -> {v['woorde_na']}")
    for r in v["toegepas"]:
        print(f"  {r['nr']:>3}  {r['voor']}\n       -> {r['na']}")
    for line in vir_skrywer(v) + vir_n_mens(v):
        print(f"  {line}")


if __name__ == "__main__":
    main()

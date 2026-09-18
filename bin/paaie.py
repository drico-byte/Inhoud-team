#!/usr/bin/env python3
"""
Where everything lives.

One module so that the runner, the setup script and the log reader cannot
disagree about a path. Every location that matters to the pipeline is derived
here from a subject, a grade and a CAPS sub-topic, so a path always states its
own CAPS location:

    goedgekeur/gr4/sosiale-wetenskappe/vervoer-op-water/les-3.json

Two locations are deliberately outside the repository:

  goedgekeur/   the approved-output boundary. Neither team owns it and neither
                reaches into the other's tree. The HTML team reads it; nothing
                in this repository writes to it except an approval, and nothing
                ever edits a file already in it.
  skrapruimte/  OCR scratch. Hundreds of temp files per profiler run must not
                land in the repository (a rasterised textbook page in git is the
                one thing the copyright discipline exists to prevent) and must
                not land in a synced folder such as OneDrive.
"""
import glob
import json
import os
import re
import unicodedata

SKILL_NAME = "wolkskool-inhoudstandaard"
SKEMA_WEERGAWE = "1.0"

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKILL = os.path.join(REPO, "skills", SKILL_NAME)
SCRIPTS = os.path.join(SKILL, "scripts")
PROMPTS = os.path.join(REPO, "prompts")
PROFIELE = os.path.join(REPO, "profiele")
KAPS = os.path.join(REPO, "kaps")
SPESIFIKASIES = os.path.join(REPO, "spesifikasies")
SPEK_KONSEP = os.path.join(SPESIFIKASIES, "konsep")
SPEK_GOEDGEKEUR = os.path.join(SPESIFIKASIES, "goedgekeur")
KONSEPTE = os.path.join(REPO, "konsepte")
LOGS = os.path.join(REPO, "logs")
GATE_LOG = os.path.join(LOGS, "gate_log.jsonl")
HARDLOOP_LOG = os.path.join(LOGS, "hardloop_log.jsonl")
VERSLAE = os.path.join(LOGS, "verslae")

# Outside the repository. Overridable so a second machine or a test run does not
# have to match this one.
SKRAPRUIMTE_DEFAULT = ("C:/temp/wolkskool-scratch" if os.name == "nt"
                       else "/tmp/wolkskool-scratch")

# Where an Afrikaans hunspell dictionary is looked for. Optional throughout:
# spelling is a warning-level check because Afrikaans compounds freely and no
# dictionary keeps up, so its absence must never stop the gate.
HUNSPELL_KANDIDATE = ["C:/hunspell/af_ZA", "/usr/share/hunspell/af_ZA"]

REVISIE_MAKS = 2          # revision cycles before the human is asked
BEGROTING_TOLERANSIE = 0.15


def skrapruimte():
    return os.environ.get("WOLKSKOOL_SCRATCH") or SKRAPRUIMTE_DEFAULT


def hunspell_pad():
    """The dictionary base path if one is installed, else None."""
    env = os.environ.get("WOLKSKOOL_HUNSPELL")
    for base in ([env] if env else HUNSPELL_KANDIDATE):
        if base and os.path.exists(base + ".aff") and os.path.exists(base + ".dic"):
            return base
    return None


# ------------------------------------------------------------------ slugs
def slug(text):
    """ASCII-safe path segment. 'Vervoer op water' -> 'vervoer-op-water'.

    Diacritics are folded rather than dropped, so 'hoë skepe' becomes
    'hoe-skepe' and not 'ho-skepe'.
    """
    s = unicodedata.normalize("NFKD", str(text))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("'", "").replace("\u2019", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-")


def kaps_pad(graad, vak, subonderwerp):
    """The shared 'gr4/sosiale-wetenskappe/vervoer-op-water' fragment."""
    return os.path.join(f"gr{int(graad)}", slug(vak), slug(subonderwerp))


# ------------------------------------------------------------------ specs
def spek_konsep(graad, vak, subonderwerp):
    """Where the planner writes. Not readable by the pipeline."""
    return os.path.join(SPEK_KONSEP, f"gr{int(graad)}", slug(vak),
                        slug(subonderwerp) + ".json")


def spek_goedgekeur(graad, vak, subonderwerp):
    """Where a human puts a spec they have read and accepted.

    Approval is a location, not a field, for the same reason it is a location for
    lessons: an agent can set a status field and cannot move a file into a folder
    a human controls.
    """
    return os.path.join(SPEK_GOEDGEKEUR, f"gr{int(graad)}", slug(vak),
                        slug(subonderwerp) + ".json")


# ------------------------------------------------------------------ drafts
def konsep_gids(graad, vak, subonderwerp):
    return os.path.join(KONSEPTE, kaps_pad(graad, vak, subonderwerp))


def les_konsep(graad, vak, subonderwerp, nommer):
    return os.path.join(konsep_gids(graad, vak, subonderwerp), f"les-{int(nommer)}.json")


def spek_inskrywing(graad, vak, subonderwerp, nommer):
    """The one lesse entry the writer and the coverage checker are given.

    Kept in a spek/ subdirectory rather than beside the draft. The fact checker is
    handed the draft and nothing else — it must judge what the lesson says, not
    what it was meant to say — and a spec sitting next to the draft is an
    invitation. Tool permissions cannot enforce that boundary, so the layout does
    what it can and the agent prompt does the rest.
    """
    return os.path.join(konsep_gids(graad, vak, subonderwerp), "spek",
                        f"les-{int(nommer)}.json")


# What a fact checker may see of a draft's provenance. Everything else under
# `herkoms` is withheld. See skryf_feitekopie -- this is an allowlist on purpose.
HERKOMS_BEHOU = ("kaps_dokument", "skrywer_prompt", "handboek_gesien",
                 "videoskrif_gesien")


def feitekopie(les_pad):
    """The copy of a draft the fact checker is given: the lesson without its
    provenance note.

    The spek/ layout above keeps the specification away from the fact checker,
    but the draft itself carries the intent. Writers record their reasoning in
    herkoms.nota — why a sentence was cut, what a requirement asked for, what
    was deliberately left out — and they are right to: it is how a decision
    survives to the next revision, and several corrections have been saved by it.

    But the fact checker is handed the draft, so it reads that reasoning, and the
    charitable-reading risk arrives through the back door. It gets worse with
    every revision, because each pass appends its own reasoning — so the
    most-corrected lessons, the ones that most need an honest check, leak most.
    Two fact checkers raised it unprompted; one said it read the note before it
    could avoid it.

    Drico's decision, 9 September 2026: strip it here rather than ask writers not
    to write it. The runner already decides what each checker sees, and this is
    the same decision.

    16 September 2026: that decision stripped one key by name, `herkoms.nota`,
    and writers also write `herkoms.hersieningsnota`, which does the identical
    job -- it quotes the requirement a revision served, in capitals, along with
    warnings lifted from the specification's own risk notes. It went straight
    through for a week. A fact checker read one and said so, exactly as two did
    about the original leak.

    So this no longer names the fields it removes. It names the ones a checker
    may keep and drops everything else under `herkoms`. A list of what to remove
    loses to every field name invented after it was written; a list of what to
    keep does not.

    18 September 2026: the leak turned up again, inside a field the allowlist
    KEEPS. `profiel_konfig` is meant to name a measurement config. Writers had
    been writing their own reasoning into it -- which config the brief named,
    what the SPECIFICATION says about the budget basis, who decided a number and
    when. Twelve lessons across four subjects, and a fact checker read one and
    said so, which is now the fourth checker to raise this unprompted.

    So `profiel_konfig` is out. Asking the allowlist question properly -- what is
    this checker ENTITLED to see? -- answers it: a fact checker verifies claims
    against outside sources and has no use for budget provenance at all. What
    remains names the curriculum document, the writer prompt and the two "did you
    look at it" records, and none of those is a place a writer reasons.

    The lesson generalises: an allowlist is only as good as the assumption that
    each kept field holds an identifier rather than prose. Check that the fields
    you keep cannot carry a sentence.
    """
    return os.path.join(os.path.dirname(les_pad), "feite-kopie",
                        os.path.basename(les_pad))


def skryf_feitekopie(les_pad):
    """Write the fact checker's copy and return its path.

    Regenerated on every call, because the draft moves. The marker left behind
    is deliberate: without it a checker meets a lesson with no note and reports
    that something dropped it, which one did before this existed. The marker
    says a note was withheld and says nothing about what it contained.
    """
    les = lees_json(les_pad)
    h = les.get("herkoms")
    if isinstance(h, dict):
        weg = [k for k in h if k not in HERKOMS_BEHOU]
        if weg:
            h = {k: v for k, v in h.items() if k in HERKOMS_BEHOU}
            h["nota_weerhou"] = (
                "Die skrywer se notas is uit hierdie kopie weerhou (%d veld(e)). Hulle dra sy "
                "redenasie en die spesifikasie se vereistes, en die feitenasiener moet beoordeel "
                "wat die les SE, nie wat dit bedoel het nie. Niks is uit die lesinhoud verwyder "
                "nie." % len(weg))
            les = dict(les, herkoms=h)
    pad = feitekopie(les_pad)
    skryf_json(pad, les)
    return pad


def newe(les_pad, agtervoegsel):
    """A sibling artifact of a draft: les-3.json -> les-3.<agtervoegsel>.json"""
    return les_pad[:-len(".json")] + f".{agtervoegsel}.json"


def hek_verslag(les_pad):
    return newe(les_pad, "hek")


def dekking_verslag(les_pad):
    return newe(les_pad, "dekking")


def feite_verslag(les_pad):
    return newe(les_pad, "feite")


def staat_pad(les_pad):
    return newe(les_pad, "staat")


# ------------------------------------------------------------------ approved

# ------------------------------------------------------------------ profiles
def vind_profiel(vak, graad, subonderwerp=None):
    """Find the profiler config for a subject-grade.

    Matched on the config's own contents rather than on its filename, so no
    naming convention has to be remembered or enforced. Returns
    (path, config) or (None, reason).
    """
    if not os.path.isdir(PROFIELE):
        return None, f"there is no {os.path.relpath(PROFIELE, REPO)}/ directory"

    paths = sorted(glob.glob(os.path.join(PROFIELE, "*.json")))
    if not paths:
        return None, ("no profiler config in profiele/ — run the profiler once for "
                      "this subject-grade before any lesson is written")

    vak_key, wrong = slug(vak), []
    kandidate = []
    for p in paths:
        try:
            cfg = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError) as e:
            wrong.append(f"{os.path.basename(p)} is not readable JSON ({e})")
            continue
        if slug(cfg.get("vak", "")) == vak_key and int(cfg.get("graad", -1)) == int(graad):
            kandidate.append((p, cfg))

    if not kandidate:
        have = []
        for p in paths:
            try:
                c = json.load(open(p, encoding="utf-8"))
                have.append(f"{os.path.basename(p)}: {c.get('vak')} Gr {c.get('graad')}")
            except (OSError, ValueError):
                pass
        return None, ("no profiler config for {} Gr {}. profiele/ holds: {}".format(
            vak, graad, "; ".join(have) or "nothing usable"))

    if subonderwerp:
        sub_key = slug(subonderwerp)
        for p, cfg in kandidate:
            for label in (cfg.get("subonderwerpe") or {}):
                if slug(label) == sub_key:
                    return p, cfg
        names = sorted({label for _, c in kandidate
                        for label in (c.get("subonderwerpe") or {})})
        return None, ("profiler config {} covers {} Gr {} but has no sub-topic "
                      "matching '{}'. It measured: {}".format(
                          os.path.basename(kandidate[0][0]), vak, graad, subonderwerp,
                          "; ".join(names) or "nothing"))

    return kandidate[0]


def onderwerp_woorde(cfg, subonderwerp):
    """The measured textbook volume for one sub-topic, or None."""
    sub_key = slug(subonderwerp)
    for label, v in (cfg.get("subonderwerpe") or {}).items():
        if slug(label) == sub_key:
            return v
    return None


# ------------------------------------------------------------- agreed wordings
def gedeelde_omskrywings_pad(vak, graad):
    """The agreed-wordings file for one subject-grade, or None.

    One file per subject-grade under kaps/, matched on the file's own `vak` and
    `graad` rather than on its name -- the same way a profiler config is matched,
    and for the same reason. Natuurwetenskappe wrote
    kaps/gedeelde-omskrywings.json before there was a second subject, so the name
    proves nothing about whose wordings are inside. A lookup that silently hands
    back another subject's list is worse than one that hands back nothing: the
    writer would read wordings for terms this subject never agreed, and a
    coverage checker would hold the draft to them.
    """
    for p_ in sorted(glob.glob(os.path.join(KAPS, "gedeelde-omskrywings*.json"))):
        try:
            d = lees_json(p_)
        except (OSError, ValueError):
            continue
        if (slug(d.get("vak", "")) == slug(vak)
                and int(d.get("graad", -1)) == int(graad)):
            return p_
    return None


def gedeelde_omskrywings(vak, graad):
    """The whole agreed-wordings file for a subject-grade, {} when there is none."""
    p_ = gedeelde_omskrywings_pad(vak, graad)
    if not p_:
        return {}
    try:
        return lees_json(p_)
    except (OSError, ValueError):
        return {}


# ------------------------------------------------------------------ io helpers
def lees_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def skryf_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def voeg_jsonl(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def rel(path):
    """Repo-relative where possible, absolute otherwise — for readable output."""
    try:
        r = os.path.relpath(path, REPO)
    except ValueError:
        return path
    return path if r.startswith("..") else r.replace(os.sep, "/")

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

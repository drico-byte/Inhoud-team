#!/usr/bin/env python3
"""
The runner. One entry point per lesson, walking the pipeline and stopping
wherever a human or an agent has to act.

    python bin/hardloop.py --vak "Sosiale Wetenskappe" --graad 4 \
                           --subonderwerp "Vervoer op water" --les 3

    python bin/hardloop.py --vak ... --graad 4 --subonderwerp ...      # overview
    python bin/hardloop.py --vak ... --les 3 --keur-goed               # sign-off
    python bin/hardloop.py --vak ... --les 3 --hervat                  # after a fix

WHAT IT DOES AND DOES NOT DO

It runs every deterministic step itself — the gate, the spec validator, the
report validator, the logging, the routing — and it stops and says exactly which
agent to invoke next with which inputs. It does not invoke the agents: they are
Claude Code subagents in .claude/agents/, invoked from a Claude Code session,
and there is no supported way to call a named project subagent from a script.
So the loop is: run this, do the one step it names, run it again.

ORDER MATTERS. The gate runs before the checkers. Reviewing a draft that is
about to be rewritten for length wastes the review and produces contradictory
feedback. The two checkers run in parallel and are kept separate on purpose —
coverage needs the spec, facts must not have it.

EXIT CODES

    0   done: nothing is outstanding for this lesson, or the approval completed
    10  waiting on an agent or on a human — the next action is printed
    1   gate FAIL — back to the writer, with numbers
    2   MENS_NODIG — a checker escalated; a person must look
    3   refused: missing profiler config, unapproved spec, or bad arguments
    4   a checker report is malformed or self-contradictory
    5   revision limit reached — escalated to a human
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402


# ---------------------------------------------------------------- small helpers
def nou():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def konsep_hash(les):
    """Content hash of a draft, ignoring `status`.

    `status` is stamped by this runner as the lesson moves konsep -> gated, and a
    stamp must not make the gate result and the checker reports look stale.
    """
    body = {k: v for k, v in les.items() if k != "status"}
    blob = json.dumps(body, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return "sha256:" + hashlib.sha256(blob).hexdigest()[:32]


def loop(script, *args):
    """Run one of the standard's scripts and return (exit_code, stdout, stderr)."""
    cmd = [sys.executable, os.path.join(P.SCRIPTS, script), *[str(a) for a in args]]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    return r.returncode, (r.stdout or ""), (r.stderr or "")


class Refuse(Exception):
    """Something is not in place. Exit 3, say what and how to fix it."""

    def __init__(self, msg, *hints):
        super().__init__(msg)
        self.hints = hints


# ---------------------------------------------------------------- output
class Uitvoer:
    """Collects the human report and the machine-readable equivalent."""

    def __init__(self, json_mode):
        self.json_mode = json_mode
        self.lines = []
        self.data = {"stappe": [], "volgende": None, "status": None, "kode": None}

    def say(self, text=""):
        self.lines.append(text)

    def head(self, text):
        self.say()
        self.say(text)
        self.say("-" * len(text))

    def step(self, name, verdict, detail=None):
        self.data["stappe"].append({"stap": name, "uitslag": verdict,
                                    "besonderhede": detail})
        self.say(f"  {verdict:<10} {name}")
        for d in (detail or []):
            self.say(f"             {d}")

    def next_action(self, wie, wat, invoer=None, uitvoer=None, waarskuwing=None):
        self.data["volgende"] = {"wie": wie, "wat": wat, "invoer": invoer or [],
                                 "uitvoer": uitvoer, "waarskuwing": waarskuwing}
        self.head(f"NEXT: {wie}")
        self.say(f"  {wat}")
        for i in (invoer or []):
            self.say(f"    in   {i}")
        if uitvoer:
            self.say(f"    out  {uitvoer}")
        if waarskuwing:
            self.say(f"    !!   {waarskuwing}")

    def finish(self, status, kode):
        self.data["status"] = status
        self.data["kode"] = kode
        if self.json_mode:
            print(json.dumps(self.data, ensure_ascii=False, indent=2))
        else:
            self.say()
            self.say(f"STATUS: {status}   (exit {kode})")
            self.say()
            print("\n".join(self.lines))
        return kode


# ---------------------------------------------------------------- preflight
def eis_profiel(vak, graad, sub):
    pad, cfg = P.vind_profiel(vak, graad, sub)
    if pad is None:
        raise Refuse(
            f"no profiler config for {vak} Gr {graad} / '{sub}' — {cfg}",
            "The profiler runs once per subject-grade, before any lesson is written.",
            "It is the only component permitted to read a textbook, and it emits",
            "numbers only. See README, 'Profiling a new subject-grade'.")
    vol = P.onderwerp_woorde(cfg, sub)
    if not vol or not vol.get("woorde"):
        raise Refuse(f"profiler config {P.rel(pad)} records no word volume for '{sub}'")
    return pad, cfg, vol


def eis_spek(vak, graad, sub, uit):
    goed = P.spek_goedgekeur(graad, vak, sub)
    if not os.path.exists(goed):
        konsep = P.spek_konsep(graad, vak, sub)
        hints = [
            "A spec is approved by a human moving it, not by a field an agent can set.",
            f"  planner writes   {P.rel(konsep)}",
            f"  human moves to   {P.rel(goed)}",
        ]
        if os.path.exists(konsep):
            hints.insert(0, "There IS a draft spec waiting to be read and approved.")
        else:
            hints.insert(0, "No spec exists yet — run the planner for this sub-topic.")
        raise Refuse(f"no approved spec for {vak} Gr {graad} / '{sub}'", *hints)

    code, out, err = loop("spec_check.py", goed, "--json")
    try:
        result = json.loads(out)
    except ValueError:
        raise Refuse(f"spec_check.py could not read {P.rel(goed)}",
                     (err or out).strip()[:400])
    if code != 0:
        raise Refuse(f"the approved spec fails spec_check.py: {P.rel(goed)}",
                     *[f"  {f}" for f in result.get("failures", [])],
                     "Fix the spec, re-approve it, then run this again. A bad spec is",
                     "cheaper to fix here than twenty lessons later.")
    uit.step("spec_check.py", "PASS",
             [f"{result.get('lessons')} lessons, {result.get('total_budget')} words total",
              *[f"warn  {w}" for w in result.get("warnings", [])]])
    return goed, P.lees_json(goed)


def eis_les_inskrywing(spek, nommer):
    for L in spek.get("lesse", []):
        if int(L.get("nommer", -1)) == int(nommer):
            return L
    have = ", ".join(str(L.get("nommer")) for L in spek.get("lesse", []))
    raise Refuse(f"the spec has no lesson {nommer} (it has: {have or 'none'})")


# ---------------------------------------------------------------- state
def lees_staat(pad, les_id):
    if os.path.exists(pad):
        return P.lees_json(pad)
    return {"les": les_id, "skema_weergawe": P.SKEMA_WEERGAWE, "konsep_hash": None,
            "hek": None, "teruggestuur_vir": [], "eskalasie": None,
            "geskiedenis": []}


def teken_op(staat, staat_pad, gebeurtenis, **velde):
    inskrywing = {"wanneer": nou(), "gebeurtenis": gebeurtenis, **velde}
    staat["geskiedenis"].append(inskrywing)
    P.skryf_json(staat_pad, staat)
    P.voeg_jsonl(P.HARDLOOP_LOG, {"les": staat["les"], **inskrywing})


def argiveer(bron, les_id, siklus, naam):
    """Keep every gate result and every checker report. After twenty lessons
    these logs are what shows whether the writer under-supplies or drifts formal,
    and that is a prompt fix rather than twenty per-lesson fixes."""
    dest = os.path.join(P.VERSLAE, les_id.replace("/", os.sep),
                        f"s{siklus}-{naam}.json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(bron, dest)
    return dest


# ---------------------------------------------------------------- steps
def hardloop_hek(les_pad, graad, begroting, uit):
    args = [les_pad, "--grade", graad, "--budget", begroting, "--json",
            "--log", P.GATE_LOG]
    dic = P.hunspell_pad()
    if dic:
        args += ["--woordeboek", dic]
    code, out, err = loop("gate.py", *args)
    try:
        r = json.loads(out)
    except ValueError:
        raise Refuse("gate.py did not return JSON", (err or out).strip()[:400])

    P.skryf_json(P.hek_verslag(les_pad), r)
    s = r.get("study") or {}
    detail = [f"{s.get('words')} words against a budget of {begroting}",
              f"{s.get('mean_sentence_len')} words per sentence, "
              f"{s.get('mean_syllables')} syllables per word, "
              f"{s.get('pct_polysyllabic')}% polysyllabic",
              *[f"FAIL  {f}" for f in r.get("failures", [])],
              *[f"warn  {w}" for w in r.get("warnings", [])],
              *[f"note  {n}" for n in r.get("notes", [])]]
    uit.step("gate.py", r["verdict"], detail)
    return code, r


def keur_verslag(verslag_pad, les_pad, spek_inskrywing_pad, uit, naam):
    """Validate a checker's own report before acting on it."""
    args = [verslag_pad, "--les", les_pad, "--json"]
    if spek_inskrywing_pad:
        args += ["--spek", spek_inskrywing_pad]
    code, out, err = loop("verdict_check.py", *args)
    try:
        r = json.loads(out)
    except ValueError:
        raise Refuse(f"verdict_check.py could not read {P.rel(verslag_pad)}",
                     (err or out).strip()[:400])
    uit.step(f"verdict_check.py ({naam})", "SOUND" if r["sound"] else "MALFORMED",
             [f"verdict {r.get('verdict')}, {r.get('items')} items",
              *[f"FAIL  {f}" for f in r.get("failures", [])],
              *[f"warn  {w}" for w in r.get("warnings", [])]])
    return code == 0, r


# ---------------------------------------------------------------- approval
def keur_goed(les_pad, doel, les, uit, staat, staat_pad, nommer):
    """Copy an approved draft across the boundary. Never editing in place, and
    never without a person saying so out loud.

    Prints its own report and returns (exit_code, status). The status carries the
    _KLAAR suffix so the caller knows not to print again.
    """
    bestaan = os.path.exists(doel)
    uit.head("HUMAN SIGN-OFF")
    uit.say(f"  lesson    {les.get('titel')}  (Gr {les.get('graad')}, "
            f"{les.get('kaps_punt')})")
    uit.say(f"  from      {P.rel(les_pad)}")
    uit.say(f"  to        {doel}")
    if bestaan:
        uit.say("  NOTE      a lesson already exists there and will be REPLACED in full.")
        uit.say("            Approved files are never edited in place; a correction goes")
        uit.say("            back through the pipeline and is re-copied.")

    if not sys.stdin.isatty():
        uit.say()
        uit.say("  Refused: approval needs a person at a terminal. Run this command")
        uit.say("  yourself in an interactive shell and type the confirmation.")
        uit.say("  An agent running this script cannot approve anything, which is")
        uit.say("  the point — location carries the approval, and a person moves it.")
        uit.say()
        uit.say("STATUS: GEWEIER_NIE_INTERAKTIEF   (exit 3)")
        print("\n".join(uit.lines))
        return 3, "GEWEIER_KLAAR"

    print("\n".join(uit.lines))
    verwag = f"les-{int(nommer)}"
    try:
        antwoord = input(f"\nType '{verwag}' to approve this lesson, "
                         f"anything else to stop: ").strip()
    except (EOFError, KeyboardInterrupt):
        # No one there to answer. isatty() lies in some shells, so this is the
        # guard that actually holds: nothing crosses the boundary unattended.
        print("\n\nNo answer read from the terminal. Nothing was copied.")
        print("Run this yourself in an interactive shell.\n")
        return 3, "GEWEIER_KLAAR"
    if antwoord != verwag:
        print("\nNot approved. Nothing was copied.\n")
        return 3, "GEWEIER_KLAAR"

    P.skryf_json(doel, dict(les, status="goedgekeur"))
    teken_op(staat, staat_pad, "goedgekeur", doel=doel,
             konsep_hash=staat["konsep_hash"], vervang=bestaan)
    print(f"\nApproved. Written to {doel}")
    print("The HTML team reads that folder. Nothing here writes to it again")
    print("unless this lesson is corrected and re-approved.\n")
    return 0, "GOEDGEKEUR_KLAAR"


# ---------------------------------------------------------------- overview
def oorsig(vak, graad, sub, spek, uit):
    uit.head(f"{vak} Gr {graad} — {sub}")
    for L in spek.get("lesse", []):
        n = L["nommer"]
        les_pad = P.les_konsep(graad, vak, sub, n)
        staat = lees_staat(P.staat_pad(les_pad), "")
        waar = []
        if os.path.exists(P.les_goedgekeur(graad, vak, sub, n)):
            waar.append("APPROVED")
        elif not os.path.exists(les_pad):
            waar.append("no draft")
        else:
            waar.append(f"hek={staat.get('hek') or '-'}")
            for naam, pad in (("dekking", P.dekking_verslag(les_pad)),
                              ("feite", P.feite_verslag(les_pad))):
                if os.path.exists(pad):
                    try:
                        waar.append(f"{naam}={P.lees_json(pad).get('verdict')}")
                    except ValueError:
                        waar.append(f"{naam}=unreadable")
                else:
                    waar.append(f"{naam}=-")
        if staat.get("eskalasie"):
            waar.append("ESCALATED")
        rev = len(staat.get("teruggestuur_vir") or [])
        if rev:
            waar.append(f"revisions={rev}/{P.REVISIE_MAKS}")
        uit.say(f"  les-{n}  {L['begroting']:>4}w  {L['titel'][:38]:<40} "
                f"{'  '.join(waar)}")
    uit.say()
    uit.say("  Add --les N to advance one lesson.")


# ---------------------------------------------------------------- the walk
def stap(a, uit):
    vak, graad, sub = a.vak, a.graad, a.subonderwerp

    profiel_pad, profiel, vol = eis_profiel(vak, graad, sub)
    uit.step("profiler config", "OK",
             [f"{P.rel(profiel_pad)}",
              f"'{sub}': {vol['woorde']} measured words over {vol['bladsye']} pages"])

    spek_pad, spek = eis_spek(vak, graad, sub, uit)
    uit.step("approved spec", "OK", [P.rel(spek_pad)])

    if a.les is None:
        oorsig(vak, graad, sub, spek, uit)
        return 0, "OORSIG"

    inskrywing = eis_les_inskrywing(spek, a.les)
    begroting = inskrywing["begroting"]
    les_id = P.kaps_pad(graad, vak, sub).replace(os.sep, "/") + f"/les-{a.les}"

    les_pad = P.les_konsep(graad, vak, sub, a.les)
    staat_pad = P.staat_pad(les_pad)
    staat = lees_staat(staat_pad, les_id)

    # The spec entry is written out on its own so the coverage checker and
    # verdict_check.py get exactly the one lesson's requirements, and so the fact
    # checker's inputs never include a path into spesifikasies/.
    inskrywing_pad = P.spek_inskrywing(graad, vak, sub, a.les)

    # --- escalation blocks the loop until a person clears it -----------------
    if staat.get("eskalasie") and not a.hervat:
        e = staat["eskalasie"]
        uit.head("ESCALATED — waiting on a person")
        uit.say(f"  {e.get('rede')}")
        uit.say(f"  raised    {e.get('wanneer')}")
        uit.say(f"  see       {P.rel(staat_pad)}")
        uit.say()
        uit.say("  When it is dealt with, re-run with --hervat to start a new cycle.")
        return (5 if e.get("soort") == "revisielimiet" else 2), "ESKALASIE"

    if a.hervat and staat.get("eskalasie"):
        # The revision budget resets too, or a lesson that spent it could never be
        # resumed — it would re-escalate on the next run. The history keeps the
        # real count, so logoorsig.py still sees a lesson that needed three tries.
        verbruik = len(staat.get("teruggestuur_vir") or [])
        staat["eskalasie"] = None
        staat["teruggestuur_vir"] = []
        teken_op(staat, staat_pad, "hervat_deur_mens", vorige_revisies=verbruik)
        uit.step("escalation cleared", "OK",
                 [f"{verbruik} earlier revision(s) recorded in the history",
                  f"a new cycle starts, {P.REVISIE_MAKS} revisions available"])

    # --- 1. the draft -------------------------------------------------------
    if not os.path.exists(les_pad):
        P.skryf_json(inskrywing_pad, inskrywing)
        uit.next_action(
            "wolkskool-skrywer (agent)",
            f"Write lesson {a.les} of '{sub}' from its spec entry.",
            invoer=[P.rel(inskrywing_pad),
                    f"spec context: vak={vak}, graad={graad}, "
                    f"kaps_onderwerp={spek.get('kaps_onderwerp')}, "
                    f"kaps_subonderwerp={sub}, profiel_konfig="
                    f"{os.path.basename(profiel_pad)}"],
            uitvoer=P.rel(les_pad),
            waarskuwing="No textbook, no scans, no transcriptions. "
                        "handboek_gesien must be false.")
        return 10, "WAG_VIR_SKRYWER"

    les = P.lees_json(les_pad)
    h = konsep_hash(les)
    P.skryf_json(inskrywing_pad, inskrywing)

    # --- 2. a new draft invalidates everything downstream -------------------
    if staat.get("konsep_hash") != h:
        siklus = len(staat.get("teruggestuur_vir") or []) + 1
        for naam, pad in (("hek", P.hek_verslag(les_pad)),
                          ("dekking", P.dekking_verslag(les_pad)),
                          ("feite", P.feite_verslag(les_pad))):
            if os.path.exists(pad):
                argiveer(pad, les_id, max(1, siklus - 1), naam + "-verouderd")
                os.remove(pad)
        staat["konsep_hash"] = h
        staat["hek"] = None
        teken_op(staat, staat_pad, "nuwe_konsep", konsep_hash=h, siklus=siklus)
        uit.step("draft", "NEW", [f"cycle {siklus}, {P.rel(les_pad)}",
                                 "stale gate result and reports archived to logs/verslae/"])

    # A changed spec makes cached results stale as surely as a changed draft does,
    # and the two go stale differently: the gate depends on the grade and the
    # budget, coverage depends on the whole spec entry, and the fact check depends
    # on neither. Re-running a web-heavy fact check for a budget edit is waste.
    hek_konteks = {"graad": int(graad), "begroting": int(begroting)}
    spek_h = konsep_hash(inskrywing)
    siklus_nou = len(staat.get("teruggestuur_vir") or []) + 1

    if staat.get("hek") is not None and staat.get("hek_konteks") != hek_konteks:
        staat["hek"] = None
        uit.step("gate result", "STALE",
                 [f"grade or budget changed to {hek_konteks} — re-gating"])
        if os.path.exists(P.hek_verslag(les_pad)):
            argiveer(P.hek_verslag(les_pad), les_id, siklus_nou, "hek-verouderd")

    if staat.get("spek_hash") not in (None, spek_h) and os.path.exists(P.dekking_verslag(les_pad)):
        argiveer(P.dekking_verslag(les_pad), les_id, siklus_nou, "dekking-verouderd")
        os.remove(P.dekking_verslag(les_pad))
        uit.step("coverage report", "STALE",
                 ["the spec entry changed — coverage must be checked again"])
    staat["spek_hash"] = spek_h

    if les.get("herkoms", {}).get("handboek_gesien") is not False:
        raise Refuse(
            "herkoms.handboek_gesien is not false in this draft",
            "A true or missing value marks calibration material, which must never",
            "be published. Status stays konsep and the HTML team never receives it.")

    # --- 3. the gate, BEFORE the checkers ----------------------------------
    if staat.get("hek") is None:
        code, hek = hardloop_hek(les_pad, graad, begroting, uit)
        staat["hek"] = hek["verdict"]
        staat["hek_konteks"] = hek_konteks
        argiveer(P.hek_verslag(les_pad), les_id, siklus_nou, "hek")
        teken_op(staat, staat_pad, "hek", verdict=hek["verdict"],
                 woorde=(hek.get("study") or {}).get("words"), begroting=begroting,
                 failures=hek.get("failures", []))

        if hek["verdict"] == "FAIL":
            return terug_na_skrywer(
                staat, staat_pad, h, uit, les_pad, inskrywing_pad,
                rede="gate FAIL",
                punte=hek["failures"],
                bron="gate.py")

        les["status"] = "gated"
        P.skryf_json(les_pad, les)
        uit.step("status", "gated", ["measured and within band; ready for review"])

    if staat.get("hek") == "FAIL":
        # A gate failure that was already reported and the draft has not changed.
        hek = P.lees_json(P.hek_verslag(les_pad))
        return terug_na_skrywer(staat, staat_pad, h, uit, les_pad, inskrywing_pad,
                                rede="gate FAIL", punte=hek["failures"],
                                bron="gate.py", herhaal=True)

    # --- 4. the two checkers, in parallel ----------------------------------
    dekking_pad, feite_pad = P.dekking_verslag(les_pad), P.feite_verslag(les_pad)
    kort = [p for p in (dekking_pad, feite_pad) if not os.path.exists(p)]
    if kort:
        uit.head("NEXT: two agents, in parallel")
        uit.say("  They are separate agents on purpose. Coverage needs the spec;")
        uit.say("  facts must not have it, or it reads the lesson charitably.")
        if not os.path.exists(dekking_pad):
            uit.next_action(
                "wolkskool-dekkingsnasiener (agent)",
                f"Check lesson {a.les} against its spec entry.",
                invoer=[P.rel(les_pad), P.rel(inskrywing_pad)],
                uitvoer=P.rel(dekking_pad))
        if not os.path.exists(feite_pad):
            uit.next_action(
                "wolkskool-feitenasiener (agent)",
                f"Verify every checkable claim in lesson {a.les} against sources.",
                invoer=[P.rel(les_pad)],
                uitvoer=P.rel(feite_pad),
                waarskuwing="Do NOT pass the spec, and do not let it read "
                            "spesifikasies/. It must judge what the lesson says.")
        return 10, "WAG_VIR_NASIENERS"

    # --- 5. validate the reports themselves --------------------------------
    verdicts = {}
    for naam, pad, spek_arg in (("dekking", dekking_pad, inskrywing_pad),
                                ("feite", feite_pad, None)):
        sound, r = keur_verslag(pad, les_pad, spek_arg, uit, naam)
        argiveer(pad, les_id, len(staat.get("teruggestuur_vir") or []) + 1, naam)
        teken_op(staat, staat_pad, f"nasien_{naam}", verdict=r.get("verdict"),
                 sound=sound, items=r.get("items"), failures=r.get("failures", []))
        if not sound:
            uit.head("MALFORMED REPORT")
            uit.say(f"  {P.rel(pad)} is not a report the pipeline can act on.")
            uit.say("  Re-run that checker. These reports are the only thing between")
            uit.say("  an error and a learner, so a broken one is not waved through.")
            return 4, "VERSLAG_ONGELDIG"
        verdicts[naam] = r.get("verdict")

    # --- 6. route ----------------------------------------------------------
    if "MENS_NODIG" in verdicts.values():
        wie = [k for k, v in verdicts.items() if v == "MENS_NODIG"]
        staat["eskalasie"] = {"soort": "mens_nodig", "wanneer": nou(),
                             "rede": f"{', '.join(wie)} returned MENS_NODIG — a writer "
                                     f"handed a defect it cannot fix will invent one or "
                                     f"strip the content"}
        teken_op(staat, staat_pad, "eskalasie", soort="mens_nodig", nasieners=wie)
        uit.head("MENS_NODIG — a person must look, now")
        for k in wie:
            r = P.lees_json(dekking_pad if k == "dekking" else feite_pad)
            uit.say(f"  {k}: {r.get('opsomming')}")
            uit.say(f"    see {P.rel(dekking_pad if k == 'dekking' else feite_pad)}")
        uit.say()
        uit.say("  This exits the loop rather than spending a revision cycle.")
        uit.say("  After you have dealt with it, re-run with --hervat.")
        return 2, "MENS_NODIG"

    if "HERSIEN" in verdicts.values():
        punte = []
        for k, v in verdicts.items():
            if v != "HERSIEN":
                continue
            r = P.lees_json(dekking_pad if k == "dekking" else feite_pad)
            for i in r.get("items", []):
                if k == "dekking" and i.get("status") in ("gedeeltelik", "afwesig"):
                    punte.append(f"[{k}] {i.get('verwysing','')[:60]} — "
                                 f"{i.get('status')}: {i.get('aksie','')}")
                if k == "feite" and i.get("status") == "weerspreek":
                    punte.append(f"[{k}] {i.get('bewering','')[:60]} — "
                                 f"corrected: {i.get('regstelling','')}")
        return terug_na_skrywer(staat, staat_pad, h, uit, les_pad, inskrywing_pad,
                                rede="HERSIEN", punte=punte,
                                bron=", ".join(k for k, v in verdicts.items()
                                               if v == "HERSIEN"))

    # --- 7. clear, awaiting a person ---------------------------------------
    doel = P.les_goedgekeur(graad, vak, sub, a.les)
    if a.keur_goed:
        return keur_goed(les_pad, doel, les, uit, staat, staat_pad, a.les)

    uit.head("CLEAR — waiting on human sign-off")
    uit.say("  gate PASS, coverage GOEDGEKEUR, facts GOEDGEKEUR, both reports sound.")
    uit.say(f"  draft     {P.rel(les_pad)}")
    uit.say(f"  would go  {doel}")
    uit.say()
    uit.say("  Nothing crosses that boundary without you. Read the draft, then:")
    uit.say(f"    python bin/hardloop.py --vak \"{vak}\" --graad {graad} "
            f"--subonderwerp \"{sub}\" --les {a.les} --keur-goed")
    return 10, "WAG_VIR_MENS"


def terug_na_skrywer(staat, staat_pad, h, uit, les_pad, inskrywing_pad,
                     rede, punte, bron, herhaal=False):
    """Send a draft back, or escalate if the revision budget is spent.

    Two cycles is the cap. A third pass rarely fixes what two could not, and by
    then the useful information is that the prompt needs changing, not the lesson.
    """
    stuur = list(staat.get("teruggestuur_vir") or [])
    if h not in stuur:
        stuur.append(h)
        staat["teruggestuur_vir"] = stuur
        teken_op(staat, staat_pad, "teruggestuur", rede=rede, bron=bron,
                 siklus=len(stuur), punte=punte[:20])

    if len(stuur) > P.REVISIE_MAKS:
        staat["eskalasie"] = {
            "soort": "revisielimiet", "wanneer": nou(),
            "rede": f"{len(stuur)} revisions requested, cap is {P.REVISIE_MAKS} "
                    f"({rede} from {bron})"}
        teken_op(staat, staat_pad, "eskalasie", soort="revisielimiet",
                 siklusse=len(stuur))
        uit.head("REVISION LIMIT — escalated")
        uit.say(f"  {len(stuur)} revisions asked for; the cap is {P.REVISIE_MAKS}.")
        uit.say("  Two cycles that did not land usually means the prompt needs the fix,")
        uit.say("  not the lesson. bin/logoorsig.py shows whether this is systematic.")
        for p in punte[:8]:
            uit.say(f"    {p}")
        uit.say()
        uit.say("  After you have dealt with it, re-run with --hervat.")
        return 5, "REVISIELIMIET"

    uit.next_action(
        "wolkskool-skrywer (agent)",
        f"Revise the draft. {rede} from {bron}. "
        f"Revision {len(stuur)} of {P.REVISIE_MAKS}.",
        invoer=[P.rel(les_pad), P.rel(inskrywing_pad),
                *[f"fix: {p}" for p in punte[:12]]],
        uitvoer=P.rel(les_pad),
        waarskuwing="Change only what is listed. Re-running the whole lesson loses "
                    "what already passed.")
    return (1 if bron == "gate.py" else 10), ("HEK_FAAL" if bron == "gate.py"
                                              else "WAG_VIR_SKRYWER")


# ---------------------------------------------------------------- entry
def main():
    ap = argparse.ArgumentParser(
        description="Walk one Wolkskool lesson through the pipeline.",
        epilog="Exit codes: 0 done, 10 waiting, 1 gate FAIL, 2 MENS_NODIG, "
               "3 refused, 4 malformed report, 5 revision limit.")
    ap.add_argument("--vak", required=True, help='e.g. "Sosiale Wetenskappe"')
    ap.add_argument("--graad", required=True, type=int, choices=range(4, 13),
                    metavar="4-12")
    ap.add_argument("--subonderwerp", required=True, help='e.g. "Vervoer op water"')
    ap.add_argument("--les", type=int, default=None,
                    help="lesson number within the sub-topic; omit for an overview")
    ap.add_argument("--keur-goed", action="store_true", dest="keur_goed",
                    help="copy a cleared draft to goedgekeur/. Needs a person at a "
                         "terminal to confirm; it cannot be done non-interactively.")
    ap.add_argument("--hervat", action="store_true",
                    help="clear an escalation and start a new cycle (a human action)")
    ap.add_argument("--json", action="store_true", dest="json_mode",
                    help="machine-readable output for an orchestrating session")
    a = ap.parse_args()

    uit = Uitvoer(a.json_mode)
    uit.head(f"Wolkskool pipeline — {a.vak} Gr {a.graad} / {a.subonderwerp}"
             + (f" / les {a.les}" if a.les else ""))
    try:
        kode, status = stap(a, uit)
    except Refuse as e:
        uit.head("REFUSED")
        uit.say(f"  {e}")
        for h in e.hints:
            uit.say(f"  {h}")
        return uit.finish("GEWEIER", 3)
    except (OSError, ValueError, KeyError) as e:
        uit.head("ERROR")
        uit.say(f"  {type(e).__name__}: {e}")
        return uit.finish("FOUT", 3)

    if status.endswith("_KLAAR"):
        return kode     # keur_goed printed its own report
    return uit.finish(status, kode)


if __name__ == "__main__":
    sys.exit(main())

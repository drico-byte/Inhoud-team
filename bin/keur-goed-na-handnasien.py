#!/usr/bin/env python3
"""Sign off a lesson whose checks were briefed by hand, without losing the reports.

WHY THIS EXISTS. `hardloop.py` remembers the draft it last saw by its hash. During a
repair cycle the checks are briefed by hand, so the runner never sees the revised
draft. The first time it is asked about that lesson again -- any call, including
--keur-goed -- it finds a new hash, decides every report beside the draft belongs to
the OLD draft, archives them as "-verouderd" and demands the checks again.

The reports are not stale: they were written for the current draft. On 21 September
2026 four clean Grade 5 lessons lost their reports this way in one command.

This script stashes the reports BEFORE the runner is called at all, lets the runner
register the draft, puts the stashed reports back, and only then signs off.

    python bin/keur-goed-na-handnasien.py --vak Lewensvaardighede --graad 5 \\
        --subonderwerp "Ontwikkeling van self" --les 2

STALENESS IS MEASURED AGAINST THE CONTENT, NOT THE FILE'S CLOCK (7 October 2026,
approved by Lampies). This used to refuse unless both reports were newer than the
draft FILE. That used the modification time as a stand-in for "has the text changed
since it was checked", and the stand-in is wrong in both directions:

  * It refuses finished work. A write that touches only fields the content
    fingerprint excludes -- `status`, and the writer's provenance note -- moves the
    clock without changing a single word a checker reads. Gr 6 Sosiale Wetenskappe
    "Demokrasie en burgerskap" lesson 8 was refused exactly that way: both reports
    clean, the content fingerprint identical to the one the runner recorded when it
    last gated the lesson, and the only thing newer than the fact report was a
    note-only rewrite eleven minutes after it.
  * It passes work it should refuse. If the content changed and the runner never saw
    it, a report written after that change is newer than the file and sails through,
    although nothing has gated or registered the text it judged.

So the comparison is now against the LAST ACTUAL CONTENT CHANGE: the most recent
`nuwe_konsep` event in the lesson's state file, which the runner writes with a
content fingerprint and a timestamp every time it sees new content. A report written
after that moment is valid however many times the file has been touched since. And
the draft's CURRENT fingerprint must still equal the one recorded at that event --
the case the old rule let through is strictly more dangerous than the one it broke
on, so the new path refuses it outright instead of swallowing it.

The fingerprint comes from `hardloop.konsep_hash`, imported. It is not
re-implemented here and must never be: a guard that paraphrases the rules it checks
has already, in this repository, cried wolf on three files for ever while being
blind to thirty.

ONE UNRESOLVABLE FACT MAY BE ACCEPTED, BY NAME (7 October 2026, approved by
Lampies). Where sources genuinely conflict the rule is to keep the best-supported
reading and disclose the conflict in one sentence -- and a lesson that does exactly
that is still reported MENS_NODIG, correctly, because the underlying fact is
unresolved and that is a person's call. There was no way to make that call, so such
a lesson could never ship. A person now writes a dated, item-level acceptance record
beside the draft; `bin/aanvaardings.py` holds every rule about it and this script
and the runner both ask that one module, so they cannot answer differently. Run

    python bin/keur-goed-na-handnasien.py ... --wys-items

to see the items holding a fact report up, with the fingerprint for each and a
record to fill in. A `weerspreek` item can never be accepted, every holding item
must be accepted individually, and there is no blanket form to write.

THE LANGUAGE STEP COMES FIRST (22 October 2026). A revised draft goes through the
language step before it is checked, so the hand cycle is: writer, then run
bin/hardloop.py until it names the two checkers (it runs the gate, the language
finder and reviewer, and the gate again on the way), then brief the checks by hand,
then this script. A language change that alters the text is a content change like a
writer's draft: the runner records it with its fingerprint, and the reports must be
newer than it. Skip the runner step and this script refuses, because the content
fingerprint is not the one the runner registered.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import aanvaardings  # noqa: E402
import hardloop  # noqa: E402  -- for konsep_hash; never re-implement it here
import paaie as P  # noqa: E402


def laaste_inhoudverandering(staat):
    """When the draft's CONTENT last changed, from the lesson's state file.

    Returns (fingerprint, epoch seconds, the timestamp as written), or three Nones
    when the state file records no content change at all.

    The last `nuwe_konsep` entry in list order, because that is the order the runner
    appended them in -- not the latest timestamp, which would let one skewed clock
    decide which fingerprint counts as current.

    A `taal` entry that carries a fingerprint counts too: the runner records one only
    when the language step changed the text (22 October 2026). Without it, every
    lesson the language step touched was refused here as "content has moved",
    because the last writer draft's fingerprint is no longer the text's.
    """
    laaste = None
    for e in (staat.get("geskiedenis") or []):
        if (isinstance(e, dict) and e.get("gebeurtenis") in ("nuwe_konsep", "taal")
                and e.get("konsep_hash") and e.get("wanneer")):
            laaste = e
    if laaste is None:
        return None, None, None
    try:
        t = datetime.fromisoformat(laaste["wanneer"])
    except (TypeError, ValueError):
        return laaste["konsep_hash"], None, laaste["wanneer"]
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return laaste["konsep_hash"], t.timestamp(), laaste["wanneer"]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vak", required=True)
    ap.add_argument("--graad", required=True)
    ap.add_argument("--subonderwerp", required=True)
    ap.add_argument("--les", required=True)
    ap.add_argument("--wys-items", action="store_true", dest="wys_items",
                    help="list the fact-report items holding this lesson up, with the "
                         "fingerprint of each and an acceptance record to fill in. "
                         "Reads only; signs nothing off.")
    a = ap.parse_args()

    les_pad = P.les_konsep(a.graad, a.vak, a.subonderwerp, a.les)
    if not os.path.exists(les_pad):
        sys.exit(f"No draft at {P.rel(les_pad)}; nothing was changed.")

    verslae = {"dekking": P.dekking_verslag(les_pad), "feite": P.feite_verslag(les_pad)}

    if a.wys_items:
        if not os.path.exists(verslae["feite"]):
            sys.exit(f"No fact report at {P.rel(verslae['feite'])}; nothing to list.")
        for reel in aanvaardings.voorbeeld_rekord(les_pad,
                                                  P.lees_json(verslae["feite"])):
            print(reel)
        return 0

    # --- has the CONTENT changed since the checks? --------------------------
    staat_pad = P.staat_pad(les_pad)
    if not os.path.exists(staat_pad):
        sys.exit(f"No state file at {P.rel(staat_pad)}, so there is no record of when "
                 f"this draft's content last changed and no fingerprint to check it "
                 f"against. Run bin/hardloop.py for this lesson once -- it gates the "
                 f"draft and registers it -- and brief any check it asks for. "
                 f"Nothing was changed.")
    staat = P.lees_json(staat_pad)
    nou_afdruk = hardloop.konsep_hash(P.lees_json(les_pad))
    reg_afdruk, inhoud_tyd, inhoud_wanneer = laaste_inhoudverandering(staat)

    if reg_afdruk is None:
        sys.exit(f"{P.rel(staat_pad)} records no content change for this draft, so "
                 f"there is nothing to measure the reports against. The runner writes "
                 f"that record the first time it sees the draft; run bin/hardloop.py "
                 f"for this lesson once. Nothing was changed.")
    if inhoud_tyd is None:
        sys.exit(f"{P.rel(staat_pad)} records the last content change with an "
                 f"unreadable timestamp ({inhoud_wanneer!r}), so report staleness "
                 f"cannot be judged. Nothing was changed.")
    if nou_afdruk != reg_afdruk:
        sys.exit(f"This draft's content has moved since the runner last saw it.\n"
                 f"  recorded  {reg_afdruk}  ({inhoud_wanneer})\n"
                 f"  now       {nou_afdruk}\n"
                 f"The text beside the reports is not the text the runner registered, "
                 f"so nothing here can say what the checks judged. Run bin/hardloop.py "
                 f"for this lesson -- it will gate the new content and ask for the "
                 f"checks it needs. Nothing was changed.")

    print(f"Content last changed {inhoud_wanneer}; the draft still fingerprints to "
          f"{nou_afdruk}.")

    # --- are the reports clean, and were they written after that change? ----
    for soort, pad in verslae.items():
        if not os.path.exists(pad):
            sys.exit(f"No {soort} report beside the draft; run the check first. "
                     f"Nothing was changed.")
        mtyd = os.path.getmtime(pad)
        if mtyd < inhoud_tyd:
            sys.exit(f"The {soort} report was written "
                     f"{datetime.fromtimestamp(mtyd, timezone.utc).isoformat(timespec='seconds')}, "
                     f"before this draft's content last changed ({inhoud_wanneer}), so it "
                     f"checked an earlier version. Run the check again. Nothing was "
                     f"changed.")

    dekking_uitspraak = P.lees_json(verslae["dekking"]).get("verdict")
    if dekking_uitspraak != "GOEDGEKEUR":
        sys.exit(f"The dekking report says {dekking_uitspraak}, not GOEDGEKEUR. "
                 f"Nothing was changed.")

    feite_verslag = P.lees_json(verslae["feite"])
    feite_uitspraak = feite_verslag.get("verdict")
    aanv = aanvaardings.beoordeel(les_pad, feite_verslag)
    if feite_uitspraak != "GOEDGEKEUR":
        # The only way past a fact report that is not GOEDGEKEUR: every item holding
        # it up has its own dated acceptance. One unaccepted item and this refuses,
        # exactly as it did before there was any acceptance at all.
        if not aanv.alles_aanvaar:
            boodskap = [f"The feite report says {feite_uitspraak}, not GOEDGEKEUR, and it "
                        f"is not held up only by accepted items."]
            boodskap.extend("  " + r for r in aanv.redes)
            boodskap.append(f"  Run this with --wys-items to see each item and its "
                            f"fingerprint.")
            boodskap.append("Nothing was changed.")
            sys.exit("\n".join(boodskap))
        print(f"The feite report says {feite_uitspraak}, held up only by "
              f"{len(aanv.aanvaar)} accepted item(s):")
        for reel in aanv.reels():
            print("  " + reel)
    elif aanv.redes:
        # A record that applies to nothing. Not a refusal -- the lesson is clean
        # without it -- but a reader must not have to find the leftover themselves.
        for reel in aanv.redes:
            print("Note: " + reel)

    stash = tempfile.mkdtemp(prefix="keur-goed-")
    for soort, pad in verslae.items():
        shutil.copy2(pad, os.path.join(stash, soort + ".json"))

    runner = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hardloop.py")
    basis = [sys.executable, runner, "--vak", a.vak, "--graad", a.graad,
             "--subonderwerp", a.subonderwerp, "--les", a.les]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")

    # 1. let the runner see the draft (this is the call that archives the reports)
    subprocess.run(basis, capture_output=True, text=True, encoding="utf-8",
                   errors="replace", env=env)
    # 2. put the reports back, untouched
    for soort, pad in verslae.items():
        shutil.copy2(os.path.join(stash, soort + ".json"), pad)
    # 3. sign off
    r = subprocess.run(basis + ["--keur-goed"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    goedgekeur = [reel for reel in r.stdout.splitlines() if "Approved in place" in reel]
    if goedgekeur:
        print(goedgekeur[0])
        for merk in ("Readable copy", "Delivered", "Outbox", "Beskermde woorde",
                     "could not be copied", "could not be put in the outbox"):
            reels = [reel for reel in r.stdout.splitlines() if merk in reel]
            if reels:
                print(reels[0])
        # The language items still open are the one part of the runner's sign-off
        # that a person must act on, so they are passed through whole.
        reels = r.stdout.splitlines()
        for i, reel in enumerate(reels):
            if "Language items still open" in reel:
                blok = [reel]
                for volg in reels[i + 1:]:
                    if not volg.strip():
                        break
                    blok.append(volg)
                print("\n".join(blok))
                break
        shutil.rmtree(stash, ignore_errors=True)
        return 0
    print("The runner did not sign it off. The reports are back beside the draft, and a "
          f"copy is kept in {stash}. Last lines of the runner:")
    print("\n".join(r.stdout.splitlines()[-15:]))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

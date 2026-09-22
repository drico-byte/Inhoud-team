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
register the draft, puts the stashed reports back, and only then signs off. It
refuses unless both reports say GOEDGEKEUR and both are newer than the draft -- a
report older than the draft really is stale, and restoring it would sign off text
nobody checked.

    python bin/keur-goed-na-handnasien.py --vak Lewensvaardighede --graad 5 \\
        --subonderwerp "Ontwikkeling van self" --les 2
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paaie as P  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vak", required=True)
    ap.add_argument("--graad", required=True)
    ap.add_argument("--subonderwerp", required=True)
    ap.add_argument("--les", required=True)
    a = ap.parse_args()

    les_pad = P.les_konsep(a.graad, a.vak, a.subonderwerp, a.les)
    if not os.path.exists(les_pad):
        sys.exit(f"No draft at {P.rel(les_pad)}; nothing was changed.")
    les_tyd = os.path.getmtime(les_pad)

    verslae = {"dekking": P.dekking_verslag(les_pad), "feite": P.feite_verslag(les_pad)}
    for soort, pad in verslae.items():
        if not os.path.exists(pad):
            sys.exit(f"No {soort} report beside the draft; run the check first. Nothing was changed.")
        verdict = P.lees_json(pad).get("verdict")
        if verdict != "GOEDGEKEUR":
            sys.exit(f"The {soort} report says {verdict}, not GOEDGEKEUR. Nothing was changed.")
        if os.path.getmtime(pad) < les_tyd:
            sys.exit(f"The {soort} report is older than the draft, so it checked an earlier "
                     f"version. Run the check again. Nothing was changed.")

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
        for merk in ("Readable copy", "Delivered", "could not be copied"):
            reels = [reel for reel in r.stdout.splitlines() if merk in reel]
            if reels:
                print(reels[0])
        shutil.rmtree(stash, ignore_errors=True)
        return 0
    print("The runner did not sign it off. The reports are back beside the draft, and a "
          f"copy is kept in {stash}. Last lines of the runner:")
    print("\n".join(r.stdout.splitlines()[-15:]))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

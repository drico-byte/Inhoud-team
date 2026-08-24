#!/usr/bin/env python3
"""
Read the logs and report the writer's systematic bias.

    python bin/logoorsig.py
    python bin/logoorsig.py --log logs/gate_log.jsonl --min 5

This is the instrument for improving the prompts. After roughly twenty lessons it
shows whether the writer under-supplies, drifts formal, or over-subordinates —
and each of those is one edit to skrywer-v1.x, not twenty per-lesson revisions.
A pattern here is a prompt fix; only a one-off is a lesson fix.

The volume figure to watch is words against *budget*, not words in the abstract.
The measured Wolkskool reference sample stopped at roughly two-thirds to
five-sixths of budget, so a mean ratio near 0.85 is the known failure mode and
means the depth instruction needs strengthening rather than the register.

Extends the starting version in the standard's references/opstelling.md.
"""
import argparse
import json
import os
import re
import statistics as st
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paaie as P  # noqa: E402

BANDE = {(4, 6): (11.0, 14.5, 1.52, 13.0),
         (7, 9): (13.0, 17.5, 1.62, 17.0),
         (10, 12): (15.0, 21.5, 1.72, 22.0)}


def band(graad):
    for (lo, hi), b in BANDE.items():
        if lo <= (graad or 0) <= hi:
            return b
    return None


def lees_jsonl(path):
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except ValueError:
                print(f"  (skipped unreadable line {n} of {P.rel(path)})")
    return rows


def teken(waarde, lo, hi, eenheid=""):
    """Mark whether a mean sits below, inside, or above the band."""
    if lo is None:
        return ""
    if waarde < lo:
        return f"   BELOW band {lo}–{hi}{eenheid} — choppy, not simple"
    if waarde > hi:
        return f"   ABOVE band {lo}–{hi}{eenheid}"
    return f"   in band {lo}–{hi}{eenheid}"


def hek_oorsig(rows, minimum):
    rows = [r for r in rows if r.get("study")]
    if not rows:
        print("  No gate runs with study text yet.\n")
        return
    n = len(rows)
    passes = sum(r.get("verdict") == "PASS" for r in rows)
    print(f"  runs {n}    pass rate {round(100 * passes / n)}%"
          f"    lessons {len({r.get('titel') for r in rows})}")
    if n < minimum:
        print(f"  Fewer than {minimum} runs — read this as anecdote, not as bias.")
    print()

    grade = Counter(r.get("graad") for r in rows)
    b = band(grade.most_common(1)[0][0]) if len(grade) == 1 else None
    lo, hi, syl, poly = b if b else (None, None, None, None)

    # --- volume against budget: the bias that matters most ---
    ratios, gaps = [], []
    for r in rows:
        beg = r.get("budget") or 0
        w = (r["study"] or {}).get("words") or 0
        if beg:
            ratios.append(w / beg)
            gaps.append(w - beg)
    if ratios:
        mr = st.mean(ratios)
        print(f"  words vs budget      mean {mr:.2f}x   "
              f"({st.mean(gaps):+.0f} words, min {min(ratios):.2f}x, "
              f"max {max(ratios):.2f}x)")
        if mr < 0.95:
            print("                       UNDER-SUPPLYING — strengthen the depth")
            print("                       instruction in the writer prompt, not the register.")
        elif mr > 1.05:
            print("                       OVER-SUPPLYING — learners revise more than a")
            print("                       textbook asks. Tighten, do not add scaffolding.")
            print("                       NOTE: this is the OPPOSITE of the documented")
            print("                       prediction. The human reference sample stopped at")
            print("                       0.67–0.83x budget, and the writer prompt is written")
            print("                       to correct under-supply. If over-supply holds across")
            print("                       lessons, that depth instruction is now overshooting")
            print("                       and the prompt needs loosening, not strengthening.")

    def reeks(sleutel, naam, lo=None, hi=None, eenheid=""):
        vals = [(r["study"] or {}).get(sleutel) for r in rows]
        vals = [v for v in vals if isinstance(v, (int, float))]
        if not vals:
            return
        m = st.mean(vals)
        print(f"  {naam:<20} mean {m:>6.2f}   "
              f"(min {min(vals)}, max {max(vals)}){teken(m, lo, hi, eenheid)}")

    reeks("mean_sentence_len", "words/sentence", lo, hi)
    reeks("mean_syllables", "syllables/word", None, syl)
    reeks("pct_polysyllabic", "3+ syllable %", None, poly)
    reeks("commas_per_sentence", "commas/sentence", None, 0.35)

    if b is None:
        print("  (grades are mixed in this log, so no single band is shown)")

    # --- what actually fails, and what merely warns ---
    def kop(text):
        # The same defect must group across lessons, so drop everything that
        # varies: the advice after the dash, the measured numbers, and the block
        # heading. Without this every failure is its own unique string and the
        # "most frequent" list says nothing.
        t = text.split(" — ")[0]
        t = re.sub(r"'[^']*'", "'…'", t)
        t = re.sub(r"\d+(?:\.\d+)?", "N", t)
        return re.sub(r"\s+", " ", t).strip()[:64]

    fouts = Counter(kop(f) for r in rows for f in (r.get("failures") or []))
    warns = Counter(kop(w) for r in rows for w in (r.get("warnings") or []))
    if fouts:
        print("\n  most frequent hard failures")
        for msg, c in fouts.most_common(6):
            print(f"    {c:>3}  {msg}")
    else:
        print("\n  no hard failures logged")
    if warns:
        print("\n  most frequent warnings")
        for msg, c in warns.most_common(6):
            print(f"    {c:>3}  {msg}")
    print()


def hardloop_oorsig(rows):
    if not rows:
        print("  No pipeline events logged yet.\n")
        return
    gebeure = Counter(r.get("gebeurtenis") for r in rows)
    print("  " + "   ".join(f"{k}={v}" for k, v in sorted(gebeure.items())))
    print()

    for naam in ("dekking", "feite"):
        verdicts = Counter(r.get("verdict") for r in rows
                           if r.get("gebeurtenis") == f"nasien_{naam}")
        if verdicts:
            print(f"  {naam:<10} " + "   ".join(f"{k}={v}" for k, v in verdicts.items()))
    onsound = [r for r in rows if r.get("gebeurtenis", "").startswith("nasien_")
               and r.get("sound") is False]
    if onsound:
        print(f"\n  {len(onsound)} malformed checker report(s) — the checker prompt is")
        print("  producing reports whose verdict does not follow from their findings.")

    esk = [r for r in rows if r.get("gebeurtenis") == "eskalasie"]
    if esk:
        print(f"\n  escalations ({len(esk)})")
        for r in esk[-8:]:
            print(f"    {r.get('wanneer','')[:16]}  {r.get('soort')}  {r.get('les')}")

    rev = Counter(r.get("bron") for r in rows if r.get("gebeurtenis") == "teruggestuur")
    if rev:
        print("\n  revisions requested by")
        for bron, c in rev.most_common():
            print(f"    {c:>3}  {bron}")
    print()


def main():
    ap = argparse.ArgumentParser(description="Report systematic bias from the logs")
    ap.add_argument("--log", default=P.GATE_LOG)
    ap.add_argument("--hardloop-log", default=P.HARDLOOP_LOG)
    ap.add_argument("--min", type=int, default=20,
                    help="runs below which the numbers are anecdote (default 20)")
    a = ap.parse_args()

    print(f"\nGATE — {P.rel(a.log)}\n")
    hek_oorsig(lees_jsonl(a.log), a.min)
    print(f"PIPELINE — {P.rel(a.hardloop_log)}\n")
    hardloop_oorsig(lees_jsonl(a.hardloop_log))
    print(f"Archived reports: {P.rel(P.VERSLAE)}/<les>/s<cycle>-<checker>.json\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

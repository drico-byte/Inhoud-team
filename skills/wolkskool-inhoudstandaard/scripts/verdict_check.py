#!/usr/bin/env python3
"""
Checker report validator.

Confirms a checker's report is structurally sound and — the part that matters —
that its verdict actually follows from its own findings. A checker that reports
three contradicted claims and then returns GOEDGEKEUR would otherwise sail
through, and its report is the only thing standing between an error and a learner.

USAGE
    python3 verdict_check.py report.json
    python3 verdict_check.py report.json --les lesson.json --spek lesse_entry.json

Exit 0 = report is sound. Exit 1 = report is malformed or self-contradictory.
Note this validates the REPORT, not the lesson. A sound report can carry a
HERSIEN verdict; that is a working pipeline, not an error.
"""
import argparse, json, sys

VERDICTS = {"GOEDGEKEUR", "HERSIEN", "MENS_NODIG"}
COVER_STATUS = {"teenwoordig", "gedeeltelik", "afwesig"}
FACT_STATUS = {"bevestig", "weerspreek", "onseker"}
COVER_TIPES = {"kern", "aanvulling", "eli10", "vraag", "fokus"}


def derive(report):
    """The verdict the findings actually support."""
    items = report.get("items", [])
    if report["nasiener"] == "dekking":
        if report.get("spesifikasie_probleem"):
            return "MENS_NODIG"
        if any(i.get("status") == "afwesig" and i.get("tipe") == "kern" for i in items):
            return "HERSIEN"
        if any(i.get("status") in {"afwesig", "gedeeltelik"} for i in items):
            return "HERSIEN"
        return "GOEDGEKEUR"
    if any(i.get("status") == "onseker" for i in items):
        return "MENS_NODIG"
    if any(i.get("status") == "weerspreek" for i in items):
        return "HERSIEN"
    return "GOEDGEKEUR"


def check(report, lesson=None, spec=None):
    """Validate a report. Pass the lesson and spec to also check COMPLETENESS.

    Without them, only internal consistency is verifiable — a checker that examined
    two claims out of thirty produces a perfectly consistent report. Skimming is a
    realistic failure and the reports are the only thing between an error and a
    learner, so supply both wherever the orchestrator can.
    """
    fails, warns = [], []

    for f in ["skema_weergawe", "nasiener", "prompt_weergawe", "les", "kaps_punt",
              "verdict", "items", "opsomming"]:
        if f not in report:
            fails.append(f"Missing required field: {f}")
    if fails:
        return {"sound": False, "failures": fails, "warnings": warns}

    if report["nasiener"] not in {"dekking", "feite"}:
        fails.append(f"nasiener must be 'dekking' or 'feite', got '{report['nasiener']}'")
        return {"sound": False, "failures": fails, "warnings": warns}
    if report["verdict"] not in VERDICTS:
        fails.append(f"verdict must be one of {sorted(VERDICTS)}, got '{report['verdict']}'")

    kind = report["nasiener"]
    items = report["items"]
    if not items:
        fails.append("items is empty — a checker that examined nothing cannot clear a lesson")

    for n, i in enumerate(items, 1):
        if kind == "dekking":
            for f in ["tipe", "verwysing", "status", "bewys"]:
                if f not in i:
                    fails.append(f"Coverage item {n}: missing '{f}'")
            if i.get("status") not in COVER_STATUS:
                fails.append(f"Coverage item {n}: status must be one of {sorted(COVER_STATUS)}")
            if i.get("tipe") not in COVER_TIPES:
                warns.append(f"Coverage item {n}: unexpected tipe '{i.get('tipe')}'")
            if i.get("status") in {"gedeeltelik", "afwesig"} and not i.get("aksie"):
                fails.append(f"Coverage item {n} is {i.get('status')} but has no 'aksie' — "
                             f"a defect the writer cannot act on comes back unfixed")
        else:
            for f in ["bewering", "blok", "status"]:
                if f not in i:
                    fails.append(f"Fact item {n}: missing '{f}'")
            if i.get("status") not in FACT_STATUS:
                fails.append(f"Fact item {n}: status must be one of {sorted(FACT_STATUS)}")
            if i.get("status") == "bevestig" and not i.get("bron"):
                fails.append(f"Fact item {n}: marked 'bevestig' with no source — verification "
                             f"from memory is the failure mode this checker exists to prevent")
            if i.get("status") == "weerspreek" and not i.get("regstelling"):
                fails.append(f"Fact item {n}: marked 'weerspreek' with no 'regstelling'")

    # coverage of the required checks
    if kind == "dekking":
        tipes = {i.get("tipe") for i in items}
        if "fokus" not in tipes:
            fails.append("No 'fokus' item — every lesson has a fokusvraag_skakel, so the "
                         "focus-question check was skipped")
        if "kern" not in tipes:
            fails.append("No 'kern' items — the core content check was not performed")
    else:
        if not any((i.get("tipe") == "superlatief") for i in items):
            warns.append("No item typed 'superlatief'. If the lesson contains no superlative "
                         "that is fine; if it does, this is the highest-risk category and was missed.")

    # --- completeness: did the checker actually look at everything? ---
    if lesson is not None:
        blocks = lesson.get("blokke", [])
        if kind == "feite":
            # every block carrying prose should appear among the checked claims
            seen = {(i.get("blok") or "").strip() for i in items}
            for b in blocks:
                if b.get("tipe") in {"studie", "eli10", "lys", "begrip", "vraag"}:
                    label = (b.get("kop") or b.get("vir") or b.get("term") or "").strip()
                    if label and label not in seen:
                        warns.append(f"No claim checked from block '{label[:34]}' — either it "
                                     f"contains nothing checkable, or it was skipped")
            if len(items) < max(4, len(blocks) // 2):
                warns.append(f"{len(items)} claims checked across {len(blocks)} blocks — low "
                             f"enough to suggest skimming rather than a claim-free lesson")
        else:
            eli = [b for b in blocks if b.get("tipe") == "eli10"]
            checked_eli = sum(1 for i in items if i.get("tipe") == "eli10")
            if len(eli) > checked_eli:
                warns.append(f"Lesson has {len(eli)} eli10 blocks but only {checked_eli} were "
                             f"checked")

    if spec is not None and kind == "dekking":
        # Count is deterministic, so it can fail. Which item is missing depends on
        # string matching against a checker's own wording, which is heuristic — a
        # legitimate paraphrase would otherwise be failed for phrasing rather than
        # for omission. So: fail on the count, warn on the name.
        spec_kern = spec.get("kern", [])
        report_kern = [i for i in items if i.get("tipe") == "kern"]
        if len(report_kern) < len(spec_kern):
            fails.append(f"Spec lists {len(spec_kern)} kern items but the report checks "
                         f"{len(report_kern)} — a coverage report that examines fewer "
                         f"requirements than the spec contains cannot clear the lesson")

        checked = " ".join((i.get("verwysing") or "").lower() for i in items)
        for k in spec_kern:
            words = [w for w in k.lower().split() if len(w) > 4]
            if words and not any(w in checked for w in words):
                warns.append(f"No report item obviously matches kern '{k[:40]}' — check by eye; "
                             f"the checker may have worded it differently")
        for a in spec.get("aanvulling", []) or []:
            item = (a.get("item") or "").lower()
            words = [w for w in item.split() if len(w) > 4]
            if words and not any(w in checked for w in words):
                warns.append(f"Spec aanvulling item not checked: '{a.get('item','')[:40]}'")
        for m in spec.get("moeilike_konsepte", []) or []:
            words = [w for w in m.lower().split() if len(w) > 4]
            if words and not any(w in checked for w in words):
                warns.append(f"Flagged difficult concept not checked for an eli10 block: "
                             f"'{m[:40]}'")

    # --- the substantive check: does the verdict follow from the findings? ---
    if report.get("verdict") in VERDICTS:
        expected = derive(report)
        if report["verdict"] != expected:
            fails.append(f"Verdict '{report['verdict']}' does not follow from the findings, "
                         f"which support '{expected}'")

    return {"sound": not fails, "nasiener": kind, "verdict": report.get("verdict"),
            "derived": derive(report) if report.get("verdict") in VERDICTS else None,
            "items": len(items), "failures": fails, "warnings": warns}


def main():
    ap = argparse.ArgumentParser(description="Validate a checker report")
    ap.add_argument("report")
    ap.add_argument("--les", default=None, help="the lesson JSON, to check completeness")
    ap.add_argument("--spek", default=None,
                    help="the lesse entry from the spec, to check every requirement was examined")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    lesson = json.load(open(a.les, encoding="utf-8")) if a.les else None
    spec = json.load(open(a.spek, encoding="utf-8")) if a.spek else None
    r = check(json.load(open(a.report, encoding="utf-8")), lesson, spec)
    if lesson is None and spec is None:
        r.setdefault("warnings", []).append(
            "Neither --les nor --spek supplied: only internal consistency was checked, "
            "not whether the checker examined everything.")

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'SOUND' if r['sound'] else 'MALFORMED'}  —  {r.get('nasiener','?')} report, "
              f"verdict {r.get('verdict','?')}, {r.get('items','?')} items")
        for x in r["failures"]:
            print(f"\n  FAIL  {x}")
        for x in r["warnings"]:
            print(f"  warn  {x}")
        print()

    sys.exit(0 if r["sound"] else 1)


if __name__ == "__main__":
    main()

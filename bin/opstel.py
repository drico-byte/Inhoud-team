#!/usr/bin/env python3
"""
Local setup and prerequisite check. Run once after cloning, and any time
something stops working.

    python bin/opstel.py

It does four things and reports on a fifth:

1. Creates the scratch directory. The profiler rasterises pages and writes
   hundreds of OCR temp files per run, and those must land outside the repository
   and outside any synced folder such as OneDrive.
2. Creates bronne/ for textbook PDFs and kaps/dokumente/ for CAPS documents.
   Both are gitignored, and stay that way.
3. Links the content standard into .claude/skills/ so Claude Code discovers it.
   The canonical copy stays at skills/wolkskool-inhoudstandaard/.
5. Checks the prerequisites and tells you what, if anything, is missing.
"""
import json
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "bin"))

from paaie import (  # noqa: E402  (path setup must precede the import)
    SKILL_NAME, hunspell_pad, skrapruimte,
)

OK, WARN, BAD = "  ok  ", " note ", " FAIL "


def line(tag, msg):
    print(f"{tag}  {msg}")


def make_dir(path, what):
    existed = os.path.isdir(path)
    os.makedirs(path, exist_ok=True)
    line(OK, f"{what}: {path}" + ("" if existed else "   (created)"))


def link_skill():
    """Make the standard discoverable to Claude Code without duplicating it.

    Claude Code loads project skills from .claude/skills/<name>/SKILL.md only. The
    canonical copy lives at skills/<name>/ because that is where the standard is
    versioned and reviewed, so this is a directory junction rather than a second
    copy — two copies of a standard is how the two drift apart.
    """
    target = os.path.join(REPO, "skills", SKILL_NAME)
    link = os.path.join(REPO, ".claude", "skills", SKILL_NAME)
    if not os.path.isdir(target):
        line(BAD, f"the standard is missing from {target}")
        return False

    os.makedirs(os.path.dirname(link), exist_ok=True)
    if os.path.exists(os.path.join(link, "SKILL.md")):
        line(OK, f"skill discoverable at .claude/skills/{SKILL_NAME}")
        return True
    if os.path.exists(link) or os.path.islink(link):
        line(WARN, f"removing a stale .claude/skills/{SKILL_NAME}")
        try:
            os.rmdir(link)
        except OSError:
            shutil.rmtree(link, ignore_errors=True)

    if os.name == "nt":
        # A junction needs no administrator rights, unlike a symbolic link.
        r = subprocess.run(["cmd", "/c", "mklink", "/J", link, target],
                           capture_output=True, text=True)
        made = r.returncode == 0
        err = (r.stderr or r.stdout).strip()
    else:
        try:
            os.symlink(target, link)
            made, err = True, ""
        except OSError as e:
            made, err = False, str(e)

    if made:
        line(OK, f"linked .claude/skills/{SKILL_NAME} -> skills/{SKILL_NAME}")
        return True
    line(BAD, f"could not link the skill into .claude/skills/  ({err})")
    print("        Without this, Claude Code will not find the standard and the")
    print("        four agents will run without it. Create the link by hand:")
    print(f'          mklink /J "{link}" "{target}"')
    return False


def check_binary(name, what, needed_for):
    path = shutil.which(name)
    if path:
        line(OK, f"{what}: {path}")
        return True
    line(WARN, f"{what} not on PATH — needed for {needed_for}")
    return False


def main():
    print("\nWolkskool content pipeline — local setup\n")

    make_dir(skrapruimte(), "scratch (OCR intermediates, never in the repo)")
    make_dir(os.path.join(REPO, "bronne"), "textbook input (gitignored)")
    make_dir(os.path.join(REPO, "kaps", "dokumente"), "CAPS documents (gitignored)")
    # One folder per phase. The names carry the grade range because the register
    # bands in the standard are defined by grade, not by phase name, and the two
    # vocabularies have to be readable against each other at a glance.
    for fase in ("intersen-gr4-6", "senior-gr7-9", "fet-gr10-12"):
        make_dir(os.path.join(REPO, "kaps", "dokumente", fase), f"CAPS: {fase}")
    ok_skill = link_skill()

    print("\nPrerequisites\n")
    ok = True
    for mod in ("pyphen", "spylls"):
        try:
            __import__(mod)
            line(OK, f"python module {mod}")
        except ImportError:
            line(BAD, f"python module {mod} missing — pip install {mod}")
            ok = False

    ok_ocr = check_binary("tesseract", "tesseract", "the profiler (OCR)")
    check_binary("pdftoppm", "poppler pdftoppm", "the profiler (rasterising pages)")
    check_binary("pdfinfo", "poppler pdfinfo", "the profiler (page count)")

    if ok_ocr:
        langs = subprocess.run(["tesseract", "--list-langs"],
                               capture_output=True, text=True)
        have = {l.strip() for l in langs.stdout.splitlines()[1:] if l.strip()}
        missing = {"afr", "osd"} - have
        if missing:
            line(BAD, f"tesseract language data missing: {', '.join(sorted(missing))}")
            ok = False
        else:
            line(OK, "tesseract language data: afr, osd")

    dic = hunspell_pad()
    if dic:
        line(OK, f"Afrikaans hunspell dictionary: {dic}")
    else:
        line(WARN, "Afrikaans hunspell dictionary not installed — spelling is a "
                   "warning-level check, so the gate runs normally without it")

    print()
    if not ok or not ok_skill:
        print("Something above needs fixing before the pipeline will run.\n")
        return 1
    print("Ready.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

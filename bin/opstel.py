#!/usr/bin/env python3
"""
Local setup and prerequisite check. Run once after cloning, and any time
something stops working.

    python bin/opstel.py

It does five things and reports on a sixth:

1. Creates the scratch directory. The profiler rasterises pages and writes
   hundreds of OCR temp files per run, and those must land outside the repository
   and outside any synced folder such as OneDrive.
2. Creates bronne/ for textbook PDFs and kaps/dokumente/ for CAPS documents.
   Both are gitignored, and stay that way.
3. Links the content standard into .claude/skills/ so Claude Code discovers it.
   The canonical copy stays at skills/wolkskool-inhoudstandaard/.
4. Links Claude Code's memory folder to geheue/, so the project's notes are
   versioned and backed up with the work they describe.
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


def make_junction(link, target):
    """Point link at target without copying anything. Returns (made, error)."""
    if os.name == "nt":
        # A junction needs no administrator rights, unlike a symbolic link.
        r = subprocess.run(["cmd", "/c", "mklink", "/J", link, target],
                           capture_output=True, text=True)
        return r.returncode == 0, (r.stderr or r.stdout).strip()
    try:
        os.symlink(target, link)
        return True, ""
    except OSError as e:
        return False, str(e)


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

    # Check that it is really the SAME directory, not merely that a SKILL.md
    # exists there. This test used to be `if SKILL.md exists: ok`, and that is how
    # a junction quietly became a second copy: once any real directory sat at the
    # link path, the script reported "ok" forever and never noticed the two
    # diverging. On 7 September 2026 the copy was missing a whole day's changes --
    # the Grade 4 budget band, the floor exception, and the entire Sosiale
    # Wetenskappe exception -- and four planner agents in a row loaded the stale
    # standard. Two of them noticed and said so; the specs came out right only
    # because their briefs happened to carry the new rules explicitly.
    if os.path.exists(link):
        if os.path.realpath(link) == os.path.realpath(target):
            line(OK, f"skill discoverable at .claude/skills/{SKILL_NAME}")
            return True
        line(WARN, f".claude/skills/{SKILL_NAME} is a SEPARATE COPY, not a link to "
                   f"skills/{SKILL_NAME} — replacing it")
        print("        Agents load the copy under .claude/skills/, so a copy that")
        print("        drifts means they read a standard nobody is editing.")
    if os.path.exists(link) or os.path.islink(link):
        try:
            # os.rmdir removes a junction without touching what it points at.
            # shutil.rmtree on a junction can follow it and delete the real
            # standard, so it is only ever the fallback for a real directory.
            os.rmdir(link)
        except OSError:
            if os.path.realpath(link) == os.path.realpath(target):
                line(BAD, "refusing to delete the standard itself")
                return False
            shutil.rmtree(link, ignore_errors=True)

    made, err = make_junction(link, target)
    if made:
        line(OK, f"linked .claude/skills/{SKILL_NAME} -> skills/{SKILL_NAME}")
        return True
    line(BAD, f"could not link the skill into .claude/skills/  ({err})")
    print("        Without this, Claude Code will not find the standard and the")
    print("        four agents will run without it. Create the link by hand:")
    print(f'          mklink /J "{link}" "{target}"')
    return False


def link_memory():
    """Keep the project's memory notes in the repository, not in a user folder.

    Claude Code reads and writes its memory at
    .claude/projects/<project-path-as-a-name>/memory/, which is outside this
    repository, is not backed up with the work it describes, and is orphaned the
    moment the project directory is moved or renamed, because that folder's name
    is derived from the path. The notes record decisions that are not recoverable
    from the files -- why a word was rejected, which classification was contested,
    what a term plan got wrong -- so they belong with the work.

    The canonical copy therefore lives at geheue/ and the memory path is a
    junction back to it, the same arrangement and for the same reason as the
    skill above. Nothing is duplicated, so nothing can drift.
    """
    target = os.path.join(REPO, "geheue")
    # Claude Code names the folder after the path: the drive colon and every
    # separator become a dash, and so does every space. "C:\Users\x" therefore
    # gives "C--Users-x" on its own -- prepending "C--" as this line used to do
    # produced "C--C--Users-x", a folder Claude Code never reads, and the working
    # junction had to be made by hand. The space rule matters now that the repo
    # lives under a directory whose name contains one.
    key = (REPO.replace(":", "-").replace(os.sep, "-").replace(" ", "-")
               .lstrip("-"))
    link = os.path.join(os.path.expanduser("~"), ".claude", "projects", key, "memory")

    if not os.path.isdir(target):
        line(WARN, "no geheue/ yet -- it appears the first time a note is written")
        return True
    if os.path.exists(os.path.join(link, "MEMORY.md")):
        line(OK, "memory notes served from geheue/")
        return True
    if os.path.exists(link) or os.path.islink(link):
        line(BAD, "a real memory folder already exists at that path")
        print("        It holds notes this repository does not. Merge it into")
        print(f"        geheue/ by hand first, then delete it:")
        print(f"          {link}")
        return False

    os.makedirs(os.path.dirname(link), exist_ok=True)
    made, err = make_junction(link, target)
    if made:
        line(OK, "linked the memory path -> geheue/")
        return True
    line(WARN, f"could not link the memory path  ({err})")
    print("        Notes will still be written, but to a user folder outside")
    print("        this repository, so they will not be backed up with it:")
    print(f'          mklink /J "{link}" "{target}"')
    return True


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
    link_memory()

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

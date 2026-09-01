#!/usr/bin/env python3
"""
Pull the plain text out of a .docx, so a video script can be read and distilled.

The video scripts for Grade 4 Sosiale Wetenskappe arrive as Word documents. They
are Wolkskool's own writing, so there is no rights question -- but a script is
still an INPUT and never goes to an agent raw. See "When the video was made
first" in the content standard: the script gets read here, its claims get
checked, and only a distilled `video_naat` object reaches a specification.

    python bin/docxteks.py "<file.docx>"
    python bin/docxteks.py "<file.docx>" --uit videoskrifte/vervoer.txt

No dependencies: a .docx is a zip holding word/document.xml.
"""
import argparse
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def paragrawe(pad):
    """Yield one string per Word paragraph, in document order."""
    with zipfile.ZipFile(pad) as z:
        try:
            rou = z.read("word/document.xml")
        except KeyError:
            sys.exit(f"{pad} has no word/document.xml -- is it really a .docx?")
    wortel = ET.fromstring(rou)
    for p in wortel.iter(f"{W}p"):
        dele = []
        for k in p.iter():
            if k.tag == f"{W}t":
                dele.append(k.text or "")
            elif k.tag == f"{W}tab":
                dele.append("\t")
            elif k.tag in (f"{W}br", f"{W}cr"):
                dele.append("\n")
        teks = "".join(dele).strip()
        # A bulleted paragraph carries its marker in the numbering part, not in
        # the text, so the bullet is lost. Mark it, because a script's bullets are
        # usually the list of things an animal or a machine can do -- which is
        # exactly what a lesson has to cover.
        if teks and p.find(f".//{W}numPr") is not None:
            teks = "- " + teks
        yield teks


def main():
    ap = argparse.ArgumentParser(description="Plain text out of a .docx")
    ap.add_argument("docx")
    ap.add_argument("--uit", help="write here instead of to the screen")
    a = ap.parse_args()

    if not os.path.exists(a.docx):
        sys.exit(f"no such file: {a.docx}")

    uit, leeg = [], 0
    for para in paragrawe(a.docx):
        if para:
            uit.append(para)
            leeg = 0
        else:
            leeg += 1
            if leeg == 1:
                uit.append("")
    teks = re.sub(r"\n{3,}", "\n\n", "\n".join(uit)).strip() + "\n"

    if a.uit:
        os.makedirs(os.path.dirname(a.uit) or ".", exist_ok=True)
        with open(a.uit, "w", encoding="utf-8") as fh:
            fh.write(teks)
        print(f"{len(teks.split())} woorde -> {a.uit}")
    else:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        print(teks)


if __name__ == "__main__":
    main()

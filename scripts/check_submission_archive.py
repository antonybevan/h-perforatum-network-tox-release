#!/usr/bin/env python3
"""Verify the manuscript submission-source archives.

For each archive this gate confirms:
  1. the archive exists;
  2. required compile inputs are present (main.tex, main.bbl, bib, key sections);
  3. forbidden artefacts are absent (aux/log/out/fls/fdb, PDFs, hidden files,
     flattened duplicate .tex);
  4. its bundled main.tex / main.bbl match the current committed source (i.e.
     the archive is not stale);
  5. no stale result values remain in the bundled .tex;
  6. no absolute local paths leak in any text member;
  7. (optional) the extracted source compiles to a PDF, if latexmk is available.

Exit 0 = PASS, non-zero = FAIL.  Run:  python scripts/check_submission_archive.py
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

MANU = Path(__file__).resolve().parent.parent / "manuscript"

# archive name -> the committed top-level source its bundled main.tex must equal
ARCHIVES = {
    "submission_source_identified.zip": ("main.tex", "main.bbl"),
    "submission_source_anonymous.zip": ("main_anonymous.tex", "main_anonymous.bbl"),
}

REQUIRED_MEMBERS = {
    "main.tex",
    "main.bbl",
    "references.bib",
    "references_extra.bib",
    "sections/abstract.tex",
    "sections/results.tex",
    "sections/supplementary.tex",
}
# Build/aux artefacts and raster figures never belong in the source archive.
# (Figure PDFs are legitimate compile inputs and are handled separately below.)
FORBIDDEN_EXT = {".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".synctex.gz",
                 ".tiff", ".DS_Store"}

# Stale result fragments from the pre-correction manuscript. Specific enough not
# to collide with DOIs/page numbers; scanned only in .tex members.
STALE_PATTERNS = [r"\+?12\.08", r"\+?11\.20", r"\+?8\.98",
                  r"5\.57\$? \(RWR\)", r"3\.19\$? \(EWI\)"]
ABS_PATH = re.compile(r"/Users/|/home/|[A-Z]:\\\\")

failures: list[str] = []


def fail(msg):
    print(f"  FAIL  {msg}")
    failures.append(msg)


def ok(msg):
    print(f"  OK    {msg}")


def check_archive(name, expected_main, expected_bbl):
    print(f"\n== {name} ==")
    path = MANU / name
    if not path.is_file():
        fail(f"{name} does not exist (run build_submission_archives.py)")
        return

    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        blobs = {n: z.read(n) for n in names}

    # 2. required members
    for req in sorted(REQUIRED_MEMBERS):
        (ok if req in names else fail)(f"{name}: contains {req}")

    # 3. forbidden artefacts / hidden files
    for n in sorted(names):
        base = n.rsplit("/", 1)[-1]
        if Path(n).suffix in FORBIDDEN_EXT:
            fail(f"{name}: forbidden artefact {n}")
        # PDFs are allowed only as figures/ compile inputs, never a bundled
        # compiled manuscript or a stale flattened PDF.
        if Path(n).suffix == ".pdf" and not n.startswith("figures/"):
            fail(f"{name}: unexpected non-figure PDF {n}")
        if base.startswith(".") and base:
            fail(f"{name}: hidden file {n}")
        if n.count("/") == 0 and n.endswith(".tex") and n != "main.tex":
            fail(f"{name}: flattened duplicate top-level .tex {n}")

    # 4. currency: bundled main.tex/main.bbl match committed source
    for member, src in [("main.tex", expected_main), ("main.bbl", expected_bbl)]:
        src_path = MANU / src
        if not src_path.is_file():
            fail(f"{name}: committed source {src} is missing (cannot verify archive currency)")
            continue
        if blobs.get(member) == src_path.read_bytes():
            ok(f"{name}: {member} matches committed {src}")
        else:
            fail(f"{name}: {member} does NOT match committed {src} (stale archive)")

    # 5. stale values in .tex members
    stale_hit = False
    for n, blob in blobs.items():
        if not n.endswith(".tex"):
            continue
        text = blob.decode("utf-8", "ignore")
        for pat in STALE_PATTERNS:
            if re.search(pat, text):
                fail(f"{name}: stale value /{pat}/ in {n}")
                stale_hit = True
    if not stale_hit:
        ok(f"{name}: no stale result values in bundled .tex")

    # 6. absolute local paths in any text member
    path_hit = False
    for n, blob in blobs.items():
        if Path(n).suffix not in {".tex", ".bib", ".bbl"}:
            continue
        if ABS_PATH.search(blob.decode("utf-8", "ignore")):
            fail(f"{name}: absolute local path in {n}")
            path_hit = True
    if not path_hit:
        ok(f"{name}: no absolute local paths")

    # 7. optional compile from extracted source
    if shutil.which("latexmk"):
        with tempfile.TemporaryDirectory() as td:
            with zipfile.ZipFile(path) as z:
                z.extractall(td)
            proc = subprocess.run(
                ["latexmk", "-pdf", "-halt-on-error", "-interaction=nonstopmode", "main.tex"],
                cwd=td, capture_output=True, text=True,
            )
            if proc.returncode == 0 and (Path(td) / "main.pdf").is_file():
                ok(f"{name}: extracted source compiles to main.pdf")
            else:
                tail = "\n".join(proc.stdout.splitlines()[-8:])
                fail(f"{name}: extracted source failed to compile\n{tail}")
    else:
        print(f"  SKIP  {name}: latexmk not available; compile check skipped")


def main():
    for name, (m, b) in ARCHIVES.items():
        check_archive(name, m, b)
    print()
    if failures:
        print(f"RESULT: FAIL ({len(failures)} issue(s))")
        sys.exit(1)
    print("RESULT: PASS -- submission archives complete, current, and clean")
    sys.exit(0)


if __name__ == "__main__":
    main()

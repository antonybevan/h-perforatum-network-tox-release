#!/usr/bin/env python3
"""Deterministically build the Zenodo reproducibility-snapshot archive.

The snapshot is a full repository archive of the *committed* project (code,
data, results, figures, manuscript) for long-term citation under the concept
DOI.  It is built from ``git ls-files`` -- i.e. exactly the version-controlled
file set -- so working-tree scratch directories (``scratch_id/``,
``scratch_anon/``, ``.gemini_scratch/``) and LaTeX build logs, all of which are
git-ignored, are structurally excluded.  A prior hand-zipped snapshot swept
those in; building from the tracked set makes that impossible.

Output (written to the repo root by default):

  h-perforatum-network-tox-release_zenodo_snapshot_v<version>_<date>.zip
  h-perforatum-network-tox-release_zenodo_snapshot_v<version>_<date>.zip.sha256

Every member lives under a top-level ``h-perforatum-network-tox-release/``
directory.  Archives are byte-reproducible: members are sorted, timestamps and
permissions are fixed, so re-running on the same commit yields an identical
SHA-256.

Run from anywhere:  python scripts/build_zenodo_snapshot.py
Options:  --version X.Y.Z  --date YYYY-MM-DD  --outdir PATH
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOP = "h-perforatum-network-tox-release"

# Deterministic timestamp for every archive member (reproducible bytes).
FIXED_DT = (2020, 1, 1, 0, 0, 0)

# Defensive backstop: even if one of these were ever accidentally tracked, it
# must never enter the citable snapshot. git-ignored paths are already excluded
# by using `git ls-files`; this is belt-and-braces.
# Software-only deposit: the manuscript LaTeX, cover letter, and submission-only
# material are never part of the citable code+data archive. git-tracked files are
# already manuscript-free (manuscript/ is git-ignored); these are belt-and-braces.
EXCLUDE_PREFIXES = (
    "scratch_id/", "scratch_anon/", ".gemini_scratch/", "tmp/",
    "manuscript/",
    "scripts/build_submission_archives.py", "scripts/check_submission_archive.py",
)
EXCLUDE_SUFFIXES = (".blg", ".log", ".aux", ".out", ".fls", ".fdb_latexmk")


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        check=True, capture_output=True, text=True,
    ).stdout
    files = [p for p in out.split("\0") if p]
    kept = [
        p for p in files
        if not p.startswith(EXCLUDE_PREFIXES) and not p.endswith(EXCLUDE_SUFFIXES)
    ]
    return sorted(kept)


def read_version_date() -> tuple[str, str]:
    """Read version and date-released from CITATION.cff (no YAML dependency)."""
    text = (ROOT / "CITATION.cff").read_text()
    ver = re.search(r'^version:\s*"?([^"\n]+)"?', text, re.MULTILINE)
    date = re.search(r'^date-released:\s*"?([^"\n]+)"?', text, re.MULTILINE)
    if not ver or not date:
        raise SystemExit("[build] could not read version/date-released from CITATION.cff")
    return ver.group(1).strip(), date.group(1).strip()


def build(version: str, date: str, outdir: Path) -> Path:
    members = tracked_files()
    missing = [p for p in members if not (ROOT / p).is_file()]
    if missing:
        raise SystemExit(f"[build] tracked files missing from working tree: {missing}")

    name = f"{TOP}_zenodo_snapshot_v{version}_{date}.zip"
    out = outdir / name
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for rel in members:
            info = zipfile.ZipInfo(f"{TOP}/{rel}", date_time=FIXED_DT)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, (ROOT / rel).read_bytes())

    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    (outdir / f"{name}.sha256").write_text(f"{digest}  {out}\n")
    print(f"built {out}  ({len(members)} files)")
    print(f"sha256 {digest}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    cff_ver, cff_date = read_version_date()
    ap.add_argument("--version", default=cff_ver, help="release version (default: CITATION.cff)")
    ap.add_argument("--date", default=cff_date, help="release date YYYY-MM-DD (default: CITATION.cff)")
    ap.add_argument("--outdir", default=str(ROOT), help="output directory (default: repo root)")
    args = ap.parse_args()
    outdir = Path(args.outdir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    build(args.version, args.date, outdir)


if __name__ == "__main__":
    main()

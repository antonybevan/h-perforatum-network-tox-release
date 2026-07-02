#!/usr/bin/env python3
"""Deterministically build the manuscript submission-source archives.

Two archives are built from an EXPLICIT manifest (never from the dirty working
tree), one per submission mode:

  manuscript/submission_source_identified.zip  -- final / camera-ready source
  manuscript/submission_source_anonymous.zip   -- double-blind review source

In both archives the primary LaTeX file is named ``main.tex`` (submission
systems expect this) and the matching bibliography is included as ``main.bbl``
so the source compiles without a bibtex/network round-trip. The anonymous
archive's ``main.tex`` is the anonymized manuscript, which \\input's the
``*_anonymous`` availability/declarations sections.

Only files required to compile the submitted manuscript are included; no stale
flattened duplicates, no PDFs, no aux/log artefacts, no local paths. Archives
are byte-reproducible: fixed member order, fixed timestamps, fixed permissions.

Run from anywhere:  python scripts/build_submission_archives.py
"""
from __future__ import annotations

import zipfile
from pathlib import Path

MANU = Path(__file__).resolve().parent.parent / "manuscript"

# Sources shared by both builds (as \input by main.tex / main_anonymous.tex).
SHARED_SECTIONS = [
    "sections/abstract.tex",
    "sections/introduction.tex",
    "sections/results.tex",
    "sections/discussion.tex",
    "sections/methods.tex",
    "sections/supplementary.tex",
]
FIGURES = [
    "figures/fig1_lollipop.pdf",
    "figures/fig2_dumbbell.pdf",
    "figures/fig3_ewi_waterfall.pdf",
    "figures/fig4_ptni_phase.pdf",
    "figures/fig5_bootstrap.pdf",
    "figures/fig6_chemsim.pdf",
    "figures/fig7_leakage.pdf",
    "figures/fig8_opregime.pdf",
]
BIB = ["references.bib", "references_extra.bib"]

# Per-build differences: which top-level source is the primary main.tex, which
# .bbl matches it, and which variant of the availability/declarations sections
# that main.tex \input's.
BUILDS = {
    "submission_source_identified.zip": {
        "main": "main.tex",
        "bbl": "main.bbl",
        "extra_sections": [
            "sections/data_availability.tex",
            "sections/code_availability.tex",
            "sections/declarations.tex",
        ],
    },
    "submission_source_anonymous.zip": {
        "main": "main_anonymous.tex",
        "bbl": "main_anonymous.bbl",
        "extra_sections": [
            "sections/data_availability_anonymous.tex",
            "sections/code_availability_anonymous.tex",
            "sections/declarations_anonymous.tex",
        ],
    },
}

# Deterministic timestamp for every archive member (reproducible bytes).
FIXED_DT = (2020, 1, 1, 0, 0, 0)


def _manifest(spec):
    """Return sorted (arcname, source_path) members for one build."""
    members = [
        ("main.tex", MANU / spec["main"]),
        ("main.bbl", MANU / spec["bbl"]),
    ]
    for rel in SHARED_SECTIONS + spec["extra_sections"] + FIGURES + BIB:
        members.append((rel, MANU / rel))
    members.sort(key=lambda m: m[0])
    return members


def build(zip_name, spec):
    members = _manifest(spec)
    missing = [str(p) for _, p in members if not p.is_file()]
    if missing:
        raise SystemExit(f"[build] missing source files for {zip_name}: {missing}")

    out = MANU / zip_name
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for arcname, path in members:
            info = zipfile.ZipInfo(arcname, date_time=FIXED_DT)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, path.read_bytes())
    return out, [m[0] for m in members]


def main():
    for name, spec in BUILDS.items():
        out, names = build(name, spec)
        print(f"built {out.relative_to(MANU.parent)}  ({len(names)} files)")
        for n in names:
            print(f"    {n}")
        print()


if __name__ == "__main__":
    main()

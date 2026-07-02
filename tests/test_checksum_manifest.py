"""Checksum-manifest coverage (audit patch 1).

Anti-fraud invariant: every data/result artifact that feeds a release gate must
be pinned in ``data/CHECKSUMS.sha256``. Otherwise a gated file could be edited
to match the manuscript while ``sha256sum -c`` never notices.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "CHECKSUMS.sha256"

# Artifacts read by the honesty gate (verify_numbers.py) and the result-table
# tests. Each must be checksum-pinned.
GATE_INPUTS = [
    "data/processed/targets_lcc.csv",
    "data/processed/dili_900_lcc.csv",
    "data/processed/network_900_liver_lcc.parquet",
    "data/external/DILIrank_2.0.xlsx",
    "results/leakage_null_distributions.csv",
    "results/bootstrap_sensitivity.csv",
    "results/chemical_similarity_control.csv",
]


def _manifest_paths():
    paths = set()
    for line in MANIFEST.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        _, path = line.split(maxsplit=1)
        paths.add(path.strip())
    return paths


@pytest.mark.parametrize("rel", GATE_INPUTS)
def test_gate_input_is_checksummed(rel):
    assert rel in _manifest_paths(), (
        f"{rel} feeds a release gate but is absent from CHECKSUMS.sha256"
    )


def test_every_committed_result_table_is_checksummed():
    manifest = _manifest_paths()
    for csv in sorted((ROOT / "results" / "tables").glob("*.csv")):
        rel = csv.relative_to(ROOT).as_posix()
        assert rel in manifest, f"{rel} is a committed result table but not checksummed"

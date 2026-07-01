#!/usr/bin/env python3
"""
Provenance: programmatic retrieval of Quercetin protein targets from ChEMBL.

This documents and reproduces the retrieval that produced the Quercetin rows of
``data/raw/targets_raw.csv`` (the rows whose ``source`` column is ``ChEMBL_API``).

The committed snapshot was retrieved from **ChEMBL v31** (Quercetin =
``CHEMBL159``). Because the ChEMBL REST API serves the *current* release, re-running
this script against a newer release can return a slightly different target set.
The committed snapshot therefore remains the *authoritative* input; this script
provides methodological provenance plus a verification mode, and it never
overwrites the committed file.

Query definition (matches the committed snapshot):

  * Molecule        : Quercetin (ChEMBL ID ``CHEMBL159``)
  * Target organism : Homo sapiens
  * Activity types  : IC50, Ki, EC50
  * Potency cutoff  : ``standard_value <= 10 uM`` (10,000 nM), ``standard_units == 'nM'``
  * Target mapping  : ChEMBL target -> UniProt accession(s) via ``target_components``

Usage::

  python scripts/retrieve_chembl_targets.py --verify        # diff vs committed snapshot
  python scripts/retrieve_chembl_targets.py --out PATH      # write a fresh (non-authoritative) retrieval

Requires network access and the ``requests`` dependency (already pinned in
``requirements-lock.txt``).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import requests

CHEMBL_BASE = "https://www.ebi.ac.uk/chembl/api/data"
EBI_ROOT = "https://www.ebi.ac.uk"
QUERCETIN_CHEMBL_ID = "CHEMBL159"
ACTIVITY_TYPES = {"IC50", "Ki", "EC50"}
POTENCY_CUTOFF_NM = 10_000.0  # 10 uM
SNAPSHOT_VERSION = "31"

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = ROOT / "data" / "raw" / "targets_raw.csv"


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    return s


def fetch_activities(session: requests.Session, chembl_id: str):
    """Yield activity records for a molecule, following ChEMBL REST pagination."""
    url = f"{CHEMBL_BASE}/activity.json"
    params = {"molecule_chembl_id": chembl_id, "limit": 1000, "offset": 0}
    while url:
        resp = session.get(url, params=params, timeout=60)
        resp.raise_for_status()
        payload = resp.json()
        yield from payload.get("activities", [])
        nxt = payload.get("page_meta", {}).get("next")
        if nxt:
            url, params = EBI_ROOT + nxt, None  # `next` already encodes the query
        else:
            url = None


def target_to_uniprot(session: requests.Session, target_chembl_id: str, cache: dict) -> list:
    """Resolve a ChEMBL target id to its UniProt accession(s)."""
    if target_chembl_id in cache:
        return cache[target_chembl_id]
    resp = session.get(f"{CHEMBL_BASE}/target/{target_chembl_id}.json", timeout=60)
    resp.raise_for_status()
    comps = resp.json().get("target_components", [])
    accs = [c["accession"] for c in comps if c.get("accession")]
    cache[target_chembl_id] = accs
    return accs


def retrieve(chembl_id: str = QUERCETIN_CHEMBL_ID) -> list:
    """Return the sorted, de-duplicated UniProt accessions matching the query."""
    session = _session()
    cache: dict = {}
    accessions: set = set()
    for act in fetch_activities(session, chembl_id):
        if act.get("target_organism") != "Homo sapiens":
            continue
        if act.get("standard_type") not in ACTIVITY_TYPES:
            continue
        if act.get("standard_units") != "nM":
            continue
        value = act.get("standard_value")
        try:
            if value is None or float(value) > POTENCY_CUTOFF_NM:
                continue
        except (TypeError, ValueError):
            continue
        target = act.get("target_chembl_id")
        if not target:
            continue
        accessions.update(target_to_uniprot(session, target, cache))
    return sorted(accessions)


def load_snapshot_quercetin() -> list:
    """UniProt accessions for Quercetin in the committed ChEMBL_API snapshot."""
    accs = set()
    with SNAPSHOT.open(newline="") as fh:
        for row in csv.DictReader(fh):
            if row["compound"] == "Quercetin" and row["source"] == "ChEMBL_API":
                accs.add(row["protein_id"])
    return sorted(accs)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Reproduce / verify the Quercetin ChEMBL target retrieval."
    )
    ap.add_argument("--verify", action="store_true",
                    help="diff a fresh retrieval against the committed snapshot")
    ap.add_argument("--out", type=Path,
                    help="write a fresh retrieval to this path (never the committed snapshot)")
    args = ap.parse_args()

    if not args.verify and not args.out:
        ap.error("specify --verify and/or --out")
    if args.out and args.out.resolve() == SNAPSHOT.resolve():
        ap.error("refusing to overwrite the authoritative snapshot data/raw/targets_raw.csv")

    print(f"Retrieving Quercetin ({QUERCETIN_CHEMBL_ID}) targets from ChEMBL REST API ...",
          file=sys.stderr)
    fresh = retrieve()
    print(f"  retrieved {len(fresh)} UniProt accessions", file=sys.stderr)

    if args.out:
        with args.out.open("w", newline="") as fh:
            writer = csv.writer(fh, lineterminator="\n")
            writer.writerow(["compound", "protein_id", "source"])
            for acc in fresh:
                writer.writerow(["Quercetin", acc, "ChEMBL_API"])
        print(f"  wrote {args.out}", file=sys.stderr)

    if args.verify:
        committed = set(load_snapshot_quercetin())
        fresh_set = set(fresh)
        only_fresh = sorted(fresh_set - committed)
        only_committed = sorted(committed - fresh_set)
        print(f"committed snapshot (ChEMBL v{SNAPSHOT_VERSION}): {len(committed)} accessions")
        print(f"fresh retrieval (current release):    {len(fresh_set)} accessions")
        print(f"intersection: {len(fresh_set & committed)}")
        if only_fresh:
            print(f"only in fresh ({len(only_fresh)}): {', '.join(only_fresh)}")
        if only_committed:
            print(f"only in committed ({len(only_committed)}): {', '.join(only_committed)}")
        if not only_fresh and not only_committed:
            print("EXACT MATCH with committed snapshot.")
        else:
            print("NOTE: differences are expected when the live ChEMBL release != "
                  f"v{SNAPSHOT_VERSION}; the committed snapshot remains authoritative.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

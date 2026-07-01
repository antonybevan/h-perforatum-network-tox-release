#!/usr/bin/env python3
"""Create the manuscript-facing consolidated results table."""

import csv
from pathlib import Path

import pandas as pd


RESULTS_DIR = Path("results")
TABLES_DIR = RESULTS_DIR / "tables"


def fmt(value, digits):
    """Format a numeric value with fixed precision, then trim trailing zeros."""
    text = f"{float(value):.{digits}f}"
    return text.rstrip("0").rstrip(".")


def fixed(value, digits):
    """Format a numeric value with fixed precision."""
    return f"{float(value):.{digits}f}"


def main():
    rwr = pd.read_csv(TABLES_DIR / "standard_rwr_lcc_permutation_results.csv")
    ewi = pd.read_csv(TABLES_DIR / "expression_weighted_rwr_permutation_results.csv")
    sp = pd.read_csv(TABLES_DIR / "shortest_path_permutation_results.csv")
    bootstrap = pd.read_csv(TABLES_DIR / "bootstrap_summary.csv")
    chemsim = pd.read_csv(TABLES_DIR / "chemical_similarity_summary.csv")

    rows = []

    rwr_900 = rwr[rwr["network_threshold"] == 900]
    for compound in ["Hyperforin", "Quercetin"]:
        row = rwr_900[rwr_900["compound"] == compound].iloc[0]
        rows.append({
            "compound": compound,
            "metric": "RWI",
            "n_targets": f"{float(row['n_targets']):.1f}",
            "observed": fixed(row["observed_influence"], 4),
            "z_score": fmt(row["z_score"], 2),
            "p_value": f"{float(row['p_value']):.4g}",
            "efficiency": fixed(row["observed_influence"], 4),
            "significant": str(bool(row["significant"])),
        })

    ewi_900 = ewi[ewi["network_threshold"] == 900]
    for compound in ["Hyperforin", "Quercetin"]:
        row = ewi_900[ewi_900["compound"] == compound].iloc[0]
        rows.append({
            "compound": compound,
            "metric": "EWI",
            "n_targets": f"{float(row['n_targets']):.1f}",
            "observed": fixed(row["observed_influence"], 4),
            "z_score": fmt(row["z_score"], 2),
            "p_value": f"{float(row['p_value']):.4g}",
            "efficiency": fixed(row["observed_influence"], 4),
            "significant": str(bool(row["significant"])),
        })

    sp_900 = sp[sp["network_threshold"] == 900]
    for compound in ["Hyperforin", "Quercetin"]:
        row = sp_900[sp_900["compound"] == compound].iloc[0]
        rows.append({
            "compound": compound,
            "metric": "Shortest_Path",
            "n_targets": f"{float(row['n_targets']):.1f}",
            "observed": fmt(row["observed_dc"], 2),
            "z_score": fmt(row["z_score"], 2),
            "p_value": f"{float(row['p_value']):.4g}",
            "efficiency": "",
            "significant": str(bool(row["significant"])),
        })

    boot = bootstrap.iloc[0]
    rows.append({
        "compound": "Hyperforin",
        "metric": "Bootstrap",
        "n_targets": f"{float(boot['sample_size']):.1f}",
        "observed": fixed(boot["observed_influence"], 4),
        "z_score": "",
        "p_value": "",
        "efficiency": "",
        "significant": str(bool(boot["exceeds_ci"])),
    })

    for compound in ["Hyperforin", "Quercetin"]:
        row = chemsim[chemsim["compound"] == compound].iloc[0]
        rows.append({
            "compound": compound,
            "metric": "Chemical_Sim",
            "n_targets": "",
            "observed": fmt(max(row["max_sim_DILI_positive"], row["max_sim_DILI_negative"]), 3),
            "z_score": "",
            "p_value": "",
            "efficiency": "",
            "significant": str(row["structural_analog_to_dilirank_positive"] == "No"),
        })

    output_file = TABLES_DIR / "consolidated_results.csv"
    with output_file.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "compound", "metric", "n_targets", "observed", "z_score",
                "p_value", "efficiency", "significant",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()

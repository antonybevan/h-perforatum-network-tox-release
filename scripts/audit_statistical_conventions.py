#!/usr/bin/env python3
"""Audit p-value conventions and null-variance shrinkage across metrics.

This diagnostic script does not overwrite production result tables. By default
it audits the committed permutation result tables and reports three p-value
conventions side by side:

1. zero-allowing empirical r / n
2. conservative empirical (r + 1) / (n + 1)
3. one-tailed Gaussian tail probability from the permutation Z-score
"""

import sys
import argparse
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
from scipy import stats
from tqdm import tqdm


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from network_tox.analysis.expression_weighted_rwr import (  # noqa: E402
    load_liver_expression,
    run_expression_weighted_rwr,
    run_standard_rwr,
)
from network_tox.core.permutation import (  # noqa: E402
    calculate_z_score,
    get_degree_matched_random,
)


DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
TABLES_DIR = RESULTS_DIR / "tables"
GTEX_FILE = DATA_DIR / "raw" / "GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct"

NETWORK_THRESHOLDS = [700, 900]
COMPOUNDS = ["Hyperforin", "Quercetin"]
N_PERMUTATIONS = 1000
RANDOM_SEED = 42
RESTART_PROB = 0.15


def load_network(threshold):
    network_file = DATA_DIR / "processed" / f"network_{threshold}_liver_lcc.parquet"
    df = pd.read_parquet(network_file)
    if {"gene1", "gene2"}.issubset(df.columns):
        return nx.from_pandas_edgelist(df, "gene1", "gene2")
    if {"protein1", "protein2"}.issubset(df.columns):
        return nx.from_pandas_edgelist(df, "protein1", "protein2")
    if {"source", "target"}.issubset(df.columns):
        return nx.from_pandas_edgelist(df, "source", "target")
    cols = df.columns.tolist()
    return nx.from_pandas_edgelist(df, cols[0], cols[1])


def load_targets(compound, preserve_order=False):
    targets_df = pd.read_csv(DATA_DIR / "processed" / "targets_lcc.csv")
    values = targets_df.loc[targets_df["compound"] == compound, "gene_symbol"].tolist()
    if preserve_order:
        return values
    return sorted(set(values))


def load_dili_genes(threshold):
    dili_df = pd.read_csv(DATA_DIR / "processed" / f"dili_{threshold}_lcc.csv")
    if "gene_name" in dili_df.columns:
        return list(dili_df["gene_name"])
    for col in ["protein_id", "gene_symbol"]:
        if col in dili_df.columns:
            return list(dili_df[col])
    return list(dili_df.iloc[:, 0])


def shortest_path_dc(G, targets, disease_genes):
    targets_in = [target for target in targets if target in G]
    disease_in = [gene for gene in disease_genes if gene in G]
    if not targets_in or not disease_in:
        return np.nan

    distances = []
    for target in targets_in:
        min_dist = float("inf")
        for disease in disease_in:
            try:
                min_dist = min(min_dist, nx.shortest_path_length(G, target, disease))
            except nx.NetworkXNoPath:
                continue
        if min_dist != float("inf"):
            distances.append(min_dist)
    return np.mean(distances) if distances else np.nan


def get_shortest_path_degree_matched_random(G, targets):
    """Match the shortest-path production script's sampling behavior."""
    target_degrees = {target: G.degree(target) for target in targets if target in G}
    all_nodes = list(G.nodes())
    all_degrees = {node: G.degree(node) for node in all_nodes}

    random_targets = []
    for _target, degree in target_degrees.items():
        min_deg = int(degree * 0.75)
        max_deg = int(degree * 1.25) + 1
        candidates = [
            node
            for node, node_degree in all_degrees.items()
            if min_deg <= node_degree <= max_deg and node not in random_targets
        ]
        if candidates:
            random_targets.append(np.random.choice(candidates))
        else:
            random_targets.append(np.random.choice(all_nodes))
    return random_targets


def compute_dili_influence(scores, dili_genes):
    return sum(scores.get(gene, 0.0) for gene in dili_genes)


def pvalue_conventions(observed, null_distribution, direction, z_score):
    null_dist = np.asarray(null_distribution, dtype=float)
    n = len(null_dist)
    if n == 0:
        return {
            "extreme_count": np.nan,
            "p_empirical_r_over_n": np.nan,
            "p_empirical_plus_one": np.nan,
            "p_gaussian_tail": np.nan,
        }

    if direction == "greater":
        extreme_count = int(np.sum(null_dist >= observed))
        p_gaussian = stats.norm.sf(z_score)
    elif direction == "less":
        extreme_count = int(np.sum(null_dist <= observed))
        p_gaussian = stats.norm.cdf(z_score)
    else:
        raise ValueError(f"Unknown direction: {direction}")

    return {
        "extreme_count": extreme_count,
        "p_empirical_r_over_n": extreme_count / n,
        "p_empirical_plus_one": (extreme_count + 1) / (n + 1),
        "p_gaussian_tail": p_gaussian,
    }


def committed_p_values():
    table_by_metric = {
        "Shortest_Path": TABLES_DIR / "shortest_path_permutation_results.csv",
        "RWR": TABLES_DIR / "standard_rwr_lcc_permutation_results.csv",
        "EWI": TABLES_DIR / "expression_weighted_rwr_permutation_results.csv",
    }
    values = {}
    for metric, path in table_by_metric.items():
        df = pd.read_csv(path)
        for row in df.itertuples(index=False):
            values[(metric, int(row.network_threshold), row.compound)] = float(row.p_value)
    return values


def rows_from_committed_tables():
    """Fast audit path using the current production result tables.

    The production p-values use the conservative (r+1)/(n+1) convention, so the
    corresponding extreme count and zero-allowing r/n value can be recovered
    deterministically for n=1000.
    """
    specs = [
        (
            "Shortest_Path",
            TABLES_DIR / "shortest_path_permutation_results.csv",
            "observed_dc",
            "less",
        ),
        (
            "RWR",
            TABLES_DIR / "standard_rwr_lcc_permutation_results.csv",
            "observed_influence",
            "greater",
        ),
        (
            "EWI",
            TABLES_DIR / "expression_weighted_rwr_permutation_results.csv",
            "observed_influence",
            "greater",
        ),
    ]
    rows = []
    for metric, path, observed_col, direction in specs:
        df = pd.read_csv(path)
        for row in df.itertuples(index=False):
            z_score = float(row.z_score)
            p_plus_one = float(row.p_value)
            extreme_count = int(round(p_plus_one * (N_PERMUTATIONS + 1) - 1))
            p_gaussian = stats.norm.cdf(z_score) if direction == "less" else stats.norm.sf(z_score)
            rows.append(
                {
                    "metric": metric,
                    "network_threshold": int(row.network_threshold),
                    "compound": row.compound,
                    "n_targets": int(row.n_targets),
                    "direction": direction,
                    "observed_metric": float(getattr(row, observed_col)),
                    "null_mean": float(row.null_mean),
                    "null_std": float(row.null_std),
                    "z_score": z_score,
                    "committed_p_value": p_plus_one,
                    "extreme_count": extreme_count,
                    "p_empirical_r_over_n": extreme_count / N_PERMUTATIONS,
                    "p_empirical_plus_one": p_plus_one,
                    "p_gaussian_tail": p_gaussian,
                }
            )
    return rows


def run_shortest_path_audit(committed):
    rows = []
    np.random.seed(RANDOM_SEED)
    for threshold in NETWORK_THRESHOLDS:
        G = load_network(threshold)
        dili_genes = load_dili_genes(threshold)
        for compound in COMPOUNDS:
            targets = load_targets(compound, preserve_order=True)
            targets_in = [target for target in targets if target in G]
            observed = shortest_path_dc(G, targets_in, dili_genes)
            null_distribution = []
            desc = f"SP {threshold} {compound}"
            for _ in tqdm(range(N_PERMUTATIONS), desc=desc):
                random_targets = get_shortest_path_degree_matched_random(G, targets_in)
                null_value = shortest_path_dc(G, random_targets, dili_genes)
                if not np.isnan(null_value):
                    null_distribution.append(null_value)

            z_score = calculate_z_score(observed, null_distribution)
            row = {
                "metric": "Shortest_Path",
                "network_threshold": threshold,
                "compound": compound,
                "n_targets": len(targets_in),
                "direction": "less",
                "observed_metric": observed,
                "null_mean": float(np.mean(null_distribution)),
                "null_std": float(np.std(null_distribution)),
                "z_score": z_score,
                "committed_p_value": committed[("Shortest_Path", threshold, compound)],
            }
            row.update(pvalue_conventions(observed, null_distribution, "less", z_score))
            rows.append(row)
    return rows


def run_rwr_audit(committed, expression=None):
    rows = []
    metric = "EWI" if expression is not None else "RWR"
    runner = run_expression_weighted_rwr if expression is not None else run_standard_rwr

    for threshold in NETWORK_THRESHOLDS:
        G = load_network(threshold)
        dili_genes = [gene for gene in load_dili_genes(threshold) if gene in G]
        for compound in COMPOUNDS:
            targets = [target for target in load_targets(compound) if target in G]
            if expression is None:
                observed_scores = runner(G, targets, restart_prob=RESTART_PROB)
            else:
                observed_scores = runner(G, targets, expression, restart_prob=RESTART_PROB)
            observed = compute_dili_influence(observed_scores, dili_genes)

            null_distribution = []
            desc = f"{metric} {threshold} {compound}"
            for i in tqdm(range(N_PERMUTATIONS), desc=desc):
                random_targets = get_degree_matched_random(
                    G,
                    targets,
                    len(targets),
                    seed=RANDOM_SEED + i,
                )
                if not random_targets:
                    continue
                if expression is None:
                    random_scores = runner(G, random_targets, restart_prob=RESTART_PROB)
                else:
                    random_scores = runner(G, random_targets, expression, restart_prob=RESTART_PROB)
                null_distribution.append(compute_dili_influence(random_scores, dili_genes))

            z_score = calculate_z_score(observed, null_distribution)
            row = {
                "metric": metric,
                "network_threshold": threshold,
                "compound": compound,
                "n_targets": len(targets),
                "direction": "greater",
                "observed_metric": observed,
                "null_mean": float(np.mean(null_distribution)),
                "null_std": float(np.std(null_distribution)),
                "z_score": z_score,
                "committed_p_value": committed[(metric, threshold, compound)],
            }
            row.update(pvalue_conventions(observed, null_distribution, "greater", z_score))
            rows.append(row)
    return rows


def variance_shrinkage_rows(audit_df):
    rows = []
    expected_ratio = np.sqrt(62 / 10)
    for metric in ["Shortest_Path", "RWR", "EWI"]:
        for threshold in NETWORK_THRESHOLDS:
            subset = audit_df[
                (audit_df["metric"] == metric)
                & (audit_df["network_threshold"] == threshold)
            ]
            hyp = subset[subset["compound"] == "Hyperforin"].iloc[0]
            quer = subset[subset["compound"] == "Quercetin"].iloc[0]
            observed_ratio = hyp["null_std"] / quer["null_std"]
            rows.append(
                {
                    "metric": metric,
                    "network_threshold": threshold,
                    "hyperforin_n_targets": int(hyp["n_targets"]),
                    "quercetin_n_targets": int(quer["n_targets"]),
                    "hyperforin_null_std": hyp["null_std"],
                    "quercetin_null_std": quer["null_std"],
                    "std_ratio_hyperforin_over_quercetin": observed_ratio,
                    "expected_sqrt_62_over_10": expected_ratio,
                    "observed_over_expected_ratio": observed_ratio / expected_ratio,
                }
            )
    return rows


def parse_args():
    parser = argparse.ArgumentParser(
        description="Audit p-value conventions and null-variance shrinkage."
    )
    parser.add_argument(
        "--recompute",
        action="store_true",
        help="Rerun the full degree-matched permutation audit instead of using committed result tables.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print("Auditing p-value conventions and null-variance shrinkage")
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    if args.recompute:
        committed = committed_p_values()
        rows = []
        rows.extend(run_shortest_path_audit(committed))
        rows.extend(run_rwr_audit(committed))

        print("Loading GTEx liver expression for EWI audit...")
        expression = load_liver_expression(GTEX_FILE, tissue_column="Liver")
        rows.extend(run_rwr_audit(committed, expression=expression))
    else:
        print("Using committed permutation tables; pass --recompute for a full null rerun.")
        rows = rows_from_committed_tables()

    audit_df = pd.DataFrame(rows)
    pvalue_file = TABLES_DIR / "pvalue_convention_audit.csv"
    audit_df.to_csv(pvalue_file, index=False)

    shrinkage_df = pd.DataFrame(variance_shrinkage_rows(audit_df))
    shrinkage_file = TABLES_DIR / "null_variance_shrinkage_audit.csv"
    shrinkage_df.to_csv(shrinkage_file, index=False)

    print(f"Saved: {pvalue_file}")
    print(f"Saved: {shrinkage_file}")
    print()
    print(audit_df[[
        "metric",
        "network_threshold",
        "compound",
        "z_score",
        "p_empirical_plus_one",
        "p_gaussian_tail",
        "committed_p_value",
    ]].to_string(index=False))
    print()
    print(shrinkage_df.to_string(index=False))


if __name__ == "__main__":
    main()

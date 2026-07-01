#!/usr/bin/env python3
"""
STRING text-mining sensitivity analysis.

Tests whether the Hyperforin > Quercetin proximity/influence ordering is robust to
literature/text-mining circularity in the STRING combined score. The DILI module
is DisGeNET-derived (literature-based), and STRING's combined score includes a
text-mining channel, so some target->DILI edges could be co-mention artifacts.

Method follows Huang et al., "A systematic evaluation of molecular networks for
discovery of disease genes", Cell Systems 2018 (doi:10.1016/j.cels.2018.03.001):
rebuild the interactome after removing edges supported SOLELY by the text-mining
channel, then re-run the analyses. Everything else is identical to the committed
pipeline (extract_string_network.py + create_lcc_filtered_data.py).

Inputs (raw, gitignored; see DATA_MANIFEST):
  data/external/9606.protein.links.detailed.v12.0.txt.gz  STRING v12.0 per-channel
  data/external/string_gene_map.txt.gz                    ENSP -> gene symbol

Detailed columns (space-separated):
  protein1 protein2 neighborhood fusion cooccurence coexpression
  experimental database textmining combined_score
  -> combined is field [9]; textmining is [8]; non-textmining channels are [2..7].

Integrity gate: the 'full' rebuild (combined>=threshold, no text-mining filter)
must recover every committed network_{700,900}.parquet edge, allowing only the
small (<1%) mapping superset caused by the broader STRING gene map. If any
committed edge is missing, the script aborts before producing sensitivity numbers.

Output (committed): results/tables/string_textmining_sensitivity.csv
"""
from __future__ import annotations

import argparse
import gzip
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from network_tox.analysis.rwr import build_rwr_operator, run_rwr_from_operator
from network_tox.analysis.expression_weighted_rwr import (
    load_liver_expression,
    build_ewi_operator,
    run_ewi_from_operator,
)
from network_tox.core.permutation import get_degree_matched_random, calculate_z_score

DATA = PROJECT_ROOT / "data"
TABLES = PROJECT_ROOT / "results" / "tables"
DETAILED = DATA / "external" / "9606.protein.links.detailed.v12.0.txt.gz"
GENEMAP = DATA / "external" / "string_gene_map.txt.gz"
GTEX = DATA / "raw" / "GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct"

THRESHOLDS = [700, 900]
N_PERM = 1000
SEED = 42
MIN_TPM = 1.0
RESTART_PROB = 0.15

DETAILED_COLS = [
    "protein1", "protein2", "neighborhood", "fusion", "cooccurence",
    "coexpression", "experimental", "database", "textmining", "combined_score",
]
NONTM_CHANNELS = ["neighborhood", "fusion", "cooccurence", "coexpression", "experimental", "database"]
COMPOUNDS = ["Hyperforin", "Quercetin"]


# --------------------------------------------------------------------------- IO
def load_gene_map(path: Path) -> dict:
    m = {}
    with gzip.open(path, "rt") as fh:
        fh.readline()  # header (#string_protein_id  preferred_name  ...)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[0] and parts[1]:
                m[parts[0]] = parts[1]
    return m


def load_detailed(path: Path, min_threshold: int) -> pd.DataFrame:
    """Read the per-channel STRING file, keeping edges with combined >= min_threshold."""
    dtypes = {c: "int16" for c in DETAILED_COLS[2:]}
    dtypes["protein1"] = "object"
    dtypes["protein2"] = "object"
    parts = []
    for chunk in pd.read_csv(path, sep=" ", skiprows=1, names=DETAILED_COLS,
                             dtype=dtypes, chunksize=2_000_000):
        parts.append(chunk[chunk["combined_score"] >= min_threshold])
    df = pd.concat(parts, ignore_index=True)
    return df


def _load_compound_targets() -> dict:
    # Use the committed liver-LCC target set (10 Hyperforin / 62 Quercetin) -- the
    # same definition the published analyses use -- so the full rebuild matches them.
    df = pd.read_csv(DATA / "processed" / "targets_lcc.csv")
    col = next((c for c in ("gene_symbol", "gene_name", "gene") if c in df.columns), df.columns[0])
    return {c: sorted(set(df[df["compound"] == c][col])) for c in COMPOUNDS}


def _load_dili_for_threshold(threshold: int) -> list:
    # Per-threshold DILI LCC set, matching the committed analyses (dili_{thr}_lcc.csv).
    df = pd.read_csv(DATA / "processed" / f"dili_{threshold}_lcc.csv")
    col = next((c for c in ("gene_name", "gene_symbol", "gene", "protein_id") if c in df.columns), df.columns[0])
    return sorted(set(df[col]))


# ------------------------------------------------------------------- network build
def build_gene_edges(df: pd.DataFrame, threshold: int, gene_map: dict, drop_textmining: bool) -> pd.DataFrame:
    sub = df[df["combined_score"] >= threshold]
    if drop_textmining:
        # Huang 2018: drop edges supported SOLELY by text mining, i.e. every
        # non-textmining channel is zero. Keep the edge if any other channel fires.
        keep = sub[NONTM_CHANNELS].to_numpy().max(axis=1) > 0
        sub = sub[keep]
    g1 = sub["protein1"].map(gene_map).to_numpy()
    g2 = sub["protein2"].map(gene_map).to_numpy()
    score = sub["combined_score"].to_numpy()
    mapped = pd.notna(g1) & pd.notna(g2)
    g1, g2, score = g1[mapped], g2[mapped], score[mapped]
    swap = g1 > g2
    a = np.where(swap, g2, g1)
    b = np.where(swap, g1, g2)
    nonself = a != b
    edf = pd.DataFrame({"gene1": a[nonself], "gene2": b[nonself], "score": score[nonself]})
    edf = edf.sort_values("score", ascending=False).drop_duplicates(["gene1", "gene2"], keep="first")
    return edf.reset_index(drop=True)


def edge_set(df: pd.DataFrame) -> set:
    c1, c2 = df.columns[0], df.columns[1]
    return set(zip(df[c1], df[c2]))  # both stored in canonical (min,max) order


def liver_genes_set() -> set:
    g = pd.read_csv(GTEX, sep="\t", skiprows=2)
    out = {}
    for _, row in g.iterrows():
        gene = row.get("Description", row.get("Name", ""))
        tpm = row.get("Liver", 0)
        if gene and pd.notna(tpm) and tpm >= MIN_TPM:
            out[gene] = float(tpm)
    return out


def liver_lcc_graph(edf: pd.DataFrame, liver_genes: set) -> nx.Graph:
    G = nx.from_pandas_edgelist(edf, "gene1", "gene2")
    liver_nodes = [n for n in G.nodes() if n in liver_genes]
    Gl = G.subgraph(liver_nodes).copy()
    if len(Gl) == 0:
        return nx.Graph()
    lcc = max(nx.connected_components(Gl), key=len)
    return Gl.subgraph(lcc).copy()


# ---------------------------------------------------------------- integrity gate
def validate_full(df: pd.DataFrame, gene_map: dict) -> bool:
    print("\n=== INTEGRITY GATE: full rebuild vs committed networks ===")
    ok = True
    expected = {700: "network_700.parquet", 900: "network_900.parquet"}
    for thr, fn in expected.items():
        rebuilt = build_gene_edges(df, thr, gene_map, drop_textmining=False)
        committed = pd.read_parquet(DATA / "processed" / fn)
        # normalise committed to canonical (min,max) gene pairs
        c1, c2 = committed.columns[0], committed.columns[1]
        c1arr = committed[c1].to_numpy().astype(str)
        c2arr = committed[c2].to_numpy().astype(str)
        cswap = c1arr > c2arr
        ca = np.where(cswap, c2arr, c1arr)
        cb = np.where(cswap, c1arr, c2arr)
        committed_set = set(zip(ca.tolist(), cb.tolist()))
        rebuilt_set = edge_set(rebuilt)
        missing = committed_set - rebuilt_set   # committed edges we failed to reproduce
        extra = rebuilt_set - committed_set     # extra edges from a more permissive mapping
        frac_extra = len(extra) / len(committed_set)
        # Faithful if EVERY committed edge is reproduced; a <1% superset is the
        # known effect of string_gene_map.txt mapping a few more proteins than the
        # original string_info file. A missing committed edge is a real failure.
        thr_ok = (len(missing) == 0) and (frac_extra < 0.01)
        ok = ok and thr_ok
        if rebuilt_set == committed_set:
            status = "EXACT MATCH"
        elif len(missing) == 0:
            status = f"SUPERSET (+{len(extra):,} = {frac_extra:.2%}; 0 committed edges missing)"
        else:
            status = f"MISMATCH ({len(missing):,} committed edges missing)"
        print(f"  >={thr}: rebuilt {len(rebuilt_set):,} | committed {len(committed_set):,} | "
              f"{status} -> {'OK' if thr_ok else 'FAIL'}")
    print("  RESULT:", "PASS" if ok else "FAIL",
          "(internal full-vs-no-tm comparison isolates the text-mining effect; "
          "committed values are an external cross-check)")
    return ok


# ------------------------------------------------------------------- metrics
def calc_dc(G: nx.Graph, targets, dili) -> float:
    t_in = [t for t in targets if t in G]
    d_in = [d for d in dili if d in G]
    if not t_in or not d_in:
        return float("nan")
    dist = nx.multi_source_dijkstra_path_length(G, d_in, weight=lambda u, v, d: 1)
    ds = [dist[t] for t in t_in if t in dist]
    return float(np.mean(ds)) if ds else float("nan")


def sp_degree_matched(G, targets):
    """Shortest-path script's sampler (permits original seed in its own pool)."""
    deg = dict(G.degree())
    target_deg = {t: deg[t] for t in targets if t in deg}
    all_nodes = list(G.nodes())
    rt = []
    for _, degree in target_deg.items():
        lo, hi = int(degree * 0.75), int(degree * 1.25) + 1
        cand = [n for n in all_nodes if lo <= deg[n] <= hi and n not in rt]
        rt.append(np.random.choice(cand) if cand else np.random.choice(all_nodes))
    return rt


def influence_at(scores: dict, dili) -> float:
    return float(sum(scores.get(g, 0.0) for g in dili))


def run_metric(metric, G, targets, dili, expression, do_perm):
    """Return (observed, z, p, n_targets, n_dili). metric in {sp, rwr, ewi}."""
    t_in = [t for t in targets if t in G]
    d_in = [d for d in dili if d in G]
    n_t, n_d = len(t_in), len(d_in)
    if n_t == 0 or n_d == 0:
        return float("nan"), float("nan"), float("nan"), n_t, n_d

    if metric == "sp":
        observed = calc_dc(G, t_in, d_in)
    elif metric == "rwr":
        W, nodes, idx = build_rwr_operator(G)
        observed = influence_at(run_rwr_from_operator(W, nodes, idx, t_in, restart_prob=RESTART_PROB), d_in)
    else:  # ewi
        Wp, nodes, idx = build_ewi_operator(G, expression)
        observed = influence_at(run_ewi_from_operator(Wp, nodes, idx, t_in, restart_prob=RESTART_PROB), d_in)

    if not do_perm:
        return observed, float("nan"), float("nan"), n_t, n_d

    null = []
    if metric == "sp":
        np.random.seed(SEED)
        for _ in range(N_PERM):
            rt = sp_degree_matched(G, t_in)
            val = calc_dc(G, rt, d_in)
            if not np.isnan(val):
                null.append(val)
        tail = "less"
    else:
        if metric == "rwr":
            W, nodes, idx = build_rwr_operator(G)
            runner = lambda seeds: run_rwr_from_operator(W, nodes, idx, seeds, restart_prob=RESTART_PROB)
        else:
            Wp, nodes, idx = build_ewi_operator(G, expression)
            runner = lambda seeds: run_ewi_from_operator(Wp, nodes, idx, seeds, restart_prob=RESTART_PROB)
        np.random.seed(SEED)
        for i in range(N_PERM):
            rt = get_degree_matched_random(G, t_in, n_t, seed=SEED + i)
            if not rt:
                continue
            null.append(influence_at(runner(rt), d_in))
        tail = "greater"

    null = np.array(null)
    z = calculate_z_score(observed, null)
    if tail == "less":
        r = int(np.sum(null <= observed))
    else:
        r = int(np.sum(null >= observed))
    p = (r + 1) / (len(null) + 1) if len(null) else float("nan")
    return observed, z, p, n_t, n_d


# ---------------------------------------------------------------- committed refs
def committed_observed():
    """Map (metric, threshold, compound) -> original observed value."""
    out = {}
    sp = pd.read_csv(TABLES / "shortest_path_permutation_results.csv")
    for _, r in sp.iterrows():
        out[("sp", int(r["network_threshold"]), r["compound"])] = float(r["observed_dc"])
    rwr = pd.read_csv(TABLES / "standard_rwr_lcc_permutation_results.csv")
    for _, r in rwr.iterrows():
        out[("rwr", int(r["network_threshold"]), r["compound"])] = float(r["observed_influence"])
    ewi = pd.read_csv(TABLES / "expression_weighted_rwr_permutation_results.csv")
    for _, r in ewi.iterrows():
        out[("ewi", int(r["network_threshold"]), r["compound"])] = float(r["observed_influence"])
    return out


# ------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="STRING text-mining sensitivity (Huang 2018 method).")
    ap.add_argument("--validate-only", action="store_true", help="only run the integrity gate")
    ap.add_argument("--observed-only", action="store_true", help="skip permutation nulls (fast headline)")
    args = ap.parse_args()

    for f in (DETAILED, GENEMAP, GTEX):
        if not f.exists():
            print(f"ERROR: missing input {f}")
            return 1

    print("Loading ENSP->gene map ...")
    gene_map = load_gene_map(GENEMAP)
    print(f"  {len(gene_map):,} mappings")
    print(f"Loading STRING detailed (combined >= {min(THRESHOLDS)}) ...")
    df = load_detailed(DETAILED, min(THRESHOLDS))
    print(f"  {len(df):,} protein-level edges at combined >= {min(THRESHOLDS)}")

    if not validate_full(df, gene_map):
        print("\nABORTING: full rebuild does not reproduce committed networks; "
              "extraction/mapping is not faithful, sensitivity numbers would be untrustworthy.")
        return 1
    if args.validate_only:
        print("\n--validate-only: integrity gate passed, stopping.")
        return 0

    do_perm = not args.observed_only
    liver = liver_genes_set()
    targets = _load_compound_targets()
    expression = load_liver_expression(GTEX, tissue_column="Liver")
    ref = committed_observed()

    rows = []
    for thr in THRESHOLDS:
        dili = _load_dili_for_threshold(thr)
        G_full = liver_lcc_graph(build_gene_edges(df, thr, gene_map, drop_textmining=False), liver)
        G_notm = liver_lcc_graph(build_gene_edges(df, thr, gene_map, drop_textmining=True), liver)
        print(f"\n--- liver-LCC (>={thr}): full {G_full.number_of_nodes()}n/{G_full.number_of_edges()}e | "
              f"no-tm {G_notm.number_of_nodes()}n/{G_notm.number_of_edges()}e ---")
        for metric in ("sp", "rwr", "ewi"):
            for comp in COMPOUNDS:
                obs_full, _, _, _, _ = run_metric(metric, G_full, targets[comp], dili, expression, do_perm=False)
                obs, z, p, n_t, n_d = run_metric(metric, G_notm, targets[comp], dili, expression, do_perm)
                orig = ref.get((metric, thr, comp), float("nan"))
                rows.append({
                    "metric": {"sp": "shortest_path_dc", "rwr": "rwr_influence", "ewi": "ewi_influence"}[metric],
                    "network_threshold": thr,
                    "compound": comp,
                    "n_targets_notm": n_t,
                    "n_dili_notm": n_d,
                    "observed_committed": orig,
                    "observed_full_rebuild": obs_full,
                    "observed_notm": obs,
                    "z_notm": z,
                    "p_notm": p,
                })
                print(f"  {metric:4s} {comp:10s}: committed={orig:.4f}  full={obs_full:.4f}  "
                      f"notm={obs:.4f}  Z={z:.3f}  p={p:.4g}  (|T|={n_t}, |D|={n_d})")

    out = pd.DataFrame(rows)

    # ordering preserved? sp: Hyperforin lower d_c; rwr/ewi: Hyperforin higher influence
    print("\n=== ORDERING ROBUSTNESS (Hyperforin vs Quercetin; full-rebuild vs no-text-mining) ===")
    for metric in ["shortest_path_dc", "rwr_influence", "ewi_influence"]:
        for thr in THRESHOLDS:
            sub = out[(out.metric == metric) & (out.network_threshold == thr)].set_index("compound")
            h, q = sub.loc["Hyperforin"], sub.loc["Quercetin"]
            better = "lower" if metric == "shortest_path_dc" else "higher"
            if metric == "shortest_path_dc":
                full_pres = h["observed_full_rebuild"] < q["observed_full_rebuild"]
                notm_pres = h["observed_notm"] < q["observed_notm"]
            else:
                full_pres = h["observed_full_rebuild"] > q["observed_full_rebuild"]
                notm_pres = h["observed_notm"] > q["observed_notm"]
            print(f"  {metric:18s} >={thr}: Hyperforin {better} full={full_pres} | "
                  f"no-tm={notm_pres}  {'OK (preserved)' if notm_pres == full_pres else 'CHANGED'}")

    if do_perm:
        TABLES.mkdir(parents=True, exist_ok=True)
        out_file = TABLES / "string_textmining_sensitivity.csv"
        out.to_csv(out_file, index=False, lineterminator="\n")
        print(f"\nSaved: {out_file}")
    else:
        # Guard: --observed-only has no permutation Z/p, so it must NOT overwrite the
        # committed table (which is produced only by a full run).
        print("\n--observed-only: results above NOT written (the committed table is "
              "produced only by a full run with permutations).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

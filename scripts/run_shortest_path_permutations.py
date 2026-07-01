#!/usr/bin/env python3
"""
Shortest Path Proximity Analysis with Degree-Matched Permutation Testing.

Calculates the mean minimum distance (d_c) from drug targets to DILI genes
with statistical validation via permutation testing.
"""

import csv
import pandas as pd
import numpy as np
import networkx as nx
from pathlib import Path
from tqdm import tqdm
from statsmodels.stats.multitest import multipletests
import sys
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / 'src'))

import warnings
warnings.filterwarnings('ignore')

# Configuration
N_PERMUTATIONS = 1000
RANDOM_SEED = 42
NETWORK_THRESHOLDS = [700, 900]

np.random.seed(RANDOM_SEED)

DATA_DIR = Path('data')
RESULTS_DIR = Path('results') / 'tables'
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def write_committed_stable_csv(df, output_file):
    """Write result table while preserving committed float text when unchanged.

    Matches the convention used by the RWR/EWI permutation scripts: if a freshly
    computed value is within 1e-14 of the committed value, the committed float
    text is preserved so trivial last-ULP / float-formatting differences across
    environments do not churn the published numbers.
    """
    committed_rows = {}
    if output_file.exists():
        with output_file.open(newline='') as handle:
            for row in csv.DictReader(handle):
                key = (row.get('network_threshold', ''), row.get('compound', ''))
                committed_rows[key] = row

    fieldnames = list(df.columns)
    with output_file.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        for row in df.to_dict(orient='records'):
            key = (str(int(row['network_threshold'])), row['compound'])
            committed = committed_rows.get(key, {})
            out_row = {}
            for field in fieldnames:
                value = row[field]
                committed_text = committed.get(field)
                if committed_text not in (None, '') and isinstance(value, (int, float, np.integer, np.floating, bool, np.bool_)):
                    try:
                        if np.isclose(float(committed_text), float(value), rtol=0, atol=1e-14):
                            out_row[field] = committed_text
                            continue
                    except ValueError:
                        pass
                out_row[field] = value
            writer.writerow(out_row)


def calculate_shortest_path(G, targets, disease_genes):
    """Calculate mean minimum shortest path distance (d_c).

    Uses a single unweighted multi-source BFS from the (fixed) disease set to
    obtain each node's distance to its NEAREST disease gene, then averages over
    the targets. This is mathematically identical to the per-target BFS it
    replaces (unweighted shortest-path lengths are exact integers) but avoids the
    O(|T| x |D|) recomputation; it reproduces the committed d_c and Z exactly.
    """
    targets_in = [t for t in targets if t in G]
    disease_in = [d for d in disease_genes if d in G]

    if not targets_in or not disease_in:
        return np.nan

    dist_to_disease = nx.multi_source_dijkstra_path_length(
        G, disease_in, weight=lambda u, v, d: 1
    )
    distances = [dist_to_disease[t] for t in targets_in if t in dist_to_disease]

    return np.mean(distances) if distances else np.nan


def get_degree_matched_random(G, targets, n_random=1):
    """Get random nodes matching the degree distribution of targets."""
    target_degrees = {t: G.degree(t) for t in targets if t in G}
    all_nodes = list(G.nodes())
    all_degrees = {n: G.degree(n) for n in all_nodes}
    
    random_sets = []
    for _ in range(n_random):
        random_targets = []
        for target, degree in target_degrees.items():
            # Find nodes with similar degree (±25%)
            min_deg = int(degree * 0.75)
            max_deg = int(degree * 1.25) + 1
            candidates = [n for n, d in all_degrees.items() 
                         if min_deg <= d <= max_deg and n not in random_targets]
            if candidates:
                random_targets.append(np.random.choice(candidates))
            else:
                random_targets.append(np.random.choice(all_nodes))
        random_sets.append(random_targets)
    
    return random_sets


def calculate_empirical_p_value(observed, null_distribution, tail):
    """
    Conservative empirical permutation p-value, (r + 1) / (n + 1).

    This is the Phipson & Smyth (2010) convention, which avoids the
    non-defensible zero p-value display. With a degree-matched
    null of n = 1000 and no null value at least as extreme as the observed,
    the floor is 1/1001 = 9.99e-4, i.e. p < 0.001.
    """
    null_dist = np.array(null_distribution)
    n = len(null_dist)
    if n == 0:
        return np.nan
    if tail == 'one_less':
        return (np.sum(null_dist <= observed) + 1) / (n + 1)
    if tail == 'one_greater':
        return (np.sum(null_dist >= observed) + 1) / (n + 1)
    raise ValueError(f"Unknown tail option: {tail}")


def run_permutation_test(G, targets, disease_genes, n_permutations, compound_name, threshold):
    """Run permutation test for shortest path analysis."""
    observed = calculate_shortest_path(G, targets, disease_genes)
    
    null_distribution = []
    desc = f"{compound_name} (≥{threshold})"
    
    for _ in tqdm(range(n_permutations), desc=desc):
        random_targets = get_degree_matched_random(G, targets, n_random=1)[0]
        null_value = calculate_shortest_path(G, random_targets, disease_genes)
        if not np.isnan(null_value):
            null_distribution.append(null_value)
    
    null_distribution = np.array(null_distribution)
    null_mean = np.mean(null_distribution)
    null_std = np.std(null_distribution)
    
    # Z-score (negative = closer than expected)
    z_score = (observed - null_mean) / null_std if null_std > 0 else 0
    
    # P-value (one-tailed, testing if closer than random)
    p_value = calculate_empirical_p_value(observed, null_distribution, tail='one_less')
    
    return {
        'observed': observed,
        'null_mean': null_mean,
        'null_std': null_std,
        'z_score': z_score,
        'p_value': p_value
    }


def main():
    print("=" * 80)
    print(" SHORTEST PATH PROXIMITY ANALYSIS WITH PERMUTATION TESTING")
    print("=" * 80)
    print()
    print(f"Configuration:")
    print(f"  Permutations: {N_PERMUTATIONS}")
    print(f"  Random seed:  {RANDOM_SEED}")
    print()
    
    # Load targets
    targets_df = pd.read_csv(DATA_DIR / 'processed' / 'targets_lcc.csv')
    hyp_targets = list(targets_df[targets_df['compound'] == 'Hyperforin']['gene_symbol'])
    quer_targets = list(targets_df[targets_df['compound'] == 'Quercetin']['gene_symbol'])
    
    print(f"Targets: {len(hyp_targets)} Hyperforin, {len(quer_targets)} Quercetin")
    print()
    
    results = []
    
    for threshold in NETWORK_THRESHOLDS:
        print("=" * 80)
        print(f" NETWORK THRESHOLD: ≥{threshold}")
        print("=" * 80)
        print()
        
        # Load network
        network_file = DATA_DIR / 'processed' / f'network_{threshold}_liver_lcc.parquet'
        network_df = pd.read_parquet(network_file)
        
        # Handle column naming
        if 'gene1' in network_df.columns:
            G = nx.from_pandas_edgelist(network_df, 'gene1', 'gene2')
        else:
            G = nx.from_pandas_edgelist(network_df, 'protein1', 'protein2')
        
        print(f"[1] Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        
        # Load DILI genes
        dili_file = DATA_DIR / 'processed' / f'dili_{threshold}_lcc.csv'
        dili_df = pd.read_csv(dili_file)
        dili_genes = list(dili_df['gene_name'])
        dili_in_network = [g for g in dili_genes if g in G]
        print(f"[2] DILI genes: {len(dili_in_network)}/{len(dili_genes)} in network")
        print()
        
        for compound, targets in [('Hyperforin', hyp_targets), ('Quercetin', quer_targets)]:
            targets_in = [t for t in targets if t in G]
            print(f"[3] {compound}: {len(targets_in)}/{len(targets)} targets in network")
            
            result = run_permutation_test(G, targets, dili_genes, N_PERMUTATIONS, compound, threshold)
            
            print()
            print(f"  Results:")
            print(f"    Observed d_c:  {result['observed']:.4f}")
            print(f"    Null mean:     {result['null_mean']:.4f}")
            print(f"    Null std:      {result['null_std']:.4f}")
            print(f"    Z-score:       {result['z_score']:.4f}")
            print(f"    P-value:       {result['p_value']:.4e}")
            print()
            
            # Conservative empirical p-value, (r+1)/(n+1); floor 1/1001 = 9.99e-4
            p_value_display = result['p_value']
            
            results.append({
                'network_threshold': threshold,
                'compound': compound,
                'n_targets': len(targets_in),
                'observed_dc': result['observed'],
                'null_mean': result['null_mean'],
                'null_std': result['null_std'],
                'z_score': result['z_score'],
                'p_value': p_value_display,
                'significant': p_value_display < 0.05
            })
    
    # Save results
    results_df = pd.DataFrame(results)
    
    # Add FDR correction
    p_values = results_df['p_value'].values
    _, p_fdr, _, _ = multipletests(p_values, method='fdr_bh')
    results_df['p_fdr'] = p_fdr
    
    # Reorder columns for publication
    results_df = results_df[['network_threshold', 'compound', 'n_targets', 'observed_dc', 
                              'null_mean', 'null_std', 'z_score', 'p_value', 'p_fdr', 'significant']]
    
    output_file = RESULTS_DIR / 'shortest_path_permutation_results.csv'
    write_committed_stable_csv(results_df, output_file)
    print(f"Results saved: {output_file}")
    print()
    
    # Summary
    print("=" * 80)
    print(" RESULTS SUMMARY")
    print("=" * 80)
    print()
    print(results_df.to_string(index=False))
    print()
    print("-" * 80)
    print(" INTERPRETATION")
    print("-" * 80)
    print()
    print("Negative Z-score = targets are CLOSER to DILI genes than expected")
    print()
    
    for threshold in NETWORK_THRESHOLDS:
        hyp_row = results_df[(results_df['network_threshold'] == threshold) & (results_df['compound'] == 'Hyperforin')].iloc[0]
        quer_row = results_df[(results_df['network_threshold'] == threshold) & (results_df['compound'] == 'Quercetin')].iloc[0]
        
        print(f"STRING ≥{threshold}:")
        print(f"  Hyperforin: d_c={hyp_row['observed_dc']:.3f}, Z={hyp_row['z_score']:.2f}")
        print(f"  Quercetin:  d_c={quer_row['observed_dc']:.3f}, Z={quer_row['z_score']:.2f}")
        print()
    
    print("=" * 80)
    print(" COMPLETED")
    print("=" * 80)


if __name__ == '__main__':
    main()

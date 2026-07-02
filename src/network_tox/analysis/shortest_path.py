"""Shortest path analysis."""

import numpy as np
import networkx as nx

def calculate_shortest_path(G, drug_targets, disease_genes):
    """
    Calculate shortest-path proximity (d_c).

    Formula: dc = 1/|T| * sum(min(dist(t, d)) for t in T) where d in D

    Implemented as a single unweighted multi-source BFS from the disease set,
    giving each node its distance to the *nearest* disease gene, then averaged
    over the targets. This is mathematically identical to the per-target,
    per-disease BFS it replaces (unweighted shortest-path lengths are exact
    integers) but avoids the O(|T| x |D|) recomputation. It is the single source
    of truth for d_c: ``core.proximity.calculate_shortest_path`` and
    ``scripts/run_shortest_path_permutations.py`` both delegate here.

    Args:
        G: NetworkX graph
        drug_targets: List of target genes
        disease_genes: List of disease genes

    Returns:
        Mean minimum distance
    """
    targets_in = [t for t in drug_targets if t in G]
    disease_in = [d for d in disease_genes if d in G]

    if not targets_in or not disease_in:
        return np.nan

    # Distance from every reachable node to its nearest disease gene. Unit edge
    # weights make this an unweighted BFS (exact integer lengths); this is the
    # exact call the permutation driver used to reproduce the committed d_c.
    dist_to_disease = nx.multi_source_dijkstra_path_length(
        G, disease_in, weight=lambda u, v, d: 1
    )

    # Targets with no path to any disease gene are absent from the mapping and
    # are dropped, matching the per-pair loop's "skip unreachable target" rule.
    distances = [dist_to_disease[t] for t in targets_in if t in dist_to_disease]

    return np.mean(distances) if distances else np.nan

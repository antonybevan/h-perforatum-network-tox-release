"""Equivalence guard for the unified shortest-path proximity (audit patch 5).

The multi-source-BFS ``calculate_shortest_path`` is the single source of truth,
shared by ``network_tox.analysis.shortest_path``, ``network_tox.core.proximity``
and ``scripts/run_shortest_path_permutations.py``. This test pins it to the
original O(|T|*|D|) per-pair implementation (kept here only as an oracle) so the
refactor cannot silently change any committed d_c value.
"""

import itertools

import numpy as np
import networkx as nx
import pytest

from network_tox.analysis import shortest_path
from network_tox.core import proximity


def _reference_dc(G, targets, disease):
    """Original per-pair implementation, retained as an independent oracle."""
    targets_in = [t for t in targets if t in G]
    disease_in = [d for d in disease if d in G]
    if not targets_in or not disease_in:
        return np.nan
    distances = []
    for t in targets_in:
        best = float("inf")
        for d in disease_in:
            try:
                best = min(best, nx.shortest_path_length(G, t, d))
            except nx.NetworkXNoPath:
                continue
        if best != float("inf"):
            distances.append(best)
    return np.mean(distances) if distances else np.nan


def _equal(a, b):
    a, b = float(a), float(b)
    if np.isnan(a) and np.isnan(b):
        return True
    return np.isclose(a, b, atol=1e-9)


@pytest.mark.parametrize("n,seed", list(itertools.product([12, 25, 40], [0, 1, 5, 42, 2024])))
def test_matches_per_pair_oracle(n, seed):
    # Lower edge probability so some graphs are disconnected -> exercises the
    # unreachable-target branch.
    G = nx.gnp_random_graph(n, 0.12, seed=seed)
    nodes = list(G.nodes())
    rng = np.random.default_rng(seed)
    targets = list(rng.choice(nodes, size=min(5, n), replace=False))
    disease = list(rng.choice(nodes, size=min(4, n), replace=False))

    expected = _reference_dc(G, targets, disease)
    assert _equal(shortest_path.calculate_shortest_path(G, targets, disease), expected)
    # proximity must delegate to the same implementation.
    assert _equal(proximity.calculate_shortest_path(G, targets, disease), expected)


def test_fixed_fixtures_match_oracle():
    G = nx.Graph()
    G.add_edges_from([("A", "B"), ("B", "C"), ("C", "D")])
    cases = [
        (["A"], ["D"]),
        (["A"], ["C", "D"]),
        (["A", "B"], ["D"]),
        (["A"], ["A"]),          # target is itself a disease gene -> distance 0
        (["X"], ["A"]),          # target absent from graph -> nan
    ]
    for targets, disease in cases:
        expected = _reference_dc(G, targets, disease)
        assert _equal(shortest_path.calculate_shortest_path(G, targets, disease), expected)


def test_disconnected_target_dropped_not_zero():
    # Two components: target 'A' can reach disease 'B'; target 'X' cannot reach
    # any disease and must be dropped (not counted as distance 0).
    G = nx.Graph()
    G.add_edges_from([("A", "B"), ("X", "Y")])
    d_c = shortest_path.calculate_shortest_path(G, ["A", "X"], ["B"])
    assert _equal(d_c, 1.0)

"""Mathematical invariants for Random Walk with Restart.

Audit patches 2 and 3: encode load-bearing invariants (node-relabeling
invariance, seed-order invariance, linearity / mean-of-single-seed) and an
independent dense linear-algebra oracle for the RWR operator.

These are deterministic property tests: each sweeps a fixed grid of graph
seeds/sizes so runs are fully reproducible without a property-based framework.
"""

import itertools

import numpy as np
import networkx as nx
import pytest

from network_tox.analysis.rwr import run_rwr, build_rwr_operator

GRAPH_SEEDS = [0, 1, 7, 42, 123, 2024]
SIZES = [6, 9, 14, 20]
CASES = list(itertools.product(SIZES, GRAPH_SEEDS))


def _connected_graph(n, seed):
    g = nx.gnp_random_graph(n, 0.35, seed=seed)
    if not nx.is_connected(g):
        g = g.subgraph(max(nx.connected_components(g), key=len)).copy()
    return g


@pytest.mark.parametrize("n,seed", CASES)
def test_node_relabeling_invariance(n, seed):
    """I2: relabeling nodes by a bijection permutes scores identically."""
    g = _connected_graph(n, seed)
    node_seeds = list(g.nodes())[:2]
    base = run_rwr(g, node_seeds)

    perm = {v: f"X{v}" for v in g.nodes()}
    g2 = nx.relabel_nodes(g, perm)
    got = run_rwr(g2, [perm[s] for s in node_seeds])

    for v in g.nodes():
        assert np.isclose(base[v], got[perm[v]], atol=1e-12)


@pytest.mark.parametrize("n,seed", CASES)
def test_seed_order_invariance(n, seed):
    """I1: the score vector is invariant to the order of the seed list."""
    g = _connected_graph(n, seed)
    node_seeds = list(g.nodes())[:3]
    forward = run_rwr(g, node_seeds)
    reverse = run_rwr(g, list(reversed(node_seeds)))
    assert all(np.isclose(forward[k], reverse[k], atol=1e-12) for k in forward)


@pytest.mark.parametrize("n,seed", CASES)
def test_rwr_linearity_mean_single_seed(n, seed):
    """I7/I8: uniform-restart multi-seed RWR equals the mean of single-seed RWRs.

    Run to a tight fixed point so both sides use the same converged operator.
    """
    g = _connected_graph(n, seed)
    node_seeds = list(g.nodes())[:3]
    multi = run_rwr(g, node_seeds, tol=1e-13, max_iter=5000)
    singles = [run_rwr(g, [s], tol=1e-13, max_iter=5000) for s in node_seeds]
    for v in g.nodes():
        expected = np.mean([s_[v] for s_ in singles])
        assert np.isclose(multi[v], expected, atol=1e-9)


@pytest.mark.parametrize("n,seed", list(itertools.product([8, 12], GRAPH_SEEDS)))
def test_dense_solve_oracle(n, seed):
    """I13/patch 3: iterative RWR matches p = alpha (I - (1-alpha) W)^{-1} r.

    An analytic check of the whole operator, independent of the iteration code.
    """
    g = _connected_graph(n, seed)
    alpha = 0.15
    W, nodes, node_idx = build_rwr_operator(g)
    W_dense = W.toarray()
    m = len(nodes)

    node_seeds = nodes[:2]
    r = np.zeros(m)
    for s in node_seeds:
        r[node_idx[s]] = 1.0 / len(node_seeds)

    p_exact = alpha * np.linalg.solve(np.eye(m) - (1 - alpha) * W_dense, r)
    scores = run_rwr(g, node_seeds, restart_prob=alpha, tol=1e-13, max_iter=5000)

    for i, node in enumerate(nodes):
        assert np.isclose(scores[node], p_exact[i], atol=1e-9)

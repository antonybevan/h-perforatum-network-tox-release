"""Random Walk with Restart (RWR) analysis."""

import numpy as np
import networkx as nx
from scipy import sparse

def build_rwr_operator(G):
    """
    Build the column-normalized transition matrix W = A D^-1 and node index.

    W depends only on the graph, not on the seed set, so for permutation testing
    (many random seed sets against one fixed graph) it can be built once and
    reused via ``run_rwr_from_operator``. This is numerically identical to letting
    ``run_rwr`` rebuild W on every call.

    Returns:
        (W, nodes, node_idx)
    """
    nodes = list(G.nodes())
    node_idx = {n: i for i, n in enumerate(nodes)}

    adj = nx.adjacency_matrix(G, nodelist=nodes)

    # Column-normalize adjacency matrix (W)
    # Convert to float to avoid integer division
    adj = adj.astype(float)
    # Sum of each column (degree)
    col_sum = np.array(adj.sum(axis=0)).flatten()
    # Avoid division by zero
    col_sum[col_sum == 0] = 1
    # Create diagonal matrix of inverse degrees
    d_inv = sparse.diags(1.0 / col_sum)
    # W = A * D^-1 (column normalized)
    # Note: Traditional definition is often W = D^-1 A (row normalized) or W = A D^-1 (column normalized)
    # The formula p = (1-a)W p + a r usually implies p is a column vector and W is column stochastic.
    # So if p_j is prob at node j, flow from j to i is M_ij * p_j.
    # M_ij = A_ij / deg(j). So W = A * D^-1.
    W = adj.dot(d_inv)
    return W, nodes, node_idx


def run_rwr_from_operator(W, nodes, node_idx, seeds, restart_prob=0.15, tol=1e-6, max_iter=100):
    """
    Run RWR given a prebuilt transition operator (see ``build_rwr_operator``).

    Identical iteration to ``run_rwr``; only the W construction is hoisted out so
    it can be shared across many seed sets.
    """
    n = len(nodes)

    # Create restart vector r
    r = np.zeros((n, 1))
    valid_seeds = [s for s in seeds if s in node_idx]

    if not valid_seeds:
        return {node: 0.0 for node in nodes}

    for seed in valid_seeds:
        r[node_idx[seed]] = 1.0 / len(valid_seeds)

    # Initialize p
    p = r.copy()

    # Iterate
    for _ in range(max_iter):
        p_new = (1 - restart_prob) * W.dot(p) + restart_prob * r
        diff = np.sum(np.abs(p_new - p))
        p = p_new
        if diff < tol:
            break

    return {nodes[i]: float(p[i, 0]) for i in range(n)}


def run_rwr(G, seeds, restart_prob=0.15, tol=1e-6, max_iter=100):
    """
    Run Random Walk with Restart using scipy.sparse.

    Formula: p^(t+1) = (1-alpha) * W * p^t + alpha * r

    Args:
        G: NetworkX graph
        seeds: List of seed nodes
        restart_prob: Restart probability (alpha)
        tol: Convergence tolerance
        max_iter: Maximum iterations

    Returns:
        Dictionary of {node: score}
    """
    if len(G) == 0:
        return {}

    W, nodes, node_idx = build_rwr_operator(G)
    return run_rwr_from_operator(
        W, nodes, node_idx, seeds,
        restart_prob=restart_prob, tol=tol, max_iter=max_iter,
    )

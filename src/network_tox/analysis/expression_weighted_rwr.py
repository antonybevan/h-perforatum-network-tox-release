"""
Expression-Weighted Random Walk with Restart (RWR)

Implements tissue-constrained influence propagation using transition-matrix
weighting based on protein expression.
"""

import warnings

import numpy as np
import networkx as nx
from scipy import sparse
from typing import Dict, List, Optional, Union
from pathlib import Path

# Minimum normalized expression assigned to non-/low-expressed nodes so they
# remain weakly traversable rather than becoming hard dead-ends in the EWI
# transition matrix. Exposed as a named constant for the expression-floor
# sensitivity analysis; the published results use 0.01.
EXPRESSION_FLOOR = 0.01


def load_liver_expression(
    gtex_file: Union[str, Path],
    tissue_column: str = "Liver"
) -> Dict[str, float]:
    """
    Load liver TPM values from GTEx v8 gene median TPM file.
    
    Args:
        gtex_file: Path to GTEx gene_median_tpm.gct file
        tissue_column: Name of tissue column to extract
        
    Returns:
        Dictionary mapping gene_symbol -> TPM value
    """
    import pandas as pd
    
    # GTEx .gct format: skip first 2 rows (version, dimensions)
    # Columns: Name, Description, then tissue columns
    df = pd.read_csv(gtex_file, sep='\t', skiprows=2)
    
    if tissue_column not in df.columns:
        raise ValueError(f"Tissue '{tissue_column}' not found. Available: {df.columns.tolist()}")
    
    # Use Description column as gene symbol (more readable than ENSG ID)
    expression = {}
    for _, row in df.iterrows():
        gene_symbol = row.get('Description', row.get('Name', ''))
        tpm = row.get(tissue_column, 0)
        if gene_symbol and pd.notna(tpm):
            expression[gene_symbol] = float(tpm)
    
    return expression


def normalize_expression_values(
    expression: Dict[str, float],
    nodes: List[str],
    method: str = "minmax",
    floor: float = EXPRESSION_FLOOR,
) -> np.ndarray:
    """
    Normalize expression values to [0, 1] range for transition weighting.
    
    Args:
        expression: Dictionary mapping gene -> TPM value
        nodes: List of all network nodes
        method: Normalization method ('minmax' or 'log_minmax')
        
    Returns:
        Array of normalized expression values (length = len(nodes))
    """
    n = len(nodes)
    expr_values = np.array([expression.get(node, 0.0) for node in nodes])
    
    if method == "log_minmax":
        # Log-transform then min-max normalize
        # Use log2(x+1) to match methodology strictly
        expr_values = np.log2(expr_values + 1)
    
    # Min-max normalize to [0, 1]
    # Add small epsilon to avoid perfect zeros (makes non-expressed nodes dead ends)
    min_val = expr_values.min()
    max_val = expr_values.max()
    
    if max_val > min_val:
        expr_normalized = (expr_values - min_val) / (max_val - min_val)
    else:
        expr_normalized = np.ones(n)  # All equal if no variance
    
    # Add small floor to avoid perfect zero (allow minimal propagation through non-expressed nodes)
    expr_normalized = np.maximum(expr_normalized, floor)
    
    return expr_normalized


def create_expression_weighted_transition_matrix(
    adj_matrix: sparse.spmatrix,
    expression: Dict[str, float],
    nodes: List[str]
) -> sparse.spmatrix:
    """
    Create transition matrix weighted by destination-node expression.
    """
    n = len(nodes)
    
    # Normalize expression to [0, 1]
    expr_normalized = normalize_expression_values(expression, nodes, method="log_minmax")
    
    # Weight each ROW by destination node expression: A'_ij = e_i * A_ij
    # This attracts signal to highly-expressed proteins (destination-node weighting)
    expr_diag = sparse.diags(expr_normalized)
    weighted_adj = expr_diag.dot(adj_matrix)
    
    # Column-normalize: each column sums to 1
    col_sum = np.array(weighted_adj.sum(axis=0)).flatten()
    col_sum[col_sum == 0] = 1.0  # Avoid division by zero
    d_inv = sparse.diags(1.0 / col_sum)
    W_prime = weighted_adj.dot(d_inv)
    
    return W_prime


def build_ewi_operator(
    G: nx.Graph,
    expression: Dict[str, float],
):
    """
    Build the expression-weighted transition matrix W' and node index.

    W' depends only on the graph and the expression vector, not on the seed set,
    so for permutation testing (many random seed sets on one fixed graph) it can
    be built once and reused via ``run_ewi_from_operator``. This is numerically
    identical to letting ``run_expression_weighted_rwr`` rebuild W' on every call.

    Returns:
        (W_prime, nodes, node_idx)
    """
    nodes = list(G.nodes())
    node_idx = {n: i for i, n in enumerate(nodes)}
    adj = nx.adjacency_matrix(G, nodelist=nodes).astype(float)
    W_prime = create_expression_weighted_transition_matrix(
        adj_matrix=adj,
        expression=expression,
        nodes=nodes,
    )
    return W_prime, nodes, node_idx


def run_ewi_from_operator(
    W_prime,
    nodes: List[str],
    node_idx: Dict[str, int],
    seeds: List[str],
    restart_prob: float = 0.15,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> Dict[str, float]:
    """
    Run expression-weighted RWR given a prebuilt operator (see ``build_ewi_operator``).

    Identical iteration to ``run_expression_weighted_rwr``; only the W' construction
    is hoisted out so it can be shared across many seed sets.
    """
    n = len(nodes)

    # Create UNIFORM restart vector over targets (not expression-weighted)
    r = np.zeros((n, 1))
    valid_seeds = [s for s in seeds if s in node_idx]

    if not valid_seeds:
        return {node: 0.0 for node in nodes}

    for seed in valid_seeds:
        r[node_idx[seed]] = 1.0 / len(valid_seeds)

    # Initialize p with restart vector
    p = r.copy()

    # Iterate until convergence (standard RWR iteration)
    diff = np.inf
    for iteration in range(max_iter):
        p_new = (1 - restart_prob) * W_prime.dot(p) + restart_prob * r
        diff = np.sum(np.abs(p_new - p))
        p = p_new
        if diff < tol:
            break
    else:
        # Loop exhausted max_iter without meeting tol: surface the residual so a
        # non-converged state is never silently returned as a "result".
        warnings.warn(
            f"Expression-weighted RWR did not converge in {max_iter} iterations "
            f"(L1 residual={diff:.2e} >= tol={tol:.1e}); returning last iterate.",
            RuntimeWarning,
            stacklevel=2,
        )

    return {nodes[i]: float(p[i, 0]) for i in range(n)}


def run_expression_weighted_rwr(
    G: nx.Graph,
    seeds: List[str],
    expression: Dict[str, float],
    restart_prob: float = 0.15,
    tol: float = 1e-6,
    max_iter: int = 100
) -> Dict[str, float]:
    """
    Run expression-weighted Random Walk with Restart.
    """
    if len(G) == 0:
        return {}

    W_prime, nodes, node_idx = build_ewi_operator(G, expression)
    return run_ewi_from_operator(
        W_prime, nodes, node_idx, seeds,
        restart_prob=restart_prob, tol=tol, max_iter=max_iter,
    )


def compute_dili_influence(
    rwr_scores: Dict[str, float],
    dili_genes: List[str]
) -> float:
    """
    Compute DILI influence as sum of RWR scores at DILI genes.
    
    Args:
        rwr_scores: Output from run_expression_weighted_rwr
        dili_genes: List of DILI-associated gene symbols
        
    Returns:
        Total influence score (sum of steady-state probabilities)
    """
    return sum(rwr_scores.get(gene, 0.0) for gene in dili_genes)


# =============================================================================
# COMPARISON WITH STANDARD RWR
# =============================================================================

def run_standard_rwr(
    G: nx.Graph,
    seeds: List[str],
    restart_prob: float = 0.15,
    tol: float = 1e-6,
    max_iter: int = 100
) -> Dict[str, float]:
    """
    Run standard (unweighted) RWR for comparison.

    Delegates to ``network_tox.analysis.rwr.run_rwr`` (identical column-normalised
    ``W = A D^{-1}`` walk with a uniform ``1/|T|`` restart vector) so there is a
    single source of truth for the standard RWR; the previous inline copy was
    byte-for-byte equivalent.
    """
    from .rwr import run_rwr
    return run_rwr(G, seeds, restart_prob=restart_prob, tol=tol, max_iter=max_iter)


# =============================================================================
# PERMUTATION TESTING COMPATIBILITY
# =============================================================================

def get_degree_matched_random_seeds(
    G: nx.Graph,
    original_seeds: List[str],
    expression: Dict[str, float],
    degree_tolerance: float = 0.25
) -> List[str]:
    """
    Sample degree-matched random seeds, preserving expression availability.
    
    For permutation testing, this ensures null distribution matches
    both degree and expression characteristics of original seeds.
    
    Args:
        G: NetworkX graph
        original_seeds: Original seed nodes to match
        expression: Expression dictionary (to ensure sampled nodes have expression)
        degree_tolerance: Fraction tolerance for degree matching (default ±25%)
        
    Returns:
        List of randomly sampled degree-matched seeds
    """
    import random
    
    nodes_in_G = set(G.nodes())
    valid_seeds = [s for s in original_seeds if s in nodes_in_G]
    
    if not valid_seeds:
        return []
    
    # Get all nodes with expression data
    expressed_nodes = [n for n in nodes_in_G if n in expression]
    
    random_seeds = []
    for seed in valid_seeds:
        seed_degree = G.degree(seed)
        min_degree = int(seed_degree * (1 - degree_tolerance))
        max_degree = int(seed_degree * (1 + degree_tolerance))
        
        # Find candidates with matching degree and expression
        candidates = [
            n for n in expressed_nodes
            if min_degree <= G.degree(n) <= max_degree and n not in random_seeds
        ]
        
        if candidates:
            random_seeds.append(random.choice(candidates))
        else:
            # Fallback: any expressed node
            fallback = [n for n in expressed_nodes if n not in random_seeds]
            if fallback:
                random_seeds.append(random.choice(fallback))
    
    return random_seeds

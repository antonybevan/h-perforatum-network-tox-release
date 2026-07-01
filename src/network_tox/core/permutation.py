"""Permutation testing."""

import numpy as np
from scipy import stats


def get_degree_matched_random(G, targets, n_sample, seed=None):
    """
    Get degree-matched random nodes.
    
    Args:
        G: NetworkX graph
        targets: Target nodes
        n_sample: Number to sample
        seed: Random seed
        
    Returns:
        List of random nodes
    """
    rng = np.random.default_rng(seed)
    
    degrees = dict(G.degree())
    target_degrees = [degrees[t] for t in targets if t in degrees]
    
    random_set = []
    nodes = list(G.nodes())
    
    for deg in target_degrees[:n_sample]:
        tol = max(1, int(deg * 0.25))
        candidates = [n for n in nodes 
                     if abs(degrees[n] - deg) <= tol 
                     and n not in targets 
                     and n not in random_set]
        if not candidates:
            candidates = [n for n in nodes if n not in targets and n not in random_set]
        if candidates:
            random_set.append(candidates[int(rng.integers(len(candidates)))])
    
    return random_set


def calculate_z_score(obs, null_dist):
    """Calculate Z-score from null distribution."""
    null_mean = np.mean(null_dist)
    null_std = np.std(null_dist)
    
    if null_std > 0:
        return (obs - null_mean) / null_std
    return 0.0


def calculate_empirical_p_value(observed, null_distribution, tail='one_greater'):
    """
    Calculate empirical p-value from null distribution.

    Args:
        observed: Observed value
        null_distribution: List or array of null values
        tail: Test direction
              'one_greater' (default): P = (sum(null >= obs) + 1) / (N + 1)
              'one_less': P = (sum(null <= obs) + 1) / (N + 1)
              'two': P = 2 * min(P_less, P_greater)

    Returns:
        Empirical p-value

    Note: We use the (r+1)/(n+1) formula to avoid zero p-values.
    """
    null_dist = np.array(null_distribution)
    n = len(null_dist)

    if n == 0:
        return np.nan

    if tail == 'one_greater':
        # Count how many null values are >= observed
        r = np.sum(null_dist >= observed)
        return (r + 1) / (n + 1)

    elif tail == 'one_less':
        # Count how many null values are <= observed
        r = np.sum(null_dist <= observed)
        return (r + 1) / (n + 1)

    elif tail == 'two':
        # Two-sided utility branch: 2 * min(P_less, P_greater)
        r_greater = np.sum(null_dist >= observed)
        p_greater = (r_greater + 1) / (n + 1)

        r_less = np.sum(null_dist <= observed)
        p_less = (r_less + 1) / (n + 1)

        return min(1.0, 2 * min(p_less, p_greater))

    else:
        raise ValueError(f"Unknown tail option: {tail}")

"""
Unit tests for permutation testing.
"""

import networkx as nx
import numpy as np
from network_tox.core import permutation


def test_get_degree_matched_random():
    """Test degree-matched sampling."""
    G = nx.barabasi_albert_graph(100, 3, seed=42)
    targets = list(G.nodes())[:10]
    
    random_set = permutation.get_degree_matched_random(G, targets, 5, seed=42)
    
    assert len(random_set) == 5
    assert len(set(random_set) & set(targets)) == 0  # No overlap


def test_get_degree_matched_random_does_not_mutate_global_rng():
    """Seeded sampling should not reset NumPy's process-global RNG state."""
    G = nx.barabasi_albert_graph(100, 3, seed=42)
    targets = list(G.nodes())[:10]

    np.random.seed(123)
    expected = np.random.random(3)
    np.random.seed(123)

    permutation.get_degree_matched_random(G, targets, 5, seed=42)

    observed = np.random.random(3)
    assert np.allclose(observed, expected)


def test_calculate_z_score():
    """Test Z-score calculation."""
    null_dist = [1, 2, 3, 4, 5]
    obs = 1
    
    z = permutation.calculate_z_score(obs, null_dist)
    
    # mean=3, std=sqrt(2), z=(1-3)/sqrt(2) = -1.414
    assert abs(z - (-1.414)) < 0.01


def test_empirical_two_sided_p_value_is_bounded():
    """Two-sided empirical p-values must remain in [0, 1]."""
    p = permutation.calculate_empirical_p_value(3, [1, 2, 3, 4, 5], tail='two')
    assert p == 1.0

"""Convergence residual guard for the RWR iterators (audit patch 4).

A walk that exhausts ``max_iter`` without reaching ``tol`` must surface a
warning rather than silently returning a non-converged iterate. A walk that
does converge must stay silent so the guard is not noise in the pipeline.
"""

import warnings

import networkx as nx
import pytest

from network_tox.analysis.rwr import run_rwr
from network_tox.analysis.expression_weighted_rwr import run_expression_weighted_rwr


def test_rwr_warns_on_nonconvergence():
    G = nx.path_graph(40)
    with pytest.warns(RuntimeWarning, match="did not converge"):
        run_rwr(G, [0], tol=1e-12, max_iter=2)


def test_ewi_warns_on_nonconvergence():
    G = nx.path_graph(40)
    expression = {n: 1.0 for n in G.nodes()}
    with pytest.warns(RuntimeWarning, match="did not converge"):
        run_expression_weighted_rwr(G, [0], expression, tol=1e-12, max_iter=2)


def test_rwr_silent_when_converged():
    G = nx.complete_graph(6)
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # any warning becomes a test failure
        run_rwr(G, [0], tol=1e-6, max_iter=100)

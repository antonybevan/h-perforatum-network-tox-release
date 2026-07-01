from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_operating_regime_benchmark as op  # noqa: E402


def test_degree_bins_merges_final_underfilled_tail():
    degrees = np.array([1] * 60 + [2] * 55 + [4] * 110 + [7] * 25)

    bins, upper_edges = op.degree_bins(degrees, min_bin=100)
    counts = np.bincount(bins)

    assert counts.tolist() == [115, 135]
    assert (counts >= 100).all()
    assert upper_edges.tolist() == [2.0, 7.0]


def test_load_real_pair_metrics_reads_canonical_shortest_path_table(tmp_path):
    path = tmp_path / "shortest_path.csv"
    pd.DataFrame(
        [
            {
                "network_threshold": 900,
                "compound": "Hyperforin",
                "n_targets": 10,
                "observed_dc": 1.3,
                "z_score": -3.8614552072649904,
            },
            {
                "network_threshold": 900,
                "compound": "Quercetin",
                "n_targets": 62,
                "observed_dc": 1.6774193548387095,
                "z_score": -5.440301947826024,
            },
        ]
    ).to_csv(path, index=False)

    real = op.load_real_pair_metrics(path=path)

    assert real["small_compound"] == "Hyperforin"
    assert real["large_compound"] == "Quercetin"
    assert real["small_n"] == 10
    assert real["large_n"] == 62
    assert np.isclose(real["large_dc"] - real["small_dc"], 0.3774193548387095)

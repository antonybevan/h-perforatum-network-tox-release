"""Integrity tests for committed result tables and the leakage decomposition.

These guard the manuscript's headline quantities against silent drift in the
committed CSVs. Several supplementary tables are hand-authored from these files
(see DATA_MANIFEST.md), so a drift here would surface in the manuscript without
any code error; these unit tests close that gap at finer granularity than
verify_numbers.py.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"


def _read(name):
    path = TABLES / name
    if not path.exists():
        pytest.skip(f"{path} not present")
    return pd.read_csv(path)


class TestLeakageDecomposition:
    def test_identity_raw_equals_direct_plus_propagated(self):
        df = _read("leakage_decomposition.csv")
        for _, row in df.iterrows():
            assert np.isclose(row["raw"], row["direct"] + row["propagated"], atol=1e-9), (
                f"{row['compound']}: raw != direct + propagated"
            )

    def test_components_nonnegative(self):
        df = _read("leakage_decomposition.csv")
        for col in ["raw", "direct", "propagated"]:
            assert (df[col] >= 0).all(), f"negative values in {col}"

    def test_hyperforin_raw_matches_perturbation_efficiency(self):
        # Raw per-target influence (PE) for Hyperforin; manuscript headline 0.1138.
        df = _read("leakage_decomposition.csv").set_index("compound")
        assert np.isclose(df.loc["Hyperforin", "raw"], 0.1138, atol=1e-3)

    def test_propagated_residual_ratio_in_reported_range(self):
        # Manuscript: the propagated advantage is a modest ~1.2-1.9x residual.
        df = _read("leakage_decomposition.csv").set_index("compound")
        ratio = df.loc["Hyperforin", "propagated"] / df.loc["Quercetin", "propagated"]
        assert 1.2 <= ratio <= 1.9, f"propagated ratio {ratio:.3f} outside reported 1.2-1.9x"


class TestConsolidatedResults:
    def test_efficiency_equals_observed_for_rwi(self):
        # Perturbation efficiency E = I under a uniform 1/|T| restart vector (not I/|T|).
        df = _read("consolidated_results.csv")
        rwi = df[df["metric"] == "RWI"]
        assert len(rwi) > 0, "no RWI rows in consolidated_results.csv"
        for _, row in rwi.iterrows():
            assert np.isclose(row["observed"], row["efficiency"], atol=5e-3), (
                f"{row['compound']}: efficiency != observed"
            )


class TestPValueConvention:
    @pytest.mark.parametrize("name", [
        "shortest_path_permutation_results.csv",
        "standard_rwr_lcc_permutation_results.csv",
        "expression_weighted_rwr_permutation_results.csv",
    ])
    def test_empirical_floor_no_underflow_style_values(self, name):
        # Conservative (r+1)/(n+1) floor at n=1000 is 1/1001 ~ 9.99e-4.
        df = _read(name)
        assert (df["p_value"] >= 1 / 1001 - 1e-9).all(), f"{name}: p below 1/1001 floor"


class TestNullVarianceShrinkage:
    def test_ratios_near_sqrt_62_over_10(self):
        # Null-SD ratio Hyperforin:Quercetin should track sqrt(62/10) ~ 2.49.
        df = _read("null_variance_shrinkage_audit.csv")
        ratios = df["std_ratio_hyperforin_over_quercetin"]
        assert ((ratios > 2.35) & (ratios < 3.10)).all(), (
            "null-SD ratios outside the sqrt(62/10)~2.49 band"
        )


class TestStringTextminingSensitivity:
    """Robustness of the Hyperforin>Quercetin ordering to STRING text-mining removal."""

    def _df(self):
        return _read("string_textmining_sensitivity.csv")

    def test_ordering_preserved_no_textmining(self):
        df = self._df()
        for metric in ["shortest_path_dc", "rwr_influence", "ewi_influence"]:
            for thr in (700, 900):
                sub = df[(df.metric == metric) & (df.network_threshold == thr)].set_index("compound")
                h = float(sub.loc["Hyperforin", "observed_notm"])
                q = float(sub.loc["Quercetin", "observed_notm"])
                if metric == "shortest_path_dc":
                    assert h < q, f"{metric} >={thr}: Hyperforin not closer without text-mining"
                else:
                    assert h > q, f"{metric} >={thr}: Hyperforin not higher without text-mining"

    def test_full_rebuild_reproduces_committed(self):
        # Rebuilding from the per-channel file (no text-mining filter) reproduces the
        # committed observed values -- validates the extraction is faithful.
        df = self._df()
        for _, r in df.iterrows():
            tol = 5e-3 if r["metric"] == "shortest_path_dc" else 2e-3
            assert np.isclose(r["observed_full_rebuild"], r["observed_committed"], atol=tol), (
                f"{r['metric']} >={r['network_threshold']} {r['compound']}: "
                f"full {r['observed_full_rebuild']} != committed {r['observed_committed']}"
            )

    def test_significant_without_textmining(self):
        df = self._df()
        assert (df["p_notm"] <= 0.05).all(), "some no-text-mining p-values are not significant"


class TestOperatingRegimeBenchmark:
    """Integrity checks for the target-count operating-regime benchmark."""

    def test_exact_real_ratio_and_named_unconditional_metrics(self):
        df = _read("operating_regime_reversal.csv")
        assert "uncond_discord" not in df.columns
        for col in ["uncond_directional_reversal", "uncond_rank_discord", "uncond_rank_concord"]:
            assert col in df.columns

        row = df[df["m_large"] == 62].iloc[0]
        assert np.isclose(row["R"], 6.2)
        assert 0.05 <= row["uncond_directional_reversal"] <= 0.07
        assert 0.10 <= row["uncond_rank_discord"] <= 0.14
        assert np.isclose(row["uncond_rank_discord"] + row["uncond_rank_concord"], 1.0)

    def test_operating_regime_summary_matches_corrected_design(self):
        sm = _read("operating_regime_summary.csv").iloc[0]
        assert -0.51 <= sm["slope_pinned"] <= -0.49
        assert 0.60 <= sm["delta_max_real"] <= 0.64
        assert np.isclose(sm["real_margin"], 0.3774193548387095)
        assert sm["real_overturnable"]
        assert sm["real_small_compound"] == "Hyperforin"
        assert sm["real_large_compound"] == "Quercetin"
        assert sm["real_n_small"] == 10
        assert sm["real_n_large"] == 62
        assert sm["canonical_target_rows"] == 72
        assert sm["canonical_unique_targets"] == 67
        assert sm["canonical_non_dili_target_rows"] == 67

    def test_moments_include_exact_62_and_profile_sensitivity(self):
        mom = _read("operating_regime_moments.csv")
        assert {"pinned", "pinned_non_dili", "uniform"} <= set(mom["mode"])
        for mode in ["pinned", "pinned_non_dili", "uniform"]:
            sub = mom[mom["mode"] == mode]
            assert 62 in set(sub["n_targets"])

    def test_reversal_confidence_intervals_are_bounded(self):
        df = _read("operating_regime_reversal.csv")
        ci_cols = [c for c in df.columns if c.endswith("_lo") or c.endswith("_hi")]
        for col in ci_cols:
            assert ((df[col] >= 0) & (df[col] <= 1)).all(), f"{col} outside [0, 1]"

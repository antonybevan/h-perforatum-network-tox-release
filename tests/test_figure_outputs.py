"""Smoke tests for committed figure outputs.

Lightweight, language-agnostic checks that every main figure exists and is a
valid, non-trivial PDF in both ``figures/main`` and the synchronized
``manuscript/figures`` copy. They intentionally do NOT re-run the R figure
scripts (which would churn the committed PDFs); they validate the published
artifacts so a missing or corrupt figure is caught by the test suite.
"""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIG_DIRS = [ROOT / "figures" / "main", ROOT / "manuscript" / "figures"]
FIG_STEMS = [
    "fig1_lollipop",
    "fig2_dumbbell",
    "fig3_ewi_waterfall",
    "fig4_ptni_phase",
    "fig5_bootstrap",
    "fig6_chemsim",
    "fig7_leakage",
    "fig8_opregime",
]


@pytest.mark.parametrize("fig_dir", FIG_DIRS, ids=lambda p: f"{p.parent.name}/{p.name}")
@pytest.mark.parametrize("stem", FIG_STEMS)
def test_figure_pdf_exists_and_valid(fig_dir, stem):
    pdf = fig_dir / f"{stem}.pdf"
    assert pdf.exists(), f"missing {pdf}"
    data = pdf.read_bytes()
    assert len(data) > 1000, f"{pdf} suspiciously small ({len(data)} bytes)"
    assert data[:5] == b"%PDF-", f"{pdf} is not a valid PDF (bad header)"


def test_all_eight_main_figures_present():
    missing = [s for s in FIG_STEMS if not (ROOT / "figures" / "main" / f"{s}.pdf").exists()]
    assert not missing, f"missing main figures: {missing}"

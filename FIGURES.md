# Figure File-to-Number Mapping

This repository's figure filenames reflect the original analysis order and do not match the final LaTeX figure numbers. LaTeX numbers figures by appearance order in `main.tex`; the compiled PDF is correct. This file documents the mapping.

| LaTeX Number | Filename | Label | Description |
|---|---|---|---|
| Figure 1 | `fig1_lollipop.pdf` | `fig:context` | Network context — target count and shortest-path proximity |
| Figure 2 | `fig2_dumbbell.pdf` | `fig:dumbbell` | Effect size and evidence dissociate |
| Figure 3 | `fig8_opregime.pdf` | `fig:opregime` | Operating regime — null-precision law and rank reversal |
| Figure 4 | `fig4_ptni_phase.pdf` | `fig:efficiency` | Perturbation efficiency |
| Figure 5 | `fig3_ewi_waterfall.pdf` | `fig:ewi` | Expression-weighted influence waterfall |
| Figure 6 | `fig7_leakage.pdf` | `fig:leakage` | Direct vs propagated decomposition |
| Figure 7 | `fig6_chemsim.pdf` | `fig:chemsim` | Chemical-similarity control |
| Figure S1 | `fig5_bootstrap.pdf` | `fig:bootstrap` | Bootstrap sensitivity (baseline) |

All figures exist in both `figures/main/` (canonical output from R scripts) and `manuscript/figures/` (synchronized copies for LaTeX compilation). Both PDF (vector) and TIFF (300 DPI raster) versions are provided.

The R scripts that generate each figure are:
- `R/fig1_lollipop.R` → Figure 1
- `R/fig2_dumbbell.R` → Figure 2
- `R/fig8_opregime.R` → Figure 3
- `R/fig4_ptni_phase.R` → Figure 4
- `R/fig3_ewi_waterfall.R` → Figure 5
- `R/fig7_leakage.R` → Figure 6
- `R/fig6_chemsim.R` → Figure 7
- `R/fig5_bootstrap.R` → Figure S1

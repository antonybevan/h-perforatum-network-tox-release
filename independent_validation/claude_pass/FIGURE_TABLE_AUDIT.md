# Figure & Table Audit — Scientific Reports Submission Standards

**Date:** 2026-07-01

---

## Figures: 7 main + 1 supplementary

| Fig | Filename | LaTeX # | Width | DPI | Format | Caption Ok? |
|-----|----------|---------|-------|-----|--------|-------------|
| 1 | fig1_lollipop | 1 ✓ | 2125×1122 | 300 | PDF+TIFF | ✓ |
| 2 | fig2_dumbbell | 2 ✓ | 2125×1299 | 300 | PDF+TIFF | ✓ |
| 3 | fig8_opregime | 3 ⚠️ | 3188×1122 | 300 | PDF+TIFF | ✓ |
| 4 | fig4_ptni_phase | 4 ✓ | 3307×1653 | 300 | PDF+TIFF | ✓ |
| 5 | fig3_ewi_waterfall | 5 ⚠️ | 2125×1535 | 300 | PDF+TIFF | ✓ |
| 6 | fig7_leakage | 6 ⚠️ | 2244×1122 | 300 | PDF+TIFF | ✓ |
| 7 | fig6_chemsim | 7 ⚠️ | 1889×1535 | 300 | PDF+TIFF | ✓ |
| S1 | fig5_bootstrap | S1 ⚠️ | 1889×1417 | 300 | PDF+TIFF | ✓ |

⚠️ 4 filenames don't match LaTeX numbers. PDF is correct. Source tree misleading.

## Tables: 4 main + 16 supplementary

| Table | Caption | Issues |
|-------|---------|--------|
| 1 | Effect size vs evidence | ✓ |
| 2 | Null SD scaling | ✓ |
| 3 | Direct vs propagated | ✓ |
| 4 | Guney fidelity | ✓ |
| S1 | Target curation | ✓ |
| S2 | Hyperforin targets | ✓ |
| S3 | Null parameters | ✓ |
| S4 | Operating-regime reversal | ✓ (caption now says "above 90th percentile") |
| S5 | Text-mining | ✓ |
| S6 | Threshold robustness | ✓ |
| S7 | α sensitivity | ⚠️ no backing CSV |
| S8 | Floor sensitivity | ⚠️ no backing CSV |
| S9 | Leak controls | ⚠️ no backing CSV |
| S10 | Network separation | ⚠️ no backing CSV |
| S11 | Direct connectivity | ⚠️ no backing CSV |
| S12 | Module sensitivity | ✓ |
| S13 | Guney null params | ✓ |
| S14 | Quercetin targets | ✓ |
| S15 | Curation | ⚠️ no backing CSV |
| S16 | DILI genes | ✓ |

## Checklist vs Scientific Reports Requirements

| Requirement | Status |
|-------------|--------|
| Vector PDF figures | ✓ all figures have PDF versions |
| 300+ DPI TIFF | ✓ all 300 DPI |
| booktabs tables | ✓ |
| siunitx decimal alignment | ✓ present in main tables |
| Line numbers | ✓ |
| 1.5 spacing | ✓ |
| Running header | ✓ |
| Data availability statement | ✓ |
| Code availability statement | ✓ |
| No unresolved references | ✓ |
| No overfull hboxes | ✓ |
| References in journal style | ⚠️ unsrtnat (numbered), close to Vancouver |
| Figure captions self-contained | ✓ |
| AI-use disclosure | ✓ in Methods |

## Issues Requiring Attention

1. **Figure filenames don't match LaTeX numbers** — 4 of 7 mismatched. Won't affect review but may confuse editors if they check source files. Either rename files or add a FIGURES.md mapping.

2. **5 supplementary tables lack committed CSV sources** (S7, S8, S9, S10, S11, S15) — numbers are hardcoded in LaTeX. Peer reviewers can't independently verify these without re-running the pipeline.

3. **d_c renders correctly in PDF** — text extraction shows "dc" but PDF rendering shows proper subscript. No issue.

4. **Cover letter needs recompile** — patched but not rebuilt.

5. **References style** — `unsrtnat` produces numbered citations. Scientific Reports accepts this but check exact requirements in the author guidelines.

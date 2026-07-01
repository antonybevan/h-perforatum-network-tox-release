# Separating effect size from statistical evidence in network-proximity rankings under target-count asymmetry: a controlled liver-interactome audit

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Release gates](https://github.com/antonybevan/h-perforatum-network-tox-release/actions/workflows/tests.yml/badge.svg)](https://github.com/antonybevan/h-perforatum-network-tox-release/actions/workflows/tests.yml)
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Docs License: CC BY 4.0](https://img.shields.io/badge/docs%20%26%20data-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Platform: Linux | macOS | Windows](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)](https://github.com/antonybevan/h-perforatum-network-tox-release)

Complete, reproducible research pipeline, data, and manuscript source for a **controlled methodological audit of network-proximity rankings under target-count asymmetry**. The manuscript separates three quantities that are easy to conflate: raw topological effect (`d_c`), standardized evidence (`Z`), and mean per-target random-walk influence (`E`). The central claim is not that proximity is biased, but that cross-compound ranking by Z-score magnitude can diverge from raw effect-size ranking because the larger target set has a sharper null.

---

## Scientific context

A network-proximity Z-score standardizes an observed target-disease distance against a size- and degree-matched random null (Guney et al. 2016; Menche et al. 2015). Because a Z-score is an effect divided by a null standard deviation, and that standard deviation shrinks with target count (approximately `|T|^-1/2`, the law of large numbers), **Z-score magnitude should not be read as a cross-compound effect-size ranking when target counts differ greatly.** This is expected precision, not a defect of proximity. We confirm the `|T|^-1/2` scaling for shortest-path, random-walk, and expression-weighted influence alike.

We therefore report an explicit effect size alongside standardized evidence. **Perturbation efficiency** is the mean per-target random-walk-with-restart influence on the disease module; by linearity of the walk, it equals the average single-target influence. It is an effect-size complement to the Z-score, not a replacement, and its own Z-score is subject to the same null-SD shrinkage.

The empirical pair is a deliberately high-contrast diagnostic example, not a representative compound sample: Hyperforin (10 targets) and Quercetin (62), two *Hypericum perforatum* constituents with about a 6-fold target-count ratio. Hyperforin is the PXR-activating, CYP/transporter-inducing constituent behind St John's Wort's hepatic drug-drug interactions, making it a mechanistic positive control for engagement of the DILI module's xenobiotic-metabolism axis; it is not claimed to be an intrinsic hepatotoxin. Quercetin is the high-target-count comparator, not a DILI outcome control.

A degree-controlled liver-network calibration benchmark then asks when the `|T|^-1/2` null-precision law is large enough to reverse raw-distance and Z-score rankings. Material reversal is a located, conditional regime: in this network it appears when the smaller set is above the 90th percentile of probe-pair margins, while unconditional raw/Z rank discordance is about 12% at the Hyperforin/Quercetin target-count ratio.

### Key numbers (STRING ≥900 liver LCC)

| Compound | Targets | Closest distance *d*c | Proximity *Z* | Perturbation efficiency *E* | Direct component | Propagated component |
|----------|---------|------------------------|----------------|-----------------------------|------------------|----------------------|
| **Hyperforin** | 10 | **1.30** | −3.86 | **0.1138** | 0.0711 | 0.0427 |
| **Quercetin**  | 62 | 1.68 | **−5.44** | 0.0322 | 0.0032 | 0.0290 |

Hyperforin is topologically closer by closest-path distance (smaller *d*c) yet has the weaker standardized evidence at STRING >=900 (smaller |*Z*|). The raw-distance ranking is stable across the evaluated thresholds, while the proximity-Z evidence ranking reverses.

> [!IMPORTANT]
> The raw per-target influence advantage (~3.5x) is dominated by direct target-DILI overlap: four of ten Hyperforin targets (ABCB1, CYP2C9, MMP2, NR1I2) are themselves DILI-module genes. The propagated component is more modest (~1.5x; bounded to ~1.2-1.9x across alternative exclusions), remains above a degree-matched background, and overlaps the upper tail of size-matched Quercetin subsets. This is a decomposition of effect size, not a DILI prediction.

---

## Reproducibility

```bash
git clone https://github.com/antonybevan/h-perforatum-network-tox-release
cd h-perforatum-network-tox-release
pip install -r requirements-lock.txt          # pinned versions (Python 3.12)
```

```bash
python scripts/run_pipeline.py                # full pipeline (network → permutations → controls → revision audits)
python verify_numbers.py                      # honesty gate: number consistency + forbidden-claim scan
python REVIEWER_EVIDENCE.py                    # regenerate the headline effect/evidence numbers
python REVIEWER_EVIDENCE_leakage_scaling.py    # leakage audit + null-SD scaling
python scripts/run_operating_regime_benchmark.py # operating-regime benchmark
python GUNEY_FIDELITY_check.py                 # revalidation vs Guney's emreg00/toolbox
```

Data integrity is anchored by `data/CHECKSUMS.sha256` (`shasum -a 256 -c data/CHECKSUMS.sha256`). All randomised steps use a fixed seed (42); permutation analyses use *n* = 1000, and the operating-regime benchmark uses 20,000 probes plus 500,000 probe pairs per size-pair cell. Figures: `Rscript R/fig1_lollipop.R` … `R/fig8_opregime.R`. The STRING no-text-mining sensitivity requires gitignored per-channel STRING downloads listed in `DATA_MANIFEST.md`.

---

## Repository structure

```text
├── src/network_tox/        # core modules: RWR, expression-weighted RWR, proximity, permutation
├── scripts/                # pipeline + analysis scripts (22-step pipeline)
├── R/                      # publication figure scripts (8 figures + setup)
├── data/                   # committed processed inputs + raw sources + CHECKSUMS.sha256
├── results/tables/         # computed tables (proximity / RWR / EWI / leakage / operating regime)
├── manuscript/             # LaTeX source (Scientific Reports format) and compiled PDF
├── tests/                  # validation suite (113 tests)
├── independent_validation/ # audit trail (codex_pass/ + claude_pass/)
├── FIGURES.md              # figure filename-to-LaTeX-number mapping
├── reproducibility.lock.yml# pinned environment specification
└── requirements-lock.txt   # pinned Python dependencies
```

## Audit & Reproducibility

This repository has passed a full adversarial multi-agent audit. Key verification:

| Gate | Command | Result |
|---|---|---|
| Number consistency | `python verify_numbers.py` | PASS |
| Data integrity | `python scripts/validate_data_integrity.py` | ALL CHECKS PASSED |
| Unit tests | `python -m pytest -q` | 113 passed |
| Checksums | `shasum -a 256 -c data/CHECKSUMS.sha256` | 45/45 OK |
| Full pipeline | `python scripts/run_pipeline.py` | 22/22 steps pass |
| Reviewer evidence | `python REVIEWER_EVIDENCE.py` | PASS |
| Guney fidelity | `python GUNEY_FIDELITY_check.py` | PASS |

Full audit reports in `independent_validation/claude_pass/`. See `MASTER_AUDIT_DASHBOARD.md` for the consolidated verdict.

---

## Methodology summary

1. **Network** — STRING v12.0 *functional association* network (combined score ≥900; integrates experimental, curated, co-expression, genomic-context and text-mining channels — **not** a purely physical PPI network), liver-filtered (GTEx v8 liver TPM ≥1), largest connected component.
2. **Proximity** — closest distance *d*c (Guney et al. 2016), degree-matched permutation *Z* (*n* = 1000, seed 42), conservative empirical (*r*+1)/(*n*+1) *p*-values.
3. **Perturbation efficiency** — mean per-target RWR influence (column-normalised *W = A D*⁻¹, restart α = 0.15; Köhler et al. 2008), equal by linearity to the size-normalised joint influence.
4. **Expression weighting** — destination-node liver-TPM transition weighting (sensitivity analysis).
5. **Direct/propagated decomposition** — separates mass on target-DILI overlap nodes from propagated influence; compares the propagated component against a global degree-matched background and size-matched Quercetin subsets.
6. **Guney fidelity** — revalidation against the canonical `emreg00/toolbox` under fixed-disease and two-sided nulls.
7. **Chemical-similarity control** — maximum Tanimoto (ECFP4) to DILIrank 2.0 reference drugs (both compounds < 0.4), arguing against close structural-analogue confounding within that reference set.
8. **Operating-regime benchmark** — degree-controlled random probes quantify when target-count asymmetry can reverse raw-distance and Z-score rankings; no toxicity outcome is modeled.

---

## License

This repository is dual-licensed by artifact type:

- **Code** (analysis pipeline, metrics, permutation/leakage/Guney-fidelity analyses, and figure scripts) is released under the **MIT License**. See `LICENSE`.
- **Manuscript text, figures, and data** (the `manuscript/`, `figures/`, `data/`, and `results/` artifacts) are released under the **Creative Commons Attribution 4.0 International (CC-BY-4.0)** license. See `LICENSE-CC-BY-4.0`.

## Citation

If you use this pipeline or data, please cite (update with the published DOI on acceptance):

```bibtex
@article{bevan_effectsize_evidence,
  title   = {Separating effect size from statistical evidence in network-proximity
             rankings under target-count asymmetry: a controlled liver-interactome audit},
  author  = {Bevan, Antony},
  journal = {(under review, Scientific Reports)},
  year    = {2026},
  note    = {Code: https://github.com/antonybevan/h-perforatum-network-tox-release}
}
```

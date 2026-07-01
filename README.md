# Separating effect size from statistical evidence in network-proximity rankings under target-count asymmetry: a controlled liver-interactome audit

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Release gates](https://github.com/antonybevan/h-perforatum-network-tox-release/actions/workflows/tests.yml/badge.svg)](https://github.com/antonybevan/h-perforatum-network-tox-release/actions/workflows/tests.yml)
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Docs License: CC BY 4.0](https://img.shields.io/badge/docs%20%26%20data-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Platform: Linux | macOS | Windows](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)](https://github.com/antonybevan/h-perforatum-network-tox-release)

Complete, reproducible research pipeline, data, and manuscript source for a **controlled methodological audit of network-proximity statistics**. Using two constituents of *Hypericum perforatum* with an extreme target-count asymmetry, we show that a proximity Z-score is a calibrated *evidence* statistic whose *magnitude* should not be read as a cross-compound *effect-size* ranking when target counts differ greatly — and we recommend reporting an explicit effect size (**perturbation efficiency**) alongside it.

---

## Scientific context

A network-proximity Z-score standardises an observed target–disease distance against a size- and degree-matched random null (Guney et al. 2016; Menche et al. 2015). Because a Z-score is an effect divided by a null standard deviation, and that standard deviation shrinks with target count (≈ |T|^−1/2, the law of large numbers), **Z-score magnitude is not comparable across compounds with very different target counts.** This is the distinction between statistical significance and effect size emphasised by the ASA statement (Wasserstein & Lazar 2016) — *expected precision, not a defect of any metric.* We confirm the |T|^−1/2 scaling for shortest-path, random-walk, and expression-weighted influence alike.

We therefore recommend reporting an effect size alongside the evidence Z-score. **Perturbation efficiency** is the mean per-target random-walk-with-restart influence on the disease module — by linearity of the walk, exactly the size-normalised propagated influence. It is an effect-size **complement** to the Z-score, not a replacement.

*H. perforatum* provides a deliberately adversarial stress-test pair (not a representative sample): Hyperforin (10 targets) and Quercetin (62), two constituents considered here because they differ ~6× in target count. Hyperforin is a **mechanistic positive control** — the PXR-activating, cytochrome-P450/transporter-inducing constituent behind St John's Wort's hepatic drug–drug interactions (Moore et al. 2000) — though *not* itself an established intrinsic hepatotoxin (LiverTox). Quercetin is used as the high-target-count comparator, not as a DILI outcome control.

### Key numbers (STRING ≥900 liver LCC)

| Compound | Targets | Closest distance *d*c | Proximity *Z* | RWR influence *Z* | Perturbation efficiency *E* |
|----------|---------|------------------------|----------------|--------------------|------------------------------|
| **Hyperforin** | 10 | **1.30** | −3.86 | +10.12 | **0.1138** |
| **Quercetin**  | 62 | 1.68 | **−5.44** | +4.55 | 0.0322 |

Hyperforin is topologically *closer* by closest-path distance (smaller *d*c) yet less *"significant"* (smaller \|*Z*\|): effect size and standardised evidence dissociate, and the Z-ranking reverses across network thresholds while the *d*c ranking does not.

> [!IMPORTANT]
> The raw per-target efficiency advantage (~3.5×) is **partly circular**: four of ten Hyperforin targets (ABCB1, CYP2C9, MMP2, NR1I2) are themselves DILI-module genes. A target–disease overlap audit gives a **modest leakage-controlled residual (~1.2–1.9×) with overlapping distributions** (~99.9th percentile against a degree-matched background; does not exceed all random sets). We do **not** claim a clean topological separation, nor that Hyperforin is an intrinsic hepatotoxin.

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
├── validation_cleanroom/   # independent reimplementations for verification
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
5. **Target–disease overlap (leakage) audit** — removes circular target–module overlap; compares against a global degree-matched background and size-matched Quercetin subsets.
6. **Guney fidelity** — revalidation against the canonical `emreg00/toolbox` under fixed-disease and two-sided nulls.
7. **Chemical-similarity control** — maximum Tanimoto (ECFP4) to DILIrank 2.0 reference drugs (both compounds < 0.4, excluding structural confounding).
8. **Operating-regime benchmark** — degree-controlled random probes quantify when target-count asymmetry can reverse raw-distance and Z-score rankings; no toxicity outcome is modelled.

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

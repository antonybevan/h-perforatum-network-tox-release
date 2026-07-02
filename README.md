# Separating effect size from statistical evidence in network-proximity rankings under target-count asymmetry: a controlled liver-interactome audit

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Docs License: CC BY 4.0](https://img.shields.io/badge/docs%20%26%20data-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Platform: Linux | macOS | Windows](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)](https://github.com/antonybevan/h-perforatum-network-tox-release)

Complete, reproducible research pipeline, data, and manuscript source for a **controlled methodological audit of network-proximity statistics**. In a liver-expressed STRING interactome, the null standard deviation of averaged target--disease statistics shrinks approximately as |T|^−1/2, so standardized evidence can rank a larger target set above a smaller set even when its raw closest-distance effect is weaker. Two *Hypericum perforatum* constituents with a 6.2× target-count ratio provide the worked biological instance. We recommend reporting raw effect size, standardized evidence, and per-target random-walk influence decomposed into direct target–disease overlap and propagated influence.

---

## Scientific context

A network-proximity Z-score standardizes an observed target–disease distance against a size- and degree-matched random null (Guney et al. 2016; Menche et al. 2015). Because a Z-score is an effect divided by a null standard deviation, and that standard deviation shrinks with target count (≈ |T|^−1/2, the law of large numbers), **Z-score magnitude should not be read as a direct effect-size ranking across compounds with very different target counts.** This is the distinction between statistical significance and effect size emphasized by the ASA statement (Wasserstein & Lazar 2016) — *expected precision, not a defect of any metric.* We confirm the |T|^−1/2 scaling for shortest-path, random-walk, and expression-weighted influence alike.

We therefore recommend reporting an effect size alongside the evidence Z-score. **Perturbation efficiency** is the mean per-target random-walk-with-restart influence on the disease module by linearity of the walk. It is an effect-size **complement** to the Z-score, not a replacement, and in this paper it is further decomposed into direct target--DILI overlap and propagated influence.

*H. perforatum* provides a worked biological instance within this characterized regime: Hyperforin (10 targets) and Quercetin (62), two constituents considered here because they differ ~6× in target count. Hyperforin is a **mechanistic positive control** — the PXR-activating, cytochrome-P450/transporter-inducing constituent behind St John's Wort's hepatic drug–drug interactions (Moore et al. 2000) — though *not* itself an established intrinsic hepatotoxin (LiverTox). Quercetin is used as the high-target-count comparator, not as a DILI outcome control.

### Key numbers (STRING ≥900 liver LCC)

| Compound | Targets | Closest distance *d*c | Proximity *Z* | Perturbation efficiency *E* | Direct overlap | Propagated influence |
|----------|---------|------------------------|----------------|------------------------------|----------------|----------------------|
| **Hyperforin** | 10 | **1.30** | −3.86 | **0.1138** | 0.0711 | **0.0427** |
| **Quercetin**  | 62 | 1.68 | **−5.44** | 0.0322 | 0.0032 | 0.0290 |

Hyperforin is topologically *closer* by closest-path distance (smaller *d*c) yet less *"significant"* (smaller |*Z*|): effect size and standardized evidence dissociate, and the Z-ranking reverses across network thresholds while the *d*c ranking does not.

> [!IMPORTANT]
> The raw per-target efficiency advantage (~3.5×) is 62% direct target–DILI overlap. A target–disease overlap audit gives a **modest leakage-controlled residual (~1.2–1.9×) with overlapping distributions**. The propagated component is above a degree-matched background (99.9th percentile) but within the spread of size-matched Quercetin subsets; alternative exclusions bound the advantage to 1.2–1.9×.

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

Data integrity is anchored by `data/CHECKSUMS.sha256` (`shasum -a 256 -c data/CHECKSUMS.sha256`). All randomized steps use a fixed seed (42); permutation analyses use *n* = 1000, and the operating-regime benchmark uses 20,000 probes plus 500,000 probe pairs per size-pair cell. Figures: `Rscript R/fig1_lollipop.R` … `R/fig8_opregime.R`. The STRING no-text-mining sensitivity requires gitignored per-channel STRING downloads listed in `DATA_MANIFEST.md`.

---

## Repository structure

```text
├── src/network_tox/        # core modules: RWR, expression-weighted RWR, proximity, permutation
├── scripts/                # pipeline + analysis scripts (22-step pipeline)
├── R/                      # publication figure scripts (8 figures + setup)
├── data/                   # committed processed inputs + raw sources + CHECKSUMS.sha256
├── results/tables/         # computed tables (proximity / RWR / EWI / leakage / operating regime)
├── manuscript/             # LaTeX source (Scientific Reports format) and compiled PDF
├── tests/                  # validation suite (unit + invariant/oracle tests)
├── independent_validation/ # audit trail (codex_pass/ + claude_pass/)
├── validation_cleanroom/   # independent reimplementations for verification
├── FIGURES.md              # figure filename-to-LaTeX-number mapping
├── reproducibility.lock.yml# pinned environment specification
└── requirements-lock.txt   # pinned Python dependencies
```

## Audit & Reproducibility

This repository has passed a full adversarial multi-agent audit. All gates below are run in a clean Python 3.12 environment installed from `requirements-lock.txt`:

| Gate | Command | Result |
|---|---|---|
| Number consistency | `python verify_numbers.py` | PASS |
| Data integrity | `python scripts/validate_data_integrity.py` | ALL CHECKS PASSED |
| Unit tests | `python -m pytest -q` | PASS (227 tests, locked Python 3.12 env) |
| Checksums | `shasum -a 256 -c data/CHECKSUMS.sha256` | PASS |
| Reviewer evidence | `python REVIEWER_EVIDENCE.py` | PASS |
| Guney fidelity | `python GUNEY_FIDELITY_check.py` | PASS |
| Full pipeline | `python scripts/run_pipeline.py` | end-to-end regeneration; run as the clean-clone release gate (one permutation step reproduces within Monte-Carlo variance) |

Full audit reports in `independent_validation/claude_pass/`. See `MASTER_AUDIT_DASHBOARD.md` for the consolidated verdict.

---

## Methodology summary

This order mirrors the manuscript Methods section.

1. **Interactome and modules** — STRING v12.0 *functional association* network (combined score ≥900; integrates experimental, curated, co-expression, genomic-context and text-mining channels — **not** a purely physical PPI network), liver-filtered (GTEx v8 liver TPM ≥1), largest connected component. The STRING ≥700 liver LCC is used for threshold robustness.
2. **Closest distance and proximity Z-score** — closest distance *d*c (Guney et al. 2016), degree-matched permutation *Z* (*n* = 1000, seed 42), conservative empirical (*r*+1)/(*n*+1) *p*-values. The primary null randomizes targets while holding the DILI module fixed; Guney-style two-sided nulls are reported as a fidelity sensitivity.
3. **Random walk with restart and perturbation efficiency** — column-normalized *W = A D*⁻¹, restart α = 0.15 (Köhler et al. 2008). Perturbation efficiency *E* equals the mean per-target influence by linearity of the steady state in the restart vector and is used as an effect-size complement to the Z-score.
4. **Expression weighting** — destination-node liver-TPM transition weighting, with floor sensitivity showing the expression floor is immaterial.
5. **Direct--propagated decomposition** — separates direct target--DILI overlap from propagated random-walk influence; compares the propagated component against a global degree-matched background, size-matched Quercetin subsets, target-exclusion controls, network separation, direct-connectivity checks, DILI-module sensitivity, and STRING text-mining robustness.
6. **Chemical-similarity control** — maximum Tanimoto similarity (ECFP4) to DILIrank 2.0 reference drugs; both compounds are below the 0.4 structural-analogue threshold, arguing against close structural-analogue confounding within the DILIrank reference set.
7. **Operating-regime benchmark** — degree-controlled random probes (20,000 per size, 500,000 cross-size pairs) characterize when |T|^−1/2 null-precision scaling can reverse Z-score vs. raw-distance rankings; no toxicity outcome is modeled.
8. **Reproducibility** — pinned Python/R environments, fixed seed 42, SHA-256 checksums, verification scripts, full pipeline regeneration, figure scripts, and archive checks.

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

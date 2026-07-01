# AGENT_E_CIRCULARITY_LEAKAGE_REPORT

Read-only audit completed. I did not edit, create, move, delete, patch, install, or regenerate files.

**Overall:** PARTIAL PASS. The repository is much stronger than a naive circularity-prone analysis: target-DILI overlap is disclosed, leave-one-out decomposition exists, no-text-mining and disease-module controls exist, and stale overclaim phrases were not found. Main residual risks are hardcoded real-pair values in operating-regime figure/generator code, several hand-authored manuscript tables, cache/external-data dependence, and inability to run the full `verify_numbers.py` gate in the current Python environment.

| Area | Status | Evidence |
|---|---:|---|
| Target-DILI overlap disclosure | PASS | Hyperforin intersect DILI = `ABCB1,CYP2C9,MMP2,NR1I2`; Quercetin intersect DILI = `MMP2`. Disclosed in [results.tex](/Users/apple/Downloads/h-perforatum-network-tox-clean/manuscript/sections/results.tex:70), source data [targets_lcc.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/data/processed/targets_lcc.csv:1), [dili_900_lcc.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/data/processed/dili_900_lcc.csv:1). |
| Leave-one-out propagated scoring | PASS | `Eself()` excludes target seeds from DILI scoring in [generate_leakage_figure_data.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/generate_leakage_figure_data.py:31); output table shows raw/direct/propagated split in [leakage_decomposition.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/leakage_decomposition.csv:1). |
| DILI-member seed removal | PARTIAL | Implemented in reviewer evidence script only, not persisted as a dedicated CSV/tested table: [REVIEWER_EVIDENCE_leakage_scaling.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/REVIEWER_EVIDENCE_leakage_scaling.py:27), hand-authored in [supplementary.tex](/Users/apple/Downloads/h-perforatum-network-tox-clean/manuscript/sections/supplementary.tex:225). |
| CYP/transporter removal | PARTIAL | Implemented as Hyperforin-specific removal of `CYP3A4,CYP2C9,CYP2B6,ABCB1,ABCC2,ABCG2`; Quercetin remains unchanged, so this is not a symmetric all-compound CYP/transporter exclusion: [REVIEWER_EVIDENCE_leakage_scaling.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/REVIEWER_EVIDENCE_leakage_scaling.py:29). |
| Shared-target removal | PARTIAL | Shared targets are removed from both sets in script, but values are not in a generated CSV: [REVIEWER_EVIDENCE_leakage_scaling.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/REVIEWER_EVIDENCE_leakage_scaling.py:32), [results.tex](/Users/apple/Downloads/h-perforatum-network-tox-clean/manuscript/sections/results.tex:86). |
| Quercetin subset controls | PASS | Raw bootstrap is clearly labelled baseline/superseded; leakage-adjusted Quercetin 10-subsets are present with 1,000 draws and overlapping upper tail: [run_bootstrap_sensitivity.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_bootstrap_sensitivity.py:99), [generate_leakage_figure_data.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/generate_leakage_figure_data.py:53), [supplementary.tex](/Users/apple/Downloads/h-perforatum-network-tox-clean/manuscript/sections/supplementary.tex:231). |
| Disease-module sensitivity | PASS | Removes the four Hyperforin-overlap DILI genes and writes `dili_module_sensitivity.csv`: [run_dili_module_sensitivity.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_dili_module_sensitivity.py:7), [dili_module_sensitivity.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/dili_module_sensitivity.csv:1). |
| Text-mining circularity | PARTIAL | No-text-mining rebuild/control exists with integrity gate and committed output, but raw per-channel STRING payloads are external/gitignored and I did not rerun writer paths: [run_string_textmining_sensitivity.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_string_textmining_sensitivity.py:115), [string_textmining_sensitivity.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/string_textmining_sensitivity.csv:1), [DATA_PROVENANCE.md](/Users/apple/Downloads/h-perforatum-network-tox-clean/DATA_PROVENANCE.md:44). |
| Operating-regime probe exclusions | PASS | Probe pool excludes DILI genes (`V\D`), and non-DILI target-profile sensitivity exists: [run_operating_regime_benchmark.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_operating_regime_benchmark.py:78), [methods.tex](/Users/apple/Downloads/h-perforatum-network-tox-clean/manuscript/sections/methods.tex:22). |
| Pseudo-module controls | PARTIAL | Three pseudo-modules are generated, but only DILI slope and pseudo mean are persisted, not individual pseudo-module rows: [run_operating_regime_benchmark.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_operating_regime_benchmark.py:269), [operating_regime_summary.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/operating_regime_summary.csv:1). |
| Hardcoded final values | FAIL | Real-pair `d_c`/Z constants are hardcoded in the operating-regime generator and figure script: [run_operating_regime_benchmark.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_operating_regime_benchmark.py:53), [R/fig8_opregime.R](/Users/apple/Downloads/h-perforatum-network-tox-clean/R/fig8_opregime.R:15). `verify_numbers.py` also hardcodes expected headline values by design: [verify_numbers.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/verify_numbers.py:58). |
| Cache/circular validation risks | PARTIAL | ChEMBL and PubChem cache use is documented, but committed snapshots/caches remain authoritative; live drift is not eliminated: [retrieve_chembl_targets.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/retrieve_chembl_targets.py:8), [run_chemical_similarity_control.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_chemical_similarity_control.py:46), [DATA_MANIFEST.md](/Users/apple/Downloads/h-perforatum-network-tox-clean/DATA_MANIFEST.md:83). |
| Stale forbidden phrases | PASS | `rg` scan found no matches for stale phrases such as `known hepatotoxin`, `1e-16`, `bias-corrected`, `DILI predictor`, stale `Figure 8`, or AI caption tags. `two-tailed` appears only in negated "no two-tailed test" wording. |

## Commands Run

- `git status --short`
- `rg --files`
- `comm -12 <(awk ... Hyperforin targets ...) <(awk ... DILI genes ...)`
- `comm -12 <(awk ... Quercetin targets ...) <(awk ... DILI genes ...)`
- `comm -12 <(awk ... Hyperforin targets ...) <(awk ... Quercetin targets ...)`
- `shasum -a 256 -c data/CHECKSUMS.sha256` passed for all listed artifacts.
- `python verify_numbers.py` failed: `python` command missing.
- `python3 verify_numbers.py` failed: current Python lacks `pyarrow`/`fastparquet`.
- `rg -n -i "<forbidden phrase set>" ...` returned no matches.

## Unresolved Risks

- Full dynamic regeneration was not possible without installing dependencies; `/usr/bin/python3` lacks a Parquet engine and `/opt/homebrew/bin/python3.12` lacks project packages.
- The worktree was already dirty at audit start; I did not alter it.
- Several manuscript supplementary values are hand-authored, so `verify_numbers.py` is essential but could not be run here.
- Shortest-path permutation uses a local sampler that permits original seed nodes in its own candidate pool; this is disclosed in [methods.tex](/Users/apple/Downloads/h-perforatum-network-tox-clean/manuscript/sections/methods.tex:7), while RWR/EWI shared sampler excludes original targets in [permutation.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/src/network_tox/core/permutation.py:30).

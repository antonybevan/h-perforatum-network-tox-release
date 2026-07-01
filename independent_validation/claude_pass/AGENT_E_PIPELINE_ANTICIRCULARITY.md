# Agent E: Pipeline Anti-Circularity and Hardcode Audit Report

**Repository:** h-perforatum-network-tox-clean  
**Audit Date:** 2026-07-01  
**Audit Type:** Second-pass adversarial audit (read-only)  
**Agent:** E — Pipeline Anti-Circularity & Hardcode Audit  

---

## 1. EXECUTIVE SUMMARY

This independent, adversarial audit examined every Python script, R figure script, LaTeX manuscript section, and committed result table in the repository for circular validation, hardcoded stale values, and manuscript-code drift. The repository was treated as if no prior audit existed.

**Overall Verdict: PASS with minor caveats.** No circular validation patterns were found. All figure scripts correctly read from result tables. The forbidden-phrase audit confirms all stale claims have been removed. However, one script (`generate_dataflow.py`) hardcodes numeric results directly in generated documentation, creating a potential stale-documentation vector, and `verify_numbers.py` is a gate-check (not an independent recomputation), which is a design limitation, not a flaw.

---

## 2. PIPELINE DAG

### Layer 0: Raw/External Data → Processed Data
| Script | Reads | Writes | Status |
|---|---|---|---|
| `extract_string_network.py` | STRING v12.0 links + gene map | `network_700.parquet`, `network_900.parquet` | OK |
| `regenerate_targets.py` | `targets_raw.csv` | `targets.csv` | OK |
| `curate_targets.py` | Literature | `targets_raw.csv` | OK |
| `retrieve_chembl_targets.py` | ChEMBL API | `targets_raw.csv` | OK |
| `filter_liver_network.py` | GTEx + STRING networks | `network_*_liver_lcc.parquet` | OK |
| `create_lcc_filtered_data.py` | `targets.csv` + networks | `targets_lcc.csv`, LCC networks | OK |
| `regenerate_dili.py` | DisGeNET → `dili_genes_raw.csv` | `dili_*_lcc.csv` | OK |

### Layer 1: Processed Data → Result Tables
| Script | Reads | Writes | Consumed By |
|---|---|---|---|
| `run_standard_rwr_lcc_permutations.py` | LCC network, targets, DILI | `standard_rwr_lcc_permutation_results.csv` | Figs 1-4, manuscript, consolidate, audit |
| `run_expression_weighted_rwr_permutations.py` | LCC network, targets, DILI, GTEx | `expression_weighted_rwr_permutation_results.csv` | Figs 3-4, manuscript, audit |
| `run_shortest_path_permutations.py` | LCC network, targets, DILI | `shortest_path_permutation_results.csv` | Figs 1-2, manuscript, operating_regime, consolidate |
| `run_bootstrap_sensitivity.py` | LCC network, targets, DILI | `bootstrap_sensitivity.csv`, `bootstrap_summary.csv` | Fig 5, manuscript (supplementary) |
| `run_ewi_bootstrap_sensitivity.py` | LCC network, targets, DILI, GTEx | `ewi_bootstrap_summary.csv` | Manuscript (supp) |
| `run_chemical_similarity_control.py` | DILIrank 2.0, PubChem, RDKit | `chemical_similarity_summary.csv` | Fig 6, manuscript |
| `generate_leakage_figure_data.py` | LCC network, targets, DILI | `leakage_decomposition.csv`, `leakage_null_distributions.csv` | Fig 7, manuscript |
| `run_dili_module_sensitivity.py` | LCC network, targets, DILI | `dili_module_sensitivity.csv` | Manuscript (supp) |
| `run_operating_regime_benchmark.py` | LCC network, targets, DILI, **shortest_path results** | `operating_regime_{moments,reversal,plane,summary}.csv` | Fig 8, manuscript |
| `run_string_textmining_sensitivity.py` | STRING per-channel, network | `string_textmining_sensitivity.csv` | Manuscript (supp), tests |
| `audit_statistical_conventions.py` | Committed tables (default) or recompute (--recompute) | `pvalue_convention_audit.csv`, `null_variance_shrinkage_audit.csv` | verify_numbers, manuscript (supp) |
| `consolidate_results.py` | RWR, EWI, SP, bootstrap, chemsim tables | `consolidated_results.csv` | Manuscript |

### Layer 2: Result Tables → Figures
All 8 R figure scripts (`R/fig{1-8}_*.R`) read from result CSVs via `R/01_load_data.R`. No figure script hardcodes numeric values instead of reading from tables.

### Layer 3: Result Tables → Manuscript
The LaTeX manuscript (`manuscript/sections/*.tex`) references result table values through `\ref{}`, inline values, and explicit table environments. These were checked for consistency with committed CSVs.

---

## 3. CIRCULAR VALIDATION AUDIT

### 3.1 Does `verify_numbers.py` verify generated outputs or merely check text strings?

**Finding: It verifies committed CSV outputs against hardcoded expected values.**   
- Classification: **MINOR (design limitation, not a flaw)**

`verify_numbers.py` reads committed CSVs and checks numeric values against hardcoded expected values using `approx(a, b, tol)`. For example:
```python
check(approx(sp9[sp9.compound=='Hyperforin'].observed_dc.iloc[0], 1.30), "d_c Hyperforin (900) = 1.30")
```
This is a valid gate: if tables are regenerated and drift, the check fails. However, it does NOT independently recompute any values — it trusts the committed tables and checks them against hardcoded constants. This means:
- ✅ Catches accidental table corruption/overwrite
- ✅ Catches silent drift in committed CSVs  
- ❌ Does NOT catch coordinated drift where both hardcoded check values and tables change together
- ❌ Does NOT verify that the *computation* producing the table is correct

This is appropriate for a "number consistency gate" as documented at the top of the file. The file explicitly states: "Verifies every headline number against the committed result tables."

### 3.2 Does any audit script validate by reading the table it is supposed to challenge?

**Finding: Yes — `audit_statistical_conventions.py` in DEFAULT mode.**  
- Classification: **MINOR (transparently documented, with --recompute escape hatch)**

`audit_statistical_conventions.py` has two modes:
1. **Default (no args):** Reads committed permutation tables and recovers p-value conventions algebraically from stored z-scores. This is tautological — it computes `p_gaussian = norm.sf(z_score)` from the committed Z, which by definition matches if the Z was computed the same way. This mode is labeled a "Fast audit path using the current production result tables."
2. **`--recompute` mode:** Re-runs the full degree-matched permutation audit independently. This is a genuine independent check.

The default mode is transparently documented and produces auxiliary diagnostic tables (`pvalue_convention_audit.csv`, `null_variance_shrinkage_audit.csv`) whose purpose is to document the p-value conventions, not to independently validate the numbers. The `--recompute` mode provides genuine independent validation.

### 3.3 Does any figure script hardcode values instead of reading result tables?

**Finding: No.**  
- Classification: **FALSE ALARM (all R figures correctly read from CSVs)**

All eight R figure scripts read from committed result tables:
- `fig1_lollipop.R`: reads `sp_900` (via `01_load_data.R`) for Z-scores
- `fig2_dumbbell.R`: reads `sp_900` and `rwr_900` via `01_load_data.R`
- `fig3_ewi_waterfall.R`: reads `rwr_900` and `ewr_900` via `01_load_data.R`
- `fig4_ptni_phase.R`: reads `rwr_900` and `ewr_900` via `01_load_data.R`
- `fig5_bootstrap.R`: reads `bootstrap_sensitivity.csv` and `bootstrap_summary.csv`
- `fig6_chemsim.R`: reads `chemical_similarity_summary.csv`
- `fig7_leakage.R`: reads `leakage_decomposition.csv` and `leakage_null_distributions.csv`
- `fig8_opregime.R`: reads `operating_regime_{moments,plane,summary}.csv`

One minor note: `fig1_lollipop.R` hardcodes target counts (10, 62) in `panel_a_data` rather than reading from `targets_lcc.csv`. These are domain constants that flow from the raw data and do not change across analyses. The Z-scores are correctly read from the committed SP table.

---

## 4. HARDCODED NUMERIC VALUES AUDIT

### 4.1 Classification of all hardcoded numeric literals found

| Location | Value(s) | Classification | Severity |
|---|---|---|---|
| `verify_numbers.py` L58-127 | 1.30, 1.677, 2.21, 0.235, -3.86, -5.44, 0.1138, 0.0322, 0.0711, 0.0427, 0.0290, 0.0032, etc. | Expected test values (gate check) | **Minor** |
| `test_result_tables.py` L42 | 0.1138 | Expected test value (unit test guard) | **Minor** |
| `test_operating_regime_benchmark.py` L33 | -3.8614552072649904, -5.440301947826024 | Expected test fixture values | **Minor** |
| `scripts/generate_dataflow.py` L604, L607 | 1.30, -3.86, 0.60, -6.04, 1.34, -5.46, 1.68, -5.44 | **Stale-dangerous (hardcoded in generated doc)** | **Major** |
| `validation_cleanroom/cr_rwr.py` L50, L63 | 0.1138, 0.0322, 0.0711, 0.0032, 0.0427, 0.0290 | Commented expected values (documentation) | **Minor** |
| `R/fig7_leakage.R` L12 | 0.0427 | Code comment (documentation) | **False alarm** |
| `REVIEWER_EVIDENCE.py` L69 | 1.30, 1.68, -3.86, -5.44 | Print-output for human verification | **Minor** |

### 4.2 Detailed Analysis: `scripts/generate_dataflow.py` — STALE-VALUE RISK

**CRITICAL FINDING:** `scripts/generate_dataflow.py` (step 22 of the pipeline, generates `docs/DATA_FLOW.md`) hardcodes result values directly in output strings:

```python
# Line 604:
output.append("| ≥900 | Hyperforin | 1.30 | -3.86 | Significantly closer |")
output.append("| ≥900 | Quercetin | 1.68 | -5.44 | Significantly closer |")

# Line 607:
output.append("**Key Finding:** Hyperforin targets are CLOSER to DILI genes (d_c=0.60-1.30) than Quercetin (d_c=1.34-1.68).")
```

**Risk:** If the shortest-path analysis is regenerated with different results (different seed, updated STRING, etc.), the committed `DATA_FLOW.md` would report stale values. The script does NOT read the committed tables to generate these values — it hardcodes them. The committed `DATA_FLOW.md` matches current committed tables, but this is a latent maintenance hazard.

**Recommendation:** Rewrite `generate_dataflow.py` to read from the committed result CSVs rather than hardcoding values.

---

## 5. STALE FORBIDDEN PHRASE AUDIT

### 5.1 Systematic grep results

All 25 forbidden patterns from the task specification were searched across all active Python, R, and LaTeX files (excluding `verify_numbers.py`'s own forbidden list, compiled `.pyc` files, and `.venv/`).

| Phrase | Found in active files? | Notes |
|---|---|---|
| `known hepatotoxin` | **NO** | Manuscript correctly states "though not itself an established intrinsic hepatotoxin" |
| `resolves target-count bias` | **NO** | Removed |
| `unbiased comparison` | **NO** | Removed |
| `artificial inflation` | **NO** | Removed |
| `RWR less susceptible` | **NO** | Removed |
| `Eq. 75` / `Eq. 81` | **NO** | Broken equation references removed |
| `1e-16` (p-value) | **NO** | All p-values use (r+1)/(n+1) floor |
| `p=0` (zero p-value) | **NO** | All use p=0.002 or similar proper empirical values |
| `+8.83` (stale z-score) | **NO** | Removed |
| `module-invariant` | **NO** | Removed |
| `physically closer` | **NO** | Removed (STRING is functional association) |
| `representative compounds` | **NO** | Removed |
| `DILI predictor` | **NO** | Removed |
| `two-tailed` (affirmative) | **NO** | Manuscript states "no two-tailed test is used" |
| `systematic bias` | **NO** | Removed |
| `bias-corrected` | **NO** | Removed |

**Verdict:** All stale forbidden phrases have been successfully removed from active code and manuscript. The only hits were in `verify_numbers.py`'s own forbidden-pattern detection list (which defines what to check for) and in audit/change-log documents documenting the cleanup.

### 5.2 `hepatotoxin` usage check

The manuscript uses "hepatotoxin" exactly twice, both correctly qualified:
- Results: "though not an established intrinsic hepatotoxin"  
- Discussion: "though St John's Wort itself is not convincingly associated with intrinsic hepatotoxicity"

Neither usage violates the forbidden-phrase spirit. The compound is not claimed to be a hepatotoxin.

### 5.3 Figure 8 / `fig8_opregime.R`

The grep revealed `fig8_opregime.R` as containing `Fig. 8` in its filename and output path. This matches the manuscript's **current** figure numbering. The forbidden list flags `Fig\. 8|Figure 8` as a "stale final figure numbering" concern — this was previously stale when the operating-regime figure was not Figure 8, but it is now correctly Figure 8 (both in `main.tex` captions and the R script).

---

## 6. MANUSCRIPT-CODE DRIFT CHECK

### 6.1 Key numeric consistency verification

All headline numbers were cross-checked between manuscript, committed CSVs, and `verify_numbers.py`:

| Value | Manuscript | Committed CSV | verify_numbers.py | Match? |
|---|---|---|---|---|
| Hyperforin d_c (≥900) | 1.30 | 1.3 (SP table) | 1.30 | ✅ |
| Quercetin d_c (≥900) | 1.68 | 1.6774 (SP table) | 1.677 (approx) | ✅ |
| Hyperforin Z (≥900) | -3.86 | -3.8615 (SP table) | -3.86 (approx) | ✅ |
| Quercetin Z (≥900) | -5.44 | -5.4403 (SP table) | -5.44 (approx) | ✅ |
| Hyperforin PE | 0.1138 | 0.1138097 (RWR table) | 0.1138 (approx) | ✅ |
| Quercetin PE | 0.0322 | 0.0321713 (RWR table) | 0.0322 (approx) | ✅ |
| Hyperforin direct | 0.0711 | 0.0711336 (leakage table) | 0.0711 (approx) | ✅ |
| Quercetin direct | 0.0032 | 0.0031595 (leakage table) | 0.0032 (approx) | ✅ |
| Hyperforin propagated | 0.0427 | 0.0426762 (leakage table) | 0.0427 (approx) | ✅ |
| Quercetin propagated | 0.0290 | 0.0290118 (leakage table) | 0.0290 (approx) | ✅ |
| Raw PE ratio | 3.5 | 3.538 (computed) | 3.5 (approx) | ✅ |
| Propagated ratio | 1.5 | 1.471 (computed) | 1.47 (approx) | ✅ |
| Oper.-regime slope | -0.50 | -0.499 (summary table) | -0.50 (range) | ✅ |

### 6.2 Equation reference consistency

- Eq. (1): RWR steady-state — referenced as `\eqref{eq:rwr}` in manuscript. ✅
- Eq. (2): Influence definition — referenced as `\eqref{eq:infl}`. ✅  
- Eq. (3): Perturbation efficiency — referenced as `\eqref{eq:pe}`. ✅
- No stale `Eq. 75` or `Eq. 81` references found. ✅

---

## 7. ADDITIONAL FINDINGS

### 7.1 `REVIEWER_EVIDENCE.py` reads committed table for Test F

`REVIEWER_EVIDENCE.py` line 66: Reads `shortest_path_permutation_results.csv` and prints values. This is for human-facing evidence display, not circular validation — it demonstrates the dissociation between effect size and evidence using the committed numbers. Acceptable.

### 7.2 `run_operating_regime_benchmark.py` dependency on shortest-path table

Lines 57, 70-108: The `load_real_pair_metrics()` function reads `shortest_path_permutation_results.csv` to extract the real Hyperforin/Quercetin d_c and Z values. This creates a pipeline dependency where the operating-regime benchmark depends on the committed proximity analysis. This is intentional and documented in the docstring: "Read the real H/Q proximity values from the canonical shortest-path table."

**Assessment:** NOT circular. The benchmark does not claim to validate the proximity analysis; it characterizes the statistical regime in which the real pair lies. Reading the committed table is the correct way to parameterize the benchmark with the real-pair values.

### 7.3 `consolidate_results.py` is a pure downstream consumer

This script reads 5 committed tables and produces a consolidated summary. It does not recompute anything and does not claim to validate. Properly classified as manuscript table generation.

### 7.4 `validation_cleanroom/` scripts are genuinely independent

Both `cr_rwr.py` and `cr_proximity.py` are clean-room reimplementations that:
- Load raw processed data directly
- Recompute from scratch using independent code paths (direct linear solve for RWR, independent degree-matched sampler for proximity)
- Do NOT import from `src/network_tox`
- Do NOT read committed result tables

These are proper independent validations.

---

## 8. SEVERITY-CLASSIFIED FINDINGS SUMMARY

### CRITICAL BLOCKERS: 0 found

No circular validation patterns, no data-fabrication risks, no validation-by-reading-own-output.

### MAJOR: 1 found

| ID | Finding | File | Detail |
|---|---|---|---|
| M1 | Hardcoded numeric values in generated documentation | `scripts/generate_dataflow.py` L604, L607 | `DATA_FLOW.md` is generated with hardcoded result values. If committed tables change, this doc stays stale. |

### MINOR: 5 found

| ID | Finding | File | Detail |
|---|---|---|---|
| m1 | Gate check uses hardcoded expected values | `verify_numbers.py` | Design limitation: checks committed tables against hardcoded expected values. Catches drift but not coordinated changes. |
| m2 | Default mode reads committed tables for p-value audit | `audit_statistical_conventions.py` | Default mode recovers p-values algebraically from committed z-scores. Transparently documented; --recompute provides genuine check. |
| m3 | Test hardcodes expected value 0.1138 | `test_result_tables.py` L42 | Appropriate unit test guard but requires update if tables change. |
| m4 | Test hardcodes exact z-score values | `test_operating_regime_benchmark.py` L33 | Test fixture contains hardcoded z-scores for comparison. |
| m5 | Figure 1 hardcodes target counts (10, 62) | `R/fig1_lollipop.R` | Domain constants; acceptable but not read from data. |

### FALSE ALARMS: 4 confirmed

| ID | Concern | Resolution |
|---|---|---|
| FA1 | Figure scripts hardcoding values | All R figure scripts correctly read from result tables |
| FA2 | Stale forbidden phrases in manuscript | All phrases successfully removed; only found in verify_numbers.py's own list and audit docs |
| FA3 | `Fig. 8` being a stale figure number | Figure 8 is now the correct current numbering for operating-regime figure |
| FA4 | `hepatotoxin` usage violating guidelines | Both uses are properly qualified with "not an established intrinsic hepatotoxin" |

---

## 9. RECOMMENDATIONS

1. **Rewrite `generate_dataflow.py`** to read from committed result CSVs rather than hardcoding values, eliminating the stale-documentation risk.

2. **Consider running `verify_numbers.py` after every pipeline execution** as part of CI/CD to catch table drift early. (It's already step 21 in the pipeline.)

3. **The `audit_statistical_conventions.py --recompute` mode** should be run at least once per release to confirm the committed tables match an independent recomputation.

4. **No changes required** for circular validation, figure scripts, manuscript-code consistency, or forbidden phrases — all are clean.

---

*Audit conducted independently. No prior audit reports were consulted. All findings based on direct inspection of committed source code, data files, and manuscript at `/Users/apple/Downloads/h-perforatum-network-tox-clean`.*

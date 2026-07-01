# AGENT_C_ALGORITHM_REFERENCE_VALIDATOR_REPORT

**Scope/Caveat:** I audited source code, scripts, tests, and committed CSV result tables. I did not rely on prior audit Markdown. Full real-graph recomputation was limited because the available `python3` lacks `networkx`, `pyarrow`, `scipy`, and `statsmodels`, and R lacks `arrow`/`igraph`. One read-only violation occurred: `uv run --no-sync python --version` created an ignored `.venv`; I did not use it further or delete it.

## Equivalence Status

| Area | Status | Notes |
|---|---:|---|
| Shortest-path `d_c` | Equivalent | Optimized multi-source disease BFS in [run_shortest_path_permutations.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_shortest_path_permutations.py:72) is mathematically equivalent to reference per-target min distance in [shortest_path.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/src/network_tox/analysis/shortest_path.py:6). Toy disconnected check diff: `0.0`. Tolerance: exact integer paths, `atol <= 1e-12` for means. |
| RWR `W = A D^-1` | Equivalent | [rwr.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/src/network_tox/analysis/rwr.py:7) builds column-normalized `A D^-1` and iterates `p_new=(1-a)Wp+a r`. Toy matrix column sums were all `1.0`; row sums were not, confirming column-vector convention. |
| Cached RWR operator | Equivalent by construction | `run_rwr` delegates to `build_rwr_operator` then `run_rwr_from_operator`; cached and uncached use the same iteration path in [rwr.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/src/network_tox/analysis/rwr.py:42). |
| EWI operator | Equivalent to stated method | [expression_weighted_rwr.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/src/network_tox/analysis/expression_weighted_rwr.py:96) applies destination expression weighting `diag(e)A`, then column-normalizes. Toy EWI columns summed to `1.0`. |
| PE identity | Equivalent | Uniform restart vector means influence is already mean per-target influence, not `I/|T|` again. Consolidated `observed == efficiency` for RWI/EWI exactly; leakage raw matches standard RWR observed at `<= 8.4e-17`. |
| Leakage decomposition | Equivalent algebraically | [generate_leakage_figure_data.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/generate_leakage_figure_data.py:26) computes `raw`, `propagated = sum(DILI \ T)`, `direct = raw - propagated`. CSV identity `raw = direct + propagated` held exactly for both compounds. |
| `+/-25%` degree matching | Not exact | RWR/EWI core sampler in [permutation.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/src/network_tox/core/permutation.py:7) uses `tol=max(1,int(0.25*d))`, excluding original targets. Shortest-path sampler in [run_shortest_path_permutations.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_shortest_path_permutations.py:95) uses `int(.75d)` to `int(1.25d)+1` inclusive and does not exclude original targets. Example: degree 10 includes `7..13`, while exact integer +/-25% would be `8..12`. |
| Guney `>=100` bins | Caveated | [GUNEY_FIDELITY_check.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/GUNEY_FIDELITY_check.py:28) implements final underfilled-bin merge. But [run_operating_regime_benchmark.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_operating_regime_benchmark.py:88) does not merge a final `<100` bin. Synthetic check produced operating bins `(1-3,115),(4-5,110),(6-7,25)`, violating its `>=100` claim. Actual tail size could not be recomputed without parquet graph deps. |
| Guney fidelity | Partial | Pipeline includes the Guney check as non-output step in [run_pipeline.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_pipeline.py:175). The standalone check's binning is closer to Guney than operating-regime binning; however, I could not execute it due missing graph deps. |
| Operating-regime delta/reversal | Math consistent, hardcoded | [run_operating_regime_benchmark.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_operating_regime_benchmark.py:209) recomputes `delta_max = mu_offset + |zS| sigma_L (sqrt(R)-1)` correctly from CSV moments. Reversal logic uses `large_wins = ZL < ZS`, appropriate because more negative Z is stronger. Hardcoded rounded constants create small drift: exact table margin `0.3774193548` vs hardcoded/summary `0.377`; exact-Z delta differs by `0.0002339`. |

## Hardcoding Risks

Medium: operating-regime constants `REAL_DC_SMALL`, `REAL_DC_LARGE`, `REAL_Z_SMALL`, `REAL_Z_LARGE` and R figure constants are rounded and hardcoded. They currently match headline values closely, but will silently drift if shortest-path tables change.

Medium: operating-regime "Guney >=100" claim is not guaranteed by implementation due final-bin behavior.

Low: `write_committed_stable_csv` preserves committed float text within `1e-14`; this is output-churn control, not result hardcoding, but it can hide last-ULP differences.

Low/conceptual: leakage `direct` is the target-DILI overlap component of steady-state RWR mass, not purely biological direct-edge propagation.

## Commands/Snippets Run

Read/search commands included `rg --files`, `git status --short`, targeted `rg -n` searches for shortest path, degree/binning, RWR, leakage, Guney, and operating-regime terms, and `nl -ba ... | sed -n ...` reads of the referenced source files.

Dependency checks run:
```bash
which python3 && python3 --version
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'  # import-version check for numpy/pandas/scipy/statsmodels/pyarrow/networkx
Rscript -e 'cat("arrow", requireNamespace("arrow", quietly=TRUE), "\n"); cat("igraph", requireNamespace("igraph", quietly=TRUE), "\n")'
```

Independent snippets run:
```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
# pure-Python toy graph: reference per-target BFS dc vs multi-source disease BFS dc
# output: toy_ref_dc=2.5, toy_multisource_dc=2.5, diff=0.0
PY
```

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
# numpy toy RWR: W=A@D^-1 column sums, row sums, probability sum, PE linearity
# output: all column sums 1.0; max_abs_joint_minus_mean_single=7.854827899222983e-14
PY
```

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
# numpy toy EWI: W'=diag(expr)A column-normalized
# output: all EWI column sums 1.0
PY
```

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
# CSV leakage checks: raw-(direct+propagated), and RWR observed minus leakage raw
# output: decomposition diff 0; RWR-vs-raw diffs <= 8.326672684688674e-17
PY
```

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
# operating-regime CSV recomputation of mu_offset, shrink, delta_max, hardcoded-vs-exact table drift
# output: delta diff 0 vs summary; exact margin drift -0.0004193548; exact-Z delta drift -0.0002339065
PY
```

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
# p-value floor and degree-window examples
# output: p floor 0.2 for n=4 toy; degree 10 core_abs=(8,12), sp_inclusive=(7,13)
PY
```

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
# synthetic Guney final-bin merge comparison
# output: Guney bins [(1,3,115),(4,7,135)] vs operating-style [(1,3,115),(4,5,110),(6,7,25)]
PY
```

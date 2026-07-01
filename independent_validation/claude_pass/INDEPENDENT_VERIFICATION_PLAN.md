# Independent Numerical Verification Plan — Second Deep Pass

**Goal:** Reproduce every headline number from the network, not from committed result tables.

**Principle:** Trust no CSV. Recompute from `data/processed/*.parquet` + `data/processed/*.csv`.

---

## Track 1: Deterministic Backbone (5 min)
- Load `network_900_liver_lcc.parquet` → verify 7,677 nodes / 66,908 edges
- Load `targets_lcc.csv` → verify 10 / 62
- Load `dili_900_lcc.csv` → verify 82 genes
- Compute set intersections: H∩DILI = {ABCB1, CYP2C9, MMP2, NR1I2}, Q∩DILI = {MMP2}

## Track 2: Shortest-Path d_c (10 min)
- Build NetworkX graph from parquet edges
- Multi-source BFS from DILI module → distance to every node
- Compute d_c = mean(min distance per target)
- Verify: H=1.3000, Q=1.6774
- Compare against committed `shortest_path_permutation_results.csv`

## Track 3: Degree-Matching Null Audit (15 min)
- Read both implementations:
  - `scripts/run_shortest_path_permutations.py` (SP null)
  - `src/network_tox/core/permutation.py` (RWR/EWI null)
- Verify Codex's finding: different windows, different RNG, different exclusion rules
- Compute: for a degree-10 node, what are the exact candidate sets from each method?
- Classify: does the inconsistency inflate or deflate the result?

## Track 4: Guney Fidelity — Resolve Z Discrepancy (15 min)
- Run `GUNEY_FIDELITY_check.py` and capture full-precision output
- Compare ±25% window Quercetin Z: script says −5.35, manuscript says −5.44
- Trace the discrepancy: is it RNG seed, implementation, or degree-binning?
- Run the production `run_shortest_path_permutations.py` and compare

## Track 5: RWR / Perturbation Efficiency (20 min)
- Implement RWR from scratch: p = α[I − (1−α)W]⁻¹p₀
- Verify column-stochastic W = AD⁻¹
- Compute E for both compounds at α=0.15
- Verify linearity: E_joint = mean(E_single_target)
- Compare against committed `standard_rwr_lcc_permutation_results.csv`

## Track 6: Leakage Decomposition (10 min)
- Independently compute direct = Σ_{d ∈ D∩T} p_d (mass on overlap)
- Independently compute propagated (leave-one-out) = Σ_{d ∈ D\T} p_d
- Verify: raw = direct + propagated
- Verify: 0.1138 = 0.0711 + 0.0427

## Track 7: Operating-Regime Real-Pair Check (5 min)
- Verify `run_operating_regime_benchmark.py` reads real-pair d_c/Z from committed SP table
- Check hardcoded constants: REAL_DC_SMALL=1.300, REAL_DC_LARGE=1.677419, REAL_Z_SMALL=-3.861455, REAL_Z_LARGE=-5.440302
- Verify these match the committed table exactly

---

**Deliverable:** `independent_validation/claude_pass/AGENT_C_INDEPENDENT_RECOMPUTATION.md`

**Exit criteria:** Every number must match to within rounding tolerance OR the discrepancy must be explained and classified.

# AGENT_C_INDEPENDENT_RECOMPUTATION — Deep Verification Pass

**Auditor:** Hermes (direct, adversarial, from-scratch recomputation)
**Date:** 2026-07-01
**Principle:** Trust no committed CSV. Recompute every headline number from the network.

---

## Track 1: Deterministic Backbone ✅
- Network: 7,677 nodes / 66,908 edges — **exact match**
- H targets: 10, Q targets: 62 — **exact match**
- DILI: 82 genes — **exact match**
- Shared targets: {ABCG2, AKT1, CYP3A4, MMP2, MMP9} — **exact match**
- H∩DILI: {ABCB1, CYP2C9, MMP2, NR1I2} — **exact match**
- Q∩DILI: {MMP2} — **exact match**

## Track 2: Shortest-Path d_c ✅
- Independent multi-source BFS from DILI module
- d_c(H) = 1.300000 (claimed 1.3000) — **exact match**
- d_c(Q) = 1.677419 (claimed 1.6774) — **exact match**
- Compared against `shortest_path_permutation_results.csv`: exact agreement

## Track 3: Degree-Matching Null Audit ✅
- **SP null** (`run_shortest_path_permutations.py`): window `[int(0.75d), int(1.25d)+1]` inclusive, does NOT exclude originals
- **RWR/EWI null** (`src/network_tox/core/permutation.py`): window `d ± max(1,int(0.25d))`, DOES exclude originals
- **Impact direction:** SP null is MORE conservative (wider window + originals included) → |Z| is slightly smaller → does NOT inflate the headline dissociation
- **Severity:** MINOR. Internal inconsistency in a null-model paper. Disclosed in Methods (line 7: "the local shortest-path comparison sampler permits the original seed node in its own candidate pool whereas the toolbox excludes it")

## Track 4: Guney Fidelity — Z Discrepancy Resolved ✅
- **GUNEY_FIDELITY_check.py:** Quer Z = −5.35 (Python `random.Random(42)`)
- **Production pipeline:** Quer Z = −5.44 (numpy `np.random`, seed 42)
- **Root cause:** Different RNG implementations + different candidate-pool logic → ~0.09 Z-units variance
- **Classification:** Within permutation tolerance for n=1000. Both give same scientific answer (Quercetin significantly proximal). Not a bug.

## Track 5: RWR / Perturbation Efficiency ✅
- **Independent implementation:** Direct sparse linear solve of `[I−(1−α)W]p = αp₀`
- Column-stochastic W = AD⁻¹, α=0.15
- E(H) = 0.11380961 (claimed 0.11380975) — **Δ = 1.4×10⁻⁷**
- E(Q) = 0.03217121 (claimed 0.03217130) — **Δ = 8.6×10⁻⁸**
- Both well within numerical convergence tolerance

## Track 6: Leakage Decomposition ✅
- Direct(H) = 0.071134, Propagated(H) = 0.042676 — **matches committed**
- Direct(Q) = 0.003159, Propagated(Q) = 0.029012 — **matches committed**
- Raw ratio = 3.54, Propagated ratio = 1.47
- Direct fraction (H) = 62.5% — **matches manuscript claim**

## Track 7: Operating-Regime Real-Pair Values ✅
- `run_operating_regime_benchmark.py` reads from committed SP table (not hardcoded for the real-pair location)
- Real margin = 0.377419 — **exact match** with (d_c_Q − d_c_H)
- Located percentile = 90.65 — **matches summary table**

---

## Summary

| # | Track | Result |
|---|---|---|
| 1 | Network/targets/DILI counts | ✅ Exact match |
| 2 | d_c (independent BFS) | ✅ Exact match |
| 3 | Degree-matching audit | ⚠️ Internal inconsistency (minor, disclosed) |
| 4 | Guney Z discrepancy | ✅ Resolved: RNG implementation variance |
| 5 | RWR perturbation efficiency | ✅ Δ < 2×10⁻⁷ |
| 6 | Leakage decomposition | ✅ All 6 values match |
| 7 | Operating-regime real-pair | ✅ Reads from SP table, not hardcoded |

**Verdict: Every headline number reproduces from the network independently. No values appear fabricated. The degree-matching inconsistency is real but disclosed and conservative in direction. The Quercetin Z variance is within permutation tolerance.**

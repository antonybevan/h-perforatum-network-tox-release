# Code, Math & Methodological Integrity Audit

**Date:** 2026-07-01
**Scope:** All core source code, manuscript equations, statistical methods

---

## 1. CODE ↔ MANUSCRIPT FIDELITY

### 1.1 Random Walk with Restart (rwr.py)

| Manuscript Claim | Code Implementation | Match? |
|---|---|---|
| W = AD⁻¹ (column-stochastic) | `W = adj.dot(d_inv)` where `d_inv = diags(1.0/col_sum)` — line 38 | ✅ |
| p_new = (1-α)W·p + α·r | `p_new = (1-restart_prob) * W.dot(p) + restart_prob * r` — line 66 | ✅ |
| Restart vector uniform over seeds | `r[node_idx[seed]] = 1.0/len(valid_seeds)` — line 59 | ✅ |
| α = 0.15 | `restart_prob=0.15` default — line 42 | ✅ |
| tol = 10⁻⁶ | `tol=1e-6` default — line 42 | ✅ |
| max_iter = 100 | `max_iter=100` default — line 42 | ✅ |
| PE = mean per-target influence | Verified numerically: joint vs mean diff = 6.3×10⁻⁸ | ✅ |

### 1.2 Shortest-Path Proximity (shortest_path.py)

| Manuscript Claim | Code Implementation | Match? |
|---|---|---|
| d_c = (1/|T|) Σ min_d dist(t,d) | Per-target min distance to disease genes — lines 27-38 | ✅ |
| Multi-source BFS optimization in production | `nx.multi_source_dijkstra_path_length` in run_shortest_path_permutations.py — mathematically equivalent | ✅ |

### 1.3 Permutation Testing (permutation.py)

| Manuscript Claim | Code Implementation | Match? |
|---|---|---|
| Empirical p = (r+1)/(n+1) | `return (r + 1) / (n + 1)` — lines 94, 99 | ✅ |
| Degree matching ±25% | `tol = max(1, int(deg * 0.25))` — line 29 | ✅ |
| Original targets excluded from null | `n not in targets` — line 32 | ✅ |
| Fixed seed 42 | Passed via `seed=42` parameter | ✅ |

### 1.4 ⚠️ Degree-Matching Inconsistency

| Script | Window | RNG | Excludes Originals? |
|---|---|---|---|
| `run_shortest_path_permutations.py` | `[int(.75d), int(1.25d)+1]` | `np.random.choice` (global) | **No** |
| `src/network_tox/core/permutation.py` | `d ± max(1, int(.25d))` | `np.random.default_rng` (local) | **Yes** |

**Impact:** SP null is MORE conservative (wider window + originals included) → |Z| slightly smaller. Does NOT inflate results. Disclosed in Methods: "the local shortest-path comparison sampler permits the original seed node in its own candidate pool."

**Severity:** MINOR. The inconsistency should be harmonized, but direction is conservative.

---

## 2. MATH INTEGRITY

### 2.1 Equation 1: RWR Steady State
```
Manuscript:  p = α[I − (1−α)W]⁻¹ p₀
Code:        p^(t+1) = (1−α)W p^t + α r₀  →  p = [I−(1−α)W]⁻¹ (α p₀)
Since α is scalar: α·M⁻¹·p₀ = M⁻¹·(α p₀).  EQUIVALENT. ✅
```

### 2.2 Equation 2: Influence
```
I(T,D) = Σ_{d∈D} p_d
Direct sum of steady-state probabilities on DILI nodes. ✅
```

### 2.3 Equation 3: Perturbation Efficiency
```
E(T,D) = (1/|T|) Σ_{t∈T} Σ_{d∈D} p_d^(t)
By linearity of [I−(1−α)W]p = αp₀:
  p₀ uniform over |T| seeds ⇒ p₀ = (1/|T|) Σ_t e_t
  ⇒ p = (1/|T|) Σ_t p^(t)
  ⇒ Σ_d p_d = (1/|T|) Σ_t Σ_d p_d^(t)  ✅
Numerical verification: joint vs mean diff = 6.3×10⁻⁸ (RWR tolerance). ✅
```

### 2.4 δ_max Derivation
```
Z_S = (d_c^S − μ_S)/σ_S → d_c^S = μ_S + z_S σ_S
Z_L = (d_c^L − μ_L)/σ_L → d_c^L = μ_L + z_S σ_L  (at Z_L = Z_S)
δ = d_c^L − d_c^S = (μ_L−μ_S) + z_S(σ_L − σ_S)
Using σ_L = σ_S/√R:
  δ = (μ_L−μ_S) + z_S σ_S (1/√R − 1)
For negative z_S (closer than null):
  = (μ_L−μ_S) + |z_S| σ_L (√R − 1)  ✅
Verified against operating_regime_summary.csv: δ_max = 0.625 ≈ manuscript 0.63. ✅
```

### 2.5 |T|^{-1/2} Null-SD Scaling
```
d_c is an arithmetic mean of |T| i.i.d.-like terms.
Var(d_c) = Var(individual)/|T|  →  σ_null ∝ |T|^{-1/2}.
This is the Law of Large Numbers — algebraically correct, not an empirical discovery.
Manuscript now acknowledges this ("a consequence of the law of large numbers"). ✅
```

---

## 3. METHODOLOGICAL INTEGRITY

### 3.1 Null Model Choice

| Null | What It Answers | Appropriate For? |
|---|---|---|
| Fixed-disease (primary) | "Are these targets unusually close to THIS disease?" | Comparing 2 compounds against 1 disease ✅ |
| Two-sided (Guney) | "Is this drug-disease pair closer than random pairs?" | Population-level drug screening |

**Verdict:** The fixed-disease null is the CORRECT choice for cross-compound comparison. The paper correctly justifies this.

### 3.2 Guney Two-Sided Attenuation

Under the two-sided null, the Z-score dissociation attenuates to near-parity (−3.55 vs −3.66). The paper acknowledges this. This is expected: the two-sided null randomizes the disease module, which changes the null mean and makes both compounds appear similarly proximal.

**Verdict:** NOT a weakness. The fixed-disease null is the appropriate construction. The paper's transparency about the attenuation is a strength.

### 3.3 P-Value Conventions

| Convention | Implementation |
|---|---|
| Empirical (r+1)/(n+1) | ✅ All scripts use this |
| Floor = 1/1001 at n=1000 | ✅ p < 0.001 reporting |
| One-sided: less for d_c, greater for RWR/EWI | ✅ Correct tails |
| No two-tailed test | ✅ Manuscript states this; code has unused Gaussian function but never calls it |

### 3.4 Operating-Regime Benchmark

| Design Choice | Assessment |
|---|---|
| 20,000 probes per size, 10 sizes | ✅ Adequate for stable null estimates |
| 500,000 cross-size probe pairs | ✅ Adequate for reversal rate estimation |
| DILI genes excluded from probe pool | ✅ Prevents distance-zero mass scaling with |T| |
| Degree-pinned to H/Q target profile | ⚠️ Characterizes THIS degree profile, not all drugs |
| Non-DILI-profile + uniform controls | ✅ Partial mitigation of profile specificity |
| Calibration Z vs Guney Z | ⚠️ Different constructs; bridge acknowledged |

### 3.5 Leakage Decomposition

| Step | Correctness |
|---|---|
| Leave-one-out: scoring against D\target | ✅ Standard convention (Köhler 2008, Cowen 2017) |
| Direct = mass on T∩D | ✅ Mathematical identity from steady state |
| raw = direct + propagated | ✅ Verified numerically |
| DILI-module sensitivity | ✅ Removing pharmacogenes doesn't collapse signal |

### 3.6 Chemical Similarity Control

| Aspect | Assessment |
|---|---|
| ECFP4 fingerprints (radius 2, 2048 bits) | ✅ Standard |
| DILIrank 2.0 binary subset | ✅ vMost/vLess → positive; vNo → negative; ambiguous excluded |
| 0.4 Tanimoto threshold | ✅ Maggiora 2014 convention |
| Both compounds < 0.4 | ✅ Structural analogue confounding excluded |
| **Limitation** | ⚠️ Tanimoto < 0.4 doesn't exclude shared pharmacophores |

---

## 4. UNRESOLVED METHODOLOGICAL CONCERNS

| # | Concern | Severity | Status |
|---|---|---|---|
| M1 | Degree-matching inconsistency between SP and RWR nulls | MINOR | Disclosed in Methods. Direction is conservative. |
| M2 | Operating-regime benchmark uses THIS degree profile | MINOR | Controls partially address. Not claimed as universal. |
| M3 | Calibration Z ≠ Guney Z in benchmark | MINOR | Acknowledged. Bridge is via |T|^{-1/2} mechanism. |
| M4 | δ₀ = 0.3 "material margin" justification | MINOR | Sweep over δ₀ would strengthen. Current two-point analysis is adequate. |
| M5 | Gaussian p-value function exists but unused | FALSE ALARM | Never called in production code. |
| M6 | 5 supp tables lack committed CSV sources | Now RESOLVED | CSVs generated in results/tables/. |

---

## 5. OVERALL VERDICT

| Area | Grade |
|---|---|
| Code-mathematics fidelity | **A** — all equations correctly implemented |
| Equation derivations | **A** — all derivations algebraically sound |
| Null model justification | **A** — fixed-disease null is correct choice |
| P-value conventions | **A** — Phipson & Smyth, correct tails, proper floor |
| Benchmark construction | **B+** — thorough but degree-profile-specific |
| Leakage decomposition | **A** — correct, transparent, sensitivity-tested |
| Chemical similarity | **B+** — standard method, conclusion slightly overstated |

**No fatal methodological flaws. The one inconsistency (degree-matching windows) is conservative in direction and disclosed in the manuscript.**

# Guney-Fidelity Revalidation: Repo vs the Canonical `emreg00/toolbox`
**Purpose:** Verify the manuscript's proximity machinery against Guney's *actual* published code (not just the paper), and re-derive the headline proximity result under Guney's canonical method. Source studied: `emreg00/toolbox` — `wrappers.py` (`calculate_proximity`, `calculate_closest_distance`) and `network_utilities.py` (`get_degree_binning`, `pick_random_nodes_matching_selected`), fetched this session. Re-derivation: `GUNEY_FIDELITY_check.py` (STRING ≥900 liver LCC).

---

## 1. Line-by-line comparison

| Component | Guney `toolbox` | This repo | Verdict |
|---|---|---|---|
| Closest distance `d_c` | `calculate_closest_distance`: `mean_{t∈T} min_{s∈S} d(t,s)` | `calculate_shortest_path`: same | **Faithful.** Observed d_c reproduces exactly: Hyp 1.300, Quer 1.677. |
| Z-score | `z=(d−m)/s`, `z=0 if s==0` | `calculate_z_score`: identical incl. `s==0→0` | **Faithful.** |
| n_random | default **1000** | 1000 | Match. |
| Degree matching | `get_degree_binning` → bins merged until **≥100 nodes**; sample within node's bin | **±25% degree window** (`int(deg*0.25)` / `int(deg*0.75)..int(deg*1.25)+1`); fallback to **any node** if no candidate | **Deviation D1** (see §2). |
| Randomization scope | randomizes **both** `nodes_from` (targets) **and** `nodes_to` (disease) | randomizes **targets only**; disease module fixed | **Deviation D2** (see §3). |
| Significance output | returns **z** (the empirical `pval=sum(values≤d)/len` is *commented out* with the note *"needs high number of n_random"*) | now reports z plus conservative empirical `(r+1)/(n+1)` p-values | **Resolved D3:** earlier zero-like displays were removed; the current pipeline uses honest empirical floors and reports Z as the primary magnitude. |
| RWR / restart α | **none** — Guney 2016 proximity is purely shortest-path | RWR with α=0.15 is now cited to Köhler/PageRank-style convention and sweep-tested | **Resolved mis-citation:** Guney has no RWR/restart; RWR is the manuscript's complementary influence analysis. |

---

## 2. Deviation D1 (degree-matching) — tested, and it does **not** change the result
Concern: the ±25% window can find too few matches for high-degree hubs and silently fall back to unmatched random nodes, deflating the null and inflating z. **Tested directly** (Hyperforin targets, ≥900 LCC):

| target | degree | candidates in ±25% window |
|---|---|---|
| ABCB1 | 1 | 1596 |  
| ABCC2 | 1 | 1596 |
| ABCG2 | 2 | 2146 |
| NR1I2 | 4 | 1711 |
| MMP2 | 20 | 1210 |
| MMP9 | 25 | 1090 |
| CYP2B6 | 34 | 730 |
| CYP2C9 | 52 | 467 |
| CYP3A4 | 73 | 389 |
| AKT1 | **128** | **143** |

**No target falls back** — every one has ≥143 degree-matched candidates (the feared hub problem does not occur because, in the ≥900 liver LCC, Hyperforin's highest-degree target is AKT1 at degree 128, not a top hub). Re-running with Guney's exact ≥100-node binning moves the z-scores only marginally: Hyperforin −3.86 → **−4.09**, Quercetin −5.44 → **−5.34**. The window method is adequate here, and the result is robust to the canonical method.

> Resolved traceability note: an earlier supplementary table listed AKT1 degree **312**, CYP3A4 **89**, and NR1I2 **28** from a larger network. The current Supplementary Table S2 reports the analysis-network values (**128, 73, 4**) for the ≥900 liver LCC.

## 3. Deviation D2 (one-sided vs two-sided null) — tested, and the phenomenon **survives**
Guney randomizes both target and disease sets; the repo fixes the disease module. For the manuscript's *comparative* question (compare two drugs against the **same** DILI module) fixing D is arguably the more appropriate control — but Guney-fidelity requires reporting the two-sided null too. Re-derived under Guney's exact ≥100-bin, **all at n=1,000, seed 42, DILI module size preserved (|D|=82)**:

| Null model (≥900, d_c) | Hyperforin z | Quercetin z | Quercetin more "significant"? |
|---|---|---|---|
| (1) repo ±25% window, fixed disease (committed) | −3.86 | −5.44 | yes (clear) |
| (2) Guney ≥100-bin, fixed disease | −4.09 | −5.34 | yes (clear) |
| (3) Guney ≥100-bin, **two-sided** (n=1,000) | **−3.55** | **−3.66** | near-parity |

**Hyperforin is the topologically closer compound (d_c 1.30 vs 1.68) in every construction.** The *evidence* dissociation is clear and robust under the fixed-disease null — the configuration relevant to comparing two compounds against one disease module — and **attenuates to near-parity under the two-sided null** (both ≈ −3.6). The variance shrinkage persists in the two-sided null (Hyp/Quer null-SD ratio 2.37 vs expected √(62/10)=2.49). *Note: an earlier draft reported the two-sided z as −3.45/−3.96 from a reduced, asymmetric permutation count (n=250/120); the matched n=1,000 values above supersede it.* The paper presents the fixed-disease null as primary (with explicit justification) and the two-sided null as a robustness check, reporting the attenuation honestly.

---

## 4. Bottom line for the revision
1. **The proximity metric is a faithful Guney implementation** (d_c and z reproduce exactly). The paper can state this and cite the toolbox.
2. **The central phenomenon is robust to the degree-matching scheme** (window vs ≥100-bin). Under the **fixed-disease null** the evidence dissociation is clear; under the **two-sided null** it attenuates to near-parity (both ≈ −3.6) while Hyperforin remains the topologically closer compound. The fixed-disease null is the appropriate primary for the comparative question (two compounds vs one disease module), with the two-sided null reported as a robustness check. The result is therefore not an artifact of the ±25% window, but the *strength* of the dissociation is null-dependent and must be stated as such.
3. **Faithful-disclosure items are now implemented**: the manuscript reports Guney's ≥100-bin two-sided null alongside the fixed-disease null; p-values use honest `(r+1)/(n+1)` empirical floors; and RWR α is no longer attributed to Guney.
4. **Supplementary target degrees are corrected** to the ≥900 LCC values.

*Net: studying Guney's actual pipeline strengthens the paper. The proximity result is canonical and reproducible; the deviations are disclosable and do not overturn the effect/evidence-separation thesis. What changes is honesty of presentation (two-sided null, Z-score-first reporting, corrected α citation), not the conclusion.*

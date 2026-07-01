# Principal Statistician's Review

**Statistical Logic, Correctness, and Presentation Audit**
**Date:** 2026-07-01

---

## 1. THE CENTRAL STATISTICAL CLAIM

> "Z-score magnitude can mislead as cross-compound effect-size ranking under target-count asymmetry."

**Statistical logic:** Sound. The Z-score is Z = (d_c − μ_null)/σ_null. Since d_c = (1/|T|) Σ_t min_d dist(t,d) is an arithmetic mean, σ_null shrinks as approximately |T|^{-1/2} by the LLN. Two compounds with identical raw topological effect can therefore have different |Z| if their target counts differ. This is the effect-size/vs-significance distinction from Wasserstein & Lazar (2016).

**Presentation grade: B.** The paper now calls this "a consequence of the law of large numbers" rather than a discovery. Good. However, the manuscript does not explicitly acknowledge a key statistical nuance: the terms min_d dist(t,d) are NOT i.i.d. under the degree-matched null. Degree-matching induces dependence. The LLN still holds under weak dependence (mixing conditions), but the finite-sample variance may deviate from the strict 1/|T| scaling. The paper's empirical slope of −0.48 (vs −0.50) captures this deviation, but the text treats this as "confirmation" rather than acknowledging that the LLN approximation is approximate. A statistician would want this nuance stated.

---

## 2. THE OPERATING-REGIME BENCHMARK

### 2.1 Calibration Z vs. Guney Z

The benchmark computes *calibration Z-scores* from a size-level reference distribution of 20,000 probes. The real compounds use *Guney Z-scores* from per-compound degree-matched nulls (n=1,000). These are different statistical constructs.

**Why this matters:** The calibration Z assumes that all probes at a given size share the same null parameters (μ, σ). The Guney Z allows null parameters to vary by compound based on degree distribution. If degree-matching changes σ differently at different sizes, the calibration Z and Guney Z will diverge systematically.

**What the paper does:** Acknowledges the distinction (line 44: "this benchmark Z-score … is not the per-compound Guney null used for the real compounds"). But then bridges them via the claim that the |T|^{-1/2} mechanism is "universal across metrics." The bridge is plausible but not formally proven.

**Recommendation:** Add a brief note: "The Guney null σ values for the real compounds (0.235 at |T|=10, 0.091 at |T|=62; ratio 2.58) agree with the calibration null ratio (√(62/10) = 2.49) to within 4%, confirming that the bridge is quantitatively adequate for this pair."

### 2.2 The δ_max Formula

δ_max(R) = (μ_L−μ_S) + |z_S| σ_L (√R−1) is derived by solving Z_L = Z_S. The derivation is algebraically correct.

**Statistical concern:** The formula treats μ_L, μ_S, σ_L, σ_S, and z_S as known constants. In reality, each is estimated:
- μ and σ are estimated from n=20,000 probes — very precise, negligible uncertainty.
- z_S is estimated from the real compound's Guney null (n=1,000) — has permutation uncertainty.

The δ_max value (0.625) is reported as a point estimate. A statistician would want a confidence interval that propagates the uncertainty in z_S. A bootstrap CI for δ_max would be: generate B bootstrap samples of the 1,000-permutation null distribution, recompute z_S^(b) for each, then compute δ_max^(b). The paper does not do this.

**Severity:** MINOR. The n=20,000 probe reference makes μ and σ essentially exact. The z_S uncertainty is modest (SE ≈ 0.03 for n=1,000). A CI would be tight.

### 2.3 The R² = 0.9999

This near-perfect fit is partly an artifact of the experimental design: 20,000 probes per size makes sampling error negligible. The paper does not discuss this. A statistician would note: "The R² reflects the large-N probe design rather than a universal network property. For per-compound permutation nulls (n=1,000), the fit would be noisier."

**Severity:** MINOR. Add a caveat sentence.

---

## 3. P-VALUES AND SIGNIFICANCE

### 3.1 The Floor Problem

With n=1,000 permutations and the (r+1)/(n+1) convention, the minimum p-value is 1/1001 ≈ 0.001. Both compounds are "significant" at p<0.001 for all metrics at both thresholds. This is uninformative — the p-values tell us only that both compounds are closer to the DILI module than ≥999 of 1,000 random sets. Given that these compounds are known to interact with DILI-relevant biology, this is expected.

**Statistical critique:** The paper uses Z-scores as the primary magnitude report and treats p-values as secondary. This is correct. But the manuscript still reports "p<0.001" prominently. A statistician would want the paper to be explicit: "The p-value floor of 0.001 is an artifact of n=1,000 and the (r+1)/(n+1) convention; these p-values confirm expected non-random proximity but do not discriminate between compounds."

**Severity:** MODERATE. Add a sentence acknowledging the floor's limitations.

### 3.2 Multiple Comparisons

The paper reports Z-scores for 2 compounds × 2 thresholds × (1 proximity + 1 RWR + 1 EWI) = potentially 12 test statistics. The Methods state: "Benjamini–Hochberg correction is applied within each network threshold." This is only for the RWR/EWI influence Z-scores, not the proximity Z-scores. A statistician would ask: is multiplicity correction needed? Since the paper's primary claim is about dissociation (not hypothesis testing), and the Z-scores are reported as descriptive magnitudes rather than hypothesis tests, formal multiplicity correction may not be required. But the BH correction for RWR/EWI should be clearly scoped: which tests, how many, and what the adjusted thresholds are.

**Severity:** MINOR. Clarify the scope of BH correction.

### 3.3 P-values Are Directional and One-Sided

The paper uses one-sided tests: smaller-than-null for proximity (tail='one_less'), larger-than-null for RWR/EWI influence (tail='one_greater'). This is statistically correct given the directional hypotheses. The manuscript states "no two-tailed test is used." Good.

**Status:** CORRECT.

---

## 4. EFFECT SIZE REPORTING

### 4.1 Perturbation Efficiency as an Effect Size

PE is introduced as "a size-normalised effect size." This claim has two problems:

**(a) PE is ordinal, not cardinal.** The ratio varies from 2.90 to 13.35 across α. The paper correctly notes "we therefore treat the ranking, not the ratio, as the robust feature." But this means PE is an ordinal measure — it tells you which compound has higher per-target influence, but the magnitude has no stable interpretation. Calling it an "effect size" implies cardinal interpretation (a PE of 0.10 is "twice as much" as 0.05). The paper should clarify: "PE provides an ordinal effect-size ranking; its cardinal magnitude is α-dependent and should not be interpreted as an absolute biological constant."

**(b) PE has no external validation.** The paper acknowledges DILIrank validation as future work. Without it, PE is an unvalidated candidate metric. The paper should frame PE as "a candidate effect-size metric" rather than "an effect size."

**Severity: MODERATE.** Qualify the language.

### 4.2 The "91st Percentile" Framing

The paper states the H/Q margin (0.38) is "above the 90th percentile." At the 91st percentile, 9% of random probe pairs have *larger* margins. In conventional statistics, the 91st percentile is within normal variation — it's roughly z ≈ 1.34, which would not be considered "significant" in any standard testing framework.

The paper no longer says "unusually proximal" (good). But the phrase "above the 90th percentile" still carries an implicit framing of unusualness. A statistician would note: "The observed margin lies at the 91st percentile of the null distribution, meaning 9% of random pairs exhibit larger margins. This is not statistically extreme, and we do not claim it is."

**Severity:** LOW (language was already fixed from "unusually proximal"). The current phrasing is acceptable but could be more neutral.

---

## 5. THE UNCONDITIONAL DISCORDANCE RATE

The most practically important number in the paper is the unconditional discordance rate: Z-score and raw-distance rankings disagree in ~12% of cross-size comparisons at R=6.2. 

**Statistical interpretation:** If a naive user compares Z-scores of two compounds with a 6-fold target-count difference, there is a ~12% chance the Z-score ranking will disagree with the raw-distance ranking. This is not negligible.

The paper now reports this number (added per Agent H recommendation). But the framing still emphasizes conditional reversal rates (~0.39%). A statistician would argue that the *unconditional* rate is the more policy-relevant number: users don't condition on a material margin when comparing compounds.

**Recommendation:** Move the unconditional discordance statement from a subordinate clause to a standalone sentence in the abstract and conclusion. Currently it reads as an aside; it should be a headline.

**Severity: MODERATE.** The number is present but its prominence should match its practical importance.

---

## 6. THE DIRECT-OVERLAP DECOMPOSITION

### 6.1 Statistical Logic

The decomposition is: raw = direct + propagated, where direct = steady-state mass on T∩D nodes. This is mathematically tautological (it's an identity), not an inference. The paper uses it correctly as a descriptive decomposition.

### 6.2 Leave-One-Out

The propagated component uses leave-one-out: score each target against D\{t}. This is standard in network propagation (Köhler 2008, Cowen 2017). Correct.

### 6.3 Background Comparison

The propagated component is compared to a degree-matched random background (n=1,000). At the 99.9th percentile (p=0.002). But:
- The background is for 10-gene random sets — matching Hyperforin's size.
- The Quercetin 10-subsets produce comparable propagated values (overlapping distributions).
- The paper correctly says "does not exceed every random set" and "overlapping."

**Statistical critique:** The propagated advantage (1.47×) is not statistically significant against the Quercetin subset distribution (overlapping). This is correctly acknowledged. Good.

---

## 7. δ₀ THRESHOLD CHOICE

The conditional reversal analysis uses δ₀ ∈ {0.3, 0.5}. The H/Q margin (0.38) falls between them:
- At δ₀=0.3: the pair is "in the regime"
- At δ₀=0.5: the pair is NOT

**Statistical concern:** A two-point threshold analysis can appear post-hoc. A principled approach would be a continuous curve of reversal rate vs. δ₀, or a principled justification of why 0.3 hops is "material" in a network where the null mean is ~2.2 hops.

The paper does not provide this justification. The δ₀=0.3 corresponds to roughly 0.3/2.2 ≈ 14% of the null mean — is that "material"? The choice needs justification.

**Severity: MODERATE.** Either add a continuous sweep or justify the threshold on substantive grounds.

---

## 8. SUMMARY OF STATISTICAL ISSUES

| # | Issue | Severity | Action |
|---|---|---|---|
| S1 | LLN caveat: terms are not i.i.d. under degree-matching | MINOR | Add one sentence acknowledging the approximation |
| S2 | Calibration Z vs Guney Z bridge needs numerical reconciliation | MINOR | Add one sentence with σ ratio comparison |
| S3 | R² = 0.9999 partly due to large-N probe design | MINOR | Add caveat sentence |
| S4 | P-value floor (0.001) is uninformative | MODERATE | Add explicit caveat about floor |
| S5 | BH correction scope unclear | MINOR | Clarify which tests, how many |
| S6 | PE is ordinal, not cardinal | MODERATE | Qualify "effect size" → "ordinal effect-size ranking" |
| S7 | Unconditional discordance should be more prominent | MODERATE | Elevate to standalone sentence in abstract/conclusion |
| S8 | δ₀ threshold needs justification | MODERATE | Add continuous sweep or principled justification |

---

## 9. WHAT THE PAPER GETS RIGHT

- ✅ Fixed-disease null is correct choice for cross-compound comparison
- ✅ (r+1)/(n+1) empirical p-values avoid zero p-values
- ✅ One-sided tests match directional hypotheses
- ✅ Z-scores are primary; p-values are secondary
- ✅ Transparency about direct-overlap confound (62%)
- ✅ Transparency about provenance asymmetry (literature vs ChEMBL)
- ✅ Transparency about two-sided null attenuation
- ✅ Transparency about α-sensitivity of PE ratios
- ✅ No overclaiming about DILI prediction

**Overall statistical grade: B+ → A− after addressing the 8 issues above.**

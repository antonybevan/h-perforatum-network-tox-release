# AGENT C — Systems/Engineering Methodology Memo
## Operating-Regime Benchmark: Structural Repositioning

**Agent:** C — Systems/Engineering Methodologist  
**Date:** 2026-07-01  
**Task:** Recast the operating-regime benchmark as the paper's calibration engine rather than a post-hoc biological-case justification.

---

## 1. Should the operating-regime benchmark lead BEFORE the biological case, or after?

**Answer: BEFORE.**

The benchmark should appear **before** the Hyperforin/Quercetin case study. The benchmark is not an extension-check on a single pair — it is the calibration apparatus that *defines the conditions under which the Z-score interpretation problem can arise at all*. When it follows the biological pair, the reader encounters the pair first and forms an intuition anchored to that pair; the benchmark then reads as a "did this generalize?" afterthought. Reversing the order makes the benchmark the engine and the biological pair a *located instance inside a characterized regime*.

**Current structure (problematic):**
```
§2.1 Biological pair: Hyperforin/Quercetin dissociation shown
§2.2 Null-SD shrinks with |T| (general principle, motivated by pair)
§2.3 Benchmark: 20K probes, δ_max, conditional reversals  ← reads as appendix
§2.4 Perturbation efficiency (solution)
```

**Recommended structure:**
```
§2.1 Benchmark: calibration apparatus → null-precision law → δ_max → conditional reversal rates
§2.2 Biological pair: Hyperforin/Quercetin as a located instance at 91st percentile
§2.3 Perturbation efficiency (solution)
```

**Soft alternative** (if the biological pair must stay first for narrative accessibility): keep the pair as a brief motivating vignette (3–4 sentences) that poses the "why does the closer compound look less significant?" question, then pivot immediately to the benchmark as the primary apparatus. Label the pair as an *illustrative preview*, then return to it in §2.2 after the benchmark is established. But the hard recommendation is to lead with the benchmark.

**Rationale:** A reviewer will ask "how do we know this isn't just one weird pair?" The benchmark answers that before the question is even asked. Leading with the benchmark also positions the paper as a *methods contribution with a worked example*, rather than a *case report with a methods appendix*.

---

## 2. How should "probes," "calibration Z-score," and "rank reversal" be introduced cleanly?

### Probes
Introduce as **synthetic stress-test instruments**, not "random target sets" in the passive sense:

> "We sampled 20,000 degree-distribution-pinned target-set *probes* at each of ten sizes — synthetic 'null compounds' whose only function is to stress-test the standardization machinery. Each probe carries a degree-controlled target set and a calibration Z-score but no biological claim."

Key qualities to emphasize:
- **Degree-pinned:** sampled from the same degree-bin profile as real compound targets (using Guney's ≥100-node bins), so they inhabit the same degree space without being real drugs
- **Synthetic:** no toxicity outcome is modeled; probes are not "fake drugs" — they are stress-test instruments
- **Scale:** 20,000 per size × 10 sizes = 200,000 probes; 500,000 cross-size pairs per size comparison

**Avoid:** "random gene sets" or "random compounds" — these suggest the probes are trying to be biological entities. They are not. They are calibration instruments.

### Calibration Z-score
Distinguish sharply from the per-compound Guney null:

> "The calibration Z-score is each probe's deviation from the *size-matched probe distribution* itself — not a separate per-probe permutation null. Because N = 20,000 per size, self-inclusion has negligible influence on the size-level null parameters. This is a benchmark-internal reference, distinct from the per-compound degree-matched null used for real drugs in §2.2."

The term "calibration Z-score" should appear as a defined term with a clear distinction from "proximity Z-score" (Guney null). Consider using a different symbol or subscript: Z_calib vs Z_prox.

**Current problem in the text:** The benchmark Z-score is described as "used to study the operating behaviour of standardisation across target counts; it is not the per-compound Guney null used for the real compounds." This is clear but buried. It needs to be prominent.

### Rank reversal
Define operationally, not as a "failure":

> "A rank reversal occurs when the smaller target set is closer by raw distance yet the larger target set has the more negative Z-score — the evidence ranking contradicts the effect ranking. This is not a bug in the Z-score; it is a consequence of the null-variance shrinkage that the Z-score is designed to exploit for sharper per-compound inference."

Frame it as a *ranking disagreement between two valid statistics*, each answering a different question. This preserves the integrity of the Z-score while characterizing when its magnitude should not be compared across compounds.

---

## 3. How do we present rare conditional reversals (0.39%) without seeming anticlimactic?

**The 0.39% is not anticlimactic — it is the core finding.** The rarity *is* the calibration. The benchmark's value is in showing that the reversal is a precisely bounded tail phenomenon, not a generic hazard.

### Framing strategy: "The boundary is the finding"

> "Conditional on a material raw-distance margin (≥0.3 hops), reversals occur in ≈0% of probe pairs up to R=4 and only 0.39% at R=8. This does not mean the problem is negligible — it means we now know *exactly when* to expect it."

The narrative arc should be:

1. **The naive problem** (~12% unconditional discordance): "If you compare Z-scores blindly, the ranking disagrees with raw distance ~12% of the time at R=6.2."
2. **The calibration answer** (conditional rates): "But once you require the smaller set to be *genuinely closer* by a material margin — the scenario that matters for biological interpretation — the reversal rate collapses to near-zero at moderate size ratios and peaks at 0.39% at R=8."
3. **The location of the biological pair**: "The Hyperforin/Quercetin pair (R=6.2, margin 0.38 at 91st percentile) lands inside this precisely characterized tail."

### Why this framing works:
- It transforms "only 0.39%" from a letdown into a precision instrument. The benchmark doesn't just say "reversals are rare" — it says "here is the exact boundary, and here is where the biological pair sits relative to it."
- The unconditional ~12% provides the tension; the conditional ~0.39% provides the resolution.
- The no-shrinkage counterfactual (0% at every R) proves that the shrinkage mechanism is necessary for any reversal at all — reinforcing that the benchmark is characterizing a real statistical phenomenon, not noise.

### What to avoid:
- Do NOT say "reversals are reassuringly rare" or "the problem is small." This undermines the benchmark's value. Say "the reversal is a precisely characterized tail regime" and let the reader judge importance.
- Do NOT lead the paragraph with "only 0.39%." Lead with the conditional framing and the materiality threshold, then report the number.

---

## 4. How should the unconditional ~12% discordance be positioned?

**The ~12% is the problem statement — it is what the conditional rates solve.**

Position it as the **naive baseline** that motivates the benchmark, not as a competing finding:

> "Unconditionally — i.e., comparing Z-score and raw-distance rankings across all cross-size probe pairs without requiring a material raw-distance margin — the two rankings disagree in ~12% of comparisons at R=6.2. This is the rate at which a naive cross-compound Z-score comparison would produce the wrong effect-size ordering. The benchmark's conditional analysis then shows that nearly all of these discordant pairs involve negligible raw-distance margins where the ranking is essentially arbitrary; once a material margin is required, the discordance rate collapses."

### Logical flow:
```
Unconditional discordance (~12%)  →  "This is why the problem matters"
Conditional reversal (0–0.39%)    →  "This is when the problem actually occurs"
δ_max derivation                  →  "This is why it occurs"
```

The unconditional rate should appear **once**, as context, and never again. Do not juxtapose it with the conditional rate in a way that makes the conditional rate look trivial ("only 0.39% vs 12%"). Instead, frame the conditional analysis as *explaining* the unconditional rate — the 12% is mostly noise pairs with tiny margins; the material-margin pairs are the ones that matter.

### Specific text placement:
The unconditional rate should appear early in the benchmark section, as the motivating observation that justifies the conditional analysis. It should NOT appear in the abstract or in the discussion as a standalone number — it is a benchmark-internal diagnostic, not a biological claim.

---

## 5. Should δ_max be derived before or after showing the reversal rates?

**BEFORE.** The derivation provides the *mechanism*; the rates provide the *empirical confirmation*. Showing rates without the derivation makes the benchmark descriptive; showing the derivation without the rates makes it theoretical. Both are needed, but the derivation must come first because it explains *why* the rates take the values they do.

### Recommended order within the benchmark section:

1. **Null-precision law** (σ_null ∝ |T|^{-1/2}, fitted slope, CI, R², module stability) — establishes the scaling
2. **δ_max derivation** — shows that the variance contrast (√R) creates an overturn-capacity envelope
3. **Envelope visualization** (Figure 3B) — the envelope as a function of R
4. **Empirical reversal rates** (conditional, by R, with δ₀ thresholds) — confirms the envelope
5. **Unconditional contrast** — explains why the naive rate is higher
6. **Biological pair location** — places Hyperforin/Quercetin at 91st percentile, inside envelope

### δ_max presentation notes:

The current derivation:  
δ_max(R) = (μ_L − μ_S) + |z_S| σ_L (√R − 1)

This is algebraically tight but needs a one-sentence intuition: "The larger set's null is √R times sharper, so it can register a weaker raw signal as stronger evidence — up to this bound."

The alternative form: |z_S| σ_S (1 − R^{-1/2}) makes the saturation explicit and is useful for showing that even at R → ∞, the overturnable margin is bounded.

---

## 6. Proposed 3-paragraph benchmark narrative (feels central, not appended)

### Paragraph 1 — The calibration apparatus

> To characterize when and under what conditions the target-count asymmetry distorts cross-compound Z-score comparisons, we constructed a calibration benchmark independent of any biological compounds. We sampled 20,000 degree-distribution-pinned target-set *probes* at each of ten sizes (|T| ∈ {5, 8, 10, 15, 20, 30, 40, 60, 62, 80}) from the same liver-expressed interactome and DILI module used throughout. Each probe is a synthetic stress-test instrument — a degree-controlled target set carrying no biological claim — and its calibration Z-score is its deviation from the size-matched probe distribution itself, not a per-compound permutation null. Across size pairs, we constructed 500,000 cross-size probe comparisons per size ratio, with the smaller set fixed at |T_S| = 10 and the larger set growing to R = |T_L|/|T_S| ∈ {1.5, 2, 3, 4, 6, 6.2, 8}. The benchmark's purpose is not to model toxicity or to evaluate real drugs; it is to characterize the statistical regime in which the Z-score's null-variance shrinkage — a feature, not a defect — can reverse the evidence ranking relative to the raw effect-size ordering.

### Paragraph 2 — The null-precision law and the overturn-capacity envelope

> The benchmark confirms that the null standard deviation scales as σ_null ∝ |T|^{-1/2} (fitted slope −0.499, 95% CI [−0.502, −0.495], R² = 0.9999), indistinguishable from the theoretical −1/2 implied by the Law of Large Numbers acting on a per-target mean. This exponent is stable across the real DILI module (−0.495) and three random size-matched pseudo-modules (mean −0.498; Fig. 3A), confirming that the scaling is a structural property of the interactome's distance geometry rather than an artefact of the specific disease-gene set. From this scaling, the maximum raw-distance margin that the larger set's sharper null can overturn follows directly: δ_max(R) = (μ_L − μ_S) + |z_S| σ_L (√R − 1). For fixed smaller-set size, the overturnable margin can be written as |z_S| σ_S (1 − R^{-1/2}), making explicit that the capacity grows with R but saturates — even at arbitrarily large target-count ratios, the larger set cannot overturn an arbitrarily large raw-distance advantage. The envelope grows because the larger set's null standard deviation shrinks; it saturates because the shrinkage itself follows |T|^{-1/2}, and the difference σ_S − σ_L = σ_S (1 − R^{-1/2}) approaches σ_S asymptotically.

### Paragraph 3 — Conditional reversal rates and the location of the biological pair

> Unconditionally, Z-score and raw-distance rankings disagree in approximately 12% of cross-size probe comparisons at R = 6.2, a rate high enough that naive cross-compound Z-score comparison would produce the wrong effect-size ordering in roughly one of every eight comparisons. However, nearly all of these discordant pairs involve negligible raw-distance margins where the ranking is effectively arbitrary. Conditioning on the smaller set being genuinely closer by a material margin (δ₀ ≥ 0.3 hops, approximately 14% of the null-mean closest distance in this network), the reversal rate collapses: ≈0% up to R = 4 and only 0.39% at R = 8 (δ₀ ≥ 0.5: ≤0.01% throughout; a no-shrinkage counterfactual gives 0% at every R, confirming that the variance shrinkage is necessary for any reversal). Reversals materialize specifically when the smaller set has an unusually large |z_S| — above the 90th percentile of probe-pair margins — so that its modest raw advantage falls inside the δ_max envelope. The Hyperforin/Quercetin pair, the biological worked example introduced next, occupies precisely this characterized regime: Hyperforin's raw-distance margin over Quercetin (d_c difference 0.38 hops) sits at the 91st percentile of probe-pair margins and below the δ_max ≈ 0.63 envelope at R = 6.2, placing it inside the reversal region (Fig. 3B–C). The benchmark thus defines the conditions under which the interpretation problem arises; the biological pair is a located instance within those conditions, not the sole evidence for them.

---

## 7. How should Figure 3 (operating regime) be described differently in the caption?

### Current caption (problems annotated):

> **The null-precision law defines a conditional operating regime for rank reversal.** [*Title is passive; doesn't say this is a calibration benchmark*] Degree-controlled target-set probes on the liver LCC and DILI module (Methods); no toxicity outcome is modelled. [*Opens with biological context, not the apparatus*] **(A)** The null standard deviation scales as σ_null ∝ |T|^{-1/2} (fitted slope −0.50; dashed −1/2 reference), with the same exponent for the real DILI module and for random size-matched pseudo-modules. [*Good*] **(B)** The maximum raw-distance margin the larger set can overturn, δ_max(R), increases with target-count ratio but saturates for fixed smaller-set size; the Hyperforin/Quercetin observed margin (0.38 at R=6.2) lies below the envelope and is therefore overturnable. [*The biological pair appears immediately in a figure that should be about the benchmark*] **(C)** Operating-regime plane at R=6.2: each point is a probe pair, plotted by raw-distance margin (>0: smaller set closer) versus evidence gap (>0: larger set stronger); the reversal region is shaded. Material-margin reversals are rare for generic probes; Hyperforin/Quercetin (orange) sits in the reversal region at the 91st proximity percentile. [*Again, the biological pair dominates the caption's second half*]

**Problems summarized:**
1. Title doesn't say "calibration benchmark" — it sounds like a biology result
2. Opens with the biological context (liver LCC, DILI module), not the benchmark apparatus
3. The biological pair appears in panels B and C, making the figure feel like it exists to validate the pair
4. The benchmark's scale (20,000 probes, 500,000 pairs) is never stated in the caption
5. The δ_max formula isn't in the caption (it should be, as this is a methods-calibration figure)

### Proposed revised caption:

> **Calibration benchmark characterizing the operating regime of the proximity Z-score under target-count asymmetry.** 20,000 degree-distribution-pinned random probe sets per size across |T| ∈ {5,…,80} from the liver-expressed STRING ≥900 interactome; 500,000 cross-size probe pairs per size comparison (Methods). Probes are synthetic calibration instruments — degree-controlled target sets carrying no biological claim — and their calibration Z-scores are deviations from the size-matched probe distribution, not per-compound permutation nulls. No toxicity outcome is modelled. **(A)** Null standard deviation scales as σ_null ∝ |T|^{-1/2} (fitted slope −0.50; dashed theoretical −1/2 reference), with the same exponent for the real DILI module (−0.495) and three random size-matched pseudo-modules (mean −0.498), confirming the scaling is a structural property of the interactome's distance geometry. **(B)** The maximum overturnable raw-distance margin, δ_max(R) = (μ_L−μ_S) + |z_S| σ_L (√R−1), derived from the |T|^{-1/2} law; the envelope grows with target-count ratio R = |T_L|/|T_S| but saturates because the variance contrast is bounded. The orange point marks the Hyperforin/Quercetin pair (R = 6.2, margin 0.38 hops), shown for reference — it lies below the envelope. **(C)** Operating-regime plane at R = 6.2: each gray point is a probe pair (margin > 0: smaller set closer; evidence gap > 0: larger set stronger Z). Orange points mark reversal-region pairs (upper-right quadrant). Material-margin reversals are conditional and rare: 0% up to R = 4, 0.39% at R = 8 (δ₀ ≥ 0.3 hops); a no-shrinkage counterfactual yields 0% throughout. The biological pair (orange cross) is a located instance at the 91st percentile of probe-pair margins — it inhabits the characterized tail, not a generic outcome.

### Key changes from current to proposed:

| Element | Current caption | Proposed caption |
|---|---|---|
| **Title** | "The null-precision law defines…" (passive, biological-sounding) | "Calibration benchmark characterizing…" (active, methodological) |
| **Opening** | Context (liver LCC, DILI module) | Apparatus (20K probes, 500K pairs) |
| **Probe identity** | "Degree-controlled target-set probes" (terse) | "Synthetic calibration instruments — degree-controlled target sets carrying no biological claim" (explicit) |
| **δ_max formula** | Absent | Included in Panel B description |
| **Biological pair** | Described in panels B and C as if central | Referenced as annotation ("shown for reference," "located instance") |
| **Conditional rates** | "Material-margin reversals are rare" (vague) | Specific: "0% up to R=4, 0.39% at R=8 (δ₀≥0.3)" |
| **Counterfactual** | Absent | "No-shrinkage counterfactual yields 0% throughout" |
| **Closing** | "Hyperforin/Quercetin sits in the reversal region at the 91st percentile" | "…inhabits the characterized tail, not a generic outcome" |

---

## Summary of recommendations (executive-ready)

| # | Question | Answer |
|---|---|---|
| 1 | Benchmark before or after biological case? | **Before.** Benchmark is the calibration engine; the biological pair is a located instance. |
| 2 | How to introduce probes / calib-Z / reversal? | Probes = synthetic stress-test instruments; calib-Z = benchmark-internal reference (≠ Guney null); reversal = ranking disagreement between valid statistics. |
| 3 | Present 0.39% without anticlimax? | Frame as precision calibration: "The boundary is the finding." Show naive ~12% first, then conditional ~0.39% as the resolution. |
| 4 | Position ~12% unconditional? | As the motivating baseline — it's what the conditional analysis *explains*. Appear once early, never in abstract/discussion as standalone. |
| 5 | δ_max before or after reversal rates? | **Before.** Derivation explains mechanism; rates provide empirical confirmation. |
| 6 | 3-paragraph narrative | (1) Apparatus: 20K probes, 500K pairs, synthetic instruments. (2) Law + envelope: σ_null ∝ \|T\|^{-1/2}, δ_max derivation, saturation. (3) Conditional rates → biological pair location at 91st percentile. |
| 7 | Figure 3 caption revision | Lead with "Calibration benchmark"; state 20K/500K scale; include δ_max formula; demote biological pair to annotation. |

---

## Implementation notes for the manuscript edit

If these recommendations are accepted, the following concrete edits to `results.tex` are needed:

1. **Reorder sections:** Move §2.3 (operating regime) before §2.1 (biological pair), renumbering accordingly. The current §2.2 (null-SD scaling) merges naturally into the benchmark as its first sub-result.

2. **Rewrite the benchmark opening sentence** (currently line 44 of results.tex): Replace "To test whether the statistical mechanism underlying the effect-size/evidence dissociation extends beyond this single pair…" with the calibration-apparatus framing from paragraph 1 above.

3. **Revise the biological-pair section** (§2.1): After the benchmark, the biological pair should open with "The Hyperforin/Quercetin pair occupies precisely this characterized regime" rather than discovering the dissociation independently.

4. **Update Figure 3 caption** in `main.tex` (line 108).

5. **The transition sentence** (currently line 26 of results.tex: "before introducing that effect size, we first test whether the statistical mechanism…") becomes unnecessary and should be removed or repurposed as a forward reference.

6. **Discussion section** (line 15 of discussion.tex): References to "The operating-regime benchmark (§2.3) establishes…" should update the section number and reinforce the benchmark-as-engine framing.

---

*End of memo.*

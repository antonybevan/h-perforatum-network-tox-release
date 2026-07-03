# Response to Reviewers

**Manuscript:** *Separating effect size from statistical evidence in network-proximity rankings under target-count asymmetry: a controlled liver-interactome audit*.

We thank the editor and both reviewers for their careful assessment. The comments substantially improved the manuscript. In particular, Reviewer 2 correctly noted that target-count-dependent shrinkage of the null variance is expected statistical precision rather than a flaw in proximity Z-scores. We have therefore reframed the manuscript around the distinction between standardized evidence and raw effect-size ranking, and we have removed language suggesting that proximity Z-scores are biased or that perturbation efficiency replaces them.

The revision makes five substantive changes:

1. **Reframed thesis.** The manuscript now states that proximity Z-scores are valid evidence statistics, but that their magnitude should not be interpreted as a cross-compound effect-size ranking when target counts differ strongly. This framing is consistent with Guney et al. (2016), Menche et al. (2015), and the ASA statement on p-values (Wasserstein and Lazar, 2016).
2. **Direct versus propagated influence.** We added a new analysis separating direct target-DILI overlap from propagated random-walk influence (Results Section 2.5, Table 3, Figure 6). The raw approximately 3.5-fold per-target influence advantage is 62% direct overlap; the propagated residual is more modest, approximately 1.5-fold and 1.2- to 1.9-fold across alternative exclusions.
3. **Requested sensitivity analyses.** We added restart-probability sensitivity, expression-floor sensitivity, and a formal null-variance scaling audit.
4. **Guney-fidelity revalidation.** We revalidated the closest-distance proximity implementation against Guney-style degree binning and a two-sided null construction, confirming that the observed closest distances and the effect/evidence dissociation are not artifacts of the local implementation.
5. **Operating-regime benchmark.** We added a degree-controlled liver-network calibration benchmark using 20,000 probes per target-set size and 500,000 cross-size probe pairs. This shows that the approximately \(|T|^{-1/2}\) null-precision law holds across the DILI module and size-matched pseudo-modules, and that material rank reversal is conditional rather than a generic outcome.

All new results are reproducible from the committed repository scripts, including `REVIEWER_EVIDENCE.py`, `REVIEWER_EVIDENCE_leakage_scaling.py`, and `GUNEY_FIDELITY_check.py`.

---

## Editor

### E.1 Code deposition in a DOI-issuing repository and Code Availability statement.

Addressed in the revised manuscript. We added a dedicated **Code Availability** section (`manuscript/sections/code_availability.tex`) describing the public GitHub repository, license terms, pinned dependency files, checksum manifest, full pipeline entry point, and reviewer-evidence verification scripts. The tagged publication snapshot will be deposited in Zenodo before final resubmission, and the Zenodo DOI will be inserted into the final Code Availability section. The repository materials include the analysis code, curated input data, committed result tables, figure-generation scripts, and checksums for the processed data artifacts.

---

## Reviewer 1

### 1.1 Motivation for the Hyperforin/Quercetin liver system.

We have expanded the Introduction to explain the choice of system. Hyperforin and Quercetin are presented as a deliberately high-contrast diagnostic pair, not as a broadly sampled compound set. They share a botanical source, differ strongly in target count (10 versus 62 targets in the liver LCC), and provide a mechanistically interpretable contrast: Hyperforin is the PXR-activating, CYP/transporter-inducing constituent associated with St John's Wort drug-interaction biology, whereas Quercetin is the high-target-count comparator. We also clarify that Hyperforin is not treated as an established intrinsic hepatotoxin and that the analysis is a controlled methodological audit rather than a DILI-risk prediction study.

### 1.2 Define DILI at first use.

Addressed. The manuscript now defines DILI as drug-induced liver injury at first mention.

### 1.3 Broken equation references.

Addressed. The two incorrect equation references were removed. The revised Results/Methods now contain correctly numbered equations for the RWR fixed point, the influence sum, and the perturbation-efficiency identity.

### 1.4 Formal link between influence `I`, `p(d)`, and efficiency.

Addressed. We now define perturbation efficiency directly from the RWR steady-state probability on disease-module nodes. Because the RWR steady state is linear in the restart vector, with a restart vector uniform over the target set,

> `E(T,D) = sum_{d in D} p_d = (1/|T|) sum_{t in T} sum_{d in D} p_d^{(t)}`.

Thus perturbation efficiency is the mean per-target influence on the disease module. We also verified the identity numerically: joint versus mean single-target influence is 0.11380975 versus 0.11380968 for Hyperforin, within RWR convergence tolerance. The earlier inconsistent secondary definition using `I/|T|` has been removed.

### 1.5 Generalization and benchmarking on DILIrank 2.0.

We agree that broader benchmarking is important, and we have revised the scope accordingly. The present repository contains curated target sets for the two stress-test compounds only. DILIrank 2.0 is a drug-level labeling resource rather than a harmonized drug-target-network benchmark; using it to test perturbation efficiency for drug-level DILI classification would require consistent target curation for many drugs and would need to account for dose, exposure, pharmacokinetics, reactivity, and binding directionality. We therefore no longer claim population-level predictive performance. Instead, we identify a properly powered DILIrank benchmark with curated targets as future work and keep the present contribution focused on statistical interpretation under target-count asymmetry.

To reduce reliance on the two-compound example, we added the operating-regime benchmark described above. This benchmark characterizes the statistic over degree-controlled random probes and shows that material effect/evidence reversal is conditional and relatively rare for generic probes.

### 1.6 Quantify variance shrinkage for RWR.

Addressed. We no longer claim that RWR or expression-weighted influence avoids target-count variance shrinkage. At STRING >=900, the null-SD ratio is 2.57 for shortest-path proximity, 2.45 for RWR, and 2.47 for EWI, close to the expected \(\sqrt{62/10}=2.49\). Across the two network thresholds, the RWR ratio spans 2.45 to 3.04. We now present this as a scaling result observed across the evaluated proximity and influence metrics.

### 1.7 Restart-probability sensitivity.

Addressed. We added a restart-probability sweep for \(\alpha \in \{0.10, 0.15, 0.20, 0.30, 0.50, 0.70\}\) at STRING >=900. The Hyperforin > Quercetin per-target influence ranking holds throughout, while the fold ratio is alpha-dependent:

| alpha | 0.10 | 0.15 | 0.20 | 0.30 | 0.50 | 0.70 |
|---|---|---|---|---|---|---|
| `E` ratio (Hyperforin/Quercetin) | 2.90 | 3.54 | 4.18 | 5.53 | 8.81 | 13.35 |

We therefore report the ordering as the robust result and avoid treating the alpha-dependent ratio as a fixed biological constant. We also corrected the RWR citation: Guney et al. use shortest-path proximity and do not define a restart parameter; the revised manuscript cites Kohler et al. (2008) for RWR.

### 1.8 Expression-floor sensitivity.

Addressed. We added an expression-floor sweep over \(0, 10^{-3}, 10^{-2}, 5 \times 10^{-2}, 10^{-1}\). The EWI ratio remains 2.69 to 2.70 across this range, indicating that the 0.01 floor does not materially affect the result.

### 1.9 AI-style figure summaries.

Addressed. The figure overlays and AI-style explanatory summaries were removed. The figures now contain standard titles, axes, legends, and journal-style captions. The manuscript retains a concise AI-use disclosure in the Methods: “AI-assisted tools were used for code drafting and language editing. All analyses, results, and interpretations were verified by the authors.”

---

## Reviewer 2

### 2.1 Dependence of proximity Z-scores on target-set size is expected precision, not bias.

We agree. This is now the central framing of the revision. We removed language describing target-count-dependent null-variance shrinkage as a defect, artifact, or bias. The revised manuscript states that a proximity Z-score is an evidence statistic,

> `Z = (M_obs - mu_null) / sigma_null`,

and that larger target sets can legitimately yield stronger standardized evidence because the null standard deviation of an averaged statistic shrinks with target count. We now explicitly distinguish Quercetin's stronger standardized evidence from Hyperforin's stronger raw topological proximity.

We formalize this point with a null-SD scaling audit. For random seed sets, the null standard deviation scales as approximately \(|T|^{-0.48}\), close to the theoretical \(-1/2\) expectation; the degree-controlled operating-regime benchmark refines this exponent to \(-0.499\) (95% CI \([-0.502,-0.495]\)):

| \|T\| | 5 | 10 | 20 | 40 | 62 |
|---|---|---|---|---|---|
| null SD | 0.00931 | 0.00677 | 0.00594 | 0.00350 | 0.00278 |

Across metrics, the Hyperforin/Quercetin null-SD ratio remains close to the expected \(\sqrt{62/10}=2.49\): shortest-path 2.57, RWR 2.45, and EWI 2.47 at STRING >=900.

### 2.2 RWR and EWI also show approximately 2.5-fold SD shrinkage.

Agreed and addressed. We deleted the earlier reduced-shrinkage claim for influence propagation. RWR is now presented as a different effect-size scale, not as a method that avoids the law-of-large-numbers shrinkage. RWR and EWI Z-scores remain evidence statistics and are subject to the same target-count scaling.

### 2.3 Perturbation-efficiency Z-scores do not replace traditional proximity Z-scores.

Agreed. We no longer present RWR or EWI Z-scores as replacements for proximity Z-scores. The revised manuscript separates four quantities:

| Quantity | Question addressed | Role |
|---|---|---|
| `d_c` (shortest-path) | How close are targets to the disease module? | Raw topological effect size |
| Proximity Z | Is that proximity surprising under a matched null? | Evidence |
| RWR per-target influence `E` | How much random-walk mass reaches the disease module per target? | Propagated effect size |
| RWR/EWI Z | Is that influence surprising under a matched null? | Evidence |

Perturbation efficiency is therefore an effect-size complement to the Z-score, not a replacement for it.

### 2.4 Support for claims and scope of conclusions.

We have substantially narrowed and re-supported the claims. First, the revised manuscript no longer claims that proximity is biased, that RWR resolves a bias, or that perturbation efficiency predicts DILI. Second, we revalidated the closest-distance proximity results against Guney-style degree binning and the two-sided null. The observed closest distances are reproduced, and the two-sided null attenuates the evidence gap to near parity (Hyperforin \(Z=-3.55\), Quercetin \(Z=-3.66\)), while the fixed-disease null remains the primary comparison for two compounds against the same disease module. Third, we added the direct-overlap analysis below, which reduces the biological overstatement of the original version.

The revised contribution is therefore a controlled methodological audit of effect-size/evidence interpretation under target-count asymmetry, not a proposed toxicity predictor or a replacement significance statistic.

---

## Additional Analysis Added in Revision: Direct Overlap Versus Propagated Influence

We added a new Results subsection, table, and figure to separate direct target-DILI overlap from propagated influence. Four of ten Hyperforin targets are DILI-module genes (ABCB1, CYP2C9, MMP2, NR1I2), whereas one of 62 Quercetin targets is a DILI-module gene (MMP2). The revised manuscript decomposes the per-target influence as follows at STRING >=900:

| Quantity | E(Hyperforin) | E(Quercetin) | Ratio |
|---|---|---|---|
| Raw per-target influence | 0.1138 | 0.0322 | 3.5x |
| Direct-overlap component | 0.0711 | 0.0032 | 22.5x |
| Propagated component (leave-one-out) | 0.0427 | 0.0290 | 1.5x |

Thus, 62% of Hyperforin's per-target influence is direct overlap. The propagated residual is more modest: approximately 1.5-fold, and 1.2- to 1.9-fold across alternative exclusions. Against a global degree-matched random 10-gene background, the propagated component is at the 99.9th percentile (3.3-fold above the background mean; empirical \(p=0.002\)), but it does not exceed all random sets and overlaps the upper tail of size-matched Quercetin subsets.

We also added two corroborating checks in the Supplement. Menche et al.'s network separation measure \(S_{AB}\) shows that both target sets are topologically separated from the DILI module. A direct-connectivity count shows that Hyperforin targets carry more distance-1 DILI links per target (3.4 versus 1.5), consistent with the direct/propagated decomposition.

Finally, we added a DILI-module sensitivity analysis in which the four genes that are both Hyperforin targets and DILI-module members are removed from the disease module. The propagated advantage does not collapse; it changes from 1.47-fold to 1.58-fold. This supports the interpretation that the propagated residual is not solely an artifact of direct target-module overlap, while also making clear that the raw 3.5-fold value should not be interpreted without the decomposition.

---

## Explicit Limitations Added or Strengthened

To avoid overinterpretation of the controlled two-compound design, the revised manuscript explicitly states that:

- Perturbation efficiency is not validated as a drug-level DILI-risk predictor.
- No full DILIrank predictive benchmark is claimed.
- Network influence is topological reach, not a toxicological outcome.
- Dose, exposure, pharmacokinetics, binding directionality, and reactivity are not modeled.
- STRING is used as a functional association network, not a purely physical PPI network.
- The DILI module is a curated association set, not a validated causal gene set.
- Hyperforin/Quercetin are a diagnostic stress-test pair, not a representative compound sample.
- Hyperforin is not presented as an established intrinsic hepatotoxin.

---

## Summary of Changes

- Revised title, abstract, and Introduction to focus on effect size versus evidence.
- Removed defect/bias-correction language, variance-escape claims, uniqueness claims, and DILI-prediction framing.
- Added Code Availability and DOI-archiving language in response to the editor's requirement.
- Removed AI-style figure summaries and regenerated figures with standard scientific captions.

### Additional analyses carried out

- Direct versus propagated influence decomposition (§2.5, Table 3, Figure 6)
- Restart-probability sensitivity (§2.6, Table S-alpha)
- Expression-floor sensitivity (§2.6, Table S-floor)
- Null-SD scaling audit (§2.1, Table 2, Table S-null)
- Guney-fidelity revalidation (§2.7, Table S-Guney)
- Fixed-disease versus two-sided null comparison (Table S-Guney)
- Operating-regime benchmark (§2.8, Table S-opregime, Figure S1)
- Text-mining robustness (Table S-textmining)
- DILI-module sensitivity (Table S-modulesens)

### Analysis not carried out and rationale

Full DILIrank predictive benchmarking was not performed. As discussed in the response to Reviewer 1.5, this would require harmonised curated target sets for many drugs, together with dose, exposure, pharmacokinetics, binding directionality, and reactivity modelling. The present paper is a controlled statistical-interpretation audit under target-count asymmetry, not a DILI-risk predictor. We identify a properly powered DILIrank benchmark with curated targets as future work.

---

We thank the editor and reviewers again for comments that substantially strengthened both the statistical framing and the empirical support for the revised manuscript.


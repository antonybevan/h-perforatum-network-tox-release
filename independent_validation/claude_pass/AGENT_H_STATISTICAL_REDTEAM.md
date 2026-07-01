# AGENT H: Statistical Red-Team Review

**Agent:** H — Adversarial Statistical Reviewer  
**Date:** 2026-07-01  
**Target:** "Separating effect size from statistical evidence in network-proximity rankings under target-count asymmetry"  
**Repository:** h-perforatum-network-tox-clean  
**Independence:** Fresh Hermes subagent. No access to prior audit reports. Reads only the specified source files.

---

## Executive Summary

This paper makes a legitimate methodological observation — that proximity Z-scores can mislead as cross-compound effect-size rankings under target-count asymmetry — and provides useful empirical quantification. However, the contribution is narrower than the framing suggests. The core mathematical mechanism (|T|^{-1/2} shrinkage) is an algebraic consequence of averaging, not an empirical discovery. The operating-regime benchmark adds genuine empirical value but the bridge to the real compounds is muddy. The perturbation-efficiency metric is unvalidated and α-sensitive. The provenance asymmetry between target sets (literature-curated vs. ChEMBL) is a fundamental confound for the biological case study. And the 91st-percentile framing of "unusually proximal" is overstated. Below, I attack every claim systematically.

**Overall verdict:** The paper's statistical mechanism is correct but its contribution is overstated. The paper is fixable with reframing, additional validation, and caveat strengthening. No single attack is fatal to the core statistical point, but the biological case study and the perturbation-efficiency metric are the weakest links.

---

## ATTACK 1: The |T|^{-1/2} law is algebraically trivial

**Claim under attack:** "The null standard deviation shrinks with target count for every metric" (results.tex §2), "σ_null ∝ |T|^{-0.48} (theoretical -1/2)" (abstract.tex L3), presented as a core finding.

**Attack:** The closest distance is defined as d_c(T,D) = (1/|T|) Σ_{t∈T} min_{s∈D} dist(t,s) (methods.tex L7). This is an arithmetic mean of |T| terms. Under the null (random degree-matched target sets), these terms are approximately i.i.d. draws from a distribution with finite variance. By the Law of Large Numbers, Var(d_c) = Var(individual term) / |T|, hence σ_null ∝ |T|^{-1/2}. This is not an empirical finding — it is an algebraic identity that follows from the definition of the statistic as an average. The paper itself acknowledges this: "This is the Law of Large Numbers acting on a mean over targets" (results.tex L26), "as expected for an averaged statistic rather than a flaw in any metric" (abstract.tex L3).

**What is the actual contribution?** The non-trivial work is: (a) confirming empirically that the i.i.d. approximation holds for this specific network's degree-geometry (the exponent is not exactly -1/2 if the null terms are correlated through degree constraints), and (b) demonstrating the practical consequence — that cross-compound Z-score comparison is unreliable. The paper should frame this as: "We confirm that the LLN-expected behavior holds in practice for this network, and we quantify the interpretive consequences." Currently, the paper presents the law as if it were a discovery.

**Evidence:** The log-log slope of -0.48 (results.tex L26) vs. theoretical -1/2, and the operating-regime slope of -0.499 (results/tables/operating_regime_summary.csv L2, `slope_pinned` = -0.49884) with R² = 0.9999.

**Classification: MAJOR (but fixable).** The paper's framing overstates the novelty of the algebraic mechanism. The contribution is the empirical confirmation and the practical demonstration, not the law itself. Reframe the introduction and abstract to make this explicit.

---

## ATTACK 2: The operating-regime benchmark adds real but limited information beyond the algebra

**Claim under attack:** The operating-regime benchmark (§2.3) as a major evidentiary contribution.

**Attack:** The benchmark does two things: (1) confirms the |T|^{-1/2} exponent empirically in the specific network (slope = -0.499, 95% CI [-0.502, -0.495], R² = 0.9999), and (2) quantifies conditional reversal rates (0.39% at R=8, δ₀=0.3). 

Item (1) is largely confirmatory of the algebra. Item (2) is genuinely non-trivial: the reversal rate depends on the specific distance geometry of the DILI module, the degree distribution of the network, and the null construction, none of which can be derived algebraically. The δ_max formula (results.tex L46) is algebraically derived from the |T|^{-1/2} law, but the realized reversal rate is an empirical quantity that the benchmark measures.

However, the benchmark only characterizes *this* liver LCC and *this* DILI module. The paper acknowledges "the rate of reversal is a property of the DILI module's distance geometry and is not claimed to be network-universal" (discussion.tex L15). But the benchmark's probes are degree-controlled random sets, not real drug-target sets. Real drug targets may have different topological properties (functional clustering, co-complex membership) that affect the null distribution's behavior. The benchmark therefore characterizes the *statistic's* behavior for a particular network geometry, not the behavior of real drug-target comparisons.

**Classification: LIMITATION ONLY.** The benchmark adds genuine empirical value, but the paper should be clearer that it characterizes the statistic-in-this-network, not drug-target ecology. The algebraic-vs-empirical boundary should be drawn more sharply.

---

## ATTACK 3: Calibration Z-scores and Guney Z-scores are different constructs, risking conflation

**Claim under attack:** The operating-regime benchmark's relevance to the real-compound Z-score dissociation.

**Attack:** The operating-regime benchmark uses *calibration Z-scores* computed from a size-level reference distribution of 20,000 probes (methods.tex L22: "each probe's calibration Z-score is its deviation from that shared size-level reference, not a separate per-probe permutation null"). The real compounds use *Guney Z-scores* from per-compound degree-matched permutation nulls (1,000 permutations, seed 42).

These are different null constructions:
- **Calibration Z:** Each probe is compared to the pooled distribution of all 20,000 probes at that size. This is a parametric-like Z (given N=20,000, the reference distribution is well-estimated).
- **Guney Z:** Each compound gets its own degree-matched null of 1,000 random sets. The null parameters (μ, σ) vary by compound depending on degree distribution.

The paper acknowledges this distinction (results.tex L44: "this benchmark Z-score is used to study the operating behaviour … it is not the per-compound Guney null used for the real compounds"). However, the paper then uses the benchmark to claim that the H/Q pair "lies in this regime" (results.tex L48), placing the real pair on the benchmark's δ_max curve (Fig. 3C). This implicitly assumes the calibration-Z and Guney-Z behave similarly, which is reasonable given the same |T|^{-1/2} mechanism, but not rigorously demonstrated. The benchmark's δ_max formula uses the calibration null's σ_L and σ_S. For the real compounds, the Guney null σ values differ from the calibration σ values because degree-matching constrains the null differently.

A reviewer would ask: do the Guney null σ values for the real compounds match the calibration null σ values at |T|=10 and |T|=62? If they differ systematically, the bridge between benchmark and real compounds weakens.

**Evidence from data:** From results.tex Table 1 (the "effevid" table): σ_null(Hyperforin, 10 targets) = 0.235, σ_null(Quercetin, 62 targets) = 0.091. Ratio = 2.58. The expected ratio from |T|^{-1/2} is √(62/10) = 2.49. Close but not identical. The difference (2.58 vs 2.49) reflects the degree-matching constraint. The benchmark's calibration σ values are not reported in the main text for direct comparison.

**Classification: MAJOR (but fixable).** The bridge between benchmark and real compounds needs explicit numerical reconciliation. Show that the calibration null σ values at |T|=10 and 62 match the real compounds' Guney null σ values, or explain the difference.

---

## ATTACK 4: The δ₀=0.3 threshold is cherry-picked to include the H/Q pair

**Claim under attack:** The conditional reversal analysis showing the H/Q pair "lies in this regime."

**Attack:** The paper conditions on δ₀ ∈ {0.3, 0.5} for the "material margin" threshold. The H/Q pair has a real margin of d_c difference = 0.377 (results/tables/operating_regime_summary.csv L2: `real_margin` = 0.3774). This falls between the two thresholds:
- At δ₀=0.3: the H/Q margin (0.38) qualifies as "material" → the pair is in the regime.
- At δ₀=0.5: the H/Q margin (0.38) does NOT qualify → the pair would NOT be in the regime.

The paper reports both thresholds, which is good practice. But the choice of δ₀=0.3 as a "material margin" is arbitrary. Why 0.3? Why not 0.2 or 0.4? The motivating example's margin sits conveniently above 0.3 but below 0.5, making the pair "in the regime" at the lower threshold but not the higher one. The paper does not discuss threshold sensitivity or justify the choice.

From the reversal table (results/tables/operating_regime_reversal.csv):
- At R=6.2, δ₀=0.3: Rrev = 0.000608 (0.061%), n = 74,016 qualifying pairs
- At R=6.2, δ₀=0.5: Rrev = 0.0 (0%), n = 18,848 qualifying pairs

The fact that at δ₀=0.5 the reversal rate drops to 0.0% (even at R=8, it's still 0.0%) suggests the "regime" is exquisitely sensitive to the threshold choice. A reviewer would demand: (a) a continuous analysis of reversal rate as a function of δ₀, not just two discrete thresholds, and (b) a justification for why 0.3 hops constitutes a "material" margin in a network where the null mean is ~2.2 hops.

**Classification: MAJOR (but fixable).** The threshold analysis needs a sweep over δ₀ (a curve, not two points) and a principled justification. The H/Q pair's margin falling between the two reported thresholds looks like threshold-hacking.

---

## ATTACK 5: "91st percentile" is not "unusually proximal"

**Claim under attack:** The H/Q pair is an instance where "the smaller set is unusually proximal" (abstract.tex L3, results.tex L48).

**Attack:** The paper reports that the H/Q margin (0.38 hops) is at the 91st percentile of probe-pair margins (results/tables/operating_regime_summary.csv L2: `located_percentile` = 90.6458). This means ~9% of random probe pairs have a margin ≥ 0.38 — i.e., the smaller set is even closer. 

In a normal distribution, the 91st percentile corresponds to z ≈ 1.34. This is not conventionally considered "unusual" — it falls within typical "non-significant" ranges in most scientific contexts. Calling this "unusually proximal" is an overstatement. 

The paper's narrative that "material rank reversal is … realised only when the smaller set is unusually proximal, as here" implies the H/Q pair represents a rare configuration. At the 91st percentile, it is uncommon but not rare. One could equally argue that ~9% of random pairs meet this condition, making the H/Q pair a relatively ordinary instance of the regime.

**Evidence:** `located_percentile` = 90.6458 from operating_regime_summary.csv. The unconditional directional reversal rate at R=6.2 is 6.5% (operating_regime_reversal.csv: `uncond_directional_reversal` = 0.065026), meaning 6.5% of random pairs show the same Z-score reversal pattern unconditionally.

**Classification: MAJOR.** The "unusually proximal" characterization is misleading at the 91st percentile. The paper should use more precise language (e.g., "above the 90th percentile" or "in the upper decile") and avoid implying extreme rarity.

---

## ATTACK 6: Extremely rare reversals undermine practical significance

**Claim under attack:** The practical importance of the Z-score reversal phenomenon.

**Attack:** The conditional reversal rates are extremely low:
- 0% at R ≤ 3 (δ₀=0.3)
- 0.0037% at R=4 (δ₀=0.3)
- 0.39% at R=8 (δ₀=0.3)
- 0% at all R for δ₀=0.5

The paper acknowledges that reversals are "conditional and rare" (abstract, discussion). But if the phenomenon requires a ratio of R≥6, a "material" margin, AND an "unusually proximal" smaller set (which occurs in ~9% of pairs), the practical window is very narrow. The unconditional directional reversal rate (6.5% at R=6.2) is higher, but the paper correctly distinguishes conditional from unconditional.

The question for a reviewer: if the phenomenon is so rare, is it worth a full paper? The counterargument (which the paper makes) is: (1) the H/Q pair is a real example, (2) the mechanism is general even if the realized rate is network-specific, and (3) methodological awareness is valuable even for rare events. This defense is reasonable but the paper should more explicitly address the "so what?" question given the extreme rarity.

**Classification: LIMITATION ONLY.** The paper is transparent about rarity. The mechanism's importance is independent of the reversal rate. But a stronger "practical significance" argument would strengthen the paper.

---

## ATTACK 7: Perturbation efficiency is an unvalidated metric with extreme α-sensitivity

**Claim under attack:** Perturbation efficiency as a useful effect-size complement.

**Attack:** Perturbation efficiency E(T,D) is introduced as "the mean per-target random-walk influence on the disease module — a size-normalised effect size" (results.tex L51). This is mathematically elegant (linearity of RWR in the restart vector), but:

**(a) No external validation.** The paper explicitly states "testing whether perturbation efficiency carries DILI signal beyond target count and degree across DILIrank 2.0 … is identified as future work" (discussion.tex L15). For a methodological paper proposing a new metric, a reviewer would demand at least a pilot validation. Without it, perturbation efficiency is an unvalidated candidate.

**(b) Extreme α-sensitivity.** The efficiency ratio varies from 2.90 at α=0.10 to 13.35 at α=0.70 (results.tex L66). This is a 4.6-fold range in the magnitude, even though the ranking is preserved. If the metric's magnitude is this sensitive to an arbitrary parameter, its practical utility as an effect size is questionable. The paper acknowledges this: "we therefore treat the ranking, not the ratio, as the robust feature" (results.tex L66). But if only the ranking is robust, then the metric is essentially an ordinal comparator, not a cardinal effect size.

**(c) No comparison to alternatives.** The paper doesn't compare perturbation efficiency to other candidate effect-size metrics (e.g., raw d_c, degree-normalized d_c, Guney's d_k, Menche's S_AB). Without such comparison, the claim that perturbation efficiency is "a natural choice" (discussion.tex L11) is unsupported.

**(d) The α=0.15 default is arbitrary.** The choice of α=0.15 is described as "a PageRank-style damping value" (methods.tex L10). This is a convention from web search, not a biologically motivated choice. The paper sweeps α and shows rank-robustness, but the choice of the primary reported value remains arbitrary.

**Classification: MAJOR (but fixable).** The metric needs at least pilot validation (even a small DILIrank subset), a comparison to alternative effect-size candidates, and a biologically motivated α selection or a more robust summary across α.

---

## ATTACK 8: 62% direct overlap undermines the network-proximity narrative

**Claim under attack:** The biological significance of Hyperforin's network-proximity advantage.

**Attack:** The decomposition (results.tex §5, results/tables/leakage_decomposition.csv) shows:
- Hyperforin raw per-target influence: 0.1138
- Direct overlap component: 0.0711 (62.5% of raw)
- Propagated component: 0.0427 (37.5% of raw)
- Quercetin raw: 0.0322, direct: 0.0032 (9.9%), propagated: 0.0290
- Propagated ratio: 1.47×

This is devastating for the biological narrative. The majority of Hyperforin's "network" advantage is not network-mediated at all — it's because 4 of its 10 targets (NR1I2, CYP2C9, ABCB1, MMP2) are themselves members of the DILI module. This is a set-overlap observation, not a network-topology finding.

The paper is commendably transparent about this: "62% of Hyperforin's per-target influence is direct overlap" (results.tex L72), "the propagated component … does not exceed every random set, and some size-matched Quercetin subsets reach comparable values" (results.tex L72). But this transparency undermines the paper's own contribution. A skeptical reviewer would ask: "If the core finding decomposes to '4/10 Hyperforin targets are DILI genes vs 1/62 for Quercetin,' what does the network analysis add?"

The paper addresses this partially: (a) the propagated component is still above a degree-matched background (99.9th percentile, empirical p=0.002), (b) the PXR-CYP-transporter axis is the established mechanism, and (c) the framework separates direct from propagated, which is itself valuable. But these defenses don't fully rescue the biological case.

**Classification: FATAL for the biological case study's headline claim; MAJOR for the paper overall.** The paper's methodological contribution (Z-scores mislead under asymmetry) survives. But the biological finding that "Hyperforin's targets are topologically better positioned" is largely reducible to target-list overlap with the DILI module. The paper should reframe the biological case study as a demonstration of the framework's ability to *detect and quantify* direct overlap, not as evidence of network-specific propagation.

---

## ATTACK 9: Target-set provenance asymmetry is a fundamental confound

**Claim under attack:** The comparability of Hyperforin and Quercetin as a case study.

**Attack:** The two target sets differ radically in provenance (supplementary.tex Table S1):
- **Hyperforin:** 10 literature-curated targets, mechanistically centered on the PXR/CYP axis. Each target has a specific, documented mechanism (direct agonism, induction, inhibition).
- **Quercetin:** 62 ChEMBL bioactivity-derived targets (IC₅₀/Kᵢ/EC₅₀ ≤ 10 μM), a broad in-vitro activity net that includes assay-context-dependent hits.

This is not just a size difference — it's a difference in target-set *quality, specificity, and biological coherence*. Hyperforin's targets are a tight functional module (the xenobiotic metabolism axis); Quercetin's are a heterogeneous collection. This asymmetry could produce the observed effect independent of topology:
- Hyperforin's curated targets may be enriched for DILI-relevant biology by construction (the PXR/CYP axis IS the DILI mechanism)
- Quercetin's ChEMBL targets may include many noise hits with no DILI relevance
- The size difference (10 vs 62) might itself be an artifact of curation depth

The paper acknowledges this limitation (discussion.tex L15: "a fully curation-matched comparison would require harmonised target evidence for both compounds, which we identify as a limitation rather than resolve here"). But a reviewer would likely demand:
1. At minimum, a ChEMBL-derived Hyperforin target set for comparison
2. Or literature-curated Quercetin targets
3. Or a sensitivity analysis restricting Quercetin to its most confident targets

Without this, the biological comparison is fundamentally confounded, and any claim about Hyperforin's topological advantage being network-mediated is suspect.

**Mitigation:** The operating-regime benchmark uses random degree-controlled probes (not real targets), so the core statistical claim is independent of provenance. The paper should explicitly separate: "The statistical mechanism (benchmark) does not depend on target-set provenance; the biological case study does, and we treat it as an illustrative demonstration with acknowledged limitations."

**Classification: FATAL for the biological case study as a clean comparison; MAJOR for the paper overall.** The statistical mechanism survives, but the paper should not present the H/Q comparison as a definitive biological finding. It should be reframed as an illustrative motivated example that highlights the need for curation-matched comparisons.

---

## ATTACK 10: Missing DILIrank benchmarking is a critical gap

**Claim under attack:** The adequacy of "future work" framing for perturbation efficiency validation.

**Attack:** The paper proposes perturbation efficiency as a practical effect-size metric and states DILIrank 2.0 benchmarking as future work (discussion.tex L15). For a methodological paper in 2026, this is a significant gap. DILIrank 2.0 (Chen 2016, Olubamiwa 2025) provides 1,336 classified drugs with known DILI concern levels. It is the obvious benchmark for any DILI-relevant network metric.

A reviewer would ask:
- Does perturbation efficiency discriminate DILI-positive from DILI-negative drugs better than raw d_c or proximity Z?
- Does it add information beyond target count and degree?
- Does the direct/propagated decomposition generalize?

Without answers to at least some of these questions, perturbation efficiency remains a mathematical construct without demonstrated utility. The "future work" framing is inadequate for a paper whose primary methodological contribution is proposing this metric.

**Classification: MAJOR (but fixable).** A pilot DILIrank analysis (even on a subset) would substantially strengthen the paper. If full DILIrank benchmarking is infeasible, the paper should more modestly frame perturbation efficiency as a "candidate effect-size metric requiring validation" rather than a "recommended" metric.

---

## ATTACK 11: The "only two compounds" criticism is partially but not fully addressed

**Claim under attack:** Generalizability beyond the H/Q pair.

**Attack:** The paper explicitly addresses the n=2 criticism: "the benchmark, not the pair alone, is what characterises the statistical regime" (results.tex L48). The benchmark uses 20,000 random probes per size (10 sizes × 20,000 = 200,000 probes; 500,000 cross-size pairs per size pair). This is statistically thorough for characterizing the *statistic's* behavior.

However, the benchmark's probes are:
- Degree-distribution-pinned to the combined H/Q target-row profile (methods.tex L22: "Primary probes were degree-distribution-pinned to the full compound-target row degree profile (10 Hyperforin rows plus 62 Quercetin rows)")
- Random degree-matched sets, not real drug-target sets with biological coherence

This means the benchmark characterizes the behavior for random sets with the *same degree profile* as these two compounds. It does NOT characterize behavior for random drugs more broadly — the degree profile of H/Q targets may be atypical. The paper partially addresses this with uniform-probe and non-DILI-profile controls (results.tex L46), but these only vary the degree profile, not the set coherence.

A reviewer would note: real drug targets are not random degree-matched sets. They tend to cluster in specific functional modules, share interaction partners, and have correlated network positions. The benchmark's randomization destroys this structure, so it may underestimate or overestimate reversal rates for real drugs.

**Classification: LIMITATION ONLY.** The benchmark largely addresses the statistical n=2 concern. The ecological validity concern (random probes vs. real drug targets) is a secondary limitation that the paper partially acknowledges.

---

## ATTACK 12: Network-universality is not claimed, but liver-only scope is under-communicated

**Claim under attack:** The generality of the operating-regime findings.

**Attack:** The paper states "the rate of reversal is a property of the DILI module's distance geometry and is not claimed to be network-universal" (discussion.tex L15). Good — this is properly hedged. The paper also shows the |T|^{-1/2} exponent is stable across the DILI module and size-matched pseudo-modules (slope_DILI = -0.495, slope_pseudo_mean = -0.498; operating_regime_summary.csv L2).

However, all these modules exist within the *same* liver-expressed LCC of the STRING ≥900 interactome. The paper has not demonstrated that:
- The exponent holds in other tissues (brain, heart, kidney interactomes)
- The reversal rates are similar in other disease modules
- The δ_max envelope is comparable in other network contexts

The abstract and introduction could be misread as claiming broader generality than demonstrated. The paper should more prominently state that all findings are within a single liver-expressed interactome and a single DILI module, with pseudo-module controls showing internal consistency but not external generalizability.

**Classification: ALREADY HANDLED in the limitations, but the abstract and conclusion could be more prominently hedged.** Upgrade to LIMITATION ONLY for communication clarity.

---

## ATTACK 13: "Material rank reversal is conditional and rare" — the data supports this but the framing is asymmetric

**Claim under attack:** The paper's central narrative about rank reversal.

**Attack:** The data indeed shows conditional reversals are rare (0–0.39%). The unconditional directional reversal rate at R=6.2 is 6.5%, which is notably higher. The paper distinguishes these correctly.

However, there's a framing asymmetry: the paper emphasizes that *conditional* reversal is rare (requiring a material margin AND an unusually proximal smaller set), but the unconditional dissociation (Z-scores ordering differently from d_c) occurs in 6.5% of pairs at R=6.2 and 11.9% in terms of rank discordance. For a typical drug comparison scenario (where you don't know a priori whether the smaller set is materially closer), the Z-score and d_c rankings disagree ~12% of the time. That's not negligible.

The paper's framing makes the problem seem rarer than it is for the typical use case. A user comparing two drugs doesn't condition on δ₀ — they just compare Z-scores. The unconditional discordance rate is the practically relevant number for a naive user, and ~12% is high enough to matter.

**Evidence:** operating_regime_reversal.csv L7: at R=6.2, `uncond_rank_discord` = 0.119398 (11.9%), `uncond_directional_reversal` = 0.065026 (6.5%).

**Classification: MAJOR.** The paper should give equal prominence to unconditional discordance rates and frame the practical risk more appropriately: "In ~12% of cross-size comparisons, the Z-score ranking disagrees with the raw-effect ranking."

---

## ATTACK 14: Guney two-sided null attenuation weakens but does not invalidate the core claim

**Claim under attack:** The robustness of the Z-score dissociation.

**Attack:** Under the Guney two-sided null (randomizing both targets and disease module), the Z-scores attenuate to near-parity: Hyperforin Z = -3.55, Quercetin Z = -3.66 (results.tex L94, results.tex Table 3). The difference is only 0.11 Z-units, compared to 1.58 under the fixed-disease null and 1.25 under the Guney fixed-disease null.

The paper argues this is expected: "the interpretation is consistent: Hyperforin is the topologically closer compound in every construction, while its evidence ranking relative to Quercetin depends on the null — strongest when the actual DILI module is held fixed, the configuration relevant to comparing two compounds against one disease" (results.tex L94).

This defense is logically sound: when comparing two drugs against the *same* disease, the fixed-disease null is the correct reference. The two-sided null answers a different question (is this drug-disease pair closer than random drug-disease pairs?). 

However, a reviewer might counter: the two-sided null is the canonical Guney construction and is more conservative. If the dissociation vanishes under the canonical null, the practical concern is diminished. The fixed-disease null is legitimate but less standard.

The paper also notes that even under the two-sided null, the null SD ratio is 2.37 vs. expected 2.49 — the shrinkage mechanism still operates, but the null-mean adjustment partially compensates.

**Classification: LIMITATION ONLY.** The paper acknowledges and discusses this appropriately. The fixed-disease null is well-justified for the cross-compound comparison use case. But the paper should more prominently note that under the canonical two-sided null, the effect essentially disappears.

---

## ADDITIONAL ATTACKS (Beyond the 14 specified)

---

## ATTACK 15: The STRING ≥900 threshold choice is under-justified

**Claim under attack:** The primary analysis threshold.

**Attack:** The paper uses STRING ≥900 as the primary threshold but reports ≥700 as a robustness check. At ≥700, the Z-score ranking *reverses*: Hyperforin Z = -6.04, Quercetin Z = -5.46 (supplementary/pipeline data, shortest_path_permutation_results.csv L2-L3). At ≥900, it flips back: Hyperforin -3.86, Quercetin -5.44.

This means the core finding (Z-score dissociation with Hyperforin weaker) is threshold-dependent. The paper's abstract emphasizes the ≥900 result without noting that at ≥700 the ranking goes the other way. The methods section mentions "the order flips at ≥900" (results.tex L8) but the abstract doesn't.

A reviewer would ask: why is ≥900 primary? Is it because that threshold produces the more interesting result (Hyperforin closer but less significant)? The ≥700 result (Hyperforin closer AND more significant) would be less noteworthy. The paper should justify the primary threshold choice (e.g., ≥900 is more stringent, removes lower-confidence edges) and more prominently report the threshold sensitivity.

**Classification: MAJOR (but fixable).** Justify the primary threshold choice and report the ≥700 reversal symmetrically in the abstract.

---

## ATTACK 16: The R²=0.9999 for the null-SD scaling is suspiciously perfect

**Claim under attack:** The precision of the |T|^{-1/2} fit.

**Attack:** The operating regime benchmark reports R² = 0.9999 for the log-log fit of σ_null vs. |T|. This is a 4-nines R² on 10 data points. While the LLN mechanism predicts near-perfect linearity, R² = 0.9999 is extremely high for any empirical measurement. It suggests that:
- The probe sampling is so large (20,000 per size) that sampling error is negligible
- The degree-pinning controls eliminate virtually all variance not explained by size
- The network's distance geometry is highly regular at this scale

The paper should explicitly note that this near-perfect fit is partly an artifact of the large N (20,000) and the controlled degree-pinning, not a universal property. For per-compound permutation nulls (N=1,000), the fit would be noisier.

**Classification: LIMITATION ONLY.** The R² is real but its interpretation should be caveated — it reflects the experimental design (large controlled probes), not a universal network property.

---

## ATTACK 17: p-values are floor-limited and uninformative

**Claim under attack:** The statistical significance reporting.

**Attack:** All permutation p-values are reported as p < 0.001 (the floor at n=1,000, using the conservative (r+1)/(n+1) convention). Both compounds are "significant" at both thresholds for both metrics. The p-values are therefore uninformative — they tell us only that both compounds are closer to the DILI module than ≥999 of 1,000 random sets. This is not surprising for compounds known to interact with DILI-relevant biology.

The paper does not overinterpret the p-values (it uses Z-scores as the primary magnitude report), but the p < 0.001 reporting creates a false impression of strong evidence where the floor is an artifact of the permutation count. The paper should either (a) increase n to get meaningful p-values, or (b) more clearly note that p < 0.001 is the floor and not a precise estimate.

**Classification: LIMITATION ONLY.** The paper correctly uses Z-scores as primary, but the p-value floor should be more prominently caveated.

---

## ATTACK 18: The chemical-similarity negative control is weak

**Claim under attack:** "Structural confounding is excluded."

**Attack:** The paper reports maximum Tanimoto similarity to DILIrank reference drugs < 0.4 for both compounds (results.tex L113). This is below the Maggiora (2014) structural-analogue threshold of 0.4. However:

- The 0.4 threshold is for *structural analogues*, not for excluding any structural signal. Compounds with Tanimoto < 0.4 can still share pharmacophores relevant to DILI.
- The similarity analysis only addresses whether the compounds *resemble known DILI drugs*, not whether they have DILI-relevant chemical features.
- Both compounds are natural products with well-characterized bioactivity profiles. The relevant question is not "do they look like DILIrank drugs?" but "do their known biological activities predict DILI risk?" — which the network analysis attempts to address.

The chemical-similarity control is appropriate but its conclusion ("structural confounding is excluded") overstates what a Tanimoto cutoff can establish.

**Classification: LIMITATION ONLY.** The similarity analysis is correct as far as it goes but its interpretive conclusion is slightly overstated.

---

## SUMMARY OF ATTACK CLASSIFICATIONS

### FATAL (paper-killing if unaddressed)
| # | Attack | Target |
|---|--------|--------|
| A8 | 62% direct overlap undermines network narrative | Biological case study |
| A9 | Target-set provenance asymmetry | Biological comparison |

### MAJOR (fixable but requires substantial work)
| # | Attack | Target |
|---|--------|--------|
| A1 | |T|^{-1/2} law is algebraically trivial | Framing/novelty claims |
| A3 | Calibration Z vs. Guney Z conflation risk | Benchmark-to-compounds bridge |
| A4 | δ₀=0.3 threshold looks cherry-picked | Conditional reversal analysis |
| A5 | "91st percentile" ≠ "unusually proximal" | Language precision |
| A7 | Perturbation efficiency unvalidated, α-sensitive | Core proposed metric |
| A10 | Missing DILIrank benchmarking | Metric validation |
| A13 | Unconditional discordance (12%) under-emphasized | Practical risk framing |
| A15 | STRING ≥900 threshold under-justified | Primary analysis choice |

### LIMITATION ONLY (acknowledged or minor)
| # | Attack | Target |
|---|--------|--------|
| A2 | Benchmark adds real but limited information | Empirical contribution |
| A6 | Extremely rare reversals | Practical significance |
| A11 | "Only two compounds" partially addressed | Generalizability |
| A12 | Liver-only scope under-communicated | Generality claims |
| A14 | Guney two-sided null attenuation | Null-dependence |
| A16 | R²=0.9999 suspiciously perfect | Fit interpretation |
| A17 | p-values floor-limited | Significance reporting |
| A18 | Chemical-similarity control weak | Structural confounding |

### ALREADY HANDLED
| # | Attack | Target |
|---|--------|--------|
| (A12) | Network-universality not claimed | Generality |

### FALSE CONCERN
| # | Attack | Target |
|---|--------|--------|
| — | Multiple testing / selective reporting | The paper reports negative results transparently |

---

## CRITICAL RECOMMENDATIONS (Priority-Ordered)

1. **Reframe the core contribution** (addresses A1, A2): The paper's novel contribution is NOT discovering the |T|^{-1/2} law (which is algebraic) but (a) empirically confirming it in a realistic network context, (b) quantifying the resulting interpretive risk via the operating-regime benchmark, and (c) providing a framework (perturbation efficiency + decomposition) for transparent cross-compound comparison. Rewrite the abstract and introduction to make this distinction explicit.

2. **Demote the biological case study** (addresses A8, A9): The H/Q comparison should be reframed as an "illustrative motivated example" rather than a finding. The provenance asymmetry (literature vs. ChEMBL) and the direct-overlap confound (62%) mean the biological claim is weak. The paper's value is methodological, not biological.

3. **Add DILIrank pilot validation** (addresses A7, A10): Even a small-scale validation of perturbation efficiency against DILIrank 2.0 classification would transform the paper from "proposing a metric" to "validating a metric." If infeasible, frame perturbation efficiency as a candidate requiring validation.

4. **Fix the threshold analysis** (addresses A4): Replace the two-point δ₀ analysis with a continuous curve of reversal rate vs. δ₀. Justify the "material margin" threshold on substantive grounds, not post-hoc alignment with the H/Q margin.

5. **Correct the "unusually proximal" language** (addresses A5): Replace with "at the 91st percentile of random probe-pair margins" or similar precise language.

6. **Report unconditional discordance prominently** (addresses A13): The ~12% unconditional rank discordance is the practically relevant number for most users. Give it equal billing with conditional reversal rates.

7. **Justify the ≥900 threshold** (addresses A15): Explain why ≥900 is primary and report the ≥700 reversal symmetrically in the abstract.

8. **Bridge the benchmark to real compounds** (addresses A3): Explicitly compare calibration null σ values with the real compounds' Guney null σ values, and discuss any discrepancies.

---

## FINAL VERDICT

This paper identifies a real and underappreciated methodological issue in network medicine: that Z-score magnitudes can mislead as cross-compound effect-size rankings under target-count asymmetry. The statistical mechanism is sound, the operating-regime benchmark is well-constructed (modulo the threshold issue), and the paper is commendably transparent about its own limitations — perhaps too transparent, as the honesty about the leakage decomposition and provenance asymmetry substantially weakens the biological case study.

The paper would benefit from:
- A more modest framing (methodological contribution, not biological discovery)
- Explicit separation of algebraic mechanism from empirical confirmation
- Pilot validation of perturbation efficiency
- More precise language about effect sizes and percentiles
- Symmetric reporting of threshold sensitivity and unconditional discordance

**The paper should survive peer review after major revisions**, but the current framing overstates both the novelty of the mechanism and the strength of the biological case study. The methodological framework (report effect size + evidence + decomposition) is the paper's lasting contribution.

---

*Agent H — Statistical Red-Team Review — Complete.*

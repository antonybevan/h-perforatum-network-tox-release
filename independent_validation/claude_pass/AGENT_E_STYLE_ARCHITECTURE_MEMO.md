# AGENT E — Guney/Menche Style Architecture Memo

## 1. How Guney Introduces Its Method Without Sounding Defensive

Guney et al. (2016, *Nature Communications*) introduces the proximity Z-score through a sequence of positive, purposeful statements rather than preemptive defenses. The method is presented as a **solution to a natural problem**, not as a rebuttal to critics:

| Guney technique | Example from Guney et al. | Our manuscript's contrasting approach |
|---|---|---|
| **Method as solution** | "To quantify the relationship between a drug and a disease, we defined the network-based proximity..." | "We therefore report an effect size alongside the evidence Z-score" — reads as a concession, not a choice |
| **Positive framing** | "We found that..." / "The proximity measure correctly identified..." | "These statements are not contradictory"; "Our findings do not contradict..." — frames everything against a potential objection |
| **No "rather than"** | Guney never says "rather than previous approaches which failed to..." | 15+ instances of "rather than" across sections (Abstract: "rather than calling them into question"; Discussion: "rather than overturning it"; Introduction: "rather than a property of two compounds alone") |
| **No preemptive denials** | Guney does not say "We do not claim that..." or "This is not a..." | 20+ instances of "we do not claim," "not a predictor," "not claimed," "not an artifact," "not interpreted as" |
| **Calm equation introductions** | "The proximity between drug T and disease D is defined as..." | Equations are introduced cleanly (Eq. 4–6 are fine), but contextualized by caveats ("the ranking is the robust feature; cardinal ratios should not be interpreted...") |

**Core principle:** Guney states what it DID. Our manuscript spends substantial word count stating what it DID NOT DO, what it DOES NOT CLAIM, and what something IS NOT. This is the hallmark of reviewer-response residue — sentences written to placate an imagined critic rather than to advance the scientific argument.

---

## 2. Structural Elements Menche Uses That Our Paper Lacks

Menche et al. (2015, *Science*) demonstrates a disciplined architecture that our manuscript could adopt:

### A. Abstract: Problem → Approach → Result → Implication (no caveats)

| Menche structure | Our abstract |
|---|---|
| Opens with the biological question | Opens with "Because the null standard deviation shrinks..." — starts by explaining a problem rather than stating a finding |
| States the method | States the method, but ends with "These findings clarify how to interpret... rather than calling them into question" — a defensive coda |
| Closes with implication, no hedging | Contains caveats about "rare for generic target sets," "rather than a property of two compounds alone," and "rather than calling them into question" |

### B. Introduction: Known → Gap → Our Approach (no contrast with prior work's failures)

Menche:
1. What is known (disease module, network medicine)
2. What is unknown / the open problem
3. Here is our approach

Our Introduction:
1. Background on proximity Z-scores
2. ASA statement about p-values (defensive framing)
3. "The question we address is therefore narrow and practical" — defensive scope-narrowing
4. Extensive justification of compound choice, including what they are NOT (not representative, not exposure-matched, not outcome-level toxicity ground truth)
5. "We do not claim the shared botanical origin controls the network computation — it does not" — explicit denial

### C. Results: Positive findings, not findings-plus-disclaimers

Menche opens each Results subsection with a finding. Our Results open with findings but then immediately append disclaimers:
- §2.1: Finding stated, then "These statements are not contradictory" — preemptive
- §2.3: Finding stated, then "We make no claim that such reversals are common, and none about toxicity"
- §2.4: Finding stated, then "cardinal ratios should not be interpreted as absolute biological constants"

### D. Discussion: Limitations localized to one section

Menche places limitations in a dedicated Limitations/Discussion section. Our manuscript scatters them through:
- **Abstract:** "rather than a property of two compounds alone"
- **Introduction:** "we make no population-level performance or toxicity-prediction claim"
- **Results:** "We make no claim that such reversals are common, and none about toxicity"; "this excludes structural confounding but not toxicity risk per se"
- **Discussion:** The Limitations subsection (correct placement), but also the opening paragraph ("rather than overturning it"), paragraph 2 ("does not itself escape"), paragraph 3 ("do not contradict"), paragraph 4 ("not a predictor," "not a toxicological outcome," "not only size," "do not eliminate it," "not claimed," "not a population of drugs")

**Missing structural element:** Our Discussion lacks a clean "Relationship to Prior Work" that simply states what prior work found and how our work extends it without the "does not contradict" framing. The current Discussion §3.1 says "Our findings do not contradict Guney et al." — this is literally the first sentence. Menche would say: "Guney et al. established proximity Z-scores as per-compound evidence statistics. Here we examine the distinct regime of cross-compound ranking under target-count asymmetry."

---

## 3. Reviewer-Response Residue: 15 Sentences That Read Like They Were Written to Placate Reviewer 2

These sentences serve no purpose for a reader who approaches the paper on its own terms. They exist only to preempt objections:

### Abstract
1. **"rather than a property of two compounds alone"** — defends the generality of the claim before it's made
2. **"These findings clarify how to interpret network-proximity statistics under target-count asymmetry rather than calling them into question"** — preemptively assures Guney et al. loyalists

### Introduction
3. **"The role of the case study is therefore to instantiate the failure condition transparently, not to estimate its prevalence"** — defines the study by what it is NOT
4. **"We select Hyperforin and Quercetin as a deliberately diagnostic, high-contrast pair, not a representative or exposure-matched one"** — tells the reader what the pair isn't
5. **"The mechanistic contrast is a liver-relevant positive control, not an outcome-level toxicity ground truth"** — defensive about biological interpretation
6. **"We do not claim the shared botanical origin controls the network computation — it does not"** — explicit denial, with a dash-em-dash for emphasis
7. **"we make no population-level performance or toxicity-prediction claim"** — preemptive disclaimer closing the Introduction

### Results
8. **"These statements are not contradictory; they answer different questions"** — the reader hasn't yet accused them of contradiction
9. **"We make no claim that such reversals are common, and none about toxicity"** — two denials in one sentence
10. **"This does not contradict the d_c result because S_AB also depends on within-set compactness"** — anticipates a contradiction the reader may not have noticed
11. **"this excludes structural confounding but not toxicity risk per se"** — the "but not" formula: concedes a limitation while denying a confound

### Discussion
12. **"Our results refine the use of network-proximity statistics rather than overturning it"** — opening sentence of Discussion, a peace offering
13. **"Our findings do not contradict Guney et al."** — another peace offering, first sentence of "Relationship to prior work"
14. **"We do not claim that random-walk influence is a superior proximity statistic; neither d_c nor d_k is the object of our argument"** — triple denial
15. **"We therefore do not claim that Hyperforin is uniquely high-leverage, only that its targets are, on average, somewhat better positioned..."** — "therefore do not claim" followed by a hedged positive

**The common pattern:** Each sentence follows the structure "X is true, but this does NOT mean Y." The reader is constantly told what NOT to conclude. In Guney/Menche style, the text simply states what IS true and trusts the reader.

---

## 4. How the Introduction Should Be Rebuilt to Sound Like Original Research

### Current architecture (defensive):
1. Background + ASA caveat about p-values
2. "The question we address is therefore narrow and practical" (scope-narrowing)
3. Why case study + DILI justification
4. Compound selection with 6+ denials (not representative, not exposure-matched, not outcome-level, do not claim, does not, not matched)
5. Three contributions (with caveat in contribution #3)

### Proposed Guney/Menche architecture (affirmative):

**Paragraph 1 — The known:**
> Network-based drug prioritization maps compound targets onto the human interactome and scores their proximity to disease-associated protein modules. The field standard, the proximity Z-score, calibrates each compound against a size- and degree-matched null, producing a standardized evidence statistic that is valid for per-compound inference.

**Paragraph 2 — The gap:**
> Comparing Z-score magnitudes across compounds, however, introduces a distinct requirement: the Z-score must be monotone in the underlying topological effect. When target counts differ sharply, the larger set's null standard deviation shrinks as |T|^−1/2 — a consequence of the law of large numbers on an averaged statistic — so that a compound with weaker raw proximity can register stronger standardized evidence. Whether this non-monotonicity materializes in practice, and under what conditions, has not been systematically examined.

**Paragraph 3 — Our approach:**
> We address this with a controlled stress test in a liver-expressed interactome. We select two Hypericum perforatum constituents — Hyperforin (10 targets) and Quercetin (62 targets) — as a deliberately high-contrast pair that satisfies explicit criteria: a large, real target-set asymmetry, a shared botanical context, contrasting and well-characterized mechanisms, and adequate curatable target evidence. The drug-induced liver injury (DILI) module serves as the disease reference, chosen because its inclusion of cytochrome-P450, transporter, and nuclear-receptor genes exposes a second, coupled question: when do direct target–disease overlaps inflate apparent network influence? We complement the pair with a degree-controlled benchmark that characterizes the operating regime in which rank reversal can occur, and we introduce perturbation efficiency — mean per-target random-walk influence — as a complementary effect-size ranking.

**Paragraph 4 — What we found (roadmap):**
> We find that proximity Z-score magnitude and raw closest distance can dissociate under target-count asymmetry, trace this to the |T|^−1/2 null-precision law, and show that the law holds across shortest-path, random-walk, and expression-weighted influence alike. A degree-controlled liver-network benchmark confirms the mechanism and reveals that material rank reversal is a located, conditional outcome — rare for generic target sets, realized only when the smaller set is above the 90th percentile of probe-pair margins. On the illustrative pair, perturbation efficiency recovers the expected mechanistic ordering while exposing the direct target–DILI overlap that an uncritical headline number would have conflated with propagated influence.

**What changed:**
- No "we do not claim," "not a predictor," "not representative," "not an outcome-level"
- No "The role of the case study is therefore to instantiate the failure condition transparently, not to estimate its prevalence"
- No "we make no population-level performance or toxicity-prediction claim"
- The gap is stated as an open scientific question, not as a defense of why this study is narrow enough to be valid
- The compound selection is described by what they ARE (criteria they satisfy), not what they ARE NOT
- The DILI module justification is positive ("chosen because...") not defensive

---

## 5. Proposed New Opening Sentence for the Abstract

### Current opening:
> "Network-based proximity prioritises compound–disease relationships by standardising a target–disease distance against a target-size- and degree-matched null to obtain a Z-score. Because the null standard deviation shrinks as the target count grows — a consequence of the law of large numbers for an averaged statistic — one compound can lie closer to a disease module yet receive the weaker Z-score when Z-magnitudes are compared across compounds."

**Problem:** Starts with background, then "Because..." — the second sentence is already explaining why a problem exists rather than stating the finding. It reads like a methods paragraph, not an abstract hook.

### Proposed new opening:
> "When network-proximity Z-scores are compared across compounds with unequal target counts, the evidence ranking can reverse the raw topological effect: the larger set's sharper null standard deviation, which shrinks as |T|^−1/2, can register weaker proximity as stronger evidence. We demonstrate this dissociation using two Hypericum perforatum constituents in a liver-expressed interactome."

**Why this works:**
- Opens with the phenomenon (not background), following the Menche pattern
- No "Because..." — just states what happens
- "We demonstrate" instead of "We therefore report"
- The phenomenon is the finding, not a theoretical concern to be managed

### Alternative (more conservative, still Guney-style):
> "Comparing network-proximity Z-scores across compounds requires the Z-score to be monotone in the underlying topological effect. Under target-count asymmetry, this requirement can fail: the null standard deviation shrinks as |T|^−1/2, so a compound with weaker raw proximity can register stronger standardized evidence. We quantify this dissociation in a controlled liver-interactome stress test and propose perturbation efficiency — mean per-target random-walk influence on the disease module — as a complementary effect-size ranking."

---

## 6. Proposed New Opening Paragraph for the Introduction

### Current opening:
> "Network-based prioritization rests on the disease-module hypothesis: proteins associated with a disease localize in a neighbourhood of the human interactome, and a compound is more likely to act on the disease when its targets fall within or near that neighbourhood. Guney et al. validated this proximity Z-score as a per-pair classifier across 402 known and 18,162 unknown drug–disease associations (mean 3.5 targets per drug) and reported, in their benchmark, no meaningful dependence on the number of targets or their degrees: within each drug's own size-matched null, the standardization removes the dependence that raw distance has on these quantities."

**Problem:** The paragraph is background on Guney, not on the scientific gap. It immediately positions the paper relative to Guney rather than relative to an open question. Then paragraph 2 jumps to the ASA p-value statement, which is a defensive move.

### Proposed new opening:
> "Network-based drug prioritization maps compound targets onto the human interactome and scores their proximity to disease-associated protein modules. The proximity Z-score — the field standard, validated across hundreds of drug–disease pairs — calibrates each compound against a size- and degree-matched null and answers the question: is this compound unusually close to this disease? A distinct question arises when compounds are ranked against each other: does the compound with the stronger Z-score also have the stronger raw topological effect? Under target-count asymmetry, the answer can be no."

**Why this works:**
- Opens with the scientific domain (network-based prioritization), not with Guney's validation
- States the Z-score's purpose positively ("answers the question") rather than defensively
- Introduces the gap as a natural, distinct question — not as a critique of prior work
- No "however," no "unlike previous work," no ASA p-value lecture
- Sets up the paper's contribution as answering a question, not defending against one

**The ASA statement** (currently paragraph 2, line 5) can move to Discussion where it belongs — as context for interpreting results, not as part of the motivation for doing the study.

---

## 7. Defensive Language Density by Section

| Section | Approx. word count | Defensive constructions | Density (per 100 words) |
|---|---|---|---|
| **Discussion** (incl. Limitations) | ~1,000 | 21 | **2.1** |
| **Introduction** | ~700 | 8 | **1.1** |
| **Abstract** | ~250 | 3 | **1.2** |
| **Results** | ~2,000 | 12 | **0.6** |

### The Discussion has the highest defensive language density.

The Discussion's Limitations paragraph (lines 14–16 in discussion.tex) is essentially one continuous string of denials and concessions:

> "not a predictor" → "not a toxicological outcome" → "not only size" → "do not eliminate it" → "limitation rather than resolve" → "future work rather than claimed" → "not claimed to be network-universal" → "not curated drug-target sets" → "not a population of drugs"

This paragraph reads like it was written directly in response to a reviewer comment: "But this is only two compounds, not a predictor, and the target sets have different provenance, and you haven't generalized to a library, and the module might not generalize..."

The Discussion's opening also launches with two peace offerings in the first two paragraphs:
- Line 3: "Our results refine... rather than overturning it"
- Line 11: "Our findings do not contradict Guney et al."

In Guney/Menche style, the Discussion would open with the finding's significance, not with a reassurance that prior work is still valid.

---

## Summary: The Root Cause

The manuscript suffers from **triple-layered defensiveness**: the same caveats appear in Abstract, Introduction, Results, AND Discussion. A reader who encounters the paper receives the following message at least four times:

> "This is a narrow, illustrative, non-predictive, non-representative stress test that does not contradict prior work, does not claim toxicity prediction, and does not claim the effect is common."

This is not how Guney or Menche write. They state what they did, what they found, and what it means. They trust the reader to understand that a two-compound study is illustrative, that a benchmark characterizes a statistic not a population, and that building on prior work does not require explicitly saying "we do not contradict it."

### Recommended surgical fixes:

1. **Abstract:** Remove "rather than calling them into question." Replace "We therefore report" with "We report."
2. **Introduction:** Remove all "not a..." and "we do not claim..." constructions. Convert negative definitions to positive ones.
3. **Results:** Move "We make no claim that such reversals are common, and none about toxicity" and "These statements are not contradictory" to Discussion or delete entirely.
4. **Discussion:** Rewrite the Limitations paragraph in positive language: "This study is a controlled two-compound audit. The framework extends naturally to..." rather than "This is not a predictor. Network influence is not a toxicological outcome."
5. **Discussion opening:** Replace "rather than overturning it" and "do not contradict" with "builds on" and "extends."

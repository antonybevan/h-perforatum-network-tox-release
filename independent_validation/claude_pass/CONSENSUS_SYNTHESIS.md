# CONSENSUS SYNTHESIS — Manuscript Architecture Redesign

**Synthesized from:** Agents A (Network Medicine PI), B (Estimand Architect), D (Biology), E (Style Analyst), F (Scientific Reports Editor)
**Date:** 2026-07-01

---

## 1. What is the paper really about?

> Network-proximity Z-scores are valid evidence statistics, but their magnitude should not be read as a cross-compound effect-size ranking when target counts differ sharply — because the null standard deviation shrinks as |T|^{-1/2} (LLN on an averaged statistic). A degree-controlled operating-regime benchmark characterizes when this can cause material rank reversal. Perturbation efficiency provides a complementary ordinal effect-size ranking. A liver-network worked example demonstrates the framework.

## 2. What should the reader understand after the abstract?

1. Proximity Z-scores are valid per-compound evidence statistics (Guney 2016)
2. Under target-count asymmetry, Z-magnitude can diverge from raw effect-size ranking
3. The mechanism is LLN: σ_null shrinks as |T|^{-1/2}
4. We characterize the regime with a benchmark; Hyperforin/Quercetin is a worked example inside it
5. We recommend reporting an explicit effect size (perturbation efficiency) alongside the Z-score

## 3. What should the Introduction accomplish?

**Not:** Defend the study design, list caveats, explain what the paper is NOT.

**Yes:** Establish network proximity as useful → identify the cross-compound interpretation gap → state our approach (benchmark + worked example + complementary metric).

Structure (4 paragraphs max):
1. Network proximity is validated (Guney) — but Z = evidence, not effect magnitude (ASA)
2. Target-count asymmetry creates an interpretation problem because σ_null ∝ |T|^{-1/2}
3. We characterize this regime (benchmark) and provide a worked liver-network example
4. Contribution statement (3 bullets)

## 4. What should each Results section accomplish?

| Section | Purpose | Current problem |
|---|---|---|
| §2.1 Null-precision law + benchmark | Characterize the statistical mechanism | Currently §2.3, buried after biological case |
| §2.2 Worked example (H/Q) | Locate the pair inside the characterized regime | Currently §2.1, presented as the primary evidence |
| §2.3 Perturbation efficiency | Introduce complementary effect-size ranking | Currently §2.4, OK but needs ordinal caveat moved to Methods |
| §2.4 Direct/propagated | Separate overlap from influence | Currently §2.5, mostly OK |
| §2.5 Guney fidelity | Validate against canonical implementation | Move to §2.5 or Supplementary |
| §2.6 Chemical similarity | Negative control | Move to Supplementary or brief note |

## 5. Defensive phrases to transform (priority ordered)

| Current | Action | Replacement |
|---|---|---|
| "The pitfall we document is interpretive" | Replace | "The phenomenon we characterize arises when..." |
| "rather than calling them into question" | Delete | — |
| "though not itself an established intrinsic hepatotoxin" | Keep 1 instance in Limitations | — |
| "we make no population-level performance or toxicity-prediction claim" | Move to Limitations | — |
| "not a generic outcome" → "located instance" | Already done | — |
| "Our findings do not contradict Guney" | Replace | "Our findings are consistent with Guney's demonstration..." |
| "the comparison is strictly topological" | Delete | Already implicit in the design |
| "we do not claim the shared botanical origin controls the network computation" | Delete | — |

## 6. Structural changes

1. **Reorder Results:** Benchmark first (§2.1), pair second (§2.2)
2. **Cut Abstract by 30%:** Remove defensive qualifiers, focus on findings
3. **Introduction: 4 paragraphs max.** Cut botanical/pharmacokinetic caveats to Methods/SI
4. **Discussion: Cut "rather than" instances by half.** Transform to positive constructions
5. **Limitations: Already strong. Keep as-is.**

## 7. Go/no-go

**GO for narrative rewrite.** The science is sound. The structure and prose need surgical transformation — not copyediting, but architectural reordering and defensive-language removal. All agents agree.

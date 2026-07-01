# DEFENSIVE LANGUAGE TRANSFORMATION MAP

**Auditor:** Hermes Agent (narrative architecture)
**Date:** 2026-07-01
**Principle:** Every defensive phrase must be either deleted, transformed into positive design logic, or placed in Limitations (once).

---

## Transformation Rules

| Class | Action |
|---|---|
| **A** | Keep — scientifically necessary boundary |
| **B** | Move to Limitations section (once, not repeated) |
| **C** | Convert into positive design logic |
| **D** | Delete — reviewer-response residue |
| **E** | Replace with precise estimand language |

---

## Phrase-by-Phrase Audit

### 1. "rather than" — 14 instances (Abstract:2, Introduction:2, Results:2, Discussion:8)

The most overused defensive construction.

| Location | Current | Action | Replacement |
|---|---|---|---|
| Abstract | "rather than a property of two compounds alone" | C | "The benchmark, not the pair alone, characterizes the statistical regime" |
| Abstract | "rather than calling them into question" | D | Delete — this is a concession to Guney that the paper doesn't need to make |
| Introduction | "rather than an established...toxicity ground truth" | C | "Hyperforin was chosen as a mechanistically interpretable positive control for hepatic PXR/CYP induction" |
| Results | "rather than a property of two compounds alone" | C | "The benchmark characterizes the regime; the pair instantiates it" |
| Results | "rather than reflecting a clear topological separation" | D | Replace with: "The propagated advantage is modest" (standalone) |
| Discussion (×8) | Various | Mixed | See below |

Discussion "rather than" audit:
- "refine the use... rather than overturning it" → C: "This study refines how proximity statistics are interpreted"
- "not a new significance statistic but the separate reporting" → E: "The resolution is the separate reporting of effect size"
- "neither d_c nor d_k is the object of our argument" → D: Delete — already implicit
- "reports effect size alongside evidence rather than in place of it" → E: "We recommend reporting effect size alongside the evidence Z-score"
- Others: similar transformations

### 2. "not a predictor" — 1 instance (Discussion)
✅ Correct placement. Keep in Limitations. Action: **A**

### 3. "we make no claim" — 1 instance (Results)
In operating-regime section. Action: **C** → "The benchmark characterizes the statistic; it does not model toxicity outcomes"

### 4. "not a generic outcome" — 1 instance (Results)
Already transformed to "located instance of a characterized regime." Action: **D** (already good)

### 5. "does not contradict" — 1 instance (Discussion)
Referring to Guney. Action: **C** → "Our findings are consistent with Guney et al.'s demonstration that proximity Z-scores provide calibrated per-pair evidence"

### 6. "not claimed" — 1 instance (Discussion)
"not claimed to be network-universal." Action: **C** → "These findings are derived from the liver-expressed interactome; extension to other tissues requires additional study"

### 7. "we do not claim" — 2 instances (Introduction, Discussion)
Introduction: "We do not claim the shared botanical origin controls the network computation" Action: **D** (already constrained by context)
Discussion: "We therefore do not claim that Hyperforin is uniquely high-leverage" Action: **C** → "Hyperforin's targets are better positioned than the mean of size-matched comparators, with overlapping upper tails"

### 8. "not itself" — 2 instances (Discussion)
"not itself an established intrinsic hepatotoxin" — appears once now (was reduced from 8+). Action: **B** — Keep in Discussion, remove from elsewhere.

### 9. "is illustrative" — 2 instances (Abstract, Introduction)
This is our addition. Correct framing. Action: **A**

### 10. "no population-level" — 1 instance (Introduction)
Action: **C** → "The pair was selected as a diagnostic contrast, not a representative sample. Generalization requires population-level benchmarking (see Limitations)."

### 11. "we identify as a limitation" — 1 instance (Discussion)
Correct placement. Action: **A**

### 12. "not a replacement" — implicit
"complements the Z-score rather than replacing it" — fine. Action: **A**

### 13. "not yet" — none found ✅

---

## Structural Recommendations

### Abstract: Remove "rather than calling them into question"
This is a Guney concession that belongs in Discussion, not Abstract. The abstract should end with what the paper DOES, not what it doesn't do.

### Introduction: Convert the defensive first paragraph
Current: "Network-based prioritization rests on... A Z-score, however, answers a specific question... the ASA cautions..."
Better: "Network-proximity Z-scores provide calibrated per-compound evidence against degree-matched nulls [Guney 2016]. Because the Z-score denominator shrinks with target count (a consequence of the law of large numbers for an averaged statistic), Z-magnitude alone can mislead as a cross-compound effect-size ranking when target counts differ sharply. We characterize this interpretive regime and propose a complementary effect-size scale."

### Results: Operating-regime benchmark should lead
Move §2.3 BEFORE §2.1. The benchmark establishes the statistical mechanism; the biological pair illustrates it. Current order reads like: "Here's a weird thing with these two compounds → oh by the way here's why it happens." Should read: "Here's the statistical mechanism → here's where it matters → here's a worked example."

### Discussion: Cut "rather than" by half
8 instances is too many. Transform 4 to positive constructions, keep 4 that are genuinely clarifying contrasts.

### Limitations: Already strong, keep as-is
The Limitations subsection is well-structured and honest. Do not change.

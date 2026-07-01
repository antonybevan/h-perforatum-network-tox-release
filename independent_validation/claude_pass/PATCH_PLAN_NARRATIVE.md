# PATCH PLAN — Narrative Architecture Rewrite

**Date:** 2026-07-01
**Principle:** Surgical edits only. No science changes. Every edit traces to a specific agent finding.

---

## PATCH 1: Abstract — Cut defensive language, sharpen findings

**File:** `manuscript/sections/abstract.tex`
**Problem:** 310 words, reads like a defense. Contains caveats that belong in Discussion.
**Changes:**
- Cut to ~200 words
- Remove "rather than calling them into question" (Agent E, F)
- Remove "though not an established intrinsic hepatotoxin" (Agent D: move to Limitations)
- Remove "In this illustrative case" → Just state the finding
- Remove "rather than a property of two compounds alone" (Agent A)
- Keep: LLN framing, benchmark, PE, unconditional discordance
- End with implication, not caveat
**Risk:** Low. No numbers change.
**Verification:** `verify_numbers.py` may need text check update.

---

## PATCH 2: Title — Consider shortening

**File:** `manuscript/main.tex` (\\title{})
**Problem:** 22 words. Scientific Reports prefers <15.
**Option A (recommended by Agent F):** "Effect size versus statistical evidence in network-proximity rankings under target-count asymmetry"
**Option B (keep liver):** "Target-count asymmetry can reverse network-proximity evidence rankings: a liver-interactome demonstration"
**Risk:** Low. No numbers change.
**Decision:** Author choice.

---

## PATCH 3: Introduction — Rebuild as 4 paragraphs

**File:** `manuscript/sections/introduction.tex`
**Problem:** 11 paragraphs, 7 caveats in ¶9 alone. Reads like reviewer response.
**Changes:**
- ¶1: Network proximity is validated (Guney, Menche). Z-score = evidence, not effect magnitude.
- ¶2: Target-count asymmetry creates interpretation problem. LLN mechanism.
- ¶3: Our approach: benchmark characterizes regime; H/Q is worked example inside it; PE is complementary metric.
- ¶4: Contribution bullets (3 max).
- Move botanical caveats (shared source, exposure, curation asymmetry) to Methods §2.1
- Move hepatoprotective Quercetin framing to Methods (Agent D)
- Remove "we do not claim the shared botanical origin controls the network computation"
- Remove "the comparison is strictly topological"
**Risk:** Medium. Restructures introduction but preserves all facts.
**Verification:** `verify_numbers.py` text checks.

---

## PATCH 4: Results — Reorder sections

**File:** `manuscript/sections/results.tex`
**Problem:** Biological pair leads; benchmark reads as post-hoc justification.
**Changes:**
- §2.1 (new): Null-precision law + operating-regime benchmark (currently §2.2 + §2.3 merged)
- §2.2 (new): Hyperforin/Quercetin as located instance (currently §2.1, reframed)
- §2.3 (new): Perturbation efficiency (currently §2.4)
- §2.4 (new): Direct/propagated decomposition (currently §2.5)
- §2.5 (new): Guney fidelity (currently §2.6)
- §2.6 (new): Chemical-similarity control (currently §2.7, or move to Supplementary)
- Add transition sentence between benchmark and pair: "The operating regime characterized above defines the conditions under which Z-magnitude and raw-distance rankings can diverge. We now present a biologically interpretable pair that falls within this regime..."
**Risk:** HIGH. Requires renumbering all \\ref{} and \\label{}. Must rebuild PDF and verify all cross-references.
**Verification:** Full LaTeX rebuild, cross-reference audit, verify_numbers.py.

---

## PATCH 5: Results text — Transform defensive language

**File:** `manuscript/sections/results.tex`
**Changes:**
- "The pitfall we document" → "The phenomenon we characterize" (Agent A)
- "These statements are not contradictory" → Delete (Agent E: let the statements speak)
- "We make no claim that such reversals are common, and none about toxicity" → "The benchmark characterizes the statistic; it does not model toxicity outcomes" (Agent A: positive construction)
- "does not contradict" → "is consistent with" (Agent A, E)
- "a size-normalised effect-size ranking" → keep (already fixed)
- "cardinal ratios should not be interpreted" → keep (already fixed)
**Risk:** Low. Prose only.

---

## PATCH 6: Discussion — Cut "rather than" by half

**File:** `manuscript/sections/discussion.tex`
**Changes:**
- "refine the use... rather than overturning it" → "This study refines how proximity statistics are interpreted" (Agent A)
- "The pitfall we document is interpretive" → "The phenomenon we characterize is interpretive" (Agent A)
- "Our findings do not contradict Guney" → "Our findings are consistent with Guney's demonstration" (Agent E)
- "We therefore do not claim that Hyperforin is uniquely high-leverage, only that its targets are, on average, somewhat better positioned than the mean of size-matched comparators while overlapping their upper tail, and above a global degree-matched background" → "Hyperforin's targets are better positioned than the mean of size-matched comparators (above the 99.9th percentile of a degree-matched background), with overlapping upper tails." (Agent A)
- "not a predictor" → keep in Limitations (correct placement)
- Move hepatotoxin disclaimer to Limitations only (remove from Discussion ¶1)
**Risk:** Low-Medium. Prose only, but needs careful re-read.

---

## PATCH 7: Introduction — Drop Quercetin hepatoprotective framing

**File:** `manuscript/sections/introduction.tex`
**Change:** "widely discussed for antioxidant and hepatoprotective biology" → "a high-target-count comparator from the same botanical source" (Agent D)
**Risk:** Low. Removes an implicit good-vs-bad contrast.

---

## PATCH 8: Discussion — Clean Relationship to Prior Work

**File:** `manuscript/sections/discussion.tex`
**Change:** First sentence: "Our findings do not contradict Guney et al.; they identify an interpretive regime their study design did not stress-test." → "Guney et al. established proximity Z-scores as calibrated per-pair classifiers. Here we characterize the distinct regime of cross-compound ranking under target-count asymmetry, where the |T|^{-1/2} dependence of σ_null becomes relevant." (Agent E)
**Risk:** Low. Same facts, different posture.

---

## PATCHES NOT APPLIED (deferred)

- **Reorder Results sections** (PATCH 4): Requires renumbering all LaTeX labels. HIGH risk. Defer to author decision.
- **Title change** (PATCH 2): Author preference.
- **Move Guney fidelity + chemical similarity to Supplementary** (Agent F suggestion): Requires restructuring. Defer.

---

## EXECUTION ORDER

1. PATCH 3 (Introduction rebuild) — highest impact
2. PATCH 1 (Abstract) — most visible
3. PATCH 5 (Results defensive language)
4. PATCH 6 (Discussion "rather than")
5. PATCH 7 (Quercetin framing)
6. PATCH 8 (Relationship to Prior Work)
7. PATCH 4 (Results reorder) — only if author approves
8. PATCH 2 (Title) — only if author approves

## VERIFICATION AFTER EACH PATCH

```bash
cd manuscript && pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex main && pdflatex main
cd .. && .venv/bin/python3 verify_numbers.py
```

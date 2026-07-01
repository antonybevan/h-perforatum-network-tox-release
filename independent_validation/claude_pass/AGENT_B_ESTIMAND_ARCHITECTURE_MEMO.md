# AGENT B — Estimand Architecture Memo

**Role:** Mathematical/Statistical Estimand Architect  
**Date:** 2026-07-01  
**Paper:** "Separating effect size from statistical evidence in network-proximity rankings under target-count asymmetry"  
**Sources read:** `manuscript/sections/results.tex`, `manuscript/sections/methods.tex`, `AGENTS.md`, `STATISTICAL_LOGIC_AUDIT.md`

---

## Executive Summary

The current Results section introduces estimands in a **defensive order**: it starts with a "problem" (the H/Q dissociation), explains the mechanism, builds a benchmark to justify the mechanism, then introduces an alternative metric (PE). A mathematical statistician would restructure this as a **positive, definition-first development**: define the estimands cleanly, characterize their mathematical properties algebraically, then locate the worked example within the characterized regime.

**Key recommendation:** Restructure Results into four phases — (A) Definition, (B) Mathematical Characterization, (C) Worked Illustration, (D) Mechanistic Decomposition. The operating-regime benchmark leads; the biological pair follows as a located instance. The $|T|^{-1/2}$ law is presented as expected LLN behavior confirmed empirically, not as a discovery. PE is introduced alongside $d_c$ as a complementary effect-size lens, not as a fix.

---

## 1. Should the estimands be introduced in a different order?

**Yes.** The current order creates a defensive narrative arc:

```
Current (defensive):
  §1: "Look, they rank differently!" (problem statement)
  §2: "Here's why — LLN" (explanation/justification)
  §3: "And it's not just this pair — benchmark confirms" (defense)
  §4: "Here's an alternative metric (PE)" (solution)
  §5: "But actually it's mostly direct overlap" (caveat)
  §6: "And we're faithful to Guney" (credibility)
  §7: "Also, not a chemical-similarity artifact" (negative control)
```

This arc says: "We found a problem, we explain it, we defend it, we offer a fix, we hedge." Every section after §1 reads as a response to an anticipated objection.

**Recommended order (mathematical-statistician's positive development):**

```
Phase A — DEFINITION (§1):
  §A1: Raw proximity d_c (topological effect size)
  §A2: Proximity Z = (d_c − μ)/σ (standardized evidence)
  §A3: Perturbation efficiency E (complementary effect-size ranking)
  → All three are introduced neutrally as valid statistical objects.
  → The Calibration-Z vs Guney-Z distinction is made HERE.

Phase B — MATHEMATICAL CHARACTERIZATION (§2):
  §B1: |T|^{-1/2} law — null SD shrinkage for any mean-based statistic
  §B2: δ_max — algebraic consequence of solving Z_L = Z_S under the |T|^{-1/2} law
  §B3: Operating-regime benchmark — empirical confirmation & regime mapping

Phase C — WORKED ILLUSTRATION (§3):
  §C1: Hyperforin/Quercetin pair located within the characterized regime
  §C2: The pair is at the 91st percentile of probe-pair margins, inside δ_max
  → The pair illustrates the regime; it does not define it.

Phase D — MECHANISTIC DECOMPOSITION (§4):
  §D1: Direct overlap — steady-state mass on T∩D
  §D2: Propagated influence — E − direct (leave-one-out)
  §D3: The propagated advantage is modest (1.5×); direct overlap dominates

Phase E — ROBUSTNESS (§5):
  §E1: Guney fidelity check
  §E2: Chemical-similarity negative control
```

This order makes the paper say: "Here are the statistical objects. Here are their mathematical properties. Here is an example that illustrates those properties. Here is a mechanistic refinement. Here are robustness checks."

---

## 2. Should the operating-regime benchmark lead BEFORE the biological case?

**Yes, unequivocally.** The current structure is:

> "The dissociation above follows from a general property... before introducing that effect size, we first test whether the statistical mechanism underlying the dissociation extends beyond this pair." (Results, lines 26–27)

This framing is defensive — the benchmark exists to *justify* the pair. The mathematical order is the reverse: characterize the space, then locate objects within it.

**Recommended reframing:**

> "We characterize the operating regime of proximity Z-scores under target-count asymmetry using a 20,000-probe degree-controlled calibration benchmark on the liver LCC. Having mapped this regime — including the $|T|^{-1/2}$ null-precision law and the $\delta_{\max}$ envelope — we then locate the Hyperforin/Quercetin pair as a worked illustration within it."

The benchmark is presented as the primary statistical contribution; the biological pair is an *illustration* of the characterized regime. This is more honest (the pair was chosen post-hoc to illustrate the phenomenon) and more mathematically natural (define the space, then give an example point).

**Practical consequence:** The benchmark subsection (§3 in current numbering) should move to precede the pair introduction. The pair becomes "an illustrative worked example within the characterized regime" rather than "the finding that motivated the benchmark."

---

## 3. Is the $|T|^{-1/2}$ law framed as elegant expected precision rather than discovery?

**Partially — it needs sharpening.** The current text straddles two framings:

- "The dissociation above follows from a general property of averaged statistics." (line 26) — *hints* at LLN but doesn't name it
- "we find $\sigma_{\text{null}} \propto |T|^{-0.48}$ (log–log slope; theoretical $-1/2$)" (line 26) — *discovers* an empirical relationship
- "The null standard deviation scales as $\sigma_{\text{null}} \propto |T|^{-0.499}$ ... indistinguishable from the theoretical $-1/2$" (line 46) — *confirms* the expected law

The LLN framing is correct but appears as an *explanation* of a problem rather than a *characterization* of a property. A mathematician would state the property first, then confirm it.

**Recommended framing:**

> "For any statistic defined as a mean over $|T|$ targets, the Law of Large Numbers implies $\sigma_{\text{null}} \propto |T|^{-1/2}$. This is not a network-specific discovery; it is an expected precision scaling. We confirm it empirically: the log–log slope across ten size points is $-0.499$ (95% CI $[-0.502, -0.495]$, $R^2 = 0.9999$), indistinguishable from the theoretical $-1/2$."

Then add the nuance (per STATISTICAL_LOGIC_AUDIT S1):

> "The terms $\min_d \text{dist}(t,d)$ are not strictly i.i.d. under degree-matching (degree-matching induces weak dependence), so the $-1/2$ exponent is an asymptotic approximation rather than an exact finite-sample identity. The empirical slope of $-0.48$ in the coarser per-target-influence estimate (Table 1) captures this finite-sample deviation, while the large-N probe calibration ($N = 20{,}000$ per size) recovers the asymptotic exponent to high precision."

Also note (per STATISTICAL_LOGIC_AUDIT S3):

> "The $R^2 = 0.9999$ partly reflects the large-$N$ probe design ($N = 20{,}000$ per size point makes sampling error negligible) rather than a universal network property; for per-compound permutation nulls ($n = 1{,}000$), the fit would be noisier."

This framing does three things: (a) states the LLN as the *cause*, not the *finding*; (b) presents the empirical confirmation as a sanity check; (c) acknowledges the approximation and experimental-design artifacts honestly.

---

## 4. Does $\delta_{\max}$ read like a natural consequence of the algebra or a defensive derivation?

**Currently it reads somewhat defensive.** The formula is introduced parenthetically:

> "the maximum raw-distance margin it can overturn is $\delta_{\max}(R) = (\mu_L-\mu_S) + |z_S|\,\sigma_L(\sqrt{R}-1)$ (Fig.~...; this follows by solving $Z_L = Z_S$ for the raw margin $\delta = d_c^L - d_c^S$, using $\sigma_S/\sigma_L = \sqrt{R}$ from the $|T|^{-1/2}$ law)"

The parenthetical "(this follows by solving...)" makes it sound like an afterthought or a justification. The derivation should be presented as a natural algebraic exercise — the kind of thing a reader would *expect* after seeing the $|T|^{-1/2}$ law.

**Recommended presentation:**

> "Given $\sigma_S/\sigma_L = \sqrt{R}$ from the $|T|^{-1/2}$ law (where $R = |T_L|/|T_S| > 1$), we can solve for the condition under which two compounds with target-count ratio $R$ would have equal proximity Z-scores. Setting $Z_L = Z_S$:
> \[
> \frac{d_c^L - \mu_L}{\sigma_L} = \frac{d_c^S - \mu_S}{\sigma_S}
> \]
> Substituting $\sigma_S = \sigma_L/\sqrt{R}$ and solving for the raw-distance margin $\delta = d_c^L - d_c^S$:
> \[
> \boxed{\delta_{\max}(R) = (\mu_L - \mu_S) + |z_S|\,\sigma_L(\sqrt{R} - 1)} \tag{1}
> \]
> This is the maximum raw-distance margin the larger set can overturn: if the smaller set's raw advantage $\delta = d_c^L - d_c^S$ is less than $\delta_{\max}$, the larger set can register a more negative Z-score despite being topologically farther away."

This presentation:
- Treats the derivation as a natural algebraic exercise (which it is)
- Boxes the formula as the key structural result
- Numbers it as an equation (currently unnumbered)
- Explains the interpretation immediately

**Additional nuance (per STATISTICAL_LOGIC_AUDIT §2.2):** The formula treats $z_S$ as known, but it's estimated from $n = 1{,}000$ permutations. This is a minor concern given the $N = 20{,}000$ probe reference makes $\mu_L, \mu_S, \sigma_L$ essentially exact. A footnote or parenthetical could note: "Uncertainty in $z_S$ (SE $\approx 0.03$ from $n = 1{,}000$ permutations) propagates to $\delta_{\max}$ with a bootstrap CI of approximately $\pm 0.02$; we report the point estimate for clarity."

---

## 5. Should PE be introduced as "complementary effect-size ranking" earlier?

**Yes.** Currently PE appears in Results §4, after the operating-regime benchmark and the $|T|^{-1/2}$ law have been established. It is presented as:

> "Perturbation efficiency $E$ is therefore exactly the mean per-target influence on the disease module --- a size-normalised effect-size ranking, not a re-standardised evidence statistic" (line 64)

This positions PE as an *alternative* to the Z-score — almost a fix for the "problem" identified in §1. But PE is subject to the *same* $|T|^{-1/2}$ variance scaling when standardized (as the paper correctly notes in §2: "influence-based Z-scores are subject to the same shrinkage as proximity Z-scores"). Introducing PE after the problem makes it look like an escape; introducing it before, alongside $d_c$, makes it a natural companion.

**Recommended placement (Phase A, §A3):**

Introduce PE immediately after $d_c$ and Proximity Z, framed as:

> "We consider two complementary effect-size estimands. The first is the raw closest distance $d_c$ (topological proximity). The second is perturbation efficiency $E$, defined as the mean per-target random-walk influence on the disease module (Eq. 4). Both are means over $|T|$ targets and therefore subject to the same $|T|^{-1/2}$ null-precision scaling when standardized. PE provides an ordinal effect-size ranking orthogonal to shortest-path proximity; its cardinal magnitude depends on the restart probability $\alpha$ and should not be interpreted as an absolute biological constant."

**Key rhetorical shift:** PE is not a "solution" to the Z-score problem — it's a different effect-size lens. Both $d_c$ and $E$ are valid; both are subject to LLN variance scaling; both can be standardized into Z-scores; the ranking stability question applies to both. This framing normalizes PE, removes the defensive "here's a better metric" implication, and makes the paper about *understanding statistical behavior* rather than *fixing a flawed metric*.

**Note on language (per STATISTICAL_LOGIC_AUDIT S6):** The paper should consistently call PE an "ordinal effect-size ranking" rather than an "effect size" simpliciter, since the cardinal magnitude is $\alpha$-dependent (ratio ranges from 2.90 to 13.35 across $\alpha \in [0.10, 0.70]$). This qualification should appear at first introduction, not buried in a later caveat.

---

## 6. Where should the calibration-Z vs Guney-Z distinction be made clearest?

**At first introduction of the Z-score concept.** Currently the reader encounters:

1. **Results §1, line 8:** "The Z-score is a standardized quantity, $Z = (d_c - \mu_{\text{null}})/\sigma_{\text{null}}$" — no distinction made; this implicitly defines the Guney Z.
2. **Results §3, line 44:** "this benchmark Z-score is used to study the operating behaviour of standardisation across target counts; it is not the per-compound Guney null used for the real compounds" — distinction introduced retroactively.
3. **Results §6:** Guney fidelity check — further muddies the waters with yet another null variant (two-sided vs fixed-disease).

This is confusing. The reader sees "Z-score" in §1 and forms a concept; §3 introduces a different kind with a brief disclaimer; §6 introduces even more variants.

**Recommended approach:**

In Phase A, immediately after defining $Z = (d_c - \mu_{\text{null}})/\sigma_{\text{null}}$:

> "The null distribution $(\mu_{\text{null}}, \sigma_{\text{null}})$ can be constructed in two ways, serving different purposes:
>
> 1. **Per-compound degree-matched null (Guney Z):** For each biological compound, $n = 1{,}000$ random target sets are drawn matching the compound's target degrees within a $\pm 25\%$ window. This is the null used for reporting proximity evidence of real compounds (Table 1).
>
> 2. **Size-level calibration null (calibration Z):** For the operating-regime benchmark, null parameters $(\mu, \sigma)$ are estimated once per target-set size from $N = 20{,}000$ random probes drawn from a common degree profile. This characterizes how standardization behaves as a function of $|T|$; it is not used for biological inference.
>
> Both constructions share the same $|T|^{-1/2}$ variance scaling, and for the Hyperforin/Quercetin pair the Guney null $\sigma$ ratio ($0.235 / 0.091 = 2.58$) agrees with the calibration-null prediction ($\sqrt{62/10} = 2.49$) to within 4%, confirming quantitative consistency between the two constructions."

This makes the distinction at the point of *definition*, not retroactively. It also addresses the STATISTICAL_LOGIC_AUDIT S2 recommendation for a numerical reconciliation.

---

## 7. Proposed clean equation flow

### Current state

The current manuscript has three numbered equations, all in Results §4 (the RWR section):
- Eq (1): $\mathbf{p} = \alpha[I - (1-\alpha)W]^{-1}\mathbf{p}_0$ (RWR steady state)
- Eq (2): $I(T,D) = \sum_{d \in D} p_d$ (influence)
- Eq (3): $E(T,D) \equiv I(T,D) = \frac{1}{|T|}\sum_{t \in T}\sum_{d \in D} p_d^{(t)}$ (PE)

Meanwhile, **the most important statistical equations are unnumbered**:
- $d_c = \frac{1}{|T|}\sum_{t\in T} \min_{s\in D} \text{dist}(t,s)$ — in Methods, unnumbered
- $Z = (d_c - \mu_{\text{null}})/\sigma_{\text{null}}$ — in Results §1, unnumbered
- $\sigma_{\text{null}} \propto |T|^{-1/2}$ — in Results §2, unnumbered
- $\delta_{\max}(R) = (\mu_L - \mu_S) + |z_S|\sigma_L(\sqrt{R} - 1)$ — in Results §3, unnumbered

This is backwards. The RWR equations are standard methodology (Köhler 2008, Cowen 2017); the proximity-statistical equations are the paper's novel contribution.

### Recommended equation flow

**Methods section (or early Results):**

| Eq | Expression | Purpose |
|----|-----------|---------|
| (1) | $d_c(T,D) = \frac{1}{|T|}\sum_{t\in T} \min_{s\in D} \text{dist}(t,s)$ | Raw proximity — topological effect size |
| (2) | $Z = (d_c - \mu_{\text{null}})/\sigma_{\text{null}}$ | Proximity Z-score — standardized evidence |
| (3) | $\mathbf{p} = \alpha[I_n - (1-\alpha)W]^{-1}\mathbf{p}_0$ | RWR steady state (standard; Köhler 2008) |
| (4) | $E(T,D) = \frac{1}{|T|}\sum_{t\in T} \sum_{d\in D} p_d^{(t)}$ | Perturbation efficiency — complementary effect size |

**Results — Mathematical Characterization (Phase B):**

| Eq | Expression | Purpose |
|----|-----------|---------|
| (5) | $\sigma_{\text{null}} \propto |T|^{-1/2}$ | Null-precision scaling (LLN) |
| (6) | $\delta_{\max}(R) = (\mu_L - \mu_S) + \|z_S\|\,\sigma_L(\sqrt{R} - 1)$ | Maximum overturnable raw-distance margin |

**Rationale:** Equations (1)–(4) define the estimands. Equations (5)–(6) are the paper's two key structural results — the variance scaling and its algebraic consequence. These deserve equation numbers because they are the mathematical spine of the paper. The RWR equations are included as (3)–(4) because they define PE, but they are standard and could even be relegated to Methods with cross-references.

### Equation placement by section

```
Methods (or Phase A — Definition):
  Eq (1): d_c definition
  Eq (2): Z definition  
  Eq (3): RWR steady state
  Eq (4): E definition (PE)

Phase B1 — Null-precision law:
  Eq (5): σ_null ∝ |T|^{-1/2}
  
Phase B2 — Overturnable margin:
  Eq (6): δ_max(R) = ...

Phase D — Decomposition:
  (No new equations needed; the decomposition is
   E = E_direct + E_propagated, which follows from
   linearity and is stated in prose.)
```

---

## 8. Additional architectural observations

### 8.1 The unconditional discordance rate should be more prominent

Per STATISTICAL_LOGIC_AUDIT §5: the unconditional discordance rate (~12% at $R = 6.2$) is the most practically important number. Currently it appears in a subordinate clause ("Unconditionally, however, Z-score and raw-distance rankings disagree in ~12% of cross-size comparisons at R=6.2, a rate high enough to matter for naive cross-compound Z-score comparison"). 

**Recommendation:** Elevate to a standalone sentence early in the operating-regime section, and include in the abstract. This is the "so what" — the regime is not just theoretically interesting; it produces practically non-negligible discordance. The conditional rates (~0.39%) are then presented as the *refined* picture: reversals of material margins are rare, but reversals of modest margins occur at rates that matter.

### 8.2 The $\delta_0$ threshold needs justification

Per STATISTICAL_LOGIC_AUDIT §7: the conditional analysis uses $\delta_0 \in \{0.3, 0.5\}$ without principled justification. The H/Q margin (0.38) falls between them.

**Recommendation:** Either (a) add a continuous sweep of reversal rate vs. $\delta_0$ as a supplementary figure, or (b) justify the thresholds: $\delta_0 = 0.3$ corresponds to ~14% of the null-mean closest distance (2.2 hops) in this network; $\delta_0 = 0.5$ corresponds to ~23%. A reference to network-distance effect-size conventions (e.g., what magnitude of $d_c$ difference is considered biologically material in the network-medicine literature) would strengthen the threshold choice.

### 8.3 The LLN caveat belongs in the main text, not a footnote

The STATISTICAL_LOGIC_AUDIT notes (S1) that the terms $\min_d \text{dist}(t,d)$ are not i.i.d. under degree-matching. The empirical slope of $-0.48$ (vs. $-0.50$) reflects this. Currently the text treats the $-0.48$ as "confirmation" of the LLN. A statistician would note the deviation and explain it.

**Recommendation:** Add one sentence in the $|T|^{-1/2}$ section acknowledging that degree-matching induces weak dependence among the per-target terms, so the $-1/2$ exponent is an asymptotic approximation; the empirical slope of $-0.48$ reflects finite-sample behavior, while the large-$N$ probe calibration ($N = 20{,}000$) recovers the asymptotic exponent to high precision.

### 8.4 Section naming should reflect the mathematical structure

Current subsection titles are narrative/descriptive:
- "Raw proximity and proximity-Z rank the two compounds differently"
- "The null standard deviation shrinks with target count for every metric"
- "The null-precision law defines a conditional operating regime for rank reversal"
- "Perturbation efficiency is the mean per-target influence"

Recommended mathematical-structure titles:
- "Estimands: proximity, standardized evidence, and perturbation efficiency" (Phase A)
- "Null-precision scaling and the overturnable-margin envelope" (Phase B)
- "The Hyperforin/Quercetin pair as a located instance" (Phase C)
- "Separating direct target-module overlap from propagated influence" (Phase D)

---

## 9. Summary of recommendations

| # | Recommendation | Priority | Affected sections |
|---|---------------|----------|-------------------|
| R1 | Restructure into 4 phases: Definition → Characterization → Illustration → Decomposition | **CRITICAL** | Entire Results |
| R2 | Operating-regime benchmark before biological pair | **CRITICAL** | Results §2–3 swap |
| R3 | Introduce PE alongside $d_c$, not as a post-hoc alternative | **HIGH** | Results §A3 (new) |
| R4 | Frame $|T|^{-1/2}$ as LLN → empirical confirmation, not discovery | **HIGH** | Results §B1 (new) |
| R5 | Present $\delta_{\max}$ as natural algebraic consequence with boxed equation | **HIGH** | Results §B2 (new) |
| R6 | Distinguish Guney-Z vs calibration-Z at first Z-score definition | **HIGH** | Results §A2 (new) |
| R7 | Number the proximity-statistical equations (1)–(6); demote RWR to Methods | **HIGH** | Methods + Results |
| R8 | Elevate unconditional discordance rate to standalone prominence | **MODERATE** | Results §B3, Abstract |
| R9 | Acknowledge LLN approximation caveat (non-i.i.d. under degree-matching) | **MODERATE** | Results §B1 |
| R10 | Add $\delta_0$ threshold justification (continuous sweep or principled rationale) | **MODERATE** | Results §B3 |

---

## 10. Proposed section map (revised Results)

```
\section{Results}

\subsection{Estimands: proximity, evidence, and perturbation efficiency}
  \label{subsec:estimands}
  [Phase A — Clean definitions of d_c, Proximity Z, and PE.
   Calibration-Z vs Guney-Z distinction made here.
   Eqs (1)–(4) defined.]

\subsection{Null-precision scaling and the overturnable-margin envelope}
  \label{subsec:opregime}
  [Phase B — Mathematical characterization.
   |T|^{-1/2} law (LLN, empirically confirmed) → Eq (5).
   δ_max derivation → Eq (6).
   20,000-probe calibration benchmark.
   Unconditional discordance rate (~12% at R=6.2) as a headline.
   Conditional reversal rates as refinement.
   LLN caveat: non-i.i.d. under degree-matching.]

\subsection{The Hyperforin/Quercetin pair as a located instance}
  \label{subsec:worked_example}
  [Phase C — Hyperforin/Quercetin numbers.
   The pair sits at the 91st percentile of probe-pair margins,
   inside the δ_max envelope at R=6.2.
   "Not a generic outcome; a mechanistically interpretable,
   located instance of a characterized regime."
   PE ranking: Hyperforin > Quercetin, stable across thresholds.]

\subsection{Separating direct target-module overlap from propagated influence}
  \label{subsec:decomposition}
  [Phase D — Mechanistic decomposition.
   Direct: 62% of Hyperforin's PE is T∩D mass.
   Propagated advantage: 1.5×, modest.
   Both components concentrate in PXR–CYP–transporter axis.]

\subsection{Robustness}
  \label{subsec:robustness}
  [Phase E — Guney fidelity, chemical-similarity negative control,
   threshold robustness, expression-floor insensitivity.]
```

---

## Appendix: Cross-reference to STATISTICAL_LOGIC_AUDIT

This memo's recommendations align with the Principal Statistician's audit (S1–S8):

| Audit item | This memo's response |
|-----------|---------------------|
| S1: LLN caveat (non-i.i.d.) | R9 — add one sentence acknowledging the approximation |
| S2: Calibration-Z vs Guney-Z bridge | R6 — distinguish at first definition; add numerical reconciliation |
| S3: $R^2 = 0.9999$ artifact | R4 — note large-N probe design as caveat |
| S4: P-value floor | (Not an estimand-architecture issue; addressed separately) |
| S5: BH correction scope | (Not an estimand-architecture issue; addressed separately) |
| S6: PE is ordinal, not cardinal | R3 — qualify "effect size" → "ordinal effect-size ranking" |
| S7: Unconditional discordance prominence | R8 — elevate to standalone sentence |
| S8: $\delta_0$ threshold justification | R10 — add continuous sweep or principled rationale |

All eight statistical-logic concerns are addressed by the estimand restructuring recommended here, plus minor text additions that do not change the mathematical content.

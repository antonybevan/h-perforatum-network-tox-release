# MANUSCRIPT ARCHITECTURE BLUEPRINT (Draft — to be finalized after agent review)

## Proposed Section Order

### Current Order (problematic)
1. §2.1: Raw proximity and Z rank differently (biological pair first)
2. §2.2: Null SD shrinks
3. §2.3: Operating-regime benchmark
4. §2.4: Perturbation efficiency
5. §2.5: Direct/propagated decomposition
6. §2.6: Guney fidelity
7. §2.7: Chemical similarity

### Proposed Order
1. §2.1: The null-precision law — |T|^{-1/2} scaling and operating-regime benchmark
2. §2.2: The Hyperforin/Quercetin pair as a located instance
3. §2.3: Perturbation efficiency — a complementary effect-size ranking  
4. §2.4: Direct/propagated decomposition
5. §2.5: Guney fidelity
6. §2.6: Chemical-similarity control

### Rationale
- The statistical mechanism (LLN → |T|^{-1/2} → δ_max → reversal rates) is the paper's primary contribution
- The biological pair illustrates the mechanism, not vice versa
- The benchmark characterizes the regime; the pair instantiates it
- This order matches how Guney/Menche papers flow: method → calibration → application

---

## Section Blueprints

### ABSTRACT
- **Purpose:** State the methodological contribution in 5 sentences
- **Reader question:** What does this paper do and why does it matter?
- **Core claim:** Proximity Z-scores are valid evidence statistics; their magnitude should not be read as effect-size ranking under target-count asymmetry
- **Tone:** Calm, composed, no caveats
- **Phrases to avoid:** "rather than calling into question," "though not an established intrinsic hepatotoxin"
- **Structure:** Problem → mechanism → calibration → worked example → implication

### INTRODUCTION
- **Purpose:** Establish that network proximity is useful, identify the cross-compound interpretation gap, state our approach
- **Reader question:** Why should I care about target-count asymmetry?
- **Core claim:** When target counts differ sharply, Z-magnitude can diverge from raw effect ranking because σ_null shrinks as |T|^{-1/2}
- **Tone:** Confident, methodological, precise
- **Phrases to avoid:** Defensive disclaimers about what the paper is NOT
- **Structure:**
  1. Network proximity is validated and useful (Guney, Menche)
  2. Z-score = evidence, not effect-size magnitude (ASA statement)
  3. Target-count asymmetry creates an interpretation problem
  4. We characterize this regime with a benchmark and worked example

### RESULTS §2.1: The Null-Precision Law
- **Purpose:** Establish the |T|^{-1/2} scaling and the operating regime
- **Core claim:** σ_null ∝ |T|^{-1/2} for all metrics; this creates the capacity for rank reversal
- **Evidence:** Log-log slope -0.499, CI [-0.502,-0.495], R²=0.9999
- **Flow:** LLN expectation → empirical confirmation → δ_max derivation → reversal rates → unconditional discordance

### RESULTS §2.2: A Worked Liver-Network Example
- **Purpose:** Show the Hyperforin/Quercetin pair inside the characterized regime
- **Core claim:** The pair sits at the 91st percentile, margin 0.38 < δ_max ≈ 0.63
- **Tone:** "The pair instantiates the regime" not "The pair proves the phenomenon"

### RESULTS §2.3: Perturbation Efficiency
- **Purpose:** Introduce the complementary effect-size ranking
- **Core claim:** PE = mean per-target RWR influence; ordinal, not cardinal
- **Flow:** RWR definition → PE identity → α-sensitivity → expression weighting

### RESULTS §2.4: Direct/Propagated Decomposition
- **Purpose:** Separate target-DILI overlap from network influence
- **Core claim:** 62% is direct overlap; propagated advantage is ~1.5×
- **Tone:** "The framework separates these components" not "We must admit the advantage is mostly overlap"

### DISCUSSION
- **Purpose:** Synthesize, not re-defend
- **Tone:** Composed, forward-looking
- **Cut:** Half the "rather than" instances
- **Structure:** Contribution → relationship to prior work → limitations → conclusion

### LIMITATIONS
- **Keep as-is** — already strong and honest. Do not dilute.

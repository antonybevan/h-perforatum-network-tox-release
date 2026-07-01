# AGENT F — Scientific Reports Editor Memo

**Manuscript:** "Separating effect size from statistical evidence in network-proximity rankings under target-count asymmetry: a controlled liver-interactome audit"
**Date:** 2026-07-01
**Role:** Scientific Reports editorial evaluation

---

## 1. Is the title too long? What would you change?

**Yes, it is too long.** At 22 words, it exceeds what is comfortable for a Scientific Reports title. The colon separates two grammatically independent noun phrases, which is common but here both halves are themselves dense. Scientific Reports favours titles under ~15 words that a reader can parse at a glance.

**What I would change:**

Delete the subtitle. The methodological contribution is already signalled by "Separating effect size from statistical evidence in network-proximity rankings under target-count asymmetry" (15 words). The tag "a controlled liver-interactome audit" adds specificity but the abstract already tells the reader this is a liver-network study; the subtitle reads as hedging ("controlled," "audit") rather than adding essential information. If the liver setting must appear in the title, collapse it into a single clause:

> "Effect size versus statistical evidence in network-proximity rankings under target-count asymmetry"

or, retaining the liver context:

> "Target-count asymmetry can reverse network-proximity evidence rankings: a liver-interactome demonstration"

Either version communicates the core finding without the defensive framing embedded in "controlled … audit."

---

## 2. Does the abstract read like a paper or a defense? Rate 1–10.

**Rating: 5/10 — reads more like a defence than a paper.**

The abstract is substantially over-length. I count approximately 310 words; Scientific Reports asks for ~150–250. It is a single unbroken paragraph that packs in: the theoretical mechanism, the numerical case study, the operating-regime benchmark results, the perturbation-efficiency remedy, the direct-vs-propagated decomposition, and the chemical-similarity negative control. That is too much.

More problematically, the tone is preemptively defensive. The abstract contains:

- "In this illustrative case…" (qualifying before the finding is stated)
- "…providing a worked demonstration of the framework" (minimising the claim)
- The final clause about "unconditionally, Z-score and raw-distance rankings disagree in ~12%…" (inserts a qualifying statistic that belongs in Results, not in the abstract's closing)

A good Scientific Reports abstract states what was found, not what was *not* claimed. The abstract currently reads as if the authors are bracing for reviewer pushback. It should be cut to ~200 words, structured as: (1) what the problem is, (2) what we did, (3) what we found, (4) the practical implication. Every "not a predictor / illustrative / worked example" qualifier should be removed from the abstract and saved for the Discussion.

---

## 3. Are Results sections ordered correctly for this journal?

**Partially.** The current order is:

1. Raw proximity and proximity-Z rank the two compounds differently
2. The null standard deviation shrinks with target count for every metric
3. The null-precision law defines a conditional operating regime for rank reversal
4. Perturbation efficiency is the mean per-target influence
5. Separating direct overlap from propagated influence
6. The proximity computation is faithful to the canonical implementation
7. Chemical-similarity negative control

The logical flow (case study → mechanism → generalisation → remedy → decomposition → validation → control) is defensible. However, two problems arise for Scientific Reports:

**Problem A: The fidelity check (§6) and chemical-similarity control (§7) are placed as appendages.** The Guney reimplementation (§6) validates that the core result is not an artefact — this is methodological housekeeping that should appear *early* (after §1 or in Methods) or be moved to Supplementary. A reader encountering it at the end has already accepted the earlier results on trust and then learns, retroactively, that those results were validated. The chemical-similarity control likewise feels like an afterthought; it would fit better immediately after the case-study presentation or as a brief note within Methods.

**Problem B: The operating-regime benchmark (§3) is placed between the mechanism (§2) and the remedy (§4).** This benchmark is heavy — it introduces a new experimental design, a mathematical derivation of δ_max, and three panels of a figure. Placing it before the reader has seen the proposed remedy (perturbation efficiency) means the manuscript spends a long time on "here is how bad the problem is, and how rare" before offering the solution. A more reader-friendly ordering would present the remedy immediately after documenting the problem, and then show the operating regime as a robustness/scope analysis.

**Suggested reordering for Scientific Reports:**

1. The core dissociation (current §1)
2. Why it happens — the |T|⁻¹/² law (current §2)
3. Perturbation efficiency as a complementary effect size (current §4)
4. Direct-vs-propagated decomposition (current §5)
5. Operating-regime benchmark — how general is this? (current §3, repositioned as scope analysis)
6. Validation: Guney fidelity + chemical similarity (current §§6–7, or → Supplementary)

---

## 4. Are limitations over-repeated? Count how many distinct places the same caveat appears.

**Yes, severely over-repeated.** The core caveat — "this is not a predictor, this is an illustrative audit / worked example, we make no population-level or toxicity claim" — appears in at least **eight distinct locations**:

| # | Location | Representative phrasing |
|---|----------|------------------------|
| 1 | Abstract | "In this illustrative case… a worked demonstration of the framework" |
| 2 | Introduction ¶3 | "The role of the case study is therefore to instantiate the failure condition transparently, not to estimate its prevalence." |
| 3 | Introduction ¶4 | "we make no population-level performance or toxicity-prediction claim" |
| 4 | Results §3 (opregime) | "We make no claim that such reversals are common, and none about toxicity." |
| 5 | Discussion ¶1 | "we do not claim that random-walk influence is a superior proximity statistic" |
| 6 | Discussion ¶2 | "We therefore do not claim that Hyperforin is uniquely high-leverage…" |
| 7 | Discussion §3 (Limitations) | "This is a controlled two-compound biological audit, not a predictor." + sub-caveats on provenance, curation asymmetry, generalisation |
| 8 | Discussion §4 (Conclusion) | "This framework provides a worked audit template, not a population-level predictor…" |

Several sub-caveats are also duplicated: the "Hyperforin is not an established intrinsic hepatotoxin" qualifier appears in the Introduction, Results, and Discussion. The "target sets differ in provenance, not only size" limitation appears in Introduction ¶4 and again in the Limitations subsection. The "curation asymmetry" point is made in Introduction, Discussion Limitations, and Supplementary Note.

**Effect on the reader:** By the fifth iteration, the reader stops trusting the authors' own findings — if the authors themselves keep insisting the work is limited, why should a reviewer invest in it? The single biggest editorial problem in this manuscript is the defensive repetition. A single, well-written Limitations subsection in the Discussion is sufficient; every other instance should be cut.

---

## 5. Is the conclusion too caveated? What would you cut?

**Yes, the conclusion is too caveated.** The conclusion paragraph (Discussion §4) contains five sentences. Of these:

- Sentence 3: "This framework provides a worked audit template, not a population-level predictor…" — repeats the "not a predictor" caveat for the eighth time.
- Sentence 4: "…the studied pair is a located instance rather than the sole evidence" — repeats the operating-regime qualifier already stated in Results and Discussion.
- Sentence 5: "Natural extensions include signed, directional edge weights…" — future-work speculation that belongs in the Limitations or Discussion body, not the Conclusion.

**What I would cut:**

1. **"This framework provides a worked audit template, not a population-level predictor, for separating effect size, evidence, and direct target–disease overlap…"** — Delete entirely. The reader already knows this. If it must stay, reduce to: "for separating effect size, evidence, and direct target–disease overlap in target-asymmetric network comparisons."

2. **"…the studied pair is a located instance rather than the sole evidence"** — Delete. The conclusion should synthesise, not re-litigate scope.

3. **"Natural extensions include signed, directional edge weights (to distinguish enzyme induction from inhibition) and influence on phenotype-specific sub-modules, linking topological reach to discrete clinical outcomes."** — Move to the end of the Limitations subsection or delete. A conclusion should not end on what the paper *didn't* do.

**A leaner conclusion would read:**

> Network-proximity Z-scores are valid evidence statistics whose magnitude should not be read as a cross-compound effect-size ranking under target-count asymmetry. Reporting raw effect size alongside standardized evidence, and decomposing per-target influence into direct-overlap and propagated components, yields a more transparent comparative picture. In the illustrative worked example, this framework recovers the expected mechanistic ordering — the PXR/CYP-inducing constituent ranking higher — while exposing the direct target–disease overlap that an uncritical headline number would have conflated with propagated influence.

That is three sentences, states the finding, states the recommendation, states the illustrative result, and stops. No apologies, no forward-looking hand-waving.

---

## 6. Which sentences would make you pause as an editor?

As an editor, I would flag the following:

**(a) Introduction — the criteria sentence (¶4):**
> "They satisfy explicit criteria: a large, real target-set asymmetry (10 vs 62 in the LCC), which is the stressor of interest; a shared botanical context (H. perforatum) that keeps the worked example within one phytochemical source without controlling systemic exposure or target-curation provenance; a contrasting, well-characterised mechanism that makes the resulting dissociation interpretable and checkable; and adequate curatable target evidence for both."

This is 70+ words with four semicolon-separated clauses, three of which contain embedded qualifications. By the time the reader reaches "adequate curatable target evidence," they have lost the thread. Break into a bulleted or numbered list, or reduce to: "The pair satisfies three criteria: (i) large target-count asymmetry (10 vs 62), (ii) a shared botanical origin that keeps the comparison within one phytochemical source, and (iii) well-characterised mechanisms that make the dissociation interpretable."

**(b) Introduction — the DILI module justification (¶3):**
> "…the present DILI association module includes cytochrome-P450, transporter, and nuclear-receptor genes—the very proteins drugs engage—so the same case also exposes a second, coupled pitfall: direct target–disease overlap inflating apparent network influence."

The em-dash phrase "—the very proteins drugs engage—" is colloquial and uninformative. The sentence also tries to introduce a second major conceptual point ("coupled pitfall") mid-paragraph, which dilutes the main argument. Split: first paragraph for the Z-score argument, second for the overlap argument.

**(c) Discussion — the Guney relationship paragraph (¶1 of "Relationship to prior work"):**
> "Random walk with restart is conceptually adjacent to attenuated-distance and diffusion-style measures, but it is not identical to Guney's diffusion-kernel proximity (dk), which downweights longer shortest paths by an exponential penalty rather than propagating restart-anchored probability mass over the adjacency matrix; we therefore do not use Guney's dk result to argue for or against random-walk influence."

This is a 55-word single sentence that does boundary work — it tells readers what the authors are *not* claiming about Guney's method. The technical distinction is valid, but the sentence reads as defensive pre-emption. Move the technical distinction to Methods; keep the Discussion focused on interpretation.

**(d) Abstract — final clause (truncated in file but visible in source):**
> "Unconditionally, Z-score and raw-distance rankings disagree in ~12% of cross-size comparisons at R=6.2, a rate high enough to matter for naive cross-compound Z-score comparison."

This is a Results-level detail dropped into the abstract's closing position. It is not a concluding statement; it is a specific numerical finding that belongs in Results. The abstract should close on the implication, not a secondary statistic.

**(e) The "not a predictor" litany (multiple locations):**
Each instance individually is reasonable; collectively they erode confidence. The phrase "this is a controlled two-compound biological audit, not a predictor" appears almost verbatim in the Limitations subsection and echoes throughout. A reader notes: if the authors are this anxious about being misinterpreted, perhaps the framing is wrong.

---

## 7. What is the single most important change needed?

**Reduce the defensive over-caveating by at least 50%, and restructure the paper to lead with what it *does* show rather than what it *does not* claim.**

The paper has a sound technical observation: under target-count asymmetry, Z-score magnitude can diverge from raw topological effect, because the null standard deviation shrinks as |T|⁻¹/². This is a useful methodological note for the network-medicine community, and it is supported by careful numerical work and a degree-controlled benchmark.

But the manuscript buries this contribution under layers of preemptive self-limitation. The abstract, introduction, results, discussion, and conclusion all contain variations of "we are not claiming X." The cumulative effect is that the paper reads as a response to a hostile review rather than as a standalone contribution.

**Concrete actions to achieve this:**

1. Write a single, definitive Limitations paragraph in the Discussion. State each limitation once, clearly, without apology. Remove all other instances.
2. Recast the framing: instead of "we are not attacking Guney / we are not a predictor / we are not claiming toxicity," write "we show that… we document that… we recommend that…"
3. Shorten the abstract to ≤200 words and remove all qualifiers ("illustrative," "worked demonstration").
4. Let the Conclusion state the finding and the recommendation without caveats. If the work is sound, it does not need to remind the reader of its own boundaries in its final paragraph.
5. Move the Guney fidelity check and chemical-similarity control out of Results — they are methodological validation, not findings.

---

## 8. Would you send this for review in current form?

**Yes, but with a requirement for major revisions before review.**

The technical content is sound and the contribution — documenting a failure mode of cross-compound Z-score comparison and proposing per-target influence as a complementary effect size — is appropriate for Scientific Reports. The computational work appears reproducible and well-documented. The operating-regime benchmark is a genuine methodological addition that strengthens the paper beyond a simple case report.

However, the manuscript in its current form would generate reviewer fatigue. The defensive tone, the repeated caveats, the prolix abstract, and the overlong introduction would cause reviewers to skim rather than engage. At least one reviewer would flag the "not a predictor" refrain as a red flag and ask: "If the authors are this defensive, what are they hiding?" — even though the answer is "nothing; the work is honestly scoped."

**My recommendation as editor:** Return to authors with a decision of "Major Revisions Required" (not "Reject"), accompanied by a letter that:

1. Acknowledges the sound methodological contribution.
2. Requires shortening the abstract to ≤200 words and removing defensive qualifiers.
3. Requires consolidating all limitations into a single Discussion subsection.
4. Requires restructuring Results to place the remedy (perturbation efficiency) before the scope analysis (operating regime).
5. Requires moving the Guney fidelity and chemical-similarity sections to Supplementary or Methods.
6. Requires a rewritten Conclusion of ≤4 sentences that states findings without caveats.

If these revisions are made, the paper would be suitable for peer review and likely to pass Scientific Reports' bar of methodological soundness and clarity.

---

## Summary

| Criterion | Assessment |
|-----------|------------|
| Title length | Too long (22 words). Cut subtitle. |
| Abstract tone | 5/10 — defensive, over-long, buries findings under qualifiers. |
| Results ordering | Partially correct. Remedy should precede scope analysis; validation controls should be in Supplementary. |
| Limitations repetition | Same caveat appears in ≥8 distinct locations. Cut to one Limitations subsection. |
| Conclusion caveating | Over-caveated. Cut 2 of 5 sentences; remove future-work speculation. |
| Pause-worthy sentences | ≥5 identified. Defensive boundary-drawing, 70+-word sentences, colloquial asides. |
| Single most important change | Reduce defensive over-caveating by ≥50%; lead with findings, not disclaimers. |
| Send for review? | Yes, but only after major revisions (consolidate limitations, restructure, shorten abstract). |

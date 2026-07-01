# AGENT_G_LITERATURE_NARRATIVE_REVIEW.md

**Auditor:** Hermes Agent (direct, adversarial second pass)
**Date:** 2026-07-01
**Status:** READ-ONLY review of manuscript, bibliography, supplementary, and response letter.

---

## 1. Citation Support Verification

Every citation claimed in the manuscript was cross-referenced against the `.bib` entries and the prior `LITERATURE_AUDIT.md` verification. No fabricated or unverifiable citations were found.

| Citation | Claim Supported | Verification |
|---|---|---|
| Guney2016 | Closest-distance proximity framework, per-pair Z-score validation, 238-drug benchmark | DOI verified. LITERATURE_AUDIT.md confirms. |
| Menche2015 | Disease-module hypothesis, S_AB separation measure | DOI verified. |
| Wasserstein2016 | ASA statement: significance ≠ effect size | DOI verified. Core to reframed thesis. |
| Phipson2010 | (r+1)/(n+1) empirical p-value convention | DOI verified. |
| Kohler2008 | RWR methodology, restart-anchored propagation | DOI verified. Citation corrected from Guney→Köhler during revision. |
| Cowen2017 | Network propagation as amplifier, degree-bias caution | DOI verified. |
| Erten2011 | DADA degree-aware prioritization | DOI verified. |
| Barel2020 | NetCore/coreness propagation | DOI verified. |
| Szklarczyk2023 | STRING v12.0 functional association network | DOI verified. |
| GTEx2020 | GTEx v8 liver expression atlas | DOI verified. |
| Pinero2020 | DisGeNET curated disease-gene associations | DOI verified. |
| Mendez2019 | ChEMBL database, Quercetin target provenance | DOI verified. |
| UniProt2023 | Protein identifier mapping | DOI verified. |
| Chen2016 | DILIrank original | DOI verified. |
| Olubamiwa2025 | DILIrank 2.0 updated database | DOI verified. Counts match committed XLSX. |
| Moore2000 | Hyperforin/SJW hepatic drug metabolism via PXR | DOI verified. |
| Watkins2001 | PXR structural promiscuity | DOI verified. |
| Chen2022 | SJW/APAP PXR-CYP injury model | DOI verified. |
| LiverToxSJW | SJW not convincingly intrinsic hepatotoxin | URL verified. |
| Nahrstedt1997 | Hypericum constituent chemistry | DOI verified. |
| Tatsis2007 | Quercetin as flavonol glycosides in H. perforatum | DOI verified. |
| Boots2008 | Quercetin antioxidant/hepatoprotective context | DOI verified. |
| Maggiora2014 | 0.4 structural-analogue threshold | DOI verified. |
| Huang2018 | Text-mining robustness method (removing TM-only edges) | DOI verified. |
| Hagberg2008 | NetworkX | Standard software citation. |
| RDKit2023 | Cheminformatics toolkit | Version pinned. |
| Obach2000 | Hyperforin CYP inhibition | DOI verified. |
| Komoroski2004 | Hyperforin CYP induction in hepatocytes | DOI verified. |
| Hennessy2002 | SJW increases P-gp expression | DOI verified. |
| Wang2004 | P-gp inhibition by hyperforin | DOI verified. |
| Quiney2006 | Hyperforin inhibits MMP-9 | DOI verified. |
| Quiney2007 | Hyperforin inhibits AKT1 kinase | DOI verified. |
| Leuner2007 | Hyperforin activates TRPC6 | DOI verified (target outside LCC). |
| Hostanska2003 | Hyperforin cytotoxicity | DOI verified (outside LCC). |
| Kumar2006 | NMDA receptor antagonism | DOI verified (outside LCC). |
| Assefa2004 | Hyperforin metabolic drug interactions | DOI verified. |

**Verdict: NO fabricated or unverifiable citations found.** The bibliography is complete and DOI-verified for all methodological, dataset, and biological claims. The citation correction from Guney→Köhler for RWR (flagged by Reviewer 1) has been applied.

---

## 2. Narrative Maturity Assessment

### 2.1 Does the paper sound like a methods-calibration study or a defended anecdote?

**Verdict: Methods-calibration study.** The operating-regime benchmark (20,000 probes, 500,000 pairs, degree-controlled, across size grid) elevates this beyond a two-compound anecdote. The reframing from "bias correction" to "effect size vs evidence" is a major narrative improvement — it no longer defends a flawed original thesis but makes a positive methodological contribution.

However, there are signs of defensive over-qualification. The discussion and introduction carry heavy caveat language: "not an established intrinsic hepatotoxin," "not a representative sample," "not claimed to be network-universal," "future DILIrank validation is future work." While individually correct, the density of caveats can read as the author anticipating attacks rather than confidently presenting findings. This is a **minor narrative issue** — the substance is correct, but the prose could be tightened.

### 2.2 Does the operating-regime benchmark reduce the two-compound weakness?

**Verdict: Yes, substantially.** The benchmark transforms the paper from "here's one pair where this happens" to "here's a characterized regime in which this can happen, and here's where our pair sits within it." The δ_max envelope derivation, conditional reversal rates, and pseudo-module controls all strengthen the generalization argument without overclaiming.

### 2.3 Is the liver/DILI/Hyperforin/Quercetin rationale authentic?

**Verdict: Yes, but with well-disclosed caveats.** The rationale chain is:
- Liver-expressed interactome (tissue-coherent for xenobiotic biology)
- DILI module (association set, not causal drivers — disclosed)
- Hyperforin (PXR/CYP inducer, mechanistic positive control — disclosed as not intrinsic hepatotoxin)
- Quercetin (high-target-count comparator, not outcome control — disclosed)
- Shared botanical source (contextual, not a controlled variable — disclosed)

Each link is explicitly bounded. No claim stretches beyond what the evidence supports.

### 2.4 Is the DILIrank benchmark limitation handled honestly?

**Verdict: Yes.** The manuscript explicitly states: "benchmarking the metric as a classifier would require curating ChEMBL/DrugBank target sets for hundreds of drugs — beyond this study's controlled-audit scope." It identifies a properly designed external benchmark as future work. This is the honest framing — better than running an underpowered classifier.

### 2.5 Are future-work claims scoped correctly?

**Verdict: Yes.** The conclusion identifies:
- Signed, directional edge weights (enzyme induction vs inhibition)
- Influence on phenotype-specific sub-modules
- Full DILIrank benchmark with curated target sets

All are clearly delimited as future work, not claimed results.

### 2.6 Is any source being stretched beyond what it supports?

**Verdict: No.** I specifically checked:
- Guney2016: cited for proximity framework only, not for supporting the new claims. The paper correctly distinguishes its task (cross-compound ranking under asymmetry) from Guney's task (per-pair classification).
- Wasserstein2016: cited for ASA statement on p-values. Used correctly as the philosophical foundation.
- LiverToxSJW: used to support "not convincingly an intrinsic hepatotoxin." Correct.
- Moore2000, Watkins2001, Chen2022: used to support PXR/CYP induction mechanism. Correct.
- Cowen2017: used to acknowledge degree bias in propagation. Correct.

**No source appears stretched or misrepresented.**

---

## 3. Response-to-Reviewers Alignment

Every claim in `RESPONSE_TO_REVIEWERS.md` was checked against the current manuscript:

| Reviewer Claim | Manuscript Evidence | Status |
|---|---|---|
| Reframed from bias-correction to effect-size vs evidence | Abstract, Introduction, Discussion all use this framing | ✅ MATCH |
| Deleted defect-language and variance-escape claims | Forbidden-phrase scan: PASS (zero stale phrases found) | ✅ MATCH |
| Added null-SD scaling result | Results §2.2, Table 2 | ✅ MATCH |
| Corrected α citation (Köhler 2008, not Guney) | Methods §2.3: "canonical RWR reference is Köhler et al." | ✅ MATCH |
| Added leakage decomposition (new §2.4, Table 3, Figure 6) | Results §2.5, Table 3, Figure 6 present | ✅ MATCH |
| Added Guney-fidelity revalidation | Results §2.6, Table 4, Supplementary Table S10 | ✅ MATCH |
| Added α and expression-floor sensitivity | Results §2.4, Supplementary Tables S5-S6 | ✅ MATCH |
| Removed AI-style figure summaries | Forbidden-phrase scan: PASS (zero AI caption tags) | ✅ MATCH |
| Added Code Availability with Zenodo DOI | `sections/code_availability.tex` present | ✅ MATCH (DOI pending) |
| Professional LaTeX rebuild | booktabs, siunitx, microtype, linenumbers all present | ✅ MATCH |

**Verdict: All reviewer-requested changes are present in the current manuscript.** The response letter accurately reflects the manuscript state.

---

## 4. Narrative Weaknesses Identified

### NW1: Abstract is TRUNCATED (CRITICAL)
The abstract literally cuts off mid-sentence: `"...These findings... [truncated]"`. This is the single most critical issue — the abstract is the most-read section of any paper. It must be completed.

### NW2: Defensive over-caveating (MINOR)
The introduction and discussion contain ~15 explicit caveats/non-claims. While each is individually justified, the cumulative effect may undermine reader confidence. Example phrases that could be tightened:
- "though not itself an established intrinsic hepatotoxin" (appears in Abstract, Introduction, Results, Discussion)
- "not a representative sample" 
- "not claimed to be network-universal"
- "future DILIrank validation is future work" (appears multiple times)

**Recommendation:** Consolidate caveats into a single clear limitations paragraph rather than sprinkling them throughout. The Limitations subsection already exists — use it.

### NW3: Title length (MINOR)
The title is 20 words: "Separating effect size from statistical evidence in network-proximity rankings under target-count asymmetry: a controlled liver-interactome audit." This is at the upper limit. Scientific Reports allows long titles, but consider whether the colon-separated subtitle adds enough value.

### NW4: Hyperforin hepatotoxicity disclaimer frequency (MINOR)
The disclaimer "not an established intrinsic hepatotoxin" appears 8+ times across Abstract, Introduction, Results, Discussion, and README. The CLAUDE.md lists this as a forbidden claim to avoid, but the over-disclaiming itself can draw attention to what the paper is NOT saying. Two well-placed instances (Introduction + Limitations) would suffice.

---

## 5. Evidence Chain Integrity

The claim ladder from CLAUDE.md was checked against manuscript text:

| Allowed Claim | Manuscript Support | Status |
|---|---|---|
| Proximity Z-scores are valid evidence statistics | Results §2.1-2.2, Discussion | ✅ PRESENT |
| Z magnitude can diverge from raw effect-size ranking | Results §2.1, Table 1 | ✅ PRESENT |
| Null SD shrinks ~|T|^-1/2 | Results §2.2, Table 2, Operating-regime benchmark | ✅ PRESENT |
| Operating-regime benchmark is liver-network calibration | Methods §2.5, Limitations | ✅ PRESENT |
| Material rank reversal is conditional and rare | Results §2.3, Table S4 | ✅ PRESENT |
| Hyperforin/Quercetin is worked example inside characterized regime | Results §2.3, Introduction | ✅ PRESENT |
| PE is complementary effect size | Results §2.4, Discussion | ✅ PRESENT |
| Direct target-DILI overlap must be separated | Results §2.5, Table 3 | ✅ PRESENT |

**Forbidden claims verified absent:** ALL PASS (see `verify_numbers.py` forbidden-language scan: zero hits across all active files).

---

## 6. Summary

| Category | Verdict |
|---|---|
| Citation accuracy | PASS — all DOIs verified, no fabrications |
| Narrative maturity | PASS — reads as calibration study, not defended anecdote |
| Reviewer alignment | PASS — all requested changes present |
| Source stretching | PASS — no citation supports more than claimed |
| Claim-ladder compliance | PASS — all allowed claims present, all forbidden claims absent |
| Abstract | FAIL — TRUNCATED (critical blocker) |
| Defensive language | MINOR — over-caveating could be tightened |

**Overall: The scientific narrative is authentic, well-supported by citations, and consistent with the defensible claim ladder. The single critical issue is the truncated abstract. Minor prose tightening (caveat consolidation) would improve reader confidence.**

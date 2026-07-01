# PATCH PLAN — Ultra Audit Second Pass

**Date:** 2026-07-01
**Auditor:** Hermes Agent
**Status:** PROPOSED — awaiting author approval where required

---

## Patching Rules Applied

- ✅ Allowed without approval: typos, stale numbers, wording scope fixes, documentation alignment, checksum refresh, source zip rebuild
- ⚠️ Require approval: thesis changes, major analysis additions, file deletions

---

## APPLIED PATCHES (auto-approved)

### P1: Fix stale comment in run_expression_weighted_rwr.py
- **File:** `scripts/run_expression_weighted_rwr.py:36`
- **Old:** `# 9 Hyp, 62 Quer`
- **New:** `# 10 Hyp, 62 Quer`
- **Reason:** Canonical data is 10/62, not 9/62.
- **Risk:** None (comment only)

### P2: Fix cover letter figure reference
- **File:** `manuscript/cover_letter.tex:47`
- **Old:** `Figure~5`
- **New:** `Figure~6`
- **Reason:** Leakage/decomposition figure was renumbered.
- **Risk:** None (descriptive only)

### P3: Fix cover letter Zenodo language
- **File:** `manuscript/cover_letter.tex:51`
- **Old:** `deposited to Zenodo with a citable DOI`
- **New:** `will be deposited to Zenodo with a citable DOI before final publication`
- **Reason:** Zenodo DOI has not been minted yet. Don't overstate.
- **Risk:** None (accuracy correction)

---

## PROPOSED PATCHES (require author review)

### P4: Reframe |T|^{-1/2} language in abstract and introduction
- **Files:** `manuscript/sections/abstract.tex`, `manuscript/sections/introduction.tex`
- **What:** Add explicit statement that the |T|^{-1/2} scaling is an algebraic consequence of averaging (LLN) and the paper's contribution is empirically confirming it in this network context and quantifying the interpretive consequences.
- **Agent H A1 recommendation**
- **Risk:** Changes thesis framing slightly. Author must approve.

### P5: Replace "unusually proximal" with precise percentile language
- **Files:** `manuscript/sections/abstract.tex`, `manuscript/sections/results.tex`
- **Old:** "unusually proximal"
- **New:** "above the 90th percentile of random probe-pair margins"
- **Agent H A5 recommendation**
- **Risk:** Low. More precise language only.

### P6: Report unconditional discordance prominently
- **Files:** `manuscript/sections/results.tex`
- **What:** Add explicit statement that ~12% of cross-size comparisons show Z-score/d_c rank discordance unconditionally.
- **Agent H A13 recommendation**
- **Risk:** Low. Adds transparency.

### P7: Add δ₀ sweep note or continuous analysis
- **Files:** `manuscript/sections/results.tex`, `manuscript/sections/methods.tex`
- **What:** Justify δ₀=0.3 choice on substantive grounds or add continuous sweep curve.
- **Agent H A4 recommendation**
- **Risk:** Medium. May require regenerating benchmark data.

### P8: Rewrite generate_dataflow.py to read from CSVs
- **File:** `scripts/generate_dataflow.py`
- **What:** Replace hardcoded numeric values (L604, L607) with reads from committed result CSVs.
- **Agent E M1 finding**
- **Risk:** Low. Purely mechanical refactor.

### P9: Reframe biological case study as illustrative example
- **Files:** `manuscript/sections/abstract.tex`, `manuscript/sections/discussion.tex`
- **What:** Demote Hyperforin/Quercetin comparison from "finding" to "illustrative motivated example demonstrating the framework."
- **Agent H A8/A9 recommendation**
- **Risk:** Medium. Changes the paper's emphasis. Author must approve.

---

## NOT APPLIED (deferred / author-decision required)

### D1: DILIrank pilot validation
- **Status:** DEFERRED. Major analysis requiring curated target sets for hundreds of drugs. Frame as future work.

### D2: Full raw STRING rebuild self-containment
- **Status:** DEFERRED. Requires committing large external payloads. Processed parquets are authoritative.

### D3: Delete dili_genes_clean.csv
- **Status:** AUTHOR DECISION. Documented as legacy orphan. No active consumer.

### D4: Add provenance metadata to uniprot_mapping.csv and PubChem cache
- **Status:** AUTHOR DECISION. Minor documentation improvement.

---

## GIT COMMIT PLAN (after patches approved)

```bash
# Stage all untracked release-critical files
git add scripts/run_operating_regime_benchmark.py
git add R/fig8_opregime.R
git add results/tables/operating_regime_*.csv
git add figures/main/fig8_opregime.{pdf,tiff}
git add manuscript/figures/fig8_opregime.{pdf,tiff}
git add tests/test_operating_regime_benchmark.py
git add LICENSE
git add independent_validation/

# Stage remaining untracked audit docs (optional)
git add AUDIT_REPORT.md CLAIM_AUDIT.md LITERATURE_AUDIT.md NARRATIVE_AUDIT.md REPRODUCIBILITY_AUDIT.md CHANGELOG_AUDIT_FIXES.md

# Commit all changes
git add -A
git commit -m "Ultra audit pass: commit operating-regime artifacts, fix LICENSE, apply patch fixes"

# Refresh checksums
shasum -a 256 data/processed/* data/raw/* data/external/* results/*.csv results/tables/*.csv > data/CHECKSUMS.sha256
git add data/CHECKSUMS.sha256

# Rebuild manuscript artifacts
cd manuscript && latexmk -pdf -interaction=nonstopmode main.tex && latexmk -pdf -interaction=nonstopmode main_anonymous.tex
# Rebuild source zip
zip -j submission_source.zip main.tex sections/*.tex references.bib references_extra.bib figures/*.pdf
git add manuscript/main.pdf manuscript/main_anonymous.pdf manuscript/submission_source.zip
git commit -m "Rebuild manuscript PDFs and source zip after audit patches"
```

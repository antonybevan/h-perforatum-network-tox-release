# Changelog — Audit Fixes

## Codex First Pass (2026-06-30)
- Fixed stale leakage background: 99.5th → 99.9th percentile, p=0.006 → p=0.002, max 0.0472 → 0.0580
- Updated operating-regime values from result tables (not hardcoded)
- Corrected figure numbering documentation
- Added operating-regime to verify_numbers.py and reproducibility.lock.yml
- Regenerated manuscript PDFs and source zip
- Removed AI-style figure overlay text

## Claude Code + Hermes Second Pass (2026-07-01)

### Critical Fixes
- Committed operating-regime artifacts (scripts, tables, figures were untracked)
- Added MIT LICENSE file (was untracked, required by README/pyproject/CITATION)
- Removed dead code: `calculate_p_value()` Gaussian approximation (never called)
- Removed orphan data files: `dili_genes_clean.csv`, `network_900_liver_lcc_weighted.parquet`
- Pruned 11 uncited bibliography entries from `references.bib`

### Statistical & Prose Fixes
- Added p-value floor caveat in Methods ("does not discriminate between compounds")
- Qualified perturbation efficiency as "ordinal effect-size ranking" (not cardinal)
- Justified δ₀ = 0.3 threshold (~14% of null-mean closest distance)
- Replaced "unusually proximal" with precise percentile language throughout
- Added unconditional ~12% discordance rate to abstract and results
- Acknowledged LLN mechanism in abstract
- Added ≥700 Z-score reversal to abstract
- Reframed biological case study as "illustrative worked example"
- Consolidated defensive caveats in discussion
- Fixed cover letter: figure reference (5→6), Zenodo DOI future tense

### Reproducibility
- Generated 6 missing supplementary table CSVs (α sweep, floor sweep, S_AB, connectivity, curation, leak controls)
- Fixed `generate_dataflow.py` to read from committed SP table (was hardcoding values)
- Created `FIGURES.md` mapping file for filename-to-LaTeX-number correspondence
- Full pipeline reproduction test: 20/21 steps pass, 18.9 min runtime
- 113/113 unit tests pass, 45/45 checksums OK

### Documentation
- Updated README.md with audit results and repo structure
- Updated AGENTS.md with project context and claim ladder
- Updated DATA_MANIFEST.md (removed orphan entries)
- Archived Codex reports to `independent_validation/codex_pass/`
- Produced 14 audit reports in `independent_validation/claude_pass/`
- Consolidated verdict in `MASTER_AUDIT_DASHBOARD.md`

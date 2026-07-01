# RISK REGISTER — Initial Assessment

**Date:** 2026-07-01
**Status:** PRE-AUDIT baseline

---

## Critical Blockers (must fix before release)

| ID | Risk | Evidence | Severity |
|---|---|---|---|
| R01 | **Operating-regime artifacts are UNTRACKED.** 4 scripts/tables/figures + 1 R script referenced by tracked manuscript, pipeline, and tests are untracked. A `git clone` or `git archive HEAD` produces a broken package. | Claude Code Agent A §4: HEAD has zero operating-regime references. | **CRITICAL** |
| R02 | ~~**Abstract is TRUNCATED.**~~ **FALSE ALARM.** The `[truncated]` flag was a read_file tool artifact, not content truncation. The compiled PDF contains the complete abstract, ending with: "These findings clarify how to interpret network-proximity statistics under target-count asymmetry rather than calling them into question." | Verified via PDF text extraction from compiled main.pdf. Abstract is complete in both source and PDF. | **FALSE ALARM** |
| R03 | **LICENSE file untracked.** MIT code license asserted by README, pyproject.toml, and CITATION.cff but the MIT LICENSE file is untracked. Staged rename moves old CC-BY to LICENSE-CC-BY-4.0 only. | Claude Code Agent A §3: three metadata files assert MIT; LICENSE file is not gitignored but untracked. | **CRITICAL** |

## Major Issues

| ID | Risk | Evidence | Severity |
|---|---|---|---|
| R04 | **Worktree is dirty: 79 modified + 25 untracked files.** The committed HEAD is a different (older) manuscript. A clean release requires a coordinated commit of all changes. | `git status --short` shows 79 modified, 25 untracked. | **MAJOR** |
| R05 | **Hardcoded real-pair values in operating-regime code.** `run_operating_regime_benchmark.py` hardcodes `REAL_DC_SMALL=1.300`, `REAL_DC_LARGE=1.677419`, `REAL_Z_SMALL=-3.861455`, `REAL_Z_LARGE=-5.440302`. If shortest-path tables change, these silently drift. | Codex Agent C §Hardcoding Risks; Codex Agent E §Hardcoded final values. | **MAJOR** |
| R06 | **DILI orphan file.** `data/processed/dili_genes_clean.csv` has 80 genes (missing IL18, IL1R2) and no active consumer. Documented as legacy but risks confusion. | Codex Agent B: FAIL; Claude Code Agent A §7: confirmed 80 genes, no active consumer. | **MAJOR** |
| R07 | **Leakage evidence script times out.** `REVIEWER_EVIDENCE_leakage_scaling.py` could not complete within 120s. Needs longer timeout investigation. | Fresh Hermes run: timed out. | **MAJOR** |
| R08 | **Full raw STRING rebuild not self-contained.** Base STRING downloads are gitignored external payloads. Processed parquet files are effectively authoritative. | Codex Agent B §Network construction: PARTIAL. | **MAJOR** |

## Minor Issues

| ID | Risk | Evidence | Severity |
|---|---|---|---|
| R09 | **pytest: 1 trivial failure.** `test_pandas_version` fails because system Python has pandas 1.3.5 (requires ≥2.0). Not a logic failure. | Fresh pytest run: 113 pass, 1 fail (version check). | **MINOR** |
| R10 | **Stale comment in run_expression_weighted_rwr.py.** Line 36 says `# 9 Hyp, 62 Quer` but canonical data is 10/62. | Codex Agent D §Stale Mismatches. | **MINOR** |
| R11 | **Figure filename/number mismatch.** `fig8_opregime.*` is manuscript Figure 3. Well-documented but easy to mispackage. | Claude Code Agent A §8. | **MINOR** |
| R12 | **docs/DATA_FLOW.md incomplete.** No operating-regime coverage. | Codex Agent A §Missing artifacts. | **MINOR** |
| R13 | **ChEMBL/PubChem cache provenance lacking.** No retrieval timestamps or metadata per entry. | Codex Agent B. | **MINOR** |
| R14 | **DATA_MANIFEST claims Git LFS but .gitattributes says plain blobs.** Documentation contradiction. | Codex Agent A §Missing artifacts. | **MINOR** |
| R15 | **Degree matching: +/-25% window slightly off from exact integer rounding.** Core RWR sampler uses `tol=max(1,int(0.25*d))` vs shortest-path sampler uses `int(.75*d)` to `int(1.25*d)+1` inclusive. Disclosed in methods. | Codex Agent C §Degree matching: Not exact. | **MINOR** |
| R16 | **Operating-regime final-bin merge may violate ≥100 claim.** Codex Agent C found operating bins (1-3,115), (4-5,110), (6-7,25) where last bin has only 25 nodes. | Codex Agent C §Guney ≥100 bins: Caveated. | **MINOR** |

## False Alarms

| ID | Original Concern | Resolution |
|---|---|---|
| F01 | Codex: "submission_source.zip is stale" | Claude Code: Working-tree zip IS current. HEAD zip is stale. False alarm for working tree. |
| F02 | Codex: "untracked count is 20" | Claude Code: 25 untracked files now (5 additional = audit reports). Count drift explained. |

## Author Decisions (not bugs, need author input)

| ID | Decision |
|---|---|
| A01 | Mint Zenodo DOI (promised in Data/Code Availability sections) |
| A02 | Commit all untracked operating-regime artifacts OR document as pre-release state |
| A03 | Decide whether to keep `dili_genes_clean.csv` (legacy orphan) or delete |
| A04 | Add provenance metadata to uniprot_mapping.csv and PubChem SMILES cache |
| A05 | Decide whether to commit raw STRING payloads or keep as external dependency |

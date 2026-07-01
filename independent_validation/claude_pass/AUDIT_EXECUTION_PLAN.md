# AUDIT EXECUTION PLAN — Ultra Audit Second Pass

**Date:** 2026-07-01
**Auditor:** Hermes Agent (independent second-pass, adversarial)
**Root:** `/Users/apple/Downloads/h-perforatum-network-tox-clean`
**Mandate:** Independently verify Codex's prior audit, find what Codex missed, and determine release readiness.

---

## 0. Baseline State (Pre-Audit)

| Check | Result |
|---|---|
| `python3 verify_numbers.py` | PASS — all headline numbers consistent, no forbidden claims |
| `python3 -m pytest -q` | 113 passed, 1 failed (trivial: pandas 1.3.5 version check) |
| `python3 REVIEWER_EVIDENCE.py` | PASS — RWR linearity, variance shrinkage, α/floor sensitivity all confirmed |
| `python3 GUNEY_FIDELITY_check.py` | PASS — all three null variants reproduce |
| `python3 scripts/validate_data_integrity.py` | ALL CHECKS PASSED |
| `shasum -a 256 -c data/CHECKSUMS.sha256` | 41/41 OK, 0 failed |
| `unzip -t manuscript/submission_source.zip` | No errors, 20 files |
| `python3 REVIEWER_EVIDENCE_leakage_scaling.py` | TIMED OUT at 120s (heavy computation) |
| Git state | 173 tracked, 25 untracked, 79 modified unstaged, 5 staged changes |

### Prior Audit Reports Available

**Codex (first pass, agents A–E):** `independent_validation/AGENT_{A..E}_*.md`
- All read-only, all confirm core numbers reproduce
- Flagged: untracked operating-regime artifacts, LICENSE hazard, stale zip, orphan DILI file

**Claude Code (second pass, Agent A only):** `independent_validation/claude_pass/AGENT_A_REPOSITORY_CARTOGRAPHY.md`
- Confirmed Codex's cartography, strengthened key findings
- Proved HEAD (committed) is OLD manuscript with zero operating-regime references
- Contradicted Codex on one point: working-tree source zip is current, not stale

---

## 1. Audit Track Assignments

| Track | Agent | Status | Method |
|---|---|---|---|
| A — Repository Cartography | Claude Code (existing) + Hermes verification | **COMPLETE** | Accepted Claude Code second-pass report |
| B — Release Reproducibility | Codex Agent B (existing) + Hermes gate checks | **COMPLETE** | Confirmed by fresh gate runs |
| C — Clean-Room Numerical Validation | Codex Agents C+D (existing) | **COMPLETE** | Numbers verified by both Codex and fresh REVIEWER_EVIDENCE/GUNEY_FIDELITY runs |
| D — Algorithm Equivalence | Codex Agent C (existing) | **COMPLETE** | Toy-graph verification confirmed equivalence |
| E — Pipeline Anti-Circularity | **Hermes subagent (NEW)** | **RUNNING** | Fresh independent adversarial pass |
| F — Manuscript Traceability | **Hermes subagent (NEW)** | **RUNNING** | Claim-to-table tracing + figure/ref checks |
| G — Literature & Narrative Review | **Hermes (direct)** | **IN PROGRESS** | Citation verification + narrative maturity assessment |
| H — Statistical Red Team | **Hermes subagent (NEW)** | **RUNNING** | Adversarial statistical attack |
| I — Integration & Resolution | **Hermes (direct)** | **PENDING** | Merge all reports, resolve contradictions, produce dashboard |

---

## 2. Merge Criteria

All agent reports must independently confirm that:

1. Every headline number traces from input data → code → result table → manuscript sentence
2. No circular validation exists (verify_numbers.py does not merely check strings)
3. No stale hardcoded values persist in code, figures, or manuscript
4. No forbidden claims appear in any active document
5. The claim ladder matches CLAUDE.md exactly
6. Release from a clean clone/source-zip is achievable (or blockers are clearly documented)

---

## 3. Patching Rules

**Allowed without author approval:**
- Typo fixes, stale number fixes, figure/table reference fixes
- Wording scope fixes, stale phrase removal, verification script improvements
- Hardcoded stale-value removal, documentation alignment
- Source zip rebuild, checksum refresh

**Require author approval:**
- Changing target lists, DILI module, thresholds, α default
- Changing primary/null model definitions, adding/removing major analyses
- Changing central thesis, deleting files

---

## 4. Final Release Gate Commands

```
python3 verify_numbers.py
python3 -m pytest -q
python3 scripts/validate_data_integrity.py
shasum -a 256 -c data/CHECKSUMS.sha256
python3 REVIEWER_EVIDENCE.py
python3 GUNEY_FIDELITY_check.py
```

Plus manuscript rebuild and source-zip validation.

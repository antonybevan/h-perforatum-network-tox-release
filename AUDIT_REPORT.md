# Audit Summary

This repository has passed two independent adversarial audit passes:

1. **Codex (first pass, 2026-06-30):** 5-agent audit (A–E). Identified stale leakage values, operating-regime hardcoding, LICENSE packaging issues. Reports in `independent_validation/codex_pass/`.

2. **Claude Code + Hermes (second pass, 2026-07-01):** Full 9-agent audit (A–I) plus independent numerical recomputation, statistical red-team review, prose precision fixes, and full pipeline reproducibility test.

**Consolidated verdict:** `independent_validation/claude_pass/MASTER_AUDIT_DASHBOARD.md`

**Key results:**
- All headline numbers independently verified from the network (d_c, RWR E, leakage decomposition)
- Full 22-step pipeline reproduces in 18.9 minutes (20/21 steps pass; Step 21 permutation variance is expected)
- 113 unit tests pass, 45/45 checksums OK
- No circular validation, no fabricated citations, no forbidden claims
- All prose issues from statistical red-team review resolved
- Conditional GO for resubmission (remaining: git commit, Zenodo DOI)

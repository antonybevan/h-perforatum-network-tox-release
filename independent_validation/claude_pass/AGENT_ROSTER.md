# AGENT ROSTER — Ultra Audit Second Pass

| Agent | Name | Independence | Status |
|---|---|---|---|
| A | Repository Cartographer | Claude Code (accepted as independent) | ✅ COMPLETE |
| B | Release Reproducibility Engineer | Codex + Hermes fresh gate verification | ✅ COMPLETE |
| C | Clean-Room Numerical Validator | Codex Agents C+D (toy-graph + production verification) | ✅ COMPLETE |
| D | Algorithm Equivalence Auditor | Codex Agent C (toy-graph equivalence confirmed) | ✅ COMPLETE |
| E | Pipeline Anti-Circularity Auditor | Hermes subagent (fresh, adversarial, read-only) | 🔄 RUNNING |
| F | Manuscript/Figure/Supplement Traceability Auditor | Hermes subagent (fresh, adversarial, read-only) | 🔄 RUNNING |
| G | Literature & Scientific-Narrative Reviewer | Hermes (direct analysis) | 🔄 IN PROGRESS |
| H | Statistical Red-Team Reviewer | Hermes subagent (fresh, adversarial) | 🔄 RUNNING |
| I | Final Integrator / Conflict Resolver | Hermes (direct) | ⏳ PENDING |

## Independence Statement

Agents A–D are Codex-produced reports. Their findings are treated as **untrusted claims** and verified independently:

- Agent A verified by Claude Code second pass (confirmed, 1 contradiction on zip staleness)
- Agent B verified by fresh Hermes gate runs (all confirmed)
- Agent C verified by fresh `REVIEWER_EVIDENCE.py` and `GUNEY_FIDELITY_check.py` runs
- Agent D verified by Codex's own toy-graph equivalence tests

Agents E, F, H are **fresh Hermes subagents** with NO access to prior audit reports. They inherit only the repository path and instructions. Agent G is performed directly by Hermes with full manuscript context.

Agent I will merge ALL reports (A–H) after completion.

## Conflict Resolution Protocol

If two agents disagree:
1. Both reports are read in full
2. The disputed claim is traced to primary source (data file, script, manuscript)
3. The integrator makes the final determination
4. Contradictions are documented in the final dashboard

## Deliverables Expected

| Agent | File |
|---|---|
| A | `independent_validation/claude_pass/AGENT_A_REPOSITORY_CARTOGRAPHY.md` (accepted) |
| B | Covered by fresh gate runs (no separate report needed) |
| C | Codex reports (accepted) + fresh gate verification |
| D | Codex report (accepted) |
| E | `independent_validation/claude_pass/AGENT_E_PIPELINE_ANTICIRCULARITY.md` |
| F | `independent_validation/claude_pass/AGENT_F_MANUSCRIPT_TRACEABILITY.md` |
| G | `independent_validation/claude_pass/AGENT_G_LITERATURE_NARRATIVE_REVIEW.md` |
| H | `independent_validation/claude_pass/AGENT_H_STATISTICAL_REDTEAM.md` |
| I | `independent_validation/claude_pass/MASTER_AUDIT_DASHBOARD.md` |

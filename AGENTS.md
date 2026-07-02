# Project Context — h-perforatum-network-tox

Network-medicine manuscript: "Separating effect size from statistical evidence in network-proximity rankings under target-count asymmetry: a controlled liver-interactome audit."

## Claim Ladder

**May claim:**
- Proximity Z-scores are valid evidence statistics
- Z magnitude can diverge from raw effect-size ranking under target-count asymmetry
- Null SD shrinks ≈ |T|^{-1/2} (LLN on averaged statistic)
- Operating-regime benchmark is a liver-network calibration study
- Material rank reversal is conditional and rare for generic probes
- Hyperforin/Quercetin is an illustrative worked example
- Perturbation efficiency is a complementary ordinal effect-size ranking
- Direct target–DILI overlap must be separated from propagated influence

**Must not claim:**
- Proximity is biased; Guney is wrong; RWR escapes shrinkage
- PE predicts DILI; Hyperforin is an intrinsic hepatotoxin
- Compounds are representative; reversals are common; module-invariant

## Key Numbers (STRING ≥900 liver LCC)

| Compound | Targets | d_c | Proximity Z | RWR E | Direct | Propagated |
|---|---|---|---|---|---|---|
| Hyperforin | 10 | 1.30 | −3.86 | 0.1138 | 0.0711 | 0.0427 |
| Quercetin | 62 | 1.68 | −5.44 | 0.0322 | 0.0032 | 0.0290 |

## Repository Gates

```
python verify_numbers.py                     # Number consistency + forbidden-language scan
python -m pytest -q                          # 227 tests
shasum -a 256 -c data/CHECKSUMS.sha256       # Data integrity (39 entries)
python scripts/run_pipeline.py               # Full 22-step pipeline
python REVIEWER_EVIDENCE.py                  # RWR linearity, variance shrinkage
python GUNEY_FIDELITY_check.py               # Canonical proximity revalidation
```


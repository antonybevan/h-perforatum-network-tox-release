# AGENT_D_NUMERICAL_REPRODUCTION_REPORT

Read-only audit completed. I did not edit, create, move, or delete files.

| Claim | Value | Source | Command | Observed | Status |
|---|---:|---|---|---:|---|
| STRING >=900 liver LCC | 7,677 nodes; 66,908 edges | [network_900_liver_lcc.parquet](/Users/apple/Downloads/h-perforatum-network-tox-clean/data/processed/network_900_liver_lcc.parquet) | inline parquet footer/dictionary decoder | 7,677; 66,908 | REPRODUCED |
| STRING >=700 liver LCC | 9,773 nodes; 142,380 edges | [network_700_liver_lcc.parquet](/Users/apple/Downloads/h-perforatum-network-tox-clean/data/processed/network_700_liver_lcc.parquet) | inline parquet decoder | 9,773; 142,380 | REPRODUCED |
| Target counts in analysis LCC | Hyperforin 10; Quercetin 62 | [targets_lcc.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/data/processed/targets_lcc.csv) | `python3` CSV count | 10; 62 | REPRODUCED |
| DILI module counts | >=700: 84; >=900: 82 | [dili_700_lcc.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/data/processed/dili_700_lcc.csv), [dili_900_lcc.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/data/processed/dili_900_lcc.csv) | `python3` CSV count | 84; 82 | REPRODUCED |
| Shortest-path observed `d_c` | >=900 H 1.3000; Q 1.6774 | [run_shortest_path_permutations.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_shortest_path_permutations.py) | inline graph decode + multi-source BFS | 1.3000; 1.6774 | REPRODUCED |
| Shortest-path null/Z | >=900 H null 2.2086+/-0.2353, Z -3.8615; Q 2.1749+/-0.0914, Z -5.4403 | [shortest_path_permutation_results.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/shortest_path_permutation_results.csv) | recalc `(obs-mean)/sd` | exact | VERIFIED |
| Standard RWR PE | >=900 H 0.113809745; Q 0.032171300 | [run_standard_rwr_lcc_permutations.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_standard_rwr_lcc_permutations.py) | inline RWR equation on decoded graph | exact | REPRODUCED |
| EWI PE | >=900 H 0.132974093; Q 0.049344209 | [run_expression_weighted_rwr_permutations.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_expression_weighted_rwr_permutations.py) | inline EWI equation + GTEx liver TPM | exact | REPRODUCED |
| Null-SD scaling | expected sqrt(62/10)=2.48998; observed ratios SP900 2.573, RWR900 2.564, EWI900 2.543 | [null_variance_shrinkage_audit.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/null_variance_shrinkage_audit.csv) | `python3` ratio check | matches | VERIFIED |
| Operating-regime slope | pinned slope -0.499458, CI [-0.502984, -0.495864], R2 0.999928 | [operating_regime_summary.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/operating_regime_summary.csv) | table trace + formula inspection | matches | TRACED |
| Operating-regime reversal | exact R=6.2: directional 0.059892; rank discord 0.119188; conditional d0.3 0.000489; d0.5 0 | [operating_regime_reversal.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/operating_regime_reversal.csv) | `python3` table read | matches | TRACED |
| Leakage decomposition | H raw/direct/prop 0.113810/0.071134/0.042676; Q 0.032171/0.003159/0.029012 | [leakage_decomposition.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/leakage_decomposition.csv) | inline RWR split by target-overlap DILI genes | exact | REPRODUCED |
| Leakage null | background n=1000, mean 0.012982, 95th 0.028064, max 0.057961, p=0.001998 | [leakage_null_distributions.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/leakage_null_distributions.csv) | `python3` quantiles | matches | VERIFIED |
| DILI reduced-module sensitivity | D' n=78; H 0.042676; Q 0.027060; ratio 1.577 | [dili_module_sensitivity.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/dili_module_sensitivity.csv) | inline RWR with four H/DILI overlaps removed | exact | REPRODUCED |
| Guney fidelity | fixed disease H -4.0928, Q -5.3386; two-sided H -3.5511, Q -3.6569 | [GUNEY_FIDELITY_check.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/GUNEY_FIDELITY_check.py) | independent Guney-bin sampler + BFS | matches manuscript-rounded values | REPRODUCED |
| Chemical similarity | DILI+ refs 542; DILI- refs 365; max DILI+ H 0.153846, Q 0.211538; both analog `No` | [chemical_similarity_summary.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/chemical_similarity_summary.csv) | DILIrank workbook count + pairwise matrix aggregation | matches | VERIFIED; RDKit not installed for fingerprint rerun |
| Text-mining sensitivity observed values | >=900 no-TM: H dc/RWR/EWI 1.3000/0.114430/0.133695; Q n=61, 1.6721/0.032868/0.050104 | [string_textmining_sensitivity.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/results/tables/string_textmining_sensitivity.csv) | observed-only rebuild from STRING detailed channels | matches | REPRODUCED_OBS; Z/p traced |

## Stale Mismatches / Notes

- [verify_numbers.py](/Users/apple/Downloads/h-perforatum-network-tox-clean/verify_numbers.py) fails in the default `python3` runtime because `pyarrow`/`fastparquet` are absent. The manual parquet decoder reproduced the relevant counts.
- [scripts/run_expression_weighted_rwr.py:36](/Users/apple/Downloads/h-perforatum-network-tox-clean/scripts/run_expression_weighted_rwr.py:36) has a stale comment: `# 9 Hyp, 62 Quer`; canonical data and recomputation are 10/62.
- [data/processed/dili_genes_clean.csv](/Users/apple/Downloads/h-perforatum-network-tox-clean/data/processed/dili_genes_clean.csv) has 80 rows and appears unreferenced except checksums; active scripts/tables use `dili_700_lcc.csv` and `dili_900_lcc.csv` with 84/82.

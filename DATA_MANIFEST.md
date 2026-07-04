# Data Manifest

This manifest records the current data dependencies and generated artifacts for
the manuscript pipeline. It is intentionally descriptive: it does not change any
scientific method or result.

## External Source Inputs

| Path | Source | Role | Required for regeneration | Notes |
|---|---|---|---|---|
| `data/external/string_links.txt.gz` | STRING v12.0 | Human functional-association edge source | Yes | Ignored by git; must be downloaded separately. |
| `data/external/string_info.txt.gz` | STRING v12.0 | STRING protein-to-gene mapping | Yes | Ignored by git; must be downloaded separately. |
| `data/raw/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct` | GTEx v8 | Liver expression filter and EWI weights | Yes | Tracked in repository. |
| `data/raw/curated_gene_disease_associations.tsv` | DisGeNET curated associations | DILI gene source | Yes | Filtered to Drug-Induced Liver Injury. |
| `data/external/DILIrank_2.0.xlsx` | FDA DILIrank 2.0 | Chemical similarity reference classes | Yes | Used only by chemical similarity control. |
| `data/raw/targets_raw.csv` | Literature and ChEMBL-derived target list | Raw compound targets | Yes | Quercetin rows reproducible via `scripts/retrieve_chembl_targets.py` (CHEMBL159, ChEMBL v31); committed snapshot is authoritative. |
| `data/raw/hyperforin_targets_references.txt` | Manual literature curation | Hyperforin target evidence | Documentation | Does not feed scripts directly. |
| `data/external/uniprot_mapping.csv` | Manual UniProt/gene mapping | Target ID normalization | Yes | Used by `scripts/regenerate_targets.py`. |
| `data/external/9606.protein.links.detailed.v12.0.txt.gz` | STRING v12.0 (per-channel subscores) | Text-mining sensitivity (Huang 2018) | Sensitivity only | Gitignored; download from stringdb-downloads.org. |
| `data/external/string_gene_map.txt.gz` | STRING v12.0 | ENSP -> gene symbol map for sensitivity | Sensitivity only | Gitignored. |

## Processed Data Artifacts

These files are committed as plain repository blobs, with binary/no-text
attributes in `.gitattributes` to preserve checksums. They should not be Git LFS
pointers in the archival package.

| Path | Producer | Consumer | Expected contents |
|---|---|---|---|
| `data/processed/network_700.parquet` | `scripts/extract_string_network.py` | LCC construction | STRING >=700 edges. |
| `data/processed/network_900.parquet` | `scripts/extract_string_network.py` | LCC construction | STRING >=900 edges. |
| `data/processed/liver_proteome.csv` | `scripts/create_lcc_filtered_data.py` | LCC/DILI filtering, tests | Genes with liver TPM >=1. |
| `data/processed/targets.csv` | `scripts/regenerate_targets.py` | LCC target filtering | Human mapped targets. |
| `data/processed/targets_lcc.csv` | `scripts/create_lcc_filtered_data.py` | All network analyses | 10 Hyperforin and 62 Quercetin LCC targets. |
| `data/processed/network_700_liver_lcc.parquet` | `scripts/create_lcc_filtered_data.py` | RWR/EWI/shortest path | Liver-expressed >=700 LCC. |
| `data/processed/network_900_liver_lcc.parquet` | `scripts/create_lcc_filtered_data.py` | RWR/EWI/shortest path/bootstrap | Liver-expressed >=900 LCC. |
| `data/processed/dili_700_lcc.csv` | `scripts/regenerate_dili.py` | RWR/EWI/shortest path | DILI genes present in >=700 LCC. |
| `data/processed/dili_900_lcc.csv` | `scripts/regenerate_dili.py` | RWR/EWI/shortest path/bootstrap | DILI genes present in >=900 LCC. |
| `data/processed/dilirank_smiles_cache.json` | `scripts/run_chemical_similarity_control.py` | Chemical similarity | PubChem SMILES cache, including empty strings for misses. |

## Result Tables

| Path | Producer | Manuscript/Figure consumer |
|---|---|---|
| `results/tables/shortest_path_permutation_results.csv` | `scripts/run_shortest_path_permutations.py` | Figures 1-2, Table 1, Supplementary Tables S3/S6. |
| `results/tables/standard_rwr_lcc_permutation_results.csv` | `scripts/run_standard_rwr_lcc_permutations.py` | Figures 2 and 4, Table 1, Supplementary Tables S3/S6. |
| `results/tables/expression_weighted_rwr_permutation_results.csv` | `scripts/run_expression_weighted_rwr_permutations.py` | Figures 4-5, Table 1, Supplementary Tables S3/S6. |
| `results/tables/expression_weighted_rwr_results.csv` | `scripts/run_expression_weighted_rwr.py` | Auxiliary RWR/EWI comparison table. |
| `results/bootstrap_sensitivity.csv` | `scripts/run_bootstrap_sensitivity.py` | Supplementary Figure S1 density plot. |
| `results/tables/bootstrap_summary.csv` | `scripts/run_bootstrap_sensitivity.py` | Supplementary Figure S1 baseline subset-control summary. |
| `results/tables/ewi_bootstrap_summary.csv` | `scripts/run_ewi_bootstrap_sensitivity.py` | EWI robust-ratio support. |
| `results/chemical_similarity_control.csv` | `scripts/run_chemical_similarity_control.py` | Full chemical similarity matrix. |
| `results/tables/chemical_similarity_summary.csv` | `scripts/run_chemical_similarity_control.py` | Figure 7 chemical-similarity control. |
| `results/tables/dilirank_reference_set.csv` | `scripts/run_chemical_similarity_control.py` | DILIrank reference audit. |
| `results/tables/consolidated_results.csv` | `scripts/consolidate_results.py` | Loaded by `R/01_load_data.R`. |
| `results/tables/pvalue_convention_audit.csv` | `scripts/audit_statistical_conventions.py` | Reviewer-response audit comparing empirical `r/n`, conservative empirical `(r+1)/(n+1)`, and Gaussian-tail p-values. |
| `results/tables/null_variance_shrinkage_audit.csv` | `scripts/audit_statistical_conventions.py` | Reviewer-response audit quantifying target-count-associated null standard deviation ratios. |
| `results/tables/dili_module_sensitivity.csv` | `scripts/run_dili_module_sensitivity.py` | Direct-overlap sensitivity values for Results and Supplementary Table S12. |
| `results/tables/leakage_decomposition.csv` | `scripts/generate_leakage_figure_data.py` | Figure 6 direct/propagated decomposition. |
| `results/leakage_null_distributions.csv` | `scripts/generate_leakage_figure_data.py` | Figure 6 leakage-control background and Quercetin-subset distributions. |
| `results/tables/target_evidence.csv` | Manual curation table | Target evidence provenance used by manuscript/supplementary documentation. |
| `results/tables/string_textmining_sensitivity.csv` | `scripts/run_string_textmining_sensitivity.py` | Supplementary STRING text-mining robustness (full rebuild vs no-text-mining; Huang 2018 method). |
| `results/tables/operating_regime_moments.csv` | `scripts/run_operating_regime_benchmark.py` | Figure 3A/B and operating-regime summary. |
| `results/tables/operating_regime_reversal.csv` | `scripts/run_operating_regime_benchmark.py` | Supplementary operating-regime reversal-rate table. |
| `results/tables/operating_regime_plane.csv` | `scripts/run_operating_regime_benchmark.py` | Figure 3C probe-pair operating plane. |
| `results/tables/operating_regime_summary.csv` | `scripts/run_operating_regime_benchmark.py` | Figure 3 annotations and Results operating-regime values. |

## Figures And Manuscript Assets

| Path | Producer | Notes |
|---|---|---|
| `figures/main/fig1_lollipop.*` | `R/fig1_lollipop.R` | Main Figure 1. |
| `figures/main/fig2_dumbbell.*` | `R/fig2_dumbbell.R` | Main Figure 2. |
| `figures/main/fig3_ewi_waterfall.*` | `R/fig3_ewi_waterfall.R` | Main Figure 5. |
| `figures/main/fig4_ptni_phase.*` | `R/fig4_ptni_phase.R` | Main Figure 4. |
| `figures/main/fig5_bootstrap.*` | `R/fig5_bootstrap.R` | Supplementary Figure S1 baseline subset-control plot. |
| `figures/main/fig6_chemsim.*` | `R/fig6_chemsim.R` | Main Figure 7 chemical-similarity control. |
| `figures/main/fig7_leakage.*` | `R/fig7_leakage.R` | Main Figure 6 leakage/decomposition audit. |
| `figures/main/fig8_opregime.*` | `R/fig8_opregime.R` | Main Figure 3 operating-regime calibration benchmark. |

## Current Known Non-Generated Items

- ChEMBL target retrieval (Quercetin) is documented and reproducible via
  `scripts/retrieve_chembl_targets.py` (`--verify` diffs a fresh retrieval against
  the committed snapshot); `data/raw/targets_raw.csv` remains the authoritative
  ChEMBL v31 snapshot, because the ChEMBL REST API serves the current release.
- Raw STRING downloads are required for a clean full rebuild but are not tracked.
- The STRING no-text-mining sensitivity requires two gitignored STRING v12.0
  per-channel downloads listed above; the committed sensitivity table is the
  authoritative result if those files are absent.
- `data/external/uniprot_mapping.csv` is a manual normalization table and does
  not carry per-entry retrieval metadata.
- `data/processed/dilirank_smiles_cache.json` is an authoritative PubChem cache
  for this analysis, but it does not store CID/retrieval timestamp/miss-reason
  metadata per entry.
- Several manuscript supplementary tables are hand-authored rather than emitted
  directly from result CSVs.

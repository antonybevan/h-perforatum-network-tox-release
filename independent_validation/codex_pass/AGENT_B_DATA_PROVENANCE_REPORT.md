# AGENT_B_DATA_PROVENANCE_REPORT

Audit target: `/Users/apple/Downloads/h-perforatum-network-tox-clean` current filesystem snapshot. Prior audit docs were not used as evidence.

## Findings

| Area | Status | Finding |
|---|---:|---|
| Checksums | PASS | `shasum -a 256 -c /Users/apple/Downloads/h-perforatum-network-tox-clean/data/CHECKSUMS.sha256` returned OK for every listed artifact. |
| Checksum coverage | PARTIAL | The checksum file includes four untracked operating-regime result CSVs, and excludes local gitignored STRING payloads plus `data/CHECKSUMS.sha256` itself. |
| Target lineage | PASS | Raw targets: 136 rows, Hyperforin 14 / Quercetin 122. Processed: 101 rows, 14 / 87. LCC: 72 rows, 10 / 62. No raw duplicate compound-protein rows; no duplicate processed compound-gene rows. |
| ChEMBL provenance | PARTIAL | `scripts/retrieve_chembl_targets.py` documents CHEMBL159, ChEMBL v31, human IC50/Ki/EC50 <= 10 uM, but the raw ChEMBL activity/assay/target-component payload is not archived. Live `--verify` was attempted but hung in API target lookup and was interrupted. |
| UniProt provenance | PARTIAL | `/data/external/uniprot_mapping.csv` has 109 manual mapping entries and drives target normalization, but lacks per-entry source IDs, retrieval dates, or UniProt release/version metadata. |
| Network construction | PARTIAL | Processed parquet metadata is internally coherent and checksummed: `network_700` 236,712 rows; `network_900` 100,383 rows; liver LCCs 142,380 and 66,908 rows. But legacy raw `string_links.txt.gz` and `string_info.txt.gz` are absent, and the current extraction script does not byte-reproduce the committed schemas. |
| External STRING sensitivity payloads | PARTIAL | Gitignored `9606.protein.links.detailed.v12.0.txt.gz` and `string_gene_map.txt.gz` are locally present, gzip-valid, and have SHA-256 values matching prose provenance, but they are not tracked or in `CHECKSUMS.sha256`. |
| DILI module | PASS | DisGeNET source has 26,522 rows; filtering `diseaseName == "Drug-Induced Liver Injury"` gives 127 unique genes, all `umls:C0860207`. LCC modules are 84 genes at >=700 and 82 at >=900. |
| DILI orphan artifact | FAIL | `/data/processed/dili_genes_clean.csv` is checksummed but not produced or consumed by current scripts; it has 80 genes and omits `IL18` and `IL1R2` present in `dili_900_lcc.csv`. |
| Expression filter | PASS | GTEx file has 56,200 rows; `liver_proteome.csv` has 13,496 unique gene symbols matching GTEx Liver TPM >= 1. Duplicated GTEx symbols are implicitly overwritten by last occurrence; document this policy. |
| DILIrank/PubChem chemical similarity | PASS | DILIrank 2.0 file has 1,336 rows: vMost 217, vLess 351, vNo 414, ambiguous 354. Reference set has 542 DILI-positive and 365 DILI-negative drugs; pairwise matrix has 1,814 rows. Summary values recompute from matrix. |
| PubChem cache provenance | PARTIAL | SMILES cache has 982 names: 907 nonempty, 75 empty. It lacks retrieval timestamp, PubChem CID/property metadata per reference drug, and miss reason fields. |
| Orphan/manual artifacts | PARTIAL | `network_900_liver_lcc_weighted.parquet` and `results/tables/target_evidence.csv` are tracked/checksummed or used as evidence, but no producing script was found. |

## Key Exact Files

Primary data inspected: `/Users/apple/Downloads/h-perforatum-network-tox-clean/data/CHECKSUMS.sha256`, `/data/raw/targets_raw.csv`, `/data/external/uniprot_mapping.csv`, `/data/processed/targets.csv`, `/data/processed/targets_lcc.csv`, `/data/raw/curated_gene_disease_associations.tsv`, `/data/raw/dili_genes_raw.csv`, `/data/processed/dili_700_lcc.csv`, `/data/processed/dili_900_lcc.csv`, `/data/processed/dili_genes_clean.csv`, `/data/raw/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct`, `/data/external/DILIrank_2.0.xlsx`, `/data/processed/dilirank_smiles_cache.json`, `/results/chemical_similarity_control.csv`, `/results/tables/chemical_similarity_summary.csv`, `/results/tables/dilirank_reference_set.csv`.

Primary scripts inspected: `/scripts/extract_string_network.py`, `/scripts/regenerate_targets.py`, `/scripts/retrieve_chembl_targets.py`, `/scripts/create_lcc_filtered_data.py`, `/scripts/regenerate_dili.py`, `/scripts/run_chemical_similarity_control.py`, `/scripts/run_string_textmining_sensitivity.py`, `/scripts/run_pipeline.py`.

## Commands Inspected

```bash
git status --short
rg --files
find . -maxdepth 3 -type f \( -iname '*manifest*' -o -iname '*checksum*' -o -iname '*provenance*' -o -iname '*.md' \) -print | sort
sed -n '1,260p' DATA_MANIFEST.md DATA_PROVENANCE.md
shasum -a 256 -c data/CHECKSUMS.sha256
find data -type f -maxdepth 3 -print0 | xargs -0 shasum -a 256
git ls-files data results | sort
git check-ignore -v data/external/9606.protein.links.detailed.v12.0.txt.gz data/external/string_gene_map.txt.gz data/external/string_links.txt.gz data/external/string_info.txt.gz
gzip -t data/external/9606.protein.links.detailed.v12.0.txt.gz data/external/string_gene_map.txt.gz
python3 scripts/validate_data_integrity.py
python3 scripts/run_string_textmining_sensitivity.py --validate-only
python3 scripts/retrieve_chembl_targets.py --verify
```

The first two Python validation commands failed because the current interpreter lacks `networkx`; parquet loading is also unavailable because `pyarrow/fastparquet` are absent. I used read-only CSV/XLSX inspections and a read-only Parquet footer parser for row/schema metadata.

## Unresolved Author Decisions

1. Decide whether committed STRING parquet files are authoritative snapshots only, or provide exact raw STRING inputs plus a script that reproduces their current schemas.
2. Either remove/label legacy `dili_genes_clean.csv`, or document its producer and intended use.
3. Archive ChEMBL v31 raw retrieval payloads or state clearly that `targets_raw.csv` is the authoritative non-reconstructable snapshot.
4. Add per-entry provenance for `uniprot_mapping.csv`.
5. Add PubChem cache metadata: retrieval date, CID, canonical SMILES source, and miss reason.
6. Document GTEx duplicate-symbol handling.
7. Decide whether gitignored STRING sensitivity payloads should be tracked, externally archived, or excluded from reproducibility claims.

# AGENT_A_REPOSITORY_CARTOGRAPHER_REPORT

Root audited: `/Users/apple/Downloads/h-perforatum-network-tox-clean`
Mode: read-only. No files edited, moved, deleted, patched, created, or tests run by this agent.

## 1. File Inventory By Category

| Category | Current inventory | Classification |
|---|---:|---|
| Git-tracked files | 173 | Baseline repository package |
| Untracked files | 20 | Mixed: active new artifacts plus audit docs |
| Non-`.git` files found | 249 | Includes ignored caches/build outputs |
| `/data/raw` | 5 files, 20M | Canonical raw inputs |
| `/data/external` | 4 files, 135M | Mixed canonical external inputs and ignored sensitivity inputs |
| `/data/processed` | 12 files, 2.2M | Canonical processed inputs |
| `/results` | 3 CSV files | Generated canonical result matrices/distributions |
| `/results/tables` | 19 CSV files | Generated canonical manuscript/result tables |
| `/scripts` | 28 Python files | Active pipeline plus legacy/helper scripts |
| `/src/network_tox` | 24 files incl. ignored caches | Canonical package code plus generated caches |
| `/R` | 10 R files | Active figure-generation layer |
| `/figures/main` | 16 files | Generated canonical figure PDFs/TIFFs |
| `/manuscript` | 57 source/build/figure files | Canonical manuscript package plus LaTeX build byproducts |
| `/tests` | 28 files incl. ignored caches | Active validation suite plus generated caches |
| `/docs` | 1 markdown file | Generated/supporting documentation |
| `/.github` | 6 files | CI/supporting metadata |
| repository root | 36 files | README/config/licenses/docs/audit notes |

Important current git state:
- Staged: `LICENSE -> LICENSE-CC-BY-4.0`, plus deletion of four old supplementary figure files under `/figures/supplementary`.
- Unstaged modified: manuscript, result, figure, script, test, checksum, docs, and config files.
- Untracked active artifacts: `/scripts/run_operating_regime_benchmark.py`, `/R/fig8_opregime.R`, four `/results/tables/operating_regime_*.csv`, and `fig8_opregime` PDFs/TIFFs in both figure directories.
- Untracked support/audit docs: `AUDIT_REPORT.md`, `CLAIM_AUDIT.md`, `LITERATURE_AUDIT.md`, `NARRATIVE_AUDIT.md`, `REPRODUCIBILITY_AUDIT.md`, `CHANGELOG_AUDIT_FIXES.md`.
- Ignored present: `.DS_Store`, `.pytest_cache`, `__pycache__`, LaTeX `.aux/.bbl/.blg/.log/.out/.fls/.fdb_latexmk`, and two large STRING sensitivity inputs.

## 2. Active/Generated/Supporting/Stale/Dangerous Classification

Canonical active source:
- `/src/network_tox/**`: RWR, expression-weighted RWR, shortest-path/proximity, network, permutation, validators/loaders.
- `/scripts/run_pipeline.py`: declared 22-step orchestration graph.
- Active analysis producers: `run_standard_rwr_lcc_permutations.py`, `run_expression_weighted_rwr_permutations.py`, `run_shortest_path_permutations.py`, `run_bootstrap_sensitivity.py`, `run_ewi_bootstrap_sensitivity.py`, `run_chemical_similarity_control.py`, `audit_statistical_conventions.py`, `run_dili_module_sensitivity.py`, `generate_leakage_figure_data.py`, `run_string_textmining_sensitivity.py`, `run_operating_regime_benchmark.py`, `consolidate_results.py`.
- `/R/fig1_lollipop.R` through `/R/fig8_opregime.R` plus `/R/00_setup_pub.R` and `/R/01_load_data.R`.
- `/manuscript/main.tex`, `/manuscript/main_anonymous.tex`, `/manuscript/sections/*.tex`, bibliography files, and synchronized manuscript figures.

Generated canonical artifacts:
- `/data/processed/*`, `/results/*.csv`, `/results/tables/*.csv`, `/figures/main/*`, `/manuscript/figures/*`, `/manuscript/main.pdf`, `/manuscript/main_anonymous.pdf`, `/manuscript/submission_source.zip`, `/docs/DATA_FLOW.md`, `/data/CHECKSUMS.sha256`.
- Checksum verification passed for the current working tree, including the new operating-regime tables.

Supporting:
- `/README.md`, `/DATA_MANIFEST.md`, `/DATA_PROVENANCE.md`, `/CITATION.cff`, `/RESPONSE_TO_REVIEWERS.md`, `/GUNEY_FIDELITY_REVALIDATION.md`, `/requirements-lock.txt`, `/reproducibility.lock.yml`, `/tests/**`, `/.github/workflows/tests.yml`.

Stale/legacy/orphan candidates:
- `/scripts/curate_targets.py` and `/scripts/filter_liver_network.py`: older/side-path utilities, not in the current 22-step pipeline.
- `/data/processed/dili_genes_clean.csv`: processed DILI derivative not found as an active consumer.
- `/data/processed/network_900_liver_lcc_weighted.parquet`: no active consumer found by text search.
- `/results/tables/expression_weighted_rwr_results.csv` and `/results/tables/ewi_bootstrap_summary.csv`: auxiliary/supporting, not primary manuscript figure inputs.
- Staged-deleted `/figures/supplementary/fig3_slope.*` and `/figures/supplementary/fig7_ewi_comparison.*`: legacy figure artifacts.
- Root audit markdowns are untracked and were not trusted as audit evidence.

Dangerous/packaging-sensitive:
- `/LICENSE` is an untracked MIT license while staged git state renames the old tracked `LICENSE` to `/LICENSE-CC-BY-4.0`; publishing without adding `/LICENSE` would leave README's MIT code-license claim unsupported.
- Active manuscript references `/manuscript/figures/fig8_opregime.pdf`, but the script, result tables, and figure files for fig8 are untracked.
- `/data/CHECKSUMS.sha256` includes untracked operating-regime tables; the checksum passes only for this working tree, not necessarily for HEAD or a partial commit.
- Ignored LaTeX/cache files are present and should not enter archival packaging.

## 3. Execution DAG

Raw/external inputs:
1. STRING base downloads `string_links.txt.gz` + `string_info.txt.gz` -> `/scripts/extract_string_network.py` -> `/data/processed/network_700.parquet`, `/data/processed/network_900.parquet`.
2. GTEx liver GCT + STRING networks -> `/scripts/create_lcc_filtered_data.py` -> `/data/processed/liver_proteome.csv`, `/data/processed/network_700_liver_lcc.parquet`, `/data/processed/network_900_liver_lcc.parquet`, `/data/processed/targets_lcc.csv`.
3. `/data/raw/targets_raw.csv` + `/data/external/uniprot_mapping.csv` -> `/scripts/regenerate_targets.py` -> `/data/processed/targets.csv`.
4. `/data/raw/curated_gene_disease_associations.tsv` -> `/scripts/regenerate_dili.py` -> `/data/raw/dili_genes_raw.csv`, `/data/processed/dili_700_lcc.csv`, `/data/processed/dili_900_lcc.csv`.
5. `/data/external/DILIrank_2.0.xlsx` + SMILES cache -> `/scripts/run_chemical_similarity_control.py` -> `/results/chemical_similarity_control.csv`, `/results/tables/chemical_similarity_summary.csv`, `/results/tables/dilirank_reference_set.csv`.
6. Ignored STRING detailed files `/data/external/9606.protein.links.detailed.v12.0.txt.gz` + `/data/external/string_gene_map.txt.gz` -> `/scripts/run_string_textmining_sensitivity.py` -> `/results/tables/string_textmining_sensitivity.csv`.

Processed inputs to results:
1. LCC networks + targets + DILI genes -> standard RWR, EWI, shortest-path permutation scripts -> three primary permutation tables.
2. Same inputs -> bootstrap/EWI-bootstrap/leakage/module-sensitivity/statistical-audit scripts -> bootstrap, leakage, null-variance, p-value, and sensitivity tables.
3. Same inputs -> `/scripts/run_operating_regime_benchmark.py` -> four operating-regime tables.
4. Primary result tables + bootstrap + chemical summary -> `/scripts/consolidate_results.py` -> `/results/tables/consolidated_results.csv`.
5. `verify_numbers.py`, `REVIEWER_EVIDENCE*.py`, and `GUNEY_FIDELITY_check.py` are audit/check scripts; they print/verify rather than producing canonical CSVs.

Results to figures:
- `fig1_lollipop`: shortest-path table.
- `fig2_dumbbell`: shortest-path + standard RWR tables.
- `fig8_opregime`: operating-regime tables; filename is `fig8` but manuscript labels it main Figure 3.
- `fig4_ptni_phase`: RWR + EWI permutation tables.
- `fig3_ewi_waterfall`: RWR + EWI permutation tables.
- `fig7_leakage`: leakage decomposition + leakage null distributions.
- `fig6_chemsim`: chemical-similarity summary.
- `fig5_bootstrap`: bootstrap sensitivity + bootstrap summary; used as supplementary figure.

Figures/manuscript:
- R scripts save PDFs and TIFFs to both `/figures/main` and `/manuscript/figures`.
- `/manuscript/main.tex` and `/manuscript/main_anonymous.tex` include the synchronized manuscript PDFs.
- `/manuscript/submission_source.zip` currently contains `main.tex`, section files, bibliography files, and figure PDFs including `fig8_opregime.pdf`.

## 4. Missing Or Ambiguous Artifacts

- Missing for a clean base-network rebuild: `/data/external/string_links.txt.gz` and `/data/external/string_info.txt.gz`.
- Present but ignored sensitivity inputs: `/data/external/9606.protein.links.detailed.v12.0.txt.gz` and `/data/external/string_gene_map.txt.gz`.
- `/docs/DATA_FLOW.md` appears incomplete relative to the current 22-step pipeline: no operating-regime coverage was found, despite the README/manuscript now depending on it.
- `/DATA_MANIFEST.md` says processed files are expected Git LFS payloads, while `/.gitattributes` says data artifacts are committed as plain blobs. This is a documentation contradiction.
- Some supplementary tables are hand-authored in LaTeX rather than generated directly from CSVs; tests and `verify_numbers.py` partially guard this, but the table-generation DAG is not fully machine-owned.
- Local ambient `python3` lacked `pyarrow`/`fastparquet`, so parquet schemas were not independently read during this audit. The parquet files are checksummed and project requirements include `pyarrow`.

## 5. Critical Risks

1. The repository is not in a publishable clean state: staged, unstaged, untracked, and ignored generated artifacts coexist.
2. The current manuscript depends on untracked operating-regime code/tables/figures; a commit or archive that omits untracked files will break reproduction and manuscript compilation.
3. License state is dangerous: MIT `/LICENSE` is untracked while CC-BY is staged as the tracked license file.
4. Full raw-to-network regeneration is not self-contained from tracked files because base STRING raw downloads are absent; processed networks are effectively authoritative binary inputs.
5. The checksum manifest validates the current working tree, not the committed repository state.
6. `/docs/DATA_FLOW.md` is no longer a complete execution graph for the active manuscript.
7. Figure numbering is semantically reordered: `fig8_opregime` is manuscript Figure 3. This is workable but easy to mispackage or misread.
8. Ignored build artifacts and caches are present; archival/export tooling must avoid sweeping them in.

## Key Commands Run

```bash
pwd
git status --porcelain=v1
git diff --cached --name-status
git diff --name-status
git ls-files --others --exclude-standard
git status --ignored --short
rg --files
find . -maxdepth 3 -type d | sort
du -sh . data data/raw data/processed data/external results results/tables figures manuscript scripts R src tests docs
sed -n '1,260p' README.md
sed -n '1,260p' scripts/run_pipeline.py
sed -n '1,240p' manuscript/main.tex
rg -n "(read_csv|read_parquet|to_csv|to_parquet|ggsave|includegraphics|operating_regime|fig8)" R scripts src tests manuscript
python3 - <<'PY'  # read-only CSV/result-table shape inventory
shasum -a 256 -c data/CHECKSUMS.sha256
zipinfo -1 manuscript/submission_source.zip
```

Failed/non-portable read-only probes:
```bash
find ... -printf   # failed: BSD find lacks -printf
python             # failed: command not found
python3 parquet read # failed: missing pyarrow/fastparquet in ambient Python
```

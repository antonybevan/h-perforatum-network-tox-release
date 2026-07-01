# AGENT A — REPOSITORY CARTOGRAPHY (Independent second-pass audit)

Auditor: independent adversarial pass (Claude). Mode: READ-ONLY. No tracked file modified.
Root: `/Users/apple/Downloads/h-perforatum-network-tox-clean`
Date observed: 2026-06-30. Repo HEAD: `1788f84 Recompile full manuscript (24pp; ...)`.

This report independently re-derives the repository map and **challenges** Codex's
`independent_validation/AGENT_A_REPOSITORY_CARTOGRAPHER_REPORT.md`. Every claim below is
backed by real command output captured during this pass.

---

## 0. Headline

The repository's *intended* release (the working tree) and its *committed* state (HEAD)
are two **different papers**. HEAD is the older 7-main-figure manuscript with **zero**
references to the operating-regime benchmark. The working tree adds an entire new analysis
(manuscript Figure 3 = "operating regime"), but that analysis lives in a mix of **untracked
new files** and **uncommitted modifications**. A naive `git commit` of only the staged
changes, a `git archive HEAD`, or a fresh clone/checkout would therefore ship a **broken or
stale** package: the manuscript would not compile, the pipeline would reference a missing
script, two tracked test/verify scripts would raise `FileNotFoundError`, and `shasum -c`
would fail on four files. This is the central cartographic risk and it is a **release
process** risk, not a science risk — all artifacts exist in the working tree and only need
`git add` + commit.

---

## 1. Raw git state (verbatim)

`git diff --cached --name-status` (STAGED):
```
R100	LICENSE	LICENSE-CC-BY-4.0
D	figures/supplementary/fig3_slope.pdf
D	figures/supplementary/fig3_slope.tiff
D	figures/supplementary/fig7_ewi_comparison.pdf
D	figures/supplementary/fig7_ewi_comparison.tiff
```

`git ls-files --others --exclude-standard` (UNTRACKED, release-relevant subset):
```
LICENSE                                   <- MIT (code license)
R/fig8_opregime.R                          <- generates manuscript Figure 3
scripts/run_operating_regime_benchmark.py  <- pipeline step producer
tests/test_operating_regime_benchmark.py   <- test
results/tables/operating_regime_moments.csv
results/tables/operating_regime_plane.csv
results/tables/operating_regime_reversal.csv
results/tables/operating_regime_summary.csv
figures/main/fig8_opregime.pdf  / .tiff
manuscript/figures/fig8_opregime.pdf / .tiff
AUDIT_REPORT.md CLAIM_AUDIT.md LITERATURE_AUDIT.md NARRATIVE_AUDIT.md
REPRODUCIBILITY_AUDIT.md CHANGELOG_AUDIT_FIXES.md  <- Codex audit docs (support only)
independent_validation/AGENT_{A..E}_*.md            <- Codex reports
```
Counts: tracked files = **173**; untracked (excl. ignored) = **25** (Codex AGENT_A reported
20 — the delta is the now-present `independent_validation/` audit reports, not new source).

`git diff --name-status` (UNSTAGED modified): 70+ files spanning the whole manuscript,
all 7 R figure scripts, all figure PDFs/TIFFs in `figures/main` and `manuscript/figures`,
`scripts/run_pipeline.py`, `scripts/consolidate_results.py`, `tests/test_result_tables.py`,
`tests/test_figure_outputs.py`, `verify_numbers.py`, `data/CHECKSUMS.sha256`,
`manuscript/submission_source.zip`, `pyproject.toml`, `reproducibility.lock.yml`, etc.

---

## 2. Release-sensitive file classification

| File / group | State | Classification |
|---|---|---|
| `src/network_tox/**` | tracked | active-required |
| `scripts/run_pipeline.py` (mod) | tracked-modified | active-required (now references untracked op-regime script) |
| `scripts/run_operating_regime_benchmark.py` | **untracked** | active-required, **dangerous-if-omitted** |
| `R/fig1..fig7_*.R` (mod) | tracked-modified | active-required |
| `R/fig8_opregime.R` | **untracked** | active-required, **dangerous-if-omitted** |
| `results/tables/operating_regime_*.csv` (×4) | **untracked** | generated-required, **dangerous-if-omitted** (consumed by tracked tests + verify + figure) |
| `figures/main/fig8_opregime.*`, `manuscript/figures/fig8_opregime.*` | **untracked** | generated-required, **dangerous-if-omitted** (manuscript Figure 3) |
| `tests/test_operating_regime_benchmark.py` | **untracked** | active-undocumented test |
| `tests/test_result_tables.py`, `verify_numbers.py` (mod) | tracked-modified | active-required; **read the untracked op-regime CSVs** |
| `LICENSE` (MIT) | **untracked** | dangerous-if-omitted (code license; asserted by README/pyproject/CITATION) |
| `LICENSE-CC-BY-4.0` (CC-BY) | staged rename | active-required (docs/data license) |
| `manuscript/main.tex` / `main_anonymous.tex` (mod) | tracked-modified | active-required (now `\includegraphics{figures/fig8_opregime.pdf}`) |
| `manuscript/submission_source.zip` (mod) | tracked-modified | generated-required (working copy current; HEAD copy stale — see §6) |
| `data/processed/dili_genes_clean.csv` | tracked | stale/legacy (documented orphan — see §7) |
| `figures/supplementary/fig3_slope.*`, `fig7_ewi_comparison.*` | staged-deleted | stale/legacy (clean removal — see §8) |
| `AUDIT_REPORT.md`, `CLAIM_AUDIT.md`, `*_AUDIT.md`, `CHANGELOG_AUDIT_FIXES.md` | **untracked** | support docs (not release-critical) |
| LaTeX `.aux/.bbl/.fls/.fdb_latexmk/.log`, `.DS_Store`, `__pycache__` | ignored/present | build byproducts — must not be archived |

---

## 3. Investigation 1 — LICENSE (dual-license packaging hazard)

The index renames HEAD's `LICENSE` (Creative Commons content) to `LICENSE-CC-BY-4.0`, and a
**new untracked `LICENSE` carrying MIT text** sits in the working tree. Verified by content:

```
$ head LICENSE                      -> "MIT License / Copyright (c) 2026 Antony Bevan ..."
$ git show :LICENSE-CC-BY-4.0       -> "Creative Commons Attribution 4.0 International ..."
$ git check-ignore LICENSE          -> (not ignored; addable)
```

The dual-license intent is asserted in **three** metadata files:
- `README.md:4` MIT badge → `opensource.org/licenses/MIT`; `README.md:5` CC-BY 4.0 for docs/data.
- `pyproject.toml:8` `license = "MIT"`.
- `CITATION.cff:36-38` `license: [MIT, CC-BY-4.0]`.

**Risk:** a commit of staged-only changes, or `git archive HEAD`, ships `LICENSE-CC-BY-4.0`
(CC-BY) **without any MIT code license**, contradicting README/pyproject/CITATION. Fix is one
line (`git add LICENSE`), but until then the code-license claim is unbacked in the committed
tree. **Severity: major. codex_status: confirms_codex** (I add the three corroborating
metadata assertions and confirm the file is not gitignored).

---

## 4. Investigation 2 — Untracked operating-regime artifacts are referenced by tracked code

`HEAD` contains **zero** references to `operating_regime`/`fig8_opregime`
(`git grep -l 'operating_regime\|fig8_opregime' HEAD` → empty). The working tree references
them from **tracked** files:

```
manuscript/main.tex:107          \includegraphics{figures/fig8_opregime.pdf}   (label fig:opregime)
manuscript/main_anonymous.tex:105 \includegraphics{figures/fig8_opregime.pdf}
scripts/run_pipeline.py:165-171  step → run_operating_regime_benchmark.py → 4 op-regime CSVs
tests/test_result_tables.py:123,135,149,156  _read("operating_regime_*.csv")
verify_numbers.py:40,83-85       op_sum/op_rev/op_mom = pd.read_csv("operating_regime_*.csv")
tests/test_figure_outputs.py:23  "fig8_opregime"
README.md:51                     "... R/fig8_opregime.R ..."
```

Every one of those targets is **untracked**. Consequence of releasing from HEAD or
staged-only commit:
- `pdflatex manuscript/main.tex` fails (missing `manuscript/figures/fig8_opregime.pdf`).
- `run_pipeline.py` step references a non-existent script.
- `pytest tests/test_result_tables.py` and `python verify_numbers.py` raise `FileNotFoundError`.
- `shasum -a 256 -c data/CHECKSUMS.sha256` fails on 4 missing files.

**Severity: major. codex_status: confirms_codex** (Codex flagged the dependency; I additionally
proved HEAD is the older manuscript with no op-regime references, so the entire analysis is
uncommitted, not merely a few stray files).

---

## 5. Investigation 3 — CHECKSUMS.sha256

48 lines = 7 comment/header lines + **41 entries**. `shasum -a 256 -c` on the working tree:
**41/41 OK, 0 failed.** Five entries point at currently-untracked or legacy artifacts:
```
line 15: data/processed/dili_genes_clean.csv            (tracked legacy orphan)
line 40-43: results/tables/operating_regime_{moments,plane,reversal,summary}.csv  (UNTRACKED)
```
So the manifest validates **only the current working tree**. On a HEAD checkout the four
op-regime tables are absent and verification fails. **Severity: minor (subsumed by §4).
codex_status: confirms_codex.**

---

## 6. Investigation 4 — submission_source.zip (Codex's "stale" hypothesis partly **contradicted**)

The **working-tree** zip is *current*, not stale. Byte-for-byte diff of extracted members vs
working source:
```
SAME: main.tex   SAME: sections/results.tex   SAME: sections/supplementary.tex
SAME: sections/methods.tex   SAME: references.bib   SAME pdf: figures/fig8_opregime.pdf
```
However the **HEAD-committed** zip is a *different, older* artifact: it contains **no**
`fig8_opregime` (count 0), an old `main.tex` (6835 B vs working 7723 B), old `results.tex`
(13472 B vs 17890 B), and lists `fig5_bootstrap.pdf` as a main figure. So:
- vs current source → zip is up to date (the "stale zip" worry is a **false alarm** for the working tree);
- vs HEAD → the tracked zip is part of the same uncommitted delta and embeds the untracked
  `fig8_opregime.pdf`.

**Severity: false_alarm (working tree) / minor. codex_status: contradicts_codex** on the
narrow "stale vs current source" framing; the embedding of untracked content is already
captured by §4.

---

## 7. Investigation 6 — data/processed/dili_genes_clean.csv (orphan, now **documented**)

Verified: 81 lines = header + **80 genes**; **IL18 and IL1R2 are absent** (`grep` → 0 matches).
The **active** DILI sets *do* contain them:
```
data/processed/dili_700_lcc.csv  (84 genes): IL1R2 @line69, IL18 @line70
data/processed/dili_900_lcc.csv  (82 genes): IL1R2 @line67, IL18 @line68
```
Sole consumer in the repo is documentation, not code:
```
DATA_MANIFEST.md:40  "Legacy curated DILI snapshot | No active manuscript consumer |
                      Retained and checksummed as a historical artifact; active analyses
                      use dili_700_lcc.csv and dili_900_lcc.csv."
```
So Codex's "unused orphan omitting IL18/IL1R2" is **confirmed numerically**, but with the
nuance that it is now **explicitly documented** as legacy in the (modified) DATA_MANIFEST —
it is documented-legacy, not an undocumented landmine. Residual risk: a reader could pick the
wrong DILI file. **Severity: minor. codex_status: confirms_codex (with documentation nuance).**

---

## 8. Investigation 5 — fig8 filenames vs manuscript numbering (no literal "Figure 8")

Figure environments in `manuscript/main.tex`, in render order → assigned number:
```
1  fig1_lollipop.pdf      -> Figure 1  (fig:context)
2  fig2_dumbbell.pdf      -> Figure 2  (fig:dumbbell)
3  fig8_opregime.pdf      -> Figure 3  (fig:opregime)   <- filename "fig8" != number 3
4  fig4_ptni_phase.pdf    -> Figure 4  (fig:efficiency)
5  fig3_ewi_waterfall.pdf -> Figure 5  (fig:ewi)
6  fig7_leakage.pdf       -> Figure 6  (fig:leakage)
7  fig6_chemsim.pdf       -> Figure 7  (fig:chemsim)
   fig5_bootstrap.pdf     -> Supplementary (supplementary.tex:30, fig:bootstrap)
```
Grep for the literal forms `Figure 8 / Fig. 8 / Fig 8 / Figure~8` across all `.tex`:
**no matches.** The manuscript's "must not say Figure 8" constraint is satisfied (figures are
referenced by `\ref{fig:opregime}` etc., not hard-coded numbers). The scrambled **filenames**
remain a real mispackaging/misreading hazard (e.g. someone hand-picks "fig8" expecting an 8th
figure). **Severity: minor / author_decision. codex_status: confirms_codex** (I add the full
filename→number permutation and independently confirm the absence of any literal "Figure 8").

---

## 9. Staged supplementary-figure deletions are clean (not a problem)

`figures/supplementary/{fig3_slope,fig7_ewi_comparison}.{pdf,tiff}` are staged for deletion;
the directory is now empty and `git ls-files figures/supplementary/` is empty. No
`\includegraphics` in any `.tex` references `figures/supplementary/` or those basenames (the
only "slope"/"comparison" hits are prose in captions). The current supplementary figure is
`figures/fig5_bootstrap.pdf` pulled from `manuscript/figures/`. **Clean stale-removal — no
finding.**

---

## 10. Challenge summary vs Codex AGENT_A

| Codex AGENT_A claim | My independent finding | Verdict |
|---|---|---|
| Untracked op-regime artifacts referenced by tracked manuscript | Confirmed + proved HEAD has 0 references (whole analysis uncommitted) | confirms, strengthened |
| LICENSE: MIT untracked while CC-BY staged → MIT claim unsupported | Confirmed; 3 metadata files assert MIT; LICENSE not gitignored | confirms |
| CHECKSUMS validates working tree not HEAD; references untracked tables | Confirmed: 41/41 OK working tree; 4 op-regime + 1 legacy entries | confirms |
| dili_genes_clean.csv orphan, no active consumer | Confirmed (80 genes, no IL18/IL1R2); but now **documented** legacy in DATA_MANIFEST | confirms w/ nuance |
| fig8_opregime = manuscript Figure 3 | Confirmed; full filename→number map; **no literal "Figure 8"** anywhere | confirms |
| (zip) "currently contains fig8_opregime.pdf" | Working-tree zip is byte-current vs source; **HEAD zip is the stale one** | refines/partly contradicts |
| Tracked count 173, untracked 20 | 173 tracked confirmed; untracked now 25 (added independent_validation reports) | confirms (count drift explained) |

No Codex AGENT_A conclusion was found to be fabricated; the one correction is the "stale zip"
framing (working-tree zip is actually current).

---

## 11. Verified numbers (independently recomputed, not table-read)

| Quantity | Method | Result |
|---|---|---|
| tracked files | `git ls-files \| wc -l` | 173 |
| untracked (excl ignored) | `git ls-files --others --exclude-standard \| wc -l` | 25 |
| CHECKSUMS entries / verify | `shasum -a 256 -c` | 41 entries, 41 OK, 0 fail |
| op-regime CSVs referenced by tracked code, untracked on disk | grep + ls-files | 4/4 untracked |
| HEAD references to operating_regime/fig8 | `git grep -l ... HEAD` | 0 |
| dili_genes_clean.csv genes / IL18,IL1R2 | `wc -l`, `grep` | 80 genes; absent |
| dili_700_lcc / dili_900_lcc genes / IL18,IL1R2 | `wc -l`, `grep` | 84 / 82; both present |
| submission_source.zip working vs source | extract + `diff` | identical (current) |
| submission_source.zip HEAD vs working | `git show HEAD:... \| unzip -l` | differs (no fig8, old tex) |

## 12. Unverified / out of scope for this track

- Numerical correctness of the operating-regime tables themselves (Tracks D/E).
- Parquet schema contents (binary inputs; checksummed only).
- Whether `docs/DATA_FLOW.md` fully covers the op-regime step (Codex flagged; not re-derived here).

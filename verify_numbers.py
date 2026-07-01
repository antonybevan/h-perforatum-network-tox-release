#!/usr/bin/env python3
"""
Honesty gate: automated number-consistency and forbidden-language check.

Verifies every headline number against the committed result tables, and scans
the revised manuscript + figure scripts for retracted claims / artefacts.
Exit 0 = PASS, exit 1 = FAIL. Run from repo root:  python verify_numbers.py
"""
import sys, re, glob
from pathlib import Path
import pandas as pd, numpy as np

ROOT = Path(__file__).resolve().parent
T = ROOT / "results" / "tables"
D = ROOT / "data" / "processed"
fail = []
def check(cond, msg):
    print(("  OK  " if cond else " FAIL ") + msg)
    if not cond: fail.append(msg)
def approx(a, b, tol=5e-3): return abs(float(a)-float(b)) <= tol
def read_text(path): return Path(path).read_text(errors="ignore")

print("="*72); print(" INPUTS / CURATION COUNTS"); print("="*72)
targets = pd.read_csv(D/"targets_lcc.csv")
dili9 = pd.read_csv(D/"dili_900_lcc.csv")
net9 = pd.read_parquet(D/"network_900_liver_lcc.parquet")
check((targets[targets.compound=="Hyperforin"].gene_symbol.nunique() == 10), "Hyperforin target count = 10")
check((targets[targets.compound=="Quercetin"].gene_symbol.nunique() == 62), "Quercetin target count = 62")
check((len(dili9) == 82), "DILI module has 82 genes in STRING >=900 liver LCC")
check((net9.shape[0] == 66908), "STRING >=900 liver LCC has 66,908 edges")
nodes9 = set(net9["gene1"]) | set(net9["gene2"])
check((len(nodes9) == 7677), "STRING >=900 liver LCC has 7,677 nodes")

print("="*72); print(" REPRODUCIBILITY ARTIFACTS"); print("="*72)
required_paths = [
    "requirements-lock.txt",
    "reproducibility.lock.yml",
    "data/CHECKSUMS.sha256",
    "scripts/run_pipeline.py",
    "scripts/run_operating_regime_benchmark.py",
    "scripts/run_string_textmining_sensitivity.py",
    "scripts/generate_dataflow.py",
    "docs/DATA_FLOW.md",
    "results/tables/string_textmining_sensitivity.csv",
    "RESPONSE_TO_REVIEWERS.md",
    "DATA_MANIFEST.md",
]
for rel in required_paths:
    check((ROOT/rel).exists(), f"{rel} exists")
lock_text = read_text(ROOT/"reproducibility.lock.yml")
check("Rscript R/fig8_opregime.R" in lock_text, "reproducibility lock includes operating-regime figure script")
repo_url = "https://github.com/antonybevan/h-perforatum-network-tox"
for rel in ["README.md", "CITATION.cff", "manuscript/sections/code_availability.tex", "manuscript/sections/data_availability.tex"]:
    check(repo_url in read_text(ROOT/rel), f"{rel} contains canonical GitHub URL")

print("="*72); print(" HEADLINE NUMBERS (committed result tables)"); print("="*72)
sp = pd.read_csv(T/"shortest_path_permutation_results.csv"); sp9 = sp[sp.network_threshold==900]
check(approx(sp9[sp9.compound=='Hyperforin'].observed_dc.iloc[0],1.30), "d_c Hyperforin (900) = 1.30")
check(approx(sp9[sp9.compound=='Quercetin'].observed_dc.iloc[0],1.677,1e-2), "d_c Quercetin (900) = 1.68")
check(approx(sp9[sp9.compound=='Hyperforin'].null_mean.iloc[0],2.21,1e-2), "null mean Hyperforin shortest path = 2.21")
check(approx(sp9[sp9.compound=='Quercetin'].null_mean.iloc[0],2.17,1e-2), "null mean Quercetin shortest path = 2.17")
check(approx(sp9[sp9.compound=='Hyperforin'].null_std.iloc[0],0.235,1e-3), "null SD Hyperforin shortest path = 0.235")
check(approx(sp9[sp9.compound=='Quercetin'].null_std.iloc[0],0.091,1e-3), "null SD Quercetin shortest path = 0.091")
check(approx(sp9[sp9.compound=='Hyperforin'].z_score.iloc[0],-3.86,1e-2), "proximity Z Hyperforin (900) = -3.86")
check(approx(sp9[sp9.compound=='Quercetin'].z_score.iloc[0],-5.44,1e-2), "proximity Z Quercetin (900) = -5.44")
sp7 = sp[sp.network_threshold==700]
check(approx(sp7[sp7.compound=='Hyperforin'].z_score.iloc[0],-6.04,1e-2), "proximity Z Hyperforin (700) = -6.04")
check(approx(sp7[sp7.compound=='Quercetin'].z_score.iloc[0],-5.46,1e-2), "proximity Z Quercetin (700) = -5.46")

rwr = pd.read_csv(T/"standard_rwr_lcc_permutation_results.csv"); rwr9 = rwr[rwr.network_threshold==900]
check(approx(rwr9[rwr9.compound=='Hyperforin'].observed_influence.iloc[0],0.1138,1e-3), "PE Hyperforin (900) = 0.1138")
check(approx(rwr9[rwr9.compound=='Quercetin'].observed_influence.iloc[0],0.0322,1e-3), "PE Quercetin (900) = 0.0322")

ewi = pd.read_csv(T/"expression_weighted_rwr_permutation_results.csv")
check(len(ewi)==4, "EWI table has 4 rows")

shrink = pd.read_csv(T/"null_variance_shrinkage_audit.csv")
ratios = shrink.std_ratio_hyperforin_over_quercetin
source_tables = {
    "Shortest_Path": sp,
    "RWR": rwr,
    "EWI": ewi,
}
for metric, source in source_tables.items():
    for threshold in [700, 900]:
        source_subset = source[source.network_threshold == threshold]
        h_std = float(source_subset[source_subset.compound == "Hyperforin"].null_std.iloc[0])
        q_std = float(source_subset[source_subset.compound == "Quercetin"].null_std.iloc[0])
        expected_ratio = h_std / q_std
        audit_ratio = float(shrink[
            (shrink.metric == metric) & (shrink.network_threshold == threshold)
        ].std_ratio_hyperforin_over_quercetin.iloc[0])
        check(
            approx(audit_ratio, expected_ratio, 1e-12),
            f"{metric} null-SD ratio at >={threshold} matches permutation table",
        )
check(((ratios>2.35)&(ratios<3.10)).all(), "null-SD ratios remain near sqrt(62/10)=2.49 (2.35-3.10)")
check(approx(shrink[(shrink.metric=="RWR") & (shrink.network_threshold==900)].std_ratio_hyperforin_over_quercetin.iloc[0],2.45,0.02), "RWR null-SD ratio at >=900 = 2.45")
check(approx(shrink[(shrink.metric=="EWI") & (shrink.network_threshold==900)].std_ratio_hyperforin_over_quercetin.iloc[0],2.47,0.02), "EWI null-SD ratio at >=900 = 2.47")

op_sum = pd.read_csv(T/"operating_regime_summary.csv").iloc[0]
op_rev = pd.read_csv(T/"operating_regime_reversal.csv")
op_mom = pd.read_csv(T/"operating_regime_moments.csv")
check(-0.51 < op_sum.slope_pinned < -0.49, "operating-regime null-SD slope ~ -0.50")
check(-0.504 < op_sum.slope_pinned_lo < -0.502 and -0.497 < op_sum.slope_pinned_hi < -0.495, "operating-regime slope CI matches manuscript")
check(op_sum.r2_pinned > 0.999, "operating-regime R^2 > 0.999")
check(approx(op_sum.slope_DILI, -0.495, 0.002), "DILI module slope ~= -0.495")
check(approx(op_sum.slope_pseudo_mean, -0.498, 0.002), "pseudo-module mean slope ~= -0.498")
check(approx(op_sum.real_margin, 0.3774193548387095, 1e-12), "operating-regime real margin is derived exactly from shortest-path table")
check(op_sum.real_small_compound == "Hyperforin" and op_sum.real_large_compound == "Quercetin", "operating-regime real pair labels are stored in summary")
check(int(op_sum.real_n_small) == 10 and int(op_sum.real_n_large) == 62, "operating-regime real pair target counts are stored in summary")
check(approx(op_sum.real_dc_small, 1.3, 1e-12) and approx(op_sum.real_dc_large, 1.6774193548387095, 1e-12), "operating-regime real d_c values are sourced from shortest-path table")
check(0.60 < op_sum.delta_max_real < 0.64, "operating-regime delta_max at exact R=6.2 is ~0.62")
check(89 < op_sum.located_percentile < 92, "H/Q margin percentile ~= 91st")
check(0.05 < op_sum.uncond_directional_reversal_real < 0.07, "operating-regime H/Q-directional reversal ~6%")
check(0.10 < op_sum.uncond_rank_discord_real < 0.14, "operating-regime bidirectional rank discordance ~12%")
check(int(op_sum.canonical_target_rows) == 72, "operating-regime uses all 72 compound-target rows for degree profile")
check(((op_rev.m_large == 62) & np.isclose(op_rev.R, 6.2)).any(), "operating-regime reversal table includes exact R=6.2 row")
check("uncond_discord" not in op_rev.columns, "operating-regime table has no ambiguous uncond_discord column")
expected_sizes = {5, 8, 10, 15, 20, 30, 40, 60, 62, 80}
check(set(op_mom[op_mom["mode"]=="pinned"].n_targets) == expected_sizes, "operating-regime moments include declared grid plus exact 62-target H/Q row")
row62 = op_rev[op_rev.m_large == 62].iloc[0]
row80 = op_rev[op_rev.m_large == 80].iloc[0]
check(0.0005 < row62["Rrev_d0.3"] < 0.0008, "conditional reversal at R=6.2, delta0=0.3 ~= 0.06%")
check(0.0035 < row80["Rrev_d0.3"] < 0.0045, "conditional reversal at R=8, delta0=0.3 ~= 0.39%")
check((op_rev["Rrev_d0.5"] == 0).all(), "conditional reversal at delta0=0.5 is 0% in all rows")
check((op_rev["Rrev_d0.3_noshrink"] == 0).all() and (op_rev["Rrev_d0.5_noshrink"] == 0).all(), "no-shrinkage counterfactual is 0%")

print("\n"+"="*72); print(" LEAKAGE / CHEMICAL-SIMILARITY TABLES"); print("="*72)
leak = pd.read_csv(T/"leakage_decomposition.csv").set_index("compound")
check(approx(leak.loc["Hyperforin","direct"],0.0711,1e-3), "Hyperforin direct-overlap component = 0.0711")
check(approx(leak.loc["Quercetin","direct"],0.0032,1e-3), "Quercetin direct-overlap component = 0.0032")
check(approx(leak.loc["Hyperforin","propagated"],0.0427,1e-3), "Hyperforin propagated component = 0.0427")
check(approx(leak.loc["Quercetin","propagated"],0.0290,1e-3), "Quercetin propagated component = 0.0290")
check(approx(leak.loc["Hyperforin","raw"]/leak.loc["Quercetin","raw"],3.5,0.1), "raw PE ratio ~= 3.5")
check(approx(leak.loc["Hyperforin","propagated"]/leak.loc["Quercetin","propagated"],1.47,0.03), "propagated ratio ~= 1.5")
check(approx(leak.loc["Hyperforin","direct"]/leak.loc["Hyperforin","raw"],0.625,0.02), "Hyperforin direct-overlap fraction ~= 62%")
leak_null = pd.read_csv(ROOT/"results"/"leakage_null_distributions.csv")
bg = leak_null[leak_null.distribution == "background"].loo_influence
hyp_prop = leak.loc["Hyperforin", "propagated"]
check(len(bg) == 1000, "leakage background distribution has n=1000")
check(approx(bg.mean(), 0.0130, 5e-4), "leakage background null mean ~= 0.0130")
check(approx(bg.quantile(0.95), 0.0281, 5e-4), "leakage background 95th percentile ~= 0.0281")
check(approx(bg.max(), 0.0580, 5e-4), "leakage background max ~= 0.0580")
check(approx((np.sum(bg >= hyp_prop) + 1) / (len(bg) + 1), 0.0020, 5e-4), "leakage propagated empirical p ~= 0.002")
dlmod = pd.read_csv(T/"dili_module_sensitivity.csv")
check(approx(dlmod[dlmod.n_dili_genes==78].ratio.iloc[0],1.58,0.02), "DILI-module sensitivity ratio after overlap-gene removal ~= 1.58")
chemsim = pd.read_csv(T/"chemical_similarity_summary.csv")
check("structural_analog_to_dilirank_positive" in chemsim.columns, "chemical-similarity summary uses scoped DILIrank-positive column name")
check((chemsim.max_sim_DILI_positive < 0.4).all(), "DILI-positive max Tanimoto values are <0.4")
ref = pd.read_csv(T/"dilirank_reference_set.csv")
check((ref.category.value_counts().get("DILI_positive",0) == 542), "retrievable DILI-positive reference count = 542")
check((ref.category.value_counts().get("DILI_negative",0) == 365), "retrievable DILI-negative reference count = 365")
dilirank = pd.read_excel(ROOT/"data"/"external"/"DILIrank_2.0.xlsx", skiprows=1)
cats = dilirank["vDILI-Concern"].str.lower().str.strip().value_counts()
check(int(cats.get("vmost-dili-concern",0)) == 217, "DILIrank 2.0 vMost count = 217")
check(int(cats.get("vless-dili-concern",0)) == 351, "DILIrank 2.0 vLess count = 351")
check(int(cats.get("vno-dili-concern",0)) == 414, "DILIrank 2.0 vNo count = 414")
check(int(cats.get("ambiguous-dili-concern",0)) == 354, "DILIrank 2.0 ambiguous count = 354")

print("\n"+"="*72); print(" P-VALUE CONVENTION (no 1e-16; empirical floor 1/1001)"); print("="*72)
for fn in ["shortest_path_permutation_results.csv","standard_rwr_lcc_permutation_results.csv",
           "expression_weighted_rwr_permutation_results.csv"]:
    df = pd.read_csv(T/fn)
    check((df.p_value >= 1/1001 - 1e-9).all(), f"{fn}: all p >= 1/1001 (no 1e-16)")

print("\n"+"="*72); print(" EFFICIENCY DEFINITION (E = I, not I/|T|)"); print("="*72)
cons = pd.read_csv(T/"consolidated_results.csv")
rwi_rows = cons[cons.metric=="RWI"]
for _,r in rwi_rows.iterrows():
    check(approx(r["observed"], r["efficiency"]), f"consolidated: efficiency == observed for {r['compound']} (E=I)")

print("\n"+"="*72); print(" MANUSCRIPT HEADLINE TEXT"); print("="*72)
manuscript_text = "\n".join(read_text(p) for p in [ROOT/"manuscript/main.tex", *sorted((ROOT/"manuscript/sections").glob("*.tex"))])
for literal, label in [
    ("10 targets", "10 targets stated"),
    ("62 targets", "62 targets stated"),
    ("82-gene DILI", "82-gene DILI stated"),
    ("$d_c = 1.30$ vs $1.68$", "dc values stated"),
    ("$-3.86$ vs $-5.44$", "proximity Z values stated"),
    ("$E = 0.1138$ for Hyperforin and $0.0322$ for Quercetin", "PE values stated"),
    ("$0.0427$ versus $0.0290$", "propagated values stated"),
    ("Hyperforin $Z = -4.09$, Quercetin $Z = -5.34$", "Guney fixed-disease values stated"),
    ("Hyperforin $Z = -3.55$, Quercetin $Z = -3.66$", "Guney two-sided values stated"),
    ("2.45--3.04 for random-walk influence", "RWR null-SD ratio range stated"),
    ("2.47--2.93 for expression-weighted influence", "EWI null-SD ratio range stated"),
    ("2.90 at $\\alpha=0.10$ to 13.35 at $\\alpha=0.70$", "alpha sweep endpoints stated"),
    ("2.69--2.70 across floors", "expression floor range stated"),
]:
    check(literal in manuscript_text, label)

print("\n"+"="*72); print(" FORBIDDEN LANGUAGE / ARTEFACTS in revised manuscript + figures"); print("="*72)
# Scan active manuscript, code, and review-facing docs. Generated LaTeX aux/log
# files and this gate itself are excluded to avoid matching the forbidden-pattern
# definitions rather than the manuscript/package surface.
scan_files = (
    [str(ROOT/"README.md"), str(ROOT/"CITATION.cff"), str(ROOT/"DATA_MANIFEST.md"),
     str(ROOT/"DATA_PROVENANCE.md"), str(ROOT/"RESPONSE_TO_REVIEWERS.md"),
     str(ROOT/"GUNEY_FIDELITY_REVALIDATION.md"), str(ROOT/"reproducibility.lock.yml")]
    + glob.glob(str(ROOT/"docs/*.md"))
    + glob.glob(str(ROOT/"manuscript/*.tex"))
    + glob.glob(str(ROOT/"manuscript/sections/*.tex"))
    + glob.glob(str(ROOT/"R/*.R"))
    + glob.glob(str(ROOT/"scripts/*.py"))
    + glob.glob(str(ROOT/"src/**/*.py"), recursive=True)
    + glob.glob(str(ROOT/"tests/*.py"))
)
forbidden = [
    (r"1e-?16", "literal 1e-16"),
    (r"known hepatotoxin", "'known hepatotoxin'"),
    (r"less susceptible", "'less susceptible' (RWR variance claim)"),
    (r"less severe shrinkage", "'less severe shrinkage'"),
    (r"unbiased comparison", "'unbiased comparison'"),
    (r"resolves target-count bias", "'resolves target-count bias'"),
    (r"systematic bias", "'systematic bias'"),
    (r"artificially inflated", "'artificially inflated'"),
    (r"artificial inflation", "'artificial inflation'"),
    (r"clean biological ground truth", "'clean biological ground truth'"),
    (r"no Quercetin subset", "'no Quercetin subset matched'"),
    (r"human PPIs", "'human PPIs' (physical-PPI framing)"),
    (r"Human PPI|STRING PPI|protein-protein interactions", "unqualified physical-PPI wording"),
    (r"physically closer", "'physically closer' (STRING is functional association)"),
    (r"module-invariant", "'module-invariant'"),
    (r"bias-corrected", "'bias-corrected'"),
    (r"best-case selection", "'best-case selection'"),
    (r"representative compounds", "'representative compounds'"),
    (r"DILI predictor", "'DILI predictor'"),
    (r"DILI classifier", "'DILI classifier'"),
    (r"hepatotoxins", "'hepatotoxins' broad chemical-control wording"),
    (r"Eq\. 75|Eq\. 81", "broken equation reference artefact"),
    (r"z=\+8\.83", "stale z=+8.83"),
    (r"Fig\. 8|Figure 8", "stale final figure numbering for operating-regime figure"),
    (r"\[CONSTRAINT ANALYSIS\]|\[CORE INFERENCE\]|\[DESCRIPTIVE CONTEXT\]|\[ROBUSTNESS CONTROL\]|\[ORTHOGONAL EXCLUSION\]", "AI caption tag"),
    (r"Influence\s*/\s*Targets|RWI_Influence\s*/\s*Targets", "I/|T| double-normalisation"),
]
def affirmative_two_tailed(txt):
    # Flag 'two-tailed' only in affirmative use; allow 'no/not ... two-tailed'
    # and the canonical "two-sided null" wording.
    out = []
    for m in re.finditer(r"two-tailed(?: test)?", txt, flags=re.IGNORECASE):
        pre = txt[max(0, m.start()-5):m.start()].lower()
        if pre.endswith("no ") or pre.endswith("not "):
            continue
        out.append(m)
    return out
def zero_pvalue_hits(txt):
    return re.findall(r"p\s*=\s*0(?:[^\.\d]|$)|p=0(?:[^\.\d]|$)", txt, flags=re.IGNORECASE)
for f in scan_files:
    txt = Path(f).read_text(errors="ignore")
    for pat,label in forbidden:
        hits = re.findall(pat, txt, flags=re.IGNORECASE)
        check(len(hits)==0, f"{Path(f).name}: free of {label}")
    check(len(affirmative_two_tailed(txt))==0, f"{Path(f).name}: free of affirmative 'two-tailed' (proximity is directional)")
    check(len(zero_pvalue_hits(txt))==0, f"{Path(f).name}: free of zero p-value display")

print("\n"+"="*72)
if fail:
    print(f" RESULT: FAIL ({len(fail)} issue(s))"); [print("   - "+m) for m in fail]; sys.exit(1)
print(" RESULT: PASS — all headline numbers consistent; no retracted claims present"); sys.exit(0)

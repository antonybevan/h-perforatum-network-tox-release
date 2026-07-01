#!/usr/bin/env python3
"""Regenerate the descriptive supplementary numbers (DILI list, curation counts,
null-SD-by-metric, direct-DILI connectivity) from committed data. Read-only."""
import sys
sys.path.insert(0, 'src')
import pandas as pd
import networkx as nx

D = 'data/processed/'
RAW = 'data/raw/'
G = nx.from_pandas_edgelist(pd.read_parquet(D + 'network_900_liver_lcc.parquet'), 'gene1', 'gene2')
t_lcc = pd.read_csv(D + 'targets_lcc.csv')
hyp = sorted(set(t_lcc[t_lcc.compound == 'Hyperforin'].gene_symbol) & set(G))
quer = sorted(set(t_lcc[t_lcc.compound == 'Quercetin'].gene_symbol) & set(G))
dili = sorted(set(pd.read_csv(D + 'dili_900_lcc.csv').gene_name) & set(G))
dset = set(dili)

print("=" * 70)
print("[#2] DILI gene set (>=900 liver LCC):", len(dili), "genes")
print("  " + " ".join(dili))

print("\n" + "=" * 70)
print("[#3] Curation provenance (verifiable stage counts)")
def cc(path, comp=None, col=None):
    df = pd.read_csv(path)
    if comp:
        c = 'compound' if 'compound' in df.columns else None
        gc = col or next((x for x in ['gene_symbol', 'gene_name', 'gene', 'protein_id'] if x in df.columns), df.columns[0])
        return df[df[c] == comp][gc].nunique() if c else len(df)
    return len(df)
print(f"  Quercetin: raw(targets_raw)={cc(RAW+'targets_raw.csv','Quercetin')} "
      f"processed(targets)={cc(D+'targets.csv','Quercetin')} LCC={len(quer)}")
print(f"  Hyperforin: raw={cc(RAW+'targets_raw.csv','Hyperforin')} "
      f"processed={cc(D+'targets.csv','Hyperforin')} LCC={len(hyp)}")
print(f"  DILI: raw(dili_genes_raw)={cc(RAW+'dili_genes_raw.csv')} "
      f">=700 LCC={cc(D+'dili_700_lcc.csv')} >=900 LCC={len(dili)}")

print("\n" + "=" * 70)
print("[#1] Null-SD by metric (from committed permutation tables, >=900)")
for fn, vcol in [('shortest_path_permutation_results.csv', 'observed_dc'),
                 ('standard_rwr_lcc_permutation_results.csv', 'observed_influence'),
                 ('expression_weighted_rwr_permutation_results.csv', 'observed_influence')]:
    df = pd.read_csv('results/tables/' + fn)
    df = df[df.network_threshold == 900]
    h = df[df.compound == 'Hyperforin'].iloc[0]
    q = df[df.compound == 'Quercetin'].iloc[0]
    ratio = h.null_std / q.null_std
    print(f"  {fn.split('_')[0]:12s}: Hyp sigma={h.null_std:.4f} Quer sigma={q.null_std:.4f} "
          f"ratio={ratio:.2f}  (mu_H={h.null_mean:.4f} mu_Q={q.null_mean:.4f}; "
          f"Z_H={h.z_score:+.2f} Z_Q={q.z_score:+.2f})")
print(f"  expected sqrt(62/10) = {(62/10)**0.5:.2f}")

print("\n" + "=" * 70)
print("[#4] Direct (distance-1) DILI connectivity (REGENERATED on >=900 LCC)")
def dili_neighbors(node):
    return sorted(set(G.neighbors(node)) & dset - {node})
for name, tgts in [('Hyperforin', hyp), ('Quercetin', quer)]:
    per = {g: dili_neighbors(g) for g in tgts}
    total = sum(len(v) for v in per.values())
    withone = sum(1 for v in per.values() if v)
    print(f"  {name}: targets={len(tgts)}  with>=1 DILI-neighbor={withone}  "
          f"total connections={total}  mean per target={total/len(tgts):.2f}")
print("\n  Per-Hyperforin-target DILI neighbours:")
for g in hyp:
    nb = dili_neighbors(g)
    print(f"    {g:8s} ({len(nb)}): {', '.join(nb) if nb else '-'}")

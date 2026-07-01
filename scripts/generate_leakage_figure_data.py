#!/usr/bin/env python3
"""Generate data for the direct-vs-propagated leakage figure.

Reproducible from the committed STRING>=900 liver LCC. Writes:
  results/tables/leakage_decomposition.csv  -- raw/direct/propagated E per compound
  results/leakage_null_distributions.csv    -- LOO influence for a degree-matched
                                               10-gene background and Quercetin 10-subsets
All randomisation is seeded (42); uses the repo's own RWR.
"""
import sys
sys.path.insert(0, 'src')
import numpy as np
import pandas as pd
import networkx as nx
from network_tox.analysis.rwr import run_rwr
from network_tox.core.permutation import get_degree_matched_random

D = 'data/processed/'
G = nx.from_pandas_edgelist(pd.read_parquet(D + 'network_900_liver_lcc.parquet'), 'gene1', 'gene2')
t = pd.read_csv(D + 'targets_lcc.csv')
hyp = sorted(set(t[t.compound == 'Hyperforin'].gene_symbol) & set(G))
quer = sorted(set(t[t.compound == 'Quercetin'].gene_symbol) & set(G))
dl = [g for g in pd.read_csv(D + 'dili_900_lcc.csv').gene_name if g in G]


def E(T):                       # raw influence on the DILI module
    s = run_rwr(G, T, restart_prob=0.15)
    return sum(s.get(g, 0.0) for g in dl)


def Eself(T):                   # leave-one-out / propagated influence
    s = run_rwr(G, T, restart_prob=0.15)
    ex = set(T)
    return sum(s.get(g, 0.0) for g in dl if g not in ex)


# 1) direct vs propagated decomposition
rows = []
for nm, T in [('Hyperforin', hyp), ('Quercetin', quer)]:
    raw, prop = E(T), Eself(T)
    rows.append({'compound': nm, 'raw': raw, 'direct': raw - prop, 'propagated': prop})
dec = pd.DataFrame(rows)
dec.to_csv('results/tables/leakage_decomposition.csv', index=False)

# 2) null distributions of the propagated (LOO) component
N = 1000
np.random.seed(42)
bg = []
for i in range(N):
    rt = get_degree_matched_random(G, hyp, len(hyp), seed=1000 + i)
    if rt:
        bg.append(Eself(rt))
rng = np.random.default_rng(42)
qs = [Eself(list(rng.choice(quer, size=len(hyp), replace=False))) for _ in range(N)]
pd.DataFrame({'distribution': ['background'] * len(bg) + ['quercetin_subset'] * len(qs),
             'loo_influence': bg + qs}).to_csv('results/leakage_null_distributions.csv', index=False)

print(dec.to_string(index=False))
hyp_obs = dec[dec.compound == 'Hyperforin'].propagated.iloc[0]
print(f"\nbackground (n={len(bg)}): mean={np.mean(bg):.5f}  95th={np.quantile(bg, .95):.5f}  99th={np.quantile(bg, .99):.5f}")
print(f"quercetin subsets (n={len(qs)}): mean={np.mean(qs):.5f}  max={np.max(qs):.5f}")
print(f"Hyperforin propagated (observed) = {hyp_obs:.5f}; "
      f"percentile vs background = {100 * np.mean(np.array(bg) < hyp_obs):.1f}")
